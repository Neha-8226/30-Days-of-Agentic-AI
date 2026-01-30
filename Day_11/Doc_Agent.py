import os
import time

# 1. Setup - No API Key needed for this test
DOCUMENT_PATH = "secret_mission.txt"

def load_document():
    """Reads the REAL text file from your hard drive."""
    if os.path.exists(DOCUMENT_PATH):
        with open(DOCUMENT_PATH, "r") as f:
            return f.read()
    else:
        print("❌ Error: Could not find the file!")
        return ""

# 2. Load the content (This proves your file path is correct!)
doc_content = load_document()

# --- THE SIMULATED AGENT ---

def run_agent():
    print("🕵️ Mission Bot: Identity Verified. Briefing loaded. (Type 'exit' to quit)")
    
    # Prove we actually read the file
    if "Blueberry-Pancake" in doc_content:
        print("   (✅ System Check: 'secret_mission.txt' loaded successfully!)")
    else:
        print("   (❌ System Check: File loaded, but content seems empty?)")

    while True:
        user_input = input("\nAgent Neha: ")
        if user_input.lower() == "exit":
            break
        
        # Simulate the AI "Reading" the document
        print("   (🕵️ Analyzing document for answers...)")
        time.sleep(1) # Fake thinking time
        
        # Simple keyword matching to simulate RAG
        if "base" in user_input.lower() or "where" in user_input.lower():
            print("🕵️ Bot: According to the briefing, the base is under the 'Eiffel Tower' in Paris.")
        elif "password" in user_input.lower():
            print("🕵️ Bot: The password is 'Blueberry-Pancake'. Keep it safe!")
        elif "president" in user_input.lower():
            print("🕵️ Bot: Classified Information: Not found in briefing.")
        else:
            print("🕵️ Bot: I can only answer questions about the Mission Briefing.")

if __name__ == "__main__":
    run_agent()