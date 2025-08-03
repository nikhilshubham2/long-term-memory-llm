import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from src.memory_manager import MemoryManager

# Load environment variables from the .env file in the project root
load_dotenv()

class ConversationAgent:
    def __init__(self, memory_manager: MemoryManager):
        self.memory_manager = memory_manager
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found. Please check your .env file.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

    def _analyze_message_intent(self, user_message: str):
        system_prompt = """You are a classification assistant. Your job is to analyze a user's message and determine the intent. Classify the message into one of three categories:
1.  **ADD_MEMORY**: The user is stating a fact or information they want you to remember for later.
2.  **DELETE_MEMORY**: The user is asking to forget, remove, or update a previously stored fact.
3.  **CONVERSATION**: The user is asking a question or making a statement that is not a direct memory command.

Respond with a JSON object in the strict format: {"intent": "CATEGORY", "content": "The core fact or subject"}
"""
        full_prompt = f"{system_prompt}\n\nUser message: \"{user_message}\""
        try:
            generation_config = genai.types.GenerationConfig(response_mime_type="application/json")
            response = self.model.generate_content(full_prompt, generation_config=generation_config)
            return json.loads(response.text)
        except Exception as e:
            print(f"Error analyzing intent with Gemini: {e}")
            return {"intent": "CONVERSATION", "content": user_message}

    def _get_conversational_response(self, user_message: str):
        memories = self.memory_manager.get_all_memories()
        memory_context = "\n".join([f"- {m['content']}" for m in memories]) if memories else "No facts are known about the user yet."

        prompt = f"""You are a helpful assistant with a memory. Here are some facts you know about the user:
<memory>
{memory_context}
</memory>

Based on the facts in your memory, answer the user's current message.

User message: "{user_message}"
Assistant:"""
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"An error occurred while generating a response with Gemini: {e}"

    # DELETION METHOD
    def _handle_deletion(self, deletion_request: str):
        """
        Uses the LLM to intelligently identify which memories to delete.
        """
        memories = self.memory_manager.get_all_memories()
        if not memories:
            return "There are no memories to delete."

        # Create a numbered list of memories for the AI to choose from
        memories_list_str = "\n".join([f"{i+1}. {mem['content']}" for i, mem in enumerate(memories)])

        # --- FIX IS HERE: Doubled curly braces {{ and }} ---
        prompt = f"""You are a memory deletion assistant. The user wants to delete a memory.
    Your task is to identify which of the following numbered memories corresponds to the user's request.

    User's deletion request: "{deletion_request}"

    Here are the current memories:
    {memories_list_str}

    Respond with a JSON object containing the numbers of the memories to delete, like {{"indices_to_delete": [1, 3]}}.
    If no memory matches the request, respond with {{"indices_to_delete": []}}.
    """
        try:
            generation_config = genai.types.GenerationConfig(response_mime_type="application/json")
            response = self.model.generate_content(prompt, generation_config=generation_config)
            
            result = json.loads(response.text)
            indices_to_delete = result.get("indices_to_delete", [])

            if not indices_to_delete:
                return "Okay, I couldn't find a specific memory to delete based on your request."

            # We get the indices from the AI and delete the memories from our list
            # We must sort and reverse the indices to avoid issues when deleting multiple items
            indices_to_delete.sort(reverse=True)
            
            deleted_memories_content = []
            for index in indices_to_delete:
                # Check index is valid
                if 0 < index <= len(memories):
                    deleted_memories_content.append(memories.pop(index - 1)['content'])
            
            # Now we tell the memory manager to save the new, shorter list of memories
            self.memory_manager.update_memories(memories)
            
            return f"Okay, I have forgotten: '{', '.join(deleted_memories_content)}'"

        except Exception as e:
            print(f"Error during AI-powered deletion: {e}")
            return "Sorry, I had trouble processing that deletion request."

    def handle_message(self, user_message: str):
        analysis = self._analyze_message_intent(user_message)
        intent = analysis.get("intent")
        content = analysis.get("content")

        if intent == "ADD_MEMORY" and content:
            self.memory_manager.add_memory(content)
            return f"Okay, I'll remember that: '{content}'"
        
        # DELETION HANDLING
        elif intent == "DELETE_MEMORY" and content:
            return self._handle_deletion(content)
        
        else: # Default CONVERSATION
            return self._get_conversational_response(user_message)