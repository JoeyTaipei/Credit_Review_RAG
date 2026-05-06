# RAG Extension 面試回答腳本  
### End-to-End Analytics Project 說法｜繁中版

這份腳本幫助你回答以下類型問題：

```text
Could you please walk me through an end-to-end analytics project you led?
How did you frame the problem, collect the data, analyze it, and drive business impact?

What metrics did you track or collect throughout the process to determine whether the project was successful?
```

---

## 1. 60 秒總回答

```text
我可以分享一個我做的 Credit Review RAG Extension。

這個專案的起點是：我原本已經有一個授信覆審分析工具，可以處理結構化財務資料，例如財務比率、風險分數和 dashboard。但我發現真實授信覆審不只看財務數字，分析師也會閱讀年報中的 Risk Factors，例如供應鏈風險、需求風險、營運風險和法律風險。

所以我把問題定義成：如何讓分析師能快速從長篇 10-K 年報中找到和信用風險相關的段落，並產生可驗證的回答？

我使用 SEC 10-K Risk Factors 作為資料來源，透過 Python 下載文件、切分文字、建立 embeddings，並用 Chroma 建立 vector store。接著我用 LangChain 建立 RAG 問答流程，讓使用者可以選公司並輸入問題，例如 “What supply chain risks does Apple disclose?” 系統會檢索相關段落，產生回答，並附上 source citations。

這個專案的 business value 是補足結構化財務分析看不到的質化風險，讓分析師更快理解公司在年報中揭露的風險，同時保留來源引用，方便人工覆核。
```

---

## 2. STAR / End-to-End 架構

### S — Situation：背景

```text
我原本的 credit review tool 已經可以分析結構化財務資料，但在真實授信覆審中，分析師還需要閱讀大量年報文字，例如 Risk Factors 和管理層討論。

這些文字資料很長，而且很難快速找到和某個問題相關的段落。
```

### T — Task：任務

```text
我的任務是建立一個 RAG prototype，讓分析師可以針對公司年報問質化風險問題，並取得有來源引用的回答。
```

### A — Action：行動

```text
我把流程拆成四步。

第一，資料蒐集。我從 SEC EDGAR 取得公司 10-K Risk Factors。

第二，資料處理。我用 Python 清理文字並用 RecursiveCharacterTextSplitter 切成 chunks。

第三，分析與檢索。我使用 OpenAI embeddings 將 chunks 轉成向量，存到 Chroma vector store，讓系統可以根據語意檢索相關段落。

第四，問答產出。我用 LangChain 組合 retriever、prompt、LLM 和 output parser，要求模型只能根據 retrieved context 回答，並附上 sources。
```

### R — Result：結果

```text
最後我完成了一個可以運作的 RAG Q&A prototype。它可以回答 AAPL、BBY、MAR 等公司在 10-K Risk Factors 中揭露的風險問題，並回傳來源引用。

這個成果展示了如何將 unstructured annual report text 加入 credit review workflow，讓分析師不只依賴財務數字，也能快速檢索質化風險訊號。
```

---

## 3. How did you frame the problem?

```text
我一開始不是從「我要做 RAG」出發，而是從業務問題出發。

原本的財務分析可以告訴我們一家公司風險分數變高，但它不一定能解釋公司自己在年報中揭露了哪些風險。

所以我把問題 framed 成：
How can we help analysts retrieve and summarize qualitative risk disclosures from long annual reports, while keeping the answer auditable?

這樣 RAG 就是合理的解法，因為它可以把問題連到原始文件段落，而不是讓 LLM 自由回答。
```

---

## 4. Data Collection：你怎麼蒐集資料？

```text
資料來源是 SEC EDGAR 上的 10-K 年報，主要使用 Item 1A. Risk Factors。

我選這個資料來源有三個原因：
第一，它是公開合法資料。
第二，Risk Factors 結構相對固定，適合做 RAG prototype。
第三，英文年報文字對 embedding 和 retrieval 品質比較穩定。
```

---

## 5. Data Processing：你怎麼處理資料？

```text
我把 10-K Risk Factors 下載後，先存成純文字檔，然後用 RecursiveCharacterTextSplitter 切成 chunks。

chunking 很重要，因為 10-K 文件很長，不能一次全部丟給 LLM。切成 chunks 後，系統才能針對問題檢索最相關的段落。
```

---

## 6. Analysis / Modeling：你怎麼分析？

```text
這個專案不是 supervised learning，也不是訓練模型。

我使用的是 RAG workflow：
先把文件 chunks 轉成 embeddings，存進 vector store。
當使用者問問題時，系統把問題也轉成 embedding，找出語意最接近的 chunks。
最後 LLM 只根據這些 retrieved chunks 產生回答。
```

簡化版：

```text
這個分析流程的核心不是預測，而是語意檢索與可追溯問答。
```

---

## 7. Business Impact：如何產生商業價值？

```text
這個 RAG extension 可以幫助分析師節省閱讀長篇年報的時間，快速定位和某個風險問題相關的段落。

它也補足結構化財務分析的不足。財務數字可以告訴我們風險分數或比率，但年報文字可以提供公司自己揭露的風險原因、外部環境和管理層觀點。

另外，source citations 讓回答可以被人工驗證，這對金融或風險分析場景很重要。
```

---

## 8. Metrics：你追蹤哪些指標？

| 類別 | Metric | 說明 |
|---|---|---|
| Data Coverage | 公司數量 | 目前 demo 使用 AAPL、BBY、MAR |
| Data Coverage | chunks 數量 | 每家公司被切成多少 chunks |
| Retrieval Quality | top-k retrieved chunks | 每次問題取回幾個相關 chunks |
| Source Traceability | sources returned | 回答是否附上來源 |
| Reliability | Not-found behavior | 找不到答案時是否避免亂回答 |
| Latency | query response time | 問答回應時間 |
| Cost | embedding / LLM cost | API 成本是否可控 |
| Usability | demo questions answered | 預設問題是否能成功回答 |

---

## 9. How did you determine success?

```text
因為這是 prototype，我沒有把成功定義成模型準確率，而是定義成 workflow 是否可用、可檢查、可延伸。

我主要看幾個指標：
第一，資料是否成功從 SEC 10-K 下載並切成 chunks。
第二，vector store 是否能成功建立，並回傳相關 chunks。
第三，LLM 回答是否有 source citations。
第四，回答是否能用原始 10-K 來源驗證。
第五，整個流程是否可以用不同公司和不同問題重複執行。
```

英文版：

```text
Because this is a prototype, I did not define success as model accuracy. I defined success as whether the workflow is usable, auditable, and extensible.

I tracked whether the filings were successfully collected, whether the documents were chunked and embedded, whether the vector store could retrieve relevant chunks, whether the answer included source citations, and whether the same workflow could work across multiple companies and questions.
```

---

## 10. What metrics did you track?

中文回答：

```text
我追蹤的 metrics 分成三類。

第一是 data pipeline metrics，例如成功下載幾家公司、每家公司產生多少 chunks、vector store collection size。

第二是 retrieval metrics，例如每個問題 top-k 取回哪些 chunks，以及 sources 是否和問題相關。

第三是 product / business metrics，例如回答是否有來源引用、分析師是否能回到原始文件驗證，以及這個流程是否能減少人工搜尋年報的時間。

因為目前是 prototype，我還沒有做 Recall@k 或 faithfulness 的正式 evaluation，但這會是下一步。
```

英文回答：

```text
I tracked three types of metrics.

First, pipeline metrics: number of filings collected, number of chunks generated, and vector store collection size.

Second, retrieval metrics: top-k retrieved chunks and whether the sources were relevant to the question.

Third, business usability metrics: whether the answer included citations, whether the analyst could verify the answer from the original filing, and whether the workflow reduced manual document search effort.

Since this is a prototype, I have not yet implemented formal RAG evaluation such as Recall@k or faithfulness scoring, but that would be a natural next step.
```

---

## 11. Why RAG instead of normal search?

```text
一般 keyword search 只能找完全符合關鍵字的段落，但風險揭露常常不是用同一個詞描述。

RAG 使用 embeddings 做 semantic search，所以即使用戶問的是 “travel demand risk”，系統也可能找到和 demand decline、economic conditions、travel restrictions 相關的段落。

此外，RAG 不只是找段落，也會把 retrieved context 整理成可讀的回答，並保留 source citations。
```

---

## 12. How did you reduce hallucination?

```text
我做了三個設計。

第一，prompt 要求模型只能根據 retrieved context 回答。
第二，temperature 設為 0，減少回答隨機性。
第三，回答必須附上 source citations，讓分析師可以回到原始 10-K 檢查。

如果 retrieved context 沒有答案，系統應該回答 not enough information，而不是猜。
```

---

## 13. What would you improve next?

```text
下一步我會做三件事。

第一，加入正式 RAG evaluation，例如 Recall@k、source coverage 和 faithfulness，衡量檢索和回答品質。

第二，擴充文件來源，不只 Risk Factors，也加入 MD&A、財務附註、新聞和產業報告。

第三，把 RAG 回答整合進自動化 credit review memo，讓分析師不只看到財務指標，也能看到公司自己揭露的質化風險。
```

---

## 14. 最安全 30 秒版本

```text
我做了一個 Credit Review RAG Extension，用 SEC 10-K Risk Factors 來回答質化信用風險問題。

我先從 SEC EDGAR 下載年報風險段落，接著用 Python 做文字切分，再用 OpenAI embeddings 和 Chroma 建立 vector store。當使用者輸入問題時，系統會檢索相關段落，讓 LLM 根據 retrieved context 回答，並附上來源引用。

這個專案的價值是補足結構化財務分析無法涵蓋的文字風險訊號，讓分析師可以更快找到公司在年報中揭露的供應鏈、需求或營運風險。
```

---

## 15. 最安全英文 60 秒版本

```text
I built a Credit Review RAG Extension to answer qualitative credit-risk questions from SEC 10-K Risk Factors.

The problem I wanted to solve is that structured financial analysis can show ratios and risk scores, but analysts also need to read annual report disclosures to understand qualitative risks such as supply chain risk, travel demand risk, operational risk, or litigation risk.

The workflow starts by collecting 10-K Risk Factors from SEC EDGAR. Then I split the text into chunks, embed the chunks using OpenAI embeddings, and store them in a Chroma vector database. When the user asks a question, the system retrieves the most relevant chunks and uses an LLM to generate an answer with source citations.

The business value is that analysts can search long filings more efficiently while still being able to verify the answer from the original source. This is a prototype, not a production system, but it demonstrates how unstructured document analysis can complement structured credit review analytics.
```
