import os
import pyttsx3
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Setup Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- SMART MODEL SELECTOR (Copied from Day 12) ---
def get_available_model():
    """Asks Google which models are available and picks the best one."""
    print("🔎 Scanning for available models...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if "gemini" in m.name:
                    print(f"   ✅ Found working model: {m.name}")
                    return m.name
    except:
        pass
    return "models/gemini-1.5-flash" # Fallback

# Automatically set the model
MODEL_NAME = get_available_model()
model = genai.GenerativeModel(MODEL_NAME)
chat = model.start_chat(history=[])

# 2. Setup the "Mouth" (Text-to-Speech)
engine = pyttsx3.init()

# Optional: Change voice (0 = Male, 1 = Female usually)
try:
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id) # Try 0 or 1
except:
    pass 

def speak(text):
    """The agent speaks the text aloud."""
    print(f"🤖 Agent: {text}")
    engine.say(text)
    engine.runAndWait()

# --- MAIN LOOP ---
speak(f"System Online using {MODEL_NAME}. I am ready to talk.")
print("(Type your message below and press Enter)")

while True:
    # 1. Input (Keyboard)
    user_input = input("\nYou: ")
    
    if user_input.lower() in ["exit", "quit", "stop"]:
        speak("Shutting down. Goodbye, Neha.")
        break
        
    # 2. Think (Gemini)
    try:
        response = chat.send_message(user_input + " (Keep your answer short and spoken naturally.)")
        
        # 3. Speak
        speak(response.text)
    except Exception as e:
        print(f"Error: {e}")