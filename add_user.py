import sqlite3
import os
from passlib.hash import bcrypt

# Paths from your database.py
DB_PATH_USERS = os.path.join(os.path.dirname(__file__), "../users.db")

def add_user(username, password):
    """Add a user to users.db with hashed password."""
    hashed_password = bcrypt.hash(password)
    conn = sqlite3.connect(DB_PATH_USERS)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print(f"User '{username}' added successfully.")
    except sqlite3.IntegrityError:
        print(f"User '{username}' already exists.")
    conn.close()

# Example: Add a default admin user
add_user("admin", "password")  # Change to your preferred credentials