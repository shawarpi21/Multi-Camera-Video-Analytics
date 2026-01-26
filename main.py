import time
import signal
import sys
import os
from backend.camera_manager import start_camera, stop_camera
from backend.config import CAMERAS
from backend.api import app  # Import app directly
import uvicorn  # Import uvicorn directly

# Additional imports for web routes and auth
from fastapi import Request, Form, HTTPException, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware  # For session-based auth

# Add session middleware (required for auth)
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-here")  # Change to a secure random key in production

# Set up templates and static files
templates = Jinja2Templates(directory="templates")  # Assuming HTML files are in 'templates' folder
app.mount("/static", StaticFiles(directory="static"), name="static")  # For CSS/JS if needed

active_cameras = set()

# Mock data (replace with real data from your backend, e.g., from database or config)
cameras = [
    {"id": 1, "status": "Active", "last_detection": "2023-10-01 12:00:00"},
    {"id": 2, "status": "Inactive", "last_detection": "None"}
]
detections = [
    {"timestamp": "2023-10-01 12:00:00", "label": "Person", "confidence": 0.95},
    {"timestamp": "2023-10-01 11:45:00", "label": "Car", "confidence": 0.88}
]

# Auth dependency for API routes (raises HTTPException for JSON responses)
def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

# Helper function for HTML routes (redirects to login)
def require_auth(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login?error=Authentication required", status_code=303)
    return user

# Login route - GET to serve the page, POST to handle form submission
@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request, error: str = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    # Add your authentication logic here (e.g., check DB, hash password)
    if username == "admin" and password == "password":  # Example - replace with real auth
        request.session["user"] = username  # Set session on success
        return RedirectResponse(url="/dashboard", status_code=303)  # Redirect to dashboard
    else:
        # Redirect back to login with error
        return RedirectResponse(url="/login?error=Invalid credentials", status_code=303)

# Signup route (if needed, similar to login)
@app.get("/signup", response_class=HTMLResponse)
async def get_signup(request: Request, error: str = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})  # Reuse login.html

@app.post("/signup")
async def signup(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # Add signup logic (e.g., create user in DB)
    request.session["user"] = username  # Set session on success
    return RedirectResponse(url="/dashboard", status_code=303)

# Dashboard route (GET only, renders HTML) - Checks auth manually and redirects if needed
@app.get("/dashboard")
async def dashboard(request: Request):
    auth_check = require_auth(request)
    if isinstance(auth_check, RedirectResponse):
        return auth_check  # Redirect to login if not authenticated
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "cameras": cameras,
        "detections": detections
    })

# Logout route (POST from dashboard.html) - Clears session
@app.post("/logout")
async def logout(request: Request):
    request.session.clear()  # Clear session
    return RedirectResponse(url="/login", status_code=303)  # Redirect to login

# API routes for dashboard interactions (e.g., start/stop camera) - Use proper dependency for JSON responses
@app.post("/api/cameras/{camera_id}/start")
async def api_start_camera(camera_id: int, user: str = Depends(get_current_user)):
    try:
        start_camera(camera_id, next((cam["source"] for cam in CAMERAS if cam["id"] == camera_id), None))
        active_cameras.add(camera_id)
        return {"message": f"Camera {camera_id} started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cameras/{camera_id}/stop")
async def api_stop_camera(camera_id: int, user: str = Depends(get_current_user)):
    try:
        stop_camera(camera_id)
        active_cameras.discard(camera_id)
        return {"message": f"Camera {camera_id} stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/detections")
async def get_detections(limit: int = 5, user: str = Depends(get_current_user)):
    # Return recent detections (replace with real logic)
    return detections[:limit]

def start_all_cameras():
    for cam in CAMERAS:
        try:
            start_camera(cam["id"], cam["source"])
            active_cameras.add(cam["id"])
            print(f"[INFO] Started camera {cam['id']}")
        except Exception as e:
            print(f"[ERROR] Failed to start camera {cam['id']}: {e}")

def stop_all_cameras():
    for cam_id in list(active_cameras):
        stop_camera(cam_id)
        active_cameras.remove(cam_id)
        print(f"[INFO] Stopped camera {cam_id}")

def signal_handler(sig, frame):
    print("[SYSTEM] Shutting down...")
    stop_all_cameras()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    print("[SYSTEM] Starting Multi-Camera Video Analytics")
    start_all_cameras()
    print("[INFO] Starting web server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)