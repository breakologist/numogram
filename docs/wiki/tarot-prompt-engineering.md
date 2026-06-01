---
title: Tarot Prompt Engineering
tags:
  - tarot
  - stable-diffusion
  - prompt-engineering
  - lora
  - zone-archetypes
  - oracle-visuals
created: 2026-06-01
status: reference-seed
---

# Tarot Prompt Engineering

**Source:** `raw/SD/Lora.md` — Major Arcana prompt fragments collected for a tarotv0.2 aesthetic.

This page is a **lookup / reference seed** — not yet integrated into any live workflow. It anchors the 22 Major Arcana as prompt-building blocks (archetype + props + setting) and provides the bridge between:

- [[oracle-visual-ideas]] — zone particle/colour/concept archetypes
- [[visual-wallpaper-pipeline-status]] — NoobAI/Illustrious settings, sampler/FG logic, negative prompts

The long-term possibility is a **zone↔arcana crosswalk**: each zone mapped to one or more arcana, then rendered with the shared prompt grammar below.

---

## 22 Major Arcana — Prompt Recipes

| Arcana | Archetype keywords | Key props / setting |
|--------|-------------------|---------------------|
| 0 — The Fool | `the fool`, `man`, `bindle`, `stick and bag`, `cliff`, `dog` | Edge of a cliff, small dog, journey beginning |
| I — The Magician | `the magician`, `man`, `robes`, `candle` / `holding candle`, `table with items`, `star`, `pentacle`, `cup`, `sword`, `wand` | Table of tools, raised wand, infinity symbol overhead |
| II — The High Priestess | `the high priestess`, `woman`, `robes`, `headpiece`, `throne`, `columns` | Veiled figure, pillars (Boaz/Jachin), scroll |
| III — The Empress | `the empress`, `woman`, `pillow throne`, `crown`, `scepter` | Lush vegetation, pregnant imagery, stars on crown |
| IV — The Emperor | `the emperor`, `man`, `beard`, `stone throne`, `crown`, `scepter` | Ram-headed throne, armor, stern gaze |
| V — The Hierophant | `the hierophant`, `man`, `religious robes`, `triple crown`, `scepter`, `throne`, `columns` | Two crossed keys, blessing gesture, monastery |
| VI — The Lovers | `the lovers`, `angel`, `naked man`, `naked woman`, `garden` / `garden of eden` | Serpent, tree of knowledge, radiant light |
| VII — The Chariot | `the chariot`, `person`, `chariot` / `riding chariot`, `pulled by sphinxes` | Black/white steeds, laurel wreath, armor |
| VIII — Strength | `strength`, `woman`, `dress`, `lion`, `outdoors` | Woman closing lion’s mouth, infinity halo, petals |
| IX — The Hermit | `the hermit`, `old man`, `beard`, `grey robes`, `staff`, `lantern` | Snow peak, single lantern, solitary path |
| X — Wheel of Fortune | `wheel of fortune`, `spoked wheel`, `symbols`, `winged animals`, `lion`, `ox`, `eagle`, `angels` | Tetragrammaton, ascending/descending figures |
| XI — Justice | `justice`, `person`, `scales of justice` / `scales`, `crown`, `robe`, `sword`, `throne` | Sword raised, scales balanced, pillars |
| XII — The Hanged Man | `the hanged man`, `man`, `upside down`, `hanging from tree` / `hanging by ankle` | Tree, halo, voluntary suspension, tau cross |
| XIII — Death | `death`, `skeleton knight`, `black armor`, `white horse`, `flag`, `war` | Rising sun through clouds, white rose, fallen king |
| XIV — Temperance | `temperance`, `angel`, `wings`, `holding cups`, `pond of water` | One foot on water, one on land, path, iris flower |
| XV — The Devil | `the devil`, `demon`, `goat head`, `wings`, `[chained/naked/goat/man/woman]` | Inverted pentagram, chains, flickering torch |
| XVI — The Tower | `the tower`, `burning tower`, `fire`, `thunderstorm`, `jumping people`, `falling` | Crown falling, lightning, one falling figure safe below |
| XVII — The Star | `the star`, `stars` / `many stars` / `big star`, `naked woman`, `holding jars`, `kneeling`, `water` | Nude female pouring water onto land and pool |
| XVIII — The Moon | `the moon`, `large moon` / `large moon in sky`, `animals`, `wolf`, `dog`, `crayfish` | Dog/wolf duality, crayfish rising from pool, path of thorns |
| XIX — The Sun | `the sun`, `large sun with face`, `child`, `riding horse`, `flag` | Naked child on white horse, sunflowers, bright wall |
| XX — Judgement | `judgement`, `angel` / `angel flying from above`, `trumpet` / `playing trumpet`, `crowd down below` / `people below` | Resurrected figures rising from coffins, trumpet call |
| XXI — The World | `the world`, `naked woman`, `flying`, `wearing cloth`, `holding staffs`, `lion`, `ox`, `eagle`, `man` | Dancing figure, laurel wreath, four fixed corners |

---

## Prompt Grammar Notes

- **Archetype first.** The arcana keyword list is designed to tokenise cleanly in Danbooru- / tag-trained checkpoints (NoobAI, Illustrious). Lead with the archetype; add props as tags in parentheses if emphasis is needed.
- **Setting / mood second.** Zone concepts from [[oracle-visual-ideas]] (e.g. “salt marshes,” “amber door,” “iron core,” “moonlight white”) slot directly after the arcana tags.
- **Sampler / CFG routing.** Use the same rules as [[visual-wallpaper-pipeline-status]]: dpmpp_2m + karras for figural intensity; euler + normal for water/night/dream scenes; ddim for geometric/calligraphic compositions. CFG 5–6 is the safe sweet spot.
- **Negative prompt baseline.** `(anime girl:1.5), (face:1.3), character, person, man, woman, boy, girl, photograph, 3d render` — because the base models inject anime faces even when none were requested.

---

## Zone ↔ Arcana Crosswalk (provisional)

*First guess at correspondences — not canonical, meant to be iterated.*

| Zone | Particle / concept | Candidate arcana |
|------|-------------------|------------------|
| 0 | eiaoung — void/reservoir | 0 — The Fool (void potential) |
| 1 | gl — inhalation/gate | IX — The Hermit (first inhale) |
| 2 | dt — stutter/fracture | XII — The Hanged Man (inversion) |
| 3 | zx — static/buzz | X — Wheel of Fortune (vortex) |
| 4 | skr — catastrophe/mass | XVI — The Tower (collapse) |
| 5 | ktt — Atlantean hinge | VII — The Chariot (threshold) |
| 6 | tch — turbulence/occlusion | VIII — Strength (feral containment) |
| 7 | bsigh — breath/ascent | XVII — The Star (water-stars) |
| 8 | mnm — multiplicity/bloom | VI — The Lovers (blossoming pair) |
| 9 | tn — iron/peak | XIII — Death (peak/terminus) |

**Note:** The crosswalk is deliberately multiple — several zones could plausibly claim The Moon (XVIII), The World (XXI), or Justice (XI). The table is a starting position for debate, not a closed syzygy.

---

## Future Expansion

- [ ] Render all 22 arcana using the pipeline in [[visual-wallpaper-pipeline-status]] and compare zone-crosswalk hypotheses.
- [ ] Add Major Arcana to [[oracle-visual-ideas]] as a parallel taxonomy to the 10-zone particle table.
- [ ] Test whether the same prompt grammar works for the 56 Minor Arcana (Wands/Cups/Swords/Pentacles) and where it breaks.
- [ ] Consider a **tarot-as-gate** reading: draw an arcana, map it to a zone via digital root, then to its syzygy pair.
