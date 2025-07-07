from flask import Flask, jsonify, render_template, request
import sqlite3

app = Flask(__name__)
DB_FILE = "back-end/db/hospital.db"

# GET inventory list
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/inventory")
def get_inventory():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()

    for item in rows:
        item['low_stock'] = item['quantity'] <= item['reorder_threshold']
        # Ensure confirmed_by exists even if null
        item['confirmed_by'] = item.get('confirmed_by') or ""

    return jsonify(rows)

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
    app.run(debug=True)
