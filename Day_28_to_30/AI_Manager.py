import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Setup & Security
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("🚨 API Key not found! Check your .env file.")
    st.stop()

genai.configure(api_key=api_key)

# 2. Kuro Republic Backend Systems (Dummy Data)
INVENTORY = {
    "gojo oversize tee": {"stock": 15, "price": "₹999"},
    "akatsuki hoodie": {"stock": 0, "price": "₹1499"},
    "sukuna sweatpants": {"stock": 5, "price": "₹1299"}
}

# 3. Defining the AI Tools
def check_inventory(product_name: str) -> str:
    """Checks the current stock and price of a specific Kuro Republic clothing item."""
    product_name = product_name.lower()
    for key, data in INVENTORY.items():
        if key in product_name:
            if data["stock"] > 0:
                return f"Yes, we have {data['stock']} units of the {key.title()} in stock! The price is {data['price']}."
            else:
                return f"Sorry, the {key.title()} is currently out of stock. We will restock soon!"
    return "I couldn't find that exact item in our current drop. Could you specify the design?"

def apply_discount_code(customer_loyalty_status: str) -> str:
    """Generates a 10% discount code for loyal returning customers."""
    if "loyal" in customer_loyalty_status.lower() or "returning" in customer_loyalty_status.lower():
        return "Awesome! Here is a 10% off code for being a great supporter of Kuro Republic: KUROFAM10"
    return "Discounts are currently reserved for our mailing list subscribers. Be sure to sign up!"

def escalate_to_founder(issue_type: str, customer_message: str) -> str:
    """Escalates complex issues (refunds, bulk orders, partnerships) to the human founders (Neha, Yug, Tejas)."""
    if "bulk" in issue_type.lower() or "partner" in issue_type.lower():
        assigned_to = "Yug"
    elif "finance" in issue_type.lower() or "refund" in issue_type.lower():
        assigned_to = "Tejas"
    else:
        assigned_to = "Neha" # Default operations escalation
        
    return f"Ticket created for: '{customer_message}'. This has been escalated to {assigned_to}. They will reach out to you within 24 hours."

# 4. Universal Model Selector & Agent Logic
@st.cache_resource
def get_working_model():
    try:
        # 1. Get all models that can generate content
        my_models = [m.name for m in genai.list_models() if "generateContent" in m.supported_generation_methods]
        
        # 2. Filter out gemini-3-pro since it has 0 free tier quota
        safe_models = [m for m in my_models if "3-pro" not in m]
        
        # 3. Prioritize 'flash' models as they have the highest free limits
        for m in safe_models:
            if "flash" in m:
                return m
                
        # 4. Fallback to the first safe model available
        return safe_models[0] if safe_models else "models/gemini-1.5-pro"
    except Exception:
        return "models/gemini-1.5-pro"

@st.cache_resource
def get_kuro_agent():
    working_model_name = get_working_model()
    # Print it to the terminal so we know exactly what we are using!
    print(f"🚀 Booting Agent with model: {working_model_name}") 
    
    return genai.GenerativeModel(
        model_name=working_model_name,
        tools=[check_inventory, apply_discount_code, escalate_to_founder],
        system_instruction="""
        You are the primary AI Store Manager for Kuro Republic, a premium anime streetwear brand.
        Your vibe is cool, helpful, and concise. 
        - If they ask about stock or prices, ALWAYS use the check_inventory tool.
        - If they mention they are a returning/loyal customer looking for a deal, use the apply_discount_code tool.
        - If they are angry, want a refund, or want to buy wholesale, use the escalate_to_founder tool.
        - If they just say hi or ask a general question about anime or streetwear, chat normally.
        """
    )

agent = get_kuro_agent()

# 5. Streamlit UI & Memory Integration
st.set_page_config(page_title="Kuro AI Manager", page_icon="🥷", layout="centered")
st.title("🥷 Kuro Republic: AI Store Manager")
st.write("Welcome to the Kuro Republic support portal. How can I help you gear up today?")

# Initialize persistent chat history
if "chat_session" not in st.session_state:
    st.session_state.chat_session = agent.start_chat(enable_automatic_function_calling=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input (Added unique key here!)
if prompt := st.chat_input("Ask about stock, discounts, or refunds...", key="kuro_chat_input"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Manager is checking the system..."):
            try:
                response = st.session_state.chat_session.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")