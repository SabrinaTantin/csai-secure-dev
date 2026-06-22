"""Lab path traversal — version corrigée."""

from pathlib import Path

STORAGE_ROOT = Path(__file__).parent / "storage"


def _safe_path(filename: str) -> Path:
    target = (STORAGE_ROOT / filename).resolve()
    root = STORAGE_ROOT.resolve()
    if not str(target).startswith(str(root)):
        raise ValueError("Path traversal detected")
    return target


def save_file(filename: str, content: bytes) -> Path:
    STORAGE_ROOT.mkdir(parents=True, exist_ok=True)
    target = _safe_path(filename)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    return target


def read_file(filename: str) -> bytes:
    target = _safe_path(filename)
    return target.read_bytes()
