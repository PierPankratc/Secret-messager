import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient


def build_client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DSN", f"sqlite:///{db_path}")

    for module_name in ["main", "src.db.create_db", "src.db.models", "src.routers.users"]:
        sys.modules.pop(module_name, None)

    import main

    return TestClient(main.app)


def test_register_user_and_one_time_message_link(tmp_path, monkeypatch):
    client = build_client(tmp_path, monkeypatch)

    register_response = client.post(
        "/user/register",
        json={"user": "alice", "passwd": "secret123"},
    )
    assert register_response.status_code == 200
    assert register_response.json()["user"] == "alice"

    login_response = client.post(
        "/user/login",
        json={"user": "alice", "passwd": "secret123"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    message_response = client.post(
        "/message",
        json={"message": "hello from secret"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert message_response.status_code == 200
    link = message_response.json()["link"]

    first_read = client.get(link, follow_redirects=False, headers={"Authorization": f"Bearer {token}"})
    assert first_read.status_code == 200
    assert first_read.json()["message"] == "hello from secret"

    second_read = client.get(link, follow_redirects=False, headers={"Authorization": f"Bearer {token}"})
    assert second_read.status_code == 404
