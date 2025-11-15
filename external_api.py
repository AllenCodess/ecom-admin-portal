# external_api.py
import requests
from typing import Optional, Dict


BASE_URL = "https://world.openfoodfacts.org"


def fetch_by_barcode(barcode: str) -> Optional[Dict]:
    """Fetch product by barcode (product code) from OpenFoodFacts.
    Returns parsed product dict or None on failure/not found.
    """
    try:
        resp = requests.get(f"{BASE_URL}/api/v0/product/{barcode}.json", timeout=5)
        resp.raise_for_status()
        data = resp.json()

        if data.get("status") == 1:
            return data.get("product")
        return None

    except requests.RequestException:
        return None


def search_product(name: str) -> Optional[Dict]:
    """Search products by name and return top hit (or None).
    Uses the search endpoint.
    """
    try:
        params = {
            "search_terms": name,
            "search_simple": 1,
            "action": "process",
            "page_size": 1
        }
        resp = requests.get(f"{BASE_URL}/cgi/search.pl", params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()

        products = data.get("products") or []
        return products[0] if products else None

    except requests.RequestException:
        return None


def enrich_inventory_item(item: Dict) -> Dict:
    """Attempt to enrich a local inventory item using barcode or name.
    Returns a new dict with enrichment fields merged (without overwriting
    local price/stock unless absent).
    """
    enriched = item.copy()
    product = None

    barcode = item.get("barcode")
    name = item.get("name")

    if barcode:
        product = fetch_by_barcode(str(barcode))

    if not product and name:
        product = search_product(name)

    if product:
        # Add fields without overwriting local values
        enriched.setdefault("product_name", product.get("product_name"))
        enriched.setdefault("brands", product.get("brands"))
        enriched.setdefault("nutriments", product.get("nutriments"))
        enriched.setdefault("image_url", product.get("image_small_url") or product.get("image_url"))

    return enriched
