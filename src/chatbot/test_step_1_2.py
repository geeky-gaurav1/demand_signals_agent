from src.chatbot.intent_classifier import classify_intent, Intent

def run_step_1_2():
    print("\n🧪 Step 1.2 – Controlled Follow-up Test\n")

    user_input = input("User: ")

    intent = classify_intent(user_input)

    print(f"\n🔎 Detected Intent: {intent.value}")

    if intent == Intent.SALES_HISTORY:
        print("\n📊 I can fetch sales history by generating POS, Inventory, and Finance datasets.")
        print("👉 Do you want deeper insights by consolidating datasets? (yes/no)")

    elif intent == Intent.CONSOLIDATED_INSIGHTS:
        print("\n📦 I can generate consolidated insights across datasets.")
        print("👉 Do you want me to proceed with data cleaning? (yes/no)")

    elif intent == Intent.CLEANUP:
        print("\n🧹 I can clean and validate the datasets.")
        print("👉 Do you want me to generate demand signals (gold layer)? (yes/no)")

    elif intent == Intent.GOLD_SIGNAL:
        print("\n🥇 I can generate demand signals and severity insights.")
        print("👉 Do you want me to proceed? (yes/no)")

    else:
        print("\n❓ I couldn’t clearly understand your request.")
        print("👉 Please rephrase or specify what you want to analyze.")

    print("\n🛑 Step 1.2 completed. No scripts executed.\n")

if __name__ == "__main__":
    run_step_1_2()
