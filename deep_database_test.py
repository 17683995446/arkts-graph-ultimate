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


class DatabaseIntegrationTest:
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
        self.critical_issues.append(error_msg)
    
    def log_warning(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        warning_msg = f"[{timestamp}] WARNING: {message}"
        print(warning_msg)
        self.warnings.append(warning_msg)
    
    def test_database_load_consistency(self) -> dict:
        """测试数据库加载的一致性"""
        self.log(f"\n{'='*60}")
        self.log("Test 1: Database Load Consistency")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Database Load Consistency",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'stats': None,
            'error': None
        }
        
        try:
            # 生成测试数据
            self.log("Generating test data...")
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
            cmd = ['node', str(wrapper_path), '/workspace/realistic_test_project', temp_output.name]
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=300)
            
            with open(temp_output.name, 'r', encoding='utf-8') as f:
                original_data = json.load(f)
            
            self.log(f"Original data: files={len(original_data['files'])}, classes={len(original_data['classes'])}, methods={len(original_data['methods'])}")
            
            # 测试多次加载的一致性
            self.log("Testing multiple loads...")
            db = Database(Path(tempfile.mktemp(suffix='.db')))
            ark_integration = ArkAnalyzerIntegration(db)
            
            load_results = []
            for i in range(3):
                self.log(f"  Load {i+1}...")
                ark_integration.load_from_json(Path(temp_output.name))
                stats = db.get_stats()
                load_results.append(stats.copy())
                self.log(f"    Stats: {stats}")
                
                if i < 2:
                    db.clear_all()
            
            # 检查一致性
            first_result = load_results[0]
            all_consistent = all(r == first_result for r in load_results)
            
            if not all_consistent:
                self.log_warning(f"Inconsistent results: {load_results}")
            
            # 验证数据完整性
            self.log("Verifying data integrity...")
            files_in_db = len(db.get_all_files())
            classes_in_db = len(db.get_classes())
            methods_in_db = len(db.get_methods())
            
            self.log(f"  DB has: files={files_in_db}, classes={classes_in_db}, methods={methods_in_db}")
            self.log(f"  JSON has: files={len(original_data['files'])}, classes={len(original_data['classes'])}, methods={len(original_data['methods'])}")
            
            data_match = (
                files_in_db == len(original_data['files']) and
                classes_in_db == len(original_data['classes']) and
                methods_in_db == len(original_data['methods'])
            )
            
            if not data_match:
                self.log_error(f"Data mismatch! DB vs JSON", None)
                result['error'] = "Data count mismatch"
            else:
                self.log("Data integrity check passed")
            
            result['success'] = data_match and all_consistent
            result['stats'] = {
                'load_results': load_results,
                'data_match': data_match,
                'all_consistent': all_consistent
            }
            
            Path(temp_output.name).unlink(missing_ok=True)
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Database load consistency test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_call_relationship_import(self) -> dict:
        """测试调用关系导入"""
        self.log(f"\n{'='*60}")
        self.log("Test 2: Call Relationship Import")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Call Relationship Import",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'stats': None,
            'error': None
        }
        
        try:
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
            cmd = ['node', str(wrapper_path), '/workspace/realistic_test_project', temp_output.name]
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=300)
            
            with open(temp_output.name, 'r', encoding='utf-8') as f:
                analysis_data = json.load(f)
            
            calls_in_json = len(analysis_data.get('calls', []))
            self.log(f"Calls in JSON: {calls_in_json}")
            
            # 检查调用数据的结构
            if calls_in_json > 0:
                sample_call = analysis_data['calls'][0]
                self.log(f"Sample call structure: {sample_call.keys()}")
                
                # 检查字段名
                has_callerId = 'callerId' in sample_call
                has_calleeId = 'calleeId' in sample_call
                has_callerMethod = 'callerMethod' in sample_call
                has_calleeMethod = 'calleeMethod' in sample_call
                
                self.log(f"  Has callerId: {has_callerId}")
                self.log(f"  Has calleeId: {has_calleeId}")
                self.log(f"  Has callerMethod: {has_callerMethod}")
                self.log(f"  Has calleeMethod: {has_calleeMethod}")
                
                if not (has_callerId or has_callerMethod):
                    self.log_warning("Call data missing caller identification")
                if not (has_calleeId or has_calleeMethod):
                    self.log_warning("Call data missing callee identification")
            
            # 测试数据库导入
            db = Database(Path(tempfile.mktemp(suffix='.db')))
            ark_integration = ArkAnalyzerIntegration(db)
            ark_integration.load_from_json(Path(temp_output.name))
            
            stats = db.get_stats()
            calls_in_db = stats['calls']
            self.log(f"Calls in DB: {calls_in_db}")
            
            # 检查调用关系的有效性
            call_graph = db.get_call_graph()
            valid_calls = 0
            invalid_calls = 0
            
            for caller_id, callee_id in call_graph:
                if caller_id > 0 and callee_id > 0:
                    valid_calls += 1
                else:
                    invalid_calls += 1
            
            self.log(f"Valid calls: {valid_calls}, Invalid calls: {invalid_calls}")
            
            if invalid_calls > 0:
                self.log_warning(f"Found {invalid_calls} invalid call relationships")
            
            result['success'] = True
            result['stats'] = {
                'calls_in_json': calls_in_json,
                'calls_in_db': calls_in_db,
                'valid_calls': valid_calls,
                'invalid_calls': invalid_calls
            }
            
            Path(temp_output.name).unlink(missing_ok=True)
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Call relationship import test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_component_relationship_import(self) -> dict:
        """测试组件关系导入"""
        self.log(f"\n{'='*60}")
        self.log("Test 3: Component Relationship Import")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Component Relationship Import",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'stats': None,
            'error': None
        }
        
        try:
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
            cmd = ['node', str(wrapper_path), '/workspace/realistic_test_project', temp_output.name]
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=300)
            
            with open(temp_output.name, 'r', encoding='utf-8') as f:
                analysis_data = json.load(f)
            
            components_in_json = len(analysis_data.get('components', []))
            self.log(f"Components in JSON: {components_in_json}")
            
            # 检查组件数据的结构
            if components_in_json > 0:
                sample_component = analysis_data['components'][0]
                self.log(f"Sample component structure: {sample_component.keys()}")
                
                # 检查字段名
                has_parent_id = 'parent_id' in sample_component
                has_child_id = 'child_id' in sample_component
                has_parentId = 'parentId' in sample_component
                has_childId = 'childId' in sample_component
                
                self.log(f"  Has parent_id: {has_parent_id}")
                self.log(f"  Has child_id: {has_child_id}")
                self.log(f"  Has parentId: {has_parentId}")
                self.log(f"  Has childId: {has_childId}")
                
                if not (has_parent_id or has_parentId):
                    self.log_warning("Component data missing parent identification")
                if not (has_child_id or has_childId):
                    self.log_warning("Component data missing child identification")
            
            # 测试数据库导入
            db = Database(Path(tempfile.mktemp(suffix='.db')))
            ark_integration = ArkAnalyzerIntegration(db)
            ark_integration.load_from_json(Path(temp_output.name))
            
            stats = db.get_stats()
            components_in_db = stats['components']
            self.log(f"Components in DB: {components_in_db}")
            
            # 检查组件关系的有效性
            component_graph = db.get_component_graph()
            valid_components = 0
            invalid_components = 0
            
            for parent_id, child_id in component_graph:
                if parent_id >= 0 and child_id > 0:
                    valid_components += 1
                else:
                    invalid_components += 1
            
            self.log(f"Valid components: {valid_components}, Invalid components: {invalid_components}")
            
            if invalid_components > 0:
                self.log_warning(f"Found {invalid_components} invalid component relationships")
            
            result['success'] = True
            result['stats'] = {
                'components_in_json': components_in_json,
                'components_in_db': components_in_db,
                'valid_components': valid_components,
                'invalid_components': invalid_components
            }
            
            Path(temp_output.name).unlink(missing_ok=True)
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Component relationship import test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_performance_large_dataset(self) -> dict:
        """测试大数据集性能"""
        self.log(f"\n{'='*60}")
        self.log("Test 4: Performance with Large Dataset")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Performance Large Dataset",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'stats': None,
            'error': None
        }
        
        try:
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
            cmd = ['node', str(wrapper_path), '/workspace/realistic_test_project', temp_output.name]
            
            self.log("Running ArkAnalyzer...")
            start_ark = time.time()
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=300)
            ark_time = time.time() - start_ark
            
            with open(temp_output.name, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            stats = {
                'files': len(data.get('files', [])),
                'classes': len(data.get('classes', [])),
                'methods': len(data.get('methods', [])),
                'calls': len(data.get('calls', [])),
                'components': len(data.get('components', []))
            }
            
            self.log(f"Analysis completed in {ark_time:.2f}s")
            self.log(f"Stats: {stats}")
            
            # 测试数据库加载性能
            self.log("Testing database load performance...")
            db = Database(Path(tempfile.mktemp(suffix='.db')))
            ark_integration = ArkAnalyzerIntegration(db)
            
            start_load = time.time()
            ark_integration.load_from_json(Path(temp_output.name))
            load_time = time.time() - start_load
            
            self.log(f"Database load completed in {load_time:.2f}s")
            
            total_time = ark_time + load_time
            self.log(f"Total time: {total_time:.2f}s")
            
            # 性能评估
            if total_time > 60:
                self.log_warning("Total time exceeds 60 seconds - performance may need optimization")
            elif total_time > 30:
                self.log_warning("Total time exceeds 30 seconds - consider optimization")
            else:
                self.log("Performance is acceptable")
            
            result['success'] = True
            result['stats'] = {
                'ark_time': ark_time,
                'load_time': load_time,
                'total_time': total_time,
                'data_stats': stats
            }
            
            Path(temp_output.name).unlink(missing_ok=True)
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Performance test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_data_integrity(self) -> dict:
        """测试数据完整性"""
        self.log(f"\n{'='*60}")
        self.log("Test 5: Data Integrity Check")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Data Integrity",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'stats': None,
            'error': None
        }
        
        try:
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
            cmd = ['node', str(wrapper_path), '/workspace/realistic_test_project', temp_output.name]
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=300)
            
            with open(temp_output.name, 'r', encoding='utf-8') as f:
                original_data = json.load(f)
            
            db = Database(Path(tempfile.mktemp(suffix='.db')))
            ark_integration = ArkAnalyzerIntegration(db)
            ark_integration.load_from_json(Path(temp_output.name))
            
            # 检查文件的完整性
            files_in_db = db.get_all_files()
            files_match = len(files_in_db) == len(original_data['files'])
            self.log(f"Files match: {files_match} ({len(files_in_db)} vs {len(original_data['files'])})")
            
            # 检查类的完整性
            classes_in_db = db.get_classes()
            classes_match = len(classes_in_db) == len(original_data['classes'])
            self.log(f"Classes match: {classes_match} ({len(classes_in_db)} vs {len(original_data['classes'])})")
            
            # 检查方法的完整性
            methods_in_db = db.get_methods()
            methods_match = len(methods_in_db) == len(original_data['methods'])
            self.log(f"Methods match: {methods_match} ({len(methods_in_db)} vs {len(original_data['methods'])})")
            
            # 检查调用关系的完整性
            call_graph = db.get_call_graph()
            calls_match = len(call_graph) <= len(original_data['calls'])
            self.log(f"Calls match: {calls_match} ({len(call_graph)} vs {len(original_data['calls'])})")
            
            # 检查组件关系的完整性
            component_graph = db.get_component_graph()
            components_match = len(component_graph) <= len(original_data['components'])
            self.log(f"Components match: {components_match} ({len(component_graph)} vs {len(original_data['components'])})")
            
            # 验证类与方法的关系
            self.log("Verifying class-method relationships...")
            orphaned_methods = 0
            for method in methods_in_db:
                if method.class_id is not None and method.class_id > 0:
                    class_exists = any(cls.id == method.class_id for cls in classes_in_db)
                    if not class_exists:
                        orphaned_methods += 1
            
            if orphaned_methods > 0:
                self.log_warning(f"Found {orphaned_methods} orphaned methods")
            
            all_match = files_match and classes_match and methods_match and calls_match and components_match
            
            result['success'] = all_match and orphaned_methods == 0
            result['stats'] = {
                'files_match': files_match,
                'classes_match': classes_match,
                'methods_match': methods_match,
                'calls_match': calls_match,
                'components_match': components_match,
                'orphaned_methods': orphaned_methods
            }
            
            if not result['success']:
                self.log_error("Data integrity check failed", None)
            
            Path(temp_output.name).unlink(missing_ok=True)
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Data integrity test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def run_all_tests(self):
        """运行所有测试"""
        self.log("\n" + "="*60)
        self.log("DATABASE INTEGRATION DEEP TEST SUITE")
        self.log("="*60)
        self.log(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.test_database_load_consistency()
        self.test_call_relationship_import()
        self.test_component_relationship_import()
        self.test_performance_large_dataset()
        self.test_data_integrity()
        
        self.print_summary()
    
    def print_summary(self):
        """打印测试摘要"""
        total_time = time.time() - self.start_time
        
        print("\n" + "="*60)
        print("TEST SUMMARY")
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
    test = DatabaseIntegrationTest()
    test.run_all_tests()
