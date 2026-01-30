import os
import json
import time

# 1. Setup - No API Key needed for this test
MEMORY_FILE = "user_memory.json"

# --- MEMORY FUNCTIONS (REAL - This part actually works!) ---

def load_memory():
    """Reads the JSON file from your hard drive."""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(key, value):
    """Writes new facts to your hard drive."""
    data = load_memory()
    data[key] = value
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(f"   (💾 Memory Saved: {key} = {value})")

# --- THE SIMULATED AGENT ---

def run_agent():
    # 1. Load Memory on Startup
    user_data = load_memory()
    
    print("🐘 Memory Agent: I remember things. (Type 'exit' to quit)")
    
    # PROOF OF MEMORY: Check if we know the user
    if user_data:
        print(f"   (🧠 I loaded this info about you: {user_data})")
        if "Name" in user_data:
            print(f"🐘 Agent: Welcome back, {user_data['Name']}! I remember you.")
    else:
        print("   (🧠 Memory is empty. I don't know you yet.)")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            break
        
        # 2. Simulate "Learning" (Manual Logic)
        # If user says "My name is...", we manually save it to JSON
        if "my name is" in user_input.lower():
            # Extract name manually
            name = user_input.split("is")[-1].strip()
            save_memory("Name", name)
            print(f"🐘 Agent: Nice to meet you, {name}! I have saved this to my long-term memory.")
        
        # If user asks "What is my name?"
        elif "what is my name" in user_input.lower():
            current_data = load_memory()
            if "Name" in current_data:
                print(f"🐘 Agent: Your name is {current_data['Name']}.")
            else:
                print("🐘 Agent: I don't know your name yet.")
        
        else:
            print("🐘 Agent: (I am just a simulation. Tell me 'My name is Neha' to test my memory!)")

if __name__ == "__main__":
    run_agent()