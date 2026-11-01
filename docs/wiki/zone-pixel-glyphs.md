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

> **Verification note (Em, 1 Nov 2026):** "5::5", "5⊕5" and "self-decadence" are wiki coinages, not CCRU terms. ccru.net does not use "self-decadence". Per the sources, 5+5 is just one of the Decadence 10-sum pairs; it scores 0 ("from 5:5 = 0") [ccru.net, [Matrix](http://www.ccru.net/digithype/pandemonium.htm)]. It is **not** a demon or net-span (there is no 5::5 in the Matrix) and **not** the Barker spiral's centre. 5's 9-sum twin is 4, and the repo puts **4::5 (Katak) innermost** on the Barker spiral [repo, `syzygies.ts`]. See [[barker-spiral]]. (Commentary page: text left as written.)
