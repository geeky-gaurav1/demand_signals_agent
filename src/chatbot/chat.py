from src.chatbot.intent_classifier import classify_intent
from src.chatbot.action_router import route_action

def start_chat():
    print("Demand Signals Assistant started.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        intent = classify_intent(user_input)
        route_action(intent)

if __name__ == "__main__":
    start_chat()
