import os 
import requests
import google.generativeai as genai
from dotenv import load_dotenv
import time

#1 Setup
load_dotenv()
genai.configure(api_key = os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# The URL of your local tool (Day 3)
TOOL_URL = "http://127.0.0.1:8000/analyze"

def get_sentiment(text):
    """The function that 'pushes the button' on your API"""
    try:
        response = requests.post(TOOL_URL, json = {"text":text})
        return response.json()
    except:
        return {"error": "Tool is offline"}
    
#2 The Agent Loop
print("🤖 Agent: I am ready! (Type 'exit' to quit)")

# ... setup code remains the same ...

print("🤖 Agent: I am ready! (Type 'exit' to quit)")

while True:
    try:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            break

        # Decision Phase
        decision_prompt = f"Does this input '{user_input}' need sentiment analysis? Answer YES or NO."
        decision = model.generate_content(decision_prompt).text.strip()
        print(f"   (🧠 Thought: {decision})")

        # Execution Phase
        if "YES" in decision.upper():
            print("   (🚀 Action: Triggering Sentiment Tool...)")
            tool_result = get_sentiment(user_input)
            
            final_prompt = f"User said: {user_input}. Tool analysis: {tool_result}. Write a reply."
            final_response = model.generate_content(final_prompt)
            print(f"🤖 Agent: {final_response.text}")
        else:
            chat_response = model.generate_content(user_input)
            print(f"🤖 Agent: {chat_response.text}")

    except Exception as e:
        print(f"\n⚠️ API Traffic limit hit. Waiting 10 seconds...")
        time.sleep(10)
        print("🔄 Retrying...")
        continue  # Loops back to let you try again