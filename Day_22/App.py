import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Setup
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

# 2. The Web Interface
st.title("🤖 My First AI App")
st.write("Welcome to the Agentic AI interface. Ask me anything!")

# Create a text box for user input
user_input = st.text_input("Type your question here:", placeholder="e.g., Explain Quantum Physics")

# Create a button
if st.button("Generate Answer"):
    if user_input:
        with st.spinner("Thinking..."):  # Show a loading spinner
            try:
                # Call Gemini
                response = model.generate_content(user_input)
                
                # Display success message
                st.success("Here is your answer:")
                
                # Display the result
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question first!")

# Sidebar for extra options
with st.sidebar:
    st.header("Settings")
    st.write(f"Using Model: `{MODEL_NAME}`")
    st.info("Built during the 30-Day Agentic AI Challenge!")