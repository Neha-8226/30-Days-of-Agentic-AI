import time

# --- SIMULATED AGENTS (No API Key needed for this test) ---

def math_agent(query):
    print("   (🧮 Math Agent: On it!)")
    time.sleep(1) # Simulate thinking
    return "🧮 Math Solution:\n   √144 = 12\n   12 + 50 = 62"

def writer_agent(query):
    print("   (✍️ Writer Agent: Inspiration striking!)")
    time.sleep(1) # Simulate thinking
    return "✍️ Creative Piece:\n   The robot sat on red dust,\n   Dreaming of rain and rust."

# --- THE MANAGER (ROUTER) ---

def manager_agent(user_input):
    print(f"\n👔 Manager: Analyzing request '{user_input}'...")
    time.sleep(1) # Simulate thinking
    
    # Simple logic to simulate the AI's decision
    decision = "GENERAL"
    if "root" in user_input or "plus" in user_input or "math" in user_input:
        decision = "MATH"
    elif "poem" in user_input or "story" in user_input:
        decision = "WRITER"
        
    print(f"   (🧠 Decision: Routing to -> {decision})")
        
    if decision == "MATH":
        return math_agent(user_input)
    elif decision == "WRITER":
        return writer_agent(user_input)
    else:
        return "👔 Manager: I'll handle this myself."

# --- MAIN LOOP ---
print("🤖 Multi-Agent Team: Ready for work! (Type 'exit' to quit)")

while True:
    user_query = input("\nYou: ")
    if user_query.lower() == "exit":
        break
    
    result = manager_agent(user_query)
    print(result)