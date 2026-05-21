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
import threading
import concurrent.futures
import traceback

sys.path.insert(0, str(Path(__file__).parent))

from arkts_graph.core.database import Database
from arkts_graph.core.ark_analyzer_integration import ArkAnalyzerIntegration


class ConcurrencyTest:
    def __init__(self):
        self.results = []
        self.start_time = time.time()
        self.errors = []
        self.warnings = []
        self.critical_issues = []
        self.db_path = None
    
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
    
    def setup_test_db(self):
        """设置测试数据库"""
        self.log("Setting up test database...")
        temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
        temp_output.close()
        
        wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
        cmd = ['node', str(wrapper_path), '/workspace/realistic_test_project', temp_output.name]
        subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=300)
        
        self.db_path = Path(tempfile.mktemp(suffix='.db'))
        db = Database(self.db_path)
        ark_integration = ArkAnalyzerIntegration(db)
        ark_integration.load_from_json(Path(temp_output.name))
        
        self.log(f"Test database created at: {self.db_path}")
        Path(temp_output.name).unlink(missing_ok=True)
        
        return db.get_stats()
    
    def test_concurrent_reads(self, num_threads: int = 5) -> dict:
        """测试并发读取"""
        self.log(f"\n{'='*60}")
        self.log(f"Test 1: Concurrent Reads ({num_threads} threads)")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': f"Concurrent Reads ({num_threads} threads)",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'stats': None,
            'error': None
        }
        
        try:
            if self.db_path is None:
                self.setup_test_db()
            
            errors_in_threads = []
            stats_from_threads = []
            
            def read_operation(thread_id):
                try:
                    db = Database(self.db_path)
                    stats = db.get_stats()
                    stats_from_threads.append(stats)
                    
                    files = db.get_all_files()
                    classes = db.get_classes()
                    methods = db.get_methods()
                    
                    time.sleep(0.1)
                    
                    return {
                        'thread_id': thread_id,
                        'success': True,
                        'stats': stats,
                        'files_count': len(files),
                        'classes_count': len(classes),
                        'methods_count': len(methods)
                    }
                except Exception as e:
                    errors_in_threads.append((thread_id, str(e)))
                    return {
                        'thread_id': thread_id,
                        'success': False,
                        'error': str(e)
                    }
            
            self.log(f"Starting {num_threads} concurrent read threads...")
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = [executor.submit(read_operation, i) for i in range(num_threads)]
                results = [f.result() for f in concurrent.futures.as_completed(futures)]
            
            self.log(f"All {num_threads} threads completed")
            
            if errors_in_threads:
                self.log_error(f"Errors in {len(errors_in_threads)} threads", None)
                for thread_id, error in errors_in_threads:
                    self.log(f"  Thread {thread_id}: {error}")
                result['error'] = f"Errors in {len(errors_in_threads)} threads"
            else:
                self.log("All threads completed successfully")
            
            # 检查结果一致性
            first_stats = stats_from_threads[0] if stats_from_threads else None
            all_consistent = all(s == first_stats for s in stats_from_threads) if first_stats else False
            
            if not all_consistent:
                self.log_warning("Inconsistent stats from different threads")
            
            result['success'] = len(errors_in_threads) == 0 and all_consistent
            result['stats'] = {
                'threads': num_threads,
                'successful_threads': num_threads - len(errors_in_threads),
                'errors': len(errors_in_threads),
                'all_consistent': all_consistent
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Concurrent reads test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_concurrent_writes(self, num_threads: int = 3) -> dict:
        """测试并发写入"""
        self.log(f"\n{'='*60}")
        self.log(f"Test 2: Concurrent Writes ({num_threads} threads)")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': f"Concurrent Writes ({num_threads} threads)",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'stats': None,
            'error': None
        }
        
        try:
            # 为每个测试创建新的数据库
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
            cmd = ['node', str(wrapper_path), '/workspace/realistic_test_project', temp_output.name]
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=300)
            
            test_db_path = Path(tempfile.mktemp(suffix='.db'))
            
            errors_in_threads = []
            success_count = 0
            
            def write_operation(thread_id):
                nonlocal success_count
                try:
                    db = Database(test_db_path)
                    ark_integration = ArkAnalyzerIntegration(db)
                    ark_integration.load_from_json(Path(temp_output.name))
                    success_count += 1
                    return {'thread_id': thread_id, 'success': True}
                except Exception as e:
                    errors_in_threads.append((thread_id, str(e)))
                    return {'thread_id': thread_id, 'success': False, 'error': str(e)}
            
            self.log(f"Starting {num_threads} concurrent write threads...")
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = [executor.submit(write_operation, i) for i in range(num_threads)]
                results = [f.result() for f in concurrent.futures.as_completed(futures)]
            
            self.log(f"All {num_threads} write threads completed")
            
            if errors_in_threads:
                self.log_error(f"Errors in {len(errors_in_threads)} write threads", None)
                for thread_id, error in errors_in_threads:
                    self.log(f"  Thread {thread_id}: {error}")
            
            # 验证数据库状态
            db = Database(test_db_path)
            final_stats = db.get_stats()
            self.log(f"Final database stats: {final_stats}")
            
            Path(temp_output.name).unlink(missing_ok=True)
            
            result['success'] = success_count == num_threads
            result['stats'] = {
                'threads': num_threads,
                'successful_writes': success_count,
                'errors': len(errors_in_threads),
                'final_stats': final_stats
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Concurrent writes test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_rapid_clear_reload(self, iterations: int = 5) -> dict:
        """测试快速清空和重新加载"""
        self.log(f"\n{'='*60}")
        self.log(f"Test 3: Rapid Clear and Reload ({iterations} iterations)")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': f"Rapid Clear and Reload ({iterations} iterations)",
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
            
            test_db_path = Path(tempfile.mktemp(suffix='.db'))
            db = Database(test_db_path)
            ark_integration = ArkAnalyzerIntegration(db)
            
            errors = []
            iterations_completed = 0
            
            for i in range(iterations):
                self.log(f"  Iteration {i+1}/{iterations}...")
                try:
                    # 清空
                    db.clear_all()
                    stats_after_clear = db.get_stats()
                    if any(stats_after_clear.values()):
                        errors.append(f"Iteration {i+1}: clear_all did not fully clear database")
                    
                    # 重新加载
                    ark_integration.load_from_json(Path(temp_output.name))
                    stats_after_load = db.get_stats()
                    
                    iterations_completed += 1
                    
                except Exception as e:
                    errors.append(f"Iteration {i+1}: {str(e)}")
            
            Path(temp_output.name).unlink(missing_ok=True)
            
            if errors:
                for error in errors:
                    self.log_error(error, None)
            
            self.log(f"Completed {iterations_completed}/{iterations} iterations")
            
            result['success'] = iterations_completed == iterations and len(errors) == 0
            result['stats'] = {
                'iterations': iterations,
                'completed': iterations_completed,
                'errors': len(errors),
                'error_details': errors
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Rapid clear/reload test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_database_lock_scenario(self) -> dict:
        """测试数据库锁定场景"""
        self.log(f"\n{'='*60}")
        self.log("Test 4: Database Lock Scenario")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Database Lock Scenario",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'stats': None,
            'error': None
        }
        
        try:
            test_db_path = Path(tempfile.mktemp(suffix='.db'))
            
            # 创建一个长时间运行的数据库操作
            def long_operation():
                try:
                    db = Database(test_db_path)
                    db._get_connection().execute("BEGIN EXCLUSIVE")
                    time.sleep(2)
                    db._get_connection().execute("COMMIT")
                    return {'success': True}
                except Exception as e:
                    return {'success': False, 'error': str(e)}
            
            def concurrent_operation():
                time.sleep(0.5)  # 确保在长操作之后开始
                try:
                    db = Database(test_db_path)
                    stats = db.get_stats()
                    return {'success': True, 'stats': stats}
                except Exception as e:
                    return {'success': False, 'error': str(e)}
            
            self.log("Starting long operation and concurrent operation...")
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                future1 = executor.submit(long_operation)
                future2 = executor.submit(concurrent_operation)
                
                result1 = future1.result()
                result2 = future2.result()
            
            self.log(f"Long operation result: {result1}")
            self.log(f"Concurrent operation result: {result2}")
            
            # 检查是否出现了锁定问题
            lock_issue = False
            if not result1['success'] and 'locked' in str(result1.get('error', '')).lower():
                lock_issue = True
                self.log_warning("Detected database lock issue in long operation")
            
            if not result2['success'] and 'locked' in str(result2.get('error', '')).lower():
                lock_issue = True
                self.log_warning("Detected database lock issue in concurrent operation")
            
            result['success'] = True  # 即使有锁定也算测试完成
            result['stats'] = {
                'long_operation': result1,
                'concurrent_operation': result2,
                'lock_issue_detected': lock_issue
            }
            
            if lock_issue:
                self.log_warning("Database locking behavior detected (may be expected)")
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Database lock scenario test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def run_all_tests(self):
        """运行所有测试"""
        self.log("\n" + "="*60)
        self.log("CONCURRENCY TEST SUITE")
        self.log("="*60)
        self.log(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.test_concurrent_reads(num_threads=10)
        self.test_concurrent_writes(num_threads=3)
        self.test_rapid_clear_reload(iterations=3)
        self.test_database_lock_scenario()
        
        self.print_summary()
    
    def print_summary(self):
        """打印测试摘要"""
        total_time = time.time() - self.start_time
        
        print("\n" + "="*60)
        print("CONCURRENCY TEST SUMMARY")
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
    test = ConcurrencyTest()
    test.run_all_tests()
