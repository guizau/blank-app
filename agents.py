from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

AGENT_SYSTEM_PROMPTS = {
    "Product": "You recommend the most suitable product or feature for the customer.",
    "Service": "You recommend a support or value-added service to help the customer.",
    "Insight": "You generate a helpful insight or trend relevant to the customer's context.",
    "Timing": "You determine the best time to engage this customer for impact.",
    "Content": "You write a short, clear, personalized message for the customer.",
    "Channel": "You choose the best communication channel for this customer."
}

def run_agent(agent_type: str, signals: dict) -> str:
    model = ChatOpenAI(temperature=0.5, model_name="gpt-4")

    prompt = ChatPromptTemplate.from_messages([
        ("system", f"You are the {agent_type} Agent. {AGENT_SYSTEM_PROMPTS[agent_type]} Use customer signals to inform your decision. Be concise."),
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
