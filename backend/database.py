import sqlite3
import os

# Define DB paths
DB_PATH_USERS = os.path.join(os.path.dirname(__file__), "../users.db")
DB_PATH_EVENTS = os.path.join(os.path.dirname(__file__), "../events.db")

def get_db_connection(db_path):
    """Get a SQLite connection."""
    return sqlite3.connect(db_path)

def init_users_db():
    """Initialize users.db if not exists."""
    conn = get_db_connection(DB_PATH_USERS)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def init_events_db():
    """Initialize events.db if not exists."""
    conn = get_db_connection(DB_PATH_EVENTS)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            camera_id INTEGER,
            label TEXT,
            confidence REAL,
            timestamp REAL
        )
    """)
    conn.commit()
    conn.close()