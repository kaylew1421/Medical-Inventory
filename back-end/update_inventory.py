import sqlite3

db_path = 'back-end/db/hospital.db'  # Adjust if your path differs

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1) Inspect columns in 'inventory'
print("Inventory table columns:")
cursor.execute("PRAGMA table_info(inventory);")
columns = cursor.fetchall()
for col in columns:
    print(col)

# 2) Update missing reorder_threshold and expiration_date
update_query = """
UPDATE inventory
SET 
  reorder_threshold = COALESCE(reorder_threshold, 10),
  expiration_date = COALESCE(expiration_date, date('now', '+6 months'))
WHERE reorder_threshold IS NULL OR expiration_date IS NULL;
"""
cursor.execute(update_query)
conn.commit()
print(f"Updated {cursor.rowcount} rows where reorder_threshold or expiration_date was NULL.")

conn.close()
