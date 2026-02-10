import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv

#1 Setup
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Smart Model Selector
def get_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if "flash" in m.name and "gemini" in m.name: return m.name
    except: pass
    return "models/gemini-1.5-flash"

MODEL_NAME = get_model()
model = genai.GenerativeModel(MODEL_NAME)

#2 Tool: The Web Scraper
def scrape_website(url):
    print(f"    Visiting:{url}...")
    try:
        # We pretend to be a real browser (User-Agent) so sites don't block us
        headers={'User-Agent':'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"    ❌ Failed to load page. Status: {response.status_code}")
            return None
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # CLEANING: Remove scripts, styles, ads, and navbars
        for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
            script.decompose()
            
        # Extract text and remove empty lines
        text = soup.get_text()
        clean_text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
        
        return clean_text[:20000]  # Limit to 20k chars context window
    
    except Exception as e:
        print(f"    ❌ Scraper Error: {e}")
        return None
    
#3 The Agent Logic
def web_agent(url, task):
    print(f"\n🕵️ Web Scraper Agent ({MODEL_NAME}) Initialized.")
    
    #1. Scrape
    content = scrape_website(url)
    
    if not content:
        return
    
    print(f"   ✅ Scrapede {len(content)} characters. Analyzing...")
    
    #2 Analyze
    prompt = f"""
    You are an intelligent Web Reader.
    Here is the full content of a webpage:
    
    --- START OF CONTENT ---
    {content}
    --- END OF CONTENT ---
    
    USER TASK: {task}
    
    Please perform the task strictly based on the content above.
    """
    
    try:
        response = model.generate_content(prompt)
        print("\n" + "="*50)
        print(response.text)
        print("="*50)
        
    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        
# --- MAIN LOOP ---
if __name__ == "__main__":
    target_url = input("\nEnter a URL to read: ")
    print("What should I do?")
    print("1. Summarize it.")
    print("2. Rewrite for LinkedIn")
    print("3. Explain the technical details")
    user_task = input("Type your task: ")
    
    web_agent(target_url, user_task)