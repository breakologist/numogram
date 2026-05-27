# Yantra ControlNet — Empirical Findings (2026-05-26)

## Pipeline

SVG zone yantra (zone-yantras-v2/) → `rsvg-convert` raster (1024×1024) → ControlNet Lineart (noob-sdxl-lineart) → txt2img via ComfyUI API.

## Key Discovery: Color Bias

**Across all variants, the diffusion model overrides zone colour palettes toward green/cyan.** This is consistent regardless of:
- Prompt style (wiki natural language vs Danbooru tags)
- Model (NoobAI-XL vs JuggernautXL)
- ControlNet strength (0.85 vs 0.95)
- CFG scale (5.0 vs 7.0)

### Variant Comparison (Zone 3 — Fire)

| Variant | Result | Geometry | Notes |
|---------|--------|----------|-------|
| NoobAI + wiki + CN 0.85 | Neon green, navy | Spiral-triangles preserved | Cool plasma, no fire |
| NoobAI + Danbooru + CN 0.85 | Dark olive, cyan | Sharp, crisp | Toxic/underwater |
| NoobAI + wiki + CN 0.95 | Forest green, edge glow | Vector-like, sharpest | Hard-surface blueprint |
| JuggernautXL + wiki + CN 0.85 | Mint green, brown texture | Organic/etched | Photographic materiality |
| SDXL base | Not tested | — | — |

### Interpretation

The ControlNet lineart model + SDXL latent space has a strong green/cyan bias for geometric linework on dark backgrounds. Prompt colour terms ("red", "amber", "fire") are overridden. This is structural — the model interprets "geometric linework" as "digital/cyber/synthwave" aesthetic.

## Fixes Explored (not yet applied)

1. **Compositing** — generate with CN guidance, then post-process: overlay original SVG lines in zone palette via ImageMagick, or colour-tonemap green→warm
2. **SDXL Base model** — less stylistically biased than NoobAI (anime) or Juggernaut (photorealism)
3. **Prompt model-switching** — use natural language for Juggernaut, Danbooru tags for NoobAI
4. **No-CN baseline** — pure txt2img for comparison (workflow wiring needs fix)

## Files

- Script: `~/Pictures/Wall/yantra_controlnet.py`
- Comparison runner: `/tmp/yantra-compare.py`
- Outputs: `~/Pictures/Wall/yantra-controlnet/` (full batch)
- Compare outputs: `~/Pictures/Wall/yantra-compare/` (6 variants)

## Recommended Next Direction

JuggernautXL showed the most promising materiality (crystalline depth, organic texture). Iterate on:
- Sampler/scheduler combos (dpmpp_2m + karras)
- ControlNet strength sweep (0.8, 0.85, 0.9, 0.95)
- Compositing: overlay original SVG lines post-generation
- Prompt tuning per model: natural language for Juggernaut, Danbooru for NoobAI