"""
AI News Researcher — Streamlit entry point.
Fetches live AI news using Gemini 2.0 Flash with Google Search grounding.

Changes in 'harsh' branch:
- Added category filter tabs
- Added JSON export / download button
- Improved error messages with retry guidance
- Added article count badge
- Extracted render helpers for maintainability
"""

import os
import json
import re
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import types

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="AI News Researcher",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load environment variables ────────────────────────────────────────────────
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ── Session state defaults ────────────────────────────────────────────────────
if "articles" not in st.session_state:
    st.session_state.articles = []
if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    st.divider()

    if GEMINI_API_KEY and GEMINI_API_KEY != "your_key_here":
        st.success("✅ API connected jai jai ai =", icon="🟢")
        genai.configure(api_key=GEMINI_API_KEY)
        api_ready = True
    else:
        st.error(
            "❌ GEMINI_API_KEY missing or not set.\n\n"
            "Please copy `.env.example` → `.env` and add your key from "
            "[Google AI Studio](https://aistudio.google.com/app/apikey).",
            icon="🔴",
        )
        api_ready = False

    st.divider()
    st.markdown("### 🔍 Search Settings")
    topic = st.text_input(
        "Research topic",
        value="artificial intelligence",
        placeholder="e.g. large language models",
    )
    count = st.slider("Number of articles", min_value=3, max_value=15, value=6)

    st.divider()
    fetch_btn = st.button("🚀 Fetch News", use_container_width=True, disabled=not api_ready)

    # ── Export section (only shown when articles are loaded) ──────────────────
    if st.session_state.articles:
        st.divider()
        st.markdown("### 📥 Export")
        json_data = json.dumps(st.session_state.articles, indent=2, ensure_ascii=False)
        st.download_button(
            label="⬇️ Download as JSON",
            data=json_data,
            file_name=f"news_{st.session_state.last_topic.replace(' ', '_')}.json",
            mime="application/json",
            use_container_width=True,
        )

    st.divider()
    st.caption("Powered by Gemini 2.0 Flash + Google Search grounding")

# ── Main header ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <h1 style='text-align:center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;
               font-size: 3rem; margin-bottom: 0;'>
        🤖 AI News Researcher
    </h1>
    <p style='text-align:center; color:#888; font-size:1.15rem; margin-top:0.4rem;'>
        Real-time AI &amp; tech news — grounded in live web results via Gemini 2.0 Flash
    </p>
    """,
    unsafe_allow_html=True,
)
st.divider()


# ── Core news-fetching logic ──────────────────────────────────────────────────
def fetch_ai_news(topic: str, count: int) -> list[dict]:
    """
    Call Gemini 2.0 Flash with Google Search grounding and return a list
    of news article dicts with keys: title, summary, source, date, category.
    Raises ValueError on bad JSON, or any API exception on network/auth failure.
    """
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        tools=[types.Tool(google_search=types.GoogleSearch())],
    )

    prompt = f"""You are an expert AI news researcher with access to real-time web search.

Search the web RIGHT NOW for the {count} most recent and important news articles about: {topic}

Return ONLY a valid JSON array — no markdown, no code fences, no backticks, no explanation.
Each element must be a JSON object with exactly these keys:
  "title"    : headline of the article (string)
  "summary"  : 2-3 sentence summary of what happened (string)
  "source"   : publication or website name (string)
  "date"     : publication date in YYYY-MM-DD format or "Recent" if unknown (string)
  "category" : one of [Research, Industry, Policy, Products, Open Source] (string)

Example of the exact format required:
[
  {{
    "title": "Example Headline",
    "summary": "Brief summary here.",
    "source": "TechCrunch",
    "date": "2025-05-22",
    "category": "Industry"
  }}
]

Return {count} items. Output the raw JSON array and absolutely nothing else."""

    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(temperature=0.2),
    )

    raw = response.text.strip()

    # Strip accidental markdown fences if the model adds them despite instructions
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"\s*```$", "", raw, flags=re.MULTILINE)
    raw = raw.strip()

    articles = json.loads(raw)
    if not isinstance(articles, list):
        raise ValueError("Gemini did not return a JSON array.")
    return articles


# ── Category badge colours ────────────────────────────────────────────────────
CATEGORY_COLORS = {
    "Research":     ("#e0f0ff", "#0066cc"),
    "Industry":     ("#fff3e0", "#e65c00"),
    "Policy":       ("#f3e5f5", "#7b1fa2"),
    "Products":     ("#e8f5e9", "#2e7d32"),
    "Open Source":  ("#fff8e1", "#f57f17"),
}

ALL_CATEGORIES = ["All"] + list(CATEGORY_COLORS.keys())


def category_badge(cat: str) -> str:
    bg, fg = CATEGORY_COLORS.get(cat, ("#f0f0f0", "#333"))
    return (
        f"<span style='background:{bg};color:{fg};padding:2px 10px;"
        f"border-radius:12px;font-size:0.78rem;font-weight:600;'>{cat}</span>"
    )


# ── Render a single article card ──────────────────────────────────────────────
def article_card(art: dict) -> str:
    cat   = art.get("category", "General")
    badge = category_badge(cat)
    title   = art.get("title", "")
    summary = art.get("summary", "")
    source  = art.get("source", "")
    date    = art.get("date", "")
    return f"""
        <div style='border:1px solid #2a2a2a; border-radius:12px;
                    padding:20px; margin-bottom:16px;
                    background: linear-gradient(145deg,#1a1a2e,#16213e);
                    box-shadow:0 4px 15px rgba(0,0,0,0.3);'>
            <div style='display:flex;justify-content:space-between;
                        align-items:center;margin-bottom:10px;'>
                {badge}
                <span style='color:#888;font-size:0.8rem;'>📅 {date}</span>
            </div>
            <h3 style='color:#e0e0ff;font-size:1.05rem;
                       margin:0 0 10px 0;line-height:1.4;'>
                {title}
            </h3>
            <p style='color:#aaa;font-size:0.9rem;
                      line-height:1.6;margin:0 0 12px 0;'>
                {summary}
            </p>
            <span style='color:#667eea;font-size:0.82rem;font-weight:500;'>
                🔗 {source}
            </span>
        </div>
    """


# ── Render articles with category filter ─────────────────────────────────────
def render_articles(articles: list[dict]):
    # ── Article count badge ───────────────────────────────────────────────────
    st.markdown(
        f"<p style='color:#667eea;font-weight:600;font-size:1rem;'>"
        f"📰 {len(articles)} article{'s' if len(articles) != 1 else ''} found</p>",
        unsafe_allow_html=True,
    )

    # ── Category filter tabs ──────────────────────────────────────────────────
    present_cats = sorted({a.get("category", "General") for a in articles})
    tab_labels   = ["All"] + [c for c in list(CATEGORY_COLORS.keys()) if c in present_cats]
    tabs         = st.tabs(tab_labels)

    for tab, label in zip(tabs, tab_labels):
        with tab:
            filtered = articles if label == "All" else [
                a for a in articles if a.get("category") == label
            ]
            if not filtered:
                st.info("No articles in this category.")
                continue
            cols = st.columns(2)
            for i, art in enumerate(filtered):
                with cols[i % 2]:
                    st.markdown(article_card(art), unsafe_allow_html=True)


# ── Main fetch flow ───────────────────────────────────────────────────────────
if fetch_btn:
    with st.spinner(f"🔍 Searching for **{count}** articles on *{topic}*…"):
        try:
            articles = fetch_ai_news(topic, count)
            st.session_state.articles   = articles
            st.session_state.last_topic = topic
            st.success(f"Found **{len(articles)}** articles on **{topic}**", icon="✅")
            render_articles(articles)
        except json.JSONDecodeError as e:
            st.error(
                f"❌ Could not parse Gemini's response as JSON.\n\n"
                f"**Detail:** {e}\n\n"
                f"💡 Try clicking **Fetch News** again — this is usually a transient issue."
            )
        except Exception as e:
            err_str = str(e)
            if "401" in err_str or "API_KEY" in err_str.upper():
                st.error(
                    "❌ Invalid or missing API key.\n\n"
                    "Please check your `.env` file and ensure `GEMINI_API_KEY` is correct."
                )
            elif "429" in err_str or "quota" in err_str.lower():
                st.error(
                    "❌ API rate limit exceeded.\n\n"
                    "Please wait a moment before trying again, or reduce the article count."
                )
            else:
                st.error(f"❌ An error occurred while fetching news.\n\n**Detail:** {e}")

# ── Show cached results if available (no new fetch) ──────────────────────────
elif st.session_state.articles:
    render_articles(st.session_state.articles)

else:
    # ── Landing placeholder ───────────────────────────────────────────────────
    st.markdown(
        """
        <div style='text-align:center;padding:60px 20px;'>
            <div style='font-size:5rem;margin-bottom:16px;'>📡</div>
            <h2 style='color:#667eea;'>Ready to fetch live AI news</h2>
            <p style='color:#888;font-size:1.05rem;'>
                Enter a topic in the sidebar and click <b>Fetch News</b> to get
                real-time results grounded in live web search.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
