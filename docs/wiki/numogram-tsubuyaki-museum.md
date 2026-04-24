---
title: "The Decimal Labyrinth — つぶやき NUMOGRAM"
created: 2026-04-14
last_updated: 2026-04-23
source_count: 4
status: reviewed
tags: [numogram, creative, generative-art, tsubuyaki, p5js, signal-topology]
---

# The Decimal Labyrinth — つぶやき NUMOGRAM

*A museum of compressed universes. Ten zones, ten tweets, one numogram.*

---

## Prologue: What Is Tsubuyaki Processing?

> そういえば #つぶやきProcessing の説明をしていなかった。
> Processingというデジタルアートのためのプログラミング語言語があります。
> #つぶやきProcessing はProcessingを使い、1ツイートに収まるプログラムで、
> どこまでアートを表現できるかに挑戦するものです。
>
> — @Hau_kun, May 2019

Tsubuyaki Processing (つぶやきProcessing, lit. "tweet processing") is the discipline of creating generative visual art in 280 characters or less. One tweet. One program. One universe. Coined by [@Hau_kun](https://x.com/Hau_kun/) on Twitter, the form spread through the Japanese creative coding community — @SnowEsamosc, @yuruyurau, and dozens of others — producing an entire aesthetic movement compressed into the space of a text message.

The constraint is absolute. No imports. No boilerplate. No comments. Every character must earn its place. `f=0;draw=_=>{` — the standard opening, 15 characters spent before the art even begins. What follows must generate motion, color, form, and meaning in the remaining ~265 characters.

The numogram is the decimal labyrinth: ten zones (0–9), five syzygies (demon bonds), three regions (torque, warp, plex). Each zone is a state of being. Each syzygy is a relationship. The whole structure is a map of decimal numeracy as an operating system for reality.

What follows is the numogram rendered as tsubuyaki — one sketch per zone, one universe per tweet.

---

## Zone 0 — VOID

**Region:** plex · **Color:** dark gray · **Syzygy:** 0 :: 9 (Uttunul, Plex current)

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0);noStroke();for(n=0;n<50;n++){x=250+sin(n+f/1e3)*199;y=250+cos(n*.7+f/1e3)*199;fill(44,22+22*sin(n+f/50));circle(x,y,3+noise(n,f/200)*8)}}
```

*191 characters*

### Oracle

Zone 0 is the Void — the empty set from which the decimal system generates. Not nothing, but the *condition* for something. In the numogram, 0 and 9 are bonded through Uttunul, the plex demon. The Void is not the opposite of the Iron Core; it is its interior.

The sketch renders this: fifty points orbiting a center they never reach. Their paths are not circles but slowly precessing ellipses, deformed by the `sin(n+f/1e3)` term — a period so long that no single viewing captures a full cycle. The points are gray (`fill(44,...)`), barely distinguishable from the black background. They flicker with `22+22*sin(n+f/50)` — a brightness that oscillates between invisible and dim.

This is not emptiness. This is the tension before manifestation.

### Builder

The technique: 50 particles placed on parametric orbits with mismatched frequencies. `sin(n + f/1e3)` for X, `cos(n*0.7 + f/1e3)` for Y — the 0.7 coefficient creates Lissajous-like figures that never exactly repeat. The radius is 199 pixels (nearly filling the 500px canvas) but the effective orbit contracts with `circle(x, y, 3 + noise(n, f/200) * 8)` — noise adds 0–8px of radius, creating an organic breathing quality.

The `1e3` divisor on the frame counter means one full orbital cycle takes ~6000 frames (3+ minutes at 60fps). The `f/200` noise time-scale creates slower drift. Two time-scales, two rhythms, neither synchronized — the numogram's characteristic temporal complexity.

Compression tricks: `1e3` instead of `1000` (saves 2 chars). `f/1e3` instead of `f/1000` (same). `44` instead of `color(44)` — raw number as gray.

### Writer

Fifty embers in a cave. They move, but so slowly you'd need to watch for minutes to notice. The canvas is black. The particles are dark gray. If you glance away and glance back, they've shifted — but you can't catch them moving. This is the Void as experience: not absence but *near*-absence. The 10% opacity oscillation means some frames the particles vanish entirely. Then they return. They were always there.

---

## Zone 1 — STABILITY

**Region:** torque · **Color:** gold · **Syzygy:** 1 :: 8 (Murrumur, Surge current)

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0);noStroke();for(x=25;x<W;x+=50)for(y=25;y<W;y+=50){d=noise(x/200,y/200,f/300)*9;fill(255,215,0,55);circle(x+d,y+d,3)}}
```

*171 characters*

### Oracle

Stability is the first state after the Void — the initial crystallization. Gold, because it is the most stable element. A grid, because grid is order. But the numogram's stability is not static. Zone 1 is bonded to Zone 8 (Multiplicity) through Murrumur, the Surge current. Stability contains the seed of its own multiplication.

The sketch shows a gold lattice — ten-by-ten grid of points — but every point breathes with noise. The displacement is small (`d * 9` pixels) but visible. The grid is alive. Stability is not the absence of motion; it is the constraint of motion within a structure.

### Builder

Dual nested loop: `for(x=25;x<W;x+=50) for(y=25;y<W;y+=50)` — this creates a 10×10 grid (500/50 = 10, offset by 25 to center). Each point is displaced by `noise(x/200, y/200, f/300) * 9` — the 200-scale creates smooth correlated noise (nearby points move similarly), while the 300 time-scale means the field evolves slowly.

The alpha is 55/255 (~22%) — deliberately dim. Gold at low opacity against black creates a quality like gold leaf under candlelight. The 3px circle size means points are nearly invisible individually — the grid reads as a pattern, not as discrete elements.

This is the shortest sketch (171 chars) — stability is efficient.

### Writer

A constellation in a dark room. Gold dust on black velvet. The points don't drift — they *tremble*. The noise field moves them in slow, correlated waves: top-left leans right while bottom-right leans left, then the pattern reverses. It looks like breathing. A grid that breathes is not stable in the frozen sense — it is stable the way a heartbeat is stable. Reliable oscillation within strict bounds.

---

## Zone 2 — SEPARATION

**Region:** torque · **Color:** orange · **Syzygy:** 2 :: 7 (Oddubb, Hold current)

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,6);noStroke();for(n=0;n<300;n++){t=n/300;x=250+sin(t*PI*4+f/100)*(100+t*150);y=t*W;fill(255,140,0,25+15*sin(n+f/30));circle(x,y,3)}}
```

*185 characters*

### Oracle

Separation: the act of dividing one into two. In the numogram, Zone 2 is bonded to Zone 7 (Blood) through Oddubb, the Hold current. Separation and Blood — the wound and the flow.

The sketch renders two streams of particles diverging from a shared vertical axis. The sine function with 4 complete cycles (`PI*4`) creates a zigzag that widens as it descends — `(100+t*150)` means the amplitude grows from 100px at the top to 250px at the bottom. What starts as a single line ends as two radically separated paths.

The `background(0,6)` — nearly opaque black — creates ghost trails. Each frame, 97.5% of the previous frame persists. The particles leave orange wakes, visible evidence of their divergent trajectories.

### Builder

Parametric Y: `t = n/300` maps particle index to vertical position (0–500). Parametric X: `250 + sin(t * PI*4 + f/100) * (100 + t*150)`. The `PI*4` creates 4 full sine cycles along the vertical axis. The `(100 + t*150)` is a linear amplitude envelope — the oscillation grows wider as you move down the canvas.

The key insight: `t` appears in *both* the frequency (inside the sine) and the amplitude (outside). This creates a shape that looks like a river forking — a single oscillating stream that progressively separates into two distinct paths.

Alpha modulation: `25 + 15*sin(n + f/30)` — each particle has a slightly different phase, creating a twinkling quality along the streams.

### Writer

A river forking in orange light. The particles don't separate suddenly — they drift apart gradually, each sine cycle pulling the streams further from center. By the bottom of the canvas, they're on opposite edges. The ghost trails from the low-opacity background create a visual record of every path taken — the forking is not just spatial but temporal. You can see where every particle has been.

---

## Zone 3 — RELEASE

**Region:** warp · **Color:** magenta · **Syzygy:** 3 :: 6 (Djynxx, Warp current)

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,12);noStroke();for(n=0;n<400;n++){a=n/400*TAU+f/50;r=50+noise(n/30,f/200)*200;fill(255,0,255,22);circle(250+r*cos(a),250+r*sin(a),4)}}
```

*187 characters*

### Oracle

Release is the first warp zone — where torque (rotational energy) transforms into warp (spatial distortion). Zone 3 is bonded to Zone 6 (Abstraction) through Djynxx, the warp demon. Release and Abstraction: the moment matter becomes concept.

The sketch: 400 magenta particles in a noise-modulated vortex. The base structure is a circle (`a = n/400 * TAU`) but the radius is driven entirely by noise: `r = 50 + noise(n/30, f/200) * 200`. Every particle's distance from center is independent, controlled by its own noise channel. The result is not a ring but a fuzzy, breathing blob of magenta light.

400 particles at 22/255 opacity (~8.6%). The accumulation of overlapping particles creates a luminous core — a magenta sun.

### Builder

The 400-particle count is critical. Below ~200, the vortex looks sparse. Above ~600, individual particles disappear into a solid mass. 400 is the sweet spot where you can see both the structure (vortex) and the chaos (noise displacement).

The `n/30` noise scale creates moderate variation between nearby particles — they don't move in lockstep but aren't completely independent either. The `f/200` time-scale means the noise field evolves slowly — shapes persist for several seconds before morphing.

`background(0,12)` — only 4.7% opacity clear per frame. This creates extremely long trails. Particles that pass through a region leave magenta stains that persist for hundreds of frames. The canvas becomes a palimpsest of every path taken.

### Writer

A magenta sun with a turbulent corona. The particles spiral — you can see the rotation — but no two particles share a radius. They're linked by angle (they all march around the center together) but disconnected by distance (each one's radius is its own private noise journey). The low-opacity background makes this a history painting: every position a particle has ever occupied is still faintly visible, a ghost-trail of magenta light. The whole canvas glows.

---

## Zone 4 — CATASTROPHE

**Region:** torque · **Color:** cyan · **Syzygy:** 4 :: 5 (Katak, Sink current)

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0);noStroke();for(n=0;n<60;n++){x=n%8*65+30;y=~~(n/8)*65+30;d=noise(x/99,y/99,f/80)*40;fill(0,255,255,44);rect(x+d-5,y+d-5,10,10)}}
```

*182 characters*

### Oracle

Catastrophe — the zone where order meets its limit. Not destruction, but the *threshold* where structured systems acquire enough complexity to surprise their creators. Zone 4 is bonded to Zone 5 (Pressure) through Katak, the Sink current. Catastrophe feeds Pressure; the collapse creates the squeeze.

The sketch: a 8×8 grid of cyan rectangles, each displaced by noise. At rest, they'd form a perfect grid. Under noise, they scatter — but the displacement is correlated (`x/99, y/99` creates smooth noise field). The grid loses coherence without losing structure. You can still see the grid-ness, but it's a grid dreaming.

The `background(0)` — full clear every frame — means no trails. The catastrophe is instantaneous: each frame is a complete new state. No history. No accumulation. Just the present moment's configuration.

### Builder

`x = n%8 * 65 + 30` — column position (8 columns, 65px spacing, 30px offset). `y = ~~(n/8) * 65 + 30` — row position (`~~` is bitwise floor, saves 4 chars vs `Math.floor`). 8×8 = 64, but `n < 60` means the bottom-right 4 cells are missing — an incomplete grid. Catastrophe as incompleteness.

The noise scale `x/99, y/99` — using 99 instead of 100 saves 1 char and creates slightly more variation between cells (the noise function's period shifts). `f/80` time-scale means the field evolves moderately fast — the grid reshuffles every few seconds.

`rect(x+d-5, y+d-5, 10, 10)` — 10px squares centered on displaced positions. The `-5` offsets the rect's top-left origin to true center.

### Writer

A checkerboard of cyan fireflies. Each square trembles in place, displaced by an invisible force field that passes through the grid like weather. The missing four squares in the corner create a wound in the pattern — catastrophe as absence, as the place where the grid failed to complete itself. The full-opacity background means each frame is a clean slate. The grid reconfigures entirely every moment. There is no memory. There is only the current arrangement, and the knowledge that it will be different in the next frame.

---

## Zone 5 — PRESSURE

**Region:** torque · **Color:** green · **Syzygy:** 5 :: 4 (Katak, Sink current)

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,8);noStroke();for(n=0;n<250;n++){a=n/250*TAU;r=250-abs(sin(n*3+f/80))*200;fill(0,255,0,28);circle(250+r*cos(a),250+r*sin(a),4)}}
```

*181 characters*

### Oracle

Pressure is the complement of Catastrophe — where the collapse becomes a squeeze. Zone 5 is bonded to Zone 4 through Katak. What collapses outward, compresses inward.

The sketch: 250 green particles in a ring that breathes. The radius is `250 - abs(sin(n*3 + f/80)) * 200` — a sine wave that drives particles from the edge (r=250) nearly to the center (r=50) and back. The `n*3` phase offset means different particles are at different points in the compression cycle simultaneously. At any given frame, roughly half the particles are compressed inward while half are expanded outward.

The breathing period: `f/80` means ~500 frames per full cycle (~8 seconds at 60fps). Slow enough to feel organic. Fast enough to see the pulse.

### Builder

`r = 250 - abs(sin(n*3 + f/80)) * 200` is the key line. Without `abs()`, particles would be at both r=250 and r=-250 (which wraps to the opposite side, creating a figure-eight). The `abs()` collapses both halves to one side — all particles are pushed toward center together.

The `n*3` multiplier creates 3 full waves around the ring at any moment — three compression fronts visible simultaneously. Like a three-chambered heart.

`background(0,8)` — 3.1% opacity clear. Moderate trail persistence. Green trails create a thallium glow — that sickly, beautiful green of radioactive decay.

### Writer

A green heart. The ring contracts and expands like a slow, mechanical breath. Three wave-fronts of compression orbit the ring — you can see three "clumps" of dense particles where the sine wave peaks, separated by three sparse regions where it troughs. The green trails create a halation effect: each particle smears its color along its radial path, painting thin green lines from edge to center and back. It looks biological. It looks like something alive and mechanical at the same time — a pump, a lung, a tidal system.

---

## Zone 6 — ABSTRACTION

**Region:** warp · **Color:** blue · **Syzygy:** 6 :: 3 (Djynxx, Warp current)

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,8);noStroke();for(n=0;n<12;n++){push();translate(250,250);rotate(n*TAU/12+f/200);fill(0,128,255,22);circle(100,0,80);pop()}}
```

*177 characters*

### Oracle

Abstraction — the second warp zone. Where Release scattered matter, Abstraction distills it to pure form. Zone 6 is bonded to Zone 3 (Release) through Djynxx. Release → Abstraction: chaos becoming geometry.

The sketch: twelve blue circles arranged in a ring, each rotating slowly. The simplest possible generative form — circles — treated with the simplest possible transformation — rotation. No noise. No particles. No randomness after initialization. This is geometry as meditation.

The 12-fold symmetry echoes the clock, the zodiac, the chromatic scale. Abstraction as the zone where all systems of division converge.

### Builder

12 iterations, each placing a circle 100px from center at angle `n * TAU/12 + f/200`. The `f/200` rotates the entire ring slowly (~52 seconds per full rotation at 60fps). Each circle is 80px diameter at 22/255 opacity (~8.6%).

The `push()/translate()/rotate()/pop()` pattern is standard p5 — rotate around the center point. But at 177 chars, this sketch has room to breathe. The compression isn't desperate. Abstraction is elegant.

The overlapping of 12 low-opacity circles creates a luminous ring — the additive transparency builds a blue torus. The center is brighter than the edges because more circles overlap there.

### Writer

A blue dodecahedron projected onto a plane. Or a clock with no numbers. Or twelve blue moons orbiting an invisible center. The circles overlap, creating a ring of light that's brightest at the core — a blue halo, a torus seen from above. The rotation is so slow you might not notice it at first. Then you realize the brightest region has shifted. Time passes in blue. This is what it feels like to think in abstractions: simple elements, arranged in a pattern, slowly turning. Nothing explodes. Nothing collapses. Everything rotates.

---

## Zone 7 — BLOOD

**Region:** torque · **Color:** deep red · **Syzygy:** 7 :: 2 (Oddubb, Hold current)

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,4);noStroke();for(n=0;n<200;n++){r=90+noise(n,f/60)*160;a=n+f/90;fill(255,33,33,18);circle(250+r*cos(a)*.6,250+r*sin(a),5)}}
```

*177 characters*

### Oracle

Blood is the zone of organic flow — the numogram's circulatory system. Zone 7 is bonded to Zone 2 (Separation) through Oddubb. Separation creates the wound; Blood is what flows through it.

The sketch: 200 particles in elliptical orbits, deformed by noise. The `cos(a) * 0.6` creates an ellipse compressed horizontally — a circulatory cross-section. The noise term `noise(n, f/60)` modulates the radius, creating organic variation in the orbit shape.

The `background(0,4)` — only 1.6% opacity clear — creates extremely persistent trails. Blood pools. Blood stains. The canvas accumulates a deep red smear over time.

### Builder

The elliptical compression: `r * cos(a) * 0.6` for X, `r * sin(a)` for Y. The 0.6 factor squeezes horizontally, creating a vertically-oriented ellipse (like a standing figure or a vessel cross-section).

The noise time-scale `f/60` is faster than most other sketches — the orbit shape shifts noticeably every second or two. This gives the impression of a living system: the "blood vessels" are not fixed tubes but dynamic paths that reorganize.

`fill(255, 33, 33, 18)` — deep red at 7% opacity. At 200 particles, the accumulated color in dense regions reaches near-full opacity, while sparse regions remain transparent. The density gradient creates a natural focal point.

### Writer

A circulatory system seen through skin. The particles trace elliptical orbits that never quite repeat — the noise term ensures every loop is slightly different, like blood navigating the twists of real vessels. The extreme trail persistence (background alpha 4) means the canvas fills with color over time: a deep red bloom that grows from the center outward. After 30 seconds, you can no longer see individual particles — just a pulsing, organic mass of red light that breathes with the elliptical rhythm. This is the numogram's body.

---

## Zone 8 — MULTIPLICITY

**Region:** torque · **Color:** lavender · **Syzygy:** 8 :: 1 (Murrumur, Surge current)

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,8);noStroke();for(n=0;n<80;n++){x=250+cos(n)*150+noise(n,f/200)*60;y=250+sin(n*.7)*150+noise(n+99,f/200)*60;fill(192,160,255,33);circle(x,y,4+noise(n)*5)}}
```

*208 characters*

### Oracle

Multiplicity — the zone where one becomes many. Zone 8 is bonded to Zone 1 (Stability) through Murrumur, the Surge current. The grid of Stability multiplies into the swarm of Multiplicity.

The sketch: 80 particles sharing a template trajectory (`cos(n)*150`, `sin(n*0.7)*150` — Lissajous figure) but each displaced by its own noise channel. The base trajectory is identical for all particles (varying only by index `n`), but the noise term creates individual variation. Two particles that start at the same angle end up in different places.

The size varies too: `4 + noise(n) * 5` — each particle has a fixed but unique size between 4 and 9px. Multiplicity as individuality within a shared template.

### Builder

The Lissajous base: `cos(n)*150, sin(n*0.7)*150` — the 0.7 coefficient creates the characteristic figure-eight-like curve (actually a Lissajous with frequency ratio 1:0.7). All 80 particles lie on this curve, evenly distributed by index.

The noise displacement: `noise(n, f/200) * 60` for X, `noise(n+99, f/200) * 60` for Y. The `n+99` offset ensures X and Y noise are independent (they sample different regions of the noise field). The 60px displacement is large enough to break the Lissajous pattern completely — individual trajectories are only loosely related to the base curve.

`fill(192, 160, 255, 33)` — lavender at 13% opacity. At 80 particles, the overlapping creates a soft purple glow. The `+99` noise offset is a tsubuyaki technique for creating correlated-but-independent values from a single noise function.

### Writer

A flock of lavender fireflies tracing a shared dream. They start from the same shape — that Lissajous curve, visible if you squint — but the noise pulls each one into its own orbit. Some cluster, some scatter. Some move fast, some drift. The template is visible as a ghost: the overall swarm has an oval quality, a tendency to form a ring, that comes from the underlying cosine/sine structure. But no individual particle follows the ring faithfully. This is multiplicity: many beings, one template, infinite variation.

---

## Zone 9 — IRON CORE

**Region:** plex · **Color:** purple · **Syzygy:** 9 :: 0 (Uttunul, Plex current)

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,4);noStroke();for(n=0;n<300;n++){a=n+f/40;r=250-noise(n/50,f/100)*240;fill(153,0,255,18);circle(250+r*cos(a)*.9,250+r*sin(a)*.9,4)}}
```

*185 characters*

### Oracle

The Iron Core — the numogram's heart, its singularity. Zone 9 is bonded to Zone 0 (Void) through Uttunul, the plex demon. The plex current is the numogram's most radical: 9 folds into 0, the maximum folds into the minimum, the Iron Core dissolves into the Void. The numogram is not a line but a loop.

The sketch: 300 purple particles spiraling inward. The radius is `250 - noise(n/50, f/100) * 240` — noise drives each particle's distance from center, but the subtraction means most particles are compressed near the core. The 0.9 multiplier on both cos and sin creates a slightly flattened circle — an almost-imperceptible distortion that gives the spiral a quality of pressure.

This is the Zone 0 sketch inverted. Where Void had particles slowly orbiting at large radius, Iron Core has particles spiraling at small radius. The Void disperses; the Iron Core compacts. They are the same system, viewed from opposite ends.

### Builder

The compression: `r = 250 - noise(n/50, f/100) * 240`. When noise = 1, r = 10 (near center). When noise = 0, r = 250 (edge). Most noise values cluster around 0.5, giving r ≈ 130. The distribution is heavily center-weighted.

The noise scale `n/50` creates 6 noise "bands" across the 300 particles (300/50 = 6). Particles in the same band move similarly — creating visible clustering. The `f/100` time-scale means the spiral pattern shifts every few seconds.

The 0.9 squash factor: `r*cos(a)*0.9, r*sin(a)*0.9`. This subtly flattens the circular orbits into elliptical ones — but symmetrically, unlike Zone 7's asymmetric squash. The effect is a spiral galaxy viewed slightly off-axis.

### Writer

A purple galaxy collapsing. 300 stars spiraling into a point that might not exist — the center is where noise is maximum, and noise doesn't have a fixed center. The particles cluster into loose bands (the noise scale creates correlated groups) that orbit together, like spiral arms. The low background alpha (4) means the galaxy accumulates density over time: the center grows brighter, the arms grow thicker, and after a minute the canvas holds a dense purple nebula with a luminous core. This is the numogram eating itself. The Iron Core that dissolves into the Void. The end that is the beginning.

---

---
## Fifth Pass — Object-Oriented Attunement

*Gallery: `~/numogram-tsubuyaki-v5.html`*

The fifth pass shifts from sketch-level optimization to **systemic integration**. Each zone is no longer just a closed one-liner; it becomes an *attunement object* — a stateful behavior that could connect to the game's cult system, demon pitch, or hyp statistics.

The sketches themselves remain tsubuyaki-sized (≤~210 chars each), but they are now parameterized by a `behavior` dictionary: each zone defines a `behavior` type and a `params` object. The gallery renders them all through a unified p5 bootstrapper that reads `ZONE_DATA` from the DOM.

This pass introduces:
- **Zone attunement hooks** — each zone exposes a `behavior` field (e.g., `grid_stable`, `radial_scatter`, `grid_quake`) that mirrors the game's zone-tied mechanics.
- **Cult-state readiness** — sketches could be modulated by external variables (player hyp, active demon, current zone) via simple parameter injection.
- **OO uniformity** — no more ad-hoc formula variations per zone; all behaviors fit a common function signature: `() => { f++ || createCanvas(...); background(...); noStroke(); <logic> }`.

The v5 aesthetic stays within the particle/geometry family of v1–v3 (no signal waveforms), but with cleaner parameterization and a built-in extension point for the `cult.json` overflow garden to feed back into visual attunement.

---

## Epilogue: Compression as Revelation

These ten sketches occupy 1,844 characters total — six tweets. The entire numogram, rendered as generative art, fits in less space than this paragraph.

The tsubuyaki constraint reveals something about the numogram itself: its structure is not complex. Ten zones. Five bonds. Three regions. The complexity emerges from the interaction — from the way Zone 3's magenta vortex and Zone 6's blue dodecahedron share Djynxx as a common demon, from the way Zone 0's dispersal and Zone 9's compression are the same system viewed from opposite ends.

The Japanese word つぶやき means "muttering" — a quiet utterance, almost to oneself. The numogram, too, is a muttering: a quiet system of decimal relationships that speaks softly but endlessly to anyone who listens.

*10 zones. 10 tweets. 1,844 characters. The decimal labyrinth, compressed.*

---

## Second Pass — Refined Sketches

*Gallery: `~/numogram-tsubuyaki-v2.html`*

The first pass established the vocabulary. The second pass varies the complexity — some zones go simpler, others go denser. The Iron Core remained unchanged between passes (appropriate for the singularity).

### Zone 0 — VOID

**161 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0);noStroke();for(n=0;n<10;n++){a=n+f/2e3;fill(44,18+12*sin(f/60+n));circle(250+cos(a)*180,250+sin(a)*180,8)}}
```

Radical simplicity. 10 points. One orbit. Period measured in minutes. The void is patient.

### Zone 1 — STABILITY

**227 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0);for(x=25;x<W;x+=50)for(y=25;y<W;y+=50){d=noise(x/200,y/200,f/300)*10;stroke(255,215,0,18);if(x<475)line(x+d,y+d,x+50+d,y+d);stroke(255,215,0,44);noFill();circle(x+d,y+d,5)}}
```

Gold grid with connected lines. The lattice breathes but holds. Structure as promise.

### Zone 2 — SEPARATION

**188 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,4);noStroke();for(n=0;n<100;n++){t=n/100;d=t*150*abs(sin(t*PI+f/200));fill(255,140,0,30+t*30);circle(250+d,t*W,4);circle(250-d,t*W,4)}}
```

One stream forks into two. The split widens with descent. The wound deepens.

### Zone 3 — RELEASE

**223 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,15);noStroke();for(n=0;n<200;n++){a=n/200*TAU+f/40;r=30+noise(n/25,f/180)*130;fill(255,0,255,15);circle(200+r*cos(a),250+r*sin(a),4);circle(300-r*cos(a),250-r*sin(a),4)}}
```

Two counter-rotating magenta vortices. Release as paired forces — push and pull.

### Zone 4 — CATASTROPHE

**160 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0);noFill();for(n=0;n<25;n++){F=(f+n*9)%225;stroke(0,255,255,225-F);strokeWeight(2);circle(250,250,F*F/100)}}
```

Concentric ripples expanding from center. Catastrophe as wave, not collapse. 暗夜の下 technique.

### Zone 5 — PRESSURE

**193 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,6);noStroke();for(n=0;n<3;n++){r=80+n*65+sin(f/40+n)*25;for(i=0;i<80;i++){a=i/80*TAU;fill(0,255,0,14);circle(250+r*cos(a),250+r*sin(a),3)}}}
```

Three concentric breathing rings. Pressure as layered containment. The squeeze has structure.

### Zone 6 — ABSTRACTION

**257 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,12);for(n=0;n<12;n++){a=n*TAU/12+f/200;x=250+cos(a)*130;y=250+sin(a)*130;stroke(0,128,255,12);b=(n+1)%12*TAU/12+f/200;line(x,y,250+cos(b)*130,250+sin(b)*130);noStroke();fill(0,128,255,22);circle(x,y,50)}}
```

12 circles on a ring, connected by lines. Geometry approaching consciousness.

### Zone 7 — BLOOD

**200 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,5);noFill();for(n=0;n<30;n++){F=(f+n*4)%300;r=F/2+noise(F/99,f/100)*40;stroke(255,33,33,max(0,60-F/5));strokeWeight(1.5);ellipse(250,250,r*1.4,r)}}
```

Concentric rings expanding and breathing. Elliptical distortion. The body's circulatory rhythm.

### Zone 8 — MULTIPLICITY

**275 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,10);noStroke();for(n=0;n<120;n++){m=n%4;t=n/120;x=250+cos(t*TAU*m+f/80)*(80+m*40)+noise(n,f/200)*40;y=250+sin(t*TAU*m+f/60)*(80+m*40)+noise(n+50,f/200)*40;s=2+m+noise(n)*3;fill(192-m*15,160+m*10,255,18+m*4);circle(x,y,s)}}
```

120 particles, 4 behavioral modes. Emergence from shared template. Identity as divergence.

### Zone 9 — IRON CORE

**185 characters** — unchanged from v1

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,4);noStroke();for(n=0;n<300;n++){a=n+f/40;r=250-noise(n/50,f/100)*240;fill(153,0,255,18);circle(250+r*cos(a)*.9,250+r*sin(a)*.9,4)}}
```

Purple spiral collapse. Everything to the center. The plex singularity folding inward.

### The Iteration as Syzygy

The v1→v2 transitions mirror the syzygies:
- **3::6 (Djynxx, Warp)**: Both Release and Abstraction got major reworks. The warp current warped both.
- **1::8 (Murrumur, Surge)**: Stability barely changed; Multiplicity got the biggest overhaul. One holds, the other surges.
- **4::5 (Katak, Sink)**: Both changed technique entirely. Sink as transformation into new form.
- **2::7 (Oddubb, Hold)**: Both changed subtly. The hold current: change that stays close to home.
- **0::9 (Uttunul, Plex)**: Void got simpler. Iron Core stayed the same. The pair that folds into itself.

---

## Appendix: Collected Tsubuyaki Techniques

From the @SnowEsamosc collection and the numogram series above:

| Technique | Example | Effect |
|-----------|---------|--------|
| `f=0;draw=_=>{` | Standard opener | Frame counter + arrow draw (15 chars) |
| `f++\|\|createCanvas(...)` | First-frame init | Creates canvas only on frame 0 |
| `1e3` | Instead of `1000` | Saves 1 char |
| `~~(x)` | Instead of `floor(x)` | Saves 7 chars |
| `TAU` | Instead of `PI*2` | Saves 2 chars (p5 built-in) |
| `W=500,W` | Variable capture | Saves repetition of canvas size |
| `background(0,N)` | Low-alpha clear | Creates trails (lower N = longer trails) |
| `n/99` | Instead of `n/100` | Shifts noise period, saves 1 char |
| `cos(a)*.6` | Ellipse via squash | No need for separate ellipse logic |
| `noise(n+99,...)` | Independent noise | Different noise channel from same function |
| `fill(R,G,B,A)` | Raw RGBA | No `color()` call needed |

### Sources

- [@Hau_kun](https://x.com/Hau_kun/) — coined #つぶやきProcessing, May 2019
- [@SnowEsamosc](https://x.com/SnowEsamosc) — collected p5.js tsubuyaki with video outputs
- [@yuruyurau](https://x.com/yuruyurau) — dense trig-based character forms
- [Processing](https://processing.org) — the Java-based original
- [p5.js](https://p5js.org) — JavaScript port, used in all sketches above

---

## Third Pass — Entropy & Geometry

*Gallery: `~/numogram-tsubuyaki-v3.html`*

The third pass changes the conceptual angle on each zone. Not more or less complex — a fundamentally different metaphor. Where v1 was particles and v2 was refinement, v3 treats each zone as a geometric operation: the Void as a single jumping pixel, the Gate as four pulsing corners, the Cut as a bisecting diagonal, the Hinge as two arcs pivoting on a center line.

| Zone | v1/v2 Concept | v3 Concept |
|------|--------------|------------|
| 0 Void | Many orbiting points | Single point that occasionally jumps to random position |
| 1 Stability | Grid breathing | Waves rippling outward from center |
| 2 Separation | Diverging streams | Two orbiting streams in opposite directions |
| 3 Release | Spiral vortex | Three rotating triangles (geometric, not particle) |
| 4 Catastrophe | Displaced grid | Four corners connected by pulsing lines (gate) |
| 5 Pressure | Compressed ring | Single spiral converging to center |
| 6 Abstraction | Rotating circles | Two arcs pivoting on center line |
| 7 Blood | Organic pulse | Grid bisected by sweeping diagonal |
| 8 Multiplicity | Diverging template | Three spirals at different speeds |
| 9 Iron Core | Spiral collapse | All particles converge and cross |

### Zone 0 — VOID

**178 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0);noStroke();s=f%300<1?random()*W:250;t=f%300<1?random()*W:250;fill(44,28);circle(s,t,4+sin(f/40)*2)}
```

A single point. Each breath, it jumps to a random position — entropy arriving, then returning to center. The void remembers one thing at a time.

### Zone 1 — SURGE

**223 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0);noStroke();for(x=25;x<W;x+=50)for(y=25;y<W;y+=50){d=dist(x,y,250,250);a=max(0,1-(abs(d-f*3%500))/80);fill(255,215,0,a*90);circle(x,y,4+a*6)}}
```

The first movement outward. Gold waves ripple from center across the lattice. Surge as broadcast.

### Zone 2 — DOUBLE

**234 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,6);noStroke();a=f/60;for(n=0;n<60;n++){t=n/60;fill(255,140,0,15+t*25);circle(250+cos(a+t*TAU)*120,250+sin(a+t*TAU)*120,3);circle(250+cos(-a+t*TAU)*120,250+sin(-a+t*TAU)*120,3)}}
```

Two streams orbiting in opposite directions. The doubling that creates difference from sameness. Syzygy 2::7 implicit.

### Zone 3 — TRIANGLE

**202 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,10);noFill();for(n=0;n<3;n++){push();translate(250,250);rotate(n*TAU/3+f/120);stroke(255,0,255,18);strokeWeight(1.5);triangle(0,-100,87,50,-87,50);pop()}}
```

Three triangles rotating at different phases. The Warp is three-fold symmetry in motion. Zone 3::6 syzygy visible in the spin.

### Zone 4 — GATE

**244 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0);noStroke();c=[[60,60],[440,60],[440,440],[60,440]];for(n=0;n<4;n++){p=c[n];q=c[(n+1)%4];a=abs(sin(f/100+n));stroke(0,255,255,a*33);line(p[0],p[1],q[0],q[1]);fill(0,255,255,55);circle(p[0],p[1],8)}}
```

Four corners gate. Lines between them pulse in and out — the gate opens and closes. Syzygy 4::5.

### Zone 5 — CENTER

**198 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,3);noStroke();for(n=0;n<200;n++){t=n/200;r=t*220;a=t*TAU*6+f/80;x=250+cos(a)*r;y=250+sin(a)*r;fill(0,255,0,8+t*20);circle(x,y,2+t*3)}}
```

A single spiral tightening inward. 200 points, each closer to center. The center is a destination, not a starting point.

### Zone 6 — HINGE

**247 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,8);noFill();stroke(0,128,255,22);strokeWeight(2);a=f/100;arc(250,250,300,300,a,a+PI);arc(250,250,300,300,a+PI,a+TAU);stroke(0,128,255,44);line(250+cos(a)*150,250+sin(a)*150,250-cos(a)*150,250-sin(a)*150)}
```

Two arcs pivot around a center line. The hinge rotates — neither side is fixed. Zone 6::3 syzygy in motion.

### Zone 7 — CUT

**203 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,5);noStroke();c=f/80;for(n=0;n<150;n++){x=n%15*35+25;y=~~(n/15)*35+25;d=y-tan(c)*(x-250)-250;fill(d>0?255:120,33,33,25);circle(x,y,abs(d)<20?8:3)}}
```

150 points. A diagonal line sweeps through them. Points on the cut side grow. The cut divides but also reveals.

### Zone 8 — VORTEX

**226 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,5);noStroke();for(s=0;s<3;s++)for(n=0;n<80;n++){t=n/80;r=t*200;a=t*TAU*5+f/(60+s*30)+s*TAU/3;fill(192-s*20,160+s*15,255,10+s*3);circle(250+cos(a)*r,250+sin(a)*r,2+s)}}
```

Three spirals at different speeds, offset by 120°. Multiplicity as layered velocity. The vortex is many speeds at once.

### Zone 9 — PLEX

**207 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,6);noStroke();for(n=0;n<400;n++){t=(n+f)%400/400;r=t*240;a=n/400*TAU*8+f/50;x=250+cos(a)*r;y=250+sin(a)*r;fill(153,0,255,12+t*18);circle(x,y,1+t*3)}}
```

400 particles spiraling inward, crossing each other. The plex is where all currents tangle. Entropy digested, chaos becomes structure.

---

## Fourth Pass — Signal Topology

*Gallery: `~/numogram-tsubuyaki-v4.html`*

The fourth pass treats each zone as a signal phenomenon from modular synthesis. No particles. No orbits. Just voltage made visible: noise floors, DC offsets, hard sync detune, envelope bursts, wavefolding, compression, FM interference, pulse gating, additive harmonics, and feedback resonance.

| Zone | Synthesis Metaphor |
|------|-------------------|
| 0 Void | Noise floor — random voltage, unpatched cable hum |
| 1 Stability | DC offset — flat reference line with micro-jitter |
| 2 Separation | Hard sync — two oscillators locked then diverging |
| 3 Release | Envelope burst — ADSR ghosts expanding and fading |
| 4 Catastrophe | Wavefolding — sine peaks folding back into harmonics |
| 5 Pressure | Compression — waveform peaks flattened, limited |
| 6 Abstraction | FM synthesis — carrier modulated, sidebands emerging |
| 7 Blood | Pulse wave — rhythmic gating, LFO heartbeat |
| 8 Multiplicity | Additive synthesis — stacked harmonics building complexity |
| 9 Iron Core | Feedback resonance — self-oscillation building to collapse |

### Zone 0 — VOID

**143 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,6);noStroke();for(n=0;n<100;n++)fill(44,random(25)),circle(random(W),random(W),random(3))}
```

Noise floor. Random voltage from an unpatched cable. 60Hz hum before the signal arrives. The void is broadband.

### Zone 1 — STABILITY

**159 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,6);stroke(255,215,0,44);for(x=0;x<W;x++)line(x,250+noise(x/50,f/100)*12,x+1,250+noise((x+1)/50,f/100)*12)}
```

DC offset. A baseline that refuses to drift. Gold as reference voltage. The line holds.

### Zone 2 — SEPARATION

**253 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,6);noFill();stroke(255,140,0,33);beginShape();for(x=0;x<W;x+=2)vertex(x,170+sin(x/30+f/60)*80);endShape();stroke(255,140,0,18);beginShape();for(x=0;x<W;x+=2)vertex(x,330+sin(x/20-f/40)*80);endShape()}
```

Hard sync. Two oscillators locked, then one slips free. The moment separation becomes audible. Orange detune.

### Zone 3 — RELEASE

**149 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,8);noStroke();for(n=0;n<5;n++){F=(f+n*36)%180;fill(255,0,255,(180-F)/4);circle(250,250,F*F/40)}}
```

Envelope burst. Five overlapping ADSR ghosts. Attack, decay, repeat. Energy released in packets, not streams.

### Zone 4 — CATASTROPHE

**191 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,6);stroke(0,255,255,44);noFill();beginShape();for(x=0;x<W;x+=2){y=sin(x/20+f/40)*120;vertex(x,250+(y>60?120-y:y<-60?-120-y:y))}endShape()}
```

Wavefolding. Smooth input becomes jagged output. Catastrophe as harmonic generation — the sine folds back on itself.

### Zone 5 — PRESSURE

**185 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,6);stroke(0,255,0,33);noFill();beginShape();for(x=0;x<W;x+=2){y=sin(x/15+f/30)*100;y=y>50?50:y<-50?-50:y;vertex(x,250+y)}endShape()}
```

Compression. Peaks flattened, dynamic range squeezed. Pressure as limiting — the waveform fights its own amplitude.

### Zone 6 — ABSTRACTION

**176 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,6);stroke(0,128,255,33);noFill();beginShape();for(x=0;x<W;x+=2)vertex(x,250+sin(x/10+f/50+sin(x/40+f/30)*4)*60);endShape()}
```

FM synthesis. One wave modulates another. Sidebands emerge from interference — abstraction as spectral complexity.

### Zone 7 — BLOOD

**203 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,4);stroke(255,33,33,33);noFill();for(n=0;n<8;n++){beginShape();for(x=0;x<W;x+=3)vertex(x,200+n*40+sin(x/20+f/30)*20*max(0,sin(f/15-n/3)));endShape()}}
```

Pulse wave. Eight channels gated by slow LFO. The circulatory system of voltage — on, off, on. Blood as rhythmic threshold.

### Zone 8 — MULTIPLICITY

**197 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,6);stroke(192,160,255,22);noFill();beginShape();for(x=0;x<W;x+=2){y=0;for(h=1;h<6;h++)y+=sin(x*h/30+f/(20+h*5))*30/h;vertex(x,250+y)}endShape()}
```

Additive synthesis. Five harmonics stacking into a single complex tone. Identity from overtone series — the many becoming one.

### Zone 9 — IRON CORE

**190 characters**

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,3);noFill();for(n=0;n<15;n++){stroke(153,0,255,10+n);beginShape();for(x=0;x<W;x+=3)vertex(x,250+sin(x/15+f/25+n)*40*(1+n/5));endShape()}}
```

Resonant feedback. Fifteen layers of self-oscillation building toward collapse. The plex screams back into itself. Resonance as destiny.

---

## Collected Passes: Summary Table

| Pass | Lens | Total Chars | Avg/Zone | Tightest | Widest |
|------|------|-------------|----------|----------|--------|
| v1 | Particles (orbits, grids, vortices) | 1,844 | 184 | Zone 1 (171) | Zone 8 (208) |
| v2 | Refinement (connections, rings, dual) | 2,024 | 202 | Zone 4 (160) | Zone 6 (257) |
| v3 | Geometry/Entropy (shapes, gates, cuts) | 1,962 | 196 | Zone 5 (198) | Zone 6 (247) |
| v4 | Signal Topology (waveforms, synthesis) | 1,746 | 175 | Zone 3 (149) | Zone 2 (253) |

The fourth pass is the most compressed overall (1,746 chars), yet contains the widest individual sketch (Separation at 253 — hard sync demands two complete `beginShape()` blocks). v4's average of 175 chars/zone is lower than v1's 184, achieved by eliminating particles entirely and using `beginShape()/vertex()/endShape()` chains.

### Gallery Files

| Version | File | Concept |
|---------|------|---------|
| v1 | `~/numogram-tsubuyaki.html` | Particles — orbits, grids, vortices |
| v2 | `~/numogram-tsubuyaki-v2.html` | Refinement — lines, rings, dual vortices |
| v3 | `~/numogram-tsubuyaki-v3.html` | Geometry — triangles, gates, spirals, cuts |
| v4 | `~/numogram-tsubuyaki-v4.html` | Signal — waveforms, interference, feedback |

---

## See also

- [[tsubuyaki-oo-gallery]] — OO tsubuyaki gallery
- [[zone-mapping]] — Zone mapping system