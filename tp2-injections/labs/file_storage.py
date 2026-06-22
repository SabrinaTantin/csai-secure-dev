from pathlib import Path


STORAGE_ROOT = Path(__file__).parent / "storage"
ALLOWED_EXTENSIONS = {".txt", ".md", ".json", ".csv"}


def safe_path(filename):
    if not isinstance(filename, str) or not filename:
        raise ValueError("Invalid filename")

    target = (STORAGE_ROOT / filename).resolve()
    root = STORAGE_ROOT.resolve()

    if not str(target).startswith(str(root)):
        raise ValueError("Invalid path")

    if target.suffix not in ALLOWED_EXTENSIONS:
        raise ValueError("Invalid extension")

    return target


def read_file(filename):
    target = safe_path(filename)
    return target.read_bytes()


def save_file(filename, content):
    target = safe_path(filename)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    return target
