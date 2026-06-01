---
title: Risomorphism-1911 — ASCII Art / Eikon Pipeline
created: 2026-06-01
tags:
  - ASCII
  - eikon
  - visual
  - pipeline
  - numogram
status: annotation
source: /home/etym/Risomorphism-1911-main (local clone)
---

# Risomorphism-1911 — ASCII Art / Eikon Pipeline

**Repo:** `/home/etym/Risomorphism-1911-main`  
**Public URL:** <https://github.com/plntrprotocol/Risomorphism-1911>  
**License:** MIT  
**CLI:** `ascii-pipeline` (entry point installed by `pip install -e .`)

Not just an ASCII renderer. The explicit design brief is **Herm-style animated eikons** — exactly the terminal/avatar format used elsewhere in this project (tsubuyaki, zone portraits, numogram cellular automata). The base grid is 48×24, matching Herm avatar dimensions. Outputs are `.txt` stills and `.eikon` animated frames.

---

## Canonical Presets

| Preset | Charset | Target | Best for |
|--------|---------|--------|----------|
| `stroke-clarity` | Dense ref 12-glyph (`@$#MHAGXS532;:,. `) | 48×24 | Crisp silhouette; safe default; scales to 768×384 |
| `d30-dense` | D30 68-glyph extended palette | 48×24 | Dense cyber-noir texture; edge-aware Laplacian block reduction; garble-risk on high-contrast geometric scenes |
| `braille-detail` | Unicode Braille (U+2800..U+28FF) | 48×24 | Max detail / halftone; ignores terminal font glyph concerns |
| `eikon-motion` | D30 charset | 48×24 | Video → animated eikon; used by `build-eikon` |

**Intermediate grids:** `d30-dense` uses 384×192 intermediate then collapses; blocking makes it heavy above N=8.

---

## Resolution Scaling

Base `48×24` is the canonical hermetic avatar. `--scale N` multiplies both grid and intermediate:

- N=1: 48×24 (avatar)
- N=4: 192×96 (fullsize/showcase)
- N=8: 384×192 (large)
- N=16: 768×384 (max practical)

`render-image --fullsize` is shorthand for `--scale 4`.

---

## Quality Diagnostics

```bash
ascii-pipeline diagnose --input out.txt --pretty
```

Key metrics: `unique_glyphs_mean`, `fill_ratio`, `heavy_ratio`, `light_ratio`, `braille_ratio`, `motion_char_diff_mean`, plus a `verdict` (`high-contrast`, `low-contrast-garble-risk`, `braille-dominant`). Always visually verify; scene-class images (architecture, cosmic) can beat portrait heuristics.

---

## Workflow Bridge to Our Stack

- **tsubuyaki / p5 sketches:** Risomorphism is an alternative/complement to p5-driven ASCII; produces `.txt`/`.eikon` files p5 can consume.
- **mod-writer spectrograms:** convert spectrogram PNG → ASCII still/animation using the same 48×24 grid as Herm avatars. A spectrogram rendered in `stroke-clarity` at scale 4 becomes a `.txt` that fits existing display pipelines.
- **numogram visualisation:** project zone diagrams, seven-segment glyphs, or ladder/labyrinth layouts through `d30-dense` for a cyber-terminal aesthetic.
- **Roguelike map export:** ASCII dungeon map → preview PNG via `render-preview`.

---

## Integration Points

| Hermes current | Tie-in |
|----------------|--------|
| Numogram | Zone glyphs as ASCII (seven-segment render → D30 charset) |
| Audio | Spectrogram/Power-of-10 scaled power → ASCII timeline |
| Lore | .eikon animation as a “moving rune” format for entity portraits |
| Visual | Automated wallpaper generation with zone chroma + ASCII overlay |

---

## Action Items

- [ ] Run CLI smoke test on a sample image to confirm `ascii-pipeline` entry point
- [ ] Test spectrogram → `.txt` conversion at 48×24 and 192×96
- [ ] Evaluate `d30-dense` for numogram glyph aesthetic vs `stroke-clarity`
- [ ] Check if `.eikon` format is suitable for embedding in wiki (preview PNG)
- [ ] Add `ascii-pipeline` to `requirements-numogram.txt` if smoke test passes

## See Also

- [[cables-gl]] — node-based visual counterpart; could pipe Risomorphism outputs into cables patches
- [[tsubuyaki]] — code-driven generative ASCII; Risomorphism is imaging-pipeline-driven
- [[visual-wallpaper-pipeline-status]] — related image/visual tooling
- [[mod-writer]] — audio source material for spectrogram ASCII conversion
