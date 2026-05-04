---
tags: ["aq", "cipher", "code", "geometry", "numogram", "qliphoth", "tetractys", "visualization"]
zone: 3
syzygy: djynxx
source: "qliphoth.systems — Numogram interactive visualization, Gematria toolkit, Component library, GitHub: lumpenspace/ccru"
created: 2026-04-24
---


# QLIPHOTH Systems — Deep Dive

> https://qliphoth.systems / GitHub: lumpenspace/ccru
> Interactive numogram visualization, AQ gematria toolkit, React component library. Built with Next.js + TypeScript.
> "lemurian technological research"

## Three Sections

### 1. Numogram — Interactive Decimal Paths
Interactive SVG visualization of the complete numogram. URL: `qliphoth.systems/numogram`

**URL Parameters (shareable state):**
- `layout=labyrinth|ladder|original|planetary` — four distinct spatial arrangements
- `layers=syzygies,currents,gates,pandemonium` — toggle visual layers
- `particles=1` — quasiphonic particle display
- `tc=1` — Time Circuit highlighting
- `selected=0,3,6` — zone selection
- `date=2026-04-15` — planetary orbit positions (for planetary layout)
- `orbits=0` — hide orbital paths
- `img=url` — embed preview image in OG tags

**Controls:** Click+drag to select zones, alt+drag to pan, scroll to zoom, ASDF to change view, digits 0-9 to toggle gates.

### 2. Gematria — Anglossic Qabbala Toolkit
AQ cipher calculator + Chrome extension for in-page overlays. URL: `qliphoth.systems/gematria`

**Ciphers defined:**
| Cipher | ID | Range | Pattern |
|--------|----|-------|---------|
| Alphanumeric Qabbala | AQ | 0-35 | Base-36 ordinal: 0-9 then a-z as 10-35 |
| Synx | Synx | 0-35 | Accelerating CCRU progression (1,2,3,4,5,6,7,9,10,12,14,15,18,20,21,28...) |
| Numeric QWERTY | NQ | 0-35 | Keyboard order: 1234567890 + qwerty rows |
| QWERTY | QW | 1-26 | Alphabet reduced to keyboard layout (qwerty...m) |
| Alphanumeric Satanic | Satanic | 0-61 | Case-sensitive alphanumeric extension |
| ALPHANUM_PRIMES | — | 1-149 | First 36 primes mapped to alphanum |
| ALPHANUM_SYNX | — | 1-1260 | Accelerating CCRU progression |

**The `trigonal()` function** generates triangular number sequences: T(0)=0, T(1)=1, T(2)=3, T(3)=6, T(4)=10, T(5)=15, T(6)=21, T(7)=28, T(8)=36, T(9)=45. These ARE the gate cumulation values. The tetractys is baked into the cipher system.

### 3. Components — React/Tailwind UI Library
Installable via `npm install github:lumpenspace/ccru`. Exported as `ccru/components`.

Components: CyberButton, CyberPanel, CypherHoverText (hover-to-calculate gematria on any text), GlitchText, CyberButtonGroup, CyberPageHeader, and more.

---

## The Four Layouts

Each layout arranges the 10 zones differently, revealing different structural truths:

### Original — The Tetractys Triangle
```
        6 (Warp)
       3 (Warp)
      2
    7   5
   4     8
      1
      8
      9
      0 (Void)
```
Vertical triangle pointing down. The Warp (6,3) at apex, Time Circuit descending, Plex (9,0) at base. This is the **tetractys arrangement** — zones stack like Pythagorean dots. The triangular number structure is visible: 1 zone at top (Warp apex), then 1 (zone 3), then 1 (zone 2), then 2 (7,5), then 2 (4,8), then 1 (1), then 1 (8... wait, 8 appears twice). Actually 8 is positioned at two different Y coordinates — once in the Time Circuit (y=660) and once lower (y=660). This is a visual compression of the Time Circuit's anticlockwise rotor.

**Insight for code:** The original layout's Y-coordinates encode the numogram's vertical hierarchy: Warp (top) → Time Circuit (middle) → Plex (bottom). The horizontal offsets encode the syzygy pairings — zones that syzygyse are at similar X positions.

### Labyrinth — The Symmetric Spider
```
    6       3
       2
    5       7
    4       8
       1
    9       0
```
Symmetric around the vertical axis. Syzygy pairs (4::5, 3::6, 2::7, 1::8, 0::9) mirror each other horizontally. The Time Circuit forms a figure-eight pattern through the center. This is the clearest layout for seeing syzygy relationships.

**Insight for code:** The labyrinth layout makes the numogram's bilateral symmetry visible. Every syzygy pair is a left-right mirror. The currents (Surge 8→7, Hold 2→5, Sink 4→5, Warp 6→3, Plex 9→9) cross the center axis.

### Ladder — The Paired Rungs
```
    4     5
    3     6
    2     7
    1     8
    0     9
```
Five horizontal rungs. Each rung is a syzygy pair. Read top to bottom: Sink pair (4::5), Warp pair (3::6), Hold pair (2::7), Surge pair (1::8), Plex pair (0::9). This is the most numerologically clean layout — the pairs are literal rungs on a ladder.

**Insight for code:** The ladder layout is the simplest representation of the syzygy system. Five pairs, five currents, five demons. The anticlockwise rotor (1→8→2→7→5→4) zigzags across the rungs.

### Planetary — The Orbital Map
Zones positioned at radii matching planetary orbits (Mercury through Pluto), with the Sun at center. Angles default to a specific configuration but can be rotated by date parameter.

```
Radii: 0(Sol)=0, 1(Mercury)=55, 2(Venus)=95, 3(Earth)=130,
       4(Mars)=165, 5(Jupiter)=210, 6(Saturn)=255, 7(Uranus)=295,
       8(Neptune)=330, 9(Pluto)=360
```

**Insight for code:** The planetary layout connects the numogram to astronomical time. Rotating the layout by date parameter means the numogram's "shape" changes with the calendar — different days produce different visual configurations. This is the numogram as calendar/clock.

---

## Data Model — What They Defined

### Zones (zones.ts)
```typescript
ZONE_CLR: Record<number, string>     // Hex colors per zone
ZONE_REGION: Record<number, Region>  // 'torque' | 'warp' | 'plex'
ZONE_PARTICLE: Record<number, string> // Quasiphonic particles
PLANET_SYMBOL: Record<number, string> // Unicode planet glyphs
ZONE_META: Record<number, ZoneMeta>  // Full metadata per zone
```

**ZoneMeta includes:**
- `planet` / `planetFull` — planetary correspondence
- `desc` — zone description
- `spinal` — spinal level (Coccygeal, Lumbar, Solar, etc.)
- `meshTag` — binary mesh tag (0000, 0001, 0011, etc.)
- `door` — phase door designation
- `phaseCount` — number of phases
- `lemurs` — associated lemure entities
- `lemurian` — Lemurian lore text
- `centauri` — Centauri correspondence

### Syzygies (syzygies.ts)
Five pairs with demon names and descriptions. Each syzygy has: `{ a, b, demon, desc }`.

### Currents (currents.ts)
Five currents with flow direction: `{ name, from, to, label, desc }`.
- Surge: 8→7 (8−1=7)
- Hold: 2→5 (7−2=5)
- Sink: 4→1 (5−4=1)
- Warp: 6→3 (6−3=3) — self-fold
- Plex: 9→9 (9−0=9) — self-fold

### Gates (gates.ts)
Nine gates with cumulation: `{ name, from, to, cum, desc, detail }`.
- Gt-00 (0→0, cum=0): "Between its existence and nonexistence there is no difference"
- Gt-01 (1→1, cum=1): "Zone-1 turning forever into itself"
- Gt-03 (2→3, cum=3): "Lo-Way to the Crypt"
- Gt-06 (3→6, cum=6): "Gate to the Swirl"
- Gt-10 (4→1, cum=10): "Gate of Submergence"
- Gt-15 (5→6, cum=15): "Fifth Gate — abduction into the Warp"
- Gt-21 (6→3, cum=21): "Sixth Gate — vortex reversal"
- Gt-28 (7→1, cum=28): "Seventh Gate"
- Gt-36 (8→9, cum=36): "Gt-36. 666. Woah, here we go."
- Gt-45 (9→9, cum=45): "The Gate of Pandemonium"

### Demons (demons.ts)
**The classification algorithm — clean and extractable:**
```typescript
const TC = new Set([1, 2, 4, 5, 7, 8])  // Time Circuit zones

for (let i = 1; i < 10; i++)
  for (let j = 0; j < i; j++) {
    const key = `${i}:${j}`
    const isSyz = i + j === 9
    const kind = isSyz ? 'syzygy'
      : (TC.has(i) && TC.has(j)) ? 'chrono'
      : (!TC.has(i) && !TC.has(j)) ? 'xeno' : 'amphi'
    ALL_DEMONS.push({ a: i, b: j, name: DEMON_NAMES[key] || '?', kind })
  }
```

This produces:
- 5 syzygetic demons (i+j=9)
- 15 chronodemons (both in Time Circuit) = C(6,2)
- 24 amphidemons (one in TC, one outside) = 6×4
- 6 xenodemons (neither in TC) = C(4,2)
- **Total: 50** (includes the 5 syzygetic carriers alongside the 45 C(10,2) demons)

---

## Geometry Library (lib/geometry.ts)

Five key functions for rendering the numogram as SVG paths:

### `quadPath(from, to, bulge)` — Curved Connection
Quadratic bezier path between two points with a bulge factor. If bulge < 0.5, returns a straight line. Otherwise, computes a perpendicular offset from the midpoint to create a curve. Used for all current and gate paths.

**Extractable:** This is a general-purpose "draw a curve between two points" function. Can be used for any graph visualization.

### `loopPath(pos, dir)` — Self-Loop
Circular loop for self-referential connections (Gt-00, Gt-01, Gt-45, Warp current, Plex current). Creates an SVG arc that returns to the same point. `dir='below'` or `dir='above'` controls which side the loop appears.

### `curveAway(from, to, cx, cy, factor)` — Avoid-Center Path
Path that curves away from a control point (usually the center of the numogram). Computes the perpendicular direction and sign to push the curve away from the center. This prevents paths from crossing through the numogram's interior.

**Extractable:** Key insight — when rendering a graph on a surface, paths should curve AWAY from the center to avoid visual congestion. The sign calculation (`dot > 0 ? -1 : 1`) determines which direction to push.

### `syzTrianglePoints(zone, pos)` — Syzygy Direction Markers
Small triangle markers that point from one zone toward its syzygy partner. Creates a triangle tip at distance 8 from the zone, pointing toward partner, with base size 5.

### `syzMidBiased(zone, pos)` — Biased Midpoint
Midpoint between a zone and its syzygy partner, biased 15% toward the first zone. Used for label placement.

---

## Extractable Ideas

### For the Abyssal Crawler / Roguelike

**1. The Four Layouts as Four Dungeon Architectures**
- Original = vertical dungeon (descending levels, Warp at top, Plex at bottom)
- Labyrinth = symmetric dungeon (mirror-image wings)
- Ladder = paired rooms (each floor has two connected rooms)
- Planetary = orbital dungeon (rooms at varying distances from center)

**2. The Demon Classification Algorithm**
The `for i=1..9, for j=0..i-1` loop with the four-way classification is clean, elegant, and directly implementable. The TC set determines which zone pairs are "internal" vs "external." This could drive procedural demon generation.

**3. The Layer Toggle System**
The URL-parameter-driven layer system (`layers=currents,gates,pandemonium`) is a general pattern for any visualization with optional overlays. Could be applied to the roguelike's map display: toggle visibility of zones, gates, demons, fog of war.

**4. The `quadPath` Geometry**
Curved SVG paths between graph nodes with bulge control. Could render the numogram dungeon map in the roguelike's UI — curved corridors instead of straight ones.

**5. The `curveAway` Anti-Congestion Pattern**
Paths that curve away from the center to avoid visual overlap. In the roguelike, this could inform corridor routing — corridors that bend away from the center of a room cluster to avoid congestion.

**6. Zone Colors as Game Palette**
The defined zone colors form a complete palette:
```
0: #aaaaaa (void grey)
1: #ee44ee (mercury magenta)
2: #4488ff (venus blue)
3: #44cc77 (earth green)
4: #ee4444 (mars red)
5: #ee8833 (jupiter orange)
6: #ddcc33 (saturn yellow)
7: #7755cc (uranus purple)
8: #9944ee (neptune violet)
9: #666666 (pluto dark grey)
```

**7. The Cyberpunk Aesthetic System**
The CSS variable system (`--cp-cyan-laser`, `--cp-acid-lime`, etc.) with Display P3 color space support. The component library (CyberButton, CyberPanel, GlitchText) provides a reusable UI system for numogram-themed interfaces.

### For Visualization / P5.js / Manim

**8. The Planetary Layout as Animated Orbit**
The planetary positions change with the `date` parameter. An animation that rotates through dates would show the numogram's zones orbiting — the numogram as clock.

**9. The Trigonal/Tetractys Structure**
The triangular number sequence (T(0)=0 through T(9)=45) embedded in the gate cumulation values. A tetractys visualization — 1 dot, then 2, then 3, then 4 — mapped to numogram zones would show the Pythagorean foundation of the system.

**10. The Quasiphonic Particle System**
Zone particles defined as phoneme fragments (eiaoung, gl, dt, zx, skr, ktt, tch, pb, mnm, tn). These could drive a sound visualization — each zone has a sonic signature that plays when entered.

---

## Links

- [[numogram]] — Main numogram overview
- [[alphanumeric-qabbala]] — AQ cipher system
- [[quasiphonic-particles]] — Sound system per zone
- [[gates-and-plexing]] — Gate construction and cumulation
- `numogram-llm-wiki` — Wiki index
- https://qliphoth.systems — Live site
- https://github.com/lumpenspace/ccru — Source code

---

## Updates (2026-05-04 — Import Analysis)

Following systematic investigation of the upstream repository (`lumpenspace/ccru`) and comparison with our calculator/oracle stack:

- **Cipher inventory** confirmed: **10** canonical ciphers (not 14). See [[ccru-ciphers]] for full catalog and value arrays.
- **Zone metadata** imported from `zones.ts`; individual zone pages created: [[zone-0]] through [[zone-9]].
- **Demon classification algorithm** documented; verify against [[pandemonium-matrix-45-demons]] via `classify_demon(i, j)`. See [[demon-classification-algorithm]].
- **Position data** for four layouts embedded in zone pages; also summarized in [[zone]].
- **Geometry library** functions ported to `numogram-visualization` pipeline (quadPath, loopPath, curveAway, syzTrianglePoints, syzMidBiased).
- **Gematria module** (`numogram-gematria` skill) implements all 10 ciphers with normalization rules identical to upstream `gematria.ts`.

**Action items raised:**
- [ ] Extend `numogram-calculator` to expose full zone metadata via `get_zone_meta(zone)` API
- [ ] Add multi‑cipher resonance mode to `numogram-oracle` (configurable cipher list)
- [ ] Consider adding demon‑classification function to `numogram-calculator` or a dedicated `pandemonium-engine` skill
- [ ] Reconcile any discrepancies between our `pandemonium-matrix-45-demons.json` and canonical `ALL_DEMONS` order/kind

**Related:**
- [[qliphoth-ccru-import-analysis]] — full gap analysis & integration roadmap
- [[numogram-gematria]] — multi‑cipher reimplementation
- [[demon-classification-algorithm]] — TC‑based kind assignment

