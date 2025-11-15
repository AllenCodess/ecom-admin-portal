Example Requests

Add an item:

curl -X POST http://127.0.0.1:5000/items \
-H "Content-Type: application/json" \
-d '{"name":"Apple","price":1.5,"stock":10,"barcode":"1234567890"}'


List items:

curl http://127.0.0.1:5000/items


Update an item:

curl -X PATCH http://127.0.0.1:5000/items/1 \
-H "Content-Type: application/json" \
-d '{"price":2.0}'


Delete an item:

curl -X DELETE http://127.0.0.1:5000/items/1

Using the CLI (cli.py)

Run the CLI help to see commands:

python cli.py --help

CLI Commands
Command	Action
list	Show all inventory items
add <name> <price> [--barcode]	Add a new item
update <id> [--name] [--price]	Update an existing item
delete <id>	Delete an item by ID
show <id>	Show a single item
CLI Examples
# Add items
python cli.py add "Banana" 0.99 --barcode 1234567890123

# List all items
python cli.py list

# Update an item
python cli.py update 1 --price 1.25

# Delete an item
python cli.py delete 1

# Show single item
python cli.py show 1
