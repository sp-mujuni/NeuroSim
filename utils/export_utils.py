import csv
from tkinter import filedialog

def export_memories_to_csv(memories):
    if not memories:
        print("No memories to export.")
        return

    filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not filepath:
        return

    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "book_id", "name", "condition", "content", "strength", "timestamp", "context_tags"
        ])
        writer.writeheader()
        for mem in memories:
            writer.writerow({
                "book_id": mem["book_id"],
                "name": mem["name"],
                "condition": mem["condition"],
                "content": mem["content"],
                "strength": mem["strength"],
                "timestamp": mem["timestamp"],
                "context_tags": ", ".join(mem["context_tags"])
            })

    print(f"Patient records exported to {filepath}")
