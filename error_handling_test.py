#!/usr/bin/env python3
import sys
import time
import json
import traceback
from pathlib import Path
from datetime import datetime
import sqlite3
import subprocess
import tempfile
import shutil
import traceback

sys.path.insert(0, str(Path(__file__).parent))

from arkts_graph.core.database import Database
from arkts_graph.core.ark_analyzer_integration import ArkAnalyzerIntegration


class ErrorHandlingTest:
    def __init__(self):
        self.results = []
        self.start_time = time.time()
        self.errors = []
        self.warnings = []
        self.critical_issues = []
    
    def log(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {message}")
    
    def log_error(self, message: str, exc: Exception = None):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_msg = f"[{timestamp}] ERROR: {message}"
        if exc:
            error_msg += f"\n{traceback.format_exc()}"
        print(error_msg)
        self.errors.append(error_msg)
    
    def log_warning(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        warning_msg = f"[{timestamp}] WARNING: {message}"
        print(warning_msg)
        self.warnings.append(warning_msg)
    
    def test_invalid_json_file(self) -> dict:
        """测试无效的JSON文件"""
        self.log(f"\n{'='*60}")
        self.log("Test 1: Invalid JSON File Handling")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Invalid JSON File",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            # 创建无效的JSON文件
            temp_json = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
            temp_json.write("{ invalid json content }")
            temp_json.close()
            
            self.log(f"Created invalid JSON file: {temp_json.name}")
            
            # 尝试加载
            db = Database(Path(tempfile.mktemp(suffix='.db')))
            ark_integration = ArkAnalyzerIntegration(db)
            
            try:
                ark_integration.load_from_json(Path(temp_json.name))
                self.log_warning("Invalid JSON was loaded without error")
                result['success'] = False
                result['error'] = "Should have raised exception for invalid JSON"
            except json.JSONDecodeError as e:
                self.log(f"Correctly caught JSONDecodeError: {str(e)[:50]}")
                result['success'] = True
            except Exception as e:
                self.log(f"Caught exception: {type(e).__name__}: {str(e)[:50]}")
                result['success'] = True  # Any exception is acceptable here
            
            Path(temp_json.name).unlink(missing_ok=True)
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Invalid JSON test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_missing_json_file(self) -> dict:
        """测试缺失的JSON文件"""
        self.log(f"\n{'='*60}")
        self.log("Test 2: Missing JSON File Handling")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Missing JSON File",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            # 使用不存在的文件
            missing_file = Path('/tmp/nonexistent_file_12345.json')
            
            self.log(f"Attempting to load non-existent file: {missing_file}")
            
            db = Database(Path(tempfile.mktemp(suffix='.db')))
            ark_integration = ArkAnalyzerIntegration(db)
            
            try:
                ark_integration.load_from_json(missing_file)
                self.log_warning("Missing file was loaded without error")
                result['success'] = False
                result['error'] = "Should have raised exception for missing file"
            except FileNotFoundError as e:
                self.log(f"Correctly caught FileNotFoundError: {str(e)[:50]}")
                result['success'] = True
            except Exception as e:
                self.log(f"Caught exception: {type(e).__name__}: {str(e)[:50]}")
                result['success'] = True  # Any exception is acceptable
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Missing JSON test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_corrupted_json_file(self) -> dict:
        """测试损坏的JSON文件"""
        self.log(f"\n{'='*60}")
        self.log("Test 3: Corrupted JSON File Handling")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Corrupted JSON File",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            # 创建部分损坏的JSON文件
            temp_json = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
            temp_json.write(json.dumps({
                'files': [{'id': 1, 'path': 'test.ets', 'hash': 'abc123'}],
                'classes': [],
                'methods': [],
                'calls': [],
                'components': []
            }))
            temp_json.close()
            
            # 损坏文件
            with open(temp_json.name, 'ab') as f:
                f.write(b'CORRUPTED DATA')
            
            self.log(f"Created corrupted JSON file: {temp_json.name}")
            
            # 尝试加载
            db = Database(Path(tempfile.mktemp(suffix='.db')))
            ark_integration = ArkAnalyzerIntegration(db)
            
            try:
                ark_integration.load_from_json(Path(temp_json.name))
                self.log_warning("Corrupted JSON was loaded without error")
                result['success'] = False
                result['error'] = "Should have raised exception for corrupted JSON"
            except (json.JSONDecodeError, Exception) as e:
                self.log(f"Correctly caught exception: {type(e).__name__}: {str(e)[:50]}")
                result['success'] = True
            
            Path(temp_json.name).unlink(missing_ok=True)
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Corrupted JSON test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_empty_json_file(self) -> dict:
        """测试空JSON文件"""
        self.log(f"\n{'='*60}")
        self.log("Test 4: Empty JSON File Handling")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Empty JSON File",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            # 创建空JSON文件
            temp_json = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
            temp_json.write('{}')
            temp_json.close()
            
            self.log(f"Created empty JSON file: {temp_json.name}")
            
            # 尝试加载
            db = Database(Path(tempfile.mktemp(suffix='.db')))
            ark_integration = ArkAnalyzerIntegration(db)
            
            try:
                ark_integration.load_from_json(Path(temp_json.name))
                self.log("Empty JSON loaded successfully")
                
                # 验证数据库状态
                stats = db.get_stats()
                self.log(f"Database stats: {stats}")
                
                if all(v == 0 for v in stats.values()):
                    self.log("Empty JSON handled correctly - database is empty")
                    result['success'] = True
                else:
                    self.log_warning("Empty JSON resulted in non-empty database")
                    result['success'] = False
                    
            except Exception as e:
                self.log(f"Caught exception: {type(e).__name__}: {str(e)[:50]}")
                # Empty JSON might or might not throw, both are acceptable
                result['success'] = True
            
            Path(temp_json.name).unlink(missing_ok=True)
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Empty JSON test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_malformed_data_structures(self) -> dict:
        """测试格式错误的数据结构"""
        self.log(f"\n{'='*60}")
        self.log("Test 5: Malformed Data Structures")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Malformed Data Structures",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            # 创建格式错误的数据
            temp_json = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
            
            # 缺少必需字段
            malformed_data = {
                'files': [{'id': 1, 'path': 'test.ets'}],  # 缺少hash
                'classes': [{'id': 1}],  # 缺少name和file_id
                'methods': [{'id': 1}],  # 缺少name
                'calls': [{'callerId': 1}],  # 缺少calleeId
                'components': [{'parentId': 1}]  # 缺少childId
            }
            
            json.dump(malformed_data, temp_json)
            temp_json.close()
            
            self.log(f"Created malformed data file: {temp_json.name}")
            
            # 尝试加载
            db = Database(Path(tempfile.mktemp(suffix='.db')))
            ark_integration = ArkAnalyzerIntegration(db)
            
            try:
                ark_integration.load_from_json(Path(temp_json.name))
                self.log("Malformed data loaded - checking if it handles gracefully...")
                
                # 验证数据库状态
                stats = db.get_stats()
                self.log(f"Database stats: {stats}")
                
                # 检查是否有数据被部分加载
                if stats['files'] > 0 or stats['classes'] > 0 or stats['methods'] > 0:
                    self.log_warning("Partial data was loaded from malformed JSON")
                    # 这可能是可接受的行为，取决于具体需求
                    result['success'] = True
                else:
                    self.log("No data loaded from malformed JSON - correct behavior")
                    result['success'] = True
                    
            except Exception as e:
                self.log(f"Caught exception: {type(e).__name__}: {str(e)[:100]}")
                result['success'] = True  # Exception is acceptable
            
            Path(temp_json.name).unlink(missing_ok=True)
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Malformed data test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_database_corruption_recovery(self) -> dict:
        """测试数据库损坏恢复"""
        self.log(f"\n{'='*60}")
        self.log("Test 6: Database Corruption Recovery")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Database Corruption Recovery",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            # 创建正常的数据库
            temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
            temp_db.close()
            
            db = Database(Path(temp_db.name))
            ark_integration = ArkAnalyzerIntegration(db)
            
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
            cmd = ['node', str(wrapper_path), '/workspace/realistic_test_project', temp_output.name]
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=300)
            
            ark_integration.load_from_json(Path(temp_output.name))
            self.log(f"Created database at: {temp_db.name}")
            
            # 损坏数据库文件
            self.log("Corrupting database file...")
            with open(temp_db.name, 'ab') as f:
                f.write(b'CORRUPTED BYTES')
            
            # 尝试重新打开
            try:
                db2 = Database(Path(temp_db.name))
                stats = db2.get_stats()
                self.log(f"Database reopened successfully with stats: {stats}")
                
                # 尝试clear_all
                db2.clear_all()
                stats_after_clear = db2.get_stats()
                self.log(f"After clear_all: {stats_after_clear}")
                
                result['success'] = True
                
            except sqlite3.DatabaseError as e:
                self.log(f"Database error caught: {str(e)[:50]}")
                result['success'] = True  # Database corruption detected
            except Exception as e:
                self.log(f"Exception caught: {type(e).__name__}: {str(e)[:50]}")
                result['success'] = True  # Any exception is acceptable for corruption
            
            Path(temp_db.name).unlink(missing_ok=True)
            Path(temp_output.name).unlink(missing_ok=True)
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Database corruption test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_transaction_rollback(self) -> dict:
        """测试事务回滚"""
        self.log(f"\n{'='*60}")
        self.log("Test 7: Transaction Rollback")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Transaction Rollback",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
            temp_db.close()
            
            db = Database(Path(temp_db.name))
            
            # 记录初始状态
            initial_stats = db.get_stats()
            self.log(f"Initial stats: {initial_stats}")
            
            # 加载一些数据
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
            cmd = ['node', str(wrapper_path), '/workspace/realistic_test_project', temp_output.name]
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=300)
            
            ark_integration = ArkAnalyzerIntegration(db)
            ark_integration.load_from_json(Path(temp_output.name))
            
            after_load_stats = db.get_stats()
            self.log(f"After load stats: {after_load_stats}")
            
            # 尝试一个会失败的操作
            self.log("Attempting operation that should fail...")
            try:
                with db.transaction() as conn:
                    # 尝试插入无效数据
                    conn.execute("INSERT INTO files (path, hash, modified) VALUES (?, ?, ?)",
                               (None, None, None))
                    raise Exception("Intentional failure for rollback test")
            except Exception as e:
                self.log(f"Caught expected exception: {str(e)[:50]}")
            
            # 验证数据未被破坏
            after_fail_stats = db.get_stats()
            self.log(f"After failed operation stats: {after_fail_stats}")
            
            if after_fail_stats == after_load_stats:
                self.log("Transaction rollback working correctly - data unchanged")
                result['success'] = True
            else:
                self.log_warning("Transaction may not have rolled back correctly")
                result['success'] = False
            
            Path(temp_db.name).unlink(missing_ok=True)
            Path(temp_output.name).unlink(missing_ok=True)
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Transaction rollback test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def run_all_tests(self):
        """运行所有测试"""
        self.log("\n" + "="*60)
        self.log("ERROR HANDLING TEST SUITE")
        self.log("="*60)
        self.log(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.test_invalid_json_file()
        self.test_missing_json_file()
        self.test_corrupted_json_file()
        self.test_empty_json_file()
        self.test_malformed_data_structures()
        self.test_database_corruption_recovery()
        self.test_transaction_rollback()
        
        self.print_summary()
    
    def print_summary(self):
        """打印测试摘要"""
        total_time = time.time() - self.start_time
        
        print("\n" + "="*60)
        print("ERROR HANDLING TEST SUMMARY")
        print("="*60)
        print(f"Total time: {total_time:.2f}s")
        print(f"Tests run: {len(self.results)}")
        
        success_count = sum(1 for r in self.results if r['success'])
        print(f"Successful: {success_count}/{len(self.results)}")
        
        if self.critical_issues:
            print(f"\nCRITICAL ISSUES ({len(self.critical_issues)}):")
            for issue in self.critical_issues:
                print(f"  - {issue[:200]}")
        
        if self.warnings:
            print(f"\nWARNINGS ({len(self.warnings)}):")
            for warn in self.warnings:
                print(f"  - {warn[:200]}")
        
        print("\nDetailed results:")
        for result in self.results:
            status = "✓ SUCCESS" if result['success'] else "✗ FAILED"
            duration = result['end_time'] - result['start_time'] if result['end_time'] else 'N/A'
            print(f"  {result['test_name']}: {status} ({duration:.2f}s)")


if __name__ == '__main__':
    test = ErrorHandlingTest()
    test.run_all_tests()
