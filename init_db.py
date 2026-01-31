import sqlite3

conn = sqlite3.connect('users.db')  # This creates or connects to 'users.db' (adjust if your app uses a different filename)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
)''')
conn.commit()
conn.close()
print("DB initialized")