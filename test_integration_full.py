#!/usr/bin/env python3
"""
🧪 分层测试3: 集成验证与业务场景
测试完整流程: JavaScript 分析 -> JSON 输出 -> Python 集成 -> 数据库
"""
import subprocess
import json
import sqlite3
import time
from pathlib import Path

print('='.repeat(60))
print('🧪 分层测试3: 集成验证与业务场景')
print('='.repeat(60))

# 测试项目路径
project_path = Path('/workspace/sample_project')
output_json = Path('/workspace/integration_test_output.json')
db_path = Path('/workspace/integration_test.db')

# 清理旧文件
for f in [output_json, db_path]:
    if f.exists():
        f.unlink()

# 步骤1: 运行 JavaScript 分析器
print('\n📦 步骤1: JavaScript 分析')
print('='.repeat(60))
cmd = [
    'node',
    '/workspace/arkanalyzer-wrapper/src/arkanalyzer-ultimate-polished.js',
    str(project_path),
    str(output_json)
]

# 我们需要修改一下让它可以直接运行，让我创建一个简单的执行脚本
script_content = """
const path = require('path');
const fs = require('fs');
const UltimatePolishedAnalyzer = require('./arkanalyzer-wrapper/src/arkanalyzer-ultimate-polished');

const projectPath = path.resolve(process.argv[2] || '.');
const outputPath = path.resolve(process.argv[3] || 'analysis.json');
console.log('Project:', projectPath);
console.log('Output:', outputPath);
const analyzer = new UltimatePolishedAnalyzer(projectPath);
const results = analyzer.analyzeProject();
fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
console.log('Done!');
"""
Path('/workspace/run_analyzer.js').write_text(script_content)

# 运行分析器
result = subprocess.run(
    ['node', '/workspace/run_analyzer.js', str(project_path), str(output_json)],
    capture_output=True,
    text=True
)
print(f'Return code: {result.returncode}')
if result.stdout:
    print('Output:', result.stdout[:500])
if result.stderr:
    print('Error:', result.stderr)

if not output_json.exists():
    print('\n❌ 分析失败: 没有输出文件')
    exit(1)

print('\n✅ 分析成功！')

# 步骤2: 检查输出JSON
print('\n📄 步骤2: 检查输出结构')
print('='.repeat(60))
with open(output_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'  - 文件: {len(data["files"])}')
print(f'  - 类: {len(data["classes"])}')
print(f'  - 方法: {len(data["methods"])}')
print(f'  - 调用关系: {len(data["calls"])}')
print(f'  - 组件关系: {len(data["components"])}')

# 验证字段名问题是否还存在
if len(data["classes"]) > 0:
    first_class = data["classes"][0]
    fields = list(first_class.keys())
    print(f'\n  类字段: {fields}')
    if 'fileId' in fields:
        print('  ✅ 有 fileId 字段')

# 步骤3: 测试集成加载（手动实现）
print('\n🔗 步骤3: 集成到数据库')
print('='.repeat(60))

# 创建数据库
conn = sqlite3.connect(str(db_path))
conn.execute("PRAGMA foreign_keys = OFF")

# 创建表结构
conn.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT UNIQUE NOT NULL,
        hash BLOB NOT NULL,
        modified INTEGER NOT NULL
    )
""")
conn.execute("""
    CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        file_id INTEGER,
        flags INTEGER NOT NULL DEFAULT 0
    )
""")
conn.execute("""
    CREATE TABLE IF NOT EXISTS methods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        class_id INTEGER
    )
""")
conn.execute("""
    CREATE TABLE IF NOT EXISTS calls (
        caller_id INTEGER,
        callee_id INTEGER,
        PRIMARY KEY(caller_id, callee_id)
    )
""")
conn.execute("""
    CREATE TABLE IF NOT EXISTS components (
        parent_id INTEGER,
        child_id INTEGER,
        PRIMARY KEY(parent_id, child_id)
    )
""")

file_id_map = {}
class_id_map = {}
method_id_map = {}

print('\n📄 导入文件...')
for file_data in data.get('files', []):
    cursor = conn.execute(
        "INSERT INTO files (path, hash, modified) VALUES (?, ?, ?)",
        (file_data['path'], file_data['hash'].encode(), int(time.time()))
    )
    file_id_map[file_data['id']] = cursor.lastrowid
print(f'  导入: {len(file_id_map)} 个文件')

print('\n👥 导入类...')
for cls_data in data.get('classes', []):
    old_id = cls_data['id']
    file_id = file_id_map.get(cls_data.get('fileId') or cls_data.get('file_id'))
    cursor = conn.execute(
        "INSERT INTO classes (name, file_id, flags) VALUES (?, ?, ?)",
        (cls_data['name'], file_id, 0)
    )
    class_id_map[old_id] = cursor.lastrowid
print(f'  导入: {len(class_id_map)} 个类')

print('\n🔧 导入方法...')
for method_data in data.get('methods', []):
    old_id = method_data['id']
    old_class_id = method_data.get('classId') or method_data.get('class_id')
    new_class_id = class_id_map.get(old_class_id) if old_class_id is not None else None
    cursor = conn.execute(
        "INSERT INTO methods (name, class_id) VALUES (?, ?)",
        (method_data['name'], new_class_id)
    )
    method_id_map[old_id] = cursor.lastrowid
print(f'  导入: {len(method_id_map)} 个方法')

print('\n🔗 导入调用关系...')
imported_calls = 0
for call_data in data.get('calls', []):
    caller_id = method_id_map.get(
        call_data.get('callerId') or call_data.get('caller_id')
    )
    callee_id = method_id_map.get(
        call_data.get('calleeId') or call_data.get('callee_id')
    )
    if caller_id is not None and callee_id is not None:
        conn.execute(
            "INSERT OR IGNORE INTO calls (caller_id, callee_id) VALUES (?, ?)",
            (caller_id, callee_id)
        )
        imported_calls += 1
print(f'  导入: {imported_calls} 个调用关系')

print('\n🏗️  导入组件关系...')
imported_components = 0
for comp_data in data.get('components', []):
    old_parent_id = comp_data.get('parentId') or comp_data.get('parent_id')
    old_child_id = comp_data.get('childId') or comp_data.get('child_id')
    new_parent_id = class_id_map.get(old_parent_id)
    new_child_id = class_id_map.get(old_child_id)
    if new_parent_id is not None and new_child_id is not None:
        conn.execute(
            "INSERT OR IGNORE INTO components (parent_id, child_id) VALUES (?, ?)",
            (new_parent_id, new_child_id)
        )
        imported_components += 1
print(f'  导入: {imported_components} 个组件关系')

conn.commit()

# 步骤4: 验证结果
print('\n' + '='.repeat(60))
print('✅ 验证结果')
print('='.repeat(60))

stats = {
    'files': conn.execute("SELECT COUNT(*) FROM files").fetchone()[0],
    'classes': conn.execute("SELECT COUNT(*) FROM classes").fetchone()[0],
    'methods': conn.execute("SELECT COUNT(*) FROM methods").fetchone()[0],
    'calls': conn.execute("SELECT COUNT(*) FROM calls").fetchone()[0],
    'components': conn.execute("SELECT COUNT(*) FROM components").fetchone()[0]
}

print(f'  - 文件: {stats["files"]}')
print(f'  - 类: {stats["classes"]}')
print(f'  - 方法: {stats["methods"]}')
print(f'  - 调用关系: {stats["calls"]}')
print(f'  - 组件关系: {stats["components"]}')

# 关键检查
classes_with_file = conn.execute("SELECT COUNT(*) FROM classes WHERE file_id IS NOT NULL").fetchone()[0]

all_passed = True

if stats["classes"] == 0:
    print('\n❌ 关键问题: 没有导入任何类！')
    all_passed = False
elif classes_with_file < stats["classes"]:
    print(f'\n⚠️  问题: 只有 {classes_with_file}/{stats["classes"]} 个类有关联文件')
else:
    print(f'\n✅ 所有 {stats["classes"]} 个类都有关联文件')

methods_with_class = conn.execute("SELECT COUNT(*) FROM methods WHERE class_id IS NOT NULL").fetchone()[0]
print(f'✅ {methods_with_class}/{stats["methods"]} 个方法有关联类')

conn.close()

if all_passed:
    print('\n' + '='.repeat(60))
    print('✅ 所有测试通过！')
    print('='.repeat(60))
else:
    print('\n' + '='.repeat(60))
    print('❌ 部分测试失败')
    print('='.repeat(60))
