import csv

def export_memories_to_csv(memories, filename="export.csv"):
    fieldnames = ["book_id", "book_contact", "name", "book_balance"]
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for memory in memories:
            writer.writerow({
                "book_id": memory.get("book_id"),
                "book_contact": memory.get("book_contact"),  # NEW FIELD
                "name": memory.get("name"),
                "book_balance": memory.get("book_balance", 0.0),
            })