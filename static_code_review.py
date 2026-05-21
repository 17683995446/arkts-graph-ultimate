#!/usr/bin/env python3
"""
静态代码核验 - 代码走读与逻辑核对
验证系统各模块的代码质量和逻辑合理性
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime

class StaticCodeReview:
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.start_time = datetime.now()
        self.node_analyzer_path = "/workspace/arkanalyzer-wrapper/src/arkanalyzer-final-fixed.js"
        
    def log_issue(self, severity, module, message, location=""):
        """记录问题"""
        issue = {
            "severity": severity,
            "module": module,
            "message": message,
            "location": location,
            "timestamp": datetime.now().isoformat()
        }
        
        if severity == "ERROR":
            self.issues.append(issue)
            print(f"  ❌ [{module}] {message} {location}")
        elif severity == "WARNING":
            self.warnings.append(issue)
            print(f"  ⚠️  [{module}] {message} {location}")
        elif severity == "INFO":
            print(f"  ℹ️  [{module}] {message}")
    
    def review_node_analyzer(self):
        """核验 Node.js 分析器代码"""
        print("\n📊 核验 Node.js 分析器")
        print("=" * 60)
        
        try:
            with open(self.node_analyzer_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # 检查代码结构
            lines = code.split('\n')
            total_lines = len(lines)
            self.log_issue("INFO", "NODE_ANALYZER", f"代码总行数: {total_lines}")
            
            # 检查注释覆盖率
            comment_lines = [l for l in lines if l.strip().startswith('//') or l.strip().startswith('*')]
            comment_ratio = len(comment_lines) / total_lines if total_lines > 0 else 0
            self.log_issue("INFO", "NODE_ANALYZER", f"注释行数: {len(comment_lines)} ({comment_ratio:.1%})")
            
            # 检查关键函数
            key_functions = [
                'extractEntities',
                'extractClasses',
                'extractMethods',
                'extractMethodCalls',
                'identifyCallRelationships',
                'identifyComponentRelationships',
                'saveResults'
            ]
            
            for func in key_functions:
                if f'    {func}(' in code or f'\t{func}(' in code:
                    self.log_issue("INFO", "NODE_ANALYZER", f"✓ 函数存在: {func}")
                else:
                    self.log_issue("ERROR", "NODE_ANALYZER", f"✗ 函数缺失: {func}")
            
            # 检查 UI 组件列表
            if 'arkTSUIComponents' in code:
                self.log_issue("INFO", "NODE_ANALYZER", "✓ UI组件列表已定义")
            else:
                self.log_issue("WARNING", "NODE_ANALYZER", "⚠ UI组件列表未定义")
            
            # 检查关键字列表
            if 'keywordsToSkip' in code:
                self.log_issue("INFO", "NODE_ANALYZER", "✓ 关键字列表已定义")
            else:
                self.log_issue("WARNING", "NODE_ANALYZER", "⚠ 关键字列表未定义")
            
            # 检查错误处理
            if 'try' in code and 'catch' in code:
                self.log_issue("INFO", "NODE_ANALYZER", "✓ 包含错误处理")
            else:
                self.log_issue("WARNING", "NODE_ANALYZER", "⚠ 缺少错误处理")
            
            # 检查日志输出
            if 'console.log' in code or 'this.log' in code:
                self.log_issue("INFO", "NODE_ANALYZER", "✓ 包含日志输出")
            else:
                self.log_issue("WARNING", "NODE_ANALYZER", "⚠ 缺少日志输出")
            
            # 检查内存泄漏风险
            if 'async' in code:
                if 'await' in code:
                    self.log_issue("INFO", "NODE_ANALYZER", "✓ 使用了 async/await")
                else:
                    self.log_issue("WARNING", "NODE_ANALYZER", "⚠ 使用了 async 但未使用 await")
            
            # 检查闭包使用
            closure_pattern = r'function\s*\([^)]*\)\s*\{[^}]*\}'
            closures = re.findall(closure_pattern, code)
            self.log_issue("INFO", "NODE_ANALYZER", f"闭包使用: {len(closures)} 个")
            
            # 检查正则表达式
            regex_patterns = re.findall(r'/[^/]+/g?', code)
            self.log_issue("INFO", "NODE_ANALYZER", f"正则表达式: {len(regex_patterns)} 个")
            
        except Exception as e:
            self.log_issue("ERROR", "NODE_ANALYZER", f"读取失败: {str(e)}")
    
    def review_analysis_result(self):
        """核验分析结果"""
        print("\n📊 核验分析结果")
        print("=" * 60)
        
        try:
            with open('/workspace/ultimate_analysis.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查数据完整性
            required_keys = ['files', 'classes', 'methods', 'calls', 'components']
            for key in required_keys:
                if key in data:
                    self.log_issue("INFO", "ANALYSIS_RESULT", f"✓ 数据字段存在: {key}")
                else:
                    self.log_issue("ERROR", "ANALYSIS_RESULT", f"✗ 数据字段缺失: {key}")
            
            # 检查数据合理性
            files = data.get('files', [])
            classes = data.get('classes', [])
            methods = data.get('methods', [])
            calls = data.get('calls', [])
            components = data.get('components', [])
            
            self.log_issue("INFO", "ANALYSIS_RESULT", f"文件数: {len(files)}")
            self.log_issue("INFO", "ANALYSIS_RESULT", f"类数: {len(classes)}")
            self.log_issue("INFO", "ANALYSIS_RESULT", f"方法数: {len(methods)}")
            self.log_issue("INFO", "ANALYSIS_RESULT", f"调用关系数: {len(calls)}")
            self.log_issue("INFO", "ANALYSIS_RESULT", f"组件关系数: {len(components)}")
            
            # 检查是否有空数据
            if len(files) == 0:
                self.log_issue("ERROR", "ANALYSIS_RESULT", "✗ 没有文件数据")
            
            if len(classes) == 0:
                self.log_issue("ERROR", "ANALYSIS_RESULT", "✗ 没有类数据")
            
            # 检查类数据格式
            if classes:
                sample_class = classes[0]
                required_class_fields = ['id', 'name', 'fileId']
                
                for field in required_class_fields:
                    if field in sample_class:
                        self.log_issue("INFO", "ANALYSIS_RESULT", f"✓ 类字段存在: {field}")
                    else:
                        self.log_issue("WARNING", "ANALYSIS_RESULT", f"⚠ 类字段缺失: {field}")
            
            # 检查方法数据格式
            if methods:
                sample_method = methods[0]
                required_method_fields = ['id', 'name', 'classId']
                
                for field in required_method_fields:
                    if field in sample_method:
                        self.log_issue("INFO", "ANALYSIS_RESULT", f"✓ 方法字段存在: {field}")
                    else:
                        self.log_issue("WARNING", "ANALYSIS_RESULT", f"⚠ 方法字段缺失: {field}")
            
            # 检查调用关系格式
            if calls:
                sample_call = calls[0]
                required_call_fields = ['id', 'callerId', 'calleeName']
                
                for field in required_call_fields:
                    if field in sample_call:
                        self.log_issue("INFO", "ANALYSIS_RESULT", f"✓ 调用字段存在: {field}")
                    else:
                        self.log_issue("WARNING", "ANALYSIS_RESULT", f"⚠ 调用字段缺失: {field}")
            
        except Exception as e:
            self.log_issue("ERROR", "ANALYSIS_RESULT", f"读取失败: {str(e)}")
    
    def review_data_consistency(self):
        """核验数据一致性"""
        print("\n📊 核验数据一致性")
        print("=" * 60)
        
        try:
            with open('/workspace/ultimate_analysis.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            files = data.get('files', [])
            classes = data.get('classes', [])
            methods = data.get('methods', [])
            
            # 检查 ID 唯一性
            file_ids = set([f['id'] for f in files])
            if len(file_ids) == len(files):
                self.log_issue("INFO", "DATA_CONSISTENCY", "✓ 文件ID唯一")
            else:
                self.log_issue("ERROR", "DATA_CONSISTENCY", f"✗ 文件ID重复: {len(files)} vs {len(file_ids)}")
            
            class_ids = set([c['id'] for c in classes])
            if len(class_ids) == len(classes):
                self.log_issue("INFO", "DATA_CONSISTENCY", "✓ 类ID唯一")
            else:
                self.log_issue("ERROR", "DATA_CONSISTENCY", f"✗ 类ID重复: {len(classes)} vs {len(class_ids)}")
            
            method_ids = set([m['id'] for m in methods])
            if len(method_ids) == len(methods):
                self.log_issue("INFO", "DATA_CONSISTENCY", "✓ 方法ID唯一")
            else:
                self.log_issue("ERROR", "DATA_CONSISTENCY", f"✗ 方法ID重复: {len(methods)} vs {len(method_ids)}")
            
            # 检查文件引用完整性
            file_id_set = set([f['id'] for f in files])
            class_file_ids = set([c['fileId'] for c in classes if 'fileId' in c])
            
            invalid_class_file_refs = class_file_ids - file_id_set
            if len(invalid_class_file_refs) > 0:
                self.log_issue("ERROR", "DATA_CONSISTENCY", f"✗ 类引用了不存在的文件ID: {len(invalid_class_file_refs)}")
            else:
                self.log_issue("INFO", "DATA_CONSISTENCY", "✓ 类引用文件ID有效")
            
            # 检查类引用完整性
            class_id_set = set([c['id'] for c in classes])
            method_class_ids = set([m['classId'] for m in methods if 'classId' in m])
            
            invalid_method_class_refs = method_class_ids - class_id_set
            if len(invalid_method_class_refs) > 0:
                self.log_issue("ERROR", "DATA_CONSISTENCY", f"✗ 方法引用了不存在的类ID: {len(invalid_method_class_refs)}")
            else:
                self.log_issue("INFO", "DATA_CONSISTENCY", "✓ 方法引用类ID有效")
            
        except Exception as e:
            self.log_issue("ERROR", "DATA_CONSISTENCY", f"检查失败: {str(e)}")
    
    def review_performance(self):
        """核验性能特征"""
        print("\n📊 核验性能特征")
        print("=" * 60)
        
        try:
            # 检查输出文件大小
            file_path = '/workspace/ultimate_analysis.json'
            file_size = os.path.getsize(file_path)
            file_size_mb = file_size / (1024 * 1024)
            
            self.log_issue("INFO", "PERFORMANCE", f"输出文件大小: {file_size_mb:.2f} MB")
            
            # 检查数据密度
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            methods = data.get('methods', [])
            calls = data.get('calls', [])
            
            avg_calls_per_method = len(calls) / len(methods) if len(methods) > 0 else 0
            self.log_issue("INFO", "PERFORMANCE", f"平均每方法调用数: {avg_calls_per_method:.2f}")
            
            # 检查字符串数据量
            total_string_length = 0
            for m in methods[:1000]:  # 抽样检查
                total_string_length += len(str(m.get('name', '')))
            
            self.log_issue("INFO", "PERFORMANCE", f"方法名称平均长度: {total_string_length/1000:.2f}")
            
        except Exception as e:
            self.log_issue("ERROR", "PERFORMANCE", f"检查失败: {str(e)}")
    
    def run_review(self):
        """运行所有核验"""
        print("=" * 80)
        print("🚀 开始静态代码核验")
        print("=" * 80)
        
        self.review_node_analyzer()
        self.review_analysis_result()
        self.review_data_consistency()
        self.review_performance()
        
        print("\n" + "=" * 80)
        print("📊 核验总结")
        print("=" * 80)
        print(f"❌ 错误: {len(self.issues)}")
        print(f"⚠️  警告: {len(self.warnings)}")
        
        if len(self.issues) == 0:
            print("\n✅ 所有核验通过！代码质量优秀！")
        else:
            print(f"\n⚠️  发现 {len(self.issues)} 个错误，需要修复")
        
        return len(self.issues) == 0

if __name__ == "__main__":
    reviewer = StaticCodeReview()
    success = reviewer.run_review()
    exit(0 if success else 1)
