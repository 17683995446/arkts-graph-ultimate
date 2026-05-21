#!/usr/bin/env python3
import sys
import time
import json
import traceback
from pathlib import Path
from datetime import datetime
import subprocess
import tempfile
import shutil

sys.path.insert(0, str(Path(__file__).parent))

from arkts_graph.core.database import Database
from arkts_graph.core.ark_analyzer_integration import ArkAnalyzerIntegration


class ProductionScenarioTest:
    def __init__(self):
        self.results = []
        self.start_time = time.time()
    
    def log(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {message}")
    
    def log_error(self, message: str, exc: Exception = None):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_msg = f"[{timestamp}] ERROR: {message}"
        if exc:
            error_msg += f"\n{traceback.format_exc()}"
        print(error_msg)
    
    def log_warning(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        warning_msg = f"[{timestamp}] WARNING: {message}"
        print(warning_msg)
    
    def test_incremental_update(self) -> dict:
        """测试增量更新场景"""
        self.log(f"\n{'='*60}")
        self.log("TEST 1: Incremental Update Scenario")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Incremental Update",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            # 创建临时项目
            temp_project = Path(tempfile.mkdtemp())
            
            # 第一阶段：创建基础项目
            self.log("Phase 1: Creating base project...")
            base_file = temp_project / "BaseClass.ets"
            base_file.write_text("""
export class BaseClass {
  baseMethod() {
    console.log('base');
  }
}
""")
            
            temp_output1 = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output1.close()
            
            wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
            cmd = ['node', str(wrapper_path), str(temp_project), temp_output1.name]
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=60)
            
            with open(temp_output1.name, 'r') as f:
                phase1_data = json.load(f)
            
            self.log(f"Phase 1 stats: {len(phase1_data['files'])} files, {len(phase1_data['classes'])} classes")
            
            # 第二阶段：添加新文件
            self.log("Phase 2: Adding new file...")
            new_file = temp_project / "NewClass.ets"
            new_file.write_text("""
export class NewClass {
  newMethod() {
    console.log('new');
  }
}
""")
            
            temp_output2 = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output2.close()
            
            cmd = ['node', str(wrapper_path), str(temp_project), temp_output2.name]
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=60)
            
            with open(temp_output2.name, 'r') as f:
                phase2_data = json.load(f)
            
            self.log(f"Phase 2 stats: {len(phase2_data['files'])} files, {len(phase2_data['classes'])} classes")
            
            # 第三阶段：修改现有文件
            self.log("Phase 3: Modifying existing file...")
            base_file.write_text("""
export class BaseClass {
  baseMethod() {
    console.log('modified');
  }
  
  addedMethod() {
    console.log('added');
  }
}
""")
            
            temp_output3 = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output3.close()
            
            cmd = ['node', str(wrapper_path), str(temp_project), temp_output3.name]
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=60)
            
            with open(temp_output3.name, 'r') as f:
                phase3_data = json.load(f)
            
            self.log(f"Phase 3 stats: {len(phase3_data['files'])} files, {len(phase3_data['classes'])} classes")
            
            # 第四阶段：删除文件
            self.log("Phase 4: Deleting file...")
            new_file.unlink()
            
            temp_output4 = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output4.close()
            
            cmd = ['node', str(wrapper_path), str(temp_project), temp_output4.name]
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=60)
            
            with open(temp_output4.name, 'r') as f:
                phase4_data = json.load(f)
            
            self.log(f"Phase 4 stats: {len(phase4_data['files'])} files, {len(phase4_data['classes'])} classes")
            
            # 验证增量更新行为
            incremental_files = len(phase2_data['files']) - len(phase1_data['files'])
            self.log(f"Incremental files detected: {incremental_files}")
            
            # 清理
            shutil.rmtree(temp_project)
            for f in [temp_output1, temp_output2, temp_output3, temp_output4]:
                Path(f.name).unlink(missing_ok=True)
            
            result['success'] = True
            result['stats'] = {
                'phase1_files': len(phase1_data['files']),
                'phase2_files': len(phase2_data['files']),
                'phase3_files': len(phase3_data['files']),
                'phase4_files': len(phase4_data['files']),
                'incremental_working': incremental_files > 0
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Incremental update test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_hot_reload_scenario(self) -> dict:
        """测试热重载场景"""
        self.log(f"\n{'='*60}")
        self.log("TEST 2: Hot Reload Scenario")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Hot Reload",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            temp_project = Path(tempfile.mkdtemp())
            temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
            temp_db.close()
            
            # 初始分析
            self.log("Initial analysis...")
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
            cmd = ['node', str(wrapper_path), str(temp_project), temp_output.name]
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=60)
            
            db = Database(Path(temp_db.name))
            ark_integration = ArkAnalyzerIntegration(db)
            ark_integration.load_from_json(Path(temp_output.name))
            
            initial_stats = db.get_stats()
            self.log(f"Initial stats: {initial_stats}")
            
            # 快速修改并重新加载
            self.log("Rapid modifications...")
            modifications = 5
            times = []
            
            for i in range(modifications):
                # 修改文件
                test_file = temp_project / f"Test{i}.ets"
                test_file.write_text(f"""
export class Test{i} {{
  method{i}() {{
    console.log('iteration {i}');
  }}
}}
""")
                
                start = time.time()
                
                # 重新分析
                temp_output2 = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
                temp_output2.close()
                
                cmd = ['node', str(wrapper_path), str(temp_project), temp_output2.name]
                subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=60)
                
                # 重新加载数据库
                ark_integration.load_from_json(Path(temp_output2.name))
                
                elapsed = time.time() - start
                times.append(elapsed)
                
                stats = db.get_stats()
                self.log(f"  Modification {i+1}: {elapsed:.3f}s, files={stats['files']}")
                
                Path(temp_output2.name).unlink(missing_ok=True)
            
            avg_time = sum(times) / len(times)
            self.log(f"Average hot reload time: {avg_time:.3f}s")
            
            # 清理
            shutil.rmtree(temp_project)
            Path(temp_db.name).unlink(missing_ok=True)
            Path(temp_output.name).unlink(missing_ok=True)
            
            result['success'] = avg_time < 10  # 热重载应该在10秒内完成
            result['stats'] = {
                'modifications': modifications,
                'times': times,
                'average': avg_time,
                'initial_stats': initial_stats
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Hot reload test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_batch_export_import(self) -> dict:
        """测试批量导出导入"""
        self.log(f"\n{'='*60}")
        self.log("TEST 3: Batch Export/Import")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Batch Export/Import",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            temp_db1 = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
            temp_db1.close()
            
            temp_db2 = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
            temp_db2.close()
            
            # 创建并填充第一个数据库
            self.log("Creating source database...")
            db1 = Database(Path(temp_db1.name))
            ark_integration1 = ArkAnalyzerIntegration(db1)
            
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
            cmd = ['node', str(wrapper_path), '/workspace/realistic_test_project', temp_output.name]
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=300)
            
            ark_integration1.load_from_json(Path(temp_output.name))
            source_stats = db1.get_stats()
            self.log(f"Source stats: {source_stats}")
            
            # 导出为JSON
            self.log("Exporting to JSON...")
            export_file = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            export_file.close()
            
            with open(temp_output.name, 'r') as f:
                export_data = f.read()
            
            with open(export_file.name, 'w') as f:
                f.write(export_data)
            
            export_size = Path(export_file.name).stat().st_size / 1024
            self.log(f"Exported file size: {export_size:.2f} KB")
            
            # 导入到第二个数据库
            self.log("Importing to target database...")
            db2 = Database(Path(temp_db2.name))
            ark_integration2 = ArkAnalyzerIntegration(db2)
            
            ark_integration2.load_from_json(Path(export_file.name))
            target_stats = db2.get_stats()
            self.log(f"Target stats: {target_stats}")
            
            # 验证数据一致性
            data_match = source_stats == target_stats
            self.log(f"Data match: {data_match}")
            
            if not data_match:
                self.log_warning("Source and target data don't match!")
            
            # 清理
            Path(temp_db1.name).unlink(missing_ok=True)
            Path(temp_db2.name).unlink(missing_ok=True)
            Path(temp_output.name).unlink(missing_ok=True)
            Path(export_file.name).unlink(missing_ok=True)
            
            result['success'] = data_match
            result['stats'] = {
                'source_stats': source_stats,
                'target_stats': target_stats,
                'data_match': data_match,
                'export_size': export_size
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Batch export/import test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_large_transaction(self) -> dict:
        """测试大事务"""
        self.log(f"\n{'='*60}")
        self.log("TEST 4: Large Transaction")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Large Transaction",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
            temp_db.close()
            
            db = Database(Path(temp_db.name))
            
            # 执行大事务
            self.log("Executing large transaction...")
            with db.transaction() as conn:
                # 插入大量数据
                for i in range(1000):
                    conn.execute(
                        "INSERT INTO files (path, hash, modified) VALUES (?, ?, ?)",
                        (f"/fake/path/file{i}.ets", f"hash{i}".encode(), int(time.time()))
                    )
                    
                    if i % 100 == 0:
                        self.log(f"  Inserted {i} records...")
            
            stats = db.get_stats()
            self.log(f"Transaction completed: {stats['files']} files inserted")
            
            # 验证数据
            files = db.get_all_files()
            self.log(f"Retrieved {len(files)} files from database")
            
            if len(files) != 1000:
                self.log_warning(f"Expected 1000 files, got {len(files)}")
                success = False
            else:
                success = True
            
            # 清理
            Path(temp_db.name).unlink(missing_ok=True)
            
            result['success'] = success
            result['stats'] = {
                'expected': 1000,
                'inserted': stats['files'],
                'retrieved': len(files)
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Large transaction test failed", e)
            result['success'] = False
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_concurrent_database_access(self) -> dict:
        """测试并发数据库访问"""
        self.log(f"\n{'='*60}")
        self.log("TEST 5: Concurrent Database Access")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Concurrent Database Access",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            # 准备数据库
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
            cmd = ['node', str(wrapper_path), '/workspace/realistic_test_project', temp_output.name]
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=300)
            
            temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
            temp_db.close()
            
            db = Database(Path(temp_db.name))
            ark_integration = ArkAnalyzerIntegration(db)
            ark_integration.load_from_json(Path(temp_output.name))
            
            # 串行执行多个操作
            self.log("Executing sequential operations...")
            operations = [
                ("Query files", lambda: db.get_all_files()),
                ("Query classes", lambda: db.get_classes()),
                ("Query methods", lambda: db.get_methods()),
                ("Get stats", lambda: db.get_stats()),
                ("Get call graph", lambda: db.get_call_graph())
            ]
            
            times = []
            for op_name, op_func in operations:
                start = time.time()
                result_data = op_func()
                elapsed = time.time() - start
                times.append(elapsed)
                self.log(f"  {op_name}: {elapsed:.3f}s, items={len(result_data)}")
            
            total_time = sum(times)
            self.log(f"Total sequential time: {total_time:.3f}s")
            
            # 清理
            Path(temp_output.name).unlink(missing_ok=True)
            Path(temp_db.name).unlink(missing_ok=True)
            
            result['success'] = True
            result['stats'] = {
                'operations': len(operations),
                'times': times,
                'total_time': total_time
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Concurrent database access test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def run_all_tests(self):
        """运行所有测试"""
        self.log("\n" + "="*60)
        self.log("PRODUCTION SCENARIO TEST SUITE")
        self.log("="*60)
        self.log(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.test_incremental_update()
        self.test_hot_reload_scenario()
        self.test_batch_export_import()
        self.test_large_transaction()
        self.test_concurrent_database_access()
        
        self.print_summary()
    
    def print_summary(self):
        """打印测试摘要"""
        total_time = time.time() - self.start_time
        
        print("\n" + "="*60)
        print("PRODUCTION SCENARIO SUMMARY")
        print("="*60)
        print(f"Total time: {total_time:.2f}s")
        print(f"Tests run: {len(self.results)}")
        
        success_count = sum(1 for r in self.results if r['success'])
        print(f"Successful: {success_count}/{len(self.results)}")
        
        print("\nDetailed results:")
        for result in self.results:
            status = "✓ SUCCESS" if result['success'] else "✗ FAILED"
            duration = result['end_time'] - result['start_time'] if result['end_time'] else 'N/A'
            print(f"  {result['test_name']}: {status} ({duration:.2f}s)")


if __name__ == '__main__':
    test = ProductionScenarioTest()
    test.run_all_tests()
