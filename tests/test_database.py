import pytest
from pathlib import Path
from arkts_graph.core.database import Database
from arkts_graph.core.models import ParsedFile, ClassEntity, MethodEntity


def test_database_initialization(temp_dir):
    db_path = temp_dir / "test.db"
    db = Database(db_path)
    assert db_path.exists()
    db.close()


def test_database_insert_and_retrieve(temp_dir, sample_arkts_file):
    db_path = temp_dir / "test.db"
    db = Database(db_path)
    parsed = ParsedFile(
        path=sample_arkts_file,
        file_hash=b"testhash",
        classes=[ClassEntity(name="SampleClass")],
        methods=[MethodEntity(name="method1"), MethodEntity(name="method2")],
    )
    db.insert_parsed_file(parsed)
    stats = db.get_stats()
    assert stats["files"] == 1
    assert stats["classes"] == 1
    assert stats["methods"] == 2
    classes = db.get_classes()
    assert len(classes) == 1
    assert classes[0].name == "SampleClass"
    methods = db.get_methods()
    assert len(methods) == 2
    db.close()


def test_database_delete_file(temp_dir, sample_arkts_file):
    db_path = temp_dir / "test.db"
    db = Database(db_path)
    parsed = ParsedFile(
        path=sample_arkts_file,
        file_hash=b"testhash",
        classes=[ClassEntity(name="SampleClass")],
    )
    db.insert_parsed_file(parsed)
    assert db.get_stats()["files"] == 1
    db.delete_file_data(sample_arkts_file)
    assert db.get_stats()["files"] == 0
    db.close()


def test_database_clear_all(temp_dir, sample_arkts_file):
    db_path = temp_dir / "test.db"
    db = Database(db_path)
    parsed = ParsedFile(
        path=sample_arkts_file,
        file_hash=b"testhash",
        classes=[ClassEntity(name="SampleClass")],
        methods=[MethodEntity(name="method1")],
    )
    db.insert_parsed_file(parsed)
    stats = db.get_stats()
    assert stats["files"] == 1
    assert stats["classes"] == 1
    db.clear_all()
    stats = db.get_stats()
    assert stats["files"] == 0
    assert stats["classes"] == 0
    db.close()
