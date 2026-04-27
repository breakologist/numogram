---
title: "Geomancy API Design"
created: 2026-04-26
last_updated: 2026-04-26
source: "raw/Geomancy.md (30 145 bytes, 501 lines) — external audit artifact"
status: draft
tags: ["geomancy", "api", "fastapi", "design", "implementation", "divination", "talisman", "perfection", "agent-hooks"]
---

# Geomancy API — Complete Implementation Design

> FastAPI-based geomancy service with full perfection algorithm, SVG talisman rendering, planetary/lunar timing layer, and Hermes agent integration. Four-phase modular rollout concept; Phase 4 delivers complete production-ready system.

*This page documents a self-contained geomancy engine designed for both human divination and automated agent consumption. It builds on the 16 geomantic figures data (already present in `divination-entropy-source.md`) and adds traditional interpretation logic (perfection), visual talisman generation, and web API endpoints.*

---

## Architecture Overview

The service centres on the `ShieldChart` class, which generates:

- **4 Mothers** → 4 Daughters → 4 Nieces → Right/Left Witnesses → Judge → Reconciler
- **House chart** (12 houses, zodiac overlay)
- **Perfection analysis** between querent (House 1) and quesited (default House 7, but focusable)
- **SVG talisman** generation per figure (dot pattern + esoteric装饰)
- **Agent-ready JSON** output for Hermes integration

**Tech stack:** FastAPI (web), Pydantic (models), optional Streamlit/Gradio/HTML frontends.

---

## Endpoints

| Endpoint | Method | Purpose | Key output |
|----------|--------|---------|------------|
| `/generate_chart` | GET | Raw chart generation (4 mothers → full shield + house chart) | All figures, zodiac assignments, bit patterns |
| `/figures` | GET | Reference data for all 16 figures (names, qualities, planets, elements, hermetic_quote) | Figure dictionary |
| `/interpret` | **POST** | Question → auto-highlight relevant houses → run perfection algorithm → return ready-to-display interpretation | `{querent, quesited, perfection_type, perfection_strength, notes, edge_cases, highlighted_houses}` |
| `/render_svg` | GET | Talisman SVG for a given figure (with size, style, pub-analogy toggles) | Complete SVG markup (embedded or URL) |
| `/oracle` | POST | Hermes-agent-specific: returns formatted speech-ready reading with timed delivery cues | Natural-language reading + metadata |

All endpoints return JSON; SVG returned as `image/svg+xml` or embedded in JSON.

---

## Perfection Algorithm (Core Interpretation Engine)

Perfection determines whether the quesited (what's asked about) is *perfected* (attained) relative to the querent. Four traditional modes:

### 1. Conjunction (strong)
- **Condition:** Same figure appears in both querent house (1) and quesited house (7 by default, or specified focus house).
- **Interpretation:** Direct conjunction — very affirmative. The matter is already realised or will come easily.

### 2. Translation (medium)
- **Condition:** A third figure appears in *both* Witness positions (right and left), or in a key path connecting 1 and 7.
- **Interpretation:** Energy flows between querent and quesited through an intermediary. Requires mediation but outcome favourable.

### 3. Mutation (weak)
- **Condition:** Both querent and quesited figures are *mobile* (Fortuna Major, Fortuna Minor, Populus, Via) and can mutate into each other via Niece calculations.
- **Interpretation:** Change possible but requires effort. Less stable than conjunction.

### 4. Aspect-based (variable strength)
- **Condition:** Houses 1 and 7 occupy traditional astrological aspects:
  - **Opposition** (houses 1 & 7, 6 apart): +1 strength
  - **Trine** (houses 1 & 5 or 1 & 9, 4 apart): +2 strength (strong)
- **Strength:** 1 for opposition, 2 for trine. Combined with other modes can boost.
- **Interpretation:** Harmonic or tensional alignment influences outcome.

### Edge Cases Handled
- **Draconis (North/South Node)** in querent or quesited → "karmic timing involved"
- **Rubeus** (Mars figure) cautions against rash action
- **Conflicting Witnesses** (both Witnesses disagree) → "inconclusive; wait"
- **Populus** in key positions → "status quo; no motion"

The algorithm returns a structured dict:
```python
{
  "querent_figure": {...},
  "quesited_figure": {...},
  "perfection_type": "Conjunction | Translation | Mutation | Aspect | None",
  "perfection_strength": "strong | medium | weak | none",
  "notes": ["human-readable explanations"],
  "edge_cases": ["special condition flags"],
  "highlighted_houses": [1, 7, ...]  # which houses the UI should emphasise
}
```

---

## Talisman SVG Rendering

Each geomantic figure is rendered as a **dot pattern** (traditional four-line dot matrix). The `/render_svg` endpoint returns a complete, production-ready SVG wrapped in a decorative talisman frame:

- **Dot scaling** controlled by `size` parameter (`small`, `medium`, `large`)
- **Styling toggles:** `include_pub` (Cummin's pub-anagram overlay), `include_astro` (zodiac/planetary glyphs), `include_quote` (hermetic phrase)
- **Color scheme:** parchment background + ink-dark dots + optional planetary hue per figure
- Output is **embeddable** (`<img src=".../render_svg?figure=Acquisitio">`) or inline-displayable

Example: `GET /render_svg?figure_value=13&size=large&include_pub=true` returns a full-page talisman ready for printing or ritual display.

---

## Integration with Existing Numogram Ecosystem

| Component | Link |
|-----------|------|
| Figure data (16 figures) | Shared with `divination-entropy-source.md`'s `GEOMANTIC_FIGURES` dict |
| House chart → zone mapping | Can feed into `numogram-divination` for zone-based routing |
| Perfection output → agent | Designed for `hermes-agent`'s `/oracle` hook: reads `notes` and `edge_cases` as speech cues |
| Astrological overlay | References traditional zodiac correspondences; could cross-link to `i-ching-connections` for planetary-chinese syncretism |

---

## Implementation Notes

The Phase 4 deliverable is a **single-file FastAPI app** (`main.py`) containing:

1. **Core geomantic engine** (ShieldChart class unchanged from v1)
2. **Perfection method** (`perfection_analysis()`) — complete traditional algorithm with edge-case handling
3. **Interpret endpoint** (`/interpret`) — question parsing + house highlighting + perfection routing
4. **SVG renderer** (`render_svg()`) — dot-pattern + talisman decoration generator
5. **Planetary hours & lunar mansion helpers** — timing layer for ritual casting
6. **Export options** — PDF chart, JSON archive, LaTeX export hooks
7. **Agent endpoint** (`/oracle`) — formatted reading with timed delivery for Hermes voice

All endpoints coexist with the original `/generate_chart` and `/figures` — zero breaking changes.

---

## GUI Options (Phase 3)

Three front-end approaches available:

| Option | Stack | Pros |
|--------|-------|------|
| **Streamlit** | Pure Python, rapid prototyping | Fastest to deploy; built-in chart components |
| **Gradio** | Python, interface blocks, RTL support | Better for mobile/chat-style interaction |
| **Pure HTML/JS** | No Python GUI deps | Most flexible; embed in any website; works with hermes-agent's browser tools |

All three consume the same FastAPI backend — pick based on deployment context.

---

## Agent Integration Hooks

The `/oracle` endpoint is explicitly built for Hermes:

```json
{
  "reading": "Acquisitio in House 10 — Gain through labour, but beware Rubeus in Witness...",
  " cues": {
    "timing": "Best cast during hour of Mercury",
    "moon": "Avoid when Moon in Via (void of course)",
    "voice": "Oracle mode, Warp timbre"
  }
}
```

This can be piped directly into `hermes-agent`'s speech synthesis layer with zone-appropriate voice modulation.

---

## Code Blocks to Preserve

The raw file contains multiple complete `main.py` versions (Phase 1–4). The critical snippets to extract:

1. **Perfection algorithm** (lines 105–160) — the heart of interpretation
2. **Interpret endpoint** (lines 165–210) — request/response model
3. **SVG renderer** (lines 292–340) — talisman construction
4. **ShieldChart class extensions** (lines 84–103, 272–292) — validation + pub analogies
5. **Agent oracle formatter** (lines 469–492) — Hermes-ready output

All are ready-to-copy; they use only stdlib + FastAPI/Pydantic.

---

## Relationship to Other Wiki Pages

- `[[divination-sources-guide]]` — Geomancy listed as core system; this page provides the *implementation* for that system
- `[[divination-entropy-source]]` — Provides figure generation (16 figures); this page adds *interpretation* and *service layer*
- `[[entropy-modules-litprog]]` — Could adopt this as a case study (API design vs. standalone module)
- `[[numogram-divination]]` — General divination methodology; this is a specific engine plug-in

---

## Next Actions

- [ ] Extract Phase 4 `main.py` into separate code file (`geomancy_api/main.py`) in the repo
- [ ] Create FastAPI project structure (`requirements.txt`, `Dockerfile` if needed)
- [ ] Add `/oracle` endpoint to `hermes-agent` plugin registry
- [ ] Wire SVG talismans into `numogram-visualizer` as optional overlay
- [ ] Document figure data schema in `divination-entropy-source.md` (cross-ref completeness)

---

**Raw source preserved:** `raw/Geomancy.md` (30 KB) in canonical vault.
