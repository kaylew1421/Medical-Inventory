import sqlite3
import csv
import os

DB_FILE = "hospital.db"
CSV_FILE = "icu_inventory_mock.csv"

# Define your table creation SQL
create_table_sql = """
CREATE TABLE IF NOT EXISTS inventory (
    sku TEXT PRIMARY KEY,
    item_name TEXT NOT NULL,
    item_type TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    reorder_threshold INTEGER NOT NULL,
    expiration_date TEXT
);
"""

# Connect to database
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create the inventory table
cursor.execute(create_table_sql)
conn.commit()

# Read and insert CSV data
with open(CSV_FILE, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    rows_inserted = 0
    for row in reader:
        cursor.execute("""
            INSERT OR REPLACE INTO inventory (sku, item_name, item_type, quantity, reorder_threshold, expiration_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row['SKU'],
            row['Item Name'],
            row['Item Type'],
            int(row['Quantity']),
            int(row['Reorder Threshold']),
            row['Expiration Date'] if row['Expiration Date'] else None
        ))
        rows_inserted += 1

conn.commit()
conn.close()

print(f"✅ Imported {rows_inserted} rows from {CSV_FILE} into {DB_FILE}")
