import os
import google.generativeai as genai
import yfinance as yf
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from datetime import date

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

# --- TOOLS ---
def get_stock_data(ticker):
    """Fetches stock price and basic info from Yahoo Finance."""
    print(f" 📊 Fetching data for {ticker}... ")
    try:
        stock = yf.Ticker(ticker)
        # Get latest price history (last 5 days)
        hist = stock.history(period = "5d")
        current_price = hist['Close'].iloc[-1]
        
        # Calculate simple momentum (Is it going up or down?)
        start_price = hist['Close'].iloc[0]
        change = ((current_price - start_price) / start_price) * 100
        
        return {
            "current_price": round(current_price, 2),
            "5_day_change_percent": round(change, 2),
            "trend": "UP 📈" if change > 0 else "DOWN 📉"
        }
    except Exception as e:
        return f"Error fetching stock data: {e}"
    
def get_market_news(ticker):
    """Searches for the latest news about the company."""
    print(f"  📰 Reading news for {ticker}...")
    try:
        with DDGS() as ddgs:
            # Search for "Company Name Stock News"
            results = list(ddgs.text(f"{ticker} stock news", max_results = 3))
            summary = "\n".join([f"-{r['title']} ({r['href']})" for r in results])
            return summary
    except:
        return "No recent news found."
    
def finance_agent(ticker):
    print(f"\n💼 Wall Street Agent ({MODEL_NAME}) Initialized.")
    print(f"  Analyzing: {ticker.upper()}")
    
    #1 Gather Data (Tools)
    stock_data = get_stock_data(ticker)
    news_data = get_market_news(ticker)
    
    print("  🧠 Analyzing data... ")
    
    #2 Reason (Gemini)
    prompt = f"""
    You are a Senior Financial Analyst at a top investment bank.
    
    Analysis Target: {ticker}
    Date: {date.today()}
    
    ### MARKET DATA:
    {stock_data}
    
    ### LATEST NEWS HEADLINE:
    {stock_data}
    
    
    ### TASK:
    Write a brief investment memo.
    1. **Execution Summary**: What is the stock doing right now?
    2. **Key Drivers**: Based on the news, what is moving the price?
    3. **Recommendation**: Give a rating (Buy / Hold / Sell) with a reasoning.
    (Disclaimer: This is AI-generated financial analysis, not professional advice).
    """
    
    response = model.generate_content(prompt)
    
    print("\n" + "="*50)
    print(response.text)
    print("="*50)
    
# --- RUN IT ---
if __name__=="__main__":
    # Ask user for a ticker (e.g., AAPL, TSLA, RELIANCE.NS for India)
    user_ticker = input("\nEnter Stock Ticker (e.g., AAPL, NVDA, RELIANCE.NS, SBIN,NS): ")
    finance_agent(user_ticker)
        
    
    