# Zone txt2img — Next Directions (2026-05-26)

## Three Angles Explored, Three More to Try

### Completed

1. **Zone-as-scene** — Standard dpmpp_2m + karras CFG 7. Full 10-zone set at `~/Pictures/Wall/zone-txt2img-v2/`. Zones as photorealistic landscapes, spaces, architectural forms.

2. **Occult schematics** — sde + exponential CFG 4-5. Monochrome blueprints, celestial diagrams, grimoire pages. See `~/Pictures/Wall/zone-strange-v1/`.

3. **Pos-fix colour sde** — sde + exponential + "vibrant full spectrum colours" in positive prompt. Best colour+texture combo. See `~/Pictures/Wall/zone-strange-v2/z3_posfix.png`.

4. **Zone-as-character** ✅ Complete — All 10 zones personified as entities via JuggernautXL. Lore-informed prompts per zone, refined over 3 batches. Full wiki documentation: [[zone-character-portraits]] and 10 per-zone entity pages ([[zone-0-void-portrait]] etc.). Output: `~/Pictures/Wall/zone-characters/`. v3 seeds 9000-9009 definitive.

### Next

#### A. Zone-as-character
Personify each zone as a living entity, blending zone lore with anatomical/biological language. Uses pos-fix colour approach. The model proved it can produce convincing entities (Zone 7's toad-demon). Prompts should pull from zone page descriptions, particle names, and Centauri Correspondence.

Best candidates:
- Zone 1 — "sky-god archaic gnosis" → mercurial electric entity
- Zone 2 — "ghosts in the doubling" → spectral mirror-being
- Zone 5 — "Hyperborean Wendigo" → pressure entity, alien abductor
- Zone 7 — already worked as creature, refine
- Zone 8 — "Lukh/Shuplu spirit-diffraction" → deep sea entity

#### B. Syzygy composites
One image per syzygy pair showing both zones at a shared boundary. Structural numogram lore made visual. 5 pairs: 4::5, 3::6, 2::7, 1::8, 0::9. Most expressive pairs:
- 4::5 (Land's "end of the cycle" — gate and current perfectly reinforce)
- 3::6 (Warp vortex — "self-folding, no rest state")
- 0::9 (Plex abyss — void touching iron core)
- some  in /Wall from Grok: ![[09voidplexhorizon.jpg]]
- ![[18surgehold.jpg]]
- ![[27holdrise.jpg]]
- ![[36warpvortex.jpg]]
- ![[45sinkhinge.jpg]]
- 
#### C. Alchemical manuscript
Aged parchment backgrounds, ink diagrams, wax seals, sigils. Combine monochrome schematic precision with texture. "Found grimoire" aesthetic. Could use the yantra SVGs composited as inked diagrams.

## Settings Reference

| Mode | Sampler | Scheduler | CFG | Prompt note |
|------|---------|-----------|-----|-------------|
| Standard scenes | dpmpp_2m | karras | 7.0 | Natural language, materials, lighting |
| Occult schematics | dpmpp_sde | exponential | 5.0 | Accept monochrome |
| Colour sde | dpmpp_sde | exponential | 5.0 | Add "vibrant full spectrum colours" to positive |
| Entity/character | dpmpp_2m | karras | 7.0 | Biological/anatomical language, "portrait of"