---
title: Planchette ASCII Glyph Channel
category: oracle
tags: [numogram, planchette, ascii-art, box-art, oracle, glyph-channel]
---

# Planchette ASCII Glyph Channel

`oracle.py --seed N --planchette --ascii-glyph` renders a terminal-safe
ASCII planchette card with per-zone glyphs, particle sigils, and a
gate-arc ring.

## Invocation

```bash
python3 oracle.py --seed 192855 --planchette --ascii-glyph
```

## Output: 48-wide × N rows

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃     ZONE 3  ·  Warp            ·  AQΣ=140    ┃
┣──────────────────────────────────────────────┫
┃  Current     3 [zx]                        ┃
┃  Gate        Gt-06 → Z6                    ┃
┃  Syzygy      6                             ┃
┃  Polarity    +  —  Process / becoming      ┃
┃  Region      Warp                          ┃
┃  Particle    ?                             ┃
┃               ━━╾━╾┳━┓╾━╾━━━                 ┃
┃                ┗━━━┻━━━┻━━━┛                 ┃
┃                       🝤                      ┃
┃──  ═──  ═──  ═Z3  ═──  ═──  ═↑6  ═──  ═──  ═──┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

## Zone-Specific Glyphs

| Zone | Glyph idea |
|------|-----------|
| 0 Void | Spiral-out / voidweb |
| 1 Surge | `/\ /\ /\` upward triangles |
| 3 Release | `━━╾━╾┳━┓╾━╾━━━` overflow |
| 5 Pressure | `├─╁─┤ ║STRESS║ ├─╁─┤` stress grid |
| 7 Blood | `┌─♥─┬─♥─┐ ──●──` blood lattice |
| 9 Plex | `█ P L E X █` full-block |

## Particle Sigils

Map zone → sigil drawn below the glyph block; see `_PART` dict in
`oracle.py`.

## Gate-Arc Ring

Bottom row ticked at 10 positions (one per zone), with `Z{n}` at
current zone and `↑{gate}` at gate target. Cyan for zone, amber
for gate target.

## Assets

Full 10-zone ASCII glyph gallery saved to wiki assets:
`planchette-glyphs/`

## See

- [[planchette-svg-renderer]] — the SVG card renderer
- [[zone-naming-triad]] — per-zone naming
- `oracle.py --planchette` — plain ASCII planchette (no glyphs)
