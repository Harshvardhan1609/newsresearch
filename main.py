"""
AI News Researcher
Entry point for the application.
Loads configuration from .env and verifies the Gemini API key is present.

Usage:
    python main.py          # verify config then hint to run Streamlit
    streamlit run app.py    # launch the full web UI
"""

import os
import sys
import subprocess
from dotenv import load_dotenv


def load_config() -> str:
    """Load environment variables and return the Gemini API key."""
    # Load variables from .env file into the environment
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or api_key == "your_key_here":
        print("ERROR: GEMINI_API_KEY is missing or still set to the placeholder value.")
        print("       Please update your .env file with a real API key.")
        print("       Get one free at: https://aistudio.google.com/app/apikey")
        sys.exit(1)

    return api_key


def main():
    api_key = load_config()
    print("✅ API key loaded successfully.")
    print()
    print("To launch the web UI, run:")
    print("    streamlit run app.py")
    print()

    # Optionally auto-launch Streamlit if --launch flag is passed
    if "--launch" in sys.argv:
        print("🚀 Launching Streamlit app…")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)


if __name__ == "__main__":
    main()
