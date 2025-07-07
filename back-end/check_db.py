import sqlite3

conn = sqlite3.connect('db/hospital.db')
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM inventory")
count = cursor.fetchone()[0]
print(f"\n✅ Inventory has {count} items.\n")

cursor.execute("SELECT sku, item_name, item_type, quantity FROM inventory")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
