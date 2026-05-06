# KRI Library（繁體中文）

本文件整理 Risk Intelligent Dashboard prototype 中可使用的 KRI（Key Risk Indicator，關鍵風險指標）。KRI 可以理解成「用來提醒風險可能升高的觀察指標」。它不是單一決策答案，而是幫助分析師快速掃描、排序、追蹤和解釋風險變化。

這些 threshold 是 prototype 用的示範規則，目的是讓 dashboard 和 report 有清楚的解讀邏輯；正式使用前應依產業、公司規模、資料品質和業務政策調整。

---

## 1. debt_ratio

**意思**

`debt_ratio` 衡量公司資產中有多少比例由負債支撐。數值越高，代表槓桿程度越高，財務彈性可能越低。

**公式**

```text
debt_ratio = total_liabilities / total_assets
```

**示範 threshold**

| Band | 條件 |
|---|---|
| Low Risk | debt_ratio < 0.50 |
| Medium Risk | 0.50 <= debt_ratio < 0.70 |
| High Risk | debt_ratio >= 0.70 |

**為什麼重要**

高負債比可能表示公司在景氣下行、利率上升或收入下滑時，承受壓力的空間較小。

**Dashboard / Report 用法**

- Dashboard：用顏色標示槓桿偏高的公司或期間。
- Report：說明負債比例是否升高，以及是否和其他 KRI 一起惡化。

**面試說法**

> 我把 debt_ratio 當成槓桿風險的簡單 KRI。它不直接代表違約，但可以提醒使用者哪些公司或期間的財務彈性可能變弱。

---

## 2. current_ratio

**意思**

`current_ratio` 衡量短期資產是否足以覆蓋短期負債。數值越低，短期流動性壓力可能越高。

**公式**

```text
current_ratio = current_assets / current_liabilities
```

**示範 threshold**

| Band | 條件 |
|---|---|
| Low Risk | current_ratio >= 1.5 |
| Medium Risk | 1.0 <= current_ratio < 1.5 |
| High Risk | current_ratio < 1.0 |

**為什麼重要**

如果短期資產不足以覆蓋短期負債，公司可能需要依賴再融資、延後付款或其他資金來源。

**Dashboard / Report 用法**

- Dashboard：追蹤流動性是否低於門檻。
- Report：解釋短期償債能力是否需要進一步人工覆核。

**面試說法**

> current_ratio 是流動性 KRI。我用它幫助 dashboard 快速顯示短期資金壓力，而不是把它當成完整的信用判斷。

---

## 3. interest_coverage

**意思**

`interest_coverage` 衡量營業獲利可以覆蓋利息費用幾倍。數值越低，代表利息負擔相對較重。

**公式**

```text
interest_coverage = EBIT / interest_expense
```

**示範 threshold**

| Band | 條件 |
|---|---|
| Low Risk | interest_coverage >= 4.0 |
| Medium Risk | 2.0 <= interest_coverage < 4.0 |
| High Risk | interest_coverage < 2.0 |

**為什麼重要**

當利息覆蓋倍數下降，公司可能更容易受到獲利下滑或利率上升影響。

**Dashboard / Report 用法**

- Dashboard：標示利息覆蓋倍數快速下降的對象。
- Report：搭配收入成長率和負債比，說明財務壓力是否集中出現。

**面試說法**

> interest_coverage 讓我把「獲利是否足以支撐利息」轉成可監控指標，適合放在風險排序和 drill-down report。

---

## 4. revenue_yoy

**意思**

`revenue_yoy` 衡量收入相較前一年是否成長或衰退。

**公式**

```text
revenue_yoy = (revenue_current_year - revenue_previous_year) / revenue_previous_year
```

**示範 threshold**

| Band | 條件 |
|---|---|
| Low Risk | revenue_yoy >= 0% |
| Medium Risk | -10% <= revenue_yoy < 0% |
| High Risk | revenue_yoy < -10% |

**為什麼重要**

收入下滑可能影響現金流、獲利能力和償債能力。它也常是其他風險指標惡化前的早期訊號。

**Dashboard / Report 用法**

- Dashboard：顯示收入年增率趨勢。
- Report：說明收入變化是否和風險分數上升有關。

**面試說法**

> revenue_yoy 是經營動能的 KRI。我用它觀察收入是否轉弱，再和流動性、槓桿和異常分數一起看。

---

## 5. altman_z

**意思**

`altman_z` 是一個把多個財務比率合成的風險參考分數，常用來觀察公司財務壓力。這裡把它作為 prototype 的教育性 KRI，不把它解讀成正式模型結論。

**公式**

```text
altman_z =
  1.2 * working_capital / total_assets
+ 1.4 * retained_earnings / total_assets
+ 3.3 * EBIT / total_assets
+ 0.6 * market_value_equity / total_liabilities
+ 1.0 * sales / total_assets
```

**示範 threshold**

| Band | 條件 |
|---|---|
| Low Risk | altman_z > 2.99 |
| Medium Risk | 1.81 <= altman_z <= 2.99 |
| High Risk | altman_z < 1.81 |

**為什麼重要**

它把流動性、累積獲利、營運獲利、槓桿和資產效率放在同一個參考分數中，適合做初步排序。

**Dashboard / Report 用法**

- Dashboard：作為 summary score 之一，輔助排序。
- Report：提醒使用者分數下降的主要可能來源。

**面試說法**

> 我使用 altman_z 作為可解釋的 composite KRI，而不是宣稱它是完整預測模型。它的價值是把多個財務面向整理成一個容易比較的訊號。

---

## 6. anomaly_score

**意思**

`anomaly_score` 用來標示某個公司或期間的指標組合是否和一般樣態不同。這裡建議使用規則式或無監督方式，不使用沒有標籤支撐的 supervised ML。

**範例公式**

```text
anomaly_score = normalized average of absolute z-scores across selected KRIs
```

或：

```text
anomaly_score = percentile rank of unusualness across observations
```

**示範 threshold**

| Band | 條件 |
|---|---|
| Low Risk | anomaly_score < 60 |
| Medium Risk | 60 <= anomaly_score < 80 |
| High Risk | anomaly_score >= 80 |

**為什麼重要**

有些風險不是單一比率超標，而是多個指標同時偏離常態。異常分數可以幫助 dashboard 找出值得人工檢查的案例。

**Dashboard / Report 用法**

- Dashboard：高亮顯示異常排名靠前的對象。
- Report：列出哪些 KRI 對異常分數貢獻最大。

**面試說法**

> 我沒有在沒有標籤的情況下硬做 supervised ML，而是把 anomaly_score 定位成無監督或規則式的早期提醒，讓使用者知道哪些案例值得 drill down。

---

## 7. risk_score

**意思**

`risk_score` 是把多個 KRI 綜合成一個 dashboard 排序分數。它不是正式信用評等，而是 prototype 中用來排序和篩選的分析分數。

**範例公式**

```text
risk_score =
  0.25 * debt_ratio_score
+ 0.20 * current_ratio_score
+ 0.20 * interest_coverage_score
+ 0.15 * revenue_yoy_score
+ 0.10 * altman_z_score
+ 0.10 * anomaly_score
```

**示範 threshold**

| Band | 條件 |
|---|---|
| Low Risk | risk_score < 40 |
| Medium Risk | 40 <= risk_score < 70 |
| High Risk | risk_score >= 70 |

**為什麼重要**

Dashboard 需要一個可以排序的欄位，讓使用者先看最需要注意的項目。risk_score 的重點是透明、可解釋、可調整。

**Dashboard / Report 用法**

- Dashboard：依 risk_score 排序。
- Report：顯示分數來源，避免只有黑箱結果。

**面試說法**

> risk_score 是 portfolio triage 的工具。它幫助使用者決定先看誰，但最後仍需要人根據資料和業務背景覆核。

---

## 8. risk_band

**意思**

`risk_band` 把連續的 `risk_score` 轉成易讀的分群，例如 Low、Medium、High。

**公式**

```text
risk_band =
  Low if risk_score < 40
  Medium if 40 <= risk_score < 70
  High if risk_score >= 70
```

**示範 threshold**

| Band | 條件 |
|---|---|
| Low | risk_score < 40 |
| Medium | 40 <= risk_score < 70 |
| High | risk_score >= 70 |

**為什麼重要**

使用者不一定想先看所有原始數字。risk_band 可以讓 dashboard、report 和簡報更容易掃描。

**Dashboard / Report 用法**

- Dashboard：用顏色、filter 和 summary cards 顯示風險分群。
- Report：用 risk_band 作為段落開頭，再展開關鍵 KRI 和文字風險來源。

**面試說法**

> risk_band 讓分析結果更容易被非技術使用者理解。它不是最終判斷，而是把複雜指標整理成可行動的 prioritization layer。

---

## 總結說法

> 這套 KRI library 的目的不是建立深度金融模型，而是把常見財務和營運訊號整理成 dashboard 可以監控、排序、解釋的欄位。它展示的是資料分析問題解決能力：如何定義指標、設定可解釋規則、呈現趨勢和異常，最後讓使用者能 drill down 做人工覆核。
