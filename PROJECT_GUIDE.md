# Project Guide

這份文件是 `Credit_review_RAG` 的閱讀導覽，目標是讓 HR、面試官或工程讀者快速理解這個 portfolio project 的定位、輸出和文件結構。

---

## 一句話定位

這是一個小型 **Risk Intelligent Dashboard prototype**：用結構化 KRI 監控和風險排序展示 analytics problem-solving，再用 SEC 10-K Risk Factors RAG Q&A 補充可追溯來源的文字風險說明。

它不是 production-ready 系統，也不是自動決策工具。

---

## 建議閱讀順序

| 讀者 | 建議先讀 | 用途 |
|---|---|---|
| HR / Recruiter | `README.md` | 快速理解專案目的、技術和定位 |
| 面試官 / Hiring Manager | `PROJECT_GUIDE.md` | 快速看完整文件地圖 |
| Data Analyst / BI 讀者 | `docs/concept/risk_intelligent_dashboard_concept_zh.md` | 理解 dashboard、KRI、risk ranking 和 report 設計 |
| Engineer / AI 讀者 | `src/rag_credit_qa.py`、`scripts/`、`docs/demo_outputs/rag_demo_results_zh.md` | 理解 RAG pipeline 和實際輸出 |
| 我自己準備面試 | `docs/_prep/` | 面試講稿和回答練習，不是主要展示文件 |

---

## Project Outputs

目前專案可以展示的輸出分成三類：

| 類別 | 檔案 / 位置 | 說明 |
|---|---|---|
| 主 README | `README.md` | 專案介紹、技術架構、執行方式 |
| Risk dashboard concept | `docs/concept/risk_intelligent_dashboard_concept_zh.md` | 將專案包裝成 Risk Intelligent Dashboard prototype |
| KRI library | `docs/concept/kri_library_zh.md` | 整理 dashboard 可用的 KRI 指標、公式和面試說法 |
| RAG demo summary | `docs/demo_outputs/rag_demo_results_zh.md` | 繁體中文整理實際 CLI 輸出 |
| Raw CLI outputs | `docs/demo_outputs/*.txt` | 保留實際執行結果與 source citations |
| Interview prep | `docs/_prep/` | 自用面試腳本，放在較不顯眼的位置 |

---

## Folder Map

```text
Credit_review_RAG/
├── PROJECT_GUIDE.md
├── README.md
├── requirements.txt
│
├── src/
│   └── rag_credit_qa.py
│
├── scripts/
│   ├── fetch_edgar_filings.py
│   ├── build_vector_store.py
│   └── demo_app.py
│
├── docs/
│   ├── README.md
│   ├── concept/
│   │   ├── kri_library_zh.md
│   │   └── risk_intelligent_dashboard_concept_zh.md
│   │
│   ├── demo_outputs/
│   │   ├── rag_demo_results_zh.md
│   │   ├── rag_demo_results.md
│   │   └── *_rag_output.txt
│   │
│   └── _prep/
│       ├── interview_script_end_to_end_zh.md
│       └── interview_risk_dashboard_pitch_zh.md
│
└── data/
    ├── edgar_filings/
    ├── chroma_db/
    └── chroma_db_v2/
```

`data/`、`.env` 和 `.venv/` 是本機執行資料與環境，不應上傳或作為主要閱讀內容。

---

## What To Show In Portfolio

建議在履歷或 GitHub pin 中強調：

- Built a small Risk Intelligent Dashboard prototype
- Designed a KRI library for monitoring and risk ranking
- Added RAG Q&A over SEC 10-K Risk Factors
- Used OpenAI embeddings, Chroma, LangChain, and source citations
- Framed the system as human-in-the-loop, not automatic decision-making

---

## Suggested Next Output

下一個最值得補的是 Tableau dashboard 截圖或 Tableau Public 連結。它可以作為主要視覺輸出，讓 HR 和面試官一眼看到這不是只有程式碼或文件，而是一個完整 analytics prototype。
