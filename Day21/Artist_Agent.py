import os
import google.generativeai as genai
import requests
import time
from dotenv import load_dotenv

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
    return "models/geminni-1.5-flash"

MODEL_NAME = get_model()
model = genai.GenerativeModel(MODEL_NAME)

#2 Tool: Image Generator (Pollinations API)
def generate_image(prompt):
    print(f"\n🎨 Generating Image for: '{prompt}'...")
    print("  (This might take 5-10 seconds)...")
    
    try:
        # Create a unique filename based on time
        timestamp = int(time.time())
        filename = f"image_{timestamp}.jpg"
        
        # The API URL (We encode the prompt into the URL)
        # We use 'lux' or 'flux' model for high quality
        url = f"https://image.pollinations.ai/prompt/{prompt}?model=flux&width=1024&height=1024&nologo=true"
        
        # Download the image
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"  ✅ Image saves as: {filename}")
            
            # Open the image automatically
            if os.name == 'nt':  # Windows
                os.startfile(filename)
            else: # Mac/Linux
                os.system(f"open {filename}" if os.name == 'posix' else f"xdg-open {filename}")
                
            return filename
        else:
            print("  ❌ Failed to fetch image from API.")
            return None
        
    except Exception as e:
        print(f" ❌ Error: {e}")
        return None
    
#3 The Agent Logic (Prompt Enhancer)
def artist_agent():
    print(f"\n🎨 AI Artist Agnet ({MODEL_NAME}) Initialized.")
    print(" Describe what you want to see (e.g., 'A cat in a space').")
    print(" (Type 'exit' to quit)")
    
    while True:
        user_input = input("\nYour Idea: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        
        print("  ✨ Refining propmpt with Gemini...")
        
        # We ask Gemini to take your simple idea and make it "Artistic"
        # Stable Diffusion works best with detailed, descriptive prompts.
        enhancement_prompt = f"""
        You are an expert AI Art Prompter.
        Take this simple user idea: "{user_input}"
        
        Rewrite it into a highly detailed, professional image generation prompt.
        Include keywords for: Lighting, Style, Resolution, Camera Angle, and Mood.
        
        Output ONLY the raw prompt text. No "Here is the prompt:" prefix.
        """
        
        try:
            #1 Enhance the prompt
            response = model.generate_content(enhancement_prompt)
            better_prompt = response.text.strip()
            print(f" 🤖 Enhanced Prompt: {better_prompt}")
            
            #2 Generate the image
            generate_image(better_prompt)
            
        except Exception as e:
            print(f" ❌ Error: {e}")

if __name__ == "__main__":
    artist_agent()