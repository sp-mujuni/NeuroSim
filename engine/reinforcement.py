class ReinforcementEngine:
    def __init__(self, learning_rate=0.1):
        self.learning_rate = learning_rate

    def reinforce(self, memory):
        old_strength = memory.get("strength", 1.0)
        new_strength = old_strength + self.learning_rate * (1.0 - old_strength)
        memory["strength"] = min(new_strength, 1.0)
        return memory
