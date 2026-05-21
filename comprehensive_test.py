#!/usr/bin/env python3
"""
综合单元测试 - 验证系统所有分支和特殊场景
"""

import json
import os
import subprocess
from datetime import datetime

class ComprehensiveUnitTest:
    def __init__(self):
        self.test_results = []
        self.start_time = datetime.now()
        
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
    
    def test_basic_analysis(self):
        """测试基础分析功能"""
        print("\n📊 测试 1: 基础分析功能")
        print("=" * 60)
        
        try:
            result = subprocess.run(
                [
                    "node",
                    "/workspace/arkanalyzer-wrapper/src/arkanalyzer-final-fixed.js",
                    "/workspace/UltimateChaosProject",
                    "/tmp/test_basic.json"
                ],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                return self.log_test("基础分析功能", False, f"分析失败: {result.stderr}")
            
            with open('/tmp/test_basic.json', 'r') as f:
                data = json.load(f)
            
            passed = (
                len(data.get('files', [])) > 0 and
                len(data.get('classes', [])) > 0 and
                len(data.get('methods', [])) > 0
            )
            
            return self.log_test(
                "基础分析功能",
                passed,
                f"文件: {len(data['files'])}, 类: {len(data['classes'])}, 方法: {len(data['methods'])}",
                data
            )
            
        except Exception as e:
            return self.log_test("基础分析功能", False, f"异常: {str(e)}")
    
    def test_data_structure(self):
        """测试数据结构正确性"""
        print("\n📊 测试 2: 数据结构正确性")
        print("=" * 60)
        
        tests_passed = []
        
        try:
            with open('/workspace/ultimate_analysis.json', 'r') as f:
                data = json.load(f)
            
            # 测试文件数据结构
            if data['files']:
                file = data['files'][0]
                file_fields = set(file.keys())
                required = {'id', 'path', 'hash'}
                has_required = required.issubset(file_fields)
                tests_passed.append(has_required)
                print(f"  {'✅' if has_required else '❌'} 文件字段: {file_fields}")
            
            # 测试类数据结构
            if data['classes']:
                cls = data['classes'][0]
                cls_fields = set(cls.keys())
                required = {'id', 'name', 'fileId'}
                has_required = required.issubset(cls_fields)
                tests_passed.append(has_required)
                print(f"  {'✅' if has_required else '❌'} 类字段: {cls_fields}")
            
            # 测试方法数据结构
            if data['methods']:
                method = data['methods'][0]
                method_fields = set(method.keys())
                required = {'id', 'name', 'classId'}
                has_required = required.issubset(method_fields)
                tests_passed.append(has_required)
                print(f"  {'✅' if has_required else '❌'} 方法字段: {method_fields}")
            
            # 测试调用数据结构
            if data['calls']:
                call = data['calls'][0]
                call_fields = set(call.keys())
                required = {'callerId', 'calleeId'}
                has_required = required.issubset(call_fields)
                tests_passed.append(has_required)
                print(f"  {'✅' if has_required else '❌'} 调用字段: {call_fields}")
            
            all_passed = all(tests_passed)
            return self.log_test(
                "数据结构正确性",
                all_passed,
                f"通过: {sum(tests_passed)}/{len(tests_passed)}",
                {"tests": tests_passed}
            )
            
        except Exception as e:
            return self.log_test("数据结构正确性", False, f"异常: {str(e)}")
    
    def test_id_uniqueness(self):
        """测试ID唯一性"""
        print("\n📊 测试 3: ID唯一性")
        print("=" * 60)
        
        try:
            with open('/workspace/ultimate_analysis.json', 'r') as f:
                data = json.load(f)
            
            tests_passed = []
            
            # 检查文件ID唯一性
            file_ids = [f['id'] for f in data['files']]
            file_ids_unique = len(file_ids) == len(set(file_ids))
            tests_passed.append(file_ids_unique)
            print(f"  {'✅' if file_ids_unique else '❌'} 文件ID唯一: {len(file_ids)}")
            
            # 检查类ID唯一性
            class_ids = [c['id'] for c in data['classes']]
            class_ids_unique = len(class_ids) == len(set(class_ids))
            tests_passed.append(class_ids_unique)
            print(f"  {'✅' if class_ids_unique else '❌'} 类ID唯一: {len(class_ids)}")
            
            # 检查方法ID唯一性
            method_ids = [m['id'] for m in data['methods']]
            method_ids_unique = len(method_ids) == len(set(method_ids))
            tests_passed.append(method_ids_unique)
            print(f"  {'✅' if method_ids_unique else '❌'} 方法ID唯一: {len(method_ids)}")
            
            all_passed = all(tests_passed)
            return self.log_test(
                "ID唯一性",
                all_passed,
                f"通过: {sum(tests_passed)}/{len(tests_passed)}",
                {"tests": tests_passed}
            )
            
        except Exception as e:
            return self.log_test("ID唯一性", False, f"异常: {str(e)}")
    
    def test_reference_integrity(self):
        """测试引用完整性"""
        print("\n📊 测试 4: 引用完整性")
        print("=" * 60)
        
        try:
            with open('/workspace/ultimate_analysis.json', 'r') as f:
                data = json.load(f)
            
            tests_passed = []
            
            # 检查类引用的文件ID有效性
            file_ids = set([f['id'] for f in data['files']])
            class_file_ids = set([c['fileId'] for c in data['classes']])
            valid_class_file_refs = class_file_ids.issubset(file_ids)
            tests_passed.append(valid_class_file_refs)
            print(f"  {'✅' if valid_class_file_refs else '❌'} 类→文件引用有效")
            
            # 检查方法引用的类ID有效性
            class_ids = set([c['id'] for c in data['classes']])
            method_class_ids = set([m['classId'] for m in data['methods']])
            valid_method_class_refs = method_class_ids.issubset(class_ids)
            tests_passed.append(valid_method_class_refs)
            print(f"  {'✅' if valid_method_class_refs else '❌'} 方法→类引用有效")
            
            # 检查调用引用的有效性
            method_ids = set([m['id'] for m in data['methods']])
            caller_ids = set([c['callerId'] for c in data['calls']])
            callee_ids = set([c['calleeId'] for c in data['calls'] if 'calleeId' in c])
            valid_caller_refs = caller_ids.issubset(method_ids)
            valid_callee_refs = callee_ids.issubset(method_ids)
            tests_passed.append(valid_caller_refs)
            tests_passed.append(valid_callee_refs)
            print(f"  {'✅' if valid_caller_refs else '❌'} 调用→方法(caller)引用有效")
            print(f"  {'✅' if valid_callee_refs else '❌'} 调用→方法(callee)引用有效")
            
            all_passed = all(tests_passed)
            return self.log_test(
                "引用完整性",
                all_passed,
                f"通过: {sum(tests_passed)}/{len(tests_passed)}",
                {"tests": tests_passed}
            )
            
        except Exception as e:
            return self.log_test("引用完整性", False, f"异常: {str(e)}")
    
    def test_scale_handling(self):
        """测试大规模数据处理"""
        print("\n📊 测试 5: 大规模数据处理")
        print("=" * 60)
        
        try:
            with open('/workspace/ultimate_analysis.json', 'r') as f:
                data = json.load(f)
            
            tests_passed = []
            
            # 检查文件数量
            file_count = len(data['files'])
            files_ok = file_count >= 100
            tests_passed.append(files_ok)
            print(f"  {'✅' if files_ok else '❌'} 文件数量: {file_count}")
            
            # 检查类数量
            class_count = len(data['classes'])
            classes_ok = class_count >= 1000
            tests_passed.append(classes_ok)
            print(f"  {'✅' if classes_ok else '❌'} 类数量: {class_count}")
            
            # 检查方法数量
            method_count = len(data['methods'])
            methods_ok = method_count >= 10000
            tests_passed.append(methods_ok)
            print(f"  {'✅' if methods_ok else '❌'} 方法数量: {method_count}")
            
            # 检查调用数量
            call_count = len(data['calls'])
            calls_ok = call_count >= 1000
            tests_passed.append(calls_ok)
            print(f"  {'✅' if calls_ok else '❌'} 调用数量: {call_count}")
            
            all_passed = all(tests_passed)
            return self.log_test(
                "大规模数据处理",
                all_passed,
                f"通过: {sum(tests_passed)}/{len(tests_passed)}",
                {
                    "files": file_count,
                    "classes": class_count,
                    "methods": method_count,
                    "calls": call_count
                }
            )
            
        except Exception as e:
            return self.log_test("大规模数据处理", False, f"异常: {str(e)}")
    
    def test_complex_scenarios(self):
        """测试复杂场景"""
        print("\n📊 测试 6: 复杂场景处理")
        print("=" * 60)
        
        try:
            with open('/workspace/ultimate_analysis.json', 'r') as f:
                data = json.load(f)
            
            tests_passed = []
            
            # 检查循环依赖处理
            circular_dir = "/workspace/UltimateChaosProject/circular"
            if os.path.exists(circular_dir):
                circular_files = [f for f in data['files'] if 'circular' in f['path']]
                tests_passed.append(len(circular_files) > 0)
                print(f"  {'✅' if len(circular_files) > 0 else '❌'} 循环依赖文件识别")
            
            # 检查递归调用处理
            recursive_dir = "/workspace/UltimateChaosProject/recursive"
            if os.path.exists(recursive_dir):
                recursive_files = [f for f in data['files'] if 'recursive' in f['path']]
                tests_passed.append(len(recursive_files) > 0)
                print(f"  {'✅' if len(recursive_files) > 0 else '❌'} 递归调用文件识别")
            
            # 检查错误处理场景
            error_dir = "/workspace/UltimateChaosProject/error_handling"
            if os.path.exists(error_dir):
                error_files = [f for f in data['files'] if 'error_handling' in f['path']]
                tests_passed.append(len(error_files) > 0)
                print(f"  {'✅' if len(error_files) > 0 else '❌'} 错误处理文件识别")
            
            # 检查异步场景
            async_dir = "/workspace/UltimateChaosProject/async"
            if os.path.exists(async_dir):
                async_files = [f for f in data['files'] if 'async' in f['path']]
                tests_passed.append(len(async_files) > 0)
                print(f"  {'✅' if len(async_files) > 0 else '❌'} 异步场景文件识别")
            
            all_passed = len(tests_passed) > 0 and all(tests_passed)
            return self.log_test(
                "复杂场景处理",
                all_passed,
                f"通过: {sum(tests_passed)}/{len(tests_passed)}",
                {"tests": tests_passed}
            )
            
        except Exception as e:
            return self.log_test("复杂场景处理", False, f"异常: {str(e)}")
    
    def test_performance(self):
        """测试性能"""
        print("\n📊 测试 7: 性能测试")
        print("=" * 60)
        
        try:
            import time
            
            start = time.time()
            
            result = subprocess.run(
                [
                    "node",
                    "/workspace/arkanalyzer-wrapper/src/arkanalyzer-final-fixed.js",
                    "/workspace/UltimateChaosProject",
                    "/tmp/test_performance.json"
                ],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            end = time.time()
            duration = end - start
            
            tests_passed = []
            
            # 检查是否成功完成
            success = result.returncode == 0
            tests_passed.append(success)
            print(f"  {'✅' if success else '❌'} 分析成功完成")
            
            # 检查性能
            performance_ok = duration < 60  # 60秒内完成
            tests_passed.append(performance_ok)
            print(f"  {'✅' if performance_ok else '❌'} 性能达标 (< 60s): {duration:.2f}s")
            
            # 检查输出文件大小
            output_size = os.path.getsize('/tmp/test_performance.json')
            size_ok = output_size > 0
            tests_passed.append(size_ok)
            print(f"  {'✅' if size_ok else '❌'} 输出文件有效: {output_size / 1024 / 1024:.2f} MB")
            
            all_passed = all(tests_passed)
            return self.log_test(
                "性能测试",
                all_passed,
                f"耗时: {duration:.2f}s, 通过: {sum(tests_passed)}/{len(tests_passed)}",
                {"duration": duration, "tests": tests_passed}
            )
            
        except Exception as e:
            return self.log_test("性能测试", False, f"异常: {str(e)}")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 80)
        print("🚀 开始综合单元测试")
        print("=" * 80)
        
        tests = [
            self.test_basic_analysis,
            self.test_data_structure,
            self.test_id_uniqueness,
            self.test_reference_integrity,
            self.test_scale_handling,
            self.test_complex_scenarios,
            self.test_performance,
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
        
        if passed == total:
            print("\n🎉 所有测试通过！系统完全正常！")
        else:
            print(f"\n⚠️  有 {total - passed} 个测试失败")
        
        return passed == total

if __name__ == "__main__":
    tester = ComprehensiveUnitTest()
    success = tester.run_all_tests()
    exit(0 if success else 1)
