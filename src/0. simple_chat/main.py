import os

from dotenv import load_dotenv
from anthropic_calls import AnthropicCalls

if __name__ == "__main__":
    load_dotenv()
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    calls = AnthropicCalls(api_key=ANTHROPIC_API_KEY, stream=True)

    n = 50
    message = ""
    while message != "END": 
        message = input("User:")
        calls.chat(message=f"{message} please use {n} words or less")