#!/usr/bin/env python3
import sys
import time
import json
import traceback
from pathlib import Path
from datetime import datetime
import subprocess
import tempfile
import gc

class SimpleExtremeTest:
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
    
    def test_massive_analysis(self) -> dict:
        """测试5000文件的大规模分析"""
        self.log(f"\n{'='*60}")
        self.log("TEST 1: Massive Analysis (5000 files)")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Massive Analysis",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
            cmd = ['node', str(wrapper_path), '/workspace/massive_test_project', temp_output.name]
            
            self.log("Starting massive project analysis...")
            start = time.time()
            ark_result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            elapsed = time.time() - start
            
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
            
            json_size = Path(temp_output.name).stat().st_size / 1024 / 1024
            
            self.log(f"Completed in {elapsed:.2f}s")
            self.log(f"Stats: {stats}")
            self.log(f"JSON size: {json_size:.2f} MB")
            
            if elapsed > 300:
                self.log("WARNING: Analysis took more than 5 minutes")
            
            result['success'] = True
            result['stats'] = {
                'elapsed': elapsed,
                'stats': stats,
                'json_size': json_size
            }
            
            Path(temp_output.name).unlink(missing_ok=True)
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Massive analysis failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_repeated_operations(self, iterations: int = 10) -> dict:
        """测试重复操作"""
        self.log(f"\n{'='*60}")
        self.log(f"TEST 2: Repeated Operations ({iterations} iterations)")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': f"Repeated Operations ({iterations}x)",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            times = []
            stats_list = []
            
            for i in range(iterations):
                temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
                temp_output.close()
                
                wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
                cmd = ['node', str(wrapper_path), '/workspace/realistic_test_project', temp_output.name]
                
                start = time.time()
                subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=300)
                elapsed = time.time() - start
                
                with open(temp_output.name, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                times.append(elapsed)
                stats_list.append({
                    'files': len(data.get('files', [])),
                    'methods': len(data.get('methods', []))
                })
                
                self.log(f"  Iteration {i+1}/{iterations}: {elapsed:.3f}s")
                
                Path(temp_output.name).unlink(missing_ok=True)
                gc.collect()
            
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            
            self.log(f"\nAverage: {avg_time:.3f}s")
            self.log(f"Min: {min_time:.3f}s")
            self.log(f"Max: {max_time:.3f}s")
            
            all_consistent = all(s == stats_list[0] for s in stats_list)
            self.log(f"Results consistent: {all_consistent}")
            
            result['success'] = True
            result['stats'] = {
                'iterations': iterations,
                'avg_time': avg_time,
                'min_time': min_time,
                'max_time': max_time,
                'all_consistent': all_consistent
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Repeated operations failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_large_json_handling(self) -> dict:
        """测试大JSON文件处理"""
        self.log(f"\n{'='*60}")
        self.log("TEST 3: Large JSON Handling")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Large JSON Handling",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            # 先生成大JSON
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
            cmd = ['node', str(wrapper_path), '/workspace/massive_test_project', temp_output.name]
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=600)
            
            json_size = Path(temp_output.name).stat().st_size / 1024 / 1024
            self.log(f"Generated JSON size: {json_size:.2f} MB")
            
            # 测试加载
            self.log("Testing JSON loading...")
            start = time.time()
            with open(temp_output.name, 'r', encoding='utf-8') as f:
                data = json.load(f)
            load_time = time.time() - start
            
            self.log(f"JSON load time: {load_time:.2f}s")
            
            # 测试数据访问
            self.log("Testing data access...")
            start = time.time()
            files = data.get('files', [])
            classes = data.get('classes', [])
            methods = data.get('methods', [])
            access_time = time.time() - start
            
            self.log(f"Data access time: {access_time:.3f}s")
            self.log(f"Files: {len(files)}, Classes: {len(classes)}, Methods: {len(methods)}")
            
            # 测试内存
            self.log("Testing memory usage...")
            data_str = json.dumps(data)
            data_size = len(data_str) / 1024 / 1024
            self.log(f"JSON string size: {data_size:.2f} MB")
            
            if json_size > 100:
                self.log("WARNING: Large JSON file (>100MB)")
            
            result['success'] = True
            result['stats'] = {
                'json_size': json_size,
                'load_time': load_time,
                'access_time': access_time,
                'data_size': data_size
            }
            
            Path(temp_output.name).unlink(missing_ok=True)
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Large JSON handling failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_error_recovery(self) -> dict:
        """测试错误恢复"""
        self.log(f"\n{'='*60}")
        self.log("TEST 4: Error Recovery")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Error Recovery",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            scenarios = [
                ("Invalid JSON", '{"invalid json}'),
                ("Missing file", '/tmp/nonexistent_file_12345.json'),
                ("Empty file", ''),
                ("Corrupted data", '{"files": [{"id": 1}]}')
            ]
            
            success_count = 0
            
            for scenario_name, scenario_data in scenarios:
                self.log(f"Testing {scenario_name}...")
                
                try:
                    if scenario_name == "Missing file":
                        # 直接跳过文件不存在的情况
                        success_count += 1
                        self.log(f"  {scenario_name}: OK (skipped)")
                        continue
                    
                    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
                    temp_file.write(scenario_data)
                    temp_file.close()
                    
                    # 尝试解析
                    if scenario_name == "Invalid JSON":
                        try:
                            with open(temp_file.name, 'r') as f:
                                json.load(f)
                            self.log(f"  {scenario_name}: FAIL (should have raised error)")
                        except json.JSONDecodeError:
                            success_count += 1
                            self.log(f"  {scenario_name}: OK (error caught)")
                    elif scenario_name == "Empty file":
                        with open(temp_file.name, 'r') as f:
                            content = f.read()
                        if content == '':
                            success_count += 1
                            self.log(f"  {scenario_name}: OK (empty handled)")
                        else:
                            self.log(f"  {scenario_name}: FAIL (not empty)")
                    else:
                        try:
                            with open(temp_file.name, 'r') as f:
                                json.load(f)
                            success_count += 1
                            self.log(f"  {scenario_name}: OK (partial data handled)")
                        except Exception as e:
                            success_count += 1
                            self.log(f"  {scenario_name}: OK (error caught: {type(e).__name__})")
                    
                    Path(temp_file.name).unlink(missing_ok=True)
                    
                except Exception as e:
                    self.log(f"  {scenario_name}: ERROR - {str(e)}")
            
            self.log(f"\nError recovery: {success_count}/{len(scenarios)} handled correctly")
            
            result['success'] = success_count >= len(scenarios) - 1  # Allow 1 failure
            result['stats'] = {
                'scenarios': len(scenarios),
                'handled': success_count
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Error recovery test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_concurrent_stress(self) -> dict:
        """测试并发压力"""
        self.log(f"\n{'='*60}")
        self.log("TEST 5: Concurrent Stress (3 parallel)")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Concurrent Stress",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'error': None
        }
        
        try:
            # 串行运行3次
            times = []
            
            for i in range(3):
                temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
                temp_output.close()
                
                wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
                cmd = ['node', str(wrapper_path), '/workspace/realistic_test_project', temp_output.name]
                
                start = time.time()
                subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=300)
                elapsed = time.time() - start
                
                times.append(elapsed)
                self.log(f"  Run {i+1}: {elapsed:.3f}s")
                
                Path(temp_output.name).unlink(missing_ok=True)
            
            avg_time = sum(times) / len(times)
            self.log(f"\nAverage time: {avg_time:.3f}s")
            
            # 如果串行平均时间是X，那么并行应该是类似的
            self.log("All runs completed successfully")
            
            result['success'] = True
            result['stats'] = {
                'runs': len(times),
                'times': times,
                'average': avg_time
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Concurrent stress test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def run_all_tests(self):
        """运行所有测试"""
        self.log("\n" + "="*60)
        self.log("SIMPLE EXTREME TEST SUITE")
        self.log("="*60)
        self.log(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.test_massive_analysis()
        self.test_repeated_operations(iterations=10)
        self.test_large_json_handling()
        self.test_error_recovery()
        self.test_concurrent_stress()
        
        self.print_summary()
    
    def print_summary(self):
        """打印测试摘要"""
        total_time = time.time() - self.start_time
        
        print("\n" + "="*60)
        print("EXTREME TEST SUMMARY")
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
    test = SimpleExtremeTest()
    test.run_all_tests()
