"""
fetch_edgar_filings.py
=======================
Phase 1: Download 10-K filings (Item 1A Risk Factors) from SEC EDGAR.

SEC EDGAR is free and does not require an API key. We just need to
identify ourselves with a User-Agent header (required by SEC).

Strategy:
  1. For each ticker, look up CIK number via SEC's company tickers JSON
  2. Get the most recent 10-K filing URL via EDGAR submissions API
  3. Download the 10-K HTML
  4. Extract Item 1A "Risk Factors" section
  5. Save as plain text to data/edgar_filings/

Run:
  python scripts/fetch_edgar_filings.py
"""

from __future__ import annotations

import json
import logging
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────

# IMPORTANT: SEC requires a real User-Agent. Replace with your name + email.
HEADERS = {
    "User-Agent": "e64992019@gs.ncku.edu.tw",
    "Accept-Encoding": "gzip, deflate",
    "Host": "data.sec.gov",
}

HEADERS_WWW = {
    "User-Agent": "e64992019@gs.ncku.edu.tw",
    "Accept-Encoding": "gzip, deflate",
}

# 5 公司，覆蓋不同產業，貼近你既有專案的故事
TICKERS = ["TSM", "AAPL", "F", "MAR", "BBY"]

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "edgar_filings"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# SEC requires polite rate limiting: ≤ 10 requests/second
REQUEST_DELAY = 0.5


# ─────────────────────────────────────────────────────────────────────────
# Step 1: ticker → CIK lookup
# ─────────────────────────────────────────────────────────────────────────

def get_cik_map() -> dict:
    """Fetch SEC's official ticker-to-CIK mapping."""
    url = "https://www.sec.gov/files/company_tickers.json"
    resp = requests.get(url, headers=HEADERS_WWW, timeout=30)
    resp.raise_for_status()
    raw = resp.json()
    # Format is {"0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."}, ...}
    return {row["ticker"]: str(row["cik_str"]).zfill(10) for row in raw.values()}


# ─────────────────────────────────────────────────────────────────────────
# Step 2: CIK → most recent 10-K filing URL
# ─────────────────────────────────────────────────────────────────────────

def get_latest_10k_url(cik: str, ticker: str) -> str | None:
    """Get the URL of the most recent 10-K filing for a CIK."""
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    recent = data["filings"]["recent"]
    forms = recent["form"]
    accession_numbers = recent["accessionNumber"]
    primary_documents = recent["primaryDocument"]

    for i, form in enumerate(forms):
        if form == "10-K":
            accession = accession_numbers[i].replace("-", "")
            doc = primary_documents[i]
            # Construct the filing URL
            filing_url = (
                f"https://www.sec.gov/Archives/edgar/data/"
                f"{int(cik)}/{accession}/{doc}"
            )
            logger.info(f"  {ticker}: found 10-K → {filing_url}")
            return filing_url
    return None


# ─────────────────────────────────────────────────────────────────────────
# Step 3: Extract Item 1A Risk Factors section from 10-K HTML
# ─────────────────────────────────────────────────────────────────────────

def extract_risk_factors(html: str) -> str:
    """Extract Item 1A. Risk Factors section from 10-K HTML."""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n")

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Try to find "Item 1A" to "Item 1B" or "Item 2" section
    # Use case-insensitive match because filings vary
    pattern = re.compile(
        r"item\s*1a[\.\s]*risk\s*factors(.*?)(item\s*1b|item\s*2[\.\s])",
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(text)
    if match:
        risk_text = match.group(1).strip()
        # If too short, probably matched wrong place
        if len(risk_text) > 1000:
            return risk_text

    # Fallback: return whole text and let the chunker handle it
    logger.warning("  Could not isolate Item 1A; using full text")
    return text


# ─────────────────────────────────────────────────────────────────────────
# Step 4: Main pipeline
# ─────────────────────────────────────────────────────────────────────────

def main():
    logger.info("=" * 60)
    logger.info("Fetching 10-K Item 1A Risk Factors from SEC EDGAR")
    logger.info("=" * 60)

    logger.info("Loading CIK map...")
    cik_map = get_cik_map()
    time.sleep(REQUEST_DELAY)

    metadata = []

    for ticker in TICKERS:
        logger.info(f"\n[{ticker}]")
        cik = cik_map.get(ticker)
        if not cik:
            logger.error(f"  CIK not found for {ticker}")
            continue

        try:
            # Get filing URL
            filing_url = get_latest_10k_url(cik, ticker)
            time.sleep(REQUEST_DELAY)
            if not filing_url:
                logger.warning(f"  No 10-K found for {ticker}")
                continue

            # Download 10-K HTML
            logger.info("  Downloading 10-K...")
            resp = requests.get(filing_url, headers=HEADERS_WWW, timeout=60)
            resp.raise_for_status()
            html = resp.text
            time.sleep(REQUEST_DELAY)

            # Extract Risk Factors
            logger.info("  Extracting Item 1A...")
            risk_text = extract_risk_factors(html)

            # Save to disk
            output_path = OUTPUT_DIR / f"{ticker}_10K_risk_factors.txt"
            output_path.write_text(risk_text, encoding="utf-8")
            logger.info(f"  ✓ Saved to {output_path.name} ({len(risk_text):,} chars)")

            metadata.append({
                "ticker": ticker,
                "cik": cik,
                "filing_url": filing_url,
                "filename": output_path.name,
                "char_count": len(risk_text),
            })

        except requests.HTTPError as e:
            logger.error(f"  HTTP error for {ticker}: {e}")
        except Exception as e:
            logger.error(f"  Failed {ticker}: {e}")

    # Save metadata for downstream RAG
    meta_path = OUTPUT_DIR / "metadata.json"
    meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))
    logger.info(f"\n✓ Metadata saved to {meta_path}")
    logger.info(f"✓ Successfully fetched {len(metadata)}/{len(TICKERS)} filings")


if __name__ == "__main__":
    main()
