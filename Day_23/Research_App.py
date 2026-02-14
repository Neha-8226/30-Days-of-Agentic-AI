import streamlit as st
import os
import google.generativeai as genai
import wikipedia
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if "flash" in m.name and "gemini" in m.name: return m.name
    except: pass
    return "models/gemini-1.5-flash"

MODEL_NAME = get_model()
model = genai.GenerativeModel(MODEL_NAME)

# 2. The Tool: Wikipedia Search
def search_web(query):
    """Searches Wikipedia and returns a summary."""
    try:
        # Fetch a 3-sentence summary of the topic
        result = wikipedia.summary(query, sentences=3)
        return f"Wikipedia Context:\n{result}"
    except wikipedia.exceptions.DisambiguationError as e:
        # If the search is too broad (e.g., "Apple" - fruit or company?)
        return f"Topic is too broad. Did you mean one of these: {e.options[:3]}?"
    except wikipedia.exceptions.PageError:
        return "No Wikipedia page found for this query."
    except Exception as e:
        return f"Search Error: {e}"

# 3. The Streamlit UI
st.set_page_config(page_title="Wikipedia Research Agent", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ Wikipedia Research Agent")
st.write("Ask me anything factual! I will search Wikipedia before answering.")

# The Chat Input
user_query = st.chat_input("E.g., Tell me about the Kolhapuri chappal...")

if user_query:
    # 1. Show User's message
    with st.chat_message("user"):
        st.write(user_query)

    # 2. Show AI's response process
    with st.chat_message("assistant"):
        
        # Searching Phase
       # Searching Phase
        with st.spinner("🔍 Extracting search topic..."):
            # Have Gemini figure out the exact keyword first!
            keyword_prompt = f"Extract the main Wikipedia search topic from this sentence: '{user_query}'. Reply with ONLY the topic name, nothing else."
            search_topic = model.generate_content(keyword_prompt).text.strip()
            
        with st.spinner(f"🔍 Searching Wikipedia for '{search_topic}'..."):
            web_data = search_web(search_topic)
        # --------------------------------
        
        # 3. Construct the Prompt for Gemini
        prompt = f"""
        You are an expert Research Assistant. 
        Answer the user's question using ONLY the factual data provided below.
        If the data says "No Wikipedia page found" or "Topic is too broad", tell the user you couldn't find the exact information and ask them to clarify.
        
        DATA:
        {web_data}
        
        USER QUESTION: {user_query}
        """
        
        # Thinking Phase
        with st.spinner("🧠 Thinking..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Gemini Error: {e}")