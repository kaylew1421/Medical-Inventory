import sqlite3

DB_FILE = "back-end/db/hospital.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE inventory ADD COLUMN confirmed_by TEXT DEFAULT '';")
    print("Column 'confirmed_by' added successfully.")
except sqlite3.OperationalError as e:
    print("Error:", e)

conn.commit()
conn.close()
