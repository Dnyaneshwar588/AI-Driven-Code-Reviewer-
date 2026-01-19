
        
import streamlit as st
import time
import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

from code_parser import parse_code
from style_checker import show_style_corrected
from error_detector import detect_errors
from ai_suggester import get_ai_suggestions


def stream_data(text):
    """Yields text word by word for the typewriter effect."""
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)

st.set_page_config(
    page_title="AI Code Reviewer Application",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #f8f9fa 0%, #e9ecef 100%);
    }
    .main {
        background-color: transparent;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        color: #1e3a8a;
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        padding: 20px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    h2, h3 {
        color: #1e293b !important;
    }
    p, div, span, label {
        color: #1e293b !important;
    }
    .stMarkdown {
        color: #1e293b !important;
    }
    
    /* Ultra-specific code block styling with high visibility */
    code {
        color: #d63384 !important;
        background-color: #f8f9fa !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        font-family: 'Courier New', monospace !important;
    }
    pre {
        background-color: #0f172a !important;
        border-radius: 8px !important;
        padding: 20px !important;
        border: 1px solid #475569 !important;
    }
    pre code, pre code * {
        color: #22d3ee !important;
        background-color: transparent !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
    }
    pre code span {
        color: #22d3ee !important;
    }
    .stCodeBlock {
        background-color: #0f172a !important;
    }
    .stCodeBlock pre {
        background-color: #0f172a !important;
    }
    .stCodeBlock code, .stCodeBlock code * {
        color: #22d3ee !important;
        background-color: transparent !important;
    }
    [data-testid="stCodeBlock"] {
        background-color: #0f172a !important;
    }
    [data-testid="stCodeBlock"] pre {
        background-color: #0f172a !important;
    }
    [data-testid="stCodeBlock"] code, [data-testid="stCodeBlock"] code *, [data-testid="stCodeBlock"] code span {
        color: #22d3ee !important;
        background-color: transparent !important;
    }
    .stMarkdown pre code, .stMarkdown pre code *, .stMarkdown pre code span {
        color: #22d3ee !important;
    }
    div[data-testid="stExpander"] pre {
        background-color: #0f172a !important;
    }
    div[data-testid="stExpander"] pre code, div[data-testid="stExpander"] pre code *, div[data-testid="stExpander"] pre code span {
        color: #22d3ee !important;
    }
    
    /* Override all pygments classes */
    .highlight, .highlight * {
        color: #22d3ee !important;
        background-color: transparent !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #f1f5f9;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        border: 2px solid transparent;
        color: #475569 !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        font-family: 'Courier New', monospace;
        color: #1e293b !important;
        background-color: white !important;
    }
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    .stTextArea label {
        color: #1e293b !important;
        font-weight: 600;
    }
    div[data-testid="stExpander"] {
        background-color: white;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin: 10px 0;
    }
    div[data-testid="stExpander"] summary {
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    div[data-testid="stExpander"] code {
        color: #22d3ee !important;
    }
    .element-container {
        margin-bottom: 1rem;
    }
    .stChatMessage {
        background-color: white !important;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .stChatMessage p {
        color: #1e293b !important;
    }
    .stChatMessage code {
        color: #d63384 !important;
        background-color: #f8f9fa !important;
    }
    [data-testid="stChatMessageContent"] {
        color: #1e293b !important;
    }
    [data-testid="stChatMessageContent"] p {
        color: #1e293b !important;
    }
    .stAlert {
        color: #1e293b !important;
    }
    .stAlert p {
        color: #1e293b !important;
    }
    </style>
""", unsafe_allow_html=True)

st.logo("logo.png", size="large")

# Header with emoji
st.markdown("<h1>🤖 AI-Driven Code Reviewer</h1>", unsafe_allow_html=True)

# Subheader with description
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
        <div style='text-align: center; padding: 10px; background-color: white; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 20px;'>
            <p style='color: #666; font-size: 1.1rem; margin: 0;'>
                ✨ Analyze your Python code with AI-powered insights • 
                🔍 Detect errors • 
                🎨 Check style • 
                💡 Get smart suggestions
            </p>
        </div>
    """, unsafe_allow_html=True)

# Refresh button with icon
col1, col2, col3 = st.columns([4, 1, 4])
with col2:
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 Code Analysis", "🤖 AI Suggestions"])



with tab1:
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); 
                    padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 4px solid #667eea;'>
            <p style='color: #333; font-size: 1.1rem; margin: 0;'>
                📋 Paste your Python code below and click <strong>Analyze</strong> to get comprehensive feedback on errors, style, and AI suggestions.
            </p>
        </div>
    """, unsafe_allow_html=True)

    code = st.text_area("💻 Code Input:", height=250, placeholder="# Paste your Python code here...\n\ndef example():\n    print('Hello, World!')")

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        analyze_button = st.button("🔍 Analyze Code", type="primary", use_container_width=True)
    
    if analyze_button:
        if not code:
            st.warning("⚠️ Please enter some code first!")
        else:
            # Store code in session state so tab2 can access it
            st.session_state.last_code = code
            
            with st.spinner("🔄 Analyzing your code..."):
                parse_result = parse_code(code)
                
            if not parse_result["success"]:
                st.error("❌ Your code has syntax errors!")
                st.code(parse_result["error"]["message"], language="text")
                st.info("💡 AI suggestions will still be provided even with syntax errors!")
            else:
                st.success("✅ Code parsed successfully!")

                st.markdown("---")
                st.markdown("### 🔍 Error Detection Results")
                
                with st.spinner("Detecting errors..."):
                    error_result = detect_errors(code)

                if error_result["success"]:
                    if error_result["error_count"] == 0:
                        st.markdown("""
                            <div style='background-color: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;'>
                                <p style='color: #155724; margin: 0; font-size: 1.1rem;'>
                                    ✨ No static errors found! Your code looks clean.
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning(f"⚠️ Found {error_result['error_count']} potential issue(s):")
                        for idx, error in enumerate(error_result["errors"], 1):
                            with st.expander(f"Issue #{idx}: {error['type']}", expanded=True):
                                st.markdown(f"**📌 Message:** {error['message']}")
                                st.info(f"💡 **Suggestion:** {error['suggestion']}")
                else:
                    st.error("❌ Could not analyze code for errors")

                st.markdown("---")
                st.markdown("### ✔️Style-Corrected Version")
                try:
                    with st.spinner("Formatting code..."):
                        style_result = show_style_corrected(code)
                    if style_result["success"]:
                        with st.expander("👁️ View Formatted Code", expanded=False):
                            st.code(style_result["corrected_code"], language="python")
                    else:
                        st.info("ℹ️ Style correction not available.")
                except Exception:
                    st.info("ℹ️ Style checking module not found.")

            st.markdown("---")
            st.markdown("### 📄 Original Code Reference")
            with st.expander("👁️ See Original Code"):
                st.code(code, language="python")

with tab2:
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); 
                    padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 4px solid #764ba2;'>
            <p style='color: #333; font-size: 1.1rem; margin: 0;'>
                🤖 Get AI-powered suggestions for your code. Paste your code and click <strong>Analyze</strong> in the first tab.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # We'll store the code in session state so tab2 can access it
    if "last_code" in st.session_state:
        with st.spinner("🤔 Asking the AI for advice..."):
            suggestions = get_ai_suggestions(st.session_state.last_code)

            for suggestion in suggestions:
                if suggestion["type"] == "AISuggestion":
                    with st.chat_message("assistant", avatar="🤖"):
                        st.write_stream(stream_data(suggestion["message"]))
                    
                elif suggestion["type"] == "Error":
                    st.error(f"❌ {suggestion['message']}")
    else:
        st.markdown("""
            <div style='text-align: center; padding: 40px; background-color: white; 
                        border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <p style='color: #999; font-size: 1.2rem;'>
                    👈 Please analyze your code in the <strong>Code Analysis</strong> tab first
                </p>
            </div>
        """, unsafe_allow_html=True)


