import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

st.title("🕵️‍♀️ API Model Debugger")

# 2. List Models
st.write("Asking Google for your available models...")

try:
    found_models = []
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            st.code(f"Model Name: {m.name}") # Print the EXACT string to the screen
            found_models.append(m.name)
            
    if not found_models:
        st.error("🚨 No models found! Your API Key might be invalid or has no quota.")
    else:
        st.success(f"✅ Found {len(found_models)} models!")

except Exception as e:
    st.error(f"🚨 Error connecting to Google: {e}")