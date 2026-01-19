from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
import os
import sqlite3

app = FastAPI(title="Multi Camera Video Analytics")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "events.db")

# Ensure folders exist
os.makedirs(os.path.join(BASE_DIR, "static"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "snapshots"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "templates"), exist_ok=True)

# Static mounts
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
app.mount("/snapshots", StaticFiles(directory=os.path.join(BASE_DIR, "snapshots")), name="snapshots")

# Templates
templates = Environment(
    loader=FileSystemLoader(os.path.join(BASE_DIR, "templates"))
)

# 🔁 ROOT → DASHBOARD (THIS FIXES YOUR ISSUE)
@app.get("/")
def root():
    return RedirectResponse(url="/dashboard")

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            camera_id TEXT,
            timestamp TEXT,
            rule TEXT,
            object_type TEXT,
            confidence REAL,
            bbox TEXT,
            zone TEXT,
            snapshot_path TEXT
        )
    """)

    cur.execute("SELECT * FROM events ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    events = [
        {
            "id": r[0],
            "camera_id": r[1],
            "timestamp": r[2],
            "rule": r[3],
            "object_type": r[4],
            "confidence": r[5],
            "bbox": r[6],
            "zone": r[7],
            "snapshot_path": r[8],
        }
        for r in rows
    ]

    template = templates.get_template("dashboard.html")
    return template.render(events=events)






