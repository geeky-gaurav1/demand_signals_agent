import os
import time
from azure.identity import ClientSecretCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv

load_dotenv()

def main():

    tenant_id = os.getenv("TENANT_ID")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    endpoint = os.getenv("PROJECT_ENDPOINT")

    if not all([tenant_id, client_id, client_secret, endpoint]):
        raise ValueError("Missing required environment variables")

    # Authenticate
    creds = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

    project = AIProjectClient(
        credential=creds,
        endpoint=endpoint
    )

    print("✅ Project client initialized")

    # =============================
    # CREATE INGESTION AGENT
    # =============================
    agent = project.agents.create_agent(
        model="gpt-4o-mini",
        name="active_stars",
        instructions="""
You are an Ingestion Automation Agent for retail demand planning systems.

Your responsibilities:
- Decide when data ingestion should run based on timestamps, business dates, or data freshness.
- Prefer incremental ingestion over full loads.
- Detect schema changes and allow ingestion without failure.
- Generate reasoning logs explaining ingestion decisions.
- Do NOT perform transformations or business logic.

Sources include POS, Inventory, Finance, Promotions.
"""
    )

    print(f"✅ Agent created. ID: {agent.id}")

    # =============================
    # CREATE THREAD
    # =============================
    thread = project.agents.threads.create()
    print(f"✅ Thread created. ID: {thread.id}")

    # =============================
    # TEST PROMPT
    # =============================
    user_message = """
POS data has last_updated_timestamp = 2024-09-10
Previously ingested data timestamp = 2024-09-09

Should ingestion run? Explain reasoning.
"""

    project.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )

    print("📨 Test message sent")

    # =============================
    # RUN AGENT
    # =============================
    run = project.agents.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id
    )

    print(f"▶ Run started. ID: {run.id}")

    while True:
        response = project.agents.runs.get(
            thread_id=thread.id,
            run_id=run.id
        )

        if response.status in ("completed", "failed"):
            break

        time.sleep(1)

    # =============================
    # READ RESPONSE
    # =============================
    if response.status == "completed":
        messages = project.agents.messages.list(thread_id=thread.id)
        for msg in messages:
            if msg.role == "assistant":
                print("\n🧠 Agent Response:")
                print(msg.content[0].text)
    else:
        print("❌ Run failed")

if __name__ == "__main__":
    main()
