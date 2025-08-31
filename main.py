import streamlit as st
import pandas as pd
from langchain_helper import get_few_shotdb_chain

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Arshad T-shirt Store QA",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# Header / Branding
# ---------------------------
st.markdown(
    """
    <div style="text-align:center;">
        <h1>👕 Arshad T-shirt Store QA Assistant</h1>
        <p style="font-size:18px; color:gray;">
        Ask questions about our T-shirt inventory and get instant insights powered by AI & SQL ⚡
        </p>
    </div>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Load LangChain
# ---------------------------
@st.cache_resource
def load_chain():
    return get_few_shotdb_chain()

chain = load_chain()

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.header("🛍️ About This App")
st.sidebar.write(
    """
    - Natural language → SQL → Answer  
    - Built with **LangChain + Streamlit**  
    - Designed for **interactive database exploration**  
    """
)

# ---------------------------
# Main App - Q&A
# ---------------------------
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []

st.subheader("💡 Ask Your Question")

# Step 1: Ask user how they want to proceed
ask_mode = st.radio(
    "Choose how you want to ask:",
    ("Type your own question", "Pick from predefined questions"),
    horizontal=True
)

# Predefined list of questions
sample_questions = [
    "How many total t-shirts are left in stock?",
    "Show me the total stock by brand.",
    "Which color has the most stock?",
    "List all sizes available for Adidas t-shirts.",
    "How many white Levi t-shirts do we have?",
    "What’s the average stock quantity per brand?",
    "Show top 5 t-shirts with highest stock.",
    "What’s the total stock across all brands?",
    "List all t-shirts in size M.",
    "Which brand has the least stock?"
]

# Step 2: Show input based on choice
question = ""
if ask_mode == "Type your own question":
    question = st.text_area(
        "✍️ Type your question here:",
        placeholder="e.g. How many Nike t-shirts are in size M?"
    )
elif ask_mode == "Pick from predefined questions":
    question = st.selectbox("📋 Choose a question:", sample_questions)

# ---------------------------
# Handle Answer Generation
# ---------------------------
if st.button("🔎 Get Answer", use_container_width=True):
    if question.strip():
        with st.spinner("Fetching answer from database..."):
            answer = chain.run(question)

        # Store only (q, a) to avoid SQL
        st.session_state.qa_history.append((question, answer))

# ---------------------------
# Show Results
# ---------------------------
if st.button("🗑️ Clear History"):
    st.session_state.qa_history = []

if st.session_state.qa_history:
    st.subheader("📌 Results")

    for i, (q, a) in enumerate(reversed(st.session_state.qa_history), 1):
        st.markdown(
            f"""
            <div style="padding:15px; margin:10px 0; border-radius:10px; background:#f9f9f9; border:1px solid #ddd;">
              <p style="color:black; font-size:20px; margin-bottom:5px;"><b>❓ Question:</b> {q}</p>
              <span style="color:black; font-size:20px;"><b>✅ Answer:</b> <span style="color:black; font-size:20px;">{a}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------------------
    # Download Button
    # ---------------------------
    df = pd.DataFrame(st.session_state.qa_history, columns=["Question", "Answer"])
    st.download_button("⬇️ Download Q&A History (CSV)", df.to_csv(index=False), "qa_history.csv")
