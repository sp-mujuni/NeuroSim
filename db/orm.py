import sqlite3

DB_PATH = "neurosim_memory.db"

# Ensure database and table setup, including book_balance column
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Create table if it doesn't exist (with book_balance column)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                id TEXT PRIMARY KEY,
                timestamp REAL,
                book_id TEXT,
                name TEXT,
                condition TEXT,
                content TEXT,
                strength REAL,
                context_tags TEXT,
                book_balance REAL
            )
        ''')
        # Add book_balance column if it doesn't exist
        cursor.execute("PRAGMA table_info(memory)")
        columns = [col[1] for col in cursor.fetchall()]
        if "book_balance" not in columns:
            cursor.execute("ALTER TABLE memory ADD COLUMN book_balance REAL")
        conn.commit()

init_db()

def save_memory_entry(memory):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO memory (
                id, timestamp, book_id, name, condition, content, strength, context_tags, book_balance
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            memory["id"],
            memory["timestamp"],
            memory["book_id"],
            memory["name"],
            memory["condition"],
            memory["content"],
            memory["strength"],
            ",".join(memory.get("context_tags", [])),
            memory.get("book_balance")
        ))
        conn.commit()

def load_all_memories():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, timestamp, book_id, name, condition, content, strength, context_tags, book_balance
            FROM memory
        ''')
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "timestamp": row[1],
                "book_id": row[2],
                "name": row[3],
                "condition": row[4],
                "content": row[5],
                "strength": row[6],
                "context_tags": row[7].split(",") if row[7] else [],
                "book_balance": row[8]
            }
            for row in rows
        ]

def update_memory_entry(memory):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE memory SET
                timestamp = ?,
                book_id = ?,
                name = ?,
                condition = ?,
                content = ?,
                strength = ?,
                context_tags = ?,
                book_balance = ?
            WHERE id = ?
        ''', (
            memory["timestamp"],
            memory["book_id"],
            memory["name"],
            memory["condition"],
            memory["content"],
            memory["strength"],
            ",".join(memory.get("context_tags", [])),
            memory.get("book_balance"),
            memory["id"]
        ))
        conn.commit()

def get_memory_by_id(memory_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM memory WHERE id = ?", (memory_id,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "timestamp": row[1],
                "book_id": row[2],
                "name": row[3],
                "condition": row[4],
                "content": row[5],
                "strength": row[6],
                "context_tags": row[7].split(",") if row[7] else [],
                "book_balance": row[8]
            }
        return None

def get_latest_book_balance(book_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT book_balance FROM memory WHERE book_id = ? ORDER BY timestamp DESC LIMIT 1", (book_id,))
        row = cursor.fetchone()
        if row and row[0] is not None:
            return row[0]
        return 0.0
