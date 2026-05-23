#!/usr/bin/env python3
"""
快速关键测试 - 验证核心功能
"""

import json
import os
import subprocess
import time

def test_quick():
    print("🚀 快速关键测试")
    print("=" * 60)
    
    # 测试1: 基础分析
    print("\n1. 测试基础分析...")
    result = subprocess.run(
        [
            "node",
            "/workspace/arkanalyzer-wrapper/src/arkanalyzer-final-fixed.js",
            "/workspace/UltimateChaosProject",
            "/tmp/quick_test.json"
        ],
        capture_output=True,
        text=True,
        timeout=60
    )
    
    if result.returncode == 0:
        print("  ✅ 分析成功")
        
        with open('/tmp/quick_test.json', 'r') as f:
            data = json.load(f)
        
        print(f"  文件: {len(data['files'])}, 类: {len(data['classes'])}, 方法: {len(data['methods'])}")
    else:
        print(f"  ❌ 分析失败: {result.stderr}")
    
    # 测试2: 输出格式
    print("\n2. 测试输出格式...")
    required_fields = ['files', 'classes', 'methods', 'calls']
    has_all = all(field in data for field in required_fields)
    print(f"  {'✅' if has_all else '❌'} 输出格式正确")
    
    # 测试3: 数据一致性
    print("\n3. 测试数据一致性...")
    file_ids = set([f['id'] for f in data['files']])
    class_file_ids = set([c['fileId'] for c in data['classes']])
    refs_valid = class_file_ids.issubset(file_ids)
    print(f"  {'✅' if refs_valid else '❌'} 引用完整性")
    
    # 测试4: 性能
    print("\n4. 测试性能...")
    start = time.time()
    result = subprocess.run(
        [
            "node",
            "/workspace/arkanalyzer-wrapper/src/arkanalyzer-final-fixed.js",
            "/workspace/sample_project",
            "/tmp/perf_test.json"
        ],
        capture_output=True,
        text=True,
        timeout=10
    )
    duration = time.time() - start
    print(f"  ⏱️  耗时: {duration:.2f}s")
    
    print("\n" + "=" * 60)
    print("🎉 快速测试完成！")

if __name__ == "__main__":
    test_quick()
