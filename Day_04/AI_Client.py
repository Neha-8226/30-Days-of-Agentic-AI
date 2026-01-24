import requests
import json

# This is the "Tool" we created on Day 3
URL = "http://127.0.0.1:8000/analyze"

print("🤖 Agent: Connected to Sentiment Tool...")

# Imagine these are comments from a user 
comments = [
    "I love learning about AI Agents!"
    "This error is making me so angry."
    "The weaker is just okay today."
]

for comment in comments:
    #1 Prepare the payload (The data packet)
    payload = {"text": comment}
    
    try:
        #2 Call the Tool (POST request)
        response = requests.post(URL, json = payload)
        
        #3 Parse the result
        data = response.json()
        
        #4 Agent makes a decision based on the tool's output
        print(f"\n📝 Input: '{data['text']}'")
        print(f" 📊 Score: {data['score']}")
        print(f" 🏷️ Label: {data['sentiment']}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Is the Day 3 server running?")
        break