# cli.py
import click
from inventory import (
    list_items,
    add_item,
    update_item,
    delete_item,
    get_item,
)
from external_api import enrich_inventory_item


@click.group()
def cli():
    """Inventory CLI tool."""
    pass


@cli.command()
def list():
    """List all inventory items."""
    items = list_items()
    if not items:
        click.echo("Inventory is empty.")
        return

    for item in items:
        click.echo(item)


@cli.command()
@click.argument("name")
@click.argument("price", type=float)
@click.option("--barcode", required=False)
def add(name, price, barcode):
    """Add an item to inventory."""
    item = {"name": name, "price": price}

    if barcode:
        item["barcode"] = barcode

    enriched = enrich_inventory_item(item)
    saved = add_item(enriched)

    click.echo(f"Added item: {saved}")


@cli.command()
@click.argument("item_id", type=int)
@click.option("--name", required=False)
@click.option("--price", required=False, type=float)
def update(item_id, name, price):
    """Update an existing inventory item."""
    updates = {}
    if name:
        updates["name"] = name
    if price is not None:
        updates["price"] = price

    updated = update_item(item_id, updates)

    if updated:
        click.echo(f"Updated item: {updated}")
    else:
        click.echo("Item not found.")


@cli.command()
@click.argument("item_id", type=int)
def delete(item_id):
    """Delete an inventory item by ID."""
    if delete_item(item_id):
        click.echo("Item deleted.")
    else:
        click.echo("Item not found.")


@cli.command()
@click.argument("item_id", type=int)
def show(item_id):
    """Show a single item."""
    item = get_item(item_id)
    if item:
        click.echo(item)
    else:
        click.echo("Item not found.")


if __name__ == "__main__":
    cli()
