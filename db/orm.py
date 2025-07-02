import sqlite3
import os

DB_PATH = "neurosim_memory.db"

# Ensure database and table setup
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                id TEXT PRIMARY KEY,
                timestamp REAL,
                content TEXT,
                type TEXT,
                strength REAL,
                context_tags TEXT
            )
        ''')
        conn.commit()

init_db()

def save_memory_entry(memory):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO memory (id, timestamp, content, type, strength, context_tags)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            memory["id"],
            memory["timestamp"],
            memory["content"],
            memory["type"],
            memory["strength"],
            ",".join(memory.get("context_tags", []))
        ))
        conn.commit()

def load_all_memories():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM memory")
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "timestamp": row[1],
                "content": row[2],
                "type": row[3],
                "strength": row[4],
                "context_tags": row[5].split(",")
            }
            for row in rows
        ]
