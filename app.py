# app.py

from flask import Flask, render_template, request, redirect, url_for, send_file
from engine.memory_engine import MemoryEngine
from engine.similarity import SimilarityScorer
from engine.reinforcement import ReinforcementEngine
import uuid
import time
from datetime import datetime
import os

app = Flask(__name__)

memory_engine = MemoryEngine()
similarity_scorer = SimilarityScorer()
reinforcement_engine = ReinforcementEngine()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_patient():
    data = request.form
    book_id = data.get("book_id")
    name = data.get("name")
    condition = data.get("condition")
    notes = data.get("notes")
    prescription = data.get("prescription")
    consultation_fee = data.get("consultation_fee")
    book_balance_final = 0.0
    try:
        consultation_fee_value = float(consultation_fee.replace(',', '')) if consultation_fee else 0.0
    except ValueError:
        consultation_fee_value = 0.0
    # Retrieve the most recent (newest) total balance for this book_id, if any
    previous_balance = memory_engine.get_latest_book_balance(book_id)
    book_balance_final = round(consultation_fee_value + (previous_balance or 0.0), 0)
    # Format values with commas for display
    consultation_fee_value_formatted = "{:,.0f}".format(consultation_fee_value)
    book_balance_final_formatted = "{:,.0f}".format(book_balance_final)

    if not book_id or not name:
        return "Missing book number or name", 400

    timestamp = time.time()
    record_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    memory = {
        "id": str(uuid.uuid4()),
        "timestamp": timestamp,
        "book_id": book_id,
        "name": name,
        "condition": condition,
        "book_balance": book_balance_final,
        "content": f"Notes: {notes}\nPrescription: {prescription}\nConsultation Fee: UGX {consultation_fee_value_formatted}\nDate Added: {record_date}\nBook Balance: UGX {book_balance_final_formatted}",
        "strength": 1.0,
        "context_tags": [condition.lower() if condition else "general"]
    }

    memory_engine.save_memory(memory)
    return redirect(url_for("index"))

@app.route("/search", methods=["GET"])
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

if __name__ == '__main__':
    app.run(debug=True)
 