---
title: AQ Synx Augmentation
created: 2026-04-27
last_updated: 2026-04-27
tags: [aq, synx, augmentation, cipher, base-36, experimental]
status: draft
---

# AQ Synx (Base-36 Augmentation)

Experimental base-36 augmentation to Alphanumeric Qabbala. Source: `ciphers.news` (external).

## Concept

Standard AQ uses A=10, B=11 … Z=35 (base-36) but maps to decimal via mod-9 reduction through the numogram zones. Synx introduces a parallel cipher mapping that preserves base-36 digits while shifting the zone assignment through an overlay.

## Implementation

- `oracle.py` `--synx` flag enables dual-cipher computation
- `SYNX_VALUES` dictionary provides per-digit zone mapping
- `compute_synx(text)` returns base-36 sum and zone
- Visual feedback: cyan HSL(180,44,66) overlay on numogram visualizer v7

## Visualizer

`numogram-visualizer-v7-djynxxogram.html` includes Synx toggle:
- Displays both AQ zone and Synx zone side-by-side
- Drift example: "You're not escaping this simulation" → AQ=666→9, Synx=3108→3

## Status

- **Exploratory** — not yet integrated into core AQ calculation
- Watchlist item; may inform future cipher expansion
- Related: [[alphanumeric-qabbala]], [[numogram-visualizer-v7]]
