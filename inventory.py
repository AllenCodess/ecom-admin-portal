# inventory.py
from typing import Dict, List, Optional

_inventory: List[Dict] = []
_next_id = 1


def list_items() -> List[Dict]:
    return _inventory.copy()


def get_item(item_id: int) -> Optional[Dict]:
    for item in _inventory:
        if item["id"] == item_id:
            return item
    return None


def add_item(item: Dict) -> Dict:
    global _next_id
    item_copy = item.copy()
    item_copy.setdefault("id", _next_id)
    _next_id += 1
    _inventory.append(item_copy)
    return item_copy


def update_item(item_id: int, updates: Dict) -> Optional[Dict]:
    item = get_item(item_id)
    if not item:
        return None
    item.update(updates)
    return item


def delete_item(item_id: int) -> bool:
    global _inventory
    for i, item in enumerate(_inventory):
        if item["id"] == item_id:
            _inventory.pop(i)
            return True
    return False


def clear_store():
    # helper for tests
    global _inventory, _next_id
    _inventory = []
    _next_id = 1
