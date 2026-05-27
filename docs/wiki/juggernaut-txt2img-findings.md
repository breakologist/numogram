# Zone txt2img with JuggernautXL — Findings (2026-05-26)

## Pipeline

Pure txt2img (no ControlNet) using JuggernautXL (`sdxl/juggernautXL_ragnarokBy.safetensors`) with lore-informed natural language prompts. Script at `/tmp/zone-txt2img-v2.py`. Outputs in `~/Pictures/Wall/zone-txt2img-v2/`.

## What Worked

### Model: JuggernautXL
- **Natural language prompts** far outperform Danbooru tags. Full sentences, material descriptions, and atmospheric cues trigger its photorealistic training.
- **CFG 7.0** is the sweet spot — balances prompt adherence with creative freedom.
- **dpmpp_2m + karras** scheduler produces clean, detailed results with good color separation.
- **30 steps** is sufficient; no noticeable improvement at 40+.

### Prompt Crafting
- **Specific materials** ("polished silver", "rust-coloured stone", "blood red") reliably rendered.
- **Lighting cues** ("dramatic lighting", "internal glow", "god rays") produce strong volumetric effects.
- **Geometric forms** ("pentagram", "concentric rings", "spiral descent") respected but interpreted as scenes, not diagrams.
- **Zone page lore** (from zone-N.md pages) gives better results than the wallpaper prompts from `run-zone-batch.py` — more specific, more vivid.

### Best Results by Zone

| Zone | What Worked | Why |
|------|-------------|-----|
| 0 | Crimson wireframe void, event horizon | "Black snow", "protocosmic abyss" triggered strong atmospheric output |
| 3 | Green/violet cosmic mandala | "Self-folding vortex" + "xenosignal" gave it structure |
| 4 | Volcanic stone staircase | "Rust-coloured stone", "magma glow", "cleavage" produced physical depth |
| 5 | Purple/silver mechanical mandala | "Atlantean Hinge", "gold pressure thread" → clockwork precision |
| 7 | Demonic reptilian entity | "Amphibious colonization", "toad totem" → model went literal creature |
| 8 | Neptune blue gothic spiral | "Deep sea", "cybergothic", "spiral descent" → cosmic horror |
| 9 | Copper/bronze biomechanical Plex | "Maximal density", "forty-five apertures" → intricate maximalism |

### What Didn't Work
- **ControlNet lineart** with any model (NoobAI, Juggernaut) produced strong green/cyan color bias — the lineart model itself has baked-in palette preferences.
- **Danbooru tags** on JuggernautXL are ignored — it's a photorealistic model, not anime.
- **Overly long prompts** (200+ chars) dilute focus. Best results came from 80-120 chars of concentrated description.
- **Reusing wallpaper prompts** from `run-zone-batch.py` worked but zone-page lore gave richer results.

## What I'd Like to Try Next

### Sampler Exploration
- **dpmpp_sde + exponential** — more chaotic latent paths, surreal/organic outputs
- **dpmpp_3m_sde + gaussian** — noise injection for texture variety
- **Lower CFG (4-5)** on the "outside" zones (0, 8, 9) for more alien territory

### Prompt Directions
- **Zone-as-character** — personified entities rather than landscapes (Zone 7 worked as creature; Zone 2's "ghosts in the doubling" could too)
- **Zone-as-task/scene** — "what does Zone 4 *do*?" narratives, not just "what does it look like?"
- **Cross-zone composites** — two zones in one image (e.g., Zone 3↔6 Warp loop as a single piece)

### Other Models
- **SDXL base** (`sd_xl_base_1.0.safetensors`) — less opinionated than Juggernaut, might give more varied outputs
- **NoobAI with natural language** (not tags) — untested
- **ACE Step / NetaYume** — available but unknown behaviour

### Compositing
- Overlay original yantra SVG lines on txt2img output for hybrid precision+atmosphere
- Colour-tonemap generated images toward zone palettes via ImageMagick

## Scripts

- `/tmp/zone-txt2img-v2.py` — main batch runner (10 zones, lore prompts)
- `~/Pictures/Wall/yantra_controlnet.py` — ControlNet variant (tested, colour bias issue)
- `/tmp/yantra-iterate.py` — single-zone iterative test harness
- Outputs: `~/Pictures/Wall/zone-txt2img-v2/`, `~/Pictures/Wall/yantra-txt2img/`, `~/Pictures/Wall/yantra-compare/`