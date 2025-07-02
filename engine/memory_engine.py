import time
import uuid
from db.orm import save_memory_entry

class MemoryEngine:
    def __init__(self):
        self.memory_store = []  # temporary in-memory list; production should use persistent DB

    def encode_observations(self, observations):
        for obs in observations:
            memory = {
                "id": str(uuid.uuid4()),
                "timestamp": time.time(),
                "content": obs.get("resource", {}).get("valueQuantity", {}).get("value", "Unknown"),
                "type": obs.get("resource", {}).get("code", {}).get("text", "Observation"),
                "strength": 1.0,
                "context_tags": [obs.get("resource", {}).get("code", {}).get("coding", [{}])[0].get("code", "unknown")]
            }
            self.memory_store.append(memory)
            save_memory_entry(memory)

    def get_memories(self):
        return self.memory_store

    def update_strength(self, memory_id, new_strength):
        for mem in self.memory_store:
            if mem["id"] == memory_id:
                mem["strength"] = new_strength
                break
