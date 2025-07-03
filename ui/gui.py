# ui/gui.py

import tkinter as tk
from tkinter import messagebox
import uuid
import time
from datetime import datetime
from utils.export_utils import export_memories_to_csv
from utils.pdf_export import export_memories_to_pdf
from utils.backup_utils import backup_database

class NeuroSimGUI:
    def __init__(self, root, memory_engine, similarity_scorer, reinforcement_engine):
        self.memory_engine = memory_engine
        self.similarity_scorer = similarity_scorer
        self.reinforcement_engine = reinforcement_engine

        self.root = root

        self.tabs = tk.Frame(self.root)
        self.tabs.pack(side="top", fill="x")

        self.entry_button = tk.Button(self.tabs, text="Enter Patient", command=self.build_entry_form)
        self.entry_button.pack(side="left")

        self.search_button = tk.Button(self.tabs, text="Search Patient", command=self.build_search_form)
        self.search_button.pack(side="left")

        self.print_all_button = tk.Button(self.tabs, text="Print All Records", command=self.print_all_records)
        self.print_all_button.pack(side="left")

        self.export_all_button = tk.Button(self.tabs, text="Export as CSV", command=self.export_all_records_csv)
        self.export_all_button.pack(side="left")

        self.backup_button = tk.Button(self.tabs, text="Backup DB", command=self.run_backup)
        self.backup_button.pack(side="left")

        self.form_frame = tk.Frame(self.root)
        self.form_frame.pack(fill="both", expand=True)

        self.last_search_result = None

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
        tk.Label(self.form_frame, text="Prescription:").grid(row=5, column=0)
        tk.Label(self.form_frame, text="Consultation Fee:").grid(row=6, column=0)

        self.book_entry = tk.Entry(self.form_frame)
        self.name_entry = tk.Entry(self.form_frame)
        self.condition_entry = tk.Entry(self.form_frame)
        self.notes_entry = tk.Text(self.form_frame, height=4, width=30)
        self.prescription_entry = tk.Text(self.form_frame, height=3, width=30)
        self.fee_entry = tk.Entry(self.form_frame)

        self.book_entry.grid(row=1, column=1)
        self.name_entry.grid(row=2, column=1)
        self.condition_entry.grid(row=3, column=1)
        self.notes_entry.grid(row=4, column=1)
        self.prescription_entry.grid(row=5, column=1)
        self.fee_entry.grid(row=6, column=1)

        tk.Button(self.form_frame, text="Save Patient Record", command=self.save_patient_record).grid(row=7, column=1)

    def save_patient_record(self):
        book_id = self.book_entry.get().strip()
        name = self.name_entry.get().strip()
        condition = self.condition_entry.get().strip()
        notes = self.notes_entry.get("1.0", tk.END).strip()
        prescription = self.prescription_entry.get("1.0", tk.END).strip()
        fee = self.fee_entry.get().strip()

        if not book_id or not name:
            messagebox.showerror("Input Error", "Book number and name are required.")
            return

        timestamp = time.time()
        record_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        memory = {
            "id": str(uuid.uuid4()),
            "timestamp": timestamp,
            "book_id": book_id,
            "name": name,
            "condition": condition,
            "content": f"Notes: {notes}\nPrescription: {prescription}\nConsultation Fee: {fee}\nDate Added: {record_date}",
            "strength": 1.0,
            "context_tags": [condition.lower() if condition else "general"]
        }

        self.memory_engine.save_memory(memory)
        messagebox.showinfo("Success", "Patient record saved.")
        self.book_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.condition_entry.delete(0, tk.END)
        self.notes_entry.delete("1.0", tk.END)
        self.prescription_entry.delete("1.0", tk.END)
        self.fee_entry.delete(0, tk.END)

    def build_search_form(self):
        self.clear_form()

        tk.Label(self.form_frame, text="Search Patient by Name or Book Number").grid(row=0, column=1)
        tk.Label(self.form_frame, text="Query:").grid(row=1, column=0)

        self.query_entry = tk.Entry(self.form_frame)
        self.query_entry.grid(row=1, column=1)

        tk.Button(self.form_frame, text="Search", command=self.exact_search).grid(row=2, column=1)

        self.result_text = tk.Text(self.form_frame, height=14, width=60)
        self.result_text.grid(row=3, column=0, columnspan=2)

        export_frame = tk.Frame(self.form_frame)
        export_frame.grid(row=4, column=1)
        tk.Button(export_frame, text="Print Result", command=self.print_last_search_result).pack(side="left")

    def exact_search(self):
        query = self.query_entry.get().strip().lower()
        memories = self.memory_engine.get_memories()

        match = None
        for mem in memories:
            if query == mem['book_id'].lower() or query == mem['name'].lower():
                match = mem
                break

        self.result_text.delete("1.0", tk.END)
        if not match:
            self.result_text.insert(tk.END, "No matching record found.")
            self.last_search_result = None
            return

        self.reinforcement_engine.reinforce(match)
        self.memory_engine.update_memory(match)
        self.result_text.insert(tk.END, f"Book #: {match['book_id']}\n")
        self.result_text.insert(tk.END, f"Name: {match['name']}\n")
        self.result_text.insert(tk.END, f"Condition: {match['condition']}\n")
        self.result_text.insert(tk.END, f"{match['content']}\n")
        # self.result_text.insert(tk.END, f"Strength: {match['strength']:.2f}\n")

        self.last_search_result = [match]

    def export_all_records_csv(self):
        memories = self.memory_engine.get_memories()
        export_memories_to_csv(memories)

    def export_all_records_pdf(self):
        memories = self.memory_engine.get_memories()
        export_memories_to_pdf(memories)

    def print_last_search_result(self):
        if self.last_search_result:
            export_memories_to_pdf(self.last_search_result)
            messagebox.showinfo("Print", "Search result saved as PDF.")
        else:
            messagebox.showwarning("Print", "No search result to print.")

    def print_all_records(self):
        memories = self.memory_engine.get_memories()
        if not memories:
            messagebox.showinfo("Print", "No records to print.")
            return
        export_memories_to_pdf(memories)
        messagebox.showinfo("Print", "All patient records saved as PDF.")

    def run_backup(self):
        backup_database()
        messagebox.showinfo("Backup Complete", "Database backup completed successfully.")
