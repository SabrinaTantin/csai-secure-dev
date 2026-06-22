import sqlite3


def init_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT)")
    conn.executemany(
        "INSERT INTO users (id, username) VALUES (?, ?)",
        [
            (1, "alice"),
            (2, "bob"),
            (3, "charlie"),
        ],
    )
    conn.commit()
    return conn


def search_users(username):
    conn = init_db()

    # Correction : requête SQL paramétrée.
    # L'entrée utilisateur n'est jamais concaténée dans la requête SQL.
    rows = conn.execute(
        "SELECT id, username FROM users WHERE username = ?",
        (username,),
    ).fetchall()

    return [dict(row) for row in rows]
