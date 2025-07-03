import time
import uuid
from db.orm import save_memory_entry, load_all_memories, update_memory_entry, get_memory_by_id, get_latest_book_balance

class MemoryEngine:
    def __init__(self):
        self.memory_store = load_all_memories()

    def save_memory(self, memory):
        self.memory_store.append(memory)
        save_memory_entry(memory)

    def get_memories(self):
        return self.memory_store
    
    def get_latest_book_balance(self, book_id):
        for mem in self.memory_store:
            if mem["book_id"] == book_id:
                return get_latest_book_balance(book_id)

    def get_memory_by_id(self, memory_id):
        for mem in self.memory_store:
            if mem["id"] == memory_id:
                return mem
        return None
    


    def update_memory(self, updated_mem):
        for i, mem in enumerate(self.memory_store):
            if mem["id"] == updated_mem["id"]:
                self.memory_store[i] = updated_mem
                update_memory_entry(updated_mem)
                break
