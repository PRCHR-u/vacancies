import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.utils import _delete_file_content, _read_file_content



def test_delete_file_content_existing_file(tmp_path):
    file_path = tmp_path / "test_file.txt"
    with open(file_path, "w") as f:
        f.write("some content")
    _delete_file_content(file_path)
    assert file_path.read_text() == ""


def test_delete_file_content_nonexistent_file(tmp_path):
    file_path = tmp_path / "nonexistent_file.txt"
    with pytest.raises(FileNotFoundError):
        _delete_file_content(file_path)
    assert not file_path.exists()


def test_read_file_content_existing_file(tmp_path):
    file_path = tmp_path / "test_file.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("some content")
    content = _read_file_content(file_path)
    assert content == "some content"


def test_read_file_content_nonexistent_file(tmp_path):
    file_path = tmp_path / "nonexistent_file.txt"
    content = _read_file_content(file_path)
    assert content is None
    assert not file_path.exists()


def test_read_file_content_with_error(tmp_path, capsys):

    file_path = tmp_path / "test_file.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("some content")
    os.chmod(file_path, 0o000)
    content = _read_file_content(file_path)
    assert content is None
    captured = capsys.readouterr()
    assert "An error occurred while reading file" in captured.out
    os.chmod(file_path, 0o777)
    os.remove(file_path)
