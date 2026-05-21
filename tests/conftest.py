import pytest
import tempfile
from pathlib import Path


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


@pytest.fixture
def sample_arkts_file(temp_dir):
    file_path = temp_dir / "Sample.ets"
    content = '''
class SampleClass {
    method1() {
        this.method2();
    }
    method2() {
        console.log("Hello");
    }
}
'''
    file_path.write_text(content, encoding="utf-8")
    return file_path
