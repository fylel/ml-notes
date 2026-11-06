/* ============================================================
   ML 筆記站 — 全站共用腳本
   - 首頁（body 有 data-page="home"）：依 window.NOTES 產生卡片、搜尋、標籤篩選
   - 筆記頁（body 有 data-note-id）：產生麵包屑、目錄、上一篇/下一篇
   資料來源：assets/notes-data.js（不用 fetch，雙擊 index.html 也能看）
   ============================================================ */

(function () {
  "use strict";

  const SITE = window.SITE || {};
  const NOTES = (window.NOTES || []).slice().sort(function (a, b) {
    return a.week - b.week || a.id.localeCompare(b.id);
  });
  const body = document.body;
  const root = body.dataset.root || ".";

  function el(tag, attrs, children) {
    const node = document.createElement(tag);
    Object.entries(attrs || {}).forEach(function ([k, v]) {
      if (k === "text") node.textContent = v;
      else node.setAttribute(k, v);
    });
    (children || []).forEach(function (c) { if (c) node.appendChild(c); });
    return node;
  }

  function noteUrl(id) { return root + "/notes/" + id + ".html"; }
  function weekLabel(n) { return "WEEK " + String(n).padStart(2, "0"); }

  /* ---------- 全站：網站名稱 / 頁尾 ---------- */
  document.querySelectorAll("[data-site='name']").forEach(function (n) { n.textContent = SITE.name || ""; });
  document.querySelectorAll("[data-site='course']").forEach(function (n) { n.textContent = SITE.course || ""; });
  document.querySelectorAll("[data-site='repo']").forEach(function (n) { if (SITE.repo) n.setAttribute("href", SITE.repo); });
  const footer = document.querySelector(".footer");
  if (footer) {
    footer.textContent = (SITE.course || "") + " · " + (SITE.semester || "") + " · " + NOTES.length + " notes · by " + (SITE.author || "");
  }

  /* ---------- 首頁 ---------- */
  if (body.dataset.page === "home") {
    const grid = document.getElementById("note-grid");
    const search = document.getElementById("search");
    const tagBox = document.getElementById("tag-filter");
    let activeTag = null;

    const allTags = Array.from(new Set(NOTES.flatMap(function (n) { return n.tags || []; })));
    allTags.forEach(function (t) {
      const b = el("button", { class: "tag", type: "button", text: t });
      b.addEventListener("click", function () {
        activeTag = activeTag === t ? null : t;
        tagBox.querySelectorAll("button").forEach(function (x) { x.classList.toggle("active", x.textContent === activeTag); });
        render();
      });
      tagBox.appendChild(b);
    });

    function render() {
      const q = (search.value || "").trim().toLowerCase();
      grid.innerHTML = "";
      const list = NOTES.filter(function (n) {
        const hay = (n.title + n.summary + (n.tags || []).join(" ")).toLowerCase();
        return (!q || hay.includes(q)) && (!activeTag || (n.tags || []).includes(activeTag));
      });
      if (!list.length) {
        grid.appendChild(el("p", { class: "empty", text: "// 找不到符合的筆記" }));
        return;
      }
      list.forEach(function (n) {
        const week = el("span", { class: "week", text: weekLabel(n.week) });
        if (n.status === "draft") week.appendChild(el("span", { class: "badge-draft", text: "草稿" }));
        const tags = el("div", { class: "tags" }, (n.tags || []).map(function (t) { return el("span", { class: "tag", text: t }); }));
        grid.appendChild(el("a", { class: "note-card", href: noteUrl(n.id) }, [
          week,
          el("h3", { text: n.title }),
          el("p", { text: n.summary }),
          tags
        ]));
      });
    }
    search.addEventListener("input", render);
    render();
  }

  /* ---------- 筆記頁 ---------- */
  const noteId = body.dataset.noteId;
  if (noteId) {
    const idx = NOTES.findIndex(function (n) { return n.id === noteId; });
    const note = NOTES[idx];
    const article = document.querySelector("article.note");

    if (note) document.title = note.title + " | " + (SITE.name || "");

    // 麵包屑
    const crumb = document.querySelector(".breadcrumb");
    if (crumb && note) {
      crumb.innerHTML = "";
      crumb.appendChild(el("a", { href: root + "/index.html", text: "~/notes" }));
      crumb.appendChild(document.createTextNode(" / " + note.id));
    }

    // 目錄：抓所有有 id 的 section 底下的 h2
    const toc = document.querySelector(".toc");
    if (toc && article) {
      const sections = Array.from(article.querySelectorAll("section[id] > h2"));
      const ol = el("ol");
      sections.forEach(function (h) {
        ol.appendChild(el("li", {}, [el("a", { href: "#" + h.parentElement.id, text: h.textContent })]));
      });
      toc.appendChild(el("div", { class: "toc-title", text: "ON THIS PAGE" }));
      toc.appendChild(ol);

      // 捲動時標示目前段落
      if ("IntersectionObserver" in window) {
        const links = toc.querySelectorAll("a");
        const io = new IntersectionObserver(function (entries) {
          entries.forEach(function (e) {
            if (e.isIntersecting) {
              links.forEach(function (a) { a.classList.toggle("active", a.getAttribute("href") === "#" + e.target.id); });
            }
          });
        }, { rootMargin: "-20% 0px -70% 0px" });
        sections.forEach(function (h) { io.observe(h.parentElement); });
      }
    }

    // 上一篇 / 下一篇
    if (article && idx !== -1) {
      const prev = NOTES[idx - 1];
      const next = NOTES[idx + 1];
      function pagerLink(n, cls, label) {
        if (!n) return el("span", { class: cls });
        return el("a", { class: cls, href: noteUrl(n.id) }, [
          el("small", { text: label + " · " + weekLabel(n.week) }),
          document.createTextNode(n.title)
        ]);
      }
      article.appendChild(el("nav", { class: "pager", "aria-label": "筆記導覽" }, [
        pagerLink(prev, "prev", "← 上一篇"),
        pagerLink(next, "next", "下一篇 →")
      ]));
    }
  }
})();
