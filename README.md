# ML 筆記站

機器學習課程的每週筆記網站。一週一頁、一頁一主題，深色技術風，部署在 GitHub Pages。

🔗 **網站**：https://fylel.github.io/ml-notes/

## 這個專案的特色

這不只是一個網頁，而是一套「可以讓 AI 持續擴充」的規則：

- **[CLAUDE.md](./CLAUDE.md)**：給 AI 看的專案說明書，寫清楚目的、風格、結構、命名、新增流程與禁止事項
- **[templates/note-template.html](./templates/note-template.html)**：每篇筆記都從同一份模板複製
- **[assets/notes-data.js](./assets/notes-data.js)**：筆記登記表，首頁卡片、上一篇/下一篇都從這裡自動產生
- **[scripts/check.py](./scripts/check.py)**：檢查腳本，確認新筆記有照規則寫

## 新增一篇筆記

對 AI 說：

> 請依照 CLAUDE.md，新增第 4 週筆記，主題是「神經網路入門」。

AI 會：複製模板 → 填內容 → 在 `notes-data.js` 登記 → 執行 `python scripts/check.py`。
不需要修改首頁或任何樣式。

## 本機預覽

直接雙擊 `index.html` 即可，不需要伺服器或安裝任何東西。

## 結構

```
index.html              首頁（自動列出筆記）
assets/style.css        全站樣式
assets/main.js          首頁列表、目錄、上一篇/下一篇
assets/notes-data.js    筆記登記表 + 網站設定
notes/NN-slug.html      每週筆記
templates/              筆記模板
scripts/check.py        規則檢查
```
