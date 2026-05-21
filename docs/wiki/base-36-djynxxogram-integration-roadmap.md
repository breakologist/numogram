---
title: "Base-36 Djynxxogram — Research Results & Integration Roadmap"
tags:
  - Numogram
  - BaseN
  - Djynxxogram
  - Research
  - Plan
  - Integration
created: 2026-05-21
updated: 2026-05-21
status: active
supersedes: session-threads-2026-05-16.md (Thread 4)
---

# Base-36 Djynxxogram — Research Results & Integration Roadmap

> *"Not a plan. A constellation. These are the ideas that pulled hardest during the Djynxxogram expedition — set down here so we can return to them when the current is right."*

---

## Results So Far

### A. Source Verification (raw/Unleashing the Numogram.md)

The raw local copy of Aamodt's text, lines 1378–1424, confirms:

**Tch 7 "Paradecimally Radixed Numograms"** catalogs 15+ alternate bases. The Djynxxogram sits at the top end alongside Base i. The exact prose:

> *"Base 36: The Sexatrigesimal Djynxxogram. With a name that strongly implies sex and cum (sexatrigeseminal), this Warp‑ciphering numogram is sure to deliver."*

**Extended Gates** (lines 1379–1398) list Gt-55 through Gt-666 explicitly, including Gt-78 (tarot), Gt-253 (Kabbalah), Gt-300 (Clock/AOE), and Gt-666 ("Clicks Djynxx").

All 14 base names now verified — including "Christian Cross—Love/Hate" (base 4), "Venus Venus Venus" (base 7), and "The Hexavigesimal Abecedarium" (base 26).

### B. Computational Explorer (`numogram-base-explorer.py`)

Built and tested. Key empirical findings:

**Finding 1: Warp analogue exists iff 3 | (N−1)**
The self-folding syzygy condition `a = (N−1)/3` produces a Warp analogue only when N−1 is divisible by 3. Bases with Warp: 4, 7, 10, 16, 22, 28. Bases without: 2, 3, 5, 6, 8, 9, 26, **36**.

**Base-36 has only ONE outer region** (the 0::Z Plex analogue) — no Warp vortex. The entire middle zone (zones 1–Y) is a single transitive network analogous to the Time-Circuit.

**Finding 2: Gate Duality — Gt-36 names two different things**
- Gt-36 (ordinal 8, standard): T₈ = 36 → Zone 8 → Zone 9 (Plex plunge in base-10)
- Gt-36 (ordinal 36, extended): T₃₆ = 666 → "Clicks Djynxx"
- In **base-36**, T₈ = 36 mod 36 = 0 → **Zone 8's gate plunges into the Void**, not Plex

**Finding 3: Self-loop zones in base-36**
- Zone 0: Gt-000 → 0 (Void self-loop)
- Zone 1: Gt-001 → 1 (Surge self-loop — same as base-10)
- Zone 9: Gt-045 → 9 (Plex self-loop — same as base-10)
- All other zones are projective (gate target ≠ source)

### C. OH4 / Scrivner's C Library

A public-domain C library (`oh4_numogrammatics.h`, v1.0, 2025) provides: digital root, triangular numbers, prime factorization, AQ calculation, TX encoding/decoding, base-36 TX. The TX connection suggests a three-layer encoding pipeline:

```
Word → AQ (base-36 sum) → TX (prime factorization) → Base-36 TX (compact notation)
```

### D. Existing Tools Audit

| Tool | Base-36 Integration Point |
|------|---------------------------|
| `oracle.py` (~/.hermes/skills/numogram-oracle) | Already computes AQ in base-36. Phase A1 added `--base36` for per-character traversal. Phase A2 added `--compare` for cross-base comparison. |
| Visualizer v7 (ao-djynxxogram.html) | Already implements base-36 Djynxxogram mode. Syzygy formula `35 - z`. Has Synx overlay. Needs zone 10–35 naming audit and 630-demon UI. |
| Roguelike (`numogram_roguelike.py`) | Currently base-10. Base-36 would be "endgame content" — 36 rooms, 630 demons, K₃₆ traversal graph. |

---

## Key Conceptual Insight: Raw vs Plexed Traversal

The Djynxxogram mode reveals a fundamental structural difference between base-36 and base-10:

| Aspect | Base-10 (Standard) | Base-36 (Djynxxogram) |
|--------|-------------------|----------------------|
| **Reduction** | Digital root (plexing) — collapses arbitrarily large AQ to 0–9 | None — each character maps directly to its own zone |
| **Traversal type** | **Plexed** — information is compressed, the path is abstract | **Raw** — full information preserved, every character is a step |
| **Zone count** | 1 zone per reading (aggregate) | N zones per N-character word (per-character) |
| **Effect on AQ** | 174 → digital root 3 → Zone 3 | 174 → 8 distinct zone visits |
| **Name resolution** | "Plex" means the word collapses to a single attractor | "Traversal" means the word spells a path through zone space |
| **What gets lost** | Character-level variation, sequence, syllable structure | Nothing — but no single-zone oracle reading to anchor on |

The standard oracle is a **compression engine** — it takes any text and reduces it to a single zone via digital root. The Djynxxogram is a **traversal engine** — it preserves the full per-character path through the 36-zone space.

**666 illustrates this perfectly:** AQ(666) = 18. In decimal, digital root 18 = 9 → Zone 9 (Plex) — the Beast's number collapses to the Pandemonium gate. In base-36, each '6' → AQ 6 → Zone 6 (Abyss). The path is 6→6→6 — three identical steps through the same zone, no variation, no descent. The Beast's number in Djynxxogram is not a gate-opening but a **stutter** — three repetitions of the same zone, which in the phonetic register sounds like *Tch-Tch-Tch* (Zone 6's quasiphonic particle). The Plex reading is an *interpretation*; the Abyss triple is a *description*.

---

## Completed Phases

### Phase A1: `--base36` flag for oracle.py ✅

Added `--base36` / `--djynxxogram` flag to `oracle.py`. Per-character traversal through all 36 Djynxxogram zones:

- `compute_base36_char(char)` — per-character analysis
- `compute_base36_traversal(text)` — full multi-character traversal
- `generate_base36_reading(text)` — 8-column table output with summary metrics

Zone naming tables: letter-native (Aya/Buh/Kuh... Zuh) + combinatorial phonemes (digit-decomposition).

**Key discovery from this phase:** The digital root (plexing) operation is the core semantic compression of the decimal numogram. Base-36's raw traversal bypasses this entirely — you see the unfiltered path through zone space. This is the relationship between *information* (36-zone) and *meaning* (10-zone attractor).

### Phase A2: Cross-Base Comparison Mode ✅

Added `--compare` flag showing the same text across bases 10, 16, 22, 26, and 36 simultaneously:

- `zone_in_base(aq, base)` — maps AQ to zone in any base
- `generate_comparison_reading(text, bases)` — compact comparison table

**Key finding from this phase:** The same AQ value lands in dramatically different zones depending on base:
| Text | AQ | Base-10 | Base-16 | Base-22 | Base-26 | Base-36 (traversal) |
|------|----|---------|---------|---------|---------|---------------------|
| NUMOGRAM | 174 | 3 (Warp) | E (14) | K (20) | I (18) | 7/36 zones |
| CCRU | 81 | 9 (Plex) | 1 (Surge) | F (15) | 3 (Warp) | 3/36 zones |
| ZEN | 72 | 9 (Plex) | 8 (Rise) | 6 (Abyss) | K (20) | 3/36 zones, OUTER |
| 666 | 18 | 9 (Plex) | 2 (Dt) | I (18) | I (18) | 1/36 zones Abyss |

**666's 1+8=9 across bases:** The digits of AQ(666)=18 sum to 1+8=9, which is the decimal attractor (Plex). In base-16, 18 mod 16 = 2 (Dt) — a different attractor entirely. In base-22, 18 mod 22 = 18 (Ih, Zone I) — which is > 9, and in the letter-zone space. The 1+8=9 relationship holds only in decimal because digital root is base-10 specific. Other bases use mod-N reduction, which produces different results.

---

## Integration Roadmap (Remaining)

### Phase A3: Generate Zone-10–35 Naming Tables (Current C integration)

Both phoneme approaches already implemented in the explorer:
- **Combinatorial:** digit-decomposition phonemes (zone 15 = 1+5 = "gl"+"ktt" = "glktt")
- **Letter-native:** AY, BUH, KUH... ZUH (for zones 10–35)

Current usage:
- **Oracle.py**: uses letter-native (Aya, Buh, Kuh... Zuh) — more natural to speak
- **Explorer**: configurable via `--phoneme` flag (default: combinatorial)

Still to do: verify consistency across both implementations and document in wiki.

### Phase B: Roguelike Integration (future)

Once the oracle integration is stable:
- Add a `--dungeon base=36` mode to `numogram_roguelike.py`
- 36 rooms, each labeled with a character
- Room-accretion rules based on K₃₆ graph
- 630 demon connections as corridor types
- The Hexavigesimal Abecedarium (base-26) as mid-game unlock

### Phase C: Visualizer Integration (future)

- Update the Djynxxogram visualizer (v7) zone names to match the letter-native system
- Add a "compute any base" panel for live exploration
- Surface the 630-demon structural implication in the UI
- Show both traversal path and decimal attractor projection

---

## Open Questions (updated)

| # | Question | Status |
|---|----------|--------|
| 1 | Does the region structure generalize to ANY base N? | **Answered.** N−1 factorization determines outer region count. Warp iff 3 \| (N−1). |
| 2 | What happens at odd vs even numograms? | Aamodt flagged this. Even bases have symmetric syzygy structures. Odd bases have a "middle" zone that pairs with itself (n/2 when n is odd?). Needs analysis. |
| 3 | What's the correct reduction for non-base-10? | Currently using AQ % base. Should it be digital-root-in-base instead? The 666/1+8=9 observation shows decimal digital root gives a different result than mod-N reduction. This may change all comparison results. |
| 4 | Can we embed the base-N explorer in the visualizer? | The v7 visualizer already has base-36 mode. Adding a "compute any base" panel would make it a full research tool. |
| 5 | What does the base-36 sound like? | 36 zones = 3 octaves. Each zone maps to a pitch class. Syzygies = dyads (intervals). Currents = interval sizes. 36-zone traversal = melody. The zone names are already phonetic (Kuh, Kss, Ih...) — a spoken-word oracle possible from the path itself. |
| 6 | What about the Z→I gate? | Gt-630 (zone 35/Z) maps to zone 18/I. The gate of Z leads to I. Does this spell something? Z → I = ZI? Also ZEN: Z→I through a different path. |

---

## Related Pages

- [[base-36-meta-numogram-djynxxogram]] — The full consolidated reference page (350 lines)
- [[numogram-visualizer-v7]] — Djynxxogram base-36 mode
- [[numogram-oracle]] — Oracle pipeline with --base36 and --compare flags (v1.2.0)
- [[session-threads-2026-05-16]] — Thread 4: the original research question
- [[extending-numogram-tetralogue]] — Base-36 as "worlds within worlds" endgame
- [[numerology-one-two-many]] — Land numbering practices
- [[numogram-base-explorer]] — The computational explorer tool

## Sources

1. `raw/Unleashing the Numogram.md` — Aamodt, Tch 7, lines 1378–1424
2. `numogram-base-explorer.py` — Computational exploration results 2026-05-21
3. `~/.hermes/skills/numogram-oracle/oracle.py` — Oracle pipeline (v1.2.0, 806 lines)
4. `~/.hermes/skills/numogram-oracle/SKILL.md` — Oracle skill documentation
5. [OH4 numogrammaticism](https://oh4.co/site/numogrammaticism.html) — C library
