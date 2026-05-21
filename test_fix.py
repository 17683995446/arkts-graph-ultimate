#!/usr/bin/env python3
import json
import sqlite3
import time
from pathlib import Path

print('='.repeat(60))
print('🔧 测试修复后的集成')
print('='.repeat(60))

# 加载测试数据
with open('/workspace/test_output_structure.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 简单的数据库测试
db_path = Path('/workspace/test_fixed.db')
if db_path.exists():
    db_path.unlink()

conn = sqlite3.connect(str(db_path))
conn.execute("PRAGMA foreign_keys = OFF")

# 创建表
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

# 导入文件
print('\n📄 导入文件...')
for file_data in data.get('files', []):
    cursor = conn.execute(
        "INSERT INTO files (path, hash, modified) VALUES (?, ?, ?)",
        (file_data['path'], file_data['hash'].encode(), int(time.time()))
    )
    file_id_map[file_data['id']] = cursor.lastrowid
print(f'  导入 {len(file_id_map)} 个文件')

# 导入类（修复后的版本）
print('\n👥 导入类...')
for cls_data in data.get('classes', []):
    old_id = cls_data['id']
    file_id = file_id_map.get(cls_data.get('fileId') or cls_data.get('file_id'))
    cursor = conn.execute(
        "INSERT INTO classes (name, file_id, flags) VALUES (?, ?, ?)",
        (cls_data['name'], file_id, 0)
    )
    class_id_map[old_id] = cursor.lastrowid
print(f'  导入 {len(class_id_map)} 个类')

# 导入方法
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
print(f'  导入 {len(method_id_map)} 个方法')

# 导入调用关系
print('\n🔗 导入调用关系...')
for call_data in data.get('calls', []):
    caller_id = method_id_map.get(call_data.get('callerId') or call_data.get('caller_id'))
    callee_id = method_id_map.get(call_data.get('calleeId') or call_data.get('callee_id'))
    if caller_id is not None and callee_id is not None:
        conn.execute(
            "INSERT OR IGNORE INTO calls (caller_id, callee_id) VALUES (?, ?)",
            (caller_id, callee_id)
        )

# 导入组件关系
print('\n🏗️  导入组件关系...')
for comp_data in data.get('components', []):
    old_parent_id = comp_data.get('parentId') or comp_data.get('parent_id')
    old_child_id = comp_data.get('childId') or comp_data.get('child_id')
    new_parent_id = class_id_map.get(old_parent_id) if old_parent_id is not None else None
    new_child_id = class_id_map.get(old_child_id) if old_child_id is not None else None
    if new_parent_id is not None and new_child_id is not None:
        conn.execute(
            "INSERT OR IGNORE INTO components (parent_id, child_id) VALUES (?, ?)",
            (new_parent_id, new_child_id)
        )

conn.commit()

# 验证结果
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
print(f'  - 调用: {stats["calls"]}')
print(f'  - 组件: {stats["components"]}')

# 检查类是否都有 file_id
classes_with_file = conn.execute("SELECT COUNT(*) FROM classes WHERE file_id IS NOT NULL").fetchone()[0]
print(f'\n🔍 类与文件关联: {classes_with_file}/{stats["classes"]}')

if stats["classes"] == 0:
    print('\n❌ 问题仍存在！')
else:
    print('\n✅ 修复成功！')

conn.close()
