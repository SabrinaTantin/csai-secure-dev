"""Tests TP2 — Lab path traversal."""

from pathlib import Path

from labs import file_storage


def setup_module():
    file_storage.STORAGE_ROOT.mkdir(parents=True, exist_ok=True)
    (file_storage.STORAGE_ROOT / "allowed.txt").write_text("ok", encoding="utf-8")
    secret = file_storage.STORAGE_ROOT.parent / "secret.txt"
    secret.write_text("top-secret", encoding="utf-8")


def test_read_allowed_file():
    content = file_storage.read_file("allowed.txt")
    assert content == b"ok"


def test_reject_parent_directory_traversal():
    try:
        file_storage.read_file("../secret.txt")
        assert False, "Path traversal non bloqué"
    except (ValueError, FileNotFoundError, OSError):
        pass


def test_save_stays_in_storage_root():
    saved = file_storage.save_file("nested/out.txt", b"data")
    assert str(saved.resolve()).startswith(str(file_storage.STORAGE_ROOT.resolve()))
