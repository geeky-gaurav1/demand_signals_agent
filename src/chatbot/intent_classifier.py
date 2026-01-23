import os
from enum import Enum
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

# -------------------------------
# Intent Enum
# -------------------------------
class Intent(Enum):
    SALES_HISTORY = "SALES_HISTORY"
    CONSOLIDATED_INSIGHTS = "CONSOLIDATED_INSIGHTS"
    CLEANUP = "CLEANUP"
    GOLD_SIGNAL = "GOLD_SIGNAL"
    UNKNOWN = "UNKNOWN"

# -------------------------------
# Azure AI Client Setup
# -------------------------------
tenant_id = os.getenv("TENANT_ID")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
endpoint = os.getenv("PROJECT_ENDPOINT")
model_name = os.getenv("AZURE_AI_MODEL")

if not all([tenant_id, client_id, client_secret, endpoint, model_name]):
    raise ValueError("Missing required environment variables")

credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)

project = AIProjectClient(
    credential=credential,
    endpoint=endpoint
)

# -------------------------------
# Create Intent Classifier Agent
# -------------------------------
agent = project.agents.create_agent(
    model=model_name,
    name="intent_classifier_agent",
    instructions="""
You are an intent classifier for a data pipeline chatbot.

Valid intents:
- SALES_HISTORY: user wants sales overview, monthly sales, POS or finance sales history
- CONSOLIDATED_INSIGHTS: user wants combined insights across datasets
- CLEANUP: user wants data cleaning or validation
- GOLD_SIGNAL: user wants demand signals or severity insights
- UNKNOWN: intent is unclear

Return ONLY the intent name. No explanations.
"""
)

# -------------------------------
# Intent Classification Function
# -------------------------------
def classify_intent(user_input: str) -> Intent:

    thread = project.agents.threads.create()

    project.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    run = project.agents.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id
    )

    messages = project.agents.messages.list(thread_id=thread.id)

    for msg in messages:
        if msg.role == "assistant":
            intent_text = msg.content[0].text.value.strip()
            return Intent(intent_text) if intent_text in Intent._value2member_map_ else Intent.UNKNOWN


    return Intent.UNKNOWN
