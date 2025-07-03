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
        self.root.configure(bg="#d0e7ff")
        self.root.title("NeuroSim Patient Memory System")

        # Fullscreen window
        self.root.state('zoomed')

        self.tabs = tk.Frame(self.root, bg="#a0c4ff", bd=2, relief="ridge")
        self.tabs.pack(side="top", fill="x")

        btn_style = {"bg": "#1e56a0", "fg": "white", "font": ("Arial", 10, "bold"), "bd": 0, "highlightthickness": 0, "padx": 15, "pady": 8}

        self.entry_button = tk.Button(self.tabs, text="Enter Patient", **btn_style, command=self.build_entry_form)
        self.entry_button.pack(side="left", padx=10, pady=10)

        self.search_button = tk.Button(self.tabs, text="Search Patient", **btn_style, command=self.build_search_form)
        self.search_button.pack(side="left", padx=10, pady=10)

        self.print_all_button = tk.Button(self.tabs, text="Print All Records", **btn_style, command=self.print_all_records)
        self.print_all_button.pack(side="left", padx=10, pady=10)

        self.backup_button = tk.Button(self.tabs, text="Backup Data", **btn_style, command=self.run_backup)
        self.backup_button.pack(side="left", padx=10, pady=10)

        self.csv_export_button = tk.Button(self.tabs, text="Export Data as CSV", **btn_style, command=self.export_all_records_csv)
        self.csv_export_button.pack(side="left", padx=10, pady=10)

        self.form_frame = tk.Frame(self.root, bg="#eff7ff")
        self.form_frame.pack(fill="both", expand=True, padx=60, pady=30)

        self.last_search_result = None

        self.build_entry_form()

    def clear_form(self):
        for widget in self.form_frame.winfo_children():
            widget.destroy()

    def create_label(self, text, row):
        label = tk.Label(self.form_frame, text=text, bg="#eff7ff", fg="#003366", font=("Verdana", 11, "bold"))
        label.grid(row=row, column=0, sticky="e", pady=10, padx=(20, 30))

    def create_entry(self, row):
        entry = tk.Entry(self.form_frame, width=50, font=("Verdana", 10), highlightbackground="#b3d7ff", highlightthickness=1, relief="flat")
        entry.grid(row=row, column=1, pady=10, ipady=6, ipadx=5)
        return entry

    def create_text(self, row, height):
        text_widget = tk.Text(self.form_frame, height=height, width=50, font=("Verdana", 10), highlightbackground="#b3d7ff", highlightthickness=1, relief="flat")
        text_widget.grid(row=row, column=1, pady=10)
        return text_widget

    def build_entry_form(self):
        self.clear_form()

        self.create_label("Book Number:", 0)
        self.book_entry = self.create_entry(0)

        self.create_label("Patient Name:", 1)
        self.name_entry = self.create_entry(1)

        self.create_label("Condition:", 2)
        self.condition_entry = self.create_entry(2)

        self.create_label("Notes:", 3)
        self.notes_entry = self.create_text(3, 4)

        self.create_label("Prescription:", 4)
        self.prescription_entry = self.create_text(4, 3)

        self.create_label("Consultation Fee:", 5)
        self.fee_entry = self.create_entry(5)

        save_btn = tk.Button(self.form_frame, text="Save Patient Record", bg="#0d3b66", fg="white", font=("Verdana", 10, "bold"), padx=20, pady=10, bd=0, highlightthickness=0, command=self.save_patient_record)
        save_btn.grid(row=6, column=1, pady=30, sticky="e")

    def build_search_form(self):
        self.clear_form()

        self.create_label("Search by Name or Book Number:", 0)
        self.query_entry = self.create_entry(0)

        search_btn = tk.Button(self.form_frame, text="Search", bg="#0077b6", fg="white", font=("Verdana", 10, "bold"), bd=0, padx=20, pady=10, highlightthickness=0, command=self.exact_search)
        search_btn.grid(row=1, column=1, sticky="e", pady=5)

        print_btn = tk.Button(self.form_frame, text="Print Result", bg="#0077b6", fg="white", font=("Verdana", 10, "bold"), bd=0, padx=20, pady=10, highlightthickness=0, command=self.print_last_search_result)
        print_btn.grid(row=1, column=0, sticky="e", pady=5)

        self.result_text = tk.Text(self.form_frame, height=25, width=100, bg="#f7fbff", font=("Courier New", 10), relief="flat")
        self.result_text.grid(row=2, column=0, columnspan=2, pady=15)

        export_frame = tk.Frame(self.form_frame, bg="#eff7ff")
        export_frame.grid(row=1, column=1, pady=20, sticky="e")

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
