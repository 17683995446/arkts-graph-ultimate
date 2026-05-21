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

# Add arkts_graph to path
sys.path.insert(0, str(Path(__file__).parent))

from arkts_graph.core.database import Database
from arkts_graph.core.ark_analyzer_integration import ArkAnalyzerIntegration


class ComprehensiveStressTest:
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
    
    def test_basic_analysis(self, project_path: Path, test_name: str = "Basic Analysis") -> dict:
        """Test basic ArkAnalyzer functionality"""
        self.log(f"\n{'='*60}")
        self.log(f"Running {test_name}...")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': test_name,
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'stats': None,
            'error': None
        }
        
        try:
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
            temp_db.close()
            
            # Run ArkAnalyzer
            wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
            cmd = ['node', str(wrapper_path), str(project_path), temp_output.name]
            self.log(f"Executing: {' '.join(cmd)}")
            
            start_ark = time.time()
            ark_result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            ark_time = time.time() - start_ark
            
            if ark_result.returncode != 0:
                raise RuntimeError(f"ArkAnalyzer failed: {ark_result.stderr}")
            
            self.log(f"ArkAnalyzer completed in {ark_time:.2f}s")
            
            # Load results
            with open(temp_output.name, 'r', encoding='utf-8') as f:
                analysis_data = json.load(f)
            
            stats = {
                'files': len(analysis_data.get('files', [])),
                'classes': len(analysis_data.get('classes', [])),
                'methods': len(analysis_data.get('methods', [])),
                'calls': len(analysis_data.get('calls', [])),
                'components': len(analysis_data.get('components', []))
            }
            
            self.log(f"Analysis stats: {stats}")
            
            # Test database integration
            self.log("Testing database integration...")
            db = Database(Path(temp_db.name))
            ark_integration = ArkAnalyzerIntegration(db)
            
            start_db = time.time()
            load_result = ark_integration.load_from_json(Path(temp_output.name))
            db_time = time.time() - start_db
            
            self.log(f"Database load completed in {db_time:.2f}s")
            self.log(f"DB load stats: {load_result}")
            
            # Verify database content
            with db._get_connection() as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM files")
                db_files = cursor.fetchone()[0]
                cursor = conn.execute("SELECT COUNT(*) FROM classes")
                db_classes = cursor.fetchone()[0]
                cursor = conn.execute("SELECT COUNT(*) FROM methods")
                db_methods = cursor.fetchone()[0]
                cursor = conn.execute("SELECT COUNT(*) FROM calls")
                db_calls = cursor.fetchone()[0]
            
            self.log(f"DB verification: files={db_files}, classes={db_classes}, methods={db_methods}, calls={db_calls}")
            
            result['success'] = True
            result['stats'] = {
                'analysis': stats,
                'db': {
                    'files': db_files,
                    'classes': db_classes,
                    'methods': db_methods,
                    'calls': db_calls
                },
                'times': {
                    'arkanalyzer': ark_time,
                    'database': db_time
                }
            }
            
            # Cleanup
            Path(temp_output.name).unlink(missing_ok=True)
            Path(temp_db.name).unlink(missing_ok=True)
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"{test_name} failed", e)
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_multiple_runs(self, project_path: Path, num_runs: int = 10) -> dict:
        """Test running analysis multiple times to check for stability"""
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
                
                wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
                cmd = ['node', str(wrapper_path), str(project_path), temp_output.name]
                
                start = time.time()
                ark_result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                elapsed = time.time() - start
                
                if ark_result.returncode != 0:
                    raise RuntimeError(f"Run {i+1} failed: {ark_result.stderr}")
                
                with open(temp_output.name, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
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
            
            # Check consistency
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
    
    def test_database_transactions(self, project_path: Path) -> dict:
        """Test database transaction handling"""
        self.log(f"\n{'='*60}")
        self.log("Testing Database Transactions...")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Database Transactions",
            'success': False,
            'start_time': time.time(),
            'end_time': None,
            'stats': None,
            'error': None
        }
        
        try:
            temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
            temp_db.close()
            
            db = Database(Path(temp_db.name))
            
            # First, load some data
            self.log("Loading initial data...")
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
            cmd = ['node', str(wrapper_path), str(project_path), temp_output.name]
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=300)
            
            ark_integration = ArkAnalyzerIntegration(db)
            ark_integration.load_from_json(Path(temp_output.name))
            
            # Get initial counts
            with db._get_connection() as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM files")
                initial_files = cursor.fetchone()[0]
                cursor = conn.execute("SELECT COUNT(*) FROM classes")
                initial_classes = cursor.fetchone()[0]
            
            self.log(f"Initial: {initial_files} files, {initial_classes} classes")
            
            # Test clear_all
            self.log("Testing clear_all...")
            db.clear_all()
            
            with db._get_connection() as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM files")
                cleared_files = cursor.fetchone()[0]
                cursor = conn.execute("SELECT COUNT(*) FROM classes")
                cleared_classes = cursor.fetchone()[0]
            
            if cleared_files != 0 or cleared_classes != 0:
                raise RuntimeError(f"clear_all failed: files={cleared_files}, classes={cleared_classes}")
            
            self.log("clear_all successful")
            
            # Reload and verify
            self.log("Reloading data...")
            ark_integration.load_from_json(Path(temp_output.name))
            
            with db._get_connection() as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM files")
                final_files = cursor.fetchone()[0]
                cursor = conn.execute("SELECT COUNT(*) FROM classes")
                final_classes = cursor.fetchone()[0]
            
            self.log(f"Final: {final_files} files, {final_classes} classes")
            
            if final_files != initial_files or final_classes != initial_classes:
                self.log_warning("Counts mismatch after reload")
            
            result['success'] = True
            result['stats'] = {
                'initial_files': initial_files,
                'initial_classes': initial_classes,
                'final_files': final_files,
                'final_classes': final_classes
            }
            
            Path(temp_output.name).unlink(missing_ok=True)
            Path(temp_db.name).unlink(missing_ok=True)
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error("Database transactions test failed", e)
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
            
            # Test 1: Empty directory
            self.log("Test 1: Empty directory")
            temp_output1 = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output1.close()
            
            wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
            cmd = ['node', str(wrapper_path), str(temp_path), temp_output1.name]
            ark_result = subprocess.run(cmd, capture_output=True, text=True)
            
            with open(temp_output1.name, 'r', encoding='utf-8') as f:
                data1 = json.load(f)
            
            self.log(f"  Empty dir result: {len(data1.get('files', []))} files")
            Path(temp_output1.name).unlink(missing_ok=True)
            
            # Test 2: Single file with minimal content
            self.log("Test 2: Single minimal file")
            minimal_file = temp_path / "minimal.ets"
            with open(minimal_file, 'w', encoding='utf-8') as f:
                f.write("// Empty file\n")
            
            temp_output2 = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output2.close()
            
            cmd = ['node', str(wrapper_path), str(temp_path), temp_output2.name]
            ark_result = subprocess.run(cmd, capture_output=True, text=True)
            
            with open(temp_output2.name, 'r', encoding='utf-8') as f:
                data2 = json.load(f)
            
            self.log(f"  Minimal file result: {len(data2.get('files', []))} files")
            Path(temp_output2.name).unlink(missing_ok=True)
            
            # Test 3: File with special characters
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
            
            cmd = ['node', str(wrapper_path), str(temp_path), temp_output3.name]
            ark_result = subprocess.run(cmd, capture_output=True, text=True)
            
            with open(temp_output3.name, 'r', encoding='utf-8') as f:
                data3 = json.load(f)
            
            self.log(f"  Special chars result: {len(data3.get('classes', []))} classes")
            Path(temp_output3.name).unlink(missing_ok=True)
            
            # Cleanup
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
        """Run all comprehensive tests"""
        self.log("\n" + "="*60)
        self.log("COMPREHENSIVE STRESS TEST SUITE")
        self.log("="*60)
        self.log(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"Project path: {project_path}")
        
        # Run tests
        self.test_basic_analysis(project_path)
        self.test_multiple_runs(project_path, num_runs=5)
        self.test_database_transactions(project_path)
        self.test_edge_cases()
        
        # Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
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
                print(f"  - {err[:100]}...")
        
        if self.warnings:
            print(f"\nWARNINGS ({len(self.warnings)}):")
            for warn in self.warnings:
                print(f"  - {warn[:100]}...")
        
        print("\nDetailed results:")
        for result in self.results:
            status = "✓ SUCCESS" if result['success'] else "✗ FAILED"
            duration = result['end_time'] - result['start_time'] if result['end_time'] else 'N/A'
            print(f"  {result['test_name']}: {status} ({duration:.2f}s)")


if __name__ == '__main__':
    test = ComprehensiveStressTest()
    test.run_all_tests(Path('/workspace/realistic_test_project'))
