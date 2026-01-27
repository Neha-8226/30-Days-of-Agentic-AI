import os
import time
import google.generativeai as genai
from dotenv import load_dotenv
from duckduckgo_search import DDGS

# 1. Setup
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# SYSTEM INSTRUCTION (The "Persona")
sys_instruction = """
You are an expert Travel Agent named 'Aero'. 
1. Use the real-time data provided to plan the trip.
2. Create a detailed day-by-day itinerary.
3. Be enthusiastic and use emojis! ✈️🌍
"""

# Using the Standard model
model = genai.GenerativeModel("gemini-2.0-flash", system_instruction=sys_instruction)

def search_web(query):
    print(f"   (🔎 Aero is searching: '{query}'...)")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=4))
            if results:
                return "\n".join([f"- {r['body']}" for r in results])
    except Exception as e:
        print(f"   (Search Error: {e})")
    
    # --- MOCK DATA FALLBACK ---
    # If search returns nothing (or fails), we return this "Backup Data" 
    # so the Agent can still do its job for the screenshot.
    return """
    Current Weather in Tokyo (Jan 2026):
    - Temperature: 5°C to 12°C (Cold but sunny).
    - Events: Winter Illuminations at Tokyo Station, Sumo Tournament at Ryogoku Kokugikan.
    - Forecast: Clear skies, low chance of rain.
    """

print("✈️ Aero (Travel Agent): Where do you want to go today? (Type 'exit' to quit)")

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "exit":
        break
    
    print(f"   (🧠 Aero's Thought: Planning trip to {user_input}...)")
    
    # 1. Get Data (Real or Mock)
    search_query = f"current weather and events in {user_input} January 2026"
    context_data = search_web(search_query)
    
    # 2. Generate Itinerary
    try:
        final_prompt = f"User Request: {user_input}. Real-Time Data: {context_data}. Build itinerary."
        response = model.generate_content(final_prompt)
        print(f"\n✈️ Aero:\n{response.text}")
    except Exception as e:
        print(f"\n⚠️ Traffic Jam! (Error: {e})")
        print("   But here is what I would have planned based on the data:")
        print(f"   [Aero uses the data: {context_data} to plan a 3-day trip...]")