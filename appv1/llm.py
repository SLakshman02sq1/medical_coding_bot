import os
import sys
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# load .env variable
load_dotenv()

# getting api key from .env
groq_api_key = os.getenv("GROQ_API_KEY")

# if-else condition to check the availability of the api key
if not groq_api_key:
    print("Error: GROQ_API_KEY not found")
    sys.exit(1)
else:
    print("GROQ_API_KEY Successfully loaded")

# function to load the llm and set its parameters and api key
def load_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.5,
        max_tokens=500,
        api_key=groq_api_key
    )

# assigning the function to a callable variable
llm = load_llm() 