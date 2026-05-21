import time
import pytest
from pathlib import Path
from arkts_graph.core.database import Database
from arkts_graph.core.engine import UpdateEngine
from arkts_graph.core.models import ChangeType


def test_full_sync(temp_dir):
    db_path = temp_dir / "test.db"
    project_dir = temp_dir / "project"
    project_dir.mkdir()
    file1 = project_dir / "File1.ets"
    file1.write_text("class Class1 { method1() {} }")
    file2 = project_dir / "File2.ts"
    file2.write_text("class Class2 { method2() {} }")
    db = Database(db_path)
    engine = UpdateEngine(project_dir, db)
    count, elapsed = engine.full_sync()
    assert count == 2
    stats = db.get_stats()
    assert stats["files"] == 2
    assert stats["classes"] == 2
    db.close()


def test_single_file_update(temp_dir):
    db_path = temp_dir / "test.db"
    project_dir = temp_dir / "project"
    project_dir.mkdir()
    test_file = project_dir / "Test.ets"
    test_file.write_text("class Test { test() {} }")
    db = Database(db_path)
    engine = UpdateEngine(project_dir, db)
    elapsed = engine._update_single_file(test_file, ChangeType.CREATED)
    assert elapsed >= 0
    stats = db.get_stats()
    assert stats["files"] == 1
    assert stats["classes"] == 1
    elapsed = engine._update_single_file(test_file, ChangeType.DELETED)
    assert elapsed >= 0
    stats = db.get_stats()
    assert stats["files"] == 0
    db.close()
