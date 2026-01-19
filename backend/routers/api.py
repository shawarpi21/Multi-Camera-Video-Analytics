import os
import sqlite3
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader

router = APIRouter()

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "events.db")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

# Setup Jinja2
templates = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# Dashboard route
@router.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    # Ensure snapshots folder exists
    os.makedirs(os.path.join(BASE_DIR, "snapshots"), exist_ok=True)

    # Query events
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, camera_id, timestamp, rule, object_type, confidence, snapshot_path
        FROM events
        ORDER BY id DESC
        LIMIT 100
    """)
    rows = cur.fetchall()
    conn.close()

    # Convert rows to dicts for template
    events = [
        {
            "id": r[0],
            "camera_id": r[1],
            "timestamp": r[2],
            "rule": r[3],
            "object_type": r[4],
            "confidence": r[5],
            "snapshot_path": r[6]
        } for r in rows
    ]

    template = templates.get_template("dashboard.html")
    return template.render(events=events)

# Example placeholder for GET /events
@router.get("/events")
def get_events():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM events ORDER BY id DESC LIMIT 100")
    rows = cur.fetchall()
    conn.close()
    return {"events": rows}
