---
title: Kanban Wiki Organization & Audit Board
created: 2026-05-06
updated: 2026-05-06
status: active
tags:
  - kanban
  - wiki-audit
  - task-tracking
  - productivity
---

## Overview

This page documents the dedicated Kanban board used for systematic improvement of the Pandemonium Wiki (the Hermetic Numogram archive at `~/.hermes/obsidian/hermetic/wiki/`).

**Board slug**: `wiki-audit`  
**Display name**: Wiki Organization & Audit 2026-05  

The board was initialized on 2026-05-06 during a session focused on link hygiene, content quality, and reconciliation with `hermes.md` (Knowledge Base Schema).

It complements the existing static audit documents (`wiki-audit-2026-04-21.md`, `wiki-log.md`) by providing live, actionable task tracking with priorities, assignees, dependencies, and progress.

## How to Use This Board

```bash
# Switch to the audit board
hermes kanban boards switch wiki-audit

# View all tasks
hermes kanban list

# Show details on a specific task
hermes kanban show <task-id>

# Typical workflow
hermes kanban claim <id>
# ...work on the task...
hermes kanban complete <id>
```

The dispatcher runs automatically via the Hermes gateway (`hermes gateway start`).

## Audit Run — 2026-05-06 (Orphan Scan)

**Task**: Connect unlinked wiki pages and fix orphan resolution (high priority)

**Action taken**: Broad inbound-link scan across 364 `.md` pages (excluding the new kanban page itself).

- **Total pages scanned**: 364
- **Potential orphans** (pages with zero inbound wikilinks): **87**

Many of the orphans are expected (experimental pages, modarchive references, phase reports, older tetralogues, writer/oracle voice notebooks). The result provides a clean starting list for link-resolution work.

**Next for this task**:
- Manually review high-value orphans (e.g. `audit-plans`, `svg-asset-inventory`, recent phase reports, `log`)
- Add targeted wikilinks from `index.md`, `log.md`, or relevant zone/entity pages
- Re-run scan after link additions to measure improvement

## Current Tasks

(Full list maintained live on the Kanban board)

| ID (short)    | Title                                                                 | Priority | Status  |
|---------------|-----------------------------------------------------------------------|----------|---------|
| t_ec415629    | Connect unlinked wiki pages and fix orphan resolution                 | high     | in-progress |
| t_7dc717ca    | Run content hygiene audit (detect AI-isms) across wiki/               | high     | ready   |
| t_d8db96f1    | Audit index.md for coherence and missing hub links                    | high     | ready   |
| ... (see `hermes kanban list` on board) |

## Related Wiki Pages

- [[wiki-audit-2026-04-21]] — Previous structural audit
- [[index]] — Central hub (currently being audited)
- [[log]] — Chronological session record
- [[wiki-content-hygiene-audit]] — Skill documentation for hygiene scanning

## Notes

- This page itself should be linked from [[index]] and [[log]] once finalized.
- Browser-use (installed via pipx) and scrapling are now available as external ingestion tools for future sources.
- The goal of this board is **actionable closure** rather than open-ended research.

---
*Living document — tasks and status will be updated as work progresses.*
