# 🤖 AI News Researcher

A real-time AI news research tool powered by **Gemini 2.0 Flash** with Google Search grounding. Built with Streamlit.

## Features

- 🔍 **Live web search** — fetches real-time news using Gemini's Google Search grounding
- 🗂️ **Category filtering** — browse by Research, Industry, Policy, Products, or Open Source
- 📥 **Export to JSON** — download fetched articles as a JSON file
- 🌙 **Dark-mode UI** — premium dark interface with gradient accents
- ⚡ **Fast & responsive** — minimal latency with Gemini 2.0 Flash

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/Harshvardhan1609/newsresearch.git
cd newsresearch
```

### 2. Create a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure your API key
Copy `.env.example` to `.env` and fill in your Gemini API key:
```bash
copy .env.example .env   # Windows
cp .env.example .env     # macOS / Linux
```

Edit `.env`:
```
GEMINI_API_KEY=your_actual_api_key_here
```

Get your free API key at [Google AI Studio](https://aistudio.google.com/app/apikey).

### 5. Run the app
```bash
streamlit run app.py
```

## Project Structure

```
newsresearch/
├── app.py            # Streamlit UI & core logic
├── main.py           # CLI entry point / config loader
├── requirements.txt  # Python dependencies
├── .env.example      # Environment variable template
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

## Dependencies

| Package | Purpose |
|---------|---------|
| `google-generativeai` | Gemini API client |
| `python-dotenv` | Load `.env` variables |
| `streamlit` | Web UI framework |

## License

MIT
