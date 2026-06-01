---
title: Eikon Pipeline Notes
created: 2026-05-31
tags: [eikon, herm, ascii-pipeline, risomorphism, avatar]
status: active
---

# Eikon Pipeline Notes

## Core Tools

- **Risomorphism-1911** (`~/Risomorphism-1911-main/`) — the ASCII art pipeline that powers Herm eikons.
- **Herm** (`~/herm-dev/`) — the TUI itself, with eikon handling in `src/service/eikon.ts` and dialogs.

## Key Presets (48×24 target)

| Preset            | Character                        | Best For                              | Hermes Recommendation      |
|-------------------|----------------------------------|---------------------------------------|----------------------------|
| `stroke-clarity`  | High-contrast, crisp outlines    | Clean silhouettes, maximum readability | **Strong default choice**  |
| `d30-dense`       | Cyber-noir, varied stroke weight | Portraits with texture/gradients      | Excellent for graphic style |
| `braille-detail`  | Halftone / Braille heavy         | Maximum perceived detail              | Usually too busy           |
| `eikon-motion`    | Frame-based animation            | Video sources (owl-style)             | Good for v2 animated version |

**Rule of thumb**: Start with `stroke-clarity`. Use `d30-dense` when you want more texture and a slightly denser feel.

## Source Image Guidelines

- Strong silhouette > fine detail
- Square or near-square sources with centered figure perform best
- Slightly zoomed-in framing (head + upper chest/shoulders) reads better than full body at 48×24
- Simple graphic sources often outperform complex ones (see default "Nous girl" vs owl)
- Complex video sources *can* work well when using the motion pipeline (owl example)

## Animation Approaches

- **State-based** (default girl): Multiple static sources baked into `idle / listening / thinking / speaking / working / error`. Reacts to user activity (e.g. headphones on/off).
- **Motion-based** (owl): Video input → `eikon-motion` pipeline → smoother frame animation.

Both are valid. The default girl proves that even "static" eikons can feel alive through state changes.

## Recommended Workflow for New Eikons (Hermes)

1. Generate source image(s) in **ComfyUI** (preferred) or cloud tools.
2. Target a **graphic/abstract** treatment with classical structural cues (caduceus + wing elements).
3. Favour clean high-contrast lighting (light subject on pure black).
4. Test with `stroke-clarity` first.
5. Use Herm's built-in **Eikon Studio** tab for final tuning (contrast, invert, symbols, zoom/pan).
6. For animated v2: prepare video source and use `eikon-motion` pipeline.

## Useful Commands

```bash
# Render a still image
ascii-pipeline render-image \
  --input source.png \
  --preset stroke-clarity \
  --out hermes.txt \
  --preview-out preview.png

# Diagnose an existing eikon
ascii-pipeline diagnose --input hermes.eikon --pretty
```

## References

- `~/Risomorphism-1911-main/README.md`
- `~/Risomorphism-1911-main/docs/canonical-foundation.md`
- `~/Risomorphism-1911-main/examples/portrait/README.md`
- Herm source: `~/herm-dev/src/service/eikon.ts` and `src/dialogs/`

## Future Work

- Create a second, more animated "owl-style" Hermes eikon
- Explore `d30-dense` for a denser cyber-noir variant
- Document ComfyUI workflows that produce good eikon sources

## Related

- [[visual-wallpaper-pipeline-status]] — ComfyUI infrastructure and visual generation pipelines
