import os
import requests,sys
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    print("Error: GROQ_API_KEY not found")
    sys.exit(1)
else:
    print("GROQ_API_KEY Successfully loaded")
    
def load_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.5,
        max_tokens=500,
        api_key=groq_api_key
    )

llm = load_llm()