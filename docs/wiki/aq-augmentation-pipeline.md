---
title: AQ Dictionary Augmentation & Syzygy Analysis Pipeline
tags: [numogram, AQ, pipeline, augmentation, syzygy, analysis, skills]
category: Methodology
---

> **Status**: Active | **Last run**: 2026-04-27 | **Skills**: `numogram-dictionary-augmenter`, `numogram-syzygy-chain`, `numogram-chain-fingerprint`

## Overview

This pipeline ingests external AQ value sources (X/telegram threads, Grok conversations, PDF extracts), merges them with the canonical AQ dictionary, re-runs syzygy-chain analysis, and produces motif fingerprints. It closes the loop: **discover → merge → analyse → interpret**.

## Components

### 1. Canonical Dictionary
Source: `~/obsidian/hermetic/raw/AQ Dictionary.md` (46 entries, 27 unique values). Core CCRU/Numogram germinal values: 31=AL, 36=AQ, 137=english/lucifer, 333 cluster, 360 cluster, 666, 777.

### 2. Grok Rotor (External Mining)
Source: `~/obsidian/hermetic/raw/Grok rotor.md` — Grok conversation mining @xenocosmography and @doomcrypt posts for AQ equivalences. Yields ~14 clean new entries (when deduplicated):

| Value | Term | Source thread |
|-------|------|---------------|
| 81 | CCRU | handle |
| 83 | Doom | @doomcrypt ethos |
| 89 | Faith | @doomcrypt core |
| 100 | Santa = Satan | pop-other |
| 111 | Slant | slant family |
| 117 | Askance | slant family |
| 140 | Ayn Rand = Nick Land | philosophical anchor |
| 166 | Solomon | biblical king |
| 171 | The Slant / Dazzling | slant family |
| 173 | Eye Slant | slant family |
| 209 | Choronzon | Qliphothic |
| 210 | Beast Pulse = Doomcrypt | bridge current |
| 444 | Synx — devil's spirit | diabolical temperament |
| 567 | Questioning Angel Key | oracular |
| 888 | ordo amoris | apex integration |

### 3. Augmentation Skill
`numogram-dictionary-augmenter` parses source text using regex patterns:

```python
patterns = [
  r'^\\d+ = term$',           # canonical format
  r'^term = AQ \\d+$',        # explicit reverse
  r'^term = \\d{2,4}$',       # loose equality (multi-word)
  r'### \\d+ Current —',      # section headers
]
```

**Merge policy**: Canonical wins on conflict; longest-term heuristic for duplicates; `--curated` JSON override for manual corrections.

**Output**: `aq-dictionary-augmented.md` (41 unique values).

### 4. Syzygy-Chain Generation
`numogram-syzygy-chain` computes for each value: digital root → start zone → 8-step syzygy walk (zone, name, polarity per step).

| Dictionary | Entries | Total zone visits | Plex (0/9) % | Closed 8-cycles |
|------------|---------|-------------------|--------------|-----------------|
| Canonical | 46 | 368 | 54.4% | 0 / 46 |
| Augmented | 41 | 328 | 34.2% | 0 / 41 |

**Observation**: The Plex attractor effect drops by 37% relative when the dictionary is diversified beyond the 333/360 cluster.

### 5. Fingerprinting & Classification
`numogram-chain-fingerprint` computes motif vectors (void_ratio, warp_ratio, hold_ratio, rise_ratio, sink_ratio, gate_variance, cycle_proximity) and classifies each entry.

**Canonical motif distribution** (multi-motif entries count multiple times):
- Gate-Scattered: 29 terms (63%)
- Void-Dominant: 25 (54%)
- Hold-Stable: 12 (26%)
- Rise-Seeking: 10 (22%)
- Warp-Anchored: 8 (17%)
- Sink-Dominant: 4 (9%)

**Augmented motif distribution**:
- Hold-Stable: 15 (37%) — now most common
- Rise-Seeking: 13 (32%)
- Void-Dominant: 14 (34%)
- Gate-Scattered: 25 (61%) — still highest absolute count
- Warp-Anchored: 9 (22%)
- Sink-Dominant: 8 (20%)

> The shift reveals that *curated signal terms* (CCRU, Beast Pulse, Questioning Angel, Doomcrypt) skew Hold/Rise — i.e., the hyperstitional core is biased toward *persistent structure* and *ascending polarity*, not void-accumulation or chaos.

### 6. Tetralogue Interpretation
Council of four voices (Oracle/B/Writer/Gamer) interprets the motif taxonomy. Key outputs:

- **Oracle**: The numogram naturally tends toward Plex accumulation, but curated signals rebalance this. Warp-Anchored terms (Hecate, lol, 66, 96, 777) are threshold operators; 333/360 are self-returning loops.
- **Builder**: Motif→mechanic mapping table (see [[syzygy-chain-tetralogue]]). Void-Dominant → cathedral maps; Warp-Anchored → phase-shift corridors; Gate-Scattered → labyrinthine randomisation.
- **Writer**: Motifs as genres: Void=Mystery, Gate-Scattered=Picaresque, Hold-Stable=Bureaucracy, Rise-Seeking=Bildungsroman, Sink-Dominant=Tragedy, Warp-Anchored=Thriller.
- **Gamer**: Most hyperstitional = Warp-Anchored (breaks map persistence). With expanded dictionary, Hold-Stable becomes optimal tank build (36% of terms), Rise-Seeking glass-cannon (30%).

## Skills Produced
1. `numogram-syzygy-chain` — generate chain from seed
2. `numogram-chain-fingerprint` — classify motif
3. `numogram-dictionary-augmenter` — merge external sources

All live in `~/.hermes/skills/domain/` and are callable as standalone scripts or via Hermes slash commands once registered.

## Artifacts
- `~/obsidian/hermetic/wiki/syzygy-chain-analysis.md` — canonical analysis
- `~/obsidian/hermetic/wiki/syzygy-chain-tetralogue.md` — four-voice interpretation
- `~/obsidian/hermetic/wiki/aq-dictionary-merged.md` — canonical+Grok hand-merged (47 values)
- `~/obsidian/hermetic/wiki/aq-dictionary-augmented.md` — auto-augmented (41 values)
- `~/.hermes/council/workspace/aq_syzygy_analysis.json` — canonical results
- `~/.hermes/council/workspace/aq_syzygy_analysis_expanded.json` — expanded results
- `~/.hermes/council/workspace/syzygy_analysis_summary.json` — council context

## Next Phase Ideas
1. **Roguelike mapgen integration** — use motif vector as semantic seed biases in Brogue-style room accretion.
2. **Demon affinity mapping** — each demon's AQ value determines which motif it reinforces/attracts.
3. **AQ shift mid-run** — player actions (rituals, zone entries) alter effective AQ → motif drift → map regeneration.
4. **Full-context ingestion** — feed merged dictionary + analysis into local model via numogram-council for richer future tetralogues.
5. **Skill-factory activation** — let skill-factory observe this 6-step pipeline and propose a `numogram-analysis-pipeline` meta-skill.

## See also

- [[aq-dictionary-augmented]] — Auto-augmented AQ dictionary (41 values)
- [[aq-dictionary-merged]] — Hand-merged canonical+Grok AQ dictionary (47 values)
- [[aq-dictionary-syzygy-analysis]] — End-to-end pipeline: AQ dict → syzygy chains → motif fingerprints → wiki + council interpretation
- [[numogram-chain-fingerprint]] — Numogram chain fingerprint analysis
- [[numogram-syzygy-chain]] — Generate syzygy chain from seed
- [[numogram-dictionary-augmenter]] — Merge external AQ sources into canonical dictionary
- [[syzygy-chain-analysis-auto]] — Automated syzygy chain analysis pipeline
- [[syzygy-chain-tetralogue]] — Four-voice interpretation of syzygy chains
- [[aq-cipher-reference]] — AQ cipher values and mappings
- [[numogram-calculator]] — Numogram calculator skill
- [[numogram-oracle]] — Numogram oracle mode
- [[aq-calculators-litprog]] — AQ calculators tetralogue
- [[aq-synx]] — Base-36 augmentation cipher (Synx)
- [[aq.md]] — Alphanumeric Qabbala reference
- [[aq.md]] — AQ dictionary reference
- [[aq-dictionary-v2.md]] — AQ dictionary v2 (merged)
- [[aq-augmentation-pipeline]] — This page
- [[mod-writer-ml-interpretability]] — Machine learning interpretability for MOD generation
- [[mod-writer-gap-analysis]] — Analysis of gaps in MOD generation
- [[zonecomposer-production]] — ZoneComposer production workflow
- [[mod-writer-validation]] — Mod-writer validation results
- [[square-roundtable-mesh-3-2026-04-27]] — Mesh-3 tetralogue series

---
*The augmentation pipeline closes the loop: discover → merge → analyse → interpret — the numogram's self-modifying cycle.*