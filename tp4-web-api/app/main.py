"""API REST durcie — TP4."""

import html
from typing import Any

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="TP4 Web API sécurisée")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.middleware("http")
async def add_security_headers(request: Any, call_next: Any) -> Response:
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1, max_length=500)

    @field_validator("title", "content")
    @classmethod
    def reject_dangerous_characters(cls, value: str) -> str:
        dangerous_patterns = ["<script", "</script", "javascript:"]
        lowered_value = value.lower()

        if any(pattern in lowered_value for pattern in dangerous_patterns):
            return html.escape(value)

        return value


NOTES: list[dict[str, Any]] = []


@app.get("/notes")
def list_notes() -> list[dict[str, Any]]:
    return NOTES


@app.post("/notes")
def create_note(payload: NoteCreate) -> dict[str, Any]:
    note = {
        "id": len(NOTES) + 1,
        "title": html.escape(payload.title),
        "content": html.escape(payload.content),
    }
    NOTES.append(note)
    return note


@app.get("/notes/{note_id}")
def get_note(note_id: int) -> dict[str, str]:
    for note in NOTES:
        if note["id"] == note_id:
            safe_title = html.escape(str(note["title"]))
            safe_content = html.escape(str(note["content"]))
            rendered_html = (
                f"<html><body><h1>{safe_title}</h1>"
                f"<div>{safe_content}</div></body></html>"
            )
            return {"html": rendered_html}

    return {"error": "not found"}
