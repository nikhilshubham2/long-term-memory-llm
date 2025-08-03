# app.py
import gradio as gr
from src.conversation_agent import ConversationAgent
from src.memory_manager import MemoryManager

# --- Initialization ---
# This is the same setup as in main.py. We create our agent one time.
print("Initializing agent and memory...")
memory = MemoryManager()
agent = ConversationAgent(memory_manager=memory)
print("Initialization complete. Launching UI...")

# --- The Chat Function ---
# This is the core function that Gradio will call for each message.
# It takes the user's message and the chat history as input.
def chat_function(message, history):
    """
    This function is the bridge between the Gradio UI and our ConversationAgent.
    """
    # We simply pass the user's message to our agent's handle_message method.
    response = agent.handle_message(message)
    return response

# --- Gradio UI Definition ---
# We use Gradio's built-in ChatInterface, which is perfect for a chatbot.
# It handles the chat history, input box, and message display for us.
ui = gr.ChatInterface(
    fn=chat_function,
    title="Long-Term Memory Agent",
    description="A conversational agent powered by Gemini that can remember, recall, and forget information across sessions.",
    examples=[
        "My favorite color is green.",
        "What is my favorite color?",
        "Forget about my favorite color."
    ]
).queue()

# --- Launch the Application ---
if __name__ == "__main__":
    # The launch() method starts the web server and opens the UI in your browser.
    # share=True creates a temporary public link so you can show it to others!
    ui.launch(share=True)