import sys
import os
import pytest
from src.utils import _delete_file_content, _read_file_content
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


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


def test_read_file_content_with_error(tmp_path, capsys, monkeypatch):
    # Create test file
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("some content", encoding="utf-8")

    # Mock the open function to raise an IOError when called
    def mock_open(*args, **kwargs):
        raise IOError("Simulated file read error")

    monkeypatch.setattr('builtins.open', mock_open)

    content = _read_file_content(file_path)
    assert content is None
    captured = capsys.readouterr()
    assert "An error occurred while reading file" in captured.out
