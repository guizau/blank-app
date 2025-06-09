import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Load secret key from Streamlit Cloud
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Moena AI Demo", layout="wide")
st.title("🧠 Moena AI Decisioning Demo")

# Signals from user
st.sidebar.header("Customer Signals")
name = st.sidebar.text_input("Name", value="Lucas Andrade")
business_type = st.sidebar.selectbox("Business Type", ["Bakery", "Retail", "Beauty", "Services"])
season = st.sidebar.selectbox("Season", ["Holiday", "Back to School", "Low Season"])
channel_pref = st.sidebar.selectbox("Preferred Channel", ["WhatsApp", "Email", "SMS", "Push Notification"])
cash_reserve = st.sidebar.slider("Cash Reserve (BRL)", 0, 20000, 7800)
monthly_revenue = st.sidebar.slider("Monthly Revenue (BRL)", 5000, 50000, 32000)

signals = {
    "name": name,
    "business_type": business_type,
    "season": season,
    "channel_preference": channel_pref,
    "cash_reserve": cash_reserve,
    "monthly_revenue": monthly_revenue
}

st.subheader("📡 Ingested Customer Signals")
st.json(signals)

# LLM-powered Content Agent
def run_content_agent(signals: dict) -> str:
    model = ChatOpenAI(temperature=0.7, model_name="gpt-4")
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
You are a Content Personalization Agent.
Write a short, compelling message for the customer below.
Be direct and practical. Max 280 characters.
        """),
        ("human", f"""
Customer name: {signals['name']}
Business type: {signals['business_type']}
Season: {signals['season']}
Channel Preference: {signals['channel_preference']}
Cash Reserve: BRL {signals['cash_reserve']}
Monthly Revenue: BRL {signals['monthly_revenue']}
        """)
    ])
    return model(prompt.format_messages()).content.strip()

# Run agent
st.subheader("🤖 LLM-Powered Agent: Content")

if st.button("Generate Personalized Message"):
    with st.spinner("Thinking..."):
        message = run_content_agent(signals)
        st.success("Generated Message:")
        st.write(f"> {message}")
