import streamlit as st
from agents import run_agent
import streamlit.components.v1 as components

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
