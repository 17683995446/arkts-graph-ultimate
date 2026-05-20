import json
import time
from pathlib import Path
from typing import Optional
from .database import Database
from .models import ParsedFile, ClassEntity, MethodEntity, CallRelationship, ComponentRelationship


class ArkAnalyzerIntegration:
    def __init__(self, db: Database):
        self.db = db

    def load_from_json(self, json_path: Path) -> dict:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        start_time = time.time()
        self.db.clear_all()

        # 创建 ID 映射表（Arkanalyzer ID -> SQLite ID）
        file_id_map = {}
        class_id_map = {}
        method_id_map = {}

        for file_data in data.get('files', []):
            cursor = self.db._get_connection().execute(
                "INSERT INTO files (path, hash, modified) VALUES (?, ?, ?)",
                (file_data['path'], file_data['hash'].encode(), int(time.time()))
            )
            file_id_map[file_data['id']] = cursor.lastrowid

        for cls_data in data.get('classes', []):
            old_id = cls_data['id']
            file_id = file_id_map.get(cls_data.get('fileId') or cls_data.get('file_id'))
            cursor = self.db._get_connection().execute(
                "INSERT INTO classes (name, file_id, flags) VALUES (?, ?, ?)",
                (cls_data['name'], file_id, 0)
            )
            class_id_map[old_id] = cursor.lastrowid

        for method_data in data.get('methods', []):
            old_id = method_data['id']
            old_class_id = method_data.get('classId') or method_data.get('class_id')
            new_class_id = class_id_map.get(old_class_id) if old_class_id is not None else None
            cursor = self.db._get_connection().execute(
                "INSERT INTO methods (name, class_id) VALUES (?, ?)",
                (method_data['name'], new_class_id)
            )
            method_id_map[old_id] = cursor.lastrowid

        # 先收集所有方法名到ID的映射（包含短名称）
        method_name_to_id = {}
        for method_data in data.get('methods', []):
            # 添加完整名称
            method_name_to_id[method_data['name']] = method_data['id']
            # 添加短名称（取::后的部分）
            if '::' in method_data['name']:
                short_name = method_data['name'].split('::')[-1]
                method_name_to_id[short_name] = method_data['id']
        
        # 导入调用关系
        for call_data in data.get('calls', []):
            try:
                # 尝试多种可能的字段名
                caller_id = method_id_map.get(
                    call_data.get('callerId') or 
                    call_data.get('caller_id') or 
                    call_data.get('callerMethod')
                )
                callee_id = method_id_map.get(
                    call_data.get('calleeId') or 
                    call_data.get('callee_id') or 
                    call_data.get('calleeMethod')
                )
                
                if caller_id is not None and callee_id is not None:
                    self.db._get_connection().execute(
                        "INSERT OR IGNORE INTO calls (caller_id, callee_id) VALUES (?, ?)",
                        (caller_id, callee_id)
                    )
            except Exception:
                pass  # 忽略错误

        for comp_data in data.get('components', []):
            try:
                old_parent_id = (
                    comp_data.get('parentId') or 
                    comp_data.get('parent_id')
                )
                old_child_id = (
                    comp_data.get('childId') or 
                    comp_data.get('child_id')
                )
                new_parent_id = class_id_map.get(old_parent_id)
                new_child_id = class_id_map.get(old_child_id)
                if new_parent_id is not None and new_child_id is not None:
                    self.db._get_connection().execute(
                        "INSERT OR IGNORE INTO components (parent_id, child_id) VALUES (?, ?)",
                        (new_parent_id, new_child_id)
                    )
            except Exception:
                pass

        self.db._get_connection().commit()
        elapsed = time.time() - start_time

        return {
            'files': len(data.get('files', [])),
            'classes': len(data.get('classes', [])),
            'methods': len(data.get('methods', [])),
            'calls': len(data.get('calls', [])),
            'components': len(data.get('components', [])),
            'elapsed': elapsed
        }

    def run_arkanalyzer(self, project_path: Path, output_path: Path) -> dict:
        import subprocess
        import sys

        # 从 /workspace/arkts_graph/core/ark_analyzer_integration.py
        # 到 /workspace/arkanalyzer-wrapper/src/cli.js
        wrapper_path = Path(__file__).parent.parent.parent / 'arkanalyzer-wrapper' / 'src' / 'cli.js'
        cmd = ['node', str(wrapper_path), str(project_path), str(output_path)]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ArkAnalyzer failed: {result.stderr}")

        return self.load_from_json(output_path)
