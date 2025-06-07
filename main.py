import json
import time

# Memory storage (simulated as a dictionary)
memory = {}

def encode_data(input_data):
    """Encodes input data into a digital format."""
    timestamp = time.time()  # Add a timestamp for uniqueness
    encoded_data = {
        "data": input_data,
        "timestamp": timestamp
    }
    return encoded_data

def store_memory(encoded_data):
    """Stores encoded data in memory."""
    memory_id = len(memory) + 1  # Generate a simple unique ID
    memory[memory_id] = encoded_data
    print(f"Memory stored with ID: {memory_id}")

def retrieve_memory(memory_id):
    """Retrieves stored memory by ID."""
    if memory_id in memory:
        data = memory[memory_id]
        print(f"Retrieved Memory [ID {memory_id}]: {data['data']} (Stored at {time.ctime(data['timestamp'])})")
    else:
        print("Memory ID not found.")

def list_all_memories():
    """Lists all stored memories."""
    print("\nCurrent Stored Memories:")
    for mem_id, data in memory.items():
        print(f"ID: {mem_id}, Data: {data['data']}, Timestamp: {time.ctime(data['timestamp'])}")
    print()

# Example Usage
if __name__ == "__main__":
    print("Digital Memory Simulation\n")

    # Encode and store memories
    input1 = "Learned about the memory function of the brain."
    input2 = "Studied Python for simulating memory systems."
    
    data1 = encode_data(input1)
    store_memory(data1)
    
    data2 = encode_data(input2)
    store_memory(data2)
    
    # List all memories
    list_all_memories()
    
    # Retrieve specific memory
    retrieve_memory(1)
    retrieve_memory(2)
    retrieve_memory(3)  # Non-existent ID for testing
