"""Mini-application volontairement vulnérable — TP1 audit."""

import hashlib
import logging
import os
import pickle
import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request, send_file

APP_SECRET = "super-secret-key-do-not-share"
UPLOAD_DIR = Path(__file__).parent / "uploads"
DB_PATH = Path(__file__).parent / "users.db"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["SECRET_KEY"] = APP_SECRET


def init_db() -> None:
    UPLOAD_DIR.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
        )
        conn.execute(
            "INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'admin123')"
        )


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/users/search")
def search_users():
    username = request.args.get("username", "")
    query = f"SELECT id, username FROM users WHERE username = '{username}'"
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(query).fetchall()
    return jsonify([{"id": row[0], "username": row[1]} for row in rows])


@app.route("/users/register", methods=["POST"])
def register_user():
    data = request.get_json(force=True)
    username = data.get("username", "")
    password = data.get("password", "")
    logger.info("Register attempt username=%s password=%s", username, password)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password)),
        )
    return jsonify({"message": "User created"}), 201


@app.route("/files/upload", methods=["POST"])
def upload_file():
    filename = request.form.get("filename", "upload.bin")
    content = request.files["file"].read()
    target = UPLOAD_DIR / filename
    target.write_bytes(content)
    return jsonify({"saved_as": str(target)})


@app.route("/files/download")
def download_file():
    filename = request.args.get("name", "")
    target = UPLOAD_DIR / filename
    return send_file(target)


@app.route("/session/load", methods=["POST"])
def load_session():
    token = request.data
    session = pickle.loads(token)
    return jsonify({"session": session})


@app.route("/admin/config")
def admin_config():
    return jsonify(
        {
            "secret_key": APP_SECRET,
            "db_path": str(DB_PATH),
            "debug": os.environ.get("FLASK_DEBUG", "true"),
        }
    )


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5001, debug=True)
