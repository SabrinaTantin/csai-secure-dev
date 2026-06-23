"""API REST vulnérable — TP4."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="TP4 Web API Lab")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NOTES: list[dict] = []


@app.get("/notes")
def list_notes():
    return NOTES


@app.post("/notes")
def create_note(payload: dict):
    note = {"id": len(NOTES) + 1, "title": payload.get("title"), "content": payload.get("content")}
    NOTES.append(note)
    return note


@app.get("/notes/{note_id}")
def get_note(note_id: int):
    for note in NOTES:
        if note["id"] == note_id:
            html = f"<html><body><h1>{note['title']}</h1><div>{note['content']}</div></body></html>"
            return {"html": html}
    return {"error": "not found"}
