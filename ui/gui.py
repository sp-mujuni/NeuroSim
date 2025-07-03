import tkinter as tk
from tkinter import messagebox
import uuid
import time
from utils.export_utils import export_memories_to_csv

class NeuroSimGUI:
    def __init__(self, root, memory_engine, similarity_scorer, reinforcement_engine):
        self.memory_engine = memory_engine
        self.similarity_scorer = similarity_scorer
        self.reinforcement_engine = reinforcement_engine

        self.root = root

        # Create notebook-like sections
        self.tabs = tk.Frame(self.root)
        self.tabs.pack(side="top", fill="x")

        self.entry_button = tk.Button(self.tabs, text="Enter Patient", command=self.build_entry_form)
        self.entry_button.pack(side="left")

        self.search_button = tk.Button(self.tabs, text="Search Patient", command=self.build_search_form)
        self.search_button.pack(side="left")

        self.form_frame = tk.Frame(self.root)
        self.form_frame.pack(fill="both", expand=True)

        self.build_entry_form()

    def clear_form(self):
        for widget in self.form_frame.winfo_children():
            widget.destroy()

    def build_entry_form(self):
        self.clear_form()

        tk.Label(self.form_frame, text="Enter Patient Details").grid(row=0, column=1)
        tk.Label(self.form_frame, text="Book Number:").grid(row=1, column=0)
        tk.Label(self.form_frame, text="Patient Name:").grid(row=2, column=0)
        tk.Label(self.form_frame, text="Condition:").grid(row=3, column=0)
        tk.Label(self.form_frame, text="Notes:").grid(row=4, column=0)

        self.book_entry = tk.Entry(self.form_frame)
        self.name_entry = tk.Entry(self.form_frame)
        self.condition_entry = tk.Entry(self.form_frame)
        self.notes_entry = tk.Text(self.form_frame, height=5, width=30)

        self.book_entry.grid(row=1, column=1)
        self.name_entry.grid(row=2, column=1)
        self.condition_entry.grid(row=3, column=1)
        self.notes_entry.grid(row=4, column=1)

        tk.Button(self.form_frame, text="Save Patient Record", command=self.save_patient_record).grid(row=5, column=1)

    def save_patient_record(self):
        book_id = self.book_entry.get().strip()
        name = self.name_entry.get().strip()
        condition = self.condition_entry.get().strip()
        notes = self.notes_entry.get("1.0", tk.END).strip()

        if not book_id or not name:
            messagebox.showerror("Input Error", "Book number and name are required.")
            return

        memory = {
            "id": str(uuid.uuid4()),
            "timestamp": time.time(),
            "book_id": book_id,
            "name": name,
            "condition": condition,
            "content": notes,
            "strength": 1.0,
            "context_tags": [condition.lower() if condition else "general"]
        }

        self.memory_engine.save_memory(memory)
        messagebox.showinfo("Success", "Patient record saved.")
        self.book_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.condition_entry.delete(0, tk.END)
        self.notes_entry.delete("1.0", tk.END)

    def build_search_form(self):
        self.clear_form()

        tk.Label(self.form_frame, text="Search Patient by Book Number or Name").grid(row=0, column=1)
        tk.Label(self.form_frame, text="Query:").grid(row=1, column=0)

        self.query_entry = tk.Entry(self.form_frame)
        self.query_entry.grid(row=1, column=1)
        tk.Button(self.form_frame, text="Search", command=self.search_patient).grid(row=2, column=1)

        self.result_text = tk.Text(self.form_frame, height=10, width=60)
        self.result_text.grid(row=3, column=0, columnspan=2)

        tk.Button(self.form_frame, text="Export All Records", command=self.export_all_records).grid(row=4, column=1)

    def search_patient(self):
        query = self.query_entry.get().strip()
        if not query:
            messagebox.showerror("Input Error", "Please enter a search term.")
            return

        results = self.similarity_scorer.score(query, self.memory_engine.get_memories())
        self.result_text.delete("1.0", tk.END)
        if not results:
            self.result_text.insert(tk.END, "No matching records found.")
            return

        for res in results:
            memory = self.memory_engine.get_memory_by_id(res["id"])
            self.reinforcement_engine.reinforce(memory)
            self.memory_engine.update_memory(memory)
            self.result_text.insert(tk.END, f"Book #: {memory['book_id']}\n")
            self.result_text.insert(tk.END, f"Name: {memory['name']}\n")
            self.result_text.insert(tk.END, f"Condition: {memory['condition']}\n")
            self.result_text.insert(tk.END, f"Notes: {memory['content']}\n")
            self.result_text.insert(tk.END, f"Strength: {memory['strength']:.2f}\n")
            self.result_text.insert(tk.END, f"---\n")

    def export_all_records(self):
        memories = self.memory_engine.get_memories()
        export_memories_to_csv(memories)
