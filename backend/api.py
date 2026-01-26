import os
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
import logging
import sqlite3
from .auth import router as auth_router
from .session import require_login
from .camera_manager import start_camera, stop_camera
from .config import CAMERAS
from .database import DB_PATH_EVENTS

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="Multi-Camera Video Analysis", version="1.0.0")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

static_dir = os.path.join(PROJECT_DIR, "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
else:
    logging.warning("Static directory not found.")

snapshots_dir = os.path.join(PROJECT_DIR, "snapshots")
if os.path.exists(snapshots_dir):
    app.mount("/snapshots", StaticFiles(directory=snapshots_dir), name="snapshots")
else:
    logging.warning("Snapshots directory not found.")

templates_dir = os.path.join(PROJECT_DIR, "templates")
if os.path.exists(templates_dir):
    templates = Environment(loader=FileSystemLoader(templates_dir))
else:
    logging.error("Templates directory not found.")
    templates = None

app.include_router(auth_router)

def get_recent_detections(limit=5):
    try:
        conn = sqlite3.connect(DB_PATH_EVENTS)
        cur = conn.cursor()
        cur.execute("SELECT camera_id, label, confidence, timestamp FROM detections ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        conn.close()
        return [{"camera_id": r[0], "label": r[1], "confidence": r[2], "timestamp": r[3]} for r in rows]
    except Exception as e:
        logging.error(f"Failed to fetch detections: {e}")
        return []

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    if templates:
        template = templates.get_template("login.html")
        return template.render(request=request)
    return {"error": "Templates not loaded"}

@app.get("/dashboard", response_class=HTMLResponse, dependencies=[Depends(require_login)])
def dashboard():
    if not templates:
        return {"error": "Templates not loaded"}
    cameras = [{"id": cam["id"], "status": "Active", "last_detection": "None"} for cam in CAMERAS]
    detections = get_recent_detections(5)
    template = templates.get_template("dashboard.html")
    return template.render(cameras=cameras, detections=detections)

# Protect APIs with auth
@app.get("/api/detections", dependencies=[Depends(require_login)])
def api_get_detections(limit: int = 10):
    return get_recent_detections(limit)

@app.post("/api/cameras/{cam_id}/start", dependencies=[Depends(require_login)])
def api_start_camera(cam_id: int):
    cam = next((c for c in CAMERAS if c["id"] == cam_id), None)
    if not cam:
        raise HTTPException(status_code=404, detail="Camera not found")
    try:
        start_camera(cam_id, cam["source"])
        return {"status": "started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cameras/{cam_id}/stop", dependencies=[Depends(require_login)])
def api_stop_camera(cam_id: int):
    try:
        stop_camera(cam_id)
        return {"status": "stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))