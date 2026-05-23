"""
AI News Researcher
Entry point for the application.
Loads configuration from .env and verifies the Gemini API key is present.
"""

import os
import sys
from dotenv import load_dotenv


def load_config() -> str:
    """Load environment variables and return the Gemini API key."""
    # Load variables from .env file into the environment
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or api_key == "your_key_here":
        print("ERROR: GEMINI_API_KEY is missing or still set to the placeholder value.")
        print("       Please update your .env file with a real API key.")
        sys.exit(1)

    return api_key


def main():
    api_key = load_config()
    print("API key loaded successfully.")
    # TODO: Initialize the Gemini client and start the news researcher
    # import google.generativeai as genai
    # genai.configure(api_key=api_key)


if __name__ == "__main__":
    main()
