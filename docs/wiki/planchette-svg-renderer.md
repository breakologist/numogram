---
title: Planchette SVG Renderer
category: oracle
tags: [numogram, planchette, divination, svg, art, renderer]
source: planchette-svg.py, planchette-cards
---

# Planchette SVG Renderer

`planchette-svg.py` is the canonical Tier 2c build script that generates
gold/indigo planchette cards from oracle `--planchette` output or direct
key-value arguments.

## File

`~/numogram/cli/scripts/planchette-svg.py` — stdlib-only Python (Pillow
optional for embedded medallion PNG; falls back to SVG-only mode).

## Invocation

```bash
# Standalone
python3 planchette-svg.py --zone 3 --current 3 --gate 6 \
    --syzygy 3::6 --aq 140 --particle ZX --word Release \
    --reading "Abysmal Comprehension."

# For each zone in batch
for z in $(seq 0 9); do
  python3 planchette-svg.py --zone $z ...
done > /tmp/gallery/
```

## Output: `450 × 620 px`

```
┌────────────────────────────────────────────────────┐
│  TITLE BAR (gold halo text)                        │
├────────────────────────────────────────────────────┤
│  SYZYGY READING                                    │
│  Current / Gate / Syzygy / Polarity / Region / Particle │
│              PIXEL MEDALLION EMPTY SPACE           │
│  ZONE 3 . RELEASE. AQΣ=140                         │
│  ABYSSMAL COMPREHENSION.                           │
│                                                    │
│  ════════════════════════════════════════════════   │
│  GATE-ARC RING — ZONE 3 · ZONE 6                   │
└────────────────────────────────────────────────────┘
```

## Data Fields

| Unit | Position | Notes |
|------|----------|-------|
| Zone Circle   | left column, mid-gap      | Nested rings, zone number centred |
| Data Fields   | right column, top         | 6 rows |
| Pixel Medallion | centre gap              | 112×112 (Pillow if available, SVG fallback) |
| Reading Verse | above arc band            | Wraps to two lines |
| Gate-arc Ring | bottom                   | 10 zone ticks, gold arc from zone to gate |

## Planchette Cards Gallery

All 10 zone cards saved to:
`/home/etym/.hermes/obsidian/hermetic/wiki/assets/planchette-cards/`

The `--ascii-glyph` counterpart: [[planchette-ascii-glyph]]

## Dependencies

- Python 3.10+
- Pillow: `pip install Pillow` (optional — SVG medallion fallback available)
