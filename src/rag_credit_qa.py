"""
rag_credit_qa.py
=================
Phase 3: RAG-powered Credit Risk Q&A.

Given a question (e.g., "What operational risks does Apple highlight?"),
the system:
  1. Embeds the question
  2. Retrieves top-k relevant chunks from the vector store
  3. Optionally filters by ticker
  4. Sends question + retrieved context to LLM
  5. Returns answer with source citations

Why these choices:
  - LangChain Expression Language (LCEL): cleanest way to compose RAG chains.
    Replaces deprecated RetrievalQA. Composable, streaming-friendly.
  - retriever.with_config: lets us swap k or filters at call time.
  - Custom prompt: enforces "cite sources" and "say 'not found' when unsure" —
    reduces hallucination, matches Deloitte's audit requirements.

Why not LangGraph / Agents?
  - This is a single-step Q&A, not a multi-tool agent.
  - LangGraph would be over-engineered. Defending YAGNI is professional.

Usage as library:
    from src.rag_credit_qa import CreditRiskQA
    qa = CreditRiskQA()
    result = qa.ask("What does AAPL say about supply chain risk?", ticker="AAPL")
    print(result["answer"])
    for src in result["sources"]:
        print(f"  - {src}")

Usage as CLI:
    python src/rag_credit_qa.py --ticker AAPL --question "supply chain risks?"
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# ─────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

CHROMA_DIR = PROJECT_ROOT / "data" / "chroma_db_v2"

EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0
DEFAULT_TOP_K = 5

# Prompt designed for credit risk audit context — emphasizes:
#   1. Only use retrieved context
#   2. Cite sources
#   3. Say "not found" rather than hallucinate
SYSTEM_PROMPT = """You are a credit risk analyst assistant for Deloitte's risk advisory practice.

Your job: answer questions about a company's risk factors using ONLY the
provided context from their 10-K filing's "Item 1A. Risk Factors" section.

Rules:
1. Use ONLY the context below. If the context doesn't contain the answer,
   reply: "Not enough information in the retrieved 10-K excerpts to answer this."
2. Cite every claim with [Source N] referring to the numbered context items.
3. Be concise. 3-5 bullet points maximum unless asked for more.
4. Use professional tone. This is for a credit committee.
5. If the question asks for opinion or prediction, decline and stick to
   what is stated in the filing.

Context:
{context}

Question: {question}

Answer (with citations):"""

PROMPT = ChatPromptTemplate.from_template(SYSTEM_PROMPT)


# ─────────────────────────────────────────────────────────────────────────
# Helper: format retrieved docs into context string
# ─────────────────────────────────────────────────────────────────────────

def format_docs(docs: list[Document]) -> str:
    """Format retrieved chunks as numbered context for the prompt."""
    blocks = []
    for i, doc in enumerate(docs, 1):
        ticker = doc.metadata.get("ticker", "?")
        chunk_id = doc.metadata.get("chunk_id", "?")
        blocks.append(
            f"[Source {i}] {ticker} 10-K Risk Factors (chunk #{chunk_id}):\n"
            f"{doc.page_content}"
        )
    return "\n\n".join(blocks)


# ─────────────────────────────────────────────────────────────────────────
# Main QA class
# ─────────────────────────────────────────────────────────────────────────

class CreditRiskQA:
    """
    RAG-based Q&A over 10-K Risk Factor sections.
    """

    def __init__(
        self,
        chroma_dir: Path | str = CHROMA_DIR,
        llm_model: str = LLM_MODEL,
        embedding_model: str = EMBEDDING_MODEL,
        top_k: int = DEFAULT_TOP_K,
    ):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found. Check .env location and variable name.")

        self.embeddings = OpenAIEmbeddings(
            model=embedding_model,
            api_key=api_key,
            chunk_size=10,
        )

        self.vectordb = Chroma(
            persist_directory=str(chroma_dir),
            embedding_function=self.embeddings,
            collection_name="credit_risk_filings",
        )

        self.llm = ChatOpenAI(
            model=llm_model,
            temperature=LLM_TEMPERATURE,
            api_key=api_key,
        )

        self.top_k = top_k

    def _build_chain(self, ticker: str | None = None):
        """Build RAG chain. If ticker given, filter retrieval to that company."""
        search_kwargs: dict[str, Any] = {"k": self.top_k}
        if ticker:
            search_kwargs["filter"] = {"ticker": ticker}

        retriever = self.vectordb.as_retriever(search_kwargs=search_kwargs)

        # LCEL pipeline: question → retrieve → format → prompt → LLM → string
        chain = (
            {
                "context": retriever | RunnableLambda(format_docs),
                "question": RunnablePassthrough(),
            }
            | PROMPT
            | self.llm
            | StrOutputParser()
        )
        return chain, retriever

    def ask(self, question: str, ticker: str | None = None) -> dict:
        """
        Ask a question, optionally restricted to one company.

        Returns:
            {
                "answer": str,
                "sources": list[str],
                "retrieved_chunks": list[Document],
            }
        """
        chain, retriever = self._build_chain(ticker)
        # Run retrieval separately so we can return source metadata
        retrieved_docs = retriever.invoke(question)
        answer = chain.invoke(question)

        sources = [
            f"{d.metadata['ticker']} 10-K Risk Factors, chunk #{d.metadata['chunk_id']} "
            f"({d.metadata.get('filing_url', '')})"
            for d in retrieved_docs
        ]

        return {
            "answer": answer,
            "sources": sources,
            "retrieved_chunks": retrieved_docs,
        }


# ─────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="RAG Credit Risk Q&A")
    parser.add_argument("--question", "-q", required=True, help="Your question")
    parser.add_argument("--ticker", "-t", default=None, help="Restrict to ticker (e.g., AAPL)")
    parser.add_argument("--top-k", "-k", type=int, default=DEFAULT_TOP_K)
    args = parser.parse_args()

    qa = CreditRiskQA(top_k=args.top_k)
    result = qa.ask(args.question, ticker=args.ticker)

    print("\n" + "=" * 70)
    print("ANSWER")
    print("=" * 70)
    print(result["answer"])

    print("\n" + "=" * 70)
    print("SOURCES")
    print("=" * 70)
    for i, src in enumerate(result["sources"], 1):
        print(f"  [Source {i}] {src}")


if __name__ == "__main__":
    main()
