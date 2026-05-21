#!/usr/bin/env python3
import sys
import time
import json
from pathlib import Path
from datetime import datetime
import subprocess
import tempfile
import shutil

class StandaloneProductionTest:
    def __init__(self):
        self.results = []
        self.start_time = time.time()
    
    def log(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {message}")
    
    def log_error(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] ERROR: {message}")
    
    def run_ark_analyzer(self, project_path: Path, output_path: Path) -> dict:
        """运行ArkAnalyzer"""
        wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
        cmd = ['node', str(wrapper_path), str(project_path), str(output_path)]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            raise RuntimeError(f"ArkAnalyzer failed: {result.stderr}")
        
        with open(output_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def test_rapid_file_changes(self) -> dict:
        """测试快速文件变化"""
        self.log(f"\n{'='*60}")
        self.log("TEST 1: Rapid File Changes")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Rapid File Changes",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            temp_project = Path(tempfile.mkdtemp())
            
            times = []
            
            for i in range(10):
                # 创建/修改文件
                test_file = temp_project / f"Test{i}.ets"
                test_file.write_text(f"""
export class Test{i} {{
  method{i}() {{
    console.log('iteration {i}');
  }}
}}
""")
                
                # 立即分析
                temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
                temp_output.close()
                
                start = time.time()
                data = self.run_ark_analyzer(temp_project, Path(temp_output.name))
                elapsed = time.time() - start
                
                times.append(elapsed)
                self.log(f"  Change {i+1}: {elapsed:.3f}s, files={len(data.get('files', []))}")
                
                Path(temp_output.name).unlink(missing_ok=True)
            
            avg_time = sum(times) / len(times)
            self.log(f"Average time per change: {avg_time:.3f}s")
            
            shutil.rmtree(temp_project)
            
            result['success'] = avg_time < 5  # 应该小于5秒
            result['stats'] = {
                'changes': 10,
                'average_time': avg_time,
                'times': times
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Rapid file changes failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_large_project_batch(self) -> dict:
        """测试大型项目批量处理"""
        self.log(f"\n{'='*60}")
        self.log("TEST 2: Large Project Batch Processing")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Large Project Batch",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            # 测试不同规模的项目
            projects = [
                ('small', '/workspace/sample_project'),
                ('medium', '/workspace/realistic_test_project'),
                ('large', '/workspace/massive_test_project')
            ]
            
            batch_results = {}
            
            for size, project_path in projects:
                self.log(f"\n  Testing {size} project ({project_path})...")
                
                temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
                temp_output.close()
                
                start = time.time()
                data = self.run_ark_analyzer(Path(project_path), Path(temp_output.name))
                elapsed = time.time() - start
                
                json_size = Path(temp_output.name).stat().st_size / 1024
                
                batch_results[size] = {
                    'time': elapsed,
                    'files': len(data.get('files', [])),
                    'classes': len(data.get('classes', [])),
                    'methods': len(data.get('methods', [])),
                    'json_size': json_size
                }
                
                self.log(f"    Time: {elapsed:.2f}s, Files: {batch_results[size]['files']}, JSON: {json_size:.2f}KB")
                
                Path(temp_output.name).unlink(missing_ok=True)
            
            # 验证结果
            all_successful = all(r['files'] > 0 for r in batch_results.values())
            
            result['success'] = all_successful
            result['stats'] = batch_results
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Large project batch failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_data_consistency(self) -> dict:
        """测试数据一致性"""
        self.log(f"\n{'='*60}")
        self.log("TEST 3: Data Consistency")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Data Consistency",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            # 运行多次分析并比较结果
            runs = []
            
            for i in range(3):
                self.log(f"  Run {i+1}...")
                
                temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
                temp_output.close()
                
                data = self.run_ark_analyzer(Path('/workspace/realistic_test_project'), Path(temp_output.name))
                
                runs.append({
                    'files': len(data.get('files', [])),
                    'classes': len(data.get('classes', [])),
                    'methods': len(data.get('methods', [])),
                    'calls': len(data.get('calls', []))
                })
                
                Path(temp_output.name).unlink(missing_ok=True)
            
            # 检查一致性
            first_run = runs[0]
            all_same = all(r == first_run for r in runs)
            
            self.log(f"  Run 1: {runs[0]}")
            self.log(f"  Run 2: {runs[1]}")
            self.log(f"  Run 3: {runs[2]}")
            self.log(f"  Consistent: {all_same}")
            
            result['success'] = all_same
            result['stats'] = {
                'runs': runs,
                'consistent': all_same
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Data consistency failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_performance_stability(self) -> dict:
        """测试性能稳定性"""
        self.log(f"\n{'='*60}")
        self.log("TEST 4: Performance Stability")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Performance Stability",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            times = []
            
            for i in range(20):
                temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
                temp_output.close()
                
                start = time.time()
                self.run_ark_analyzer(Path('/workspace/realistic_test_project'), Path(temp_output.name))
                elapsed = time.time() - start
                
                times.append(elapsed)
                
                if (i + 1) % 5 == 0:
                    self.log(f"  Completed {i+1}/20 runs")
                
                Path(temp_output.name).unlink(missing_ok=True)
            
            avg = sum(times) / len(times)
            min_t = min(times)
            max_t = max(times)
            variance = max_t - min_t
            
            self.log(f"  Average: {avg:.3f}s")
            self.log(f"  Min: {min_t:.3f}s")
            self.log(f"  Max: {max_t:.3f}s")
            self.log(f"  Variance: {variance:.3f}s")
            
            # 性能应该在合理范围内波动
            stable = variance < avg * 0.5  # 波动小于平均值的50%
            
            result['success'] = stable
            result['stats'] = {
                'runs': 20,
                'average': avg,
                'min': min_t,
                'max': max_t,
                'variance': variance,
                'stable': stable
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Performance stability failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_json_export_integrity(self) -> dict:
        """测试JSON导出完整性"""
        self.log(f"\n{'='*60}")
        self.log("TEST 5: JSON Export Integrity")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "JSON Export Integrity",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            data = self.run_ark_analyzer(Path('/workspace/realistic_test_project'), Path(temp_output.name))
            
            # 检查数据结构
            required_keys = ['files', 'classes', 'methods', 'calls', 'components']
            missing_keys = [k for k in required_keys if k not in data]
            
            if missing_keys:
                self.log_error(f"Missing keys in JSON: {missing_keys}")
                result['success'] = False
                result['stats'] = {'missing_keys': missing_keys}
                return result
            
            # 检查数据完整性
            self.log(f"  Files: {len(data['files'])}")
            self.log(f"  Classes: {len(data['classes'])}")
            self.log(f"  Methods: {len(data['methods'])}")
            self.log(f"  Calls: {len(data['calls'])}")
            self.log(f"  Components: {len(data['components'])}")
            
            # 检查每个文件的结构
            if data['files']:
                sample_file = data['files'][0]
                file_keys = set(sample_file.keys())
                self.log(f"  Sample file keys: {file_keys}")
                
                required_file_keys = ['id', 'path', 'hash']
                missing_file_keys = [k for k in required_file_keys if k not in sample_file]
                
                if missing_file_keys:
                    self.log_warning(f"Missing file keys: {missing_file_keys}")
            
            # 检查类结构
            if data['classes']:
                sample_class = data['classes'][0]
                class_keys = set(sample_class.keys())
                self.log(f"  Sample class keys: {class_keys}")
            
            Path(temp_output.name).unlink(missing_ok=True)
            
            result['success'] = len(missing_keys) == 0
            result['stats'] = {
                'files': len(data['files']),
                'classes': len(data['classes']),
                'methods': len(data['methods']),
                'calls': len(data['calls']),
                'components': len(data['components'])
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"JSON export integrity failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def run_all_tests(self):
        """运行所有测试"""
        self.log("\n" + "="*60)
        self.log("STANDALONE PRODUCTION TEST SUITE")
        self.log("="*60)
        self.log(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.test_rapid_file_changes()
        self.test_large_project_batch()
        self.test_data_consistency()
        self.test_performance_stability()
        self.test_json_export_integrity()
        
        self.print_summary()
    
    def print_summary(self):
        """打印测试摘要"""
        total_time = time.time() - self.start_time
        
        print("\n" + "="*60)
        print("PRODUCTION TEST SUMMARY")
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
    test = StandaloneProductionTest()
    test.run_all_tests()
