"""
demo_app.py
============
Phase 4 (optional): Streamlit demo UI for face-to-face interviews.

Run:
    streamlit run scripts/demo_app.py

This is purely for visual demo. Not part of the core RAG.
"""

import streamlit as st

from src.rag_credit_qa import CreditRiskQA

st.set_page_config(
    page_title="Credit Risk RAG Demo",
    page_icon="🏦",
    layout="wide",
)

st.title("🏦 Credit Risk Q&A (RAG)")
st.caption(
    "Ask questions about 10-K Risk Factors. "
    "Powered by LangChain + Chroma + OpenAI. "
    "All answers cite source chunks."
)

# Sidebar: ticker filter
TICKERS = ["(All)", "TSM", "AAPL", "F", "MAR", "BBY"]
ticker_choice = st.sidebar.selectbox("Filter by company", TICKERS)
top_k = st.sidebar.slider("Retrieval top-k", 1, 10, 5)

# Sample questions
st.sidebar.markdown("---")
st.sidebar.markdown("**Sample questions:**")
samples = [
    "What are the major operational risks?",
    "Discuss supply chain disruption risks.",
    "What customer concentration risks exist?",
    "Describe regulatory and compliance risks.",
    "How might rising interest rates affect this company?",
]
for s in samples:
    if st.sidebar.button(s, key=s):
        st.session_state["question"] = s

# Main input
question = st.text_area(
    "Your question",
    value=st.session_state.get("question", ""),
    height=80,
)

if st.button("Ask", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Retrieving and synthesizing..."):
            qa = CreditRiskQA(top_k=top_k)
            ticker = None if ticker_choice == "(All)" else ticker_choice
            result = qa.ask(question, ticker=ticker)

        st.subheader("Answer")
        st.markdown(result["answer"])

        st.subheader("Sources")
        for i, src in enumerate(result["sources"], 1):
            st.text(f"[Source {i}] {src}")

        with st.expander("Retrieved chunks (full text)"):
            for i, doc in enumerate(result["retrieved_chunks"], 1):
                st.markdown(f"**Source {i}** — `{doc.metadata['ticker']}`, "
                            f"chunk #{doc.metadata['chunk_id']}")
                st.text(doc.page_content[:600] + "...")
                st.markdown("---")
