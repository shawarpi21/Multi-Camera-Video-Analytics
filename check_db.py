import sqlite3
conn = sqlite3.connect("events.db")
cur = conn.cursor()
cur.execute("DELETE FROM events")
conn.commit()
conn.close()
print("Old images removed")





