# CLAUDE.md — ML 筆記站 專案規則

> 這份文件是給 AI（Claude、Codex、Copilot 等）閱讀的「專案說明書」。
> 任何 AI 在新增或修改這個專案前，**必須先讀完本文件並遵守所有規則**。
> 人類協作者也請以本文件為準。

---

## 1. 專案目的

這是一個 **機器學習課程筆記網站**，把每週上課內容整理成一頁一頁的筆記，部署在 GitHub Pages。

- 讀者：修課同學、未來的自己（考前複習用）
- 目標：每一篇筆記都能在 **5 分鐘內抓到重點**，且所有頁面長得一致
- 核心精神：**新增一篇筆記 = 複製模板 + 填內容 + 登記一行資料**，不需要動到樣式或程式

---

## 2. 技術限制（不可違反）

| 項目 | 規定 |
|------|------|
| 技術 | 純 HTML + CSS + 原生 JavaScript，**不使用任何框架或 build 工具** |
| 部署 | GitHub Pages，從 repo 根目錄直接發布（根目錄有 `.nojekyll`） |
| 外部資源 | 只允許：Google Fonts、KaTeX（cdn.jsdelivr.net）。不得新增其他 CDN |
| 本機預覽 | 直接雙擊 `index.html` 就要能正常顯示（所以**不可用 `fetch()` 讀資料檔**） |
| 編碼 | 所有檔案 UTF-8，HTML 開頭 `<meta charset="UTF-8">` |
| 語言 | 內容用 **繁體中文**，專有名詞第一次出現時附英文，例如「梯度下降（Gradient Descent）」 |

---

## 3. 資料夾結構

```
ml-notes/
├── CLAUDE.md              ← 本文件（AI 規則，最高優先）
├── AGENTS.md              ← 指向本文件，給其他 AI 工具讀
├── README.md              ← 給人看的專案介紹
├── index.html             ← 首頁：自動列出所有筆記（不要手動加卡片）
├── .nojekyll              ← 讓 GitHub Pages 不經過 Jekyll
├── assets/
│   ├── style.css          ← 全站唯一樣式表（設計 token 都在 :root）
│   ├── main.js            ← 全站共用腳本（首頁列表、目錄、上一篇/下一篇）
│   └── notes-data.js      ← ★ 筆記登記表 + 網站設定（新增筆記一定要改這裡）
├── notes/
│   ├── 01-what-is-ml.html
│   ├── 02-linear-regression.html
│   └── ...                ← 每篇筆記一個 HTML
├── templates/
│   └── note-template.html ← ★ 新筆記一律從這裡複製
└── scripts/
    └── check.py           ← 檢查腳本，新增/修改後必跑
```

**不要**新增上面沒列出的資料夾；圖片若有需要，放 `assets/img/<筆記id>/`。

---

## 4. 檔案命名規則

- 筆記檔：`notes/NN-slug.html`
  - `NN`：兩位數週次（第 1 週 → `01`，第 12 週 → `12`）
  - `slug`：英文小寫 + 連字號，2～4 個單字，描述主題
  - ✅ `03-logistic-regression.html`　❌ `3_Logistic.html`　❌ `第三週.html`
- 同一週有兩個主題：`05-svm.html`、`05b-kernel-trick.html`
- 筆記的 **id = 檔名去掉 `.html`**（例如 `03-logistic-regression`），全站唯一
- 圖片：`assets/img/<id>/<描述>.png`，例如 `assets/img/02-linear-regression/loss-curve.png`

---

## 5. 網頁風格（深色技術風）

所有顏色、字體、間距都定義在 `assets/style.css` 的 `:root`，**筆記頁裡禁止寫 inline style 或自訂顏色**。

| Token | 用途 |
|-------|------|
| `--bg` `#0b0f14` | 頁面背景 |
| `--panel` `#121821` | 卡片、區塊背景 |
| `--line` `#1f2a37` | 邊框 |
| `--text` / `--muted` | 主文字 / 次要文字 |
| `--accent` `#4fd1c5`（青綠） | 連結、重點、標題前綴 |
| `--accent-2` `#a78bfa`（紫） | 標籤、次強調 |
| `--warn` `#f6ad55`（橘） | 常見錯誤提醒 |

- 字體：內文 `Noto Sans TC`，程式碼與標籤 `JetBrains Mono`
- 標題 `h2` 前會自動出現 `#` 符號（CSS 處理，不要手打）
- 整體感覺：像工程師的終端機筆記，**乾淨、低飽和背景、少量亮色點綴**
- 若要調整風格，只改 `:root` 的 token，不要在各頁覆寫

---

## 6. 筆記頁結構（每篇都必須相同）

每篇筆記由下列區塊組成，**順序固定、class 名稱固定**。模板裡已全部寫好。

| 順序 | 區塊 | 標記 | 必填 | 說明 |
|------|------|------|------|------|
| 1 | 頁面設定 | `<body data-note-id="..." data-root="..">` | ✅ | id 必須等於檔名 |
| 2 | 標題區 | `<header class="note-head">` | ✅ | 週次、標題、日期、標籤 |
| 3 | 一句話重點 | `<div class="tldr">` | ✅ | 1～2 句，說完這週在學什麼 |
| 4 | 學習目標 | `<section id="goals">` | ✅ | 3～5 點，用「能夠…」開頭 |
| 5 | 主要內容 | 多個 `<section id="...">` + `<h2>` | ✅ | 2～5 個段落，每段一個 `h2` |
| 6 | 重點回顧 | `<section id="recap" class="recap">` | ✅ | 3～6 點條列，考前看這裡就好 |
| 7 | 延伸閱讀 | `<section id="refs">` | 選填 | 外部連結 |

**目錄（TOC）與「上一篇／下一篇」由 `main.js` 自動產生**，不要手寫。

### 6.1 可用元件（只能用這些）

```html
<!-- 提示框：三種類型 -->
<div class="callout tip"><strong>小技巧</strong> 內容</div>
<div class="callout note"><strong>補充</strong> 內容</div>
<div class="callout warn"><strong>常見錯誤</strong> 內容</div>

<!-- 數學公式（KaTeX）：行內用 \( \)，獨立一行用 $$ $$ -->
<p>損失函數 \( L(\theta) \) 定義為：</p>
$$ L(\theta) = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2 $$

<!-- 程式碼：一律標語言 -->
<pre><code class="lang-python">model.fit(X, y)</code></pre>

<!-- 名詞定義 -->
<dl class="terms">
  <dt>過擬合 Overfitting</dt><dd>模型把訓練資料的雜訊也學起來，導致測試表現變差。</dd>
</dl>

<!-- 比較表 -->
<table class="compare">...</table>
```

需要新元件時：**先在 `style.css` 加樣式、再更新本節文件**，不可只在單一頁面自創。

---

## 7. 新增一篇筆記的標準流程（SOP）

AI 收到「幫我新增第 N 週筆記：主題 X」時，依序執行：

1. **決定 id**：依第 4 節命名，例如 `04-neural-network`
2. **複製模板**：`templates/note-template.html` → `notes/<id>.html`
3. **填寫內容**：
   - 把模板中所有 `{{...}}` 佔位符換掉，**不得留下任何 `{{`**
   - `data-note-id` 填 id；`data-root` 保持 `..`
   - 依第 6 節區塊順序撰寫；每個 `<section>` 要有唯一 `id`（英文小寫連字號）
4. **登記筆記**：在 `assets/notes-data.js` 的 `window.NOTES` 陣列**依週次順序**加入一筆：
   ```json
   {
     "id": "04-neural-network",
     "week": 4,
     "title": "神經網路入門",
     "summary": "一句話摘要，會顯示在首頁卡片（40 字內）",
     "tags": ["深度學習", "反向傳播"],
     "date": "2026-10-01",
     "status": "done"
   }
   ```
   - 這段必須是 **嚴格 JSON**（雙引號、最後一筆後面不加逗號），檢查腳本會解析它
   - `status`：`done`（完成）或 `draft`（草稿，首頁會顯示「草稿」標記）
   - `tags` 優先沿用既有標籤，避免同義不同字（例：統一用「分類」，不要再出現「分類問題」）
5. **執行檢查**：`python scripts/check.py`，全部通過才算完成
6. **不需要**修改 `index.html`、`main.js`、`style.css`——首頁會自動出現新卡片

---

## 8. 內容撰寫規則

- **先講直覺，再講公式，最後給程式碼**
- 每篇至少一個 `callout`（tip / note / warn 任一）
- 公式要有中文解釋，每個符號第一次出現時說明意義
- 程式碼以 Python（NumPy / scikit-learn / PyTorch）為主，保持 15 行內，能直接執行
- 不貼大段老師投影片原文；用自己的話重寫
- 不確定的內容標註 `<div class="callout note"><strong>待確認</strong> …</div>`，不要編造

---

## 9. AI 修改專案時的規則

**必須做：**
- 動手前先讀 `CLAUDE.md`、`assets/notes-data.js`，以及至少一篇既有筆記當範例
- 完成後執行 `python scripts/check.py` 並回報結果
- 改了共用檔案（`style.css`、`main.js`、模板）時，在回覆中說明影響範圍

**禁止做：**
- ❌ 在筆記頁寫 `<style>`、inline `style=""`，或新增 `<script>`（模板底部內建的 4 個 script 保持原樣，不要增刪）
- ❌ 手動在 `index.html` 加筆記卡片
- ❌ 改變既有筆記的檔名或 id（會讓外部連結失效）
- ❌ 引入框架、npm 套件、build 步驟
- ❌ 刪除筆記（只能把 `status` 改成 `draft`，除非使用者明確要求刪除）
- ❌ 修改本文件的規則，除非使用者明確要求；若規則確實需要改，**先提出、再修改**

---

## 10. 常見任務對照

| 使用者說 | AI 該做的事 |
|----------|-------------|
| 「新增第 5 週筆記，主題 SVM」 | 走第 7 節 SOP |
| 「把網站改成藍色系」 | 只改 `style.css` 的 `:root` token |
| 「第 2 週筆記補一個例子」 | 只改該筆記，在對應 `section` 內新增，必要時加 callout |
| 「首頁加一個搜尋功能」 | 改 `main.js` + `index.html`，並更新本文件第 3 節說明 |
| 「新增一種元件，例如練習題」 | 先加 CSS → 更新第 6.1 節 → 再在筆記中使用 |
| 「改網站名稱 / 課程名稱」 | 改 `notes-data.js` 的 `window.SITE` |

---

## 11. 完成定義（Definition of Done）

一個新增或修改任務，滿足以下全部條件才算完成：

- [ ] `python scripts/check.py` 顯示 `ALL CHECKS PASSED`
- [ ] 新筆記出現在首頁，且點進去能看到目錄與上一篇／下一篇
- [ ] 沒有任何 `{{` 佔位符殘留
- [ ] 沒有 inline style、沒有新增外部 CDN
- [ ] 手機寬度（375px）下版面不破
