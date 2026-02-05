import os
import time
import google.generativeai as genai
from duckduckgo_search import DDGS
from dotenv import load_dotenv

#1 Setup
load_dotenv()
genai.configure(api_key = os.getenv("GEMINI_API_KEY"))

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

# --- TOOLS ---

def search(query):
    """Real web search using DuckDuckGo"""
    print(f"  🌐 Searching: '{query}'...")
    try:
        with DDGS() as ddgs:
            # Get top 2 results per sub-query to keep it fast
            results = list(ddgs.text(query, max_results=2))
            return str(results)
    except Exception as e:
        print(f"  ❌ Search failed: {e}")
        return ""
    
def generate_plan(topic):
    """The Agent plans 3 specific sub-questions to research."""
    prompt = f"""
    You are a Research Lead.
    The user wants to know about: "{topic}".
    Break this into 3 specific, distinct search queries to get a comprehensive answer.
    
    Output format:
    Query 1
    Query 2
    Query 3
    
    (Do not output anything else. No numbers, just lines).
    """
    response = model.generate_content(prompt)
    # Clean up the response into a list
    queries = response.text.strip().split('\n')
    # Filter out empty lines
    return [q.strip() for q in queries if q.strip()][:3]

# ---MAIN AGENT LOOP ---
def deep_research_agent(user_topic):
    print(f"\n🧠 Deep Research Agent ({MODEL_NAME})")
    print(f"🎯 Objective: Comprehensive report on '{user_topic}'")
    
    #1 PLAN
    print("\n1️⃣ Planning Phase...")
    sub_queries = generate_plan(user_topic)
    
    if not sub_queries:
        print("❌ Failed to generate a plan.")
        return
    
    print(f"   -> Strategy: {sub_queries}")
    
    #2 EXECUTE (Loop through the plan)
    print("\n2️⃣ Execution Phase...")
    all_knowledge = ""
    
    for i, query in enumerate(sub_queries):
        # We add a tiny delay to be polite to the search engine
        time.sleep(1)
        data = search(query)
        all_knowledge += f"\n--- DATA FROM SEARCH '{query}' ---\n{data}\n"
        
        #3 SYNTHESIZE
        print("\n3️⃣ Analysis Phase (Writing Report)...")
        final_prompt = f"""
        You are a Senior Editor.
        Write a comprehensive deep-dive resport on:
        "{user_topic}"
        
        Base your report STRICTLY on the gathered research data below:
        {all_knowledge}
        
        Format:
        # Deep Dive: {user_topic}
        ## Executive Summary
        ## Key Insights (Combine data from different searches)
        ## Technical/Specific Details
        ## Conclusion
        """
        
        report = model.generate_content(final_prompt).text
        
        # Save it
        filename = f"Deep_Dive_{user_topic.replace('', '_')}.md"
        with open(filename, "w", encoding = "utf-8") as f:
            f.write(report)
            
        print(f"\n✅ Mission Complete! Report saved to: {filename}")
        print(f"  (Check your Day_15 folder for the full markdown file)")
        
# Run it
if __name__ == "__main__":
    topic = input("Enter a complex topic: ")
    deep_research_agent(topic)
