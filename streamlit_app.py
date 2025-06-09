import os
import streamlit as st

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Moena AI Decisioning Demo", layout="wide")

st.title("🧠 Moena AI Decisioning Demo")

# 1. Collect customer signal inputs
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

# 2. Simulated agent logic
def run_agents(signals):
    return {
        "Product Agent": {
            "decision": "Offer Working Capital Loan",
            "rationale": "Lucas browsed loan pages and it's peak season for bakeries."
        },
        "Service Agent": {
            "decision": "Assign Loan Advisor Callback",
            "rationale": "Customer clicked on 'contact advisor' recently."
        },
        "Insight Agent": {
            "decision": "Bakery revenue typically increases 20% during holidays with new POS systems.",
            "rationale": "Lucas recently added a POS system and is entering high season."
        },
        "Timing Agent": {
            "decision": "Send message at 2:00 PM",
            "rationale": "Historical engagement is highest in mid-afternoon."
        },
        "Content Agent": {
            "decision": "“We’ve unlocked a loan tailored to help your bakery grow this season.”",
            "rationale": "Direct and benefit-driven messaging fits Lucas's profile."
        },
        "Channel Agent": {
            "decision": "Use WhatsApp",
            "rationale": "Lucas prefers informal, fast channels and doesn't respond to email."
        }
    }

# 3. Display agent outputs
st.subheader("🤖 Agent Decisions")
agent_results = run_agents(signals)

cols = st.columns(3)
for i, (agent, output) in enumerate(agent_results.items()):
    with cols[i % 3]:
        st.markdown(f"**{agent}**")
        st.success(f"Decision: {output['decision']}")
        st.caption(f"Why: {output['rationale']}")

# 4. Compose final message
st.subheader("📬 Final Output to Customer")
st.info(f"""
At {agent_results['Timing Agent']['decision']} on {agent_results['Channel Agent']['decision']}, 
Lucas receives:
> {agent_results['Content Agent']['decision']}
""")
