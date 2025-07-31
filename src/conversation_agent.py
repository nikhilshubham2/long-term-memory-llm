# src/conversation_agent.py
import os
import json
import openai
from dotenv import load_dotenv
from src.memory_manager import MemoryManager

# Load environment variables from the .env file in the project root
load_dotenv()

class ConversationAgent:
    def __init__(self, memory_manager: MemoryManager):
        """
        Initializes the ConversationAgent.

        Args:
            memory_manager (MemoryManager): An instance of the memory manager.
        """
        self.memory_manager = memory_manager
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            # This error is critical, so we stop the program if the key is missing.
            raise ValueError("OPENAI_API_KEY not found. Please check your .env file.")
        self.client = openai.OpenAI(api_key=api_key)

    def _analyze_message_intent(self, user_message: str):
        """
        Uses an LLM to classify the user's intent.

        This is the "brain" that decides whether a message is a command
        to remember something, forget something, or just part of a normal chat.
        """
        # This system prompt is a powerful way to instruct the LLM on its task.
        system_prompt = """You are a classification assistant. Your job is to analyze a user's message and determine the intent. Classify the message into one of three categories:
1.  **ADD_MEMORY**: The user is stating a fact or information they want you to remember for later. Examples: "I use Shram and Magnet as productivity tools", "My favorite color is blue", "Remember that my flight is at 8 PM".
2.  **DELETE_MEMORY**: The user is asking to forget, remove, or update a previously stored fact. Examples: "I don't use Magnet anymore", "Forget about my favorite color", "My flight has been changed, so forget the 8 PM time".
3.  **CONVERSATION**: The user is asking a question or making a statement that is not a direct memory command. This is the default case. Examples: "What are the productivity tools that I use?", "Hello, how are you?", "What's the weather like?".

Respond with a JSON object in the strict format: {"intent": "CATEGORY", "content": "The core fact or subject"}
- For ADD_MEMORY, 'content' should be the specific fact to remember (e.g., "I use Shram and Magnet as productivity tools").
- For DELETE_MEMORY, 'content' should be the specific fact or subject to forget (e.g., "Magnet" or "my favorite color").
- For CONVERSATION, 'content' can be an empty string or the original message.
"""
        try:
            # We use a capable model and enforce JSON output for reliable parsing.
            response = self.client.chat.completions.create(
                model="gpt-4o-mini", # A cost-effective and powerful model for this task
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"User message: \"{user_message}\""}
                ],
                response_format={"type": "json_object"}
            )
            # The response content is a JSON string, so we parse it into a Python dictionary.
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            # If the API call fails, we default to treating it as a normal conversation.
            print(f"Error analyzing intent: {e}")
            return {"intent": "CONVERSATION", "content": user_message}

    def _get_conversational_response(self, user_message: str):
        """
        Generates a standard conversational response, but with the added context of long-term memories.
        """
        memories = self.memory_manager.get_all_memories()
        
        # We format the memories nicely for the prompt.
        if memories:
            memory_context = "\n".join([f"- {m['content']}" for m in memories])
        else:
            memory_context = "No facts are known about the user yet."

        # This prompt is for the main response generation.
        prompt = f"""You are a helpful assistant with a memory. Here are some facts you know about the user:
<memory>
{memory_context}
</memory>

Based on the facts in your memory, answer the user's current message.

User message: "{user_message}"
Assistant:"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo", # This model is fast and efficient for conversation.
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"An error occurred while generating a response: {e}"

    def handle_message(self, user_message: str):
        """
        The main public method to process a user's message.
        It orchestrates the analysis, memory operations, and response generation.
        """
        # Step 1: Analyze the user's intent.
        analysis = self._analyze_message_intent(user_message)
        intent = analysis.get("intent")
        content = analysis.get("content")

        # Step 2: Act based on the classified intent.
        if intent == "ADD_MEMORY" and content:
            self.memory_manager.add_memory(content)
            return f"Okay, I'll remember that: '{content}'"
        elif intent == "DELETE_MEMORY" and content:
            self.memory_manager.delete_memory(content)
            return f"Okay, I have forgotten everything related to: '{content}'"
        else: # Default to CONVERSATION
            return self._get_conversational_response(user_message)