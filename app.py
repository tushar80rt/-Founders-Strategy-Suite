from env_config import load_environment
load_environment()

import streamlit as st
from camel_agents import (
    idea_validator_agent,
    business_model_agent,
    pitch_deck_agent,
    ui_design_agent,
    growth_strategy_agent,
    monetization_agent,
)
import re
import time

def clean_text(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    return text.replace('\u2014', '-').replace('\u2013', '-')

# Streamlit config
st.set_page_config(
    page_title="🏆 Startup Incubator - Powered by Camel AI, Mistral & langGraph",
    layout="wide",
    initial_sidebar_state="expanded"
)

#  CSS Styling 
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
div.stTextInput > div > div {
    max-width: 800px !important;
    margin: 0 auto;
}
.stTextInput>div>div>input {
    width: 100% !important;
    padding: 16px 24px !important;
    font-size: 18px !important;
    font-weight: 500;
    color: #f9fafb !important;
    background: #1f2937 !important;
    border: 2px solid #374151 !important;
    border-radius: 16px !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput>div>div>input::placeholder {
    color: #9ca3af !important;
    font-style: italic;
}
.stTextInput>div>div>input:focus {
    outline: none !important;
    border-color: #3b82f6 !important;
    background: #111827 !important;
    transform: scale(1.02);
}
.stButton>button {
    display: block;
    margin: 30px auto 0 auto;
    background: linear-gradient(135deg, #4f46e5, #3b82f6);
    color: white !important;
    font-weight: 700 !important;
    font-size: 20px !important;
    padding: 16px 52px !important;
    border-radius: 30px !important;
    border: none !important;
    cursor: pointer;
    box-shadow: 0 6px 15px rgba(59,130,246,0.4);
    transition: all 0.4s ease;
    font-family: 'Inter', sans-serif !important;
}
.stButton>button:hover {
    box-shadow: 0 8px 25px rgba(59,130,246,0.65);
    transform: translateY(-3px) scale(1.05);
}
.answer-box {
    border: 1.5px solid #3b82f6;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 20px;
    background: #1e293b;
    font-family: 'Inter', sans-serif;
    color: #f9fafb;
    box-shadow: 0 4px 12px rgba(59,130,246,0.15);
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
}
.answer-title {
    font-weight: 700;
    font-size: 22px;
    color: #60a5fa;
    margin-bottom: 10px;
}
.answer-subtitle {
    font-weight: 600;
    font-size: 16px;
    color: #93c5fd;
    margin-bottom: 8px;
}
[data-testid="stSidebar"] {
    background: #0f172a !important;
    color: #f1f5f9 !important;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("💡 Founders' Strategy Suite")
    st.markdown("""
**AI-powered Startup Incubator built with [Camel AI](https://www.camel-ai.org/), [Mistral LLM](https://mistral.ai/), and [langGraph](https://www.langchain.com/langgraph)**

This app transforms your startup ideas into actionable business plans by leveraging a suite of expert AI agents orchestrated through langGraph's powerful AI workflow toolkit.
""")
    creativity_level = st.slider(
        "🎚️ AI Creativity Level",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Adjust how creative/conservative the AI responses should be"
    )
    st.markdown("""
### What you get:
- ✅ Idea Validation
- 💰 Business Model
- 📊 Pitch Deck
- 🎨 UI/UX Design
- 📈 Growth Strategy
- 💲 Monetization Plans

Powered by **Camel AI**, **Mistral LLMs**, and **langGraph orchestration**.
""")
    st.markdown("---")
    st.caption("© 2025 💡 Founders' Strategy Suite")

# Centered layout
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.markdown("""
    <h1 style='text-align: center; color: #f9fafb; margin-bottom: 30px;'>
    💡 Founders' Strategy Suite
    </h1>
    """, unsafe_allow_html=True)

    idea = st.text_input(
        "Describe your startup idea:",
        placeholder="What can I help you with today?",
        key="idea_input",
        label_visibility="collapsed"
    )

    if "conversations" not in st.session_state:
        st.session_state["conversations"] = []

    tasks = [
        ("✅ Idea Validation", idea_validator_agent),
        ("💰 Business Model", business_model_agent),
        ("📊 Pitch Deck", pitch_deck_agent),
        ("🎨 UI Design", ui_design_agent),
        ("📈 Growth", growth_strategy_agent),
        ("💲 Monetization", monetization_agent),
    ]

    if st.button("✨ Generate Business Plan", type="primary", use_container_width=True):
        if not idea.strip():
            st.warning("Please enter your idea first")
        else:
            progress_bar = st.progress(0, text="Analyzing your idea...")
            plan = {}

            for idx, (section, func) in enumerate(tasks):
                progress = int((idx + 1) / len(tasks) * 100)
                progress_bar.progress(progress, text=f"Generating {section}...")
                answer = func(idea)
                container = st.container()
                with container:
                    st.markdown(f'<div class="answer-box">'
                                f'<div class="answer-subtitle">Section {idx + 1} of {len(tasks)}</div>'
                                f'<div class="answer-title">{section}</div>'
                                f'<div style="margin-top: 12px;">{answer}</div>'
                                f'</div>', unsafe_allow_html=True)
                plan[section] = answer
                # time.sleep(0.1)


            progress_bar.empty()
            st.success("Business plan generated successfully!")
            st.session_state.conversations.insert(0, {"idea": idea, "plan": plan})

    if st.session_state.conversations:
        st.markdown("## 📚 Previous Analyses")

    for idx, convo in enumerate(st.session_state.conversations):
        with st.expander(f"💡 Idea: {clean_text(convo['idea'])}", expanded=(idx == 0)):
            for section, content in convo["plan"].items():
                st.markdown(f"### {section}")
                st.write(content)
                st.markdown("---")

