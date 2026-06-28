import importlib
import sys
from pathlib import Path


def test_create_db_imports_and_creates_sqlite_database(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DSN", f"sqlite:///{db_path}")
    monkeypatch.chdir(tmp_path)

    sys.modules.pop("src.db.create_db", None)
    sys.modules.pop("src.db.models", None)

    module = importlib.import_module("src.db.create_db")

    assert module.engine is not None
    assert db_path.exists()
