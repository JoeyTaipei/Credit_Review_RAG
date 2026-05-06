# Risk Intelligent Dashboard Prototype Concept（繁體中文）

本文件說明如何把結構化授信覆審分析專案與 SEC 10-K Risk Factors RAG extension，包裝成一個小型 **Risk Intelligent Dashboard prototype**。重點不是深度金融專業，也不是 production-ready 系統，而是展示資料分析問題解決能力。

---

## 專案定位

這個 prototype 模擬一個風險監控 dashboard，幫助使用者回答三個問題：

1. 哪些對象的風險指標正在變差？
2. 哪些指標造成風險排序上升？
3. 公開揭露文件中是否有可以輔助解釋的質化風險訊號？

它把 structured analytics 和 unstructured document Q&A 放在同一個分析流程中：

```text
structured financial data
→ KRI monitoring
→ anomaly detection
→ risk ranking
→ Tableau visualization
→ drill-down report
→ RAG Q&A over risk disclosures
→ human review
```

---

## 解決的分析問題

單看財務數字時，使用者可能知道某個分數變高，但不一定知道原因。單看長篇文件時，使用者又可能花很多時間搜尋相關段落。

因此，這個 prototype 的問題定義是：

```text
如何把結構化 KRI 指標和非結構化風險揭露文字整合起來，
讓使用者能更快排序、理解和覆核潛在風險？
```

---

## Data Pipeline

資料流程分成兩條線。

**Structured pipeline**

```text
raw financial data
→ clean and transform
→ calculate KRIs
→ generate risk_score and risk_band
→ export dashboard/report-ready dataset
```

**Unstructured RAG pipeline**

```text
SEC 10-K Risk Factors
→ text extraction
→ chunking
→ OpenAI embeddings
→ Chroma vector store
→ LangChain retriever and Q&A chain
→ answer with source citations
```

這樣的設計讓 dashboard 可以同時呈現數字面和文字面資訊。

---

## KRI Monitoring

KRI monitoring 是 dashboard 的基礎。prototype 可追蹤：

- `debt_ratio`：槓桿程度
- `current_ratio`：短期流動性
- `interest_coverage`：利息覆蓋能力
- `revenue_yoy`：收入成長或衰退
- `altman_z`：多指標合成的財務壓力參考
- `anomaly_score`：是否偏離一般樣態
- `risk_score`：排序用的綜合分數
- `risk_band`：Low / Medium / High 分群

這些指標讓使用者可以從 dashboard 快速看出「誰需要先被檢查」和「哪個指標正在推升風險」。

---

## Anomaly Detection

這裡的 anomaly detection 不需要 supervised labels。它可以先用規則式或無監督方法，例如：

- 觀察 KRI 是否超過 threshold
- 比較同一對象前後期間的變化
- 使用 z-score 或 percentile 找出偏離常態的觀察值
- 計算多個 KRI 的綜合異常分數

這種設計適合 junior data analyst portfolio，因為它誠實地展示「沒有真實標籤時，先做可解釋的異常提醒」，而不是硬把問題包裝成 supervised ML。

---

## Risk Ranking

`risk_score` 和 `risk_band` 用來做 portfolio triage，也就是排序和優先處理。

Dashboard 可以依照 `risk_score` 由高到低排列，並提供 filter：

- risk_band
- 指標是否超過 threshold
- revenue_yoy 是否轉負
- anomaly_score 是否偏高
- 是否有 RAG 補充說明

這讓使用者不必逐筆閱讀所有資料，而是先看最值得注意的項目。

---

## Tableau Visualization

Tableau dashboard 可以模擬以下視覺化：

- KPI cards：High risk 數量、平均 risk_score、異常案例數
- Risk ranking table：依 risk_score 排序
- Trend chart：觀察 KRI 隨時間變化
- Heatmap：各 KRI 是否超過 threshold
- Scatter plot：比較槓桿、流動性與風險分數
- Filter panel：依 risk_band、年度、產業或資料群組篩選

視覺化的目標不是做漂亮圖表而已，而是讓使用者更快定位問題。

---

## Drill-down Reports

Dashboard 可以連到 drill-down report，針對單一對象整理：

- risk_band 和 risk_score
- 主要惡化的 KRI
- 異常分數來源
- 趨勢說明
- RAG 問答摘要
- source citations
- human review note

這讓分析結果從「總覽」進一步變成可解釋的分析記錄。

---

## RAG Q&A

RAG extension 的角色是補足結構化指標看不到的質化資訊。

使用者可以問：

```text
What risks are disclosed about supply chain?
What risks are disclosed about demand?
What operational risks are discussed?
```

系統會從 SEC 10-K Risk Factors 中檢索相關段落，產生簡短回答，並附上 source citations。這讓使用者可以回到原始文件驗證，而不是只相信 LLM 的文字。

---

## Human-in-the-loop

這個 prototype 不自動做正式決策。Human-in-the-loop 是重要設計：

- Dashboard 負責排序和提醒。
- Report 負責整理指標和原因。
- RAG 負責協助搜尋和摘要文字揭露。
- 使用者負責覆核來源、判斷背景、更新結論。

這樣的定位比較安全，也更符合 intern / junior data analyst 面試中的期待。

---

## 不 overclaim 的說法

建議說：

```text
This is a small Risk Intelligent Dashboard prototype.
It combines KRI monitoring, anomaly detection, risk ranking, visualization,
drill-down reporting, and RAG-assisted document review.
```

避免說：

```text
This is a production credit risk system.
This automatically makes credit decisions.
This is a supervised ML default prediction model.
```

---

## Portfolio 重點

這個專案最適合展現的能力是：

- 把模糊業務問題拆成資料流程
- 設計可解釋的 KRI library
- 建立排序和異常提醒邏輯
- 用 Tableau 呈現可掃描的 dashboard
- 用 RAG 補足文件搜尋和來源追溯
- 清楚說明 prototype 限制與下一步

總結一句：

> 這個 prototype 展示的是 analytics problem-solving：如何把數字指標、異常偵測、視覺化和文件問答整合成一個可解釋、可覆核的風險分析工作流。
