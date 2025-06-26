# 🧠 Real-Time Memory Interaction and Visualization

MemLog implements a simulated memory management system backed by an SQLite database. It allows users to store and retrieve "memories" (text entries for now), while visualizing in real-time the memory retention, access frequency, and age distribution using `matplotlib`.

## 🚀 Features

- Store and retrieve text-based memories via command line input
- Automatic memory decay after a configurable TTL (default: 1 hour)
- Real-time plots showing:
  - Active vs. decayed memories
  - Memory access frequency
  - Age distribution of stored memories
- Threaded user interaction while visualizing

## 📦 Requirements

- Python 3.7 or higher
- `matplotlib` for data visualization

## 🛠️ Setup Instructions

### 1. Clone or Download the Project

```bash
git clone https://github.com/sp-mujuni/MemLog.git
cd MemLog
````

### 2. Create and Activate a Virtual Environment

#### On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install matplotlib
```

## 🧪 Running the Script

Once the environment is set up:

```bash
python main.py
```

You will see a GUI window with real-time plots and a terminal interface for inputting commands.

### Supported Commands:

* `store` — Adds a new memory to the database
* `retrieve` — Retrieves a memory by its ID
* `exit` — Ends terminal interaction (visualization will continue)

## 🗃️ Database

* The script creates a SQLite database called `memorybase.db`
* Data schema includes:

  * `id`: Auto-incremented ID
  * `data`: Text content of the memory
  * `timestamp`: When the memory was created
  * `last_accessed`: Last access timestamp
  * `access_count`: Number of times the memory has been accessed

## 🧼 Memory Expiry

Memories expire after 1 hour (3600 seconds) of inactivity. Expired memories are shown in red on the "Memory Retention" chart.

## 🔄 Visualization Refresh Rate

* All visual plots are updated every 2 seconds using `matplotlib.animation.FuncAnimation`.

---

## 📖 License

MIT License