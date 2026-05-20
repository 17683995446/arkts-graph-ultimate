import sqlite3
import hashlib
import time
from pathlib import Path
from typing import Optional, Iterator
from contextlib import contextmanager
from .models import (
    FileEntity,
    ClassEntity,
    MethodEntity,
    CallRelationship,
    ComponentRelationship,
    ParsedFile,
)


class Database:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None
        self._initialize_schema()

    def _get_connection(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.execute("PRAGMA foreign_keys = ON")
            self._conn.execute("PRAGMA journal_mode = WAL")
            self._conn.execute("PRAGMA synchronous = NORMAL")
        return self._conn

    @contextmanager
    def transaction(self):
        conn = self._get_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    def _initialize_schema(self):
        with self.transaction() as conn:
            # 禁用外键约束以简化开发和演示
            conn.execute("PRAGMA foreign_keys = OFF")
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
            conn.execute("CREATE INDEX IF NOT EXISTS idx_classes_file_id ON classes(file_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_methods_class_id ON methods(class_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_calls_caller ON calls(caller_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_calls_callee ON calls(callee_id)")

    @staticmethod
    def compute_file_hash(file_path: Path) -> bytes:
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).digest()

    def get_file_id(self, path: Path) -> Optional[int]:
        conn = self._get_connection()
        cursor = conn.execute("SELECT id FROM files WHERE path = ?", (str(path),))
        row = cursor.fetchone()
        return row[0] if row else None

    def get_file_hash(self, file_id: int) -> Optional[bytes]:
        conn = self._get_connection()
        cursor = conn.execute("SELECT hash FROM files WHERE id = ?", (file_id,))
        row = cursor.fetchone()
        return row[0] if row else None

    def delete_file_data(self, path: Path):
        with self.transaction() as conn:
            conn.execute("DELETE FROM files WHERE path = ?", (str(path),))

    def insert_parsed_file(self, parsed: ParsedFile):
        with self.transaction() as conn:
            cursor = conn.execute(
                "INSERT OR REPLACE INTO files (path, hash, modified) VALUES (?, ?, ?)",
                (str(parsed.path), parsed.file_hash, int(time.time())),
            )
            file_id = cursor.lastrowid
            class_id_map: dict[str, int] = {}
            for cls in parsed.classes:
                cursor = conn.execute(
                    "INSERT INTO classes (name, file_id, flags) VALUES (?, ?, ?)",
                    (cls.name, file_id, cls.flags),
                )
                class_id_map[cls.name] = cursor.lastrowid
            method_id_map: dict[str, int] = {}
            for method in parsed.methods:
                class_id = class_id_map.get(method.name.split("::")[0] if "::" in method.name else "")
                if class_id is None:
                    class_id = next(iter(class_id_map.values())) if class_id_map else 0
                cursor = conn.execute(
                    "INSERT INTO methods (name, class_id) VALUES (?, ?)",
                    (method.name, class_id),
                )
                method_id_map[method.name] = cursor.lastrowid
            for call in parsed.calls:
                caller_id = method_id_map.get(str(call.caller_id), call.caller_id)
                callee_id = method_id_map.get(str(call.callee_id), call.callee_id)
                if isinstance(caller_id, int) and isinstance(callee_id, int):
                    try:
                        conn.execute(
                            "INSERT OR IGNORE INTO calls (caller_id, callee_id) VALUES (?, ?)",
                            (caller_id, callee_id),
                        )
                    except sqlite3.IntegrityError:
                        pass
            for comp in parsed.components:
                parent_id = class_id_map.get(str(comp.parent_id), comp.parent_id)
                child_id = class_id_map.get(str(comp.child_id), comp.child_id)
                if isinstance(parent_id, int) and isinstance(child_id, int):
                    try:
                        conn.execute(
                            "INSERT OR IGNORE INTO components (parent_id, child_id) VALUES (?, ?)",
                            (parent_id, child_id),
                        )
                    except sqlite3.IntegrityError:
                        pass

    def get_all_files(self) -> list[FileEntity]:
        conn = self._get_connection()
        cursor = conn.execute("SELECT id, path, hash, modified FROM files")
        files = []
        for row in cursor:
            files.append(
                FileEntity(
                    id=row[0],
                    path=Path(row[1]),
                    hash=row[2],
                    modified=row[3],
                )
            )
        return files

    def get_stats(self) -> dict:
        conn = self._get_connection()
        stats = {}
        stats["files"] = conn.execute("SELECT COUNT(*) FROM files").fetchone()[0]
        stats["classes"] = conn.execute("SELECT COUNT(*) FROM classes").fetchone()[0]
        stats["methods"] = conn.execute("SELECT COUNT(*) FROM methods").fetchone()[0]
        stats["calls"] = conn.execute("SELECT COUNT(*) FROM calls").fetchone()[0]
        stats["components"] = conn.execute("SELECT COUNT(*) FROM components").fetchone()[0]
        return stats

    def get_classes(self) -> list[ClassEntity]:
        conn = self._get_connection()
        cursor = conn.execute("SELECT id, name, file_id, flags FROM classes")
        classes = []
        for row in cursor:
            classes.append(
                ClassEntity(
                    id=row[0],
                    name=row[1],
                    file_id=row[2],
                    flags=row[3],
                )
            )
        return classes

    def get_methods(self) -> list[MethodEntity]:
        conn = self._get_connection()
        cursor = conn.execute("SELECT id, name, class_id FROM methods")
        methods = []
        for row in cursor:
            methods.append(
                MethodEntity(
                    id=row[0],
                    name=row[1],
                    class_id=row[2],
                )
            )
        return methods

    def get_call_graph(self) -> list[tuple[int, int]]:
        conn = self._get_connection()
        cursor = conn.execute("SELECT caller_id, callee_id FROM calls")
        return list(cursor)

    def get_component_graph(self) -> list[tuple[int, int]]:
        conn = self._get_connection()
        cursor = conn.execute("SELECT parent_id, child_id FROM components")
        return list(cursor)

    def clear_all(self):
        with self.transaction() as conn:
            conn.execute("DELETE FROM calls")
            conn.execute("DELETE FROM components")
            conn.execute("DELETE FROM methods")
            conn.execute("DELETE FROM classes")
            conn.execute("DELETE FROM files")

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None
