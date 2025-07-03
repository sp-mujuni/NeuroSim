import tkinter as tk
from engine.memory_engine import MemoryEngine
from engine.similarity import SimilarityScorer
from engine.reinforcement import ReinforcementEngine
from ui.gui import NeuroSimGUI

# Initialize core components
memory_engine = MemoryEngine()
similarity_scorer = SimilarityScorer()
reinforcement = ReinforcementEngine()

# Launch GUI for patient entry and retrieval
app = tk.Tk()
app.title("Namulundu Hospital")
NeuroSimGUI(app, memory_engine, similarity_scorer, reinforcement)

# Start GUI mainloop
app.mainloop()
