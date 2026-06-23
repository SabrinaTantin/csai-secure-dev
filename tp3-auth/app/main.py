"""Application login sécurisée — TP3."""

import os
import time
from typing import Annotated

import bcrypt
from fastapi import Cookie, FastAPI, HTTPException, Request, Response
from pydantic import BaseModel

SESSION_SECRET = os.getenv("SESSION_SECRET", "test-secret-for-pytest-only")

USERS = {
    "admin": bcrypt.hashpw(b"admin123", bcrypt.gensalt()),
    "student": bcrypt.hashpw(b"python2026", bcrypt.gensalt()),
}

login_attempts: dict[str, list[float]] = {}

MAX_ATTEMPTS = 5
WINDOW_SECONDS = 60

app = FastAPI(title="TP3 Auth Lab")


class LoginRequest(BaseModel):
    username: str
    password: str


def verify_password(username: str, password: str) -> bool:
    stored_hash = USERS.get(username)

    if stored_hash is None:
        return False

    return bcrypt.checkpw(password.encode(), stored_hash)


def check_rate_limit(ip: str) -> None:
    now = time.time()

    attempts = login_attempts.get(ip, [])
    recent_attempts = [
        attempt_time
        for attempt_time in attempts
        if now - attempt_time < WINDOW_SECONDS
    ]

    if len(recent_attempts) >= MAX_ATTEMPTS:
        raise HTTPException(
            status_code=429,
            detail="Too many login attempts. Please try again later.",
        )

    recent_attempts.append(now)
    login_attempts[ip] = recent_attempts


@app.post("/login")
def login(payload: LoginRequest, response: Response, request: Request):
    client_ip = request.client.host if request.client else "unknown"

    check_rate_limit(client_ip)

    if not verify_password(payload.username, payload.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session_token = f"{payload.username}:{SESSION_SECRET}:{int(time.time())}"

    response.set_cookie(
        key="session",
        value=session_token,
        httponly=True,
        samesite="lax",
        secure=True,
    )

    return {"message": "Logged in", "user": payload.username}


@app.get("/profile")
def profile(session: Annotated[str | None, Cookie()] = None):
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")

    username = session.split(":")[0]

    return {"user": username}
