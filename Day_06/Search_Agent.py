import os
import time
import google.generativeai as genai
from dotenv import load_dotenv
from duckduckgo_search import DDGS

# 1. Setup
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-lite-preview-02-05") 

def search_web(query):
    print(f"   (🔎 Tool Action: Searching the web for '{query}'...)")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if results:
                return "\n".join([f"- {r['body']}" for r in results])
            return "No results found."
    except Exception as e:
        return f"Search error: {e}"

print("🤖 Research Agent: I have internet access! (Type 'exit' to quit)")

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "exit":
        break

    # FIXED: We now convert input to lowercase before checking keywords
    if "price" in user_input.lower() or "who" in user_input.lower() or "what" in user_input.lower():
        search_data = search_web(user_input)
        
        try:
            final_prompt = f"User: {user_input}. Data: {search_data}. Answer:"
            response = model.generate_content(final_prompt)
            print(f"🤖 Agent: {response.text}")
        except Exception:
            # FALLBACK: If Gemini is busy, print the data anyway!
            print("\n⚠️ (Gemini is busy, but here is what I found:)")
            print(f"🤖 Agent: Based on my search:\n{search_data}")
            
    else:
        try:
            response = model.generate_content(user_input)
            print(f"🤖 Agent: {response.text}")
        except:
            print("⚠️ System is busy. Try again.")
            