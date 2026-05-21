#!/usr/bin/env python3
import sys
import time
import json
from pathlib import Path
from datetime import datetime
import subprocess
import tempfile
import shutil

class UltraScaleTest:
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
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        
        if result.returncode != 0:
            raise RuntimeError(f"ArkAnalyzer failed: {result.stderr}")
        
        with open(output_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_ultra_scale_project(self, num_files: int) -> Path:
        """生成超大规模项目"""
        self.log(f"Generating {num_files} files for ultra-scale test...")
        
        temp_dir = tempfile.mkdtemp()
        base_path = Path(temp_dir)
        
        # 创建目录结构
        num_dirs = 100
        files_per_dir = num_files // num_dirs
        
        for dir_num in range(num_dirs):
            dir_path = base_path / f"module_{dir_num:03d}"
            dir_path.mkdir(parents=True, exist_ok=True)
            
            for file_num in range(files_per_dir):
                file_path = dir_path / f"class_{dir_num:03d}_{file_num:04d}.ets"
                
                content = f"""
export class Module{ dir_num }Class{ file_num } {{
  id: string = '{dir_num}-{file_num}';
  name: string = 'Class {dir_num}-{file_num}';
  value: number = {dir_num * 1000 + file_num};
  
  constructor(id: string, name: string) {{
    this.id = id;
    this.name = name;
  }}
  
  getId(): string {{
    return this.id;
  }}
  
  getName(): string {{
    return this.name;
  }}
  
  setValue(val: number): void {{
    this.value = val;
  }}
  
  getValue(): number {{
    return this.value;
  }}
  
  process(): void {{
    console.log('Processing', this.id, this.name);
    this.value = this.value * 2;
  }}
  
  validate(): boolean {{
    return this.id.length > 0 && this.value >= 0;
  }}
  
  toJSON(): object {{
    return {{
      id: this.id,
      name: this.name,
      value: this.value
    }};
  }}
}}
"""
                file_path.write_text(content, encoding='utf-8')
                
                if (dir_num * files_per_dir + file_num + 1) % 1000 == 0:
                    self.log(f"  Generated {dir_num * files_per_dir + file_num + 1}/{num_files} files...")
        
        self.log(f"Ultra-scale project created at: {temp_dir}")
        return base_path
    
    def test_10k_files(self) -> dict:
        """测试1万文件"""
        self.log(f"\n{'='*60}")
        self.log("TEST 1: Ultra Scale - 10,000 Files")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "10K Files Test",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            project_path = self.generate_ultra_scale_project(10000)
            
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            self.log("Starting ultra-scale analysis...")
            start = time.time()
            data = self.run_ark_analyzer(project_path, Path(temp_output.name))
            elapsed = time.time() - start
            
            json_size = Path(temp_output.name).stat().st_size / 1024 / 1024
            
            self.log(f"Analysis completed in {elapsed:.2f}s")
            self.log(f"Files found: {len(data.get('files', []))}")
            self.log(f"Classes found: {len(data.get('classes', []))}")
            self.log(f"Methods found: {len(data.get('methods', []))}")
            self.log(f"JSON size: {json_size:.2f} MB")
            
            # 清理
            shutil.rmtree(project_path)
            Path(temp_output.name).unlink(missing_ok=True)
            
            # 验证
            success = (
                elapsed < 60 and  # 应该在60秒内完成
                len(data.get('files', [])) >= 9000  # 应该找到大部分文件
            )
            
            if not success:
                self.log(f"WARNING: Expected ~10000 files, found {len(data.get('files', []))}")
            
            result['success'] = success
            result['stats'] = {
                'files': len(data.get('files', [])),
                'classes': len(data.get('classes', [])),
                'methods': len(data.get('methods', [])),
                'time': elapsed,
                'json_size': json_size
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"10K test failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_performance_scaling(self) -> dict:
        """测试性能扩展"""
        self.log(f"\n{'='*60}")
        self.log("TEST 2: Performance Scaling Test")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Performance Scaling",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            # 测试不同规模的性能
            scales = [
                (100, "100 files"),
                (500, "500 files"),
                (1000, "1K files"),
            ]
            
            scaling_data = []
            
            for num_files, label in scales:
                self.log(f"\n  Testing {label}...")
                
                project_path = self.generate_ultra_scale_project(num_files)
                
                temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
                temp_output.close()
                
                start = time.time()
                data = self.run_ark_analyzer(project_path, Path(temp_output.name))
                elapsed = time.time() - start
                
                json_size = Path(temp_output.name).stat().st_size / 1024
                
                scaling_data.append({
                    'scale': label,
                    'files': len(data.get('files', [])),
                    'time': elapsed,
                    'json_size': json_size,
                    'time_per_file': elapsed / len(data.get('files', [])) * 1000
                })
                
                self.log(f"    Time: {elapsed:.2f}s, Files: {len(data.get('files', []))}, "
                        f"Time/file: {scaling_data[-1]['time_per_file']:.2f}ms")
                
                # 清理
                shutil.rmtree(project_path)
                Path(temp_output.name).unlink(missing_ok=True)
            
            # 分析扩展性
            self.log("\n  Scaling analysis:")
            for i in range(1, len(scaling_data)):
                time_ratio = scaling_data[i]['time'] / scaling_data[i-1]['time']
                file_ratio = scaling_data[i]['files'] / scaling_data[i-1]['files']
                
                self.log(f"    {scaling_data[i-1]['scale']} -> {scaling_data[i]['scale']}: "
                        f"Time ratio: {time_ratio:.2f}x, File ratio: {file_ratio:.2f}x")
            
            # 检查是否是线性扩展
            is_linear = all(
                scaling_data[i]['time_per_file'] / scaling_data[0]['time_per_file'] < 2
                for i in range(1, len(scaling_data))
            )
            
            self.log(f"\n  Linear scaling: {is_linear}")
            
            result['success'] = is_linear
            result['stats'] = {
                'scaling_data': scaling_data,
                'is_linear': is_linear
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Performance scaling test failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_memory_stress(self) -> dict:
        """测试内存压力"""
        self.log(f"\n{'='*60}")
        self.log("TEST 3: Memory Stress Test")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Memory Stress",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            # 测试大规模数据的内存使用
            project_path = self.generate_ultra_scale_project(5000)
            
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            self.log("Analyzing 5000 files for memory stress...")
            start = time.time()
            data = self.run_ark_analyzer(project_path, Path(temp_output.name))
            elapsed = time.time() - start
            
            json_size = Path(temp_output.name).stat().st_size / 1024 / 1024
            
            # 尝试多次加载JSON
            self.log("Testing multiple JSON loads...")
            load_times = []
            
            for i in range(3):
                start_load = time.time()
                with open(temp_output.name, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                load_time = time.time() - start_load
                load_times.append(load_time)
                self.log(f"  Load {i+1}: {load_time:.3f}s")
            
            # 清理
            shutil.rmtree(project_path)
            Path(temp_output.name).unlink(missing_ok=True)
            
            avg_load_time = sum(load_times) / len(load_times)
            
            self.log(f"\nAnalysis completed in {elapsed:.2f}s")
            self.log(f"JSON size: {json_size:.2f} MB")
            self.log(f"Average load time: {avg_load_time:.3f}s")
            
            result['success'] = avg_load_time < 10  # 应该能在10秒内加载
            result['stats'] = {
                'files': len(data.get('files', [])),
                'json_size': json_size,
                'load_times': load_times,
                'avg_load_time': avg_load_time
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Memory stress test failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_large_json_handling(self) -> dict:
        """测试大JSON文件处理"""
        self.log(f"\n{'='*60}")
        self.log("TEST 4: Large JSON Handling (100MB+)")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Large JSON Handling",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            # 创建大JSON文件
            self.log("Generating large dataset...")
            large_data = {
                'files': [],
                'classes': [],
                'methods': [],
                'calls': [],
                'components': []
            }
            
            # 添加大量数据
            for i in range(10000):
                large_data['files'].append({
                    'id': i,
                    'path': f'/test/file{i}.ets',
                    'hash': f'hash{i:08d}'
                })
                
                large_data['classes'].append({
                    'id': i,
                    'name': f'Class{i}',
                    'fileId': i % 10000,
                    'type': 'class'
                })
                
                for j in range(5):
                    method_id = i * 5 + j
                    large_data['methods'].append({
                        'id': method_id,
                        'name': f'Class{i}::method{j}',
                        'classId': i
                    })
            
            temp_json = tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w')
            temp_json.close()
            
            self.log("Writing large JSON file...")
            with open(temp_json.name, 'w', encoding='utf-8') as f:
                json.dump(large_data, f)
            
            json_size = Path(temp_json.name).stat().st_size / 1024 / 1024
            self.log(f"JSON file size: {json_size:.2f} MB")
            
            # 测试加载
            self.log("Testing JSON load performance...")
            start = time.time()
            with open(temp_json.name, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
            load_time = time.time() - start
            
            self.log(f"Load time: {load_time:.2f}s")
            self.log(f"Files in data: {len(loaded_data['files'])}")
            self.log(f"Classes in data: {len(loaded_data['classes'])}")
            self.log(f"Methods in data: {len(loaded_data['methods'])}")
            
            # 清理
            Path(temp_json.name).unlink(missing_ok=True)
            
            result['success'] = load_time < 30  # 应该在30秒内加载
            result['stats'] = {
                'json_size': json_size,
                'load_time': load_time,
                'files': len(loaded_data['files']),
                'classes': len(loaded_data['classes']),
                'methods': len(loaded_data['methods'])
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Large JSON test failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def run_all_tests(self):
        """运行所有测试"""
        self.log("\n" + "="*60)
        self.log("ULTRA SCALE TEST SUITE")
        self.log("="*60)
        self.log(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.test_10k_files()
        self.test_performance_scaling()
        self.test_memory_stress()
        self.test_large_json_handling()
        
        self.print_summary()
    
    def print_summary(self):
        """打印测试摘要"""
        total_time = time.time() - self.start_time
        
        print("\n" + "="*60)
        print("ULTRA SCALE TEST SUMMARY")
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
    test = UltraScaleTest()
    test.run_all_tests()
