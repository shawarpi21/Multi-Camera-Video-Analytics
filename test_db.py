import sqlite3

# Connect to the database (replace 'example.db' with your actual DB file if needed)
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Create a 'users' table (as before)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
''')

# Example: Create a 'cameras' table for your video analytics project
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cameras (
        id INTEGER PRIMARY KEY,
        location TEXT NOT NULL,
        status TEXT DEFAULT 'active'
    )
''')

# Insert sample data (only if tables are empty, to avoid duplicates)
cursor.execute("INSERT OR IGNORE INTO users (name) VALUES ('Alice')")
cursor.execute("INSERT OR IGNORE INTO cameras (location) VALUES ('Entrance')")

# Commit changes
conn.commit()

# Query and print results
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables in DB:", tables)  # Shows all tables, e.g., [('users',), ('cameras',)]

cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
print("Users:", users)

cursor.execute("SELECT * FROM cameras")
cameras = cursor.fetchall()
print("Cameras:", cameras)

# Close connection
conn.close()