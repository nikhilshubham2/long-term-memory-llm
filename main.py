from src.memory_manager import MemoryManager
from src.conversation_agent import ConversationAgent

def main():
    memory = MemoryManager()
    agent = ConversationAgent(memory_manager=memory)
    print("Chat with the Long-Term Memory Agent!")
    print("Type 'exit' to end the conversation.")
    print("-" * 50)
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Agent: Goodbye!")
            break
        response = agent.handle_message(user_input)
        print(f"Agent: {response}")

if __name__ == "__main__":
    main()