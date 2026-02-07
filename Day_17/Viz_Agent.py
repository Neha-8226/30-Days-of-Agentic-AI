import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- THE FIX: Smart Model Selector ---
def get_model():
    try:
        # Loop through available models to find a working "Flash" model
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if "flash" in m.name and "gemini" in m.name:
                    return m.name
    except:
        pass
    return "models/gemini-1.5-flash" # Fallback

MODEL_NAME = get_model()
print(f"🤖 Using Model: {MODEL_NAME}") # It will print which model it found
model = genai.GenerativeModel(MODEL_NAME)

# 2. Load Data
# Make sure 'sales_data.csv' is in the SAME folder where you run this script
csv_path = "sales_data.csv"

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    print("❌ Error: 'sales_data.csv' not found. Please create the file first!")
    exit()

def visualize_data(user_objective):
    print(f"\n🎨 Viz Agent: Planning chart for '{user_objective}'...")
    
    # We give the AI the column info so it knows what to plot
    columns = list(df.columns)
    data_sample = df.head(3).to_string()
    
    # 3. The "Data Scientist" Prompt
    prompt = f"""
    You are a Python Data Visualization Expert.
    Dataset Columns: {columns}
    Sample Data:
    {data_sample}
    
    User Objective: "{user_objective}"
    
    Task:
    Write Python code using 'matplotlib' and 'seaborn' to visualize this.
    1. Create a figure.
    2. Plot the data (Choose the best chart type: Bar, Line, Scatter, etc.).
    3. Add title and labels.
    4. Save the plot as 'chart_output.png'.
    
    Output ONLY the raw Python code. No markdown.
    """
    
    try:
        response = model.generate_content(prompt)
        code = response.text.replace("```python", "").replace("```", "").strip()
        
        print(f"   🐍 Generated Plotting Code...")
        
        # 4. Execute the Code
        # We pass 'df', 'plt', and 'sns' so the code can use them
        exec(code, {"df": df, "plt": plt, "sns": sns})
        
        print("   ✅ Chart saved as 'chart_output.png'!")
        print("   -> Go check your folder to see the image!")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

# --- RUN IT ---
print("🤖 Auto-Visualizer Ready.")
goal = input("What do you want to see? (e.g., 'Sales by Region', 'Sales over Time'): ")
visualize_data(goal)