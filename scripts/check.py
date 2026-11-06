#!/usr/bin/env python3
"""
ML 筆記站 檢查腳本
用法：在專案根目錄執行  python scripts/check.py
檢查 notes-data.js 登記表與 notes/*.html 是否符合 CLAUDE.md 的規則。
全部通過會印出 ALL CHECKS PASSED，否則列出錯誤並以 exit code 1 結束。
只用 Python 標準庫，不需安裝任何套件。
"""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "assets" / "notes-data.js"
NOTES_DIR = ROOT / "notes"

ID_PATTERN = re.compile(r"^(\d{2})[a-z]?-[a-z0-9]+(?:-[a-z0-9]+){0,3}$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REQUIRED_FIELDS = {"id": str, "week": int, "title": str, "summary": str,
                   "tags": list, "date": str, "status": str}
ALLOWED_STATUS = {"done", "draft"}
ALLOWED_HOSTS = {"fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net"}
FIXED_SECTIONS = {"goals", "recap", "refs"}
EXPECTED_SCRIPTS = 4

errors: list[str] = []
warnings: list[str] = []


def err(where: str, msg: str) -> None:
    errors.append(f"[{where}] {msg}")


def warn(where: str, msg: str) -> None:
    warnings.append(f"[{where}] {msg}")


class NoteParser(HTMLParser):
    """收集筆記頁中檢查需要的結構資訊。"""

    def __init__(self) -> None:
        super().__init__()
        self.body_attrs: dict = {}
        self.sections: list[tuple[str, str]] = []   # (id, class)
        self.section_h2: dict[str, bool] = {}
        self.classes: list[str] = []
        self.scripts = 0
        self.external: list[str] = []
        self.inline_style = False
        self.style_tag = False
        self.h1_text = ""
        self.meta_tags: list[str] = []
        self.time_value = ""
        self._in_h1 = False
        self._in_meta = 0
        self._in_tag_span = False
        self._section_stack: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class") or ""
        self.classes.extend(cls.split())
        if "style" in a:
            self.inline_style = True
        if tag == "style":
            self.style_tag = True
        if tag == "body":
            self.body_attrs = a
        if tag == "script":
            self.scripts += 1
            if a.get("src"):
                self.external.append(a["src"])
        if tag == "link" and a.get("href"):
            self.external.append(a["href"])
        if tag == "section":
            sid = a.get("id", "")
            self.sections.append((sid, cls))
            self._section_stack.append(sid)
        if tag == "h2" and self._section_stack:
            self.section_h2[self._section_stack[-1]] = True
        if tag == "h1":
            self._in_h1 = True
        if tag == "div" and "meta" in cls.split():
            self._in_meta = 1
        elif tag == "div" and self._in_meta:
            self._in_meta += 1
        if self._in_meta and tag == "span" and "tag" in cls.split():
            self._in_tag_span = True
            self.meta_tags.append("")
        if self._in_meta and tag == "time":
            self.time_value = a.get("datetime", "")

    def handle_endtag(self, tag):
        if tag == "section" and self._section_stack:
            self._section_stack.pop()
        if tag == "h1":
            self._in_h1 = False
        if tag == "span":
            self._in_tag_span = False
        if tag == "div" and self._in_meta:
            self._in_meta -= 1

    def handle_data(self, data):
        if self._in_h1:
            self.h1_text += data
        if self._in_tag_span and self.meta_tags:
            self.meta_tags[-1] += data


def load_registry() -> list[dict]:
    text = DATA_FILE.read_text(encoding="utf-8")
    m = re.search(r"window\.NOTES\s*=\s*(\[.*\])\s*;", text, re.S)
    if not m:
        err("notes-data.js", "找不到 window.NOTES = [...];")
        return []
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError as e:
        err("notes-data.js", f"window.NOTES 不是合法 JSON（第 {e.lineno} 行附近）：{e.msg}。"
            "記得用雙引號、最後一筆後面不要加逗號。")
        return []


def check_registry(notes: list[dict]) -> None:
    seen = set()
    prev_week = -1
    for i, n in enumerate(notes):
        where = f"notes-data.js #{i + 1} {n.get('id', '?')}"
        for field, typ in REQUIRED_FIELDS.items():
            if field not in n:
                err(where, f"缺少欄位 {field}")
            elif not isinstance(n[field], typ):
                err(where, f"欄位 {field} 型別應為 {typ.__name__}")
        nid = n.get("id", "")
        m = ID_PATTERN.match(nid)
        if not m:
            err(where, "id 不符合命名規則 NN-slug（兩位數週次 + 英文小寫連字號）")
        elif isinstance(n.get("week"), int) and int(m.group(1)) != n["week"]:
            err(where, f"id 開頭週次 {m.group(1)} 與 week={n['week']} 不一致")
        if nid in seen:
            err(where, "id 重複")
        seen.add(nid)
        if n.get("status") not in ALLOWED_STATUS:
            err(where, f"status 必須是 {sorted(ALLOWED_STATUS)}")
        if not DATE_PATTERN.match(str(n.get("date", ""))):
            err(where, "date 格式應為 YYYY-MM-DD")
        if len(str(n.get("summary", ""))) > 40:
            warn(where, "summary 超過 40 字，首頁卡片可能太長")
        if isinstance(n.get("week"), int):
            if n["week"] < prev_week:
                err(where, "沒有依週次順序排列")
            prev_week = n["week"]


def check_note_file(n: dict) -> None:
    nid = n.get("id", "")
    path = NOTES_DIR / f"{nid}.html"
    where = f"notes/{nid}.html"
    if not path.exists():
        err(where, "檔案不存在（已登記但找不到 HTML）")
        return
    html = path.read_text(encoding="utf-8")
    if "{{" in html:
        err(where, "還有 {{...}} 佔位符沒有替換")

    p = NoteParser()
    p.feed(html)

    if p.body_attrs.get("data-note-id") != nid:
        err(where, f"body 的 data-note-id 應為 {nid}")
    if p.body_attrs.get("data-root") != "..":
        err(where, 'body 的 data-root 應為 ".."')
    if p.inline_style:
        err(where, "不可使用 inline style=\"\"")
    if p.style_tag:
        err(where, "不可使用 <style> 標籤")
    if p.scripts != EXPECTED_SCRIPTS:
        err(where, f"script 數量應為模板內建的 {EXPECTED_SCRIPTS} 個，目前是 {p.scripts}")
    for url in p.external:
        hm = re.match(r"https?://([^/]+)", url)
        if hm and hm.group(1) not in ALLOWED_HOSTS:
            err(where, f"不允許的外部資源：{url}")

    for cls in ("note-head", "tldr"):
        if cls not in p.classes:
            err(where, f"缺少必要區塊 .{cls}")
    if not any(c == "callout" for c in p.classes):
        err(where, "至少需要一個 callout（tip / note / warn）")

    if p.h1_text.strip() != n.get("title"):
        err(where, f"h1「{p.h1_text.strip()}」與登記的 title「{n.get('title')}」不一致")
    if p.time_value != n.get("date"):
        err(where, f"<time datetime> 與登記的 date 不一致")
    if [t.strip() for t in p.meta_tags] != n.get("tags"):
        err(where, "頁面上的標籤與登記的 tags 不一致（順序也要相同）")

    ids = [sid for sid, _ in p.sections]
    if "" in ids:
        err(where, "每個 section 都必須有 id")
    dup = {x for x in ids if ids.count(x) > 1 and x}
    if dup:
        err(where, f"section id 重複：{', '.join(sorted(dup))}")
    for sid in ids:
        if sid and not p.section_h2.get(sid):
            err(where, f"section#{sid} 缺少 h2 標題")
    if "goals" not in ids:
        err(where, "缺少 section#goals（學習目標）")
    if "recap" not in ids:
        err(where, "缺少 section#recap（重點回顧）")
    elif "recap" not in dict(p.sections)["recap"].split():
        err(where, 'section#recap 需要 class="recap"')

    if "goals" in ids and "recap" in ids:
        gi, ri = ids.index("goals"), ids.index("recap")
        if gi != 0:
            err(where, "section#goals 必須是第一個 section")
        content = [s for s in ids[gi + 1:ri]]
        if not 2 <= len(content) <= 5:
            err(where, f"goals 與 recap 之間應有 2～5 個內容段落，目前 {len(content)} 個")
        if any(s in FIXED_SECTIONS for s in content):
            err(where, "內容段落順序錯誤")
        tail = ids[ri + 1:]
        if tail not in ([], ["refs"]):
            err(where, "recap 之後只能接 section#refs（選填）")


def check_orphans(notes: list[dict]) -> None:
    registered = {n.get("id") for n in notes}
    for f in sorted(NOTES_DIR.glob("*.html")):
        if f.stem not in registered:
            err(f"notes/{f.name}", "有 HTML 檔但沒有在 notes-data.js 登記")


def main() -> int:
    notes = load_registry()
    if notes:
        check_registry(notes)
        for n in notes:
            check_note_file(n)
        check_orphans(notes)

    print(f"檢查 {len(notes)} 篇筆記\n")
    for w in warnings:
        print("  ⚠️  " + w)
    for e in errors:
        print("  ❌ " + e)
    if errors:
        print(f"\n{len(errors)} 個錯誤，請修正後再執行一次。")
        return 1
    print(("\n" if warnings else "") + "✅ ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
