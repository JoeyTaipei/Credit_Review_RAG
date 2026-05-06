# Risk Intelligent Dashboard 面試 Pitch（繁體中文）

這份文件幫助你在 intern / junior data analyst 面試中，用更清楚、更安全的方式介紹專案。定位重點是 analytics problem-solving，而不是深度金融專家或 production 系統。

---

## 30 秒 Pitch

```text
我做了一個小型 Risk Intelligent Dashboard prototype，用來模擬分析團隊如何監控和解釋風險訊號。

這個專案分成兩層：第一層是結構化資料分析，計算 debt ratio、current ratio、interest coverage、revenue growth、risk score 等 KRI，並用 dashboard 做風險排序和異常提醒。第二層是 RAG extension，使用 SEC 10-K Risk Factors，讓使用者可以針對公開揭露文件提問，並取得有來源引用的回答。

我把它定位成輔助分析師做 triage 和 drill-down 的 prototype，不是自動決策系統。它展示的是如何把數字指標、文件檢索、視覺化和人工覆核串成一個可解釋的分析流程。
```

---

## 90 秒 Pitch

```text
我可以分享一個 Risk Intelligent Dashboard prototype。這個專案的出發點是：在風險監控或授信覆審這類分析情境中，使用者不只需要看單一財務數字，也需要知道哪些對象值得優先檢查，以及風險變化背後可能有哪些文字揭露可以參考。

所以我把問題拆成兩個部分。第一部分是 structured analytics。我用 Python 建立資料流程，計算多個 KRI，例如 debt_ratio、current_ratio、interest_coverage、revenue_yoy、altman_z、anomaly_score、risk_score 和 risk_band。這些指標可以放進 Tableau dashboard，用來做 monitoring、ranking、filtering 和 drill-down report。

第二部分是 unstructured document analysis。我建立一個 RAG extension，使用 SEC 10-K Risk Factors 作為公開文件來源。流程包含文字擷取、chunking、OpenAI embeddings、Chroma vector store 和 LangChain RAG chain。使用者可以問風險揭露相關問題，系統會檢索相關段落，產生回答，並附上 source citations。

這個專案的價值不是取代分析師，也不是宣稱 production-ready，而是展示一個完整的 analytics workflow：先用 KRI 和 anomaly score 找出需要注意的案例，再用 dashboard 和 report 解釋數字，最後用 RAG 補充文件層面的質化風險，並保留人工覆核。
```

---

## Q1. Why this project?

```text
我想做的不只是單一 dashboard 或單一 LLM demo，而是一個更接近真實分析工作的 prototype。

很多分析問題不是只有「算出一個分數」，而是需要先定義指標、建立資料流程、排序優先順序、設計視覺化，最後還要能回到來源解釋原因。

所以我把專案定位成 Risk Intelligent Dashboard prototype，展示如何把 structured KRI monitoring 和 unstructured document Q&A 結合起來，讓使用者可以更快找到需要 drill down 的案例。
```

---

## Q2. What metrics / KRIs did you use?

```text
我把 KRI 分成幾類。

第一類是槓桿和償債能力，例如 debt_ratio 和 interest_coverage。

第二類是流動性，例如 current_ratio。

第三類是經營趨勢，例如 revenue_yoy。

第四類是 composite 或 ranking 指標，例如 altman_z、anomaly_score、risk_score 和 risk_band。

這些 KRI 的目的不是給出最終結論，而是讓 dashboard 可以做 monitoring、ranking 和 prioritization。使用者看到 high risk band 或 anomaly score 偏高時，可以再進入 drill-down report 查看原因。
```

---

## Q3. How does RAG add value?

```text
結構化指標可以告訴我們「哪裡可能有變化」，但不一定能解釋公開文件中揭露了什麼風險。

RAG 的價值是補足文字層面的資訊。使用者可以針對 SEC 10-K Risk Factors 提問，系統會檢索相關段落，產生簡短回答，並附上 source citations。

這讓分析流程更可檢查。使用者不是只看 LLM 的摘要，而是可以回到原始文件確認來源。
```

---

## Q4. How did you frame the problem?

```text
我一開始不是把問題 framed 成「我要做 AI」或「我要做模型」，而是從使用者工作流程出發。

我把問題定義成：

How can we help users monitor risk signals, prioritize cases, and explain risk changes using both structured metrics and source-backed document evidence?

因此，我的解法不是只有一個模型，而是一個 end-to-end analytics workflow：資料清理、KRI 計算、異常提醒、風險排序、dashboard、report、RAG Q&A 和 human review。
```

---

## Q5. What is the business impact?

```text
這個 prototype 的 business impact 是提高分析效率和可解釋性。

使用者可以先透過 dashboard 找出風險分數較高或異常分數較高的案例，不需要逐筆手動掃描所有資料。

接著可以透過 drill-down report 看到是哪幾個 KRI 造成風險升高。

最後，RAG Q&A 可以幫助使用者快速找到公開揭露文件中的相關段落，並用 source citations 支援人工覆核。

所以它的價值是把原本分散的數字分析、文件搜尋和報告整理，變成一個更有結構的分析流程。
```

---

## Q6. Why not supervised ML?

```text
我沒有加入 supervised ML，因為這個 prototype 沒有真實、可靠的標籤，例如正式違約標籤或人工審核結果。

在沒有標籤的情況下，硬做分類模型容易 overclaim。比較合理的做法是先建立可解釋的 KRI rules、risk score 和 anomaly score，用它們做監控、排序和人工覆核。

如果未來有足夠品質的歷史標籤，才適合評估是否加入 supervised model。
```

---

## Q7. How would you evaluate success?

```text
因為這是 prototype，我不會用 production model accuracy 來包裝它。

我會看幾個比較合理的成功標準：

第一，資料流程是否能穩定產生 dashboard-ready dataset。
第二，KRI threshold 和 risk_band 是否能清楚解釋。
第三，dashboard 是否能讓使用者快速找到需要優先檢查的案例。
第四，drill-down report 是否能說明主要風險指標。
第五，RAG answer 是否附上 source citations，讓使用者能回到原始文件驗證。
```

---

## Q8. What are the limitations?

```text
目前它是 prototype，不是 production-ready system。

KRI threshold 是示範規則，需要依照真實資料、產業和業務政策調整。

anomaly_score 是用於提醒，不是正式模型判斷。

RAG 回答依賴 retrieved context，仍需要人工覆核。

另外，目前沒有使用真實標籤做 supervised ML，也沒有宣稱可以自動做決策。
```

---

## Q9. What are the next steps?

```text
下一步我會做四件事。

第一，補強 KRI library，讓每個指標都有清楚的定義、threshold 和 dashboard 用法。

第二，加入更完整的 evaluation，例如 dashboard usability check、RAG source coverage 和 answer faithfulness。

第三，讓 drill-down report 更自動化，能清楚列出主要風險驅動因素。

第四，如果未來有可靠標籤，再評估是否加入 supervised ML；在目前階段，我會維持可解釋的 rules 和 human-in-the-loop。
```

---

## 最安全的一句話

```text
這個專案不是要證明我是金融專家，而是展示我如何把一個模糊的風險監控問題，拆成資料 pipeline、KRI monitoring、anomaly detection、dashboard、report 和 RAG-assisted document review 的完整分析流程。
```
