# RAG Demo Results（繁體中文）

本文件整理 `Credit_review_RAG` 專案的實際 CLI demo 輸出，重點是展示 RAG extension 如何從 SEC 10-K Risk Factors 中檢索相關段落，產生可回溯來源的風險問答。

---

## 專案目的

`Credit_review_RAG` 是 Annual Credit Review Intelligence Tool 的 RAG 延伸模組，不是 autonomous agent。主專案處理結構化財務資料，例如財務比率、風險分數、Tableau dashboard 與授信覆審報告；本模組則補足非結構化年報文字中的質化風險訊號。

這個 demo 使用 SEC 10-K Risk Factors 作為資料來源，透過 LangChain 建立 RAG 問答流程，使用 OpenAI embeddings 將文件段落向量化，儲存在本機 Chroma vector store，並在回答中保留 source citations，方便分析師回到原始 10-K 來源驗證。

---

## Demo 設計

Demo 以 CLI 方式針對三家公司提出風險問題：

| Ticker | 公司 | 問題主題 |
|---|---|---|
| AAPL | Apple | 供應鏈風險 |
| BBY | Best Buy | 供應鏈風險 |
| MAR | Marriott | 旅遊需求風險 |

流程設計如下：

1. 從 SEC 10-K Risk Factors 擷取公司風險揭露文字。
2. 將文字切成 chunks，建立 OpenAI embeddings。
3. 將向量與 metadata 儲存在 Chroma。
4. 使用 LangChain RAG chain 依 ticker 與問題檢索相關 chunks。
5. 產生簡短回答，並列出 CLI 輸出的來源引用。

---

## AAPL：Apple 供應鏈風險

**CLI 問題**

```text
What supply chain risks does Apple disclose?
```

**回答摘要**

Apple 的 10-K 風險揭露指出，公司面臨供應短缺與價格上升的風險，這些因素可能影響營運結果、財務狀況與股價。Apple 也依賴零組件供應商；若供應商營運失敗、整併，或轉向更通用的零組件，可能使 Apple 難以用商業上合理的條件取得所需零件。此外，Apple 大部分硬體產品由外包夥伴製造，且主要位於亞洲，因此供應鏈集中度與地理區域因素也是重要風險。

**CLI 來源引用**

```text
[Source 1] AAPL 10-K Risk Factors, chunk #71 (https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm)
[Source 2] AAPL 10-K Risk Factors, chunk #45 (https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm)
[Source 3] AAPL 10-K Risk Factors, chunk #112 (https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm)
[Source 4] AAPL 10-K Risk Factors, chunk #232 (https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm)
[Source 5] AAPL 10-K Risk Factors, chunk #91 (https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm)
```

---

## BBY：Best Buy 供應鏈風險

**CLI 問題**

```text
What supply chain risks does Best Buy disclose?
```

**回答摘要**

Best Buy 的 CLI 回答聚焦於零售與供應鏈營運基礎設施。公司揭露的風險包含：維護與升級支援零售及供應鏈作業的技術基礎設施、運輸途中或門市與其他設施中的員工、顧客與庫存安全、第三方是否能符合公司標準或承諾，以及履約服務、退貨處理等供應鏈容量需求成長所帶來的挑戰。CLI 輸出也指出，運輸與配送產業若出現整併、企業倒閉或更高政治審查，可能不利於營運。

**CLI 來源引用**

```text
[Source 1] BBY 10-K Risk Factors, chunk #66 (https://www.sec.gov/Archives/edgar/data/764478/000076447826000009/bby-20260131.htm)
[Source 2] BBY 10-K Risk Factors, chunk #65 (https://www.sec.gov/Archives/edgar/data/764478/000076447826000009/bby-20260131.htm)
[Source 3] BBY 10-K Risk Factors, chunk #102 (https://www.sec.gov/Archives/edgar/data/764478/000076447826000009/bby-20260131.htm)
[Source 4] BBY 10-K Risk Factors, chunk #223 (https://www.sec.gov/Archives/edgar/data/764478/000076447826000009/bby-20260131.htm)
[Source 5] BBY 10-K Risk Factors, chunk #105 (https://www.sec.gov/Archives/edgar/data/764478/000076447826000009/bby-20260131.htm)
```

---

## MAR：Marriott 旅遊需求風險

**CLI 問題**

```text
What risks does Marriott disclose about travel demand?
```

**回答摘要**

Marriott 的 CLI 回答指出，旅遊需求可能因多種因素波動，進而對業務、流動性、財務狀況與營運結果造成不利影響。不過，檢索到的 10-K excerpts 對「旅遊需求」的具體情境或趨勢說明有限；CLI 輸出最後也明確表示 retrieved excerpts 中資訊不足，無法完整回答此問題。這是一個很好的 demo 範例，說明 RAG 不應在檢索證據不足時過度延伸。

**CLI 來源引用**

```text
[Source 1] MAR 10-K Risk Factors, chunk #66 (https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231.htm)
[Source 2] MAR 10-K Risk Factors, chunk #363 (https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231.htm)
[Source 3] MAR 10-K Risk Factors, chunk #58 (https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231.htm)
[Source 4] MAR 10-K Risk Factors, chunk #135 (https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231.htm)
[Source 5] MAR 10-K Risk Factors, chunk #29 (https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231.htm)
```

---

## 限制

- 本專案是 prototype / RAG extension，不是 production-ready RAG system，也不是 autonomous agent。
- Demo 目前只涵蓋少數公司與單一年度的 SEC 10-K Risk Factors。
- 回答品質取決於 retrieval 結果；若檢索到的 excerpts 資訊不足，系統應承認不足，而不是自行補完。
- 尚未進行正式 RAG evaluation，例如 Recall@k、faithfulness、source coverage 或 answer quality 評估。
- 目前主要使用 Risk Factors，尚未納入完整 10-K、新聞、產業報告或內部授信資料。
- LLM 回答應作為分析輔助，不應直接作為授信決策依據。

---

## 面試 Talking Point

可以這樣說明：

> 我把這個專案定位成 Annual Credit Review Tool 的 RAG extension，而不是 autonomous agent。主專案處理結構化財務資料，例如 ratios、risk score、dashboard 和 report；RAG extension 則處理 SEC 10-K Risk Factors 這類非結構化文字。它使用 OpenAI embeddings、Chroma vector store 和 LangChain RAG pipeline，讓分析師能針對供應鏈、需求或營運風險提問，並看到 source citations 回到原始 10-K 驗證。重點不是讓 LLM 自動做授信決策，而是補足財務數字看不到的 qualitative risk signals。
