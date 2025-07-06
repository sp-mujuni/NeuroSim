from flask import Flask, render_template, request, redirect, url_for, send_file, session
from engine.memory_engine import MemoryEngine
from engine.similarity import SimilarityScorer
from engine.reinforcement import ReinforcementEngine
from utils.csv_export import export_memories_to_csv
from utils.pdf_export import export_memories_to_pdf
from auth import auth_bp
import uuid
import time
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Replace with a secure key in production

app.register_blueprint(auth_bp)

memory_engine = MemoryEngine()
similarity_scorer = SimilarityScorer()
reinforcement_engine = ReinforcementEngine()

# Decorator to require login
def login_required(view_func):
    def wrapped_view(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("auth.login"))
        return view_func(*args, **kwargs)
    wrapped_view.__name__ = view_func.__name__
    return wrapped_view

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/patients")
@login_required
def patients():
    return render_template("patients.html")

@app.route("/books")
@login_required
def books():
    query = request.args.get("query", "").strip().lower()
    all_records = memory_engine.get_memories()
    unique_books = {}

    for rec in all_records:
        key = rec['book_id'].lower()
        if query and query not in key:
            continue
        if key not in unique_books or rec['timestamp'] > unique_books[key]['timestamp']:
            unique_books[key] = rec

    return render_template("books.html", books=unique_books.values())

@app.route("/bill/<book_id>", methods=["GET", "POST"])
@login_required
def edit_bill(book_id):
    records = [m for m in memory_engine.get_memories() if m['book_id'] == book_id]
    if not records:
        return "Book not found", 404

    latest = sorted(records, key=lambda x: x['timestamp'], reverse=True)[0]

    if request.method == "POST":
        new_fee = request.form.get("bill")

        # Update only the book_balance field
        try:
            latest['book_balance'] = float(new_fee.replace(',', '')) if new_fee else 0.0
        except ValueError:
            latest['book_balance'] = 0.0

        memory_engine.update_memory(latest)
        return redirect(url_for("books"))

    return render_template("edit_bill.html", book=latest)


@app.route("/add", methods=["POST"])
@login_required
def add_patient():
    data = request.form
    book_id = data.get("book_id")
    book_contact = data.get("book_contact")
    name = data.get("name")
    condition = data.get("condition")
    notes = data.get("notes")
    prescription = data.get("prescription")
    consultation_fee = data.get("consultation_fee")
    doctor = data.get("doctor")
    doctor_contact = data.get("doctor_contact")
    book_balance_final = 0.0
    try:
        consultation_fee_value = float(consultation_fee.replace(',', '')) if consultation_fee else 0.0
    except ValueError:
        consultation_fee_value = 0.0
    # Retrieve the most recent (newest) total balance for this book_id, if any
    previous_balance = memory_engine.get_latest_book_balance(book_id)
    book_balance_final = consultation_fee_value + (previous_balance or 0.0)
    # Format values with commas for display
    consultation_fee_value_formatted = "{:,.0f}".format(consultation_fee_value)
    book_balance_final_formatted = "{:,.0f}".format(book_balance_final)

    if not book_id or not name:
        return "Missing book number or name", 400

    timestamp = time.time()
    record_date = datetime.fromtimestamp(timestamp)
    formatted_date = record_date.strftime('%Y-%m-%d %H:%M:%S')


    memory = {
        "id": str(uuid.uuid4()),
        "timestamp": record_date,
        "book_id": book_id,
        "book_contact": book_contact,
        "name": name,
        "condition": condition,
        "book_balance": book_balance_final,
        "content": f"Notes: {notes}\nPrescription: {prescription}\nConsultation Fee: UGX {consultation_fee_value_formatted}\nDoctor: {doctor}\nDoctor's Contact: {doctor_contact}\nDate Added: {formatted_date}",
    }

    memory_engine.save_memory(memory)
    return redirect(url_for("patients"))

@app.route("/search", methods=["GET"])
@login_required
def search():
    query = request.args.get("query", "")
    query_str = str(query).lower()
    results = []
    for mem in memory_engine.get_memories():
        book_id_str = str(mem.get('book_id', '')).lower()
        name_str = str(mem.get('name', '')).lower()
        if query_str == book_id_str or query_str == name_str:
            reinforcement_engine.reinforce(mem)
            memory_engine.update_memory(mem)
            results.append(mem)
    return render_template("search.html", results=results, query=query)

@app.route("/export/all/csv")
@login_required
def export_all_csv():
    memories = memory_engine.get_memories()
    export_memories_to_csv(memories, "namulundu_all_records.csv")
    return send_file("namulundu_all_records.csv", as_attachment=True)

@app.route("/export/all/pdf")
@login_required
def export_all_pdf():
    memories = memory_engine.get_memories()
    export_memories_to_pdf(memories, "namulundu_all_records.pdf")
    return send_file("namulundu_all_records.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
 