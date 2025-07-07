import sqlite3
from email_utils import send_email

DB_FILE = 'db/hospital.db'  # Adjust path if needed

def send_alerts():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sku, item_name, quantity, reorder_threshold FROM inventory
        WHERE quantity <= reorder_threshold
    """)
    low_stock_items = cursor.fetchall()
    conn.close()

    if not low_stock_items:
        print("All good — no low stock items.")
        return

    # Compose email content
    subject = "Low Stock Alert - Neuro ICU Inventory"
    body = "Dear Unit Manager,\n\nThe following items are below their reorder thresholds:\n"
    for sku, name, qty, threshold in low_stock_items:
        body += f"- {name} (SKU: {sku}): Quantity {qty}, Threshold {threshold}\n"
    body += "\nPlease reorder ASAP.\nRegards,\nInventory Management System"

    # Replace with actual recipient emails
    recipients = ['kaylew1421@outlook.com']

    send_email(subject, body, recipients)
    print("Low stock alert email sent!")

if __name__ == "__main__":
    send_alerts()
