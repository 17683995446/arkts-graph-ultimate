#!/usr/bin/env python3
import sys
import time
import json
import traceback
from pathlib import Path
from datetime import datetime
import subprocess
import tempfile
import psutil
import os
import gc

sys.path.insert(0, str(Path(__file__).parent))

from arkts_graph.core.database import Database
from arkts_graph.core.ark_analyzer_integration import ArkAnalyzerIntegration


class ExtremeStressTest:
    def __init__(self):
        self.results = []
        self.start_time = time.time()
        self.process = psutil.Process(os.getpid())
        self.initial_memory = self.process.memory_info().rss / 1024 / 1024
    
    def log(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {message}")
    
    def log_error(self, message: str, exc: Exception = None):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_msg = f"[{timestamp}] ERROR: {message}"
        if exc:
            error_msg += f"\n{traceback.format_exc()}"
        print(error_msg)
    
    def get_memory_usage(self) -> float:
        gc.collect()
        return self.process.memory_info().rss / 1024 / 1024
    
    def test_massive_project_analysis(self) -> dict:
        """测试5000文件的大规模项目分析"""
        self.log(f"\n{'='*60}")
        self.log("TEST 1: Massive Project Analysis (5000 files, 42MB)")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Massive Project Analysis",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            self.log(f"Initial memory: {self.initial_memory:.2f} MB")
            
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
            cmd = ['node', str(wrapper_path), '/workspace/massive_test_project', temp_output.name]
            
            self.log("Starting ArkAnalyzer on 5000 files...")
            mem_before = self.get_memory_usage()
            self.log(f"Memory before analysis: {mem_before:.2f} MB")
            
            start = time.time()
            ark_result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            elapsed = time.time() - start
            
            mem_after = self.get_memory_usage()
            self.log(f"Memory after analysis: {mem_after:.2f} MB")
            self.log(f"Memory increase: {mem_after - mem_before:.2f} MB")
            
            if ark_result.returncode != 0:
                raise RuntimeError(f"ArkAnalyzer failed: {ark_result.stderr}")
            
            with open(temp_output.name, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            stats = {
                'files': len(data.get('files', [])),
                'classes': len(data.get('classes', [])),
                'methods': len(data.get('methods', [])),
                'calls': len(data.get('calls', [])),
                'components': len(data.get('components', []))
            }
            
            self.log(f"Analysis completed in {elapsed:.2f}s")
            self.log(f"Stats: {stats}")
            
            # 检查JSON文件大小
            json_size = Path(temp_output.name).stat().st_size / 1024 / 1024
            self.log(f"Output JSON size: {json_size:.2f} MB")
            
            if json_size > 100:
                self.log(f"WARNING: JSON output is very large ({json_size:.2f} MB)")
            
            result['success'] = True
            result['stats'] = {
                'analysis_time': elapsed,
                'data_stats': stats,
                'memory_used': mem_after - mem_before,
                'json_size': json_size
            }
            
            Path(temp_output.name).unlink(missing_ok=True)
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Massive project test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_database_load_massive_data(self) -> dict:
        """测试加载大规模数据到数据库"""
        self.log(f"\n{'='*60}")
        self.log("TEST 2: Database Load Massive Data")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Database Load Massive Data",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            self.log("Generating massive dataset first...")
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
            cmd = ['node', str(wrapper_path), '/workspace/massive_test_project', temp_output.name]
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=600)
            
            with open(temp_output.name, 'r', encoding='utf-8') as f:
                data_size = len(f.read())
            
            self.log(f"JSON data size: {data_size / 1024 / 1024:.2f} MB")
            
            temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
            temp_db.close()
            
            self.log("Creating database...")
            db = Database(Path(temp_db.name))
            
            mem_before = self.get_memory_usage()
            self.log(f"Memory before load: {mem_before:.2f} MB")
            
            self.log("Loading data into database...")
            ark_integration = ArkAnalyzerIntegration(db)
            
            start = time.time()
            ark_integration.load_from_json(Path(temp_output.name))
            elapsed = time.time() - start
            
            mem_after = self.get_memory_usage()
            self.log(f"Memory after load: {mem_after:.2f} MB")
            self.log(f"Memory increase: {mem_after - mem_before:.2f} MB")
            
            stats = db.get_stats()
            self.log(f"Database stats: {stats}")
            self.log(f"Load completed in {elapsed:.2f}s")
            
            # 测试查询性能
            self.log("Testing query performance...")
            start = time.time()
            files = db.get_all_files()
            classes = db.get_classes()
            methods = db.get_methods()
            query_time = time.time() - start
            
            self.log(f"Query time: {query_time:.3f}s")
            self.log(f"Files: {len(files)}, Classes: {len(classes)}, Methods: {len(methods)}")
            
            if query_time > 5:
                self.log(f"WARNING: Query time is slow ({query_time:.3f}s)")
            
            db_size = Path(temp_db.name).stat().st_size / 1024 / 1024
            self.log(f"Database file size: {db_size:.2f} MB")
            
            result['success'] = True
            result['stats'] = {
                'load_time': elapsed,
                'query_time': query_time,
                'db_stats': stats,
                'memory_increase': mem_after - mem_before,
                'db_size': db_size
            }
            
            Path(temp_output.name).unlink(missing_ok=True)
            Path(temp_db.name).unlink(missing_ok=True)
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Database load test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_memory_leak_detection(self) -> dict:
        """测试内存泄漏"""
        self.log(f"\n{'='*60}")
        self.log("TEST 3: Memory Leak Detection")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Memory Leak Detection",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            iterations = 5
            memory_readings = []
            
            self.log(f"Running {iterations} iterations to detect memory leaks...")
            
            for i in range(iterations):
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
                
                mem_usage = self.get_memory_usage()
                memory_readings.append(mem_usage)
                
                self.log(f"  Iteration {i+1}: Memory = {mem_usage:.2f} MB")
                
                Path(temp_output.name).unlink(missing_ok=True)
                Path(temp_db.name).unlink(missing_ok=True)
                
                gc.collect()
            
            # 分析内存趋势
            first_reading = memory_readings[0]
            last_reading = memory_readings[-1]
            avg_reading = sum(memory_readings) / len(memory_readings)
            memory_growth = last_reading - first_reading
            
            self.log(f"First reading: {first_reading:.2f} MB")
            self.log(f"Last reading: {last_reading:.2f} MB")
            self.log(f"Average: {avg_reading:.2f} MB")
            self.log(f"Growth: {memory_growth:.2f} MB")
            
            if memory_growth > 50:
                self.log("WARNING: Significant memory growth detected (>50MB)")
                leak_detected = True
            elif memory_growth > 20:
                self.log("INFO: Moderate memory growth detected (>20MB)")
                leak_detected = False
            else:
                self.log("No significant memory leak detected")
                leak_detected = False
            
            result['success'] = True
            result['stats'] = {
                'iterations': iterations,
                'memory_readings': memory_readings,
                'first': first_reading,
                'last': last_reading,
                'average': avg_reading,
                'growth': memory_growth,
                'leak_detected': leak_detected
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Memory leak test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_resource_cleanup(self) -> dict:
        """测试资源清理"""
        self.log(f"\n{'='*60}")
        self.log("TEST 4: Resource Cleanup")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Resource Cleanup",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            self.log("Testing file handle cleanup...")
            initial_files = len(self.process.open_files())
            self.log(f"Initial open files: {initial_files}")
            
            for i in range(10):
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
                
                Path(temp_output.name).unlink(missing_ok=True)
                Path(temp_db.name).unlink(missing_ok=True)
            
            final_files = len(self.process.open_files())
            self.log(f"Final open files: {final_files}")
            
            file_leak = final_files - initial_files
            if file_leak > 5:
                self.log(f"WARNING: File handle leak detected ({file_leak} files)")
                leak_detected = True
            else:
                self.log("No file handle leak detected")
                leak_detected = False
            
            result['success'] = True
            result['stats'] = {
                'initial_files': initial_files,
                'final_files': final_files,
                'leak': file_leak,
                'leak_detected': leak_detected
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Resource cleanup test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_performance_regression(self) -> dict:
        """测试性能回归"""
        self.log(f"\n{'='*60}")
        self.log("TEST 5: Performance Regression")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Performance Regression",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            iterations = 20
            times = []
            
            self.log(f"Running {iterations} iterations to check performance consistency...")
            
            for i in range(iterations):
                temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
                temp_output.close()
                
                wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
                cmd = ['node', str(wrapper_path), '/workspace/realistic_test_project', temp_output.name]
                
                start = time.time()
                subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=300)
                elapsed = time.time() - start
                
                times.append(elapsed)
                if (i + 1) % 5 == 0:
                    self.log(f"  {i+1}/{iterations}: {elapsed:.3f}s")
                
                Path(temp_output.name).unlink(missing_ok=True)
            
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            std_dev = (sum((t - avg_time) ** 2 for t in times) / len(times)) ** 0.5
            
            self.log(f"Average time: {avg_time:.3f}s")
            self.log(f"Min time: {min_time:.3f}s")
            self.log(f"Max time: {max_time:.3f}s")
            self.log(f"Std deviation: {std_dev:.3f}s")
            
            if std_dev / avg_time > 0.3:
                self.log("WARNING: High performance variance detected")
                regression = True
            else:
                self.log("Performance is consistent")
                regression = False
            
            result['success'] = True
            result['stats'] = {
                'iterations': iterations,
                'average': avg_time,
                'min': min_time,
                'max': max_time,
                'std_dev': std_dev,
                'regression': regression
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Performance regression test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def run_all_tests(self):
        """运行所有测试"""
        self.log("\n" + "="*60)
        self.log("EXTREME STRESS TEST SUITE")
        self.log("="*60)
        self.log(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"Initial memory: {self.initial_memory:.2f} MB")
        
        self.test_massive_project_analysis()
        self.test_database_load_massive_data()
        self.test_memory_leak_detection()
        self.test_resource_cleanup()
        self.test_performance_regression()
        
        self.print_summary()
    
    def print_summary(self):
        """打印测试摘要"""
        total_time = time.time() - self.start_time
        final_memory = self.get_memory_usage()
        
        print("\n" + "="*60)
        print("EXTREME TEST SUMMARY")
        print("="*60)
        print(f"Total time: {total_time:.2f}s")
        print(f"Initial memory: {self.initial_memory:.2f} MB")
        print(f"Final memory: {final_memory:.2f} MB")
        print(f"Memory growth: {final_memory - self.initial_memory:.2f} MB")
        print(f"Tests run: {len(self.results)}")
        
        success_count = sum(1 for r in self.results if r['success'])
        print(f"Successful: {success_count}/{len(self.results)}")
        
        print("\nDetailed results:")
        for result in self.results:
            status = "✓ SUCCESS" if result['success'] else "✗ FAILED"
            duration = result['end_time'] - result['start_time'] if result['end_time'] else 'N/A'
            print(f"  {result['test_name']}: {status} ({duration:.2f}s)")


if __name__ == '__main__':
    test = ExtremeStressTest()
    test.run_all_tests()
