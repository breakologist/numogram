---
title: Wiki Navigation Quick Reference
created: 2026-05-04
status: draft
tags: [navigation, quick-reference]
---

# Wiki Navigation Quick Reference

> A concise guide to finding content in the Hermetic Archive. Use this as a cheat sheet for efficient navigation.

---

## 🔍 Search Shortcuts

**Basic search:** Type keywords in the search bar.

**Advanced operators:**
- `file:name` — Search in file names
- `path:folder` — Search in specific folder
- `tag:tagname` — Search by tag
- `content:keyword` — Search in content (default)
- `ctime:YYYY-MM-DD` — Filter by creation date
- `mtime:YYYY-MM-DD` — Filter by modification date

**Examples:**
- `tag:#audio path:mod-writer` — Find audio pages in mod-writer folder
- `file:validation content:96.4` — Find files with "96.4" in name or content
- `mtime:2026-05-04` — Find pages updated today

---

## 🏷️ Tags

**Common tags:**
- `#audio` — Audio synthesis and MIR
- `#visual` — Diagrams, videos, exhibits
- `#numogram` — Core numogram theory
- `#ro-guelike` — Roguelike agents and games
- `#phase5` — Phase 5 project documentation
- `#status/active`, `#status/draft`, `#status/complete`
- `#type/exhibition`, `#type/tutorial`, `#type/reference`, `#type/logs`

**Usage:** Add 3-5 relevant tags to each page's frontmatter.

---

## 📊 Dataview Queries

**All pages (recently updated):**
```dataview
table file.mtime as "Updated", file.path as "Page"
from "#wiki"
where file.mtime > date(today) - dur[P1W]
sort file.mtime desc
limit 20
```

**Phase 5 pages:**
```dataview
table status as "Status", file.path as "Page"
from "#phase5"
sort file.name
```

**Audio-related pages:**
```dataview
list from "#audio" or #visual
where contains(file.tags, "#audio")
sort file.name
```

---

## 📅 Periodic Notes

**Location:** `.wiki/periodics/`

- **Daily notes:** `daily/2026-05-02.md` — Session logs, scratch work
- **Weekly notes:** `weekly/2026-W18.md` — Progress summaries
- **Monthly notes:** `monthly/2026-05.md` — Status reports

---

## ✅ Tasks

**Query open tasks:**
```tasks
not done
```

**Query Phase 5 tasks:**
```tasks
path includes "phase5"
not done
```

---

## 🔗 Backlinks

- Check the **Backlinks** pane on any page to see what references it
- Use **Unlinked mentions** to find related content without explicit links
- Follow link chains to explore topics in depth

---

## 🎨 Visual Maps

- Use **Excalidraw** plugin to create hand-drawn diagrams
- Visual maps show relationships between concepts
- Find visual maps in the `assets/` folder or linked from pages

---

## 📁 External Tools

**Git commands:**
- `git log --oneline --since="2026-05-01"` — Recent commits
- `git diff --name-only HEAD~5..HEAD` — Files changed in last 5 commits
- `git grep -n "validation" -- "*.md"` — Search for "validation" in markdown

**ripgrep (rg):**
- `rg "Phase 5" --include="*.md"` — Find all mentions of "Phase 5"
- `rg "96\.4" --include="*.md"` — Find all 96.4% references

---

## 🎯 Quick Paths

- **Main Index:** `index.md`
- **Visual Hub:** `visual-hub.md`
- **Phase 5 Report:** `phase5-validation-report.md`
- **Wiki Assets:** `assets/` folder
- **Session Logs:** `periodics/daily/`
- **All Pages:** Use dataview query above

---

## 💡 Tips

- Use **multiple methods together** — search, then browse tags, then check backlinks
- **Add tags** to all new pages for better discoverability
- **Update status** in frontmatter when page is complete
- **Link related pages** to strengthen the knowledge graph
- **Create visual maps** for complex relationships

---

*"The numogram is a map of the archive's structure — follow the currents from zone to zone."*
