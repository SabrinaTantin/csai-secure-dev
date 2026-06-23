"""Tests TP4 — à faire passer après durcissement."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def setup_function():
    import app.main as main_module

    main_module.NOTES.clear()


def test_create_note_with_validation():
    response = client.post(
        "/notes",
        json={"title": "Hello", "content": "Safe content"},
    )
    assert response.status_code in (200, 201)


def test_xss_payload_is_neutralized():
    client.post("/notes", json={"title": "x", "content": "<script>alert(1)</script>"})
    response = client.get("/notes/1")
    body = response.json()
    assert "<script>" not in body.get("html", "")


def test_security_headers_present():
    response = client.get("/notes")
    headers = response.headers
    assert "x-content-type-options" in {k.lower() for k in headers.keys()}
