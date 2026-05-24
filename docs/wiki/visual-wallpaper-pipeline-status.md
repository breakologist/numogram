# Visual / Wallpaper Pipeline — Status & Directions

*Last updated: 2026-05-19*

## Current Infrastructure

### ComfyUI
- **Version:** 0.17.0
- **Workspace:** `~/ComfyUI/`
- **GPU:** RTX 3060 (12GB VRAM), CUDA 13.2, driver 595.71
- **Launch:** `cd ~/ComfyUI && source comfyui-env/bin/activate.fish && python main.py --listen 0.0.0.0 --port 8188`
- **CLI:** `comfy-cli` v1.10.1 installed via pipx, workspace set to `~/ComfyUI/`

### Checkpoints (available)
| Model                                                                                    | Type                    | Size    |
| ---------------------------------------------------------------------------------------- | ----------------------- | ------- |
| NoobAI-XL-v1.1                                                                           | checkpoints/Noob        | 6.9 GB  |
| Illustrious-XL-v2.0                                                                      | checkpoints/Illustrious | 6.8 GB  |
| juggernautXL_ragnarokBy                                                                  | checkpoints/sdxl        | 6.9 GB  |
| sd_xl_base_1.0                                                                           | checkpoints/sdxl        | 6.8 GB  |
| sd_xl_turbo_1.0_fp16                                                                     | checkpoints/sdxl        | 6.8 GB  |
| ace_step_v1_3.5b                                                                         | checkpoints             | 7.5 GB  |
| acestep_v1.5_turbo                                                                       | checkpoints             | 4.7 GB  |
| anime-preview3-base                                                                      | checkpoints/Anima       | 4.1 GB  |
| dreamshaper_8                                                                            | checkpoints/1.5         | 2.1 GB  |
| photon_v1                                                                                | checkpoints/1.5         | 2.1 GB  |
| Dvine-v11.1-Illustrious                                                                  | checkpoints/Illustrious | 6.8 GB  |
| oneObsession_v16Noobai                                                                   | checkpoints/Noob        | 6.8 GB  |
| xavier_v10                                                                               | checkpoints/Noob        | 6.8 GB  |
| autismmixSDXL_autismmixConfetti                                                          | checkpoints/Pony        | 6.8 GB  |
| GothaLomo Chroma v1.2 FP8                                                                | checkpoints/Chroma      | 8.9 GB  |
| NetaYumev35 (fine-tuned from [Neta Lumina](https://huggingface.co/neta-art/Neta-Lumina)) | checkpoints             | 10.3 GB |

### Custom Nodes (installed)
ComfyMath, ComfyUI_Comfyroll_CustomNodes, comfyui-autocomplete-plus, comfyui-custom-scripts, comfyui-downloader, comfyui-easy-noobai, comfyui-easy-use, comfyui_essentials, comfyui-image-saver, comfyui-impact-pack

### Wallpaper Pipeline

```
numogram-zone-wallpapers.py        ← Direct ComfyUI REST API, NoobAI checkpoint
         │
         ▼
    ~/Pictures/Wall/zones/         ← Raw zone wallpapers (1920×1080, 10 zones)
         │
composite-zone-glyphs.sh           ← ImageMagick overlay (zone #, name, syzygy, AQ, color)
         │
         ▼
    ~/Pictures/Wall/zones-glyphed/ ← Annotated wallpapers
         │
         ▼
    Conky (~/.config/conky/)       ← Desktop display via conky.conf + numogram-quotes.txt
```

Some wallpapers also generated via **Grok Imagine** (before ComfyUI pipeline was mature).

### Scripts
- `~/Pictures/Wall/numogram-zone-wallpapers.py` — Builds workflow JSON from scratch using raw `urllib`, queues 10 zones sequentially, downloads outputs. Uses NoobAI-XL, 36 steps, euler_ancestral, sgm_uniform.
- `~/Pictures/Wall/composite-zone-glyphs.sh` — Overlays zone number (large), name, syzygy pair, AQ values, Hermes glyph per zone. Uses zone palette matching manim-numogram.

### Archives
- `~/Pictures/Wall/zones/` — Tarballs of generated zones (30.tar.gz, 40.tar.gz, zoneso.7z, anima-zones.7z)
- `~/Pictures/Wall/zones-glyphed/` — glyphedzones.7z

## What the ComfyUI v5.1.0 Skill Unlocks

The `creative/comfyui` skill (`~/.hermes/skills/creative/comfyui/`) provides structured scripts we aren't yet using:

| Script | Current State | What It Would Do |
|--------|-------------|------------------|
| `run_workflow.py` | ❌ not used | Parameter injection, progress monitoring, output download via structured CLI |
| `run_batch.py` | ❌ not used | Sweep seeds/params in parallel (e.g. 10 zones × 3 seeds = 30 images) |
| `extract_schema.py` | ❌ not used | See what's controllable in any workflow without reading the JSON |
| `auto_fix_deps.py` | ❌ not used | Auto-install missing nodes/models for a given workflow |
| `health_check.py` | ❌ not used | Full verification checklist |

## Possible Directions

### Near-term (would work with current setup, no new credits needed)

1. **Upgrade wallpaper script to use `run_batch.py`** — Replace the ad-hoc urllib loop with the structured batch script. Get parallel generation, progress monitoring, seed sweeps.

2. **Style transfer on existing walls via img2img** — Use `run_workflow.py --input-image` with existing zone walls as source, different checkpoint/prompt for style variants.

3. **AnimateDiff video loops** — The AIDMA workflow JSON is already in `~/ComfyUI/`. Animate Diff short clips for each zone, feed into TouchDesigner MCP.

4. **Conky wall cycling** — Use feh or hyprctl to rotate between glyphed zone walls on a timer.

5. **I-Ching hexagram walls** — All 64 hexagrams mapped to zones (via digital root). Generate walls for hexagram families.

6. **ControlNet-guided numogram diagrams** — Feed SVG numogram diagrams as ControlNet input to guide generation toward specific zone geometries.

### Medium-term (when SuperGrok/Grok credits return)

7. **Grok Imagine zone walls** — Use Grok Imagine for walls the ComfyUI pipeline can't easily produce (complex compositions, specific aesthetics). Compare NoobAI vs Grok Imagine styles.

8. **x_search → Grok → wallpaper pipeline** — Find CCRU threads on X, have Grok synthesize visual descriptions, feed into ComfyUI as prompts.

### Cross-current

9. **Zone MIR feature → wallpaper prompt** — Extract MIR features from zone audio (mod-writer output), map spectral centroids to color palettes, feed into wallpaper pipeline. Audio → Visual synesthesia pipe.

10. **Wallpaper → roguelike tiles** — Downscale zone walls to tile sprites for the roguelike. Each zone gets a distinct visual tile.

11. **AQ values as generation seeds** — Use zone name AQ sums, syzygy pair AQ diffs, or oracle-reading AQ chains as the random seed for image generation. E.g. Zone 1 "SURGE" → AQ sum 160 → seed `160`; Zone 6 "HINGE" → sum 107. Each wallpaper encodes its numerological signature. Could be extended to: AQ of a specific demon call → seed for that demon's wall; AQ of a syzygy chain → multi-image sequence with linked seeds; oracle reading AQ vectors → wallpaper palette via seed-space proximity.

## Pipeline Evolution

| Date | Change |
|------|--------|
| 2026-05-19 | `run-zone-batch.py` created — structured pipeline using ComfyUI skill's `run_workflow.py`. Template extracted to `zone_template_api.json`. `comfy-cli` installed. |
| 2026-05-19 | Zone 0 iterated through 4 generations (vision-guided). Final: wiki-informed prompt + CFG 5.0 + NoobAI detailer LoRA at 0.6. |
| 2026-05-19 | Full 10-zone batch generated (baseline, no LoRA). |
| 2026-05-19 | NoobAI detailer LoRA integrated into workflow template (`zone_template_api.json`). All zones can now use `--lora-strength`. |
| 2026-05-19 | Zone 6 iterated (2 generations): added Saturnian hexagon, abstract cyclones, violet/teal gradient via wiki lore. |
| 2026-05-19 | Zone 5 re-prompted for Atlantean hinge (self-decadence, closed loop, Jovian pressure) vs Zone 6's Lemurian hinge (subdecadence, open pivot). |
| 2026-05-20 | Full v2 glyphed wallpaper set deployed as `zone*-glyphed-v2.png` in `~/Pictures/Wall/`. |
| 2026-05-20 | I-Ching Yang (☰ Qian/Creative) and Yin (☷ Kun/Receptive) walls begun — Chinese ink-wash / gold-leaf aesthetic. |
| 2026-05-20 | Discovered SD resources at `~/raw/SD/` — NoobAI, Illustrious, and prompt engineering guides. |

## NoobAI-XL Settings & Prompt Notes (from I-Ching wall experiments)

### Recommended Settings
| Parameter | Value | Notes |
|-----------|-------|-------|
| **CFG** | 3.0–5.5 | Above 5.5 forces rigid adherence; 7.0 can force unwanted anime characters |
| **Steps** | 28–40 | Euler a needs fewer; complex scenes benefit from 40 |
| **Sampler** | `euler_ancestral` | NoobAI standard; matches euler a |
| **CLIP skip** | None | Not needed for NoobAI/Illustrious |
| **VAE** | SDXL default | NoobAI ships with baked-in VAE |
| **Resolution** | 1920×1080 works | Official recommended: 768×1344, 832×1216, 1024×1024, 1344×768 |

### Prompt Engineering
- **Quality prefix**: `"masterpiece, best quality, absurdres, highres"` before the descriptive prompt
- **Weighted tags**: `(cinnabar red:1.3)` works but can trigger anime character generation
- **Anti-character battle**: Use strong negatives to suppress anime faces: `(anime girl:1.5), (face:1.3), character, person, human, woman, man`
- **Color foregrounding**: Put desired colors early in the prompt, e.g. `(jade green:1.3) glowing central sigil`
- **Danbooru tag format**: Underscores become spaces, parentheses escaped: `lucy \(cyberpunk\)`
- **Natural language works**: NoobAI does understand plain English, not just Danbooru tags

### Recommended Negative Prompts
- **Default blocklist**: `"text, watermark, signature, anime girl, character, person, cluttered, busy, soft edges, blurry"`
- **For abstract/non-character images**: Add `(face:1.5), (hair:1.4), woman, man, boy, girl, portrait, skin, eyes, mouth`
- **For quality suppression**: `"worst quality, bad quality, low quality, bad anatomy, ugly, distorted"`
- **For NoobAI specifically**: The anime bias means character suppression needs heavier weights than other models

### LoRA Notes
- **NoobAI detailer**: `noob/NOOB_EPSv1_1_detailer_by_vlnvk_v1_0.safetensors` at 0.6 strength — adds crisp detail
- **Illustrious LoRAs** (18 available) should be compatible since NoobAI-XL is based on Illustrious-XL
- **SDXL LoRAs** also compatible (architecture-shared)

### Future Directions
- **Illustrious-XL-v2.0** model for East Asian art styles — tested 2026-05-20 (see below)
- **Neo-Nihonga_Pop_Surrealism LoRA** at 0.8 strength — genuine mineral pigment texture, gold leaf, aged silk/paper aesthetic
- **Pony models** (`autismmixSDXL`) as alternative base

## Illustrious-XL-v2.0 + Neo-Nihonga Findings (2026-05-20)

### Settings Used
| Parameter | Value | Notes |
|-----------|-------|-------|
| **CFG** | 5.0 | Recommended 3-5.5 for Illustrious |
| **Steps** | 40 | DPM++ benefits from more steps |
| **Sampler** | `dpmpp_2m` + `karras` | Richer texture than euler a. Good for landscapes, dragons, textured scenes |
| **Sampler (Yin/stillness)** | `euler` + `normal` | Softer, dreamier. Good for water, mist, nocturnal scenes |
| **Sampler (abstract)** | `ddim` + `ddim_uniform` | Cleaner, sharper edges. Good for geometric, calligraphic, lacquerware style |
| **LoRA** | `Neo-Nihonga_Pop_Surrealism` at 0.7-0.8 | Strong painterly effect. 0.7 for subtle, 0.8 for full style transfer |
| **Negative** | `(anime girl:1.5), (face:1.3), character, person, photograph, 3d render` | Suppress anime bias |

### Sampler-Focus Analogy (from modular synthesis)
Different sampler/scheduler combos behave like different filter types or module topologies:
- **euler_ancestral + sgm_uniform** = stock filter, works for most things
- **dpmpp_2m + karras** = multimode filter with resonance — rich texture, more "character"
- **ddim + ddim_uniform** = bandpass — clean, precise, removes low-end mud
- **euler + normal** = lowpass — smooth, soft, dreamy

CFG acts like **focus** (in optics) or **CV modulation depth** (in synthesis):
- CFG 3-4: wide depth of field, creative interpretation, less literal
- CFG 5-5.5: sharp focus, good adherence without rigidity
- CFG 7+: narrow depth of field, can force unwanted elements (anime characters)

### I-Ching & Four Symbols Prompt Engineering

#### Representing Yin/Yang
| Archetype | Prompt keywords | Sampler preference |
|-----------|----------------|-------------------|
| **Yang (Figurative)** | celestial dragon, gold-leaf, rising sun, cinnabar, malachite | dpmpp_2m + karras |
| **Yang (Abstract)** | six yang lines, sacred calligraphy, geometric, gold on lacquer | ddim + ddim_uniform |
| **Yang (Landscape)** | volcano, molten gold, forge, eruption, dragon in smoke | dpmpp_2m + karras |
| **Yin (Water)** | dark water, ink-wash, scattered figures, moonlight, ripples | euler + normal |
| **Yin (Cavern)** | underground, still lake, stalactites, bioluminescence, stillness | euler + normal |
| **Yin (Ghostly)** | will-o-the-wisps, jellyfish, ghost mushrooms, scattered, diffuse | euler + normal |

#### Representing the Four Symbols (⚌⚍⚎⚏)
| Symbol | Essence | Visual Keywords | Color |
|--------|---------|----------------|-------|
| ⚌ **Elder Yang** | Peak yang, summer, noon, fire | radiating gold, sun at zenith, stationary fire, cinnabar, blinding light | Gold/Cinnabar |
| ⚍ **Younger Yin** | Descent toward yin, autumn, evening | amber softening to violet, afternoon shadows, gentle decline, horizon | Amber/Violet |
| ⚎ **Younger Yang** | Ascent toward yang, spring, dawn | silver-green, dawn breaking, awakening, spring from winter, first light | Silver/Green |
| ⚏ **Elder Yin** | Depth of yin, winter, midnight, water | deep indigo, void condensed, moonlight absorbed, absolute stillness | Indigo/Silver |

#### Key Insight: The 2-Line Grammar
The Four Symbols encode **directionality** — they are not static states but transitions:
- A single line (— or - -) describes a static position
- A trigram (3 lines) describes a complete state
- **The 2-line symbols** describe movement: whether energy is rising (⚎), falling (⚍), or at either extreme (⚌⚏)
- This makes them the natural grammar for seasonal/temporal cycles in wallpaper design

### Key Observations vs NoobAI-XL
- **Texture**: NoobAI = digital-crisp, high-gloss, neon glow. Illustrious = matte, mineral pigment (`iwa-enogu`), gold leaf (`kinpaku`), aged paper/silk
- **Color**: NoobAI = RGB light. Illustrious = crushed mineral pigments (cinnabar/shu red, malachite green, azurite blue)
- **Anime bias**: Both need strong anti-character negatives, but Illustrious is slightly less prone to inserting anime faces
- **Style transfer**: Neo-Nihonga LoRA at 0.8 strongly overrides base aesthetic — use 0.6-0.7 for subtler effect
- **Composition**: NoobAI tends toward scattered/diffuse; Illustrious+Neo-Nihonga tends toward centralized, symmetrical compositions

### ComfyUI Workflow Learnings

#### Template Architecture
- `zone_template_api.json` defines a reusable workflow with placeholder values (`__SEED__`, `__POSITIVE_PROMPT__`, etc.)
- `run_workflow.py` extracts a schema from the template, then injects `--args` parameters via schema lookup
- The schema auto-detects node inputs by scanning all nodes — any field with a unique value becomes a parameter
- **Critical**: Workflow node IDs (3=KSampler, 4=CheckpointLoader, 6/7=CLIPTextEncode, 8=VAEDecode, 10=SaveImage, 11=LoraLoader) must be stable across templates

#### Parameter Injection
- Sampler/scheduler/CFG/seed/steps all injected via KSampler inputs in `--args`
- Checkpoint via `ckpt_name`, LoRA via `lora_name` + `lora_strength` + `lora_strength_clip`
- The schema auto-discovers: `sampler_name`, `scheduler`, `steps`, `cfg`, `seed`, `ckpt_name`, `lora_name`, `lora_strength`, `lora_strength_clip`
- Unknown parameters generate warnings but don't fail — they're silently skipped
- **Warning**: `seed=-1` is auto-expanded to a random seed (logged as a warning, not an error)

#### Multi-Workflow Batches
- Chain workflows with `&&` for sequential generation (model stays loaded in VRAM)
- Use `--output-dir` to keep outputs organized in subdirectories
- `--timeout` prevents hanging on failed generations
- The `run_zone_batch.py` script wraps this with zone prompt lookup, seed sweeps, and auto-glyph

#### Reliability Notes
- **TQDM_DISABLE=1** required in ComfyUI server environment when subprocess-capturing stdout/stderr — prevents BrokenPipeError from tqdm progress bars
- **Connection refused**: Server may take 30-60s to load models into VRAM after restart — wait for "Starting server" log message
- **400 errors**: Usually from invalid parameter values (e.g., `"scheduler": "uniform"` instead of `"ddim_uniform"`)
- **VRAM management**: Model stays loaded between runs; changing checkpoints requires the new model to load (extra time)

### LoRA & Sampler Experiments: Leyendecker + Jiu Tian Xuan Nu

#### Leyendecker LoRA Findings
- **LoRA**: `illustrious/JC_Leyendecker-guy90-Illust-Lorav1.safetensors`
- **Sweet spot strength**: 0.8 — pushes the Art Nouveau/Deco aesthetic without losing coherence
- **At 0.6**: Mixed Eastern/Western face, softer painterly feel, some anime softness remains
- **At 0.8**: Anime influence almost entirely suppressed. Face reads as 1920s American commercial art ideal. Bolder lines, lithographic texture

#### Sampler + CFG Grid (dpmpp_2m + karras vs dpmpp_2m_sde_gpu + karras)
| Combo | CFG | Face Clarity | Texture | Best for |
|-------|-----|-------------|---------|----------|
| dpmpp_2m + karras | 4 | ❌ Smudged/indistinct | Soft, painterly | Concept sketches |
| dpmpp_2m + karras | 6 | ✅ Clear, sharp | Clean, balanced | Crisp lines, classic illustration |
| dpmpp_2m_sde_gpu + karras | 4 | ❌ Still smudged | Rich texture, painterly | Atmospheric vibe-over-detail |
| dpmpp_2m_sde_gpu + karras | 6 | ✅ **Best** | Impasto, thick brushstrokes, tactile | **Masterpiece feel — heavy pigments, Art Nouveau weight** |

- **CFG 6** is the sweet spot for the Leyendecker LoRA — enough guidance to lock in sharp, chiseled highlights without burning
- **dpmpp_2m_sde_gpu** adds tactile "painterly chaos" that complements Art Nouveau's tension between graphic lines and organic texture
- **CFG 4 loses face detail regardless of sampler** — the model needs CFG 5.5+ to resolve small features

## Related Skills
- `creative/comfyui` — Structured workflow execution
- `desktop/comfyui-zone-wallpapers` — Zone wallpaper specific skill (may be superseded by above)
- `creative/touchdesigner-mcp` — Real-time visual output channel
- `creative/p5js` — Alternative procedural generation
- `creative/manim-numogram` — Animated numogram diagrams

## Key Unresolved Challenges

### Multi-Figure Composition
Diffusion models (Illustrious/NoobAI) reliably render single-figure scenes but struggle with precise multi-figure compositions:
- `2boys` for warrior+sage produced 4 figures instead of 2
- `1girl, 1animal` for Chang'e+deer dropped the human figure entirely
- Best approach: generate figures individually and composite in post-processing, or use inpainting

### Character Bleeding
The model's Danbooru training causes specific game/anime characters to appear when prompts trigger associated tags:
- "summer forest + fireflies + warm light" --> Touhou characters
- "shrine maiden + red/white" --> Touhou characters
- Mitigation: specific negatives like `reimu, hakurei, genshin impact, touhou` for generic archetypes

### Anime Base Model Constraint
Both NoobAI and Illustrious are fundamentally anime-trained. Neo-Nihonga LoRA provides excellent East Asian painting style transfer, but the underlying model still produces anime-typical facial proportions at base. Higher LoRA strength (0.8+) and Leyendecker-style LoRAs can push toward Western illustration aesthetics instead.

## Future Directions

### Workflow Improvements
- **Hires fix / Refiner**: Second pass at higher resolution with lower denoising for detail enhancement
- **Detail Daemon**: ComfyUI Detail Daemon node for fine texture during upscaling
- **Adetailer**: Face-focused inpainting for character portraits (CFG 4 background + CFG 7 face)
- **Multi-LoRA chaining**: Stack multiple LoraLoaders (e.g., Neo-Nihonga + Tranquil)

### Unexplored LoRAs (14 of 18 Illustrious LoRAs untested)
- `MoriiMee_Gothic_Realistic` -- Gothic architecture aesthetic
- `Semi-realism_illustrious` -- Grounded illustration
- `HyperdetailedRealismMJ7` -- Maximum detail
- `ByeFrog_Style_IL` -- Unique style transfer
- `VoxMachinaV3ILXL` -- Stylized rendering
- `8.0-sprite pixel art` -- Retro gaming aesthetic

### Medium Expansion
- **64 Hexagrams**: Map 64 hexagrams to walls via digital root
- **Wu Xing**: Five Phase element walls (Wood, Fire, Earth, Metal, Water)
- **Seasonal progression**: Spring, Summer, Autumn, Winter landscape series
- **Chinese Zodiac**: 12 zodiac animals in Neo-Nihonga style

### Pipeline
- **Template library**: Dedicated workflow templates per subject type
- **Batch scheduling**: Prompt CSV input for cron-driven batch runs
- **Auto-glyphing**: Post-processing ImageMagick in workflow output
- **Animation**: AnimateDiff or Stable Video Diffusion wallpaper animation
- **IPAdapter**: Reference image style transfer from existing art
- **LLM prompt generator**: Chain LLM call to prompt to generation for automated ideation
