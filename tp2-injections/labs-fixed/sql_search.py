"""Lab SQL — version corrigée."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "users.db"


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)"
        )
        conn.execute("DELETE FROM users")
        conn.executemany(
            "INSERT INTO users (username) VALUES (?)",
            [("alice",), ("bob",), ("charlie",)],
        )


def search_users(username: str) -> list[dict]:
    init_db()
    query = "SELECT id, username FROM users WHERE username = ?"
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(query, (username,)).fetchall()
    return [{"id": row[0], "username": row[1]} for row in rows]
