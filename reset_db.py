import sqlite3

# Replace 'users.db' with the exact file from backend/database.py
conn = sqlite3.connect('users.db')
cur = conn.cursor()

# Copy the table creation from your init_users_db() function (from database.py)
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
""")
conn.commit()
conn.close()
print("Database reset and initialized successfully.")