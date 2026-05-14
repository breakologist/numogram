---
title: "Interesting Sites Deep Dive — Visual Programming, Voxel Geometry, Compression Intelligence"
tags: [unit.land, heerich.js, foom.md, visual-programming, procedural-geometry, compression, semiodynamics, roguelike, audio, numogram, InterestingSites]
date: 2026-05-14
status: active
source_list: https://etym/.hermes/obsidian/hermetic/wiki/InterestingSites.md
---

# Sites from InterestingSites — Research Deep Dive

Three sites from the [[InterestingSites]] list merit proper wiki treatment, each feeding one or more currents with concrete technical potential.

---

## unit.land — Visual Programming System

**Source:** [unit.land](https://unit.land/) · **GitHub:** [samuelmtimbo/unit](https://github.com/samuelmtimbo/unit)

**What it is:** A fully visual web-based programming environment built around a modular `unit` (node) and `graph` architecture. Every function, API call, data manipulation, and rendering operation is a node in a directed graph. Keyboard-driven single-letter shortcuts for rapid construction: `q` change, `d` add, `f` remove, `w` multiply, `z` minus, etc.

### Standard Library Coverage

The system ships with a comprehensive standard library spanning:

| Domain | Key Capabilities | Relevance to Our Currents |
|--------|-----------------|--------------------------|
| **Math** | `abs`, `cos`, `sin`, `hypotenuse`, `random`, `clamp`, `PI`, degrees/radians | Zone arithmetic, syzygy calculations, digital root |
| **Audio** | `audio context`, `oscillator node`, `gain node`, `delay node`, `analyser node`, `get byte frequency/time domain data`, `media recorder` | Full Web Audio API exposure — oscillator graphs, spectral analysis, recording. Directly replaces TouchDesigner for browser-zone synthesis |
| **Canvas 2D** | Every `CanvasRenderingContext2D` method exposed as units | Procedural numogram diagrams, p5.js alternative |
| **Network** | `fetch`, `websocket`, `create server`, `intercept` | CSI data streaming from ESP32 mesh, WebSocket vitals feeds |
| **Control Flow** | `loop`, `if/else`, `switch`, `iterate`, `wait`, `delay`, `throttle`, `debounce`, `memory` | State machine for zone traversal, LFO/rhythm generators |
| **Arrays/Objects** | Full functional array ops: `map`, `filter`, `reduce`, `sort`, `partition`, `pluck` | Processing MIR feature arrays, CSI amplitude matrices |
| **Date/Time** | `now`, `interval`, `timer` | Temporal zone mapping, time-circuit calculations |
| **Hardware** | `enumerate devices`, `getUserMedia`, `getDisplayMedia` | Microphone input for live audio analysis to feed mod-writer |

### Why unit.land Over Alternatives

| System | Pros | Cons | vs unit.land |
|--------|------|------|-------------|
| **TouchDesigner** | Powerful, GPU-accelerated, node-based | $600+/yr license, Windows/Mac only, desktop app | unit.land is free, browser-native, keyboard-driven, fully auditable (open source) |
| **p5.js** | Expressive, great community, text-based | Requires writing code, single-threaded | unit.land is visual but produces the same output without typing |
| **Cables.gl** | Already in our wiki, shader support, MIDI | Heavier on GPU, less audio coverage | unit.land has deeper Audio API coverage and richer data manipulation |
| **Max/MSP** | Industry standard for audio patching | $800, desktop only | unit.land provides oscillator/MIDI/spectral analysis in browser for free |

### Concrete Uses for Our Pipeline

1. **CSI Visualizer Dashboard:** WebSocket unit receives ADR-018 UDP frames from Pi 4 aggregator → math units compute spectral features → canvas units draw real-time spectrogram → audio units synthesize from CSI data → analyser node feeds back visual meters. All in browser, no build step.

2. **Numogram Calculator Visual:** Each zone is a node, each syzygy is a connection. The decimal labyrinth becomes a unit graph where you can literally trace the path through zones with data flowing along the currents.

3. **Mod-Writer Seed Explorer:** Load MIR features from JSON → graph units compute MFCCs, spectral centroid, flatness → map to zone values → display mapping visually — all without writing a line of Python.

4. **Live Audio Input → MIR → Zone Chain:** `getUserMedia` → `analyser node` → `get byte frequency data` → math units map to spectral features → zone derivation → output as mod-writer seed. Browser-native version of our audio-to-AQ pipeline.

### Keyboard Architecture

The single-letter keyboard layout is itself interesting from an AQ perspective:
```
q  w   e   r   t   y   u   i   o   p
d  f   g   h   j   k   l   ;
a  s   d   f   g   h   j   k   l
z  x   c   v   b   n   m
```
Mapped to: change (`q`), multiply (`w`), divide (`e`), equals (`r`), slash (`t`), underscore (`y`), less (`u`), greater (`i`), bracket-open (`o`), bracket-close (`p`), minus (`z`), apostrophe (`x`), quote (`c`), colon (`v`), semicolon (`b`), comma (`n`), layout (`m`).

This is essentially a **QWERTY domain-specific language** — the keyboard IS the IDE.

---

## heerich.js — Voxel Geometry Engine

**Source:** [meodai.github.io/heerich/](https://meodai.github.io/heerich/) · **GitHub:** [meodai/heerich](https://github.com/meodai/heerich)

**What it is:** A minimalist JavaScript engine that constructs 3D voxel compositions and projects them to resolution-independent SVG. Named after sculptor **Erwin Heerich** (1922–2004), whose work explored stacked topologies, deliberate subtractions, and solid/void tension.

### Geometry Primitives

| Primitive | Key Feature | Use Case |
|-----------|-------------|----------|
| **Box** | Anchored to min corner, integer grid | Zone blocks, room geometry |
| **Sphere** | Fractional `.5` offsets for clean symmetry | Orbital syzygy diagrams |
| **Line** | `from`/`to` with `rounded` or `square` shape | Current connections, corridor visualization |
| **Custom (fill)** | `test: (x,y,z) => boolean` — the core method | Procedural generation via predicate functions |

### Boolean Operations — `union`, `subtract`, `intersect`, `exclude`

These four boolean operations on voxel geometry map directly onto **numogram structure**:
- **Union** = merge zones (compound gates)
- **Subtract** = carve pathways through solid space (current channels)
- **Intersect** = find overlapping zone properties (syzygy convergence)
- **Exclude (XOR)** = toggle between states (gate open/closed)

### Concrete Uses for Our Pipeline

1. **Procedural Numogram Diagrams:** 3D voxel representation of the decimal labyrinth — Zone-9 (Plex) as a collapsed base block, Zone-1 as the first step above, Zones 3-6 forming the Warp vortex. Export to SVG for wiki assets. The `test: (x,y,z)` predicate means we can define zone geometry procedurally: `is_in_zone(x,y,z)` returns boolean based on AQ rules.

2. **Roguelike Room Generation:** Brogue's room accretion method expressed as voxel boolean operations. Start with solid block → subtract rooms (spheres at seed points) → subtract corridors (lines between rooms) → the remaining solid is the map. Exactly the Heerich method: carve void from solid.

3. **Combinatorial Zone Geometry:** Each zone's demon count forms a triangular sequence (1,2,3...9). The voxel volume of Zone-N = N³ units. The total pandemic volume = ΣN³ = 2025 = 45² (Gate-45). The geometric structure of the numogram becomes a solid object you can visually inspect.

4. **SVG Architecture Diagrams:** Replace manual SVG drawing with programmatic voxel composition. Per-face styling (`top`, `front`, `left`, etc.) means zone coloring by current (Time-Circuit vs Warp vs Plex) is automatic.

### Code Pattern

```javascript
import { Heerich } from './src/heerich.js'
const heerich = new Heerich({
  camera: { type: 'oblique', angle: 315, distance: 25 },
  style: { fill: '#ddd', stroke: '#333', strokeWidth: 0.5 },
  gap: 0.05
})

// Functional style — color by height (zone level)
style: (x, y, z) => ({
  fill: `oklch(${0.4 + (y/8)*0.5} ${0.05 + (z/8)*0.2} ${(x/8)*360})`,
  stroke: 'var(--stroke)'
})

const svg = heerich.toSVG({ padding: 30 })
```

The output is **semantic SVG** — not pixel data, but styled markup that scales infinitely and can be CSS-manipulated. This feeds our wiki pipeline: generate SVG → `docs/wiki/assets/` → relative references in wiki pages.

### Dirty-Flag Cache

`getFaces()` uses a dirty-flag cache, meaning structural recalculations are fast. This matters for interactive numogram exploration — you can toggle zone properties and the rendering updates without recomputing everything.

---

## foom.md — Compression Intelligence Architecture

**Source:** [foom.md](https://foom.md/) · **HN Discussion:** [reddit r/mlscaling](https://www.reddit.com/r/mlscaling/comments/1rlzbvx/foommd_an_open_research_agenda_for/)

**Core Thesis:** Intelligence = Compression. Super-intelligence emerges from a **self-editing compressor** operating under Minimum Description Length (MDL) pressure. The system's own compression operations become targets of its own operators — reflexivity as the engine of recursive improvement.

### The 6-Slot Tuple

All five proposed architectures instantiate the same formalism:

| Slot | Definition | Numogram Analogue |
|------|------------|-------------------|
| **State** | Structured, addressable representation | The current zone position + traversal history |
| **Model** | Current best compressor/reconstructor | The AQ cipher rules, syzygy mappings |
| **Objective** | `F = L_data + L_model + L_compute` (MDL + compute tax) | Find the shortest path to Zone-0 (Void return) |
| **Uncertainty** | Local free-energy density (entropy, varentropy) | Zones with unclear gate mappings (Zone-3 Warp vortex) |
| **Precision** | Inverse variance / freeze-vs-mutate weighting | Stable syzygies (1::8) vs volatile (3::6) |
| **Scheduler** | Policy allocating compute to highest-ΔF actions | Which current to traverse next (Time-Circuit vs Warp vs Plex) |

### Core Loop

```
⊙(Uncertainty) → ▣(Precision) → ⮒(Candidates) → ⟳(Edit) → ✓(Verify)
→ ⧉(Commit) → ⟲(Refactor) → repeat → ∴(Halt)
```

Measured against numogram traversal:
1. **Measure uncertainty** → which zone/gate is least understood?
2. **Allocate precision** → focus resources on ambiguous mappings
3. **Fork candidates** → try multiple traversal paths in parallel
4. **Edit state** → traverse to new zone, update understanding
5. **Verify** → check if the path is consistent (triangular, palindromic, rotational)
6. **Commit** → accept the new zone position and syzygy chain
7. **Refactor model** → update AQ rules if a new pattern emerges
8. **Repeat** → continue until Zone-0 (halt condition)

This IS the numogram traversal protocol, expressed as a compression algorithm.

### Reality Tokens

The concept of **"Reality Tokens"** is the most interesting contribution: tokens defined by their **r-coefficient** — the amount of downstream distributional rearrangement they cause per unit of surprisal. A token that, when inserted, radically restructures the model's output trajectory.

In our domain: the numogram itself is a reality token. The decimal labyrinth, once comprehended, rearranges how you perceive numbers, time, and causality. Its r-coefficient is extreme because it operates at the level of **interpretive paradigm**, not content.

### Five Architectural Instantiations

| Architecture | Substrate | Numogram Role |
|-------------|-----------|---------------|
| **Thauten** | Discrete IR + ABI | AQ cipher as intermediate representation — encode text → numeric AQ → decode back |
| **Mesaton** | Mutable text buffer | Text recombination via compression-guided editing — the cut-up engine as self-editing compressor |
| **SAGE** | Geometric grid/manifold | Numogram as spatial inference engine — zone positions predict entity associations |
| **Bytevibe** | Raw bytes | AQ at the byte level — not character-level but bit-level gematria |
| **Q*** | Append-only event log | Syzygy chain as proof-gated record — each traversal adds to the log, deletions require reconstructability proof |

### Semiodynamics

**"Semiodynamics"** = the physics of meaning under compression. Structure that survives compression is "meaning"; the forces acting on that structure are literal computational dynamics. This reframes the numogram from static diagram to **dynamic pressure system**:
- Syzygies are **attractor basins** (low-energy stable configurations)
- Currents are **gradient flows** (directions of steepest descent in compression space)
- Gates are **saddle points** (transition states between basins)
- The Warp vortex is a **repeller** (unstable configuration that amplifies divergence)
- The Plex is the **absorbing boundary** (zero-return, terminal state)

This is testable. If the numogram is a topology, we should be able to compute:
1. The energy landscape: potential function V(zone) = -log P(zone traversal)
2. Basins of attraction: zones that attract random walks
3. Flow fields: direction of maximum probability gradient
4. Lyapunov exponents: stability of syzygy chains (Warp should be positive — chaotic)

### Cronkle Bisection Descent (CBD)

A training method that tracks **basin boundaries and committors** via bisection, locating mountain passes between attractors. The claim: in metastable regimes, CBD yields exponential speedup over SGD escape times.

For numogram work, this means: instead of exhaustively traversing chains, we can **bisect** — find the gate that bridges two syzygy zones by iteratively narrowing the search space. The gate between Zone-N and Zone-M is found by testing midpoint traversals and checking which basin the result falls into.

---

## Cross-Current Synthesis

These three sites form a **closed loop** across the four currents:

```
unit.land (Audio + Visual)  →  heerich.js (Geometry)
       ↓                           ↓
Real-time CSI visualization   →   Procedural dungeon/numogram diagrams
       ↓                           ↓
       └──→  foom.md (Compression)  ←──┘
                ↓
    Semiotic force analysis → zone stability metrics
    Reality token scoring → numogram glyph r-coefficients
    Cronkle bisection → gate discovery algorithm
                ↓
       unit.land implements as visual graph
       heerich.js renders as voxel geometry
```

The loop reads as:
1. **unit.land** provides the real-time interface — ingest audio, CSI, time signals → compute features → emit data
2. **heerich.js** provides the geometry engine — take the data → construct 3D voxel diagrams → export SVG
3. **foom.md** provides the theoretical framework — ask what compression survives, which zones are stable, what gates are saddle points
4. Back to unit.land: implement the compression metrics as visual graph nodes, render stability scores

## Empirical Validation Questions

| Question | Test | Expected Outcome |
|----------|------|-----------------|
| Can unit.land's Audio API replicate our Python MIR pipeline? | Load WAV → analyser node → frequency data → compare to scipy FFT results | Feature correlation > 0.95 for centroid, rolloff; MFCC matching via post-processing |
| Does heerich.js generate numogram diagrams matching our p5.js? | Same input parameters → compare SVG output to existing numogram-visualization | Structural equivalence, different rendering aesthetic |
| Do numogram basins correspond to MDL basins? | Compute traversal probability vs compression length → scatter plot | High correlation between frequent zone traversals and low description length |
| Can Cronkle bisection find gates faster than exhaustive search? | Time exhaustive syzygy search vs bisection for all 45 demon pairs | Speedup factor depends on zone depth; should be O(log N) vs O(N) |

## Related

- [[InterestingSites]] — source list
- [[cables-gl]] — existing visual programming wiki entry
- [[p5js]] — existing procedural graphics skill
- [[numogram-visualizer-extensions]] — debugging the numogram visualizer
- [[numogram-combinatorial-svg]] — SVG infographic templates
- [[ruview-wifi-csi-transducer]] — CSI sensing pipeline (the other unit.land use case: real-time visualizer)
- [[text-recombination-engine]] — text generation, relates to Mesaton architecture
- [[numogram-calculator]] — zone computation, relates to SAGE geometry
