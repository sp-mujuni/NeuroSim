import sqlite3
import time
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
DATABASE_FILE = "memory4.db"
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
def is_memory_expired(memory_row):
    """Checks if a memory has expired based on TTL."""
    last_accessed = memory_row[3]
    return time.time() - last_accessed > MEMORY_TTL

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
    active_memories, decayed, _ = get_memory_data()
    active = len(active_memories)
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

# Real-time update function
def update(frame, ax1, ax2, ax3):
    """Updates all plots dynamically."""
    plot_memory_retention(ax1)
    plot_access_frequency(ax2)
    plot_memory_age_distribution(ax3)

# Example usage
if __name__ == "__main__":
    print("Real-Time Digital Memory Trends Visualization\n")

    # Set up the database
    setup_database()

    # Create a figure for real-time plots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))

    # Set up the real-time animation
    ani = FuncAnimation(
        fig, update, fargs=(ax1, ax2, ax3), interval=2000
    )  # Updates every 2 seconds

    plt.tight_layout()
    plt.show()
