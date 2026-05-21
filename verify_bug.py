#!/usr/bin/env python3
import json
from pathlib import Path

print('='.repeat(60))
print('🔍 测试3: 验证字段名问题')
print('='.repeat(60))

# 1. 检查 JSON 输出
test_json = Path('/workspace/test_output_structure.json')
data = json.load(open(test_json, 'r', encoding='utf-8'))

print('\n📄 JSON 结构分析:')
print(f'  - files: {len(data["files"])}')
if data["files"]:
    print(f'  - 文件字段: {list(data["files"][0].keys())}')

print(f'\n  - classes: {len(data["classes"])}')
if data["classes"]:
    print(f'  - 类字段: {list(data["classes"][0].keys())}')
    print(f'  - 示例类: {data["classes"][0]}')

print(f'\n  - components: {len(data["components"])}')
if data["components"]:
    print(f'  - 组件字段: {list(data["components"][0].keys())}')

print('\n' + '='.repeat(60))
print('❌ 发现的问题:')
print('='.repeat(60))

# 问题 1: 字段名不匹配 - fileId vs file_id
print('\n1️⃣  字段名不匹配:')
print('  - JavaScript 输出: fileId (驼峰命名)')
print('  - Python 集成: file_id (下划线命名)')

# 问题 2: 让我直接读取 integration 代码
print('\n2️⃣  集成代码中的问题:')
print('  - line 34: cls_data.get("file_id") -> 应该是 "fileId"')
print('  - 这导致 class 没有 file_id，可能导致查询失败')

print('\n' + '='.repeat(60))
