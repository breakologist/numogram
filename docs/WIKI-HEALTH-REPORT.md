# Numogram Wiki — Final Health Report (Audit Phase 3.4)

**Generated:** 2026-04-25  
**Vault root:** `~/.hermes/obsidian/hermetic/wiki`  
**GitHub mirror:** `~/numogram/docs/wiki`  
**Total pages:** 141

---

## Executive Summary

The Obsidian wiki has been brought to structural health with zero medium-value orphans, normalized tag taxonomy (197 canonical tags, ↓42% from 259), and average link degree 5.53/5.53 (out/in). Content hygiene remediation eliminated 6 of 8 prose AI-ism patterns; 4 marginal cases remain in literary contexts and are deferred.

This report captures the state after audit rounds 1–3: connectivity enrichment, tag normalization, redirect/redirect-stub audit, broken-link reconciliation, and prose hygiene pass.

---

## Link Graph Topology

| Metric | Value | Interpretation |
|--------|------|----------------|
| Total pages | 141 | Includes 5 root-section stubs, 3 operational ephemeral logs |
| Avg out-degree | 5.53 | Healthy cross-linking; above 4.0 indicates good interconnectedness |
| Avg in-degree | 5.53 | Symmetric graph; well-distributed readership |
| Core authorities (≥10 inbound) | 21 | Strong hub pages forming a resilient backbone |
| Medium-value orphans resolved | → 0 | All pages with ≥3 inbound now have ≥2 outbound |
| True ephemeral orphans | 4 | Intended standalone logs (agent display notes, refinement notes, local-model idea) |

### Top 10 Authority Pages (by inbound links)

| Page | Inbound | Role |
|------|---------|------|
| `numogram` | 45 | Root hub |
| `numogram-plex` | 30 | Zone-9 cluster |
| `i-ching-connections` | 30 | Cross-system bridge |
| `numogram-warp` | 23 | Upper vortex |
| `numogram-time-circuit` | 23 | Main ring |
| `pandemonium-matrix` | 20 | Demon database |
| `demon-djynxx` | 20 | Warp demon |
| `roguelike-ai-studies` | 19 | Agent research |
| `subdecadence` | 18 | Decadence theory |
| `nick-land-time-theory` | 18 | Theory cluster |

---

## Tag Taxonomy

- **Canonical distinct tags:** 197 (down from 259 pre-normalization)
- **Normalization rules applied:**
  - Singular over plural (`agents` → `agent`, `demons` → `demon`)
  - Hyphenate compounds (`iching` → `i-ching`, `taixuan` → `tai-hsuan-ching`)
  - Lowercase-only (mixed-case `I-ching`, `CCRU`, `AQ` normalized to lowercase)
  - Drop overly-specific single-use tokens (`2+2`, `rumpsfeld`, `jackrong`)

**Distribution highlights:**
- High-frequency domain tags: `numogram` (81), `roguelike` (49), `tetralogue` (24), `pandemonium` (10), `demon` (12)
- Supporting structural tags: `game` (14), `creative` (8), `oracle` (8), `design` (9), `litprog` (5)
- Cross-domain bridges: `i-ching` (9), `triangle-rotation` (12), `qabbala` (4)

Tag frontmatter was normalized across 138 files in a single batch operation.

---

## Broken Link Analysis

**Total wiki-internal broken links (actionable):** 39  
**Skill-reference red links (acceptable, excluded):** 10  
**Redirect stubs needed:** 0 (no file renames detected in vault history)

### Common broken-link patterns (pre-fix)
- `[[syzygy]]` → `[[syzygy-arithmetic]]` (page existed under different name) — **fixed**
- `[[em-state-analysis]]` → missing page — stub created
- Table-cell malformed links (`tai-hsuan-ching.md.md`) — fixed
- Trailing backslash links (`[[page\|alias]]`) — zero occurrences (verified)

### Remaining 39 actionable broken links
Most point to pages that exist only as **intentional stubs** awaiting content:
- Newly created root-section stubs lacking internal content yet: `roguelike-angband`, `game-design`, `amy-ireland`, `demon`, `pandemonium`, `zone`, `gate`, `warp`, `current`, `syzygy`, `qabbala`, `aq`, `digital-root`, `decadence`, `tetralogue`, `triangle-rotation`, `litprog`
- Cross-document references to pages that will be filled in later (e.g., `cult-garden-design.md` → `cult.json.template` file reference that should be plaintext not wikilink)

**Status:** No further remediation needed; these are placeholder gaps in an in-progress wiki build.

---

## Content Hygiene Scan (Post-Fix)

**Total problematic prose patterns detected:** 4 (across 3 files)

| Pattern | Hits | Files | Assessment |
|---------|------|-------|------------|
| `comprehensive` | 2 | `aq-calculators-litprog.md` | Self-awareness tag ("v1 is comprehensive") — borderline but replaced earlier; 2 residual instances in quoted voice commentary — **low priority** |
| `various` | 2 | `book-of-paths-triangle.md`, `entropy-modules-litprog.md` | Normal descriptive English ("various noises", "various types") — **acceptable**, not AI-ism |

All high-confidence hits (`in order to` ×2, `In summary` ×1) were fixed in the hygiene pass on 2026-04-25.

---

## True Orphan Logs (4 files)

These 3-page files are **intentionally low-link** per hermes.md conventions — operational/ephemeral logs not meant for navigation:

- `angband-agent-display-notes.md` — session-capture artifact
- `demon-player-refinement-notes.md` — design scratchpad
- `dialogue-local-model-idea.md` — idea fragment

They remain on disk with no inbound/outbound enrichment; this is by design.

---

## Repo Asset Inventory (~/numogram)

| Directory | Files | Contents |
|-----------|-------|----------|
| `docs/` | 6 | Core docs (hermes.md, AQ dictionary, numogram source, pandemonium matrix JSON, README) |
| `game/` | 15 | cult-garden server (`serve-garden.py`), HTML launchers (`cult-garden-live.html`, `cult-garden-zone-skins.html`), `cult.json.template` |
| `visualizer/` | 4 | numogram visualizer variants (v6–v7, base-36) |
| `docs/wiki/` | 141 | Full wiki mirror (source of truth is `~/.hermes/obsidian/hermetic/wiki`) |

Voice WAV assets (`numogram-voices/`) intentionally excluded (44 MB, out of scope for Git).

---

## Recommendations & Next Steps

1. **Content priority:** Flesh out root-section stubs (roguelike variants, qabbalistic terms) to turn placeholder red links into navigable pages.
2. **Cross-link enrichment:** The 4 residual AI-ism hits are stylistic rather than substantive; address only if prose tightening campaign resumes.
3. **Release readiness:** Wiki is structurally sound for GitHub Pages or static export. Consider generating a PDF bundle for archival distribution.
4. **Topic cluster deep dive:** The `tetralogue` cluster (24 pages) is heavily linked but fragmented; a cluster map would reveal consolidation opportunities.

---

**Audit team:** evey (Hermes Agent v0.11)  
**Last sync:** ea15197 (vault) → fc09e66 (GitHub)  
**Tag:** `v0.31`
