# Release v0.32 — Wiki Audit Complete

**Date:** 2026-04-25  
**Commit:** bbce5df (HEAD → master)  
**Tag:** v0.32

---

## Summary

The Obsidian wiki has completed a full structural audit (phases 1–4). The vault now contains **141 markdown pages** with normalized tag taxonomy (197 canonical tags), zero medium-value orphans, and a healthy link graph (average degree 5.53/5.53). A formal health report and updated README document the baseline.

This release syncs the vault to the GitHub repo at `docs/wiki/` and adds the health report as a canonical reference.

---

## What Changed

### Wiki structural audit (4 phases)

| Phase | Action | Outcome |
|-------|--------|---------|
| **1 — Connectivity** | Enriched low-link pages with "See also" sections; added missing index entries; fixed broken wikilinks (syzygy → syzygy-arithmetic, malformed table links) | Zero medium-value orphans remain; 21 core authority hub pages (≥10 inbound) |
| **2 — Tag normalization** | Singularized, hyphenated, lowercased; dropped single-use tokens | Canonical tags reduced from 259 → 197 across 138 files |
| **3 — Redirect & hygiene scan** | No file renames detected → zero redirects needed; quantified AI-ism patterns | 30 initial hits; 6 fixed; 4 residual minor cases deferred |
| **4 — Health report** | Compiled comprehensive metrics (link graph, tag distribution, orphan analysis, broken links) | `docs/WIKI-HEALTH-REPORT.md` established as canonical audit artifact |

### Content hygiene pass

Fixed 3 prose patterns across 3 files:
- `in order to` → `to` (2 occurrences in comparative-qabalism-triangle-rotation.md)
- `In summary` → `Ultimately` (1 in triangular-numbers.md)
- `various contributors` → `a shifting cast of contributors` (1 in angband-ccru-warwick.md)

4 marginal AI-ism hits remain (`comprehensive` ×2 in quoted voice text, `various` ×2 in literary contexts) — low priority.

### README refresh

- Updated wiki page count (124 → 141)
- Added repository status section with health metrics
- Documented cult-garden server instructions
- Cross-reference to `docs/WIKI-HEALTH-REPORT.md`

---

## Assets

**Docs (`docs/`)**
- `wiki/` — 141 markdown pages (Obsidian vault mirror)
- `WIKI-HEALTH-REPORT.md` — full audit metrics & methodology
- `aq-dictionary.md`, `hermes.md`, `numogram-source.txt`, `pandemonium-matrix.json` unchanged

**Game (`game/`)**
- `serve-garden.py` — cult-garden overflow visualizer server
- `cult-garden-live.html`, `cult-garden-zone-skins.html` — front-end pages (fetch `./cult.json`)
- `cult.json.template` — player save template (personal `cult.json` excluded)

**Visualizer (`visualizer/`)**
- `numogram-visualizer-v7.html` (primary)
- `numogram-visualizer-v7-djynxxogram.html` (base-36 variant)

---

## Repository Health

```
Total pages:        141
Canonical tags:     197
Avg link degree:    5.53 out / 5.53 in
Core authorities:   21 (≥10 inbound)
Medium orphans:     0  ✓
True ephemeral logs: 4 (by design)
Actionable broken links: 39 (mostly intentional stub placeholders)
```

See `docs/WIKI-HEALTH-REPORT.md` for the full dataset.

---

## Next Steps

- **Topic cluster deep dives:** expand root-section stubs (roguelike variants, qabbalistic terms), enrich `tetralogue` cluster (24 pages), flesh out cult-garden lore connections
- **Residual prose polish:** address 4 marginal AI-ism hits if tightening campaign resumes
- **Release packaging:** consider PDF bundle generation for static distribution
- **GitHub Pages:** wiki is structurally ready for static export

---

**Merged commit:** bbce5df  
**Git tag:** v0.32  
**Vault commit:** ea15197
