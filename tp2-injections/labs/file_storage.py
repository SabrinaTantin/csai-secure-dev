"""Lab path traversal — version vulnérable."""

from pathlib import Path

STORAGE_ROOT = Path(__file__).parent / "storage"


def save_file(filename: str, content: bytes) -> Path:
    STORAGE_ROOT.mkdir(parents=True, exist_ok=True)
    target = STORAGE_ROOT / filename
    target.write_bytes(content)
    return target


def read_file(filename: str) -> bytes:
    target = STORAGE_ROOT / filename
    return target.read_bytes()
