# Zone Pixel Glyphs — Visual Tier 0

> All 10 decimal numogram zones, 32×32 PICO-8 grid sprites.  
> Generator: `scripts/zone_glyphs_v2.py` · Assets: `docs/wiki/assets/zone-glyphs/`

## Conventions

| Zone | DECOM particle | Lead pigment | Visual motif                                      |
|------|----------------|--------------|---------------------------------------------------|
| 0    | eiaoung        | black/crimson| Concentric void diamond; ring-zero; silent center |
| 1    | gl             | amber        | Glottal gag reflex; inaugural/recoil doorframe    |
| 2    | dt             | red          | Imploded fricative; stutter fracture; angle tick  |
| 3    | zx             | green        | Buzz-cutter static; radial spokes                 |
| 4    | skr            | cream        | Reptiloid mass; growl anti-ziggurat with spines   |
| 5    | ktt            | gold/pink    | **Atlantean Hinge** — diamond constriction; two pink triangles pinching toward gold pressure thread; self-decadence golden ratio |
| 6    | tch            | navy         | Turbular erosion; static chew; zonal scratch      |
| 7    | bsigh          | cyan         | Lips-flap-ascent; trailing breath-wisp            |
| 8    | mn             | moon-white   | Moan-pleasure; three-fold petal bloom; spirit-diffraction |
| 9    | tn             | iron/copper  | **Iron Core / Plex** — pandemonium aperture; forty-five bloom; plutonium peak |

## In oracle.py (`--planchette`)

```
python3 oracle.py --seed 192855 --planchette
```

Prints a planchette box after every reading:

```
  ╔══════════════════════════════════════════════════════╗
  ║   ZONE 5 — Time-Circuit     [     ktt]                    ║
  ╠══════════════════════════════════════════════════════╣
  ║   Current:  1    Gate: Gt-6 =Z6     Syzygy: 5::4          ║
  ║   PNG: ~/numogram/docs/wiki/assets/zone-glyphs/zone-5.png  ║
  ╚══════════════════════════════════════════════════════╝
```

In base36/Djynxxogram mode the planchette is anchored to the **decimal attractor** (digital root of total AQ across the character traversal), not the last Djynxxogram character.

## Roadmap

| Tier | Visual                          | Status   |
|------|----------------------------------|----------|
| 0    | Terminal planchette box          | ✓ Live   |
| 1a   | 10 standalone PNG glyphs         | ✓ Saved  |
| 1b   | Inline terminal image            | TODO     |
| 2    | Syzygy chain SVG                 | TODO     |
| 3    | Djynxxogram 36-zone planchette   | TODO     |
| 4    | Realtime canvas (p5.js / TD)     | TODO     |
