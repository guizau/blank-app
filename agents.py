from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

AGENT_SYSTEM_PROMPTS = {
    "Product": "You recommend the most suitable product or feature for the customer.",
    "Service": "You recommend a support or value-added service to help the customer.",
    "Insight": "You generate a helpful insight or trend relevant to the customer's context.",
    "Timing": "You determine the best time to engage this customer for impact.",
    "Content": "You write a short, clear message the customer will receive.",
    "Channel": "You choose the best communication channel for this customer."
}

# Output format prompt
STRUCTURE_INSTRUCTION = """
Return only a valid JSON object with the following fields:
- "agent": string (one of: Product, Service, Insight, Timing, Content, Channel)
- "decision": short text
- "why": short explanation
- "estimated_impact": brief business impact
- "confidence": integer from 1 (low) to 10 (high)
"""

def run_agent(agent_type: str, signals: dict) -> dict:
    model = ChatOpenAI(temperature=0.5, model_name="gpt-4")

    prompt = ChatPromptTemplate.from_messages([
        ("system", f"""
You are the {agent_type} Agent. {AGENT_SYSTEM_PROMPTS[agent_type]}
{STRUCTURE_INSTRUCTION}
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

    try:
        response = model(prompt.format_messages())
        return eval(response.content)  # Safe if you're only running this for demo/testing
    except Exception as e:
        return {
            "agent": agent_type,
            "decision": "N/A",
            "why": f"Error: {str(e)}",
            "estimated_impact": "N/A",
            "confidence": 0
        }
