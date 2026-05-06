# Credit Review RAG Extension

### 使用 SEC 10-K Risk Factors 的信用風險文件問答模組

本專案是一個 **RAG（Retrieval-Augmented Generation）文件問答 prototype**，用來示範如何將公司年報中的非結構化文字資料，轉換成可查詢、可追溯來源的風險分析工具。

它是授信覆審分析流程的延伸模組：主系統負責處理結構化財務數字，例如財務比率、風險分數與儀表板；本模組則補足年報文字中的質化風險訊號，例如供應鏈風險、旅遊需求風險、營運風險與外部環境風險。

---

## 專案目的

傳統的財務風險分析多半依賴結構化數字，例如收入、負債、利潤率或流動比率。  
但在真實的信用風險審查中，分析師也需要閱讀大量公司揭露文件，例如 10-K 年報中的 Risk Factors。

這些文件通常很長，不容易快速找到和特定風險相關的段落。  
因此，本專案建立一個 RAG 問答流程，讓使用者可以直接問：

```text
What supply chain risks does Apple disclose?
What risks does Marriott disclose about travel demand?
What supply chain risks does Best Buy disclose?
```

系統會從 SEC 10-K Risk Factors 中檢索相關段落，產生簡短回答，並附上來源引用，讓使用者可以回到原始文件驗證。

---

## 核心價值

本專案展示三個能力：

1. **非結構化資料處理**
  從 SEC 10-K 年報中擷取 Risk Factors 文字，並切分成適合檢索的 chunks。
2. **RAG 問答流程**
  使用 embeddings 與 Chroma vector store 找出相關段落，再由 LLM 根據 retrieved context 產生回答。
3. **可追溯來源的回答**
  每個回答都保留 source citations，避免讓 LLM 自由編造，並提高分析結果的可檢查性。

---

## 使用資料


| 資料來源                  | 說明           |
| --------------------- | ------------ |
| SEC EDGAR             | 美國上市公司公開揭露文件 |
| Form 10-K             | 年度報告         |
| Item 1A. Risk Factors | 公司揭露的主要風險因素  |
| Demo 公司               | AAPL、BBY、MAR |


目前 demo 使用數家公司作為 prototype 測試。公司數量可以擴充，但目前專案重點是展示完整 RAG workflow，而不是建立大規模 production search system。

---

## 系統流程

```text
SEC 10-K Risk Factors
        ↓
下載與擷取文字
        ↓
文字切分（chunking）
        ↓
OpenAI embeddings
        ↓
Chroma vector store
        ↓
Retriever 找出相關段落
        ↓
LLM 根據 retrieved context 回答
        ↓
輸出 answer + source citations
```

---

## 技術架構


| 類別              | 工具                                       |
| --------------- | ---------------------------------------- |
| 程式語言            | Python                                   |
| 資料來源            | SEC EDGAR                                |
| 文件切分            | LangChain RecursiveCharacterTextSplitter |
| Embedding Model | OpenAI text-embedding-3-small            |
| Vector Store    | Chroma                                   |
| RAG Framework   | LangChain LCEL                           |
| LLM             | OpenAI gpt-4o-mini                       |
| 介面              | CLI；Streamlit 可選                         |
| 版本控制            | Git / GitHub                             |


---

## 專案結構

```text
Credit_review_RAG/
├── data/
│   ├── edgar_filings/          # SEC 10-K Risk Factors 原文，不建議 push
│   └── chroma_db_v2/           # Chroma vector store，不建議 push
│
├── docs/
│   ├── rag_demo_output.png     # Demo 截圖
│   └── rag_demo_results_zh.md  # Demo 結果整理
│
├── scripts/
│   ├── fetch_edgar_filings.py  # 下載 SEC 10-K Risk Factors
│   ├── build_vector_store.py   # 建立 embeddings 與 vector store
│   └── demo_app.py             # Streamlit demo，可選
│
├── src/
│   └── rag_credit_qa.py        # RAG 問答主程式
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 快速開始

### 1. 建立 virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 2. 安裝套件

```powershell
pip install -r requirements.txt
```

### 3. 建立 `.env`

在專案根目錄建立 `.env`：

```env
OPENAI_API_KEY=your_api_key_here
```

請勿將 `.env` 上傳到 GitHub。

---

## 執行方式

### Phase 1：下載 SEC 10-K Risk Factors

```powershell
python scripts\fetch_edgar_filings.py
```

輸出位置：

```text
data/edgar_filings/
```

### Phase 2：建立 vector store

```powershell
python scripts\build_vector_store.py
```

輸出位置：

```text
data/chroma_db_v2/
```

### Phase 3：執行 RAG 問答

```powershell
python src\rag_credit_qa.py -t AAPL -q "What supply chain risks does Apple disclose?"
python src\rag_credit_qa.py -t BBY -q "What supply chain risks does Best Buy disclose?"
python src\rag_credit_qa.py -t MAR -q "What risks does Marriott disclose about travel demand?"
```

---

## Demo 結果

整理後的 demo 結果放在：

```text
docs/rag_demo_results_zh.md
```

成功執行畫面可放在：

```text
docs/rag_demo_output.png
```

README 顯示如下：

RAG Demo Output

---

## 為什麼用 RAG？

本專案的核心問題不是「如何讓 LLM 自由回答」，而是：

```text
如何從長篇公司揭露文件中，找出和特定信用風險問題相關的段落，並產生可驗證的回答？
```

RAG 適合這個問題，因為它可以：

- 從文件庫中檢索相關段落
- 限制 LLM 只能根據 retrieved context 回答
- 產生回答時附上來源
- 讓分析師可以回到原文驗證

---

## 如何降低 hallucination？

本專案使用三個設計降低 LLM 編造風險：

1. **Context-only prompt**
  Prompt 要求模型只能使用 retrieved context 回答。
2. **Temperature = 0**
  降低回答隨機性，讓輸出更穩定。
3. **Source citations**
  每個回答都附上來源 chunk，讓使用者可以回到原始文件檢查。

---

## 限制

目前版本仍是 prototype，有以下限制：

- Demo 公司數量有限
- 目前主要使用 SEC 10-K Risk Factors，未納入完整 10-K、新聞或產業報告
- 尚未進行正式 RAG evaluation，例如 Recall@k、faithfulness、answer quality
- LLM 回答仍需人工確認，不應直接作為正式信用決策
- Vector store 目前使用本機 Chroma，尚非 production 架構

---

## 未來改進

未來可以擴充：

1. 加入更多公司與年度
2. 支援更多 10-K sections，例如 MD&A、Notes to Financial Statements
3. 加入新聞、產業報告或公司公告
4. 建立 RAG evaluation，例如 Recall@k 與 faithfulness
5. 改用 pgvector，和 PostgreSQL 分析流程整合
6. 建立 Streamlit UI，讓使用者可選公司並輸入問題
7. 將 RAG 回答加入自動化信用審查報告初稿

---

## 專案定位

這個專案不是要取代分析師，也不是 production-ready credit risk system。  
它的目標是展示如何將非結構化公司揭露文件納入分析流程，幫助使用者更快找到和信用風險相關的質化資訊。

簡單來說：

```text
Structured financial analytics tells us what changed.
RAG over filings helps us understand what the company disclosed about possible risks.
```