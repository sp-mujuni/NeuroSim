from fpdf import FPDF
from tkinter import filedialog
from datetime import datetime

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Namulundu Patient Records', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def add_memory(self, memory):
        self.set_font('Arial', '', 10)
        self.cell(0, 8, f"Book ID: {memory['book_id']}", ln=True)
        self.cell(0, 8, f"Name: {memory['name']}", ln=True)
        self.cell(0, 8, f"Condition: {memory['condition']}", ln=True)
        self.multi_cell(0, 8, f"Notes: {memory['content']}")
        self.cell(0, 8, f"Strength: {memory['strength']:.2f}", ln=True)
        timestamp = datetime.fromtimestamp(memory['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        self.cell(0, 8, f"Recorded: {timestamp}", ln=True)
        self.ln(5)

def export_memories_to_pdf(memories):
    if not memories:
        print("No data to export.")
        return

    filepath = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not filepath:
        return

    pdf = PDFReport()
    pdf.add_page()

    for memory in memories:
        pdf.add_memory(memory)

    pdf.output(filepath)
    print(f"PDF report saved to {filepath}")
