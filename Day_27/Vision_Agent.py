import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
from dotenv import load_dotenv

# 1. Setup & Security
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("🚨 API Key not found! Check your .env file.")
    st.stop()

genai.configure(api_key=api_key)

# 2. Universal Model Selector (To prevent 404/429 errors!)
@st.cache_resource
def get_working_model():
    try:
        my_models = [m.name for m in genai.list_models() if "generateContent" in m.supported_generation_methods]
        best_model = my_models[0] 
        for m in my_models:
            if "flash" in m: return m
        return best_model
    except Exception:
        return "models/gemini-1.5-flash"

model = genai.GenerativeModel(get_working_model())

# 3. Streamlit UI Setup
st.set_page_config(page_title="AI Brand Marketer", page_icon="📸", layout="wide")
st.title("📸 Autonomous Vision-Marketing Agent")
st.write("Upload a product design, and the AI will analyze the aesthetic to generate a multi-platform marketing campaign.")

# 4. Image Upload & Processing
uploaded_file = st.file_uploader("Upload a product image (e.g., T-shirt design, merch)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open and display the image using PIL
    col1, col2 = st.columns([1, 1])
    
    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Design", use_container_width=True)
        analyze_button = st.button("Generate Marketing Campaign 🚀")
    
    if analyze_button:
        with col2:
            with st.spinner("Analyzing visual aesthetic and writing copy..."):
                try:
                    # The prompt orchestrating the Agent's persona
                    prompt = """
                    You are an expert streetwear marketing agent. 
                    Analyze this product image carefully. Pay attention to the art style, the vibe, and any visible text or themes.
                    
                    Based on the image, generate the following:
                    
                    1. **Instagram Caption:** Engaging, edgy, using relevant streetwear/anime hashtags.
                    2. **Twitter/X Post:** Short, punchy, designed for high engagement.
                    3. **Shopify Product Description:** A compelling paragraph highlighting the aesthetic, followed by 3-4 bullet points on why this piece is a must-have.
                    
                    Format the output clearly with headers.
                    """
                    
                    # Gemini takes a list containing BOTH the text prompt and the PIL image!
                    response = model.generate_content([prompt, image])
                    
                    st.success("✅ Campaign Generated!")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Error generating content: {e}")