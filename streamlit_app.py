import os
import streamlit as st
from agents import run_agent
from crud import (
    create_campaign, get_campaigns, update_campaign, delete_campaign,
    create_message, get_campaign_messages, update_message, delete_message,
    get_db
)

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Moena AI Demo", layout="wide")
st.title("🧠 Moena AI Multi-Agent Demo")

# Initialize session state for database
if 'db' not in st.session_state:
    st.session_state.db = next(get_db())

# Campaign Management Section
st.header("📢 Campaign Management")

# Create Campaign
with st.expander("Create New Campaign"):
    with st.form("create_campaign_form"):
        campaign_name = st.text_input("Campaign Name")
        campaign_description = st.text_area("Campaign Description")
        submitted = st.form_submit_button("Create Campaign")
        if submitted and campaign_name:
            create_campaign(st.session_state.db, campaign_name, campaign_description)
            st.success("Campaign created successfully!")

# List and Manage Campaigns
st.subheader("Your Campaigns")
campaigns = get_campaigns(st.session_state.db)

for campaign in campaigns:
    with st.expander(f"📋 {campaign.name}"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**Description:** {campaign.description or 'No description'}")
            st.write(f"**Created:** {campaign.created_at.strftime('%Y-%m-%d %H:%M')}")
            
            # Messages for this campaign
            st.write("**Messages:**")
            messages = get_campaign_messages(st.session_state.db, campaign.id)
            for message in messages:
                st.write(f"- {message.content}")
        
        with col2:
            # Add new message
            with st.form(f"add_message_form_{campaign.id}"):
                message_content = st.text_area("Message Content")
                if st.form_submit_button("Add Message"):
                    if message_content:
                        create_message(
                            st.session_state.db,
                            campaign.id,
                            message_content
                        )
                        st.success("Message added!")
                        st.rerun()
            
            # Delete campaign
            if st.button("Delete Campaign", key=f"delete_{campaign.id}"):
                delete_campaign(st.session_state.db, campaign.id)
                st.success("Campaign deleted!")
                st.rerun()

# Original Customer Signals Section
st.header("👥 Customer Signals")
name = st.text_input("Name", value="Lucas Andrade")
business_type = st.selectbox("Business Type", ["Bakery", "Retail", "Beauty", "Services"])
season = st.selectbox("Season", ["Holiday", "Back to School", "Low Season"])
channel_pref = st.selectbox("Preferred Channel", ["WhatsApp", "Email", "SMS", "Push Notification"])
cash_reserve = st.slider("Cash Reserve (BRL)", 0, 20000, 7800)
monthly_revenue = st.slider("Monthly Revenue (BRL)", 5000, 50000, 32000)

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
AGENTS = ["Product", "Timing", "Content", "Channel"]

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

