import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import time
import threading

class Dashboard:
    def __init__(self, memory_engine):
        self.memory_engine = memory_engine

    def plot_memory_strengths(self):
        memories = self.memory_engine.get_memories()
        if not memories:
            print("No memories to visualize.")
            return

        timestamps = [datetime.fromtimestamp(mem["timestamp"]) for mem in memories]
        strengths = [mem["strength"] for mem in memories]
        labels = [mem["type"] for mem in memories]

        plt.figure(figsize=(10, 6))
        plt.title("Memory Strength Over Time")
        plt.xlabel("Time")
        plt.ylabel("Strength")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.plot(timestamps, strengths, marker='o', linestyle='-')

        for i, label in enumerate(labels):
            plt.annotate(label, (timestamps[i], strengths[i]))

        plt.tight_layout()
        plt.grid(True)
        plt.show()

    def run_dashboard_loop(self, interval=30):
        def loop():
            while True:
                self.plot_memory_strengths()
                time.sleep(interval)

        thread = threading.Thread(target=loop)
        thread.daemon = True
        thread.start()

def launch_dashboard(memory_engine):
    dashboard = Dashboard(memory_engine)
    dashboard.run_dashboard_loop()
