import os 
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

#1 Setup
load_dotenv()
genai.configure(api_key = os.getenv("GEMINI_API_KEY"))

# We need a smart model for coding 
def get_vision_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if "flash" in m.name and "gemini" in m.name:
                    return m.name
    except:
        pass 
    return "models/gemini-1.5-flash"

MODEL_NAME = get_vision_model()
model = genai.GenerativeModel(MODEL_NAME)

#2 Load the design (Screenshot or Sketch)
image_path = "Design_Mockup.png"

print(f"\n🎨 UI-to-Code Agent Online({MODEL_NAME})")

if os.path.exists(image_path):
    img = Image.open(image_path)
    print(f"  (Analyzing design: {image_path}...)")
    
    #3 The "Frontend Engineer" Prompt
    prompt = """
    You are an expert Frontend Developer.
    Look at this image.
    Write the HTML and CSS to recreate this UI as closely as possible.
    
    Rules:
    - Use modern HTML5 and embedded CSS (in <style> tags).
    - Make it responsive and pretty.
    - Output ONLY the raw HTML code (no markdown "```", no explainations).    
    """
    
    print("  (Writing code...)")
    response = model.generate_content([prompt, img])
    
    #4 Clean and Save the output
    html_code = response.text.replace("```html", "").replace("```", "")
    
    output_file = "website.html"
    with open(output_file, "w", encoding = "utf-8") as f:
        f.write(html_code)
        
    print(f"\n✅ Success! Website generated: {output_file}")
    print("  -> Open 'website.html' in your browser to see the result!")

else:
    print("❌ Error: Please put a 'Design_Mockup.png' in the folder.") 
    