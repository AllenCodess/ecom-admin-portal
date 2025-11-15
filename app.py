# app.py
from flask import Flask, request, jsonify
from inventory import (
    list_items,
    add_item,
    get_item,
    update_item,
    delete_item
)
from external_api import enrich_inventory_item

app = Flask(__name__)


@app.get("/items")
def get_items():
    return jsonify(list_items()), 200


@app.get("/items/<int:item_id>")
def get_single_item(item_id):
    item = get_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


@app.post("/items")
def create_item():
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    enriched = enrich_inventory_item(data)
    saved = add_item(enriched)

    return jsonify(saved), 201


@app.patch("/items/<int:item_id>")
def patch_item(item_id):
    updates = request.json
    item = update_item(item_id, updates)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    return jsonify(item), 200


@app.delete("/items/<int:item_id>")
def remove_item(item_id):
    if not delete_item(item_id):
        return jsonify({"error": "Item not found"}), 404

    return jsonify({"message": "Deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
