import sqlite3
from fastapi import APIRouter, Request, Form, HTTPException  # <-- **ADDED: Request for session access**
from fastapi.responses import RedirectResponse
from passlib.hash import pbkdf2_sha256
from .database import DB_PATH_USERS, init_users_db

router = APIRouter()
init_users_db()

@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):  # <-- **ADDED: request: Request**
    try:
        conn = sqlite3.connect(DB_PATH_USERS)
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username=?", (username,))
        result = cur.fetchone()
        conn.close()
        if result and pbkdf2_sha256.verify(password, result[0]):
            request.session["user"] = username  # <-- **CHANGED: Store username in session instead of cookie**
            return RedirectResponse("/dashboard", status_code=302)
        return RedirectResponse("/login?error=invalid", status_code=302)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Login error")

@router.post("/logout")
def logout(request: Request):  # <-- **ADDED: request: Request**
    request.session.clear()  # <-- **CHANGED: Clear session instead of deleting cookie**
    return RedirectResponse("/login", status_code=302)