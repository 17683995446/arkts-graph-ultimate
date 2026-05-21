import pytest
from pathlib import Path
from arkts_graph.core.parser import ArkTSParser


def test_parser_initialization():
    parser = ArkTSParser()
    assert parser is not None


def test_parser_extract_class(sample_arkts_file):
    parser = ArkTSParser()
    parsed = parser.parse(sample_arkts_file)
    assert len(parsed.classes) == 1
    assert parsed.classes[0].name == "SampleClass"


def test_parser_extract_methods(sample_arkts_file):
    parser = ArkTSParser()
    parsed = parser.parse(sample_arkts_file)
    method_names = [m.name for m in parsed.methods]
    assert any("method1" in m for m in method_names)
    assert any("method2" in m for m in method_names)


def test_parser_file_hash(sample_arkts_file):
    parser = ArkTSParser()
    parsed1 = parser.parse(sample_arkts_file)
    parsed2 = parser.parse(sample_arkts_file)
    assert parsed1.file_hash == parsed2.file_hash
