import os
import google.generativeai as genai
from dotenv import load_dotenv
from pypdf import PdfReader

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

#2 The PDF Reader Tool
def read_pdf(file_path):
    """Extracts text from a PDF file."""
    print(f"  📖 Reading PDF: {file_path}...")
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f" ❌ Error reading PDF: {e}")
        return None
    
#3 The Agent Logic
def chat_with_pdf():
    pdf_path = "Document.pdf"
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print("❌ Error: 'Document.pdf' not found in this folder.")
        print("  -> Please add a PDF file and rename it to 'Document.pdf'")
        return
    
    # Load Knowledge Base
    print(f"\n📚 PDF Agent ({MODEL_NAME}) Initialized.")
    pdf_content = read_pdf(pdf_path)
    
    if not pdf_content:
        return
    
    print(f" ✅ Loaded {len(pdf_content)} characters of text.")
    print("  (Agent is ready! Ask questions about the document.)")
    print("-"*40)
    
    # Chat Loop
    while True:
        user_query = input("\n")
        if user_query.lower() in ["exit", "quit", "bye"]:
            print("👋 Closing the book")
            break
        
        #4 Construct the Prompt (RAG - Retrieval Augmented Generation)
        # We sandwich the user's question with the PDF content
        prompt = f"""
        You are a helpful assistant.
        Answer the user's question based strictly on the document text provided below.
        If the answer is not in the text, say "I cannot find that information in the document."
        
        DOCUMENT TEXT:
        {pdf_content}
        
        USER QUESTION:
        {user_query} 
        """
        
        try:
            response = model.generate_content(prompt)
            print(f"🤖 Agent: {response.text.strip()}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
if __name__ == "__main__":
    chat_with_pdf()
            
