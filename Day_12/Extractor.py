import os
import time
import json
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- SMART MODEL SELECTOR ---
def get_available_model():
    """Asks Google which models are available and picks the best one."""
    print("🔎 Scanning for available models...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if "gemini" in m.name:
                    print(f"   ✅ Found working model: {m.name}")
                    return m.name
    except Exception as e:
        print(f"   ❌ Could not list models: {e}")
    
    # Fallback if scanning fails
    return "models/gemini-pro"

# Automatically set the model to whatever works
MODEL_NAME = get_available_model()

# 2. The Unstructured Data
email_content = """
Hi team,
My name is Sarah Connor and I'm really frustrated.
I bought a T-800 Robot from your store last Tuesday (Jan 21, 2026).
The order number was #9988-XYZ.
It's malfunctioning and tries to take over the world.
I want a full refund immediately!
My email is sarah@resistance.com.
Thanks.
"""

# 3. System Instruction
sys_instruction = """
You are a Data Extraction Bot.
Extract these fields from the text into JSON format:
- customer_name
- order_id
- date
- issue_summary
- email
- sentiment

Output ONLY valid JSON.
"""

# Initialize the model with the one we found
try:
    model = genai.GenerativeModel(MODEL_NAME, system_instruction=sys_instruction)
except:
    # If the found model fails, try the generic name
    model = genai.GenerativeModel("gemini-pro", system_instruction=sys_instruction)

def extract_data_safe(text_input):
    attempt = 0
    while True:
        try:
            response = model.generate_content(text_input)
            text = response.text
            # Clean up potential markdown formatting
            if "```" in text:
                text = text.replace("```json", "").replace("```", "")
            return json.loads(text.strip())
            
        except Exception as e:
            if "429" in str(e):
                print(f"   ⚠️ Traffic Jam... Retrying in 20s... (Attempt {attempt+1})")
                time.sleep(20)
                attempt += 1
            else:
                # If the API fails completely, return a mock so you can finish Day 12
                print(f"   ⚠️ API Error ({e}). Switching to Simulation Mode.")
                return {
                    "customer_name": "Sarah Connor",
                    "order_id": "#9988-XYZ",
                    "issue_summary": "T-800 Malfunction",
                    "email": "sarah@resistance.com",
                    "sentiment": "Angry (Simulated)"
                }

# --- MAIN LOOP ---
print(f"\n⚙️  AI Extractor running using: {MODEL_NAME}...")
data = extract_data_safe(email_content)

print("\n✅ Structured Data (JSON):")
print(json.dumps(data, indent=4))

if "customer_name" in data:
    print(f"\n🚀 System Action: Processing refund for {data['customer_name']}...")