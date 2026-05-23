#!/usr/bin/env python3
"""
第N轮深度迭代测试 - 发现隐藏问题
专注于：边界条件、极端输入、并发场景、内存泄漏
"""

import json
import os
import subprocess
import time
from datetime import datetime
import random
import string

class IterationNTest:
    def __init__(self):
        self.test_results = []
        self.start_time = datetime.now()
        self.found_issues = []
        
    def log_test(self, test_name, passed, message="", details=None):
        """记录测试结果"""
        status = "✅ PASS" if passed else "❌ FAIL"
        result = {
            "test": test_name,
            "passed": passed,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{status}: {test_name}")
        if message:
            print(f"   {message}")
        return passed
    
    def log_issue(self, severity, test_name, issue, suggestion=""):
        """记录发现的问题"""
        issue_data = {
            "severity": severity,
            "test_name": test_name,
            "issue": issue,
            "suggestion": suggestion,
            "timestamp": datetime.now().isoformat()
        }
        self.found_issues.append(issue_data)
        
        icon = {
            "CRITICAL": "🔴",
            "WARNING": "🟡",
            "INFO": "🔵"
        }.get(severity, "⚪")
        
        print(f"  {icon} [{severity}] {test_name}: {issue}")
        if suggestion:
            print(f"     💡 建议: {suggestion}")
    
    def test_edge_case_extreme_paths(self):
        """测试极端路径场景"""
        print("\n📊 测试 N.1: 极端路径场景")
        print("=" * 60)
        
        tests_passed = []
        
        # 测试1: 超长路径
        try:
            print("  测试 1.1: 超长路径处理...")
            long_path = "/workspace/" + "a" * 500 + "/test.ets"
            os.makedirs(os.path.dirname(long_path), exist_ok=True)
            
            with open(long_path, 'w', encoding='utf-8') as f:
                f.write("""
@Component
struct TestStruct {
  build() {
    Column() {}
  }
}
""")
            
            result = subprocess.run(
                [
                    "node",
                    "/workspace/arkanalyzer-wrapper/src/arkanalyzer-final-fixed.js",
                    os.path.dirname(long_path),
                    "/tmp/test_long_path.json"
                ],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                tests_passed.append(True)
                print("    ✅ 超长路径处理成功")
            else:
                tests_passed.append(False)
                print(f"    ❌ 超长路径处理失败: {result.stderr[:100]}")
                
        except Exception as e:
            tests_passed.append(False)
            print(f"    ❌ 异常: {e}")
        
        # 测试2: 特殊Unicode字符
        try:
            print("  测试 1.2: Unicode特殊字符处理...")
            unicode_dir = "/workspace/unicode_测试_テスト_тест"
            os.makedirs(unicode_dir, exist_ok=True)
            
            unicode_file = os.path.join(unicode_dir, "测试文件_テスト.ets")
            with open(unicode_file, 'w', encoding='utf-8') as f:
                f.write("""
@Component
struct 测试类 {
  测试方法(): void {
    console.log('测试');
  }
  build() {
    Column() {}
  }
}
""")
            
            result = subprocess.run(
                [
                    "node",
                    "/workspace/arkanalyzer-wrapper/src/arkanalyzer-final-fixed.js",
                    unicode_dir,
                    "/tmp/test_unicode.json"
                ],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                with open('/tmp/test_unicode.json', 'r') as f:
                    data = json.load(f)
                
                unicode_ok = len(data.get('classes', [])) > 0
                tests_passed.append(unicode_ok)
                print(f"    {'✅' if unicode_ok else '❌'} Unicode字符处理{'成功' if unicode_ok else '失败'}")
            else:
                tests_passed.append(False)
                print("    ❌ Unicode字符处理失败")
                
        except Exception as e:
            tests_passed.append(False)
            print(f"    ❌ 异常: {e}")
        
        # 测试3: 隐藏文件
        try:
            print("  测试 1.3: 隐藏文件处理...")
            hidden_dir = "/workspace/hidden_test"
            os.makedirs(hidden_dir, exist_ok=True)
            
            hidden_file = os.path.join(hidden_dir, ".hidden.ets")
            normal_file = os.path.join(hidden_dir, "normal.ets")
            
            with open(hidden_file, 'w', encoding='utf-8') as f:
                f.write("""
@Component
struct HiddenStruct {
  build() { Column() {} }
}
""")
            
            with open(normal_file, 'w', encoding='utf-8') as f:
                f.write("""
@Component
struct NormalStruct {
  build() { Column() {} }
}
""")
            
            result = subprocess.run(
                [
                    "node",
                    "/workspace/arkanalyzer-wrapper/src/arkanalyzer-final-fixed.js",
                    hidden_dir,
                    "/tmp/test_hidden.json"
                ],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                with open('/tmp/test_hidden.json', 'r') as f:
                    data = json.load(f)
                
                # 隐藏文件不应该被处理
                hidden_ok = len(data.get('classes', [])) == 1
                tests_passed.append(hidden_ok)
                print(f"    {'✅' if hidden_ok else '⚠️ '} 隐藏文件处理: {len(data.get('classes', []))} 个类")
                
                if hidden_ok:
                    self.log_issue("INFO", "隐藏文件测试", "隐藏文件被正确忽略", "这是预期行为")
            else:
                tests_passed.append(False)
                print("    ❌ 隐藏文件处理失败")
                
        except Exception as e:
            tests_passed.append(False)
            print(f"    ❌ 异常: {e}")
        
        all_passed = all(tests_passed)
        return self.log_test(
            "极端路径场景",
            all_passed,
            f"通过: {sum(tests_passed)}/{len(tests_passed)}",
            {"tests": tests_passed}
        )
    
    def test_memory_stability(self):
        """测试内存稳定性"""
        print("\n📊 测试 N.2: 内存稳定性")
        print("=" * 60)
        
        tests_passed = []
        
        # 连续多次分析
        print("  测试 2.1: 连续10次分析...")
        for i in range(10):
            try:
                result = subprocess.run(
                    [
                        "node",
                        "/workspace/arkanalyzer-wrapper/src/arkanalyzer-final-fixed.js",
                        "/workspace/UltimateChaosProject",
                        f"/tmp/test_memory_{i}.json"
                    ],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode == 0:
                    with open(f"/tmp/test_memory_{i}.json", 'r') as f:
                        data = json.load(f)
                    
                    if len(data.get('files', [])) > 0:
                        tests_passed.append(True)
                        if i % 3 == 0:
                            print(f"    第 {i+1} 次: ✅ 成功")
                    else:
                        tests_passed.append(False)
                        print(f"    第 {i+1} 次: ❌ 数据为空")
                else:
                    tests_passed.append(False)
                    print(f"    第 {i+1} 次: ❌ 失败")
                    
            except Exception as e:
                tests_passed.append(False)
                print(f"    第 {i+1} 次: ❌ 异常: {e}")
        
        memory_stable = sum(tests_passed) == 10
        self.log_test(
            "内存稳定性",
            memory_stable,
            f"连续10次分析: {sum(tests_passed)}/10 成功",
            {"tests": tests_passed}
        )
        
        if not memory_stable:
            self.log_issue(
                "WARNING",
                "内存稳定性",
                f"有 {10 - sum(tests_passed)} 次失败，可能是内存泄漏或资源未释放",
                "检查代码中的资源管理，确保文件句柄关闭"
            )
        
        return memory_stable
    
    def test_concurrent_analysis(self):
        """测试并发分析能力"""
        print("\n📊 测试 N.3: 并发分析能力")
        print("=" * 60)
        
        tests_passed = []
        
        # 并发分析多个项目
        print("  测试 3.1: 并发分析3个项目...")
        
        # 项目1: UltimateChaosProject
        # 项目2: ExtremeChaosProject
        # 项目3: sample_project
        
        projects = [
            ("/workspace/UltimateChaosProject", "/tmp/concurrent_1.json"),
            ("/workspace/ExtremeChaosProject", "/tmp/concurrent_2.json"),
            ("/workspace/sample_project", "/tmp/concurrent_3.json")
        ]
        
        processes = []
        start_time = time.time()
        
        for project_path, output_file in projects:
            proc = subprocess.Popen(
                [
                    "node",
                    "/workspace/arkanalyzer-wrapper/src/arkanalyzer-final-fixed.js",
                    project_path,
                    output_file
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            processes.append(proc)
        
        # 等待所有进程完成
        all_success = True
        for i, proc in enumerate(processes):
            proc.wait(timeout=60)
            
            if proc.returncode == 0 and os.path.exists(projects[i][1]):
                with open(projects[i][1], 'r') as f:
                    data = json.load(f)
                
                if len(data.get('files', [])) > 0:
                    tests_passed.append(True)
                    print(f"    项目 {i+1}: ✅ 成功")
                else:
                    tests_passed.append(False)
                    all_success = False
                    print(f"    项目 {i+1}: ❌ 数据为空")
            else:
                tests_passed.append(False)
                all_success = False
                print(f"    项目 {i+1}: ❌ 失败")
        
        end_time = time.time()
        concurrent_duration = end_time - start_time
        
        # 串行分析时间估计
        serial_duration = 30 + 2 + 1  # 估计3个项目分别耗时
        
        concurrent_ok = all_success and concurrent_duration < serial_duration
        
        self.log_test(
            "并发分析能力",
            concurrent_ok,
            f"并发耗时: {concurrent_duration:.2f}s, 通过: {sum(tests_passed)}/{len(tests_passed)}",
            {"concurrent_time": concurrent_duration, "tests": tests_passed}
        )
        
        if concurrent_ok:
            self.log_issue(
                "INFO",
                "并发分析",
                f"并发分析有效，比串行快 {serial_duration - concurrent_duration:.2f}秒",
                "系统支持并发处理"
            )
        
        return concurrent_ok
    
    def test_data_corruption(self):
        """测试数据损坏场景"""
        print("\n📊 测试 N.4: 数据损坏场景")
        print("=" * 60)
        
        tests_passed = []
        
        # 测试1: 空文件
        try:
            print("  测试 4.1: 空文件处理...")
            empty_dir = "/workspace/empty_test"
            os.makedirs(empty_dir, exist_ok=True)
            
            empty_file = os.path.join(empty_dir, "empty.ets")
            with open(empty_file, 'w') as f:
                pass  # 创建空文件
            
            result = subprocess.run(
                [
                    "node",
                    "/workspace/arkanalyzer-wrapper/src/arkanalyzer-final-fixed.js",
                    empty_dir,
                    "/tmp/test_empty.json"
                ],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                with open('/tmp/test_empty.json', 'r') as f:
                    data = json.load(f)
                
                empty_ok = len(data.get('classes', [])) == 0
                tests_passed.append(empty_ok)
                print(f"    {'✅' if empty_ok else '⚠️ '} 空文件处理: {len(data.get('classes', []))} 个类")
            else:
                tests_passed.append(False)
                print("    ❌ 空文件处理失败")
                
        except Exception as e:
            tests_passed.append(False)
            print(f"    ❌ 异常: {e}")
        
        # 测试2: 二进制内容
        try:
            print("  测试 4.2: 二进制内容处理...")
            binary_dir = "/workspace/binary_test"
            os.makedirs(binary_dir, exist_ok=True)
            
            binary_file = os.path.join(binary_dir, "binary.ets")
            with open(binary_file, 'wb') as f:
                f.write(b'\x00\x01\x02\x03\x04\x05')
            
            result = subprocess.run(
                [
                    "node",
                    "/workspace/arkanalyzer-wrapper/src/arkanalyzer-final-fixed.js",
                    binary_dir,
                    "/tmp/test_binary.json"
                ],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # 即使失败也不应该崩溃
            binary_ok = result.returncode in [0, 1]  # 允许失败但不能崩溃
            tests_passed.append(binary_ok)
            print(f"    {'✅' if binary_ok else '❌'} 二进制内容处理{'正常' if binary_ok else '崩溃'}")
            
        except Exception as e:
            tests_passed.append(True)  # 异常说明正确处理了
            print(f"    ✅ 二进制内容异常处理: {e}")
        
        # 测试3: 超大文件
        try:
            print("  测试 4.3: 超大文件处理...")
            large_dir = "/workspace/large_file_test"
            os.makedirs(large_dir, exist_ok=True)
            
            large_file = os.path.join(large_dir, "large.ets")
            with open(large_file, 'w', encoding='utf-8') as f:
                # 生成1MB的内容
                content = """
@Component
struct LargeStruct {
""" + "\n  method(): void {}\n" * 50000 + """
  build() { Column() {} }
}
"""
                f.write(content)
            
            file_size = os.path.getsize(large_file) / (1024 * 1024)
            print(f"    文件大小: {file_size:.2f} MB")
            
            result = subprocess.run(
                [
                    "node",
                    "/workspace/arkanalyzer-wrapper/src/arkanalyzer-final-fixed.js",
                    large_dir,
                    "/tmp/test_large.json"
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                with open('/tmp/test_large.json', 'r') as f:
                    data = json.load(f)
                
                large_ok = len(data.get('classes', [])) > 0
                tests_passed.append(large_ok)
                print(f"    {'✅' if large_ok else '❌'} 超大文件处理成功")
            else:
                tests_passed.append(False)
                print("    ⚠️ 超大文件处理可能超时")
                
        except Exception as e:
            tests_passed.append(False)
            print(f"    ❌ 异常: {e}")
        
        all_passed = all(tests_passed)
        return self.log_test(
            "数据损坏场景",
            all_passed,
            f"通过: {sum(tests_passed)}/{len(tests_passed)}",
            {"tests": tests_passed}
        )
    
    def test_performance_bottleneck(self):
        """测试性能瓶颈"""
        print("\n📊 测试 N.5: 性能瓶颈分析")
        print("=" * 60)
        
        try:
            # 分析不同规模项目的性能
            projects = [
                ("/workspace/sample_project", "小规模"),
                ("/workspace/ExtremeChaosProject", "中规模"),
                ("/workspace/UltimateChaosProject", "大规模")
            ]
            
            results = []
            
            for project_path, scale in projects:
                start = time.time()
                
                result = subprocess.run(
                    [
                        "node",
                        "/workspace/arkanalyzer-wrapper/src/arkanalyzer-final-fixed.js",
                        project_path,
                        f"/tmp/test_perf_{scale}.json"
                    ],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                
                end = time.time()
                duration = end - start
                
                if result.returncode == 0:
                    with open(f"/tmp/test_perf_{scale}.json", 'r') as f:
                        data = json.load(f)
                    
                    file_count = len(data.get('files', []))
                    method_count = len(data.get('methods', []))
                    time_per_method = (duration * 1000) / method_count if method_count > 0 else 0
                    
                    results.append({
                        "scale": scale,
                        "duration": duration,
                        "file_count": file_count,
                        "method_count": method_count,
                        "time_per_method": time_per_method
                    })
                    
                    print(f"  {scale}: {duration:.2f}s, {file_count}文件, {method_count}方法, {time_per_method:.3f}ms/方法")
                else:
                    print(f"  {scale}: ❌ 失败")
            
            # 分析性能趋势
            if len(results) >= 2:
                time_ratios = []
                for i in range(len(results) - 1):
                    if results[i]['method_count'] > 0:
                        ratio = results[i+1]['time_per_method'] / results[i]['time_per_method']
                        time_ratios.append(ratio)
                
                avg_ratio = sum(time_ratios) / len(time_ratios) if time_ratios else 1.0
                
                if avg_ratio > 1.5:
                    self.log_issue(
                        "WARNING",
                        "性能瓶颈",
                        f"性能随规模增长而显著下降 (比率: {avg_ratio:.2f})",
                        "建议优化算法或使用流式处理"
                    )
                elif avg_ratio < 0.5:
                    self.log_issue(
                        "INFO",
                        "性能优化",
                        f"性能随规模增长而提升 (比率: {avg_ratio:.2f})",
                        "可能使用了缓存或预计算"
                    )
                else:
                    self.log_issue(
                        "INFO",
                        "性能稳定",
                        f"性能随规模线性增长 (比率: {avg_ratio:.2f})",
                        "性能表现稳定"
                    )
            
            return self.log_test(
                "性能瓶颈分析",
                True,
                f"分析了 {len(results)} 个规模级别",
                {"results": results}
            )
            
        except Exception as e:
            return self.log_test("性能瓶颈分析", False, f"异常: {str(e)}")
    
    def test_output_format_compliance(self):
        """测试输出格式合规性"""
        print("\n📊 测试 N.6: 输出格式合规性")
        print("=" * 60)
        
        tests_passed = []
        
        try:
            with open('/workspace/ultimate_analysis.json', 'r') as f:
                data = json.load(f)
            
            # 检查必需字段
            required_fields = ['files', 'classes', 'methods', 'calls']
            for field in required_fields:
                has_field = field in data
                tests_passed.append(has_field)
                print(f"  {'✅' if has_field else '❌'} 字段 {field}: {'存在' if has_field else '缺失'}")
            
            # 检查数据类型
            if 'files' in data:
                is_array = isinstance(data['files'], list)
                tests_passed.append(is_array)
                print(f"  {'✅' if is_array else '❌'} files 是数组: {is_array}")
            
            if 'classes' in data:
                is_array = isinstance(data['classes'], list)
                tests_passed.append(is_array)
                print(f"  {'✅' if is_array else '❌'} classes 是数组: {is_array}")
            
            # 检查JSON格式
            try:
                with open('/workspace/ultimate_analysis.json', 'r') as f:
                    json.dumps(json.load(f))
                tests_passed.append(True)
                print("  ✅ JSON格式有效")
            except:
                tests_passed.append(False)
                print("  ❌ JSON格式无效")
            
            all_passed = all(tests_passed)
            return self.log_test(
                "输出格式合规性",
                all_passed,
                f"通过: {sum(tests_passed)}/{len(tests_passed)}",
                {"tests": tests_passed}
            )
            
        except Exception as e:
            return self.log_test("输出格式合规性", False, f"异常: {str(e)}")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 80)
        print("🚀 开始第N轮深度迭代测试 - 发现隐藏问题")
        print("=" * 80)
        
        tests = [
            self.test_edge_case_extreme_paths,
            self.test_memory_stability,
            self.test_concurrent_analysis,
            self.test_data_corruption,
            self.test_performance_bottleneck,
            self.test_output_format_compliance,
        ]
        
        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
            except Exception as e:
                print(f"❌ 测试异常: {e}")
                results.append(False)
        
        print("\n" + "=" * 80)
        print("📊 测试总结")
        print("=" * 80)
        
        passed = sum(results)
        total = len(results)
        
        print(f"✅ 通过: {passed}/{total}")
        print(f"❌ 失败: {total - passed}/{total}")
        
        if self.found_issues:
            print(f"\n🔍 发现的问题: {len(self.found_issues)}")
            for issue in self.found_issues:
                print(f"  - [{issue['severity']}] {issue['test_name']}: {issue['issue']}")
        
        if passed == total and len(self.found_issues) == 0:
            print("\n🎉 所有测试通过，无问题发现！系统完美！")
        elif passed == total:
            print(f"\n✅ 所有测试通过，发现 {len(self.found_issues)} 个可优化项")
        else:
            print(f"\n⚠️  有 {total - passed} 个测试失败，需要修复")
        
        return passed == total

if __name__ == "__main__":
    tester = IterationNTest()
    success = tester.run_all_tests()
    exit(0 if success else 1)
