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


class SimpleStressTest:
    def __init__(self):
        self.results = []
        self.start_time = time.time()
        self.errors = []
        self.warnings = []
    
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
    
    def run_ark_analyzer(self, project_path: Path, output_path: Path) -> dict:
        """Run ArkAnalyzer and return results"""
        wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
        cmd = ['node', str(wrapper_path), str(project_path), str(output_path)]
        
        self.log(f"Executing: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            raise RuntimeError(f"ArkAnalyzer failed: {result.stderr}")
        
        with open(output_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def test_basic_analysis(self, project_path: Path) -> dict:
        """Test basic ArkAnalyzer functionality"""
        self.log(f"\n{'='*60}")
        self.log("Running Basic Analysis Test...")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Basic Analysis",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'stats': None,
            'error': None
        }
        
        try:
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            start_ark = time.time()
            analysis_data = self.run_ark_analyzer(project_path, Path(temp_output.name))
            ark_time = time.time() - start_ark
            
            self.log(f"ArkAnalyzer completed in {ark_time:.2f}s")
            
            stats = {
                'files': len(analysis_data.get('files', [])),
                'classes': len(analysis_data.get('classes', [])),
                'methods': len(analysis_data.get('methods', [])),
                'calls': len(analysis_data.get('calls', [])),
                'components': len(analysis_data.get('components', []))
            }
            
            self.log(f"Analysis stats: {stats}")
            
            if stats['files'] == 0:
                self.log_warning("No files found!")
            
            result['success'] = True
            result['stats'] = {
                'analysis': stats,
                'times': {
                    'arkanalyzer': ark_time
                }
            }
            
            Path(temp_output.name).unlink(missing_ok=True)
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Basic Analysis test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_multiple_runs(self, project_path: Path, num_runs: int = 10) -> dict:
        """Test running analysis multiple times"""
        self.log(f"\n{'='*60}")
        self.log(f"Running Multiple Runs Test ({num_runs} runs)...")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': f"Multiple Runs ({num_runs}x)",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'stats': None,
            'error': None,
            'runs': []
        }
        
        try:
            times = []
            stats_list = []
            
            for i in range(num_runs):
                self.log(f"Run {i+1}/{num_runs}")
                
                temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
                temp_output.close()
                
                start = time.time()
                data = self.run_ark_analyzer(project_path, Path(temp_output.name))
                elapsed = time.time() - start
                
                stats = {
                    'files': len(data.get('files', [])),
                    'classes': len(data.get('classes', [])),
                    'methods': len(data.get('methods', [])),
                    'calls': len(data.get('calls', []))
                }
                
                times.append(elapsed)
                stats_list.append(stats)
                
                result['runs'].append({
                    'run': i+1,
                    'time': elapsed,
                    'stats': stats
                })
                
                self.log(f"  Run {i+1}: {elapsed:.2f}s, stats={stats}")
                
                Path(temp_output.name).unlink(missing_ok=True)
            
            if len(stats_list) > 1:
                first = stats_list[0]
                consistent = True
                for i, stats in enumerate(stats_list[1:], 2):
                    if stats != first:
                        self.log_warning(f"Run {i} has inconsistent stats: {stats} vs {first}")
                        consistent = False
                
                if not consistent:
                    self.log_warning("Inconsistent results across runs!")
            
            avg_time = sum(times) / len(times)
            max_time = max(times)
            min_time = min(times)
            
            self.log(f"\nAverage time: {avg_time:.2f}s (min: {min_time:.2f}s, max: {max_time:.2f}s)")
            
            result['success'] = True
            result['stats'] = {
                'avg_time': avg_time,
                'min_time': min_time,
                'max_time': max_time,
                'consistent': len(set(str(s) for s in stats_list)) == 1
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Multiple runs test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_edge_cases(self) -> dict:
        """Test various edge cases"""
        self.log(f"\n{'='*60}")
        self.log("Testing Edge Cases...")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Edge Cases",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'stats': None,
            'error': None
        }
        
        try:
            temp_dir = tempfile.mkdtemp()
            temp_path = Path(temp_dir)
            
            self.log("Test 1: Empty directory")
            temp_output1 = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output1.close()
            data1 = self.run_ark_analyzer(temp_path, Path(temp_output1.name))
            self.log(f"  Empty dir result: {len(data1.get('files', []))} files")
            Path(temp_output1.name).unlink(missing_ok=True)
            
            self.log("Test 2: Single minimal file")
            minimal_file = temp_path / "minimal.ets"
            with open(minimal_file, 'w', encoding='utf-8') as f:
                f.write("// Empty file\n")
            
            temp_output2 = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output2.close()
            data2 = self.run_ark_analyzer(temp_path, Path(temp_output2.name))
            self.log(f"  Minimal file result: {len(data2.get('files', []))} files")
            Path(temp_output2.name).unlink(missing_ok=True)
            
            self.log("Test 3: Special characters")
            special_file = temp_path / "special_chars.ets"
            with open(special_file, 'w', encoding='utf-8') as f:
                f.write("""
export class TestClass {
  testMethod() {
    const s = "Special chars: 测试 こんにちは \u00e9\u00f1";
    console.log(s);
  }
}
""")
            
            temp_output3 = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output3.close()
            data3 = self.run_ark_analyzer(temp_path, Path(temp_output3.name))
            self.log(f"  Special chars result: {len(data3.get('classes', []))} classes")
            Path(temp_output3.name).unlink(missing_ok=True)
            
            shutil.rmtree(temp_dir)
            
            result['success'] = True
            result['stats'] = {
                'empty_dir_files': len(data1.get('files', [])),
                'minimal_file_files': len(data2.get('files', [])),
                'special_chars_classes': len(data3.get('classes', []))
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Edge cases test failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def run_all_tests(self, project_path: Path):
        self.log("\n" + "="*60)
        self.log("SIMPLE STRESS TEST SUITE")
        self.log("="*60)
        self.log(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"Project path: {project_path}")
        
        self.test_basic_analysis(project_path)
        self.test_multiple_runs(project_path, num_runs=5)
        self.test_edge_cases()
        
        self.print_summary()
    
    def print_summary(self):
        total_time = time.time() - self.start_time
        
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Total time: {total_time:.2f}s")
        print(f"Tests run: {len(self.results)}")
        
        success_count = sum(1 for r in self.results if r['success'])
        print(f"Successful: {success_count}/{len(self.results)}")
        
        if self.errors:
            print(f"\nERRORS ({len(self.errors)}):")
            for err in self.errors:
                print(f"  - {err[:200]}")
        
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
    test = SimpleStressTest()
    test.run_all_tests(Path('/workspace/realistic_test_project'))
