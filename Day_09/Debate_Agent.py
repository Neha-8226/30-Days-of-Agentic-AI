import time
import random

# --- SIMULATED AGENTS (No API Key needed) ---

def ask_alex_optimist(last_input):
    """Alex: The Tech Optimist (Simulated)"""
    print("   (🔵 Alex is thinking...)")
    time.sleep(1) # Simulate processing time
    
    # Alex always finds a positive spin
    responses = [
        "Absolutely! Mars is the backup drive for humanity. We need to expand to survive! 🚀",
        "Technology will solve the radiation issues. We will build domed cities and terraform the planet! 🌌",
        "Think of the scientific breakthroughs! Living on Mars will push engineering to new heights. 🦾"
    ]
    return random.choice(responses)

def ask_sam_skeptic(last_input):
    """Sam: The Tech Skeptic (Simulated)"""
    print("   (🔴 Sam is thinking...)")
    time.sleep(1) # Simulate processing time
    
    # Sam always finds a flaw
    responses = [
        "But at what cost? We haven't even fixed Earth yet. Why ruin another planet? 🌍",
        "The radiation is deadly and the gravity will destroy our bones. It's a suicide mission. ☠️",
        "This is just an escape fantasy for billionaires. Regular people will suffer. 📉"
    ]
    return random.choice(responses)

# --- MAIN LOOP: The Autonomous Debate ---
print("🥊 The Debate Arena is Open! (Agents will talk to each other)")
topic = input("Enter a topic (e.g., 'Should humans live on Mars?'): ")

print(f"\n--- Round 1: Moderator throws the topic '{topic}' ---")

# Step 1: Moderator starts
last_message = f"The topic is: {topic}. What is your opening statement?"
print(f"📢 Moderator: {last_message}\n")

for round_num in range(1, 4): # Run for 3 rounds
    
    # --- Agent A Speaks ---
    response_A = ask_alex_optimist(last_message)
    print(f"🔵 Alex (Optimist): {response_A}")
    
    # Pass A's output as input to B
    last_message = response_A 
    print("-" * 20)
    
    # --- Agent B Speaks ---
    response_B = ask_sam_skeptic(last_message)
    print(f"🔴 Sam (Skeptic): {response_B}")
    
    # Pass B's output as input to As
    last_message = response_B
    
    print(f"\n--- Round {round_num} Complete ---\n")

print("🔔 DING DING! Debate Finished.")