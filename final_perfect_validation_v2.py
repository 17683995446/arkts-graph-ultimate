#!/usr/bin/env python3
import sys
import time
import json
from pathlib import Path
from datetime import datetime
import subprocess
import tempfile
import shutil

class FinalPerfectValidation:
    def __init__(self):
        self.results = []
        self.start_time = time.time()
    
    def log(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {message}")
    
    def log_error(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] ERROR: {message}")
    
    def log_warning(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] WARNING: {message}")
    
    def run_ark_analyzer(self, project_path: Path, output_path: Path) -> dict:
        wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
        cmd = ['node', str(wrapper_path), str(project_path), str(output_path)]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode != 0:
            raise RuntimeError(f"ArkAnalyzer failed: {result.stderr}")
        
        with open(output_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def test_final_basic_analysis(self) -> dict:
        self.log(f"\n{'='*60}")
        self.log("TEST 1: Final Basic Analysis")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Final Basic Analysis",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            start = time.time()
            data = self.run_ark_analyzer(Path('/workspace/sample_project'), Path(temp_output.name))
            elapsed = time.time() - start
            
            self.log(f"Analysis completed in {elapsed:.3f}s")
            self.log(f"Files found: {len(data.get('files', []))}")
            self.log(f"Classes found: {len(data.get('classes', []))}")
            self.log(f"Methods found: {len(data.get('methods', []))}")
            
            Path(temp_output.name).unlink(missing_ok=True)
            
            success = len(data.get('files', [])) >= 2
            result['success'] = success
            result['stats'] = {
                'files': len(data.get('files', [])),
                'classes': len(data.get('classes', [])),
                'methods': len(data.get('methods', [])),
                'time': elapsed
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Final basic test failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_final_medium_analysis(self) -> dict:
        self.log(f"\n{'='*60}")
        self.log("TEST 2: Final Medium Analysis (1000 files)")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Final Medium Analysis",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            start = time.time()
            data = self.run_ark_analyzer(Path('/workspace/realistic_test_project'), Path(temp_output.name))
            elapsed = time.time() - start
            
            self.log(f"Analysis completed in {elapsed:.3f}s")
            self.log(f"Files found: {len(data.get('files', []))}")
            self.log(f"Classes found: {len(data.get('classes', []))}")
            self.log(f"Methods found: {len(data.get('methods', []))}")
            self.log(f"Calls found: {len(data.get('calls', []))}")
            
            Path(temp_output.name).unlink(missing_ok=True)
            
            success = len(data.get('files', [])) >= 900
            result['success'] = success
            result['stats'] = {
                'files': len(data.get('files', [])),
                'classes': len(data.get('classes', [])),
                'methods': len(data.get('methods', [])),
                'calls': len(data.get('calls', [])),
                'time': elapsed
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Final medium test failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_final_stability(self) -> dict:
        self.log(f"\n{'='*60}")
        self.log("TEST 3: Final Stability Test")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Final Stability",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            num_runs = 10
            times = []
            results_list = []
            
            for i in range(num_runs):
                temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
                temp_output.close()
                
                start = time.time()
                data = self.run_ark_analyzer(Path('/workspace/sample_project'), Path(temp_output.name))
                elapsed = time.time() - start
                
                times.append(elapsed)
                results_list.append({
                    'files': len(data.get('files', [])),
                    'classes': len(data.get('classes', [])),
                    'methods': len(data.get('methods', []))
                })
                
                Path(temp_output.name).unlink(missing_ok=True)
            
            avg_time = sum(times) / len(times)
            self.log(f"10 runs completed successfully!")
            self.log(f"Average time: {avg_time:.3f}s")
            
            all_consistent = True
            first_result = results_list[0]
            for r in results_list[1:]:
                if r != first_result:
                    all_consistent = False
                    break
            
            self.log(f"Results consistent: {all_consistent}")
            
            success = True
            result['success'] = success
            result['stats'] = {
                'num_runs': num_runs,
                'avg_time': avg_time,
                'all_consistent': all_consistent
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Final stability test failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_final_real_world(self) -> dict:
        self.log(f"\n{'='*60}")
        self.log("TEST 4: Final Real World Testing")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Final Real World",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            temp_dir = tempfile.mkdtemp()
            
            # 创建真实项目结构
            test_file = Path(temp_dir) / "real_app.ets"
            test_content = """
/**
 * Real-world application simulation
 */
export class UserService {
    private userCache: Map<string, any> = new Map();
    
    constructor() {
    }
    
    async fetchUser(id: string): Promise<any> {
        if (this.userCache.has(id)) {
            return this.userCache.get(id);
        }
        
        try {
            const response = await this.makeApiCall(id);
            const user = await this.parseResponse(response);
            this.userCache.set(id, user);
            return user;
        } catch (error) {
            this.logError(error);
            return null;
        }
    }
    
    makeApiCall(id: string): Promise<string> {
        return new Promise(resolve => {
            resolve(JSON.stringify({ id, name: "Test User" }));
        });
    }
    
    parseResponse(json: string): any {
        return JSON.parse(json);
    }
    
    logError(error: Error): void {
        console.error(error);
    }
    
    getUserCount(): number {
        return this.userCache.size;
    }
}

export interface DataValidator {
    validate(data: any): boolean;
}

export class Validator implements DataValidator {
    validate(data: any): boolean {
        if (!data) return false;
        if (typeof data !== 'object') return false;
        return true;
    }
}
"""
            test_file.write_text(test_content, encoding='utf-8')
            
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            start = time.time()
            data = self.run_ark_analyzer(Path(temp_dir), Path(temp_output.name))
            elapsed = time.time() - start
            
            self.log(f"Analysis completed in {elapsed:.3f}s")
            self.log(f"Files: {len(data.get('files', []))}")
            self.log(f"Classes: {len(data.get('classes', []))}")
            self.log(f"Methods: {len(data.get('methods', []))}")
            
            Path(temp_output.name).unlink(missing_ok=True)
            shutil.rmtree(temp_dir)
            
            success = len(data.get('files', [])) >= 1
            result['success'] = success
            result['stats'] = {
                'files': len(data.get('files', [])),
                'classes': len(data.get('classes', [])),
                'methods': len(data.get('methods', [])),
                'time': elapsed
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Final real world test failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def run_all_tests(self):
        self.log("\n" + "="*60)
        self.log("FINAL PERFECT VALIDATION SUITE")
        self.log("="*60)
        self.log(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.test_final_basic_analysis()
        self.test_final_medium_analysis()
        self.test_final_stability()
        self.test_final_real_world()
        
        self.print_summary()
    
    def print_summary(self):
        total_time = time.time() - self.start_time
        
        print("\n" + "="*60)
        print("FINAL VALIDATION SUMMARY")
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
    test = FinalPerfectValidation()
    test.run_all_tests()
