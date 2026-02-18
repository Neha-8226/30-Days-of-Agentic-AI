import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("🚨 API Key not found! Check your .env file.")
    st.stop()

genai.configure(api_key=api_key)

# 2. THE UNIVERSAL SELECTOR
# We stop guessing. We ask the API: "What DO I have?" and use the first one.
def get_working_model():
    try:
        my_models = []
        for m in genai.list_models():
            if "generateContent" in m.supported_generation_methods:
                my_models.append(m.name)
        
        if not my_models:
            st.error("🚨 Your API Key has access to ZERO models. This is an account issue.")
            st.stop()
            
        # We prefer a 'flash' model if available, otherwise take the first one.
        # This logic adapts to YOUR specific list.
        best_model = my_models[0] 
        for m in my_models:
            if "flash" in m:
                best_model = m
                break
                
        return best_model
    except Exception as e:
        st.error(f"Error listing models: {e}")
        st.stop()

# 3. CONFIGURE THE BOT
MODEL_NAME = get_working_model()
model = genai.GenerativeModel(MODEL_NAME)

st.set_page_config(page_title="Memory Bot", page_icon="🧠")
st.title("🧠 The Chatbot with Memory")
st.success(f"✅ Auto-Connected to: `{MODEL_NAME}`") # This tells us the truth!

# --- PHASE 1: INITIALIZE MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your AI Assistant. I remember our conversation. Try me!"}
    ]

# --- PHASE 2: DISPLAY HISTORY ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- PHASE 3: HANDLE NEW INPUT ---
user_input = st.chat_input("Type your message here...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    gemini_history = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg["content"]]})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                chat = model.start_chat(history=gemini_history)
                response = chat.send_message(user_input)
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")