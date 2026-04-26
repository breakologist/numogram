---
title: "Divination Entropy Source Module"
created: 2026-04-26
last_updated: 2026-04-26
source: "raw/Coin Toss Etc.md (114832 bytes, 1745 lines)"
source_notes: "Complete Python implementation of multi-backend entropy module including I Ching, geomancy, and physics-based coin toss with GUI. Imported from external audit."
status: draft
tags: ["entropy", "divination", "iching", "geomancy", "coin-toss", "implementation", "module", "numogram", "oracle", "gui"]
---

# Divination Entropy Source Module

> 114 KB, 1745 lines. A complete Python module for oracular randomness with four entropy backends, full I Ching hexagram and Western geomancy support, dual GUI implementations, and direct roguelike integration hooks.

*This is a reference implementation — the actual code you can drop into a project. It documents a concrete entropy module built for numogram oracle and roguelike altar mechanics, with multiple backends ranging from standard PRNG to true atmospheric noise to chaotic logistic maps.*

---

## Overview

The module centres on the `UnusualCoinTosser` class — a flexible divination engine that can generate:

- **Binary coin tosses** (Heads/Tails) via four distinct backends
- **I Ching lines** (6–9) with proper yarrow-stalk probabilities or 3-coin method
- **Full hexagram casts** (64 King Wen sequence) with lookup and interpretation data
- **Western geomantic figures** (16 figures) with full court generation (Mothers → Daughters → Nieces → Witnesses → Judge)
- **Physics-based coin simulation** (velocity, gravity, friction) for tactile ritual altars
- **Two GUI front-ends** (Tkinter tabbed interface + enhanced canvas renderer)

All data tables (64 hexagrams, 16 geomancy figures) are embedded. All randomness sources are swappable at runtime. The module is designed to be **importable** and **roguelike-ready**.

---

## Architecture

```
UnusualCoinTosser
├── Backend selection (__init__)
│   ├── 'standard' → random.random()
│   ├── 'secure'   → secrets.randbelow()
│   ├── 'true'     → random.org atmospheric noise API
│   └── 'chaos'    → logistic map (r=3.99, deterministic chaos)
├── Core methods
│   ├── toss_coin() → 'Heads' | 'Tails'
│   └── get_iching_line(style='yarrow') → 6|7|8|9
├── Full cast pipelines
│   ├── cast_hexagram() → 6 lines + hexagram number + name
│   └── cast_geomancy() → 4 mothers → full chart (figures + Court)
├── Numogram integration
│   └── numogram_map(hexagram_number) → zone mapping (per i-ching-connections)
└── GUI front-ends
    ├── v1 (Tkinter tabbed: I Ching, Geomancy, Coin, Numogram, History)
    └── v2 (enlarged canvas + coloured numogram tab + richer ASCII hexagram renderer)
```

---

## Entropy Backends

| Backend | Source | Pros | Cons | Use case |
|---------|--------|------|------|----------|
| **standard** | `random.random()` | Fast, deterministic (seeded), no deps | Not cryptographically secure | Testing, replayable runs, deterministic divination sessions |
| **secure** | `secrets.randbelow()` | CSPRNG, no external calls | Still pseudo-random | Production oracle where unpredictability matters but no internet |
| **true** | random.org atmospheric noise | Non-deterministic, verifiable source | Requires internet, rate-limited, fallback needed | Ritual casting where "live cosmos" feeling is desired |
| **chaos** | Logistic map (xₙ₊₁ = 3.99 × xₙ × (1−xₙ)) | Deterministic chaos; stateful (consecutive tosses correlated); beautiful metaphor for I Ching's unfolding | Not crypto-secure; sensitive to initial seed | When you want *natural-feeling* correlation between successive casts; mirrors yarrow's "accumulating uncertainty" |

**Note:** The chaos backend is the most conceptually interesting for numogram work — it turns the coin sequence into a ** dynamical system**, where each toss influences the next through a simple nonlinear recurrence. This mirrors how the I Ching's yarrow-stalk method produces *context-sensitive* probabilities (the 50%→44%→12% shifts arise from the physical batch-draw, not independent flips).

---

## I Ching Subsystem

### Probabilities

| Method | 6 (old yin) | 7 (young yang) | 8 (young yin) | 9 (old yang) |
|--------|-------------|----------------|----------------|---------------|
| 3-coin (fast) | 1/8 (12.5%) | 3/8 (37.5%) | 3/8 (37.5%) | 1/8 (12.5%) |
| Yarrow (authentic) | 1/16 (6.25%) | 5/16 (31.25%) | 7/16 (43.75%) | 3/16 (18.75%) |

The module implements **both**. Yarrow probabilities are generated procedurally (simulating the 49-stalk reduction ritual), not via a static table.

### Data

All 64 hexagrams embedded as dictionary:

```python
HEXAGRAMS = {
    1:  {"name": "䷀ Creative (乾)", "lines": [9,9,9,9,9,9]},
    2:  {"name": "䷁ Receptive (坤)", "lines": [6,6,6,6,6,6]},
    ...
    63: {"name": "䷣ Already Fording (既濟)", "lines": [...]},
    64: {"name": "䷤ Not Yet Fording (未濟)", "lines": [...]},
}
```

Each cast returns: `{"primary": {...}, "secondary": {...}, "numeric": 1–64}` where primary = moving lines present, secondary = no moving lines.

**Roguelike hook:** `hex_data["primary"]["number"]` can directly spawn zone-appropriate loot/enemies. The `numogram_map()` function translates hexagram number to a numogram zone for further routing.

---

## Western Geomancy Subsystem

Full 16-figure dictionary (`GEOMANTIC_FIGURES`) with elemental/planetary correspondences (not shown here but present in source).

**Algorithm:**
1. Generate 4 "Mothers" — each a 4-bit number (odd = single line, even = double line)
2. Transpose to form 4 "Daughters"
3. Compute successive "Nieces" (sum adjacent pairs, reduce: even=double, odd=single)
4. First two nieces = "Witnesses"; third niece = "Judge"
5. Final figure (sum of Judge + Fourth Niece, reduced) = "Extra Witness" (optional)

All standard. The module outputs the full chart as a dict with figure names, bit patterns, and traditionally-associated meanings.

---

## Physics-Based Coin Toss

A minimal 2D physics simulation (velocity, gravity, friction) runs independently of the randomness backend — it takes the **outcome** from whichever backend you selected and animates a coin spinning and landing. This is for **altar displays** where the divination feels tactile. Parameters:

```python
physics_coin_toss(outcome: str, initial_velocity=5.0, gravity=9.8, friction=0.99)
```

Outcome determines heads/tails; physics just makes it look convincing. Useful for ritual rooms in roguelikes where the player *sees* the coin flip before result text prints.

---

## GUI Front-Ends

### v1 (Lines 836–855)
- Tabbed Tkinter interface
- Tab 1: I Ching (hexagram display + line-by-line cast)
- Tab 2: Geomancy (figure display + court generation)
- Tab 3: Coin & Physics (toss button + animated coin)
- Tab 4: Numogram (zone display with colour tags)
- Tab 5: History (scrollable log of all casts)

### v2 (Lines 1094–1506)
- Larger ritualistic canvas window
- Enhanced hexagram ASCII renderer (6-line vertical glyph)
- Coloured numogram tab (zone numbers coloured per region palette)
- Integrated logging across all tabs
- Richer display for both hexagram and geomantic figures

Both versions are fully functional; v2 is the polished presentation layer.

---

## Roguelike Integration Points

The module includes explicit comments for embedding in game loops:

```python
# In your roguelike main loop, at Oracle Altar:
hex_data = tosser.cast_hexagram()
# Use hex_data["primary"]["number"] to spawn loot / enemies
# Or physics toss for physical altar:
result = tosser.physics_coin_toss(tosser.toss_coin())
```

**Suggested mapping:**
- Hexagram number (1–64) → spawn table index (roll mod 64 or map to demon zone)
- Geomancy Judge → quest / curse assignment
- Coin outcome (H/T) → binary trap disarm / door lock
- Zone colour from numogram tab → UI accent for that floor

---

## Numogram Cross-References

- `numogram_map(hexagram_number)` uses mapping from `[[i-ching-connections]]` (hexagram → zone correspondence).
- Zone colours in GUI v2 Numogram tab derive from the standard zone palette (Time-Circuit gold/orange, Warp magenta/cyan, Plex purple).
- For deeper integration, see `[[numogram-divination]]` (general oracle methodology) and `[[entropy-modules-litprog]]` (which examines the broader seven-source entropy ecosystem this module could plug into).

---

## Code Structure & Reuse

The file is structured as a **single-class module** with inline data tables. To use in another project:

1. Extract the `UnusualCoinTosser` class into its own file (e.g., `divination.py`)
2. Copy `HEXAGRAMS` and `GEOMANTIC_FIGURES` dicts (or move them to a separate `data.py` if space is concern)
3. Import and instantiate: `tosser = UnusualCoinTosser(method='chaos', seed=12345)`
4. Call `tosser.cast_hexagram()` or `tosser.toss_coin()` as needed

All GUI code can be dropped into a separate script that imports the class — the two front-ends are **non-essential display layers**; the core logic is pure Python stdlib.

---

## Relationship to Existing Entropy Pages

| Wiki page | Role | This module's niche |
|-----------|------|---------------------|
| `hardware-entropy.md` | Catalog of 12 physical entropy sources (thermal, CPU, GPU, etc.) | This module *consumes* entropy — it's a **client** that could use those sources as `method='true'` backends |
| `entropy-modules-litprog.md` | Tetralogue examining two Manim visualizations (convergence vs digestion) | This is a **concrete implementation** the litprog could read and critique |
| `numogram-oracle-litprog.md` | Oracle pipeline design (seed→zone→syzygy→current→gate→reading→voice) | This module provides the **seed generation layer** (coin/I Ching/geomancy) for that pipeline |
| `divination-sources-guide.md` | Comparative survey of oracular systems (I Ching, geomancy, Ifá, etc.) | This module **implements three of those systems** (I Ching, geomancy, coin-toss) in working code |

In short: **theory → practice bridge**. The module turns the survey data into runnable rituals.

---

## Next Steps

- [ ] Extract core class to `numogram/oracle/divination_source.py` in the codebase
- [ ] Hook chaos/true backends into `numogram-entropy` plugin's `Source` interface
- [ ] Wire hexagram→zone mapping into `oracle.py`'s traversal layer
- [ ] Consider adding `method='hardware'` backend that reads from `hardware-entropy` collectors
- [ ] Port GUI v2 to p5.js web version for browser-based oracle altar


- [[geomancy-api-design]] — For interpretation layer and FastAPI service design (complements figure generation)
---

**Source file:** `raw/Coin Toss Etc.md` (preserved in canonical vault)

## See also

- [[llm-spirit-realm-modding]] — QRNG-LLM spirit-realm interface research
