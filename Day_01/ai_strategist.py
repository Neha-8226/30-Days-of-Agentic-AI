import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors

# 1. Load the secrets from your .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. Initialize the AI Client with a Stable Connection fix
# This 'http_options' helps prevent the SSL/Timeout errors you saw earlier
client = genai.Client(
    api_key=api_key,
    http_options={'api_version': 'v1'} 
)

# 3. Get user input
user_goal = input("What tech role do you want by March 2026? ")

# 4. The Professional Retry Loop
# To a 10 LPA Engineer, a single failure is just a reason to try again.
for attempt in range(3):
    try:
        print(f"🤖 AI is thinking (Attempt {attempt + 1})...")
        
        # Using the most stable model for Free Tier
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"I want to be a {user_goal}. Give me a 3-step technical roadmap for a 10 LPA+ job."
        )
        
        # 5. Output the result and exit the loop on success
        print("\n--- YOUR AI STRATEGY ---")
        print(response.text)
        break
        
    except Exception as e:
        if "429" in str(e):
            print("⏳ Quota hit. Waiting 20 seconds for the server to cool down...")
            time.sleep(20)
        elif "404" in str(e):
            print("❌ 404 Error: The API couldn't find the model. Verify your key.")
            break
        else:
            print(f"❌ Critical Error: {e}")
            break

print("\n--- Day 1 Script Execution Finished ---")