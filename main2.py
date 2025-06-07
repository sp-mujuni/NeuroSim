import sqlite3
import time
from datetime import datetime

# Constants
DATABASE_FILE = "memory.db"
MEMORY_TTL = 60  # Time-to-live for memory in seconds

# Database setup
def setup_database():
    """Initializes the database and memory table."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            timestamp REAL NOT NULL,
            last_accessed REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Memory functions
def store_memory(data):
    """Stores a new memory in the database."""
    timestamp = time.time()
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO memory (data, timestamp, last_accessed)
        VALUES (?, ?, ?)
    """, (data, timestamp, timestamp))
    conn.commit()
    conn.close()
    print(f"Memory stored: '{data}'")

def retrieve_memory(memory_id):
    """Retrieves a memory by ID."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM memory WHERE id = ?", (memory_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        if is_memory_expired(row):
            delete_memory(memory_id)
            print(f"Memory [ID {memory_id}] has decayed and is no longer accessible.")
        else:
            update_last_accessed(memory_id)
            print(f"Retrieved Memory [ID {row[0]}]: '{row[1]}' (Stored at {time.ctime(row[2])})")
    else:
        print("Memory ID not found.")

def list_all_memories():
    """Lists all memories in the database, excluding expired ones."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM memory")
    rows = cursor.fetchall()
    conn.close()

    print("\nCurrent Stored Memories:")
    for row in rows:
        if is_memory_expired(row):
            delete_memory(row[0])
        else:
            print(f"ID: {row[0]}, Data: '{row[1]}', Timestamp: {time.ctime(row[2])}")
    print()

def is_memory_expired(memory_row):
    """Checks if a memory has expired based on TTL."""
    last_accessed = memory_row[3]
    return time.time() - last_accessed > MEMORY_TTL

def update_last_accessed(memory_id):
    """Updates the last accessed timestamp for a memory."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE memory
        SET last_accessed = ?
        WHERE id = ?
    """, (time.time(), memory_id))
    conn.commit()
    conn.close()

def delete_memory(memory_id):
    """Deletes a memory from the database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM memory WHERE id = ?", (memory_id,))
    conn.commit()
    conn.close()

def search_memory(keyword):
    """Searches for memories containing a specific keyword."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM memory WHERE data LIKE ?", (f"%{keyword}%",))
    rows = cursor.fetchall()
    conn.close()

    print(f"\nSearching for memories with keyword: '{keyword}'")
    if rows:
        for row in rows:
            if is_memory_expired(row):
                delete_memory(row[0])
            else:
                print(f"Found Memory [ID {row[0]}]: '{row[1]}'")
    else:
        print("No matching memories found.")

# Example usage
if __name__ == "__main__":
    print("Digital Memory Simulation with SQLite Persistence\n")

    # Set up the database
    setup_database()

    # Store memories
    store_memory("Learned about memory function in the brain.")
    store_memory("Explored Python for simulating digital memory.")
    store_memory("Studied context-based retrieval and memory decay.")

    # List all memories
    list_all_memories()

    # Retrieve specific memory
    retrieve_memory(1)

    # Search for memories
    search_memory("Python")
    search_memory("brain")

    # Wait for memories to decay
    print("\nWaiting for memories to decay...")
    time.sleep(MEMORY_TTL + 1)
    list_all_memories()
