import os
import streamlit as st
from agents import run_agent

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Moena AI Demo", layout="wide")
st.title("🧠 Moena AI Multi-Agent Demo")

# Sidebar – Customer Signals
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

# Run all agents
AGENTS = ["Product", "Service", "Insight", "Timing", "Content", "Channel"]

if st.button("Run All Agents"):
    with st.spinner("Agents making decisions..."):
        agent_outputs = [run_agent(agent, signals) for agent in AGENTS]

    st.subheader("🤖 Agent Decisions")

    cols = st.columns(3)
    for i, agent_data in enumerate(agent_outputs):
        with cols[i % 3]:
            st.markdown(f"### `{agent_data['agent']} Agent`")
            st.markdown(f"**Decision:** {agent_data['decision']}")
            st.markdown(f"**Why:** {agent_data['why']}")
            st.markdown(f"**Impact:** {agent_data['estimated_impact']}")
            st.progress(agent_data.get("confidence", 0) / 10)

    # Final output card
    st.subheader("📬 Final Composed Message")
    content = next((a for a in agent_outputs if a['agent'] == "Content"), None)
    timing = next((a for a in agent_outputs if a['agent'] == "Timing"), None)
    channel = next((a for a in agent_outputs if a['agent'] == "Channel"), None)

    if content and timing and channel:
        st.markdown("#### Personalized Output")
        st.info(f"""
At **{timing['decision']}**, via **{channel['decision']}**,  
{signals['name']} receives:  
> {content['decision']}
        """)

