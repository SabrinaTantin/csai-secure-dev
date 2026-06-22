"""Tests TP3 — à faire passer après sécurisation."""

import os

from fastapi.testclient import TestClient

os.environ.setdefault("SESSION_SECRET", "test-secret-for-pytest-only")

from app.main import app  # noqa: E402

client = TestClient(app)


def test_login_success():
    response = client.post("/login", json={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    cookie = response.cookies.get("session")
    assert cookie is not None


def test_login_invalid_password():
    response = client.post("/login", json={"username": "admin", "password": "wrong"})
    assert response.status_code == 401


def test_session_cookie_is_httponly():
    response = client.post("/login", json={"username": "admin", "password": "admin123"})
    set_cookie = response.headers.get("set-cookie", "")
    assert "httponly" in set_cookie.lower()
