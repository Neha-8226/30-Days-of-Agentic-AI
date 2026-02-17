import streamlit as st
import os
import google.generativeai as genai
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# 1. Setup & Security
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("🚨 API Key not found! Please check your .env file.")
    st.stop()

genai.configure(api_key=api_key)

# Smart model selector for text
@st.cache_resource
def get_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and "flash" in m.name:
                return m.name
    except Exception:
        pass
    return "gemini-1.5-flash-latest"

model = genai.GenerativeModel(get_model())

# Function to extract text from the PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# 2. UI Configuration
st.set_page_config(page_title="Document AI", page_icon="📄")
st.title("📄 PDF Research Assistant")
st.write("Upload a PDF document and ask me anything about it!")

# 3. File Upload & Processing
uploaded_file = st.file_uploader("Upload your PDF...", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extracting text from document..."):
        # Extract the text and store it in Streamlit's session state
        document_text = extract_text_from_pdf(uploaded_file)
        st.success("✅ Document processed successfully!")
        
        with st.expander("👀 Peek at the extracted text"):
            st.write(document_text[:1000] + "... [Text truncated for display]")

    # 4. Chat Interface
    user_query = st.chat_input("E.g., Summarize this document, or What are the key takeaways?")
    
    if user_query:
        with st.chat_message("user"):
            st.write(user_query)
            
        with st.chat_message("assistant"):
            with st.spinner("🧠 Analyzing document..."):
                try:
                    # Inject the document text into the prompt
                    prompt = f"""
                    You are a helpful Research Assistant. 
                    Answer the user's question using ONLY the provided document text below.
                    If the answer is not in the document, say "I cannot find that in the document."
                    
                    DOCUMENT TEXT:
                    {document_text}
                    
                    USER QUESTION: {user_query}
                    """
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Generation Error: {e}")