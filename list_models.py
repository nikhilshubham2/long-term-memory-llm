# list_models.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load the API key from your .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Finding available models for your API key...")
print("-" * 30)

# List all models that support the "generateContent" method
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(f"Model found: {m.name}")

print("-" * 30)