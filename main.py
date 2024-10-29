from agents.agent import LLMAgent
from dotenv import load_dotenv
import os

def main():
    load_dotenv()

    api_key = os.getenv("TOGETHER_API_KEY")

    if not api_key:
        print("Error: API key not found. Please set it in the .env file.")
        return
     
    agent = LLMAgent(api_key)

    print("Welcome to the LLMAgent CLI!")
    conversation_id = "user_conversation"

    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        response = agent.process_message(user_input, conversation_id)
        print(f"Agent: {response}\n")

if __name__ == "__main__":
    main()
