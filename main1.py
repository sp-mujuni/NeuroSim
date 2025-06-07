import json
import time
from datetime import datetime, timedelta

# Memory storage (simulated as a dictionary)
memory = {}

# Memory decay settings (in seconds)
MEMORY_TTL = 60  # Memory lasts for 60 seconds before decaying

def encode_data(input_data):
    """Encodes input data into a digital format."""
    timestamp = time.time()  # Add a timestamp for uniqueness
    encoded_data = {
        "data": input_data,
        "timestamp": timestamp,
        "last_accessed": timestamp  # For decay tracking
    }
    return encoded_data

def store_memory(encoded_data):
    """Stores encoded data in memory."""
    memory_id = len(memory) + 1  # Generate a unique ID
    memory[memory_id] = encoded_data
    print(f"Memory stored with ID: {memory_id}")

def retrieve_memory(memory_id):
    """Retrieves stored memory by ID."""
    if memory_id in memory:
        if is_memory_expired(memory_id):
            delete_memory(memory_id)
            print(f"Memory [ID {memory_id}] has decayed and is no longer accessible.")
        else:
            memory[memory_id]['last_accessed'] = time.time()  # Update access time
            data = memory[memory_id]
            print(f"Retrieved Memory [ID {memory_id}]: {data['data']} (Stored at {time.ctime(data['timestamp'])})")
    else:
        print("Memory ID not found.")

def list_all_memories():
    """Lists all stored memories, excluding decayed ones."""
    print("\nCurrent Stored Memories:")
    for mem_id in list(memory.keys()):
        if is_memory_expired(mem_id):
            delete_memory(mem_id)
        else:
            data = memory[mem_id]
            print(f"ID: {mem_id}, Data: {data['data']}, Timestamp: {time.ctime(data['timestamp'])}")
    print()

def is_memory_expired(memory_id):
    """Checks if a memory has decayed based on TTL."""
    if memory_id in memory:
        last_accessed = memory[memory_id]['last_accessed']
        if time.time() - last_accessed > MEMORY_TTL:
            return True
    return False

def delete_memory(memory_id):
    """Deletes a memory from storage."""
    if memory_id in memory:
        del memory[memory_id]

def search_memory(keyword):
    """Searches for memories containing a specific keyword."""
    print(f"\nSearching for memories with keyword: '{keyword}'")
    found = False
    for mem_id in list(memory.keys()):
        if is_memory_expired(mem_id):
            delete_memory(mem_id)
        else:
            if keyword.lower() in memory[mem_id]['data'].lower():
                found = True
                print(f"Found Memory [ID {mem_id}]: {memory[mem_id]['data']}")
    if not found:
        print("No matching memories found.")

# Example Usage
if __name__ == "__main__":
    print("Enhanced Digital Memory Simulation\n")

    # Encode and store memories
    input1 = "Learned about the memory function of the brain."
    input2 = "Studied Python for simulating memory systems."
    input3 = "Explored context-based retrieval and memory decay."
    
    data1 = encode_data(input1)
    store_memory(data1)
    
    data2 = encode_data(input2)
    store_memory(data2)
    
    data3 = encode_data(input3)
    store_memory(data3)

    # List all memories
    time.sleep(2)  # Simulate passage of time
    list_all_memories()

    # Retrieve specific memory
    retrieve_memory(1)

    # Search for memories
    search_memory("Python")
    search_memory("brain")

    # Simulate memory decay
    print("\nWaiting for memories to decay...")
    time.sleep(MEMORY_TTL + 1)  # Wait until memories expire
    list_all_memories()  # Check decayed memories
