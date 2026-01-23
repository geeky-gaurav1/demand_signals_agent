import subprocess
from src.chatbot.intents import Intent

def route_action(intent: Intent):
    if intent == Intent.SALES_HISTORY:
        subprocess.run(["python", "src/data_generation/run_all.py"])

    elif intent == Intent.CONSOLIDATED_INSIGHTS:
        subprocess.run(["python", "src/data_generation/consolidation.py"])

    elif intent == Intent.CLEANUP:
        subprocess.run(["python", "src/silver_layer/cleanup.py"])

    elif intent == Intent.GOLD_SIGNAL:
        subprocess.run(["python", "src/gold_layer/demand_signal_generator.py"])

    else:
        print("Sorry, I couldn’t understand the request.")
