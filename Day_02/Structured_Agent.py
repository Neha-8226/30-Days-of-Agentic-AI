import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

role = "AI Developer" # Hardcoded to save you typing time

try:
    print(f"🤖 Fetching Day 2 Result for {role}...")
    # Strict prompt to force JSON
    prompt = f"Return ONLY a JSON object for the role of {role} with 'role', 3 'skills', and 'difficulty' (1-10). No markdown."
    response = model.generate_content(prompt)
    
    # Clean and Parse
    text = response.text.strip().replace("```json", "").replace("```", "")
    data = json.loads(text)
    
    # SAVE THE RESULT to a file (This is your 'Proof of Work')
    with open("Day_02/result.json", "w") as f:
        json.dump(data, f, indent=4)
    
    print("\n✅ SUCCESS! Result saved to Day_02/result.json")
    print(json.dumps(data, indent=2))

except Exception as e:
    print(f"❌ Error: {e}. If it's a 429, wait 30 seconds.")