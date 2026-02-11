import os
import google.generativeai as genai
from gtts import gTTS
import time
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

# --- TOOL: THE MOUTH (Speak) ---
def speak(text):
    print(f"   🔊 Speaking...")
    try:
        # Convert text to audio
        tts = gTTS(text=text, lang='en', slow=False)
        filename = "reply.mp3"
        
        # Remove old file if it exists
        if os.path.exists(filename):
            os.remove(filename)
            
        tts.save(filename)
        
        # Play audio (Windows)
        os.system(f"start {filename}")
        
        # Wait a bit so the program doesn't close while talking
        time.sleep(len(text) // 10 + 2) 
        
    except Exception as e:
        print(f"   ❌ Audio Error: {e}")

# --- MAIN LOOP ---
def talking_ai():
    print(f"\n🗣️ Talking Agent ({MODEL_NAME}) Online.")
    print("   (Type your question, and I will SPEAK the answer!)")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        # Think (Gemini)
        try:
            response = model.generate_content(user_input)
            ai_reply = response.text.strip()
            
            # Print text
            print(f"🤖 AI: {ai_reply}")
            
            # Speak Audio
            speak(ai_reply)
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    talking_ai()