from src.chatbot.intent_classifier import classify_intent, Intent
from src.chatbot.execution_controller import execute_pipeline_step

def run_step_2():
    print("\n🧪 Step 2 – Controlled Execution Test\n")

    user_input = input("User: ")

    intent = classify_intent(user_input)
    print(f"\n🔎 Detected Intent: {intent.value}")

    if intent == Intent.UNKNOWN:
        print("\n❓ Unable to determine intent.")
        return

    # Controlled follow-up
    confirm = input("\n👉 Do you want to proceed? (yes/no): ").strip().lower()

    if confirm in ("yes", "y"):
        execute_pipeline_step(intent)
    else:
        print("\n🛑 Execution cancelled by user.")

if __name__ == "__main__":
    run_step_2()
