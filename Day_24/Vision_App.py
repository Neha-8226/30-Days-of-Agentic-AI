import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# 1. Setup & Security Check
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. UI Configuration
st.set_page_config(page_title="AI Vision Agent", page_icon="👁️")
st.title("👁️ Multimodal Vision Agent")

# If the API key is missing, stop the app and show a friendly error!
if not api_key:
    st.error("🚨 API Key not found! Please make sure you copied your .env file into the Day_24 folder.")
    st.stop()

genai.configure(api_key=api_key)

# 3. The BULLETPROOF Model Selector
@st.cache_resource
def get_vision_model():
    """Scans your account and picks the best available vision model."""
    try:
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        # Look for 1.5 flash first (Best)
        for name in available_models:
            if "1.5" in name and "flash" in name:
                return name
        # Look for older vision model (Fallback)
        for name in available_models:
            if "vision" in name:
                return name
                
        # Return whatever is available if the above fails
        if available_models:
            return available_models[0]
            
    except Exception as e:
        st.error(f"Error connecting to Google: {e}")
        st.stop()

MODEL_NAME = get_vision_model()
model = genai.GenerativeModel(MODEL_NAME)
st.success(f"✅ Successfully connected to: `{MODEL_NAME}`")

# 4. The Interface
st.write("Upload any image, and I will analyze it for you!")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Your Uploaded Image", use_container_width=True)
    
    user_prompt = st.chat_input("E.g., Describe the people in this photo...")
    
    if user_prompt:
        with st.chat_message("user"):
            st.write(user_prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("🧠 Analyzing pixels..."):
                try:
                    response = model.generate_content([user_prompt, image])
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Generation Error: {e}")