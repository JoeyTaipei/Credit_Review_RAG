# Credit Review RAG Extension  
### SEC 10-K Risk Factors 問答模組｜Annual Credit Review Tool 延伸專案

本專案是 **Annual Credit Review Intelligence Tool** 的獨立 RAG extension，用來補足主專案中「結構化財務資料分析」無法涵蓋的非結構化文件風險訊號。

主專案處理：

```text
structured financial data
→ financial ratios
→ risk scoring
→ Tableau dashboard
→ auto-generated credit review reports
```

本 RAG extension 處理：

```text
SEC 10-K Risk Factors
→ text chunking
→ embeddings
→ Chroma vector store
→ RAG Q&A
→ answer with source citations
```

> **定位說明**  
> 本專案不是完整 production RAG system，也不是 autonomous AI agent。  
> 它是一個輕量級 prototype，用來展示如何將年報文字中的質化風險訊號加入授信覆審分析流程。

---

## 為什麼需要 RAG？

原本的授信覆審主專案主要分析結構化財務資料，例如：

- Revenue
- Net Income
- Debt Ratio
- Current Ratio
- Interest Coverage
- Altman Z' Score
- Risk Score
- Suggested Action

但真實授信覆審不只看財務數字。分析師也會閱讀年報中的文字資訊，例如：

- Risk Factors
- Management Discussion & Analysis
- Supply chain risks
- Customer demand risks
- Litigation risks
- Cybersecurity risks
- Macroeconomic risks

這些非結構化文字無法只靠財務比率捕捉。  
因此本專案加入 RAG，讓分析師可以問：

```text
What supply chain risks does Apple disclose?
What risks does Marriott disclose about travel demand?
What supply chain risks does Best Buy disclose?
```

系統會從 SEC 10-K Risk Factors 中找出相關段落，產生簡短回答，並附上來源引用。

---

## 專案成果

目前本專案已完成：

- 下載 SEC 10-K Risk Factors
- 擷取並儲存年報風險段落
- 使用 RecursiveCharacterTextSplitter 切分文件
- 使用 OpenAI `text-embedding-3-small` 建立 embeddings
- 使用 Chroma 建立本機 vector store
- 使用 LangChain 建立 RAG Q&A chain
- 回答公司風險問題並附上 source citations
- 已測試 AAPL、BBY、MAR 等公司問答

---

## Demo Preview

請將成功執行畫面截圖放在：

```text
docs/rag_demo_output.png
```

README 會顯示：

![RAG Demo Output](docs/rag_demo_output.png)

若圖片沒有顯示，請確認：

```text
docs/rag_demo_output.png
```

檔名大小寫完全一致。

---

## 目前 Demo 公司

目前建議展示以下公司：

| Ticker | Company | Demo Question |
|---|---|---|
| AAPL | Apple | What supply chain risks does Apple disclose? |
| BBY | Best Buy | What supply chain risks does Best Buy disclose? |
| MAR | Marriott | What risks does Marriott disclose about travel demand? |

Ford (`F`) 可作為延伸測試，但因 10-K chunks 較多，可能需要更穩定的 batching 或 rate-limit handling。

---

## 技術架構

| Component | Tool |
|---|---|
| Data Source | SEC EDGAR 10-K Risk Factors |
| Text Splitting | LangChain RecursiveCharacterTextSplitter |
| Embeddings | OpenAI `text-embedding-3-small` |
| Vector Store | Chroma |
| RAG Framework | LangChain LCEL |
| LLM | OpenAI `gpt-4o-mini` |
| Demo Interface | CLI；Streamlit optional |
| Environment | Python virtual environment |

---

## 專案結構

```text
Credit_review_RAG/
├── data/
│   ├── edgar_filings/          # SEC 10-K Risk Factors 原文
│   └── chroma_db_v2/           # Chroma vector store
│
├── docs/
│   ├── rag_demo_output.png     # RAG 成功執行截圖
│   └── rag_demo_results.md     # 整理後的 demo 問答結果
│
├── scripts/
│   ├── fetch_edgar_filings.py  # 下載 SEC 10-K Risk Factors
│   ├── build_vector_store.py   # 建立 embeddings + Chroma vector store
│   └── demo_app.py             # Streamlit demo，可選
│
├── src/
│   └── rag_credit_qa.py        # RAG Q&A chain
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Setup

### 1. 建立與啟動 virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 2. 安裝套件

```powershell
pip install -r requirements.txt
```

### 3. 建立 `.env`

在專案根目錄新增：

```text
.env
```

內容：

```env
OPENAI_API_KEY=your_api_key_here
```

請確認 `.gitignore` 包含：

```gitignore
.env
*.env
.venv/
data/chroma_db/
data/chroma_db_v2/
```

不要把 `.env` push 到 GitHub。

---

## 執行流程

### Phase 1：下載 SEC 10-K Risk Factors

```powershell
python scripts\fetch_edgar_filings.py
```

成功後會產生：

```text
data/edgar_filings/
├── AAPL_10K_risk_factors.txt
├── BBY_10K_risk_factors.txt
├── MAR_10K_risk_factors.txt
└── metadata.json
```

實際公司數量會依 `fetch_edgar_filings.py` 中的 ticker 設定而不同。

---

### Phase 2：建立 Vector Store

```powershell
python scripts\build_vector_store.py
```

成功後會看到類似：

```text
Embedding with text-embedding-3-small...
Vector store built
Collection size: xxxx chunks
Test query: What are the major operational risks?
Result 1: [BBY] ...
Result 2: [BBY] ...
Result 3: [MAR] ...
```

> Chunk 數量會依公司數量、10-K 長度與 chunk size 設定而變動。  
> 不要在 README 中寫死固定 chunk 數，例如 250 chunks。

目前成功使用的 Chroma path：

```text
data/chroma_db_v2/
```

---

### Phase 3：RAG Q&A 測試

#### Apple

```powershell
python src\rag_credit_qa.py -t AAPL -q "What supply chain risks does Apple disclose?"
```

#### Best Buy

```powershell
python src\rag_credit_qa.py -t BBY -q "What supply chain risks does Best Buy disclose?"
```

#### Marriott

```powershell
python src\rag_credit_qa.py -t MAR -q "What risks does Marriott disclose about travel demand?"
```

成功輸出會包含：

```text
ANSWER
...

SOURCES
[Source 1] ...
[Source 2] ...
[Source 3] ...
```

---

## Streamlit Demo

如果需要簡單 UI，可以執行：

```powershell
streamlit run scripts\demo_app.py
```

建議只做最小功能：

- 選擇 ticker
- 輸入問題
- 點擊 Ask
- 顯示 Answer
- 顯示 Sources

不建議在目前階段做過度複雜的 multi-page website 或自動產生完整報告系統，避免增加 bug。

---

## 面試 Talking Points

### 1. 為什麼用 RAG？

> 我原本的主專案處理的是 structured financial data，例如財務比率、風險分數和 Tableau dashboard。  
> 但真實授信覆審也會看年報中的非結構化文字，例如 Risk Factors、供應鏈風險、需求風險、訴訟和營運風險。  
> 因此我把 RAG 做成 extension，讓分析師可以針對 SEC 10-K 問質化風險問題，並看到來源引用。這不是為了硬加技術，而是補足結構化分析看不到的 qualitative risk signals。

---

### 2. 為什麼用 LangChain？

> 因為 RAG 需要組合多個元件：retriever、prompt、LLM 和 output parser。  
> LangChain LCEL 讓這些元件可以用 pipeline 的方式組合，也方便未來替換模型或 vector store。  
> 如果只是單一 LLM API call，我會直接用 OpenAI SDK；但這裡是 RAG workflow，所以 LangChain 比較合理。

---

### 3. 為什麼用 Chroma？

> Demo 階段選 Chroma，因為它是本機 vector store，不需要額外 server，也不需要額外 API key。  
> 如果進入 production，可以考慮 Pinecone、Weaviate，或和 PostgreSQL 整合更好的 pgvector。

---

### 4. 怎麼降低 hallucination？

本專案使用三層防護：

1. Prompt 明確要求只使用 retrieved context  
2. `temperature=0`，讓回答穩定  
3. 強制輸出 sources，讓分析師可以回到原始 10-K 段落驗證  

面試說法：

> 我不讓 LLM 自由回答，而是要求它只能根據 retrieved 10-K excerpts 回答，並附上來源。  
> 如果找不到答案，就應該回答 not enough information。這對金融業 auditability 很重要。

---

## 不要 Overclaim

| 不要說 | 建議說法 |
|---|---|
| 我做了一個 autonomous AI agent | 我做了一個 RAG Q&A module |
| 我訓練了 embedding model | 我使用 OpenAI 預訓練 embedding model |
| 我的 RAG 準確率很高 | 我完成 prototype 和 sanity check，尚未做 quantitative evaluation |
| 這是 production-ready system | 這是 prototype / next-phase extension |
| RAG 取代財務分析 | RAG 補足財務數字看不到的文字風險訊號 |

---

## 與主專案的關係

| Project | Data Type | Output | Purpose |
|---|---|---|---|
| Annual Credit Review Intelligence Tool | Structured financial data | Risk score, Tableau dashboard, Markdown reports | 財務數字分析與授信覆審 workflow |
| Credit Review RAG Extension | Unstructured annual report text | RAG Q&A with source citations | 補足年報文字中的質化風險分析 |

面試時可以這樣說：

> 我把專案分成兩層。  
> 第一層是已完成的 structured analytics pipeline，處理財務數字、風險分數、dashboard 和報告。  
> 第二層是 RAG extension，處理 SEC 10-K Risk Factors 這類 unstructured documents。  
> 兩者合起來，模擬授信覆審中「財務數字 + 文件風險」的分析流程。

---

## Known Issues / Troubleshooting

### 1. OpenAI API key 讀不到

確認 `.env` 在專案根目錄，並且變數名稱是：

```env
OPENAI_API_KEY=your_key
```

不是：

```env
OPEN_AI_API_KEY=your_key
```

---

### 2. Rate limit / TPM limit

如果看到：

```text
429 Too Many Requests
```

可以調低 embedding batch size：

```python
OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    chunk_size=10,
    max_retries=10,
    retry_min_seconds=10,
    retry_max_seconds=30,
)
```

---

### 3. Chroma HNSW index error

如果看到：

```text
Error loading hnsw index
```

建議：

1. 避免中文路徑，改用英文路徑，例如 `C:\Projects\Credit_review_RAG`
2. 刪除舊 vector store
3. 改用新的資料夾，例如 `data/chroma_db_v2`
4. 重新 build vector store

---

## Limitations

目前版本限制：

- 僅為 prototype，不是 production RAG system
- 目前 demo 公司數量有限
- 尚未做 Recall@k、faithfulness、answer quality 等正式 RAG evaluation
- 目前主要使用 SEC 10-K Risk Factors，未納入完整 10-K、新聞或產業報告
- LLM 回答仍需人工驗證，不應直接作為授信決策依據

---

## Future Improvements

未來可改進：

1. 加入更多公司與年度
2. 支援完整 10-K sections，例如 MD&A、Notes to Financial Statements
3. 加入 RAG evaluation，例如 Recall@k、source coverage、faithfulness
4. 改用 pgvector，和 PostgreSQL credit review pipeline 整合
5. 建立簡單 Streamlit UI
6. 將 RAG answer 加入 auto-generated credit review memo
7. 加入 human review log，記錄分析師是否接受或修改 LLM 回答

---

## 最短面試版說法

> 主專案處理 structured financial data，包含財務比率、風險分數、Tableau dashboard 和自動報告。  
> 這個 RAG extension 處理 unstructured annual report text，使用 SEC 10-K Risk Factors 建立 vector store，讓分析師可以問公司揭露的供應鏈、需求或營運風險，並看到來源引用。  
> 這樣 RAG 是為了解決真實的業務問題：授信覆審不只看財務數字，也需要閱讀年報文字風險。
