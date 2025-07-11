from flask import Flask, jsonify, render_template, request
import sqlite3
import os

app = Flask(__name__)

# 📄 Resolve database file path relative to this file
DB_FILE = os.path.join(os.path.dirname(__file__), 'db', 'hospital.db')
print(f"✅ Using database at: {DB_FILE}")

# GET inventory list
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/inventory")
def get_inventory():
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory")
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()

        for item in rows:
            # Flag items that are low stock
            item['low_stock'] = item['quantity'] <= item['reorder_threshold']
            # Ensure confirmed_by exists even if null
            item['confirmed_by'] = item.get('confirmed_by') or ""

        return jsonify(rows)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# POST update inventory
@app.route("/api/inventory/update", methods=["POST"])
def update_inventory():
    updates = request.json
    if not updates:
        return {"status": "fail", "message": "No data provided"}, 400

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        for item in updates:
            cursor.execute("""
                UPDATE inventory
                SET quantity = ?, confirmed_by = ?
                WHERE sku = ?
            """, (item["quantity"], item.get("confirmed_by", ""), item["sku"]))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Inventory updated successfully"}

    except Exception as e:
        return {"status": "error", "message": str(e)}, 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
