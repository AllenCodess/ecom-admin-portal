import json
import pytest
from app import app
from inventory import clear_store


@pytest.fixture
def client():
    clear_store()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_crud_lifecycle(client):
    # Create
    rv = client.post("/items", json={"name": "TestItem", "price": 9.99, "stock": 5})
    assert rv.status_code == 201
    created = rv.get_json()
    assert created["name"] == "TestItem"
    item_id = created["id"]

    # Read single
    rv = client.get(f"/items/{item_id}")
    assert rv.status_code == 200
    fetched = rv.get_json()
    assert fetched["id"] == item_id

    # Update
    rv = client.patch(f"/items/{item_id}", json={"price": 12.49})
    assert rv.status_code == 200
    updated = rv.get_json()
    assert updated["price"] == 12.49

    # Delete
    rv = client.delete(f"/items/{item_id}")
    assert rv.status_code == 200

    # Confirm deletion
    rv = client.get(f"/items/{item_id}")
    assert rv.status_code == 404
