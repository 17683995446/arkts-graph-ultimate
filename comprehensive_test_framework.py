#!/usr/bin/env python3
import sys
import time
import json
from pathlib import Path
from datetime import datetime
import subprocess
import tempfile
import shutil
import random
import signal

class ComprehensiveTestFramework:
    def __init__(self):
        self.results = []
        self.start_time = time.time()
        self.all_passed = True
    
    def log(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {message}")
    
    def log_error(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] ERROR: {message}")
        self.all_passed = False
    
    def log_warning(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] WARNING: {message}")
    
    def run_ark_analyzer(self, project_path: Path, output_path: Path) -> dict:
        """运行ArkAnalyzer"""
        wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
        cmd = ['node', str(wrapper_path), str(project_path), str(output_path)]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode != 0:
            raise RuntimeError(f"ArkAnalyzer failed: {result.stderr}")
        
        with open(output_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def test_extreme_file_sizes(self) -> dict:
        """测试极端文件大小"""
        self.log(f"\n{'='*60}")
        self.log("TEST 1: Extreme File Sizes")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Extreme File Sizes",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            temp_dir = tempfile.mkdtemp()
            
            # 创建极小文件（1行代码）
            tiny_file = Path(temp_dir) / "tiny.ets"
            tiny_file.write_text("export class Tiny { }", encoding='utf-8')
            
            # 创建大文件（1MB代码）
            large_file = Path(temp_dir) / "large.ets"
            large_content = "export class Large {\n"
            for i in range(20000):
                large_content += f"  method{i}(): void {{ console.log('test'); }}\n"
            large_content += "}"
            large_file.write_text(large_content, encoding='utf-8')
            
            # 创建混合大小的多个文件
            for i in range(50):
                file_path = Path(temp_dir) / f"mixed_{i}.ets"
                if i % 5 == 0:
                    # 大文件
                    content = "export class MixedClass {\n"
                    for j in range(1000):
                        content += f"  func{j}() {{ }}\n"
                    content += "}"
                else:
                    # 小文件
                    content = f"export class Mixed{i} {{ method() {{ }} }}"
                file_path.write_text(content, encoding='utf-8')
            
            self.log("Created files with extreme sizes")
            
            # 分析
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            start = time.time()
            data = self.run_ark_analyzer(Path(temp_dir), Path(temp_output.name))
            elapsed = time.time() - start
            
            self.log(f"Analysis completed in {elapsed:.2f}s")
            self.log(f"Files found: {len(data.get('files', []))}")
            self.log(f"Classes found: {len(data.get('classes', []))}")
            
            # 清理
            shutil.rmtree(temp_dir)
            Path(temp_output.name).unlink(missing_ok=True)
            
            success = len(data.get('files', [])) >= 50
            if not success:
                self.log_warning(f"Expected at least 52 files, found {len(data.get('files', []))}")
            
            result['success'] = success
            result['stats'] = {
                'files': len(data.get('files', [])),
                'classes': len(data.get('classes', [])),
                'time': elapsed
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Extreme file sizes test failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_rapid_successive_analyses(self) -> dict:
        """测试快速连续分析"""
        self.log(f"\n{'='*60}")
        self.log("TEST 2: Rapid Successive Analyses")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Rapid Successive Analyses",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            num_runs = 20
            times = []
            
            self.log(f"Running {num_runs} successive analyses...")
            
            for i in range(num_runs):
                temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
                temp_output.close()
                
                start = time.time()
                data = self.run_ark_analyzer(Path('/workspace/sample_project'), Path(temp_output.name))
                elapsed = time.time() - start
                
                times.append(elapsed)
                
                if (i + 1) % 5 == 0:
                    self.log(f"  Completed {i+1}/{num_runs} runs, last: {elapsed:.3f}s")
                
                Path(temp_output.name).unlink(missing_ok=True)
            
            avg_time = sum(times) / len(times)
            max_time = max(times)
            min_time = min(times)
            variance = max_time - min_time
            
            self.log(f"\nAverage time: {avg_time:.3f}s")
            self.log(f"Min time: {min_time:.3f}s")
            self.log(f"Max time: {max_time:.3f}s")
            self.log(f"Variance: {variance:.3f}s")
            
            # 检查性能稳定性
            stable = variance < avg_time * 0.5
            if not stable:
                self.log_warning("Performance variance exceeds 50%")
            
            result['success'] = stable
            result['stats'] = {
                'num_runs': num_runs,
                'avg_time': avg_time,
                'min_time': min_time,
                'max_time': max_time,
                'variance': variance,
                'stable': stable
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Rapid analyses test failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_unicode_encoding(self) -> dict:
        """测试各种Unicode编码"""
        self.log(f"\n{'='*60}")
        self.log("TEST 3: Unicode Encoding Test")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Unicode Encoding",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            temp_dir = tempfile.mkdtemp()
            
            # 创建包含各种Unicode字符的文件
            unicode_file = Path(temp_dir) / "unicode_test.ets"
            unicode_content = """
export class UnicodeTest {
  chinese_name: string = "测试";
  japanese_name: string = "日本語";
  korean_name: string = "한국어";
  arabic_name: string = "العربية";
  emoji: string = "🚀💻📱🎨";
  cyrillic: string = "Русский";
  special: string = "©®™§¶†‡";
  math: string = "∞±×÷≠≤≥";
  
  method_with_unicode(): void {
    const greeting = "Hello 你好 こんにちは 안녕하세요";
    console.log(greeting);
  }
  
  process_text(): string {
    return "Unicode处理成功！";
  }
}
"""
            unicode_file.write_text(unicode_content, encoding='utf-8')
            
            # 创建包含中文类名和方法名的文件
            chinese_file = Path(temp_dir) / "chinese.ets"
            chinese_content = """
export class 用户管理 {
  private 用户列表: string[] = [];
  
  添加用户(姓名: string): void {
    this.用户列表.push(姓名);
  }
  
  获取用户数量(): number {
    return this.用户列表.length;
  }
  
  清空用户(): void {
    this.用户列表 = [];
  }
}
"""
            chinese_file.write_text(chinese_content, encoding='utf-8')
            
            # 创建包含混合编码的文件
            mixed_file = Path(temp_dir) / "mixed.ets"
            mixed_content = """
export class MixedEncoding {
  greetEveryone(): void {
    console.log("Hello World!");
    console.log("你好世界！");
    console.log("Bonjour le monde!");
    console.log("Hola Mundo!");
  }
  
  calculateSum(a: number, b: number): number {
    return a + b; // 这是中文注释
  }
}
"""
            mixed_file.write_text(mixed_content, encoding='utf-8')
            
            self.log("Created Unicode test files")
            
            # 分析
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            start = time.time()
            data = self.run_ark_analyzer(Path(temp_dir), Path(temp_output.name))
            elapsed = time.time() - start
            
            self.log(f"Analysis completed in {elapsed:.2f}s")
            self.log(f"Files found: {len(data.get('files', []))}")
            self.log(f"Classes found: {len(data.get('classes', []))}")
            self.log(f"Methods found: {len(data.get('methods', []))}")
            
            # 清理
            shutil.rmtree(temp_dir)
            Path(temp_output.name).unlink(missing_ok=True)
            
            success = len(data.get('files', [])) == 3
            if not success:
                self.log_warning(f"Expected 3 files, found {len(data.get('files', []))}")
            
            result['success'] = success
            result['stats'] = {
                'files': len(data.get('files', [])),
                'classes': len(data.get('classes', [])),
                'methods': len(data.get('methods', [])),
                'time': elapsed
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Unicode test failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_empty_and_near_empty_projects(self) -> dict:
        """测试空项目和几乎空的项目"""
        self.log(f"\n{'='*60}")
        self.log("TEST 4: Empty and Near-Empty Projects")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Empty Projects",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            # 测试完全空的目录
            self.log("Testing completely empty directory...")
            empty_dir = tempfile.mkdtemp()
            
            temp_output1 = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output1.close()
            
            data1 = self.run_ark_analyzer(Path(empty_dir), Path(temp_output1.name))
            
            self.log(f"Empty project: {len(data1.get('files', []))} files found")
            
            # 测试只有注释的文件
            self.log("\nTesting only comments file...")
            comment_dir = tempfile.mkdtemp()
            comment_file = Path(comment_dir) / "only_comments.ets"
            comment_content = """
// This is a comment
/* Multi-line comment */
// Still a comment
// No actual code here
"""
            comment_file.write_text(comment_content, encoding='utf-8')
            
            temp_output2 = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output2.close()
            
            data2 = self.run_ark_analyzer(Path(comment_dir), Path(temp_output2.name))
            
            self.log(f"Comments only: {len(data2.get('files', []))} files, "
                    f"{len(data2.get('classes', []))} classes")
            
            # 测试只有变量声明的文件
            self.log("\nTesting only variables file...")
            var_dir = tempfile.mkdtemp()
            var_file = Path(var_dir) / "only_vars.ets"
            var_content = """
const a = 1;
let b = "test";
var c = true;
const d: number = 42;
// No classes or functions
"""
            var_file.write_text(var_content, encoding='utf-8')
            
            temp_output3 = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output3.close()
            
            data3 = self.run_ark_analyzer(Path(var_dir), Path(temp_output3.name))
            
            self.log(f"Vars only: {len(data3.get('files', []))} files, "
                    f"{len(data3.get('classes', []))} classes")
            
            # 清理
            shutil.rmtree(empty_dir)
            shutil.rmtree(comment_dir)
            shutil.rmtree(var_dir)
            Path(temp_output1.name).unlink(missing_ok=True)
            Path(temp_output2.name).unlink(missing_ok=True)
            Path(temp_output3.name).unlink(missing_ok=True)
            
            success = (len(data1.get('files', [])) == 0 and 
                      len(data2.get('files', [])) == 1 and 
                      len(data3.get('files', [])) == 1)
            
            result['success'] = success
            result['stats'] = {
                'empty_project': len(data1.get('files', [])),
                'comments_only': len(data2.get('files', [])),
                'vars_only': len(data3.get('files', []))
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Empty projects test failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_special_characters_in_names(self) -> dict:
        """测试名称中的特殊字符"""
        self.log(f"\n{'='*60}")
        self.log("TEST 5: Special Characters in Names")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Special Character Names",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            temp_dir = tempfile.mkdtemp()
            
            # 创建包含各种特殊字符的文件
            special_file = Path(temp_dir) / "special_names.ets"
            special_content = """
export class ClassWithNumbers123 {
  method_with_underscores(): void { }
  methodWithCamelCase(): void { }
  _privateMethod(): void { }
  methodWith$Dollar(): void { }
  $prefixMethod(): void { }
}

// File names with special characters
export interface MyInterface {
  data: any;
}

// Numbers in names
export type Type123 = string;
const var_2024 = 2024;
"""
            special_file.write_text(special_content, encoding='utf-8')
            
            # 创建包含各种文件命名方式的项目
            for i in range(10):
                # 不同的文件命名风格
                file_names = [
                    f"camelCase{123}.ets",
                    f"PascalCase{i}.ets",
                    f"snake_case_{i}.ets",
                    f"mixed_123_Case.ets"
                ]
                
                for fn in file_names:
                    file_path = Path(temp_dir) / fn
                    file_content = f"export class {fn.replace('.ets', '')} {{ method() {{ }} }}"
                    file_path.write_text(file_content, encoding='utf-8')
            
            self.log("Created special character test files")
            
            # 分析
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            start = time.time()
            data = self.run_ark_analyzer(Path(temp_dir), Path(temp_output.name))
            elapsed = time.time() - start
            
            self.log(f"Analysis completed in {elapsed:.2f}s")
            self.log(f"Files found: {len(data.get('files', []))}")
            self.log(f"Classes found: {len(data.get('classes', []))}")
            
            # 清理
            shutil.rmtree(temp_dir)
            Path(temp_output.name).unlink(missing_ok=True)
            
            success = len(data.get('files', [])) >= 40
            if not success:
                self.log_warning(f"Expected at least 41 files, found {len(data.get('files', []))}")
            
            result['success'] = success
            result['stats'] = {
                'files': len(data.get('files', [])),
                'classes': len(data.get('classes', [])),
                'time': elapsed
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Special character names test failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_code_with_comments_and_whitespace(self) -> dict:
        """测试包含大量注释和空白的代码"""
        self.log(f"\n{'='*60}")
        self.log("TEST 6: Comments and Whitespace")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Comments and Whitespace",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            temp_dir = tempfile.mkdtemp()
            
            # 创建包含大量注释和空白的文件
            comment_heavy = Path(temp_dir) / "comments.ets"
            heavy_content = """
/**
 * This is a very large multi-line comment
 * that spans multiple lines
 * and contains a lot of text
 * 
 * More description here
 * And even more here
 */
export class CommentedClass {
  /**
   * This method does something important
   * @param x A number parameter
   * @param y Another number parameter
   * @returns The sum
   */
  methodWithLotsOfComments(x: number, y: number): number {
    // This is a comment
    // And another one
    // And one more
    const result = x + y;
    
    /* This is a
       multi-line
       comment */
    
    return result; // Return the result
  }
  
  // Empty lines
  
  anotherMethod(): void {
  }
}
"""
            comment_heavy.write_text(heavy_content, encoding='utf-8')
            
            # 创建包含大量空白的文件
            whitespace_heavy = Path(temp_dir) / "whitespace.ets"
            whitespace_content = """


export class WhitespaceClass {


  method1(): void {


  }


  method2(): void {

  }

}



"""
            whitespace_heavy.write_text(whitespace_content, encoding='utf-8')
            
            # 创建混合的文件
            for i in range(5):
                file_path = Path(temp_dir) / f"mixed_{i}.ets"
                content = f"""
// Lots of comments
export class Mixed{i} {{
  
  // Comment
  method1() {{ }}
  
  // Another comment
  method2() {{ }}
}}
"""
                file_path.write_text(content, encoding='utf-8')
            
            self.log("Created comment and whitespace test files")
            
            # 分析
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            start = time.time()
            data = self.run_ark_analyzer(Path(temp_dir), Path(temp_output.name))
            elapsed = time.time() - start
            
            self.log(f"Analysis completed in {elapsed:.2f}s")
            self.log(f"Files found: {len(data.get('files', []))}")
            self.log(f"Classes found: {len(data.get('classes', []))}")
            
            # 清理
            shutil.rmtree(temp_dir)
            Path(temp_output.name).unlink(missing_ok=True)
            
            success = len(data.get('files', [])) == 7
            if not success:
                self.log_warning(f"Expected 7 files, found {len(data.get('files', []))}")
            
            result['success'] = success
            result['stats'] = {
                'files': len(data.get('files', [])),
                'classes': len(data.get('classes', [])),
                'time': elapsed
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Comments and whitespace test failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_various_project_structures(self) -> dict:
        """测试各种项目结构"""
        self.log(f"\n{'='*60}")
        self.log("TEST 7: Various Project Structures")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Project Structures",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            temp_dir = tempfile.mkdtemp()
            
            # 扁平结构
            flat_dir = Path(temp_dir) / "flat"
            flat_dir.mkdir()
            for i in range(20):
                file_path = flat_dir / f"file_{i}.ets"
                file_path.write_text(f"export class Flat{i} {{ method() {{ }} }}", encoding='utf-8')
            
            # 深层嵌套结构
            deep_dir = Path(temp_dir) / "deep"
            current = deep_dir
            for i in range(20):
                current = current / f"level_{i}"
                current.mkdir(parents=True, exist_ok=True)
                for j in range(2):
                    file_path = current / f"file_{j}.ets"
                    file_path.write_text(f"export class Deep{i}{j} {{ method() {{ }} }}", encoding='utf-8')
            
            # 混合结构
            mix_dir = Path(temp_dir) / "mixed"
            mix_dir.mkdir()
            for i in range(5):
                subdir = mix_dir / f"dir_{i}"
                subdir.mkdir()
                for j in range(3):
                    file_path = subdir / f"file_{j}.ets"
                    file_path.write_text(f"export class Mix{i}{j} {{ method() {{ }} }}", encoding='utf-8')
            
            self.log("Created various project structures")
            
            # 分析
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            start = time.time()
            data = self.run_ark_analyzer(Path(temp_dir), Path(temp_output.name))
            elapsed = time.time() - start
            
            self.log(f"Analysis completed in {elapsed:.2f}s")
            self.log(f"Files found: {len(data.get('files', []))}")
            self.log(f"Classes found: {len(data.get('classes', []))}")
            
            # 清理
            shutil.rmtree(temp_dir)
            Path(temp_output.name).unlink(missing_ok=True)
            
            success = len(data.get('files', [])) >= 60
            if not success:
                self.log_warning(f"Expected at least 60 files, found {len(data.get('files', []))}")
            
            result['success'] = success
            result['stats'] = {
                'files': len(data.get('files', [])),
                'classes': len(data.get('classes', [])),
                'time': elapsed
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Project structures test failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def run_all_tests(self):
        """运行所有测试"""
        self.log("\n" + "="*60)
        self.log("COMPREHENSIVE TEST FRAMEWORK")
        self.log("="*60)
        self.log(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.test_extreme_file_sizes()
        self.test_rapid_successive_analyses()
        self.test_unicode_encoding()
        self.test_empty_and_near_empty_projects()
        self.test_special_characters_in_names()
        self.test_code_with_comments_and_whitespace()
        self.test_various_project_structures()
        
        self.print_summary()
    
    def print_summary(self):
        """打印测试摘要"""
        total_time = time.time() - self.start_time
        
        print("\n" + "="*60)
        print("COMPREHENSIVE TEST SUMMARY")
        print("="*60)
        print(f"Total time: {total_time:.2f}s")
        print(f"Tests run: {len(self.results)}")
        
        success_count = sum(1 for r in self.results if r['success'])
        print(f"Successful: {success_count}/{len(self.results)}")
        
        if not self.all_passed:
            print("\n⚠️ Some issues were found!")
        
        print("\nDetailed results:")
        for result in self.results:
            status = "✓ SUCCESS" if result['success'] else "✗ FAILED"
            duration = result['end_time'] - result['start_time'] if result['end_time'] else 'N/A'
            print(f"  {result['test_name']}: {status} ({duration:.2f}s)")

if __name__ == '__main__':
    test = ComprehensiveTestFramework()
    test.run_all_tests()
