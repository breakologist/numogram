# Post-Audit Roadmap — v0.32 → v0.33

**Last updated:** 2026-04-25  
**Session:** audit complete, health report delivered, v0.32 tagged  
**Next milestone:** v0.33 (content expansion phase)

---

## In-Flight Batches (paused, not complete)

### Batch A — Residual Content Polish (low priority)
- [ ] **AI-ism sweep (tier 2)** — 4 marginal hits in literary contexts:
  - `aq-calculators-litprog.md`: "comprehensive" ×2 (in quoted WRITER voice)
  - `book-of-paths-triangle.md`: "various" (table cell, possibly acceptable)
  - `entropy-modules-litprog.md`: "various" (descriptive prose)
- [ ] Decision: replace with sharper synonyms or leave as-is (authorial voice)

### Batch B — Root-Section Stub Fulfillment (medium priority)
17 stub pages created in audit. Need game-specific/entity-specific content:

| Cluster | Stubs | Recommended owner |
|---------|-------|-------------------|
| **Roguelike variants** | `roguelike-angband.md`, `roguelike-caves-of-qud.md`, `roguelike-cogmind.md`, `roguelike-drl.md`, `roguelike-nethack.md`, `roguelike-rogue.md` | Roguelike architect + local-model council |
| **Qabbalistic terms** | `qabbala.md`, `aq.md`, `digital-root.md`, `syzygy.md`, `gate.md`, `current.md`, `warp.md`, `zone.md` | Numogram oracle (AQ calculator as source) |
| **Entity cluster** | `demon.md`, `pandemonium.md` | Lore writer (45-demon matrix as source) |
| **Meta & methodology** | `game-design.md`, `tetralogue.md`, `triangle-rotation.md`, `litprog.md` | Hermes seed doc + existing narrative pages |
| **People** | `amy-ireland.md` | Research (CCRU genealogies) |

### Batch C — Cult-Garden Lore Wiring (high priority)
- [ ] Cross-link `cult-garden/lore.md` and `cult-garden/readings.md` into tetralogue cluster
- [ ] Add "See also" from tetralogue pages back to cult-garden subpages
- [ ] Document `serve-garden.py` server lifecycle in `hermes-agent-guide.md`

### Batch D — Roguelike Variant Deep Dive (medium-high priority)
- [ ] Populate 11 variant stub pages with:
  - Release dates, developers, lineage
  - Numogram resonance notes (topology, demon integration, mechanics)
  - Agent playability assessment (screen parser compatibility)
- [ ] Link from `roguelike` hub page to each variant
- [ ] Consider comparative table format

### Batch E — Remaining Broken Link Triage (maintenance)
41 actionable broken links (mostly stub→missing). Two patterns:
- [ ] **File references mis-Wikilinked** (e.g., `cult-garden-design.md` → `cult.json.template`): convert to inline code/file path
- [ ] **Cross-doc red links** (`jackrong-model-profile` → not a wiki page): either create stub or convert to plain text

---

## Quick Wins (next session starter)

1. **Pick one cluster** from Batch B and draft 3–5 pages end-to-end (roguelike variant or qabbalistic term cluster). Momentum builder.
2. **Cult-garden cross-linking pass** — cheap, high connectivity return.
3. **Finalize AI-ism decisions** — if we want prose uniformly tight, apply remaining 4 fixes; otherwise mark batch A closed.

---

## Deferred / Optional

- **GitHub Pages export** — wiki is structurally ready; create `mkdocs.yml` or Jekyll config if chosen
- **PDF bundle generation** — print-ready archive using Pandoc or similar
- **Voice WAV asset management** — consider Git LFS if inclusion ever desired
- **CI/automation hooks** — pre-commit lint, automatic sync from vault to repo on commit

---

## Reflections (post-audit observations)

- **Tag density:** 197 canonical tags across 141 pages, but ~80% of tags appear only once or twice. Possible over-tagging vs. personal-knowledge-base intentionality. Candidate consolidation clusters: `game`/`game-design`/`game-analysis`, `visualization`/`svg`/`infographic`, `theory`/`methodology`/`structural`.
- **Tetralogue cluster:** 24 pages (largest tag cluster) but sparse internal cross-linking — reads as four parallel monologues rather than a dialogue. Low-effort navbox template could knit them into a proper tetralogue.
- **Stub TTL consideration:** 17 root-section stubs are intentional placeholders. Consider a policy (e.g., 90-day checkpoint) to either fill or fold them to prevent permanent dead ends.
- **Sync protocol:** Manual `rsync` is correctly conservative. A `make sync` recipe (encapsulating vault commit → rsync → repo commit) would document the workflow without automating it.

---

## Status Legend

- [ ] pending
- [/] in-progress
- [x] complete
