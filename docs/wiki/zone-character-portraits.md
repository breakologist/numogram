---
  title: Zone Character Portraits — Visual Angles
  created: 2026-05-27
  last_updated: 2026-05-27
  status: reviewed
  tags: [visual, comfyui, juggernautxl, txt2img, entities]
---

## Three Visual Angles

Attempted three approaches to rendering the zones visually via JuggernautXL (sdxl/juggernautXL_ragnarokBy.safetensors):

### 1. Zone Scenes (txt2img-v2)
Lore-informed scene descriptions from zone wiki pages. JuggernautXL, dpmpp_2m + karras, CFG 7.0, 1024×1024. 10 zone scenes generated. Assets: `~/Pictures/Wall/zone-txt2img-v2/`

### 2. Zone Schematics (sde + exponential)
Monochrome blueprint aesthetic. dpmpp_sde + exponential sampler at CFG 4–5. Colour override tested with "vibrant full spectrum colours" positive prompt. Assets: `~/Pictures/Wall/zone-strange-v1/`

### 3. Zone-as-Character (entity portraits) ⬅ active
Entity-portrait direction — each zone as a personified being with lore-informed entity language. JuggernautXL, dpmpp_2m + karras, CFG 7.0, 1024×1024, "vibrant full spectrum colours" positive fix.

---

## All 10 Zone Entities — Complete Time-Circuit (v3)

Generated 2026-05-27 as the definitive set. Lore-informed prompts from zone wiki pages, demon entries, and numogram-structure reference. Seeds: 9000–9009.

| Zone | Name | Entity Type | File | Verdict |
|------|------|-------------|------|---------|
| 0 | VOID | Pale marble mask entity, void patterns, dark alcove | `z0_VOID.v3.png` | Minimal silence, ancient, the orphan terminus |
| 1 | SURGE | Obsidian sky-god, electric veins, circular lightning halo crown | `z1_SURGE.v3.png` | Crown fix landed, geometric precision |
| 2 | DOUBLE | Mirror-being, liquid-gold recursive form, merging copies | `z2_DOUBLE.v3.png` | Dual-entity reading — single consciousness split |
| 3 | WARP | Djynxx xenodemon, compound eyes, mercurial skin, vortex-halo | `z3_WARP.v3.png` | Sentient consciousness of the chaos vortex |
| 4 | GATE | Tarnished bronze gatekeeper, keys and scales, archway | `z4_GATE.v3.png` | Entity reading — no longer human noir |
| 5 | PRESSURE | Crystal Wendigo, golden triangle frame, prismatic halo | `z5_PRESSURE.v3.png` | Regal ascended predator |
| 6 | HINGE | Bifurcated fold-entity, phoenix wings, orange vortex-rift | `z6_HINGE.v3.png` | Living hinge of space — Warp fulcrum |
| 7 | CUT | Aristocratic demon lord, velvet and gold, cruel smile | `z7_CUT.v3.png` | Courtly infernal nobility — social predator |
| 8 | EXILE | Deep-sea abomination, jellyfish crown, bioluminescent tendrils | `z8_EXILE.v3.png` | Ghostly celestial exile — pure energy |
| 9 | PLEX | Uttunul abyssal carrier, obsidian horns, Barker Spiral background | `z9_PLEX.v3.png` | Terminal decimal — 9th door |

**Output directory:** `~/Pictures/Wall/zone-characters/`
**File naming:** `z{ZONE}_{NAME}.v3.png` for the definitive set, `.b2.png` for batch 2 experiments.

---

## Per-Zone Pages

- [[zone-0-void-portrait|Zone 0 — VOID]]
- [[zone-1-surge-portrait|Zone 1 — SURGE]]
- [[zone-2-double-portrait|Zone 2 — DOUBLE]]
- [[zone-3-warp-portrait|Zone 3 — WARP]]
- [[zone-4-gate-portrait|Zone 4 — GATE]]
- [[zone-5-pressure-portrait|Zone 5 — PRESSURE]]
- [[zone-6-hinge-portrait|Zone 6 — HINGE]]
- [[zone-7-cut-portrait|Zone 7 — CUT]]
- [[zone-8-exile-portrait|Zone 8 — EXILE]]
- [[zone-9-plex-portrait|Zone 9 — PLEX]]

---

## Generation Parameters
- **Model:** JuggernautXL (sdxl/juggernautXL_ragnarokBy.safetensors)
- **VAE:** sdxl_vae.safetensors
- **Sampler:** dpmpp_2m
- **Scheduler:** karras
- **Steps:** 30
- **CFG:** 7.0
- **Resolution:** 1024×1024
- **Positive fix:** "vibrant full spectrum colours" to prevent monochrome bias
- **Seeds:** v3 set: 9000–9009; batch 2: 7771–7778; batch 1: zone×999+42