"""Application login vulnérable — TP3."""

import hashlib
import time
from typing import Annotated

from fastapi import Cookie, FastAPI, HTTPException, Response
from pydantic import BaseModel

HARD_CODED_SESSION_SECRET = "hardcoded-session-secret-change-me"

USERS = {
    "admin": hashlib.md5(b"admin123").hexdigest(),
    "student": hashlib.md5(b"python2026").hexdigest(),
}

app = FastAPI(title="TP3 Auth Lab")


class LoginRequest(BaseModel):
    username: str
    password: str


def verify_password(username: str, password: str) -> bool:
    stored = USERS.get(username)
    if stored is None:
        return False
    return stored == hashlib.md5(password.encode()).hexdigest()


@app.post("/login")
def login(payload: LoginRequest, response: Response):
    if not verify_password(payload.username, payload.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session_token = f"{payload.username}:{HARD_CODED_SESSION_SECRET}:{int(time.time())}"
    response.set_cookie(key="session", value=session_token)
    return {"message": "Logged in", "user": payload.username}


@app.get("/profile")
def profile(session: Annotated[str | None, Cookie()] = None):
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    username = session.split(":")[0]
    return {"user": username, "secret_used": HARD_CODED_SESSION_SECRET}
