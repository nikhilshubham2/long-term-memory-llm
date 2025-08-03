## Key Features

-   **Intent-Driven Memory:** The agent first classifies the user's intent (e.g., add, delete, or converse) to handle requests accurately and efficiently.
-   **Contextual Conversations:** Stored memories are injected into conversational prompts, allowing the LLM to provide personalized, context-aware responses.
-   **AI-Powered Deletion:** Instead of simple text matching, the agent uses the LLM's intelligence to identify which specific memories to delete based on natural language commands, making the process robust and intuitive.
-   **API Agnostic Design:** Initially built for OpenAI, the agent was successfully migrated to the **Google Gemini API**, demonstrating architectural flexibility and adaptability.
-   **Secure Configuration:** API keys and sensitive information are managed securely using a `.env` file, which is excluded from version control.
-   **Unit Tested:** Core components like the `MemoryManager` are validated with `pytest` to ensure reliability.
-   **Interactive Web UI:** A user-friendly web interface built with **Gradio** allows for easy, real-time interaction with the agent.

## Tech Stack

-   **Language:** Python 3
-   **LLM API:** Google Gemini API (`google-generativeai`)
-   **Environment Management:** `python-dotenv`
-   **Testing:** `pytest`

## Architectural Decisions

1.  **Two-Step AI Interaction:** Instead of a single prompt, the agent first uses a fast, low-cost API call to classify the user's intent. This separates the logic of memory management from conversation, making the system more efficient and easier to debug.

2.  **The Pivot to AI-Powered Deletion:** An initial attempt at memory deletion used simple string matching (e.g., deleting a memory if it contained the word "job"). Testing revealed this was brittle. The final implementation is far more powerful: it presents the LLM with a numbered list of current memories and asks it to identify which indices to delete based on the user's request. This leverages the AI's contextual understanding to perform a much more accurate deletion.

3.  **Adapting to API Provider Constraints:** After encountering limitations with OpenAI's free tier, the project was successfully migrated to the Google Gemini API. This pivot proved that the core application logic was well-designed and not tightly coupled to a single service provider.

## Setup and Installation

Follow these steps to set up and run the project locally.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/long-term-memory-llm.git
    cd long-term-memory-llm
    ```

2.  **Create and activate a virtual environment:**
    ```powershell
    # Create the environment
    python -m venv venv

    # Activate the environment on Windows
    .\venv\Scripts\Activate.ps1
    ```

3.  **Install dependencies from `requirements.txt`:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    -   Create a file named `.env` in the root of the project.
    -   Add your Google Gemini API key to the file in the following format:
        ```
        GEMINI_API_KEY="your_api_key_here"
        ```

## Usage

This application can be run in two modes: through an interactive web UI or via the command line.

### Web Interface

To launch the user-friendly web UI, run the `app.py` script from the project's root directory.

```bash
python app.py
```

This will start a local web server and provide two URLs in your terminal. Open the "local URL" in your browser to interact with the agent. A temporary public "share URL" will also be generated, which can be used to share the demo with others.

### Command-Line Interface

For a simple, terminal-based interaction, run the `main.py` script:

```bash
python main.py
```

The application will start, and you can begin chatting with it in your terminal. Type `exit` to end the session.

To run the conversational agent, execute the `main.py` script from the project's root directory. Ensure your virtual environment is activated first.


## Example Conversation

Here is a sample interaction demonstrating the agent's capabilities:

```
Chat with the Long-Term Memory Agent!
Type 'exit' to end the conversation.
--------------------------------------------------
You: My favorite city is Bangalore.
Agent: Okay, I'll remember that: 'My favorite city is Bangalore'
You: I work as a Machine Learning Engineer.
Agent: Okay, I'll remember that: 'The user's occupation is Machine Learning Engineer'
You: What is my job and what city do I like?
Agent: You are a Machine Learning Engineer and your favorite city is Bangalore.
You: My favorite food is pizza.
Agent: Okay, I'll remember that: 'favorite food is pizza'
You: I am a software engineer.
Agent: That's interesting!  While I know you work as a Machine Learning Engineer, which is a type of software engineering, I also know your favorite programming language is Python and your favorite city is Bangalore.  Do you specialize in any particular area of software engineering? Perhaps you use Python in your work?
You: Forget about my job and city
Agent: Okay, I have forgotten: 'The user's occupation is Machine Learning Engineer, My favorite city is Bangalore, My favorite city is Bangalore., I work as a Machine Learning Engineer, My favorite city is Bangalore., I work as a Machine Learning Engineer, I work as a Machine Learning Engineer, I work as a Machine Learning Engineer, I work as a Machine Learning Engineer'
You: What is my favorite food? 
Agent: Your favorite food is pizza.
You: Which is my favorite city?
Agent: I don't have any information about your favorite city in my memory.  I know your favorite programming language is Python and your favorite food is pizza.
You: My favorite city is Mumbai.
Agent: Okay, I'll remember that: 'favorite city is Mumbai'
You: Forget about my favorite programming language.
Agent: Okay, I have forgotten: 'My favorite programming language is Python, My favorite programming language is Python'
You: Which is my favorite city and programming language?
Agent: Your favorite city is Mumbai.  I don't have any information about your favorite programming language.
You: My Favorite city is Goa and favorite programming language is java.
Agent: Okay, I'll remember that: 'Favorite city is Goa and favorite programming language is Java'
You: Which is my favorite city and programming language?
Agent: Based on my information, your favorite city is Goa and your favorite programming language is Java.  There's some conflicting information in my memory about your favorite city (it also lists Mumbai), but the most recent entry indicates Goa.
You: exit
Agent: Goodbye!

```

## Project Structure

```
/long-term-memory-llm
|
|-- /src                  # Source code for the application
|   |-- __init__.py
|   |-- memory_manager.py     # Handles reading/writing to the memory file
|   `-- conversation_agent.py # Core logic, interacts with Gemini API
|
|-- /tests                # Unit tests for the project
|   `-- test_memory_manager.py
|-- app.py                # Gradio Web UI application
|-- main.py               # Main entry point to run the application
|-- requirements.txt      # Project dependencies
|-- .env                  # Stores secret API keys (not committed)
|-- .gitignore            # Specifies files for Git to ignore
|-- README.md             # You are here!
`-- venv/                 # Python virtual environment folder
```