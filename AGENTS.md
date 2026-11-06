# AGENTS.md

本專案的完整 AI 協作規則寫在 **[CLAUDE.md](./CLAUDE.md)**，所有 AI 代理（Codex、Copilot、Cursor、Gemini 等）都請以該文件為準。

最重要的三件事：

1. 新筆記一律從 `templates/note-template.html` 複製到 `notes/NN-slug.html`
2. 在 `assets/notes-data.js` 的 `window.NOTES` 登記一筆（嚴格 JSON）
3. 完成後執行 `python scripts/check.py`，必須顯示 `ALL CHECKS PASSED`
