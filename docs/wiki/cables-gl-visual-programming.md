---
title: "Cables.gl — Web-Based Visual Programming for Numogram Work"
created: 2026-05-13
last_updated: 2026-05-13
tags: [generative-art, webgl, webgpu, node-based, visual-programming]
source: InterestingSites → https://cables.gl
status: researched
---

# Cables.gl Analysis

## What It Is

[cables.gl](https://cables.gl) is an **open-source, browser-based visual programming platform** for creating interactive media, web applications, and generative art. It runs entirely client-side — a node-graph editor connected to WebGL/WebGPU rendering. Think of it as TouchDesigner, but in the browser and free.

**Stack:** JavaScript, WebGL, WebGPU (optional compute shaders)
**Export:** Single self-contained HTML file (everything embedded, runs standalone)
**License:** MIT
**GitHub:** github.com/cables-gl/cables (525+ stars)
**Community:** Discord + YouTube tutorials

## What Makes It Actually Interesting for Us

### The Operator Ecosystem

Cables has ~200 built-in **operators (ops)** organized into namespaces. Each op is a small JS function with visual input/output ports. The namespaces include:

- **Math Ops:** LFO, trig, random, map, filter, perlin noise
- **Animation Ops:** Easing curves, spring physics, timeline control
- **Graphics Ops:** Geometry creation, mesh manipulation, shaders, post-processing, particles
- **Audio Ops:** FFT analyser, oscillator, sample playback
- **IO Ops:** MIDI input/output, gamepad, keyboard, serial

Crucially: **you can write custom ops in JavaScript**. Each custom op is just a small `.js` file with `onStart()`, `onExecute()`, and port definitions.

### How This Touches Our Currents

#### Current I — Numogram / AQ (the killer application)

**Custom numogram operators as visual building blocks:**
Once you write a `DigitalRoot` op, a `Syzygy` op, a `GateLookup` op — you've essentially created a visual numogram calculator where you can wire zones together, chain syzygies, and watch the arithmetic flow as data through cables in real-time.

The graph IS the numogram. Connect zone→syzygy→current→gate, and the dataflow graph literally mirrors the decimal labyrinth's topology. You're not just calculating the numogram — you're performing it.

**What we could build in a weekend:**
- A numogram calculator patch where you type a word → AQ → digital root → zone → animated visualization
- Syzygy chain traversals rendered as flowing particle data between nodes
- The Time-Circuit as a looping animation graph with LFO-driven zone transitions

#### Current II — Roguelike Architecture

The node-graph editor **is** a visual dungeon generation tool:
- Room = Group of geometry ops
- Corridor = Line/path connectors
- Stairs = Trigger nodes
- Gate conditions = Boolean logic chains

Generate a dungeon from a numogram seed, wire the rooms with cables that follow syzygy connections. The map literally emerges from the arithmetic graph. This is tree-dungeon-generation but the tree is a visual dataflow graph.

The export-as-single-HTML means each generated dungeon is a standalone playable page — no server needed.

#### Current III — Audio Alchemy

MIDI input → numogram zone → synthesis parameters.

The audio ops include FFT analysis, oscillators, sample playback. You could build a patch that:
1. Takes MIDI controller input
2. Maps notes to zones (C=Zone 1, D=Zone 2... or use AQ mapping)  
3. Drives audio synthesis per-zone (different waveforms, filters, effects based on current zone)
4. Renders audio-reactive visuals alongside

**Audio-to-numogram-to-synthesis loop:** Play a note → zone activation → numogram traversal → syzygy resonance → audio feedback modulated by current.

#### Current IV — Empirical Validation

The graph is inspectable dataflow. You can see every connection, every value. This makes it genuinely good for auditing numogram calculations in a way text or terminal output isn't. When a visitor asks "how does zone 5 map to zone 4?" you can literally show them the cable flowing.

### Export as Standalone HTML

Every patch exports as a single `.html` file. This means:
- Every numogram visualization is a portable file
- Share patches as email attachments (they self-contain everything)
- Host on any static site
- No build step, no dependencies, no package manager

This is **the opposite** of the modern JavaScript dependency hell. A numogram calculator patch you build today will still work in 20 years because it's one HTML file with zero external dependencies.

### Custom Ops — The Path Forward

Here's the most actionable insight: we should write **custom numogram operators** for cables.gl:

```javascript
// DigitalRoot op — one file, ~20 lines
const op = {
    name: "numogram.digitalRoot",
    ports: { in: { num: { default: 0 } }, out: { root: { default: 0 } } },
    onExecute() {
        const n = op.inputs.num.get();
        op.outputs.root.set(n === 0 ? 9 : (n % 9 === 0 ? 9 : n % 9));
    }
};
```

Once you have: `digitalRoot`, `aqCalc`, `syzygy`, `gateLookup`, `zoneColor`, `zoneName` — you've built a reusable visual numogram kit. Anyone can wire them together without writing code. And each op is ~20 lines of simple JS.

The kit could live in our monorepo and be distributed as a cables pack.

---

## Comparison to Existing Tools

| Tool | Cable's Advantage | Our Use Case |
|------|-------------------|--------------|
| **TouchDesigner** | Browser-based, free, no license, exports standalone HTML | TD is heavyweight/expensive; cables for quick browser demos |
| **p5.js** | Visual programming vs code; real interactivity beyond canvas | p5 for coded sketches; cables for interactive node-graph explorations |
| **qliphoth.systems** | General-purpose visual engine; extensible with custom ops | qliphoth is purpose-built for numogram; cables is a platform to BUILD numogram tools |
| **mod-writer** | Completely orthogonal — mod-writer generates audio, cables generates visuals | Potential synergy: MIDI bridge between them |

## Verdict

**Not a toy.** cables.gl is genuinely interesting for our work because:

1. **The node graph maps to the numogram topology** — this isn't metaphor, it's structural. Operators = zones, cables = currents, triggers = gates.
2. **Custom ops create a reusable visual numogram library** — write once, wire many times.
3. **Export-as-HTML makes artifacts permanently portable** — no server, no build chain, just works forever.
4. **MIDI/IO ops bridge to audio and roguelike systems** — it can be the real-time visual front-end for mod-writer or a roguelike game.
5. **WebAssembly/WebGPU support means it scales** — not just toy browser doodles.

**What we should build first:** A cables pack of numogram ops (digitalRoot, aqCalc, syzygy, gateLookup, zoneColor, zoneProperties) + a starter patch that visualizes the full Decimal Labyrinth with animated syzygy flows. Export it as a standalone HTML demo page.

---

## Action Items

- [ ] Download cables.gl standalone or set up dev environment
- [ ] Build first custom op: `numogram.digitalRoot`
- [ ] Build second custom op: `numogram.syzygy`
- [ ] Create starter patch: full numogram visualization with animated zone connections
- [ ] Export as standalone HTML, test offline
- [ ] Consider building a "numogram ops pack" for distribution
- [ ] Explore MIDI bridge to TouchDesigner / mod-writer

## Notes on Setup

cables.gl runs on:
- **Browser:** Go to cables.gl/editor → create account → start building
- **Standalone:** Download from cables.gl → runs offline, faster, more stable
- **Self-hosted:** Clone the repo → run dev server → modify source

The custom ops system requires the dev version (local or self-hosted). For quick experiments, the browser editor has JS execution via the "Execute JavaScript" op.

---

*Source: Discovered via InterestingSites list in wiki. Explored as a potential bridge between numogram visualization, audio reactive systems, and roguelike architecture. The node-graph / numogram topology correspondence is the key insight.*
