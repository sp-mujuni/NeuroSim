import sqlite3
import time
from datetime import datetime
import matplotlib.pyplot as plt

# Constants
DATABASE_FILE = "memory3.db"
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
            last_accessed REAL NOT NULL,
            access_count INTEGER DEFAULT 0
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
        INSERT INTO memory (data, timestamp, last_accessed, access_count)
        VALUES (?, ?, ?, 0)
    """, (data, timestamp, timestamp))
    conn.commit()
    conn.close()
    print(f"Memory stored: '{data}'")

def retrieve_memory(memory_id):
    """Retrieves a memory by ID and updates its access count."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM memory WHERE id = ?", (memory_id,))
    row = cursor.fetchone()
    
    if row:
        if is_memory_expired(row):
            delete_memory(memory_id)
            print(f"Memory [ID {memory_id}] has decayed and is no longer accessible.")
        else:
            update_last_accessed(memory_id)
            print(f"Retrieved Memory [ID {row[0]}]: '{row[1]}' (Stored at {time.ctime(row[2])})")
    else:
        print("Memory ID not found.")
    conn.close()

def is_memory_expired(memory_row):
    """Checks if a memory has expired based on TTL."""
    last_accessed = memory_row[3]
    return time.time() - last_accessed > MEMORY_TTL

def update_last_accessed(memory_id):
    """Updates the last accessed timestamp and increments access count."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE memory
        SET last_accessed = ?, access_count = access_count + 1
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

# Visualization functions
def plot_memory_retention():
    """Plots the number of active vs. decayed memories."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM memory")
    rows = cursor.fetchall()
    conn.close()

    active_count = 0
    decayed_count = 0

    for row in rows:
        if is_memory_expired(row):
            decayed_count += 1
        else:
            active_count += 1

    # Plotting
    labels = ['Active Memories', 'Decayed Memories']
    counts = [active_count, decayed_count]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, counts, color=['green', 'red'])
    plt.title('Memory Retention Over Time')
    plt.ylabel('Number of Memories')
    plt.show()

def plot_access_frequency():
    """Plots the access frequency of each memory."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, access_count FROM memory")
    rows = cursor.fetchall()
    conn.close()

    ids = [row[0] for row in rows]
    access_counts = [row[1] for row in rows]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(ids, access_counts, color='blue')
    plt.title('Memory Access Frequency')
    plt.xlabel('Memory ID')
    plt.ylabel('Access Count')
    plt.xticks(ids)
    plt.show()

def plot_memory_age_distribution():
    """Plots the age distribution of active memories."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp FROM memory")
    rows = cursor.fetchall()
    conn.close()

    current_time = time.time()
    ages = [(current_time - row[0]) / 60 for row in rows if not is_memory_expired(row)]  # Age in minutes

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.hist(ages, bins=10, color='orange', edgecolor='black')
    plt.title('Memory Age Distribution')
    plt.xlabel('Memory Age (minutes)')
    plt.ylabel('Number of Memories')
    plt.show()

# Example usage
if __name__ == "__main__":
    print("Digital Memory Simulation with Visualization\n")

    # Set up the database
    setup_database()

    # Store memories
    store_memory("Learned about memory trends visualization.")
    store_memory("Explored matplotlib for plotting graphs.")
    store_memory("Studied memory age distribution and retention.")
    store_memory("Analyzed access frequency of stored memories.")
    store_memory("Implemented a memory decay mechanism with TTL.")

    # Retrieve and interact with memories
    retrieve_memory(1)
    retrieve_memory(2)

    # Visualizations
    print("\nGenerating Memory Retention Graph...")
    plot_memory_retention()

    print("\nGenerating Access Frequency Graph...")
    plot_access_frequency()

    print("\nGenerating Memory Age Distribution Graph...")
    plot_memory_age_distribution()
