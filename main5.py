import sqlite3
import time
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading

# Constants
DATABASE_FILE = "memory5.db"
MEMORY_TTL = 3600  # Time-to-live for memory in seconds

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
    """Retrieves a memory by ID."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM memory WHERE id = ?", (memory_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        if is_memory_expired(row):
            print(f"Memory [ID {memory_id}] has decayed and is no longer accessible.")
        else:
            update_last_accessed(memory_id)
            print(f"Retrieved Memory [ID {row[0]}]: '{row[1]}' (Stored at {time.ctime(row[2])})")
    else:
        print("Memory ID not found.")

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

def get_memory_data():
    """Fetches all memory data from the database and categorizes it."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM memory")
    rows = cursor.fetchall()
    conn.close()

    active_memories = []
    decayed_memories = 0
    access_counts = []

    for row in rows:
        if is_memory_expired(row):
            decayed_memories += 1
        else:
            active_memories.append(row)
            access_counts.append(row[4])  # Collect access counts for active memories

    return active_memories, decayed_memories, access_counts

# Real-time visualization functions
def plot_memory_retention(ax1):
    """Plots real-time memory retention."""
    _, decayed, _ = get_memory_data()
    active = len(_) - decayed
    ax1.clear()
    ax1.bar(['Active', 'Decayed'], [active, decayed], color=['green', 'red'])
    ax1.set_title('Memory Retention Over Time')
    ax1.set_ylabel('Number of Memories')

def plot_access_frequency(ax2):
    """Plots real-time access frequency."""
    active_memories, _, access_counts = get_memory_data()
    ids = [mem[0] for mem in active_memories]
    ax2.clear()
    ax2.bar(ids, access_counts, color='blue')
    ax2.set_title('Memory Access Frequency')
    ax2.set_xlabel('Memory ID')
    ax2.set_ylabel('Access Count')

def plot_memory_age_distribution(ax3):
    """Plots real-time memory age distribution."""
    active_memories, _, _ = get_memory_data()
    current_time = time.time()
    ages = [(current_time - mem[2]) / 60 for mem in active_memories]  # Age in minutes
    ax3.clear()
    ax3.hist(ages, bins=10, color='orange', edgecolor='black')
    ax3.set_title('Memory Age Distribution')
    ax3.set_xlabel('Age (minutes)')
    ax3.set_ylabel('Number of Memories')

def update(frame, ax1, ax2, ax3):
    """Updates all plots dynamically."""
    plot_memory_retention(ax1)
    plot_access_frequency(ax2)
    plot_memory_age_distribution(ax3)

# User interaction function
def handle_user_input():
    """Handles user input in a separate thread."""
    while True:
        command = input("\nEnter command (store/retrieve/exit): ").strip().lower()
        if command == "store":
            data = input("Enter memory to store: ")
            store_memory(data)
        elif command == "retrieve":
            try:
                memory_id = int(input("Enter memory ID to retrieve: "))
                retrieve_memory(memory_id)
            except ValueError:
                print("Invalid ID format.")
        elif command == "exit":
            print("Exiting user interaction. Visualization will continue.")
            break
        else:
            print("Unknown command. Try 'store', 'retrieve', or 'exit'.")

# Example usage
if __name__ == "__main__":
    print("Real-Time Memory Interaction and Visualization\n")

    # Set up the database
    setup_database()

    # Start user input handling in a separate thread
    user_thread = threading.Thread(target=handle_user_input, daemon=True)
    user_thread.start()

    # Create a figure for real-time plots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))

    # Set up the real-time animation
    ani = FuncAnimation(
        fig, update, fargs=(ax1, ax2, ax3), interval=2000
    )  # Updates every 2 seconds

    plt.tight_layout()
    plt.show()
