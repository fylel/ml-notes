/* ============================================================
   筆記登記表 + 網站設定
   ------------------------------------------------------------
   新增筆記時：在 window.NOTES 陣列「依週次順序」加入一筆。
   window.NOTES 的內容必須是嚴格 JSON（雙引號、無結尾逗號），
   scripts/check.py 會解析它。詳見 CLAUDE.md 第 7 節。
   ============================================================ */

window.SITE = {
  "name": "ML 筆記站",
  "course": "機器學習導論",
  "semester": "2026 Fall",
  "author": "Neil",
  "repo": "https://github.com/fylel/ml-notes"
};

window.NOTES = [
  {
    "id": "01-what-is-ml",
    "week": 1,
    "title": "什麼是機器學習",
    "summary": "從「寫規則」到「從資料學規則」：監督式、非監督式與強化學習的差別。",
    "tags": ["基礎觀念", "監督式學習"],
    "date": "2026-09-08",
    "status": "done"
  },
  {
    "id": "02-linear-regression",
    "week": 2,
    "title": "線性迴歸與梯度下降",
    "summary": "用一條直線預測數值，並用梯度下降一步步找到最好的參數。",
    "tags": ["迴歸", "梯度下降", "監督式學習"],
    "date": "2026-09-15",
    "status": "done"
  },
  {
    "id": "03-logistic-regression",
    "week": 3,
    "title": "邏輯迴歸與分類",
    "summary": "把線性輸出丟進 Sigmoid 變成機率，用交叉熵訓練二元分類器。",
    "tags": ["分類", "梯度下降", "監督式學習"],
    "date": "2026-09-22",
    "status": "done"
  }
];
