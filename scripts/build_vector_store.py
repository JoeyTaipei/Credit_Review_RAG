"""
build_vector_store.py
======================
Phase 2: Chunk the 10-K Risk Factors text and build a Chroma vector store.

Why these choices:
  - RecursiveCharacterTextSplitter: splits on natural boundaries
    (paragraphs → sentences → words). Better than fixed-length splits
    because it preserves semantic coherence.
  - chunk_size=1000, chunk_overlap=150: standard for 10-K filings.
    Each chunk is ~1 paragraph; overlap prevents losing context at boundaries.
  - text-embedding-3-small: OpenAI's cheapest embedding model. Total cost
    for 5 companies × ~50K chars ≈ $0.005.
  - Chroma local persistence: no server, no Docker, just a folder.

Run:
  python scripts/build_vector_store.py
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from dotenv import load_dotenv   # 新增

# 載入專案根目錄的 .env
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")   # 新增from __future__ import annotations

import json
import logging
from pathlib import Path

from dotenv import load_dotenv   # 新增

# 載入專案根目錄的 .env
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")   # 新增

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────

FILINGS_DIR = PROJECT_ROOT / "data" / "edgar_filings"
CHROMA_DIR = PROJECT_ROOT / "data" / "chroma_db_v2"
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

EMBEDDING_MODEL = "text-embedding-3-small"


# ─────────────────────────────────────────────────────────────────────────
# Step 1: Load filings + chunk
# ─────────────────────────────────────────────────────────────────────────

def load_and_chunk_filings() -> list[Document]:
    """Read filings from disk, chunk them, attach metadata."""
    metadata_path = FILINGS_DIR / "metadata.json"
    metadata_list = json.loads(metadata_path.read_text(encoding="utf-8"))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    all_docs: list[Document] = []

    TARGET_TICKERS = {"AAPL", "MAR", "BBY"}
    for meta in metadata_list:
        if meta["ticker"] not in TARGET_TICKERS:
            continue

        ticker = meta["ticker"]
        filename = meta["filename"]
        filing_url = meta["filing_url"]

        text_path = FILINGS_DIR / filename
        text = text_path.read_text(encoding="utf-8")

        chunks = splitter.split_text(text)
        logger.info(f"[{ticker}] {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
                metadata={
                    "ticker": ticker,
                    "filing_url": filing_url,
                    "chunk_id": i,
                    "section": "Item 1A. Risk Factors",
                    "source": f"{ticker} 10-K (Risk Factors), chunk #{i}",
                },
            )
            all_docs.append(doc)

    logger.info(f"\nTotal: {len(all_docs)} chunks across {len(metadata_list)} companies")
    return all_docs


# ─────────────────────────────────────────────────────────────────────────
# Step 2: Build vector store
# ─────────────────────────────────────────────────────────────────────────

def build_vector_store(docs: list[Document]):
    """Embed and persist."""
    logger.info(f"\nEmbedding with {EMBEDDING_MODEL}...")
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        chunk_size=10,
        max_retries=10,
        retry_min_seconds=10,
        retry_max_seconds=30,
    )

    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name="credit_risk_filings",
    )

    logger.info(f"✓ Vector store built at {CHROMA_DIR}")
    logger.info(f"  Collection size: {vectordb._collection.count()} chunks")

    # Sanity check: do a test retrieval
    test_query = "What are the major operational risks?"
    results = vectordb.similarity_search(test_query, k=3)
    logger.info(f"\nTest query: '{test_query}'")
    for i, r in enumerate(results, 1):
        logger.info(f"  Result {i}: [{r.metadata['ticker']}] {r.page_content[:120]}...")


def main():
    if not (FILINGS_DIR / "metadata.json").exists():
        raise FileNotFoundError(
            "Run scripts/fetch_edgar_filings.py first to download filings."
        )

    docs = load_and_chunk_filings()
    build_vector_store(docs)


if __name__ == "__main__":
    main()
