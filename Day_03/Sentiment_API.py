from fastapi import FastAPI
from textblob import TextBlob
from pydantic import BaseModel

app = FastAPI()

# This defines the data structure for the incoming request
class TextInput(BaseModel):
    text: str
    
@app.get("/")
def home():
    # A simple status check to ensure your server is alive
    return {"status": "Day 3 API is Online!",
            "engine": "TextBlob Local"}
    
@app.post("/analyze")
def analyze_sentiment(input_data: TextInput):
    # This runs entirely on your local machine
    blob = TextBlob(input_data.text)
    polarity = blob.sentiment.polarity
    
    # Simple logic to label the sentiment
    if polarity > 0:
        label = "Positive"
    elif polarity < 0:
        label = "Negative"
    else:
        label = "Neutral"
        
    return {
        "text": input_data.text,
        "score": round(polarity, 2),
        "sentiment": label
    } 