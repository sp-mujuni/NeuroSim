from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable

def export_memories_to_pdf(memories, filename="export.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("<para align='center'><b>Namulundu Hospital</b></para>", styles["Title"]))
    content.append(HRFlowable(width="100%", thickness=1, color="black"))
    content.append(Spacer(1, 0.2 * inch))

    for memory in memories:        
        content.append(Paragraph(f"<b>Book ID:</b> {memory.get('book_id')}", styles["Normal"]))
        content.append(Paragraph(f"<b>Book Contact:</b> {memory.get('book_contact')}", styles["Normal"]))
        content.append(Paragraph(f"<b>Name:</b> {memory.get('name')}", styles["Normal"]))
        content.append(Paragraph(f"<b>Condition:</b> {memory.get('condition')}", styles["Normal"]))
        content.append(Paragraph(f"<b>Content:</b><br/>{memory.get('content').replace('\n', '<br/>')}", styles["Normal"]))
        content.append(Paragraph(f"<b>Book Balance:</b> {memory.get('book_balance', 0.0):.2f}", styles["Normal"]))
        content.append(Paragraph(f"<b>Timestamp:</b> {memory.get('timestamp')}", styles["Normal"]))
        content.append(Spacer(1, 0.5 * inch))

    doc.build(content)
