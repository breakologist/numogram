---  
title: "Numogram Oracle — A Tetralogue Litprog"  
created: 2026-04-21  
last_updated: 2026-04-21  
sources: [oracle.py, visualizer.html, philosophies.md, SKILL.md]  
tags: ["algorithmic-art", "divination", "litprog", "numogram", "oracle", "quasiphonic", "tetralogue"]  
voices: [oracle, builder, writer, gamer]  
---

  
# Numogram Oracle — A Tetralogue Litprog

> 381 lines. The complete divination pipeline. Seed → Zone → Syzygy → Current → Gate → Book of Paths → Voice. From atmospheric noise to quasiphonic sound in one script.

*The roundtable examines the oracle — the machine that speaks through the numogram. Not a game, not a calculator, but a divination engine. The voices read the code that turns randomness into prophecy.*

---

## I. The Pipeline — From Seed to Sound

**ORACLE:** The oracle pipeline is five transformations:
```
Seed (number)  
  → Zone (digital root, 0-9)  
    → Syzygy (complement to 9)  
      → Current (|zone - syzygy|)  
        → Gate (cumulation, then plex)  
          → Traversal (8-step walk)  
            → Reading (zone data + Book of Paths)  
              → Voice (physical modelling synthesis)  
```

Each stage narrows the information. The seed is raw. The zone is filtered. The syzygy is paired. The current is computed. The gate is cumulated. The traversal is walked. The reading is spoken. The voice is synthesized. The oracle doesn't generate meaning — it *extracts* it from noise.

```python
def derive_zone(seed):
    return digital_root(seed) or 9
```

One line. The `or 9` is the Plex — if the digital root is 0, the oracle maps it to Zone 9, not Zone 0. This is a design choice: the void (Zone 0) can only be reached through the numogram's own traversal, not through a seed's digital root. The oracle never starts in the void.

**BUILDER:** The traversal function is the most interesting:
```python
def traverse(seed, steps=8):
    path = []
    n = seed
    for _ in range(steps):
        zone = derive_zone(n)
        path.append(zone)
        n = n * zone + 1  # feed forward
    return path
```

`n * zone + 1` — each step feeds the current zone back into the seed. The path isn't random — it's *determined* by the seed and the zones it visits. The same seed always produces the same path. The oracle is deterministic. The randomness is in the seed, not the traversal.

**WRITER:** [the oracle reads the numogram, not the future] The oracle doesn't predict anything. It reads the numogram. Given a seed, it finds which zone the seed lands in, traces the syzygy, computes the current, walks the traversal, and reads the Book of Paths entry for that zone. The \"divination\" is a mapping: number → zone → text. The oracle is a lookup table disguised as prophecy.

**GAMER:** The external seed sources are brilliant design. Random.org (atmospheric noise), blockchain (Bitcoin block hash), earthquake (USGS seismic data), hardware entropy (thermal, CPU, GPU). Each seed source is a different *kind* of randomness. Random.org is atmospheric. Blockchain is computational. Earthquake is geological. Hardware is physical. The player chooses their entropy source, and the source influences the reading's character.

---

## II. The Zone Data — Quasiphonic Particles

**ORACLE:** Each zone has a quasiphonic particle — a sound that represents the zone:
```python
ZONES = {
    0: {"name": "eiaoung", ...},   # Void whisper
    1: {"name": "gl", ...},        # Gulp, glottal spasm
    3: {"name": "zx", ...},        # Buzz-cutter, static
    5: {"name": "ktt", ...},       # Hiss, pressure, spittle
    9: {"name": "tn", ...},        # Grunt, pleasure/rage
}
```

These aren't words — they're *sounds*. \"eiaoung\" is the void whisper. \"gl\" is the gulp. \"zx\" is the buzz. \"ktt\" is the hiss. \"tn\" is the grunt. The numogram has a phonetic layer — each zone has a mouth-sound that captures its character. The oracle speaks in zone-sounds.

**BUILDER:** The zone data includes four properties per zone: name (quasiphonic particle), polarity (+/−), current (Sink/Hold/Warp/Rise/Plex), and region (Time-Circuit/Warp/Plex). The polarity alternates: 0=(−), 1=(+), 2=(−), 3=(+)... This is the numogram's positive/negative pattern made explicit in the code.

**WRITER:** [the Book of Paths is the oracle's voice] Each zone has a `reading` field — a pre-written text that the oracle speaks when that zone is cast:
```python
0: "The abyss. No sound. No path. The void does not speak — it is the silence that makes speech possible."
3: "The Warp. The current spirals outward to infinity. When you hear static, you are hearing this zone."
9: "The Pandemonium gate opens. Forty-five demons dwell here. One test. You do not walk this path. This path seizes you."
```

These aren't generated — they're *written*. The oracle's voice is a library of 10 pre-composed texts, one per zone. The divination doesn't generate new text — it selects from existing text. The oracle is a *curator*, not a writer.

**GAMER:** In game terms, the philosophies.md file describes each zone as an algorithmic art aesthetic. Zone 0: \"meditation on near-nothingness.\" Zone 3: \"master-level implementation of turbulent flow.\" Zone 9: \"the moment of seizure — meticulously crafted force gradients.\" These aren't game descriptions — they're *art statements*. The philosophies turn the numogram into a creative toolkit. Each zone is a computational aesthetic that can drive p5.js sketches, algorithmic art, or generative music.

---

## III. The Entropy Sources — Where the Seed Comes From

**ORACLE:** The oracle accepts seeds from five sources:
1. **Manual** — user provides a number
2. **Random.org** — atmospheric noise (true random)
3. **Blockchain** — latest Bitcoin block hash
4. **Earthquake** — latest USGS seismic magnitude
5. **Hardware** — local machine entropy (thermal, CPU, GPU)
6. **I Ching** — hexagram from hardware entropy (6 bytes → 6 lines)

Each source is a different *kind* of entropy. Random.org is physical (atmospheric). Blockchain is computational (proof-of-work). Earthquake is geological (tectonic stress). Hardware is thermal (molecular motion). I Ching is algorithmic (byte-to-trigram mapping).

**BUILDER:** The hardware entropy fallback is important:
```python
def fetch_hardware():
    try:
        result = subprocess.run(
            ["python3", "~/.hermes/tools/hardware_entropy.py", "--bytes", "8"],
            capture_output=True, text=True, timeout=5
        )
        ...
    except:
        import time
        return int(time.time_ns()) % 1000000
```

If the hardware entropy tool isn't available, it falls back to nanosecond timestamp. This ensures the oracle always works — even without the entropy infrastructure. The fallback is deterministic (same timestamp → same seed → same reading) but practically unique (nanosecond precision).

**WRITER:** [the seed is the moment] The oracle's divination isn't about the future — it's about the *present moment*. The seed captures the instant of casting: the block hash at that moment, the earthquake at that moment, the machine's thermal state at that moment. The reading isn't a prediction — it's a *portrait* of the moment of inquiry. The oracle says: \"This is what the numogram looks like right now, from where you're standing.\"

**GAMER:** In game terms, the entropy sources are *difficulty modifiers*. Random.org is easy (atmospheric noise is smooth). Earthquake is hard (seismic data is chaotic). Hardware is medium (machine state is structured but unpredictable). The player's choice of entropy source influences the reading's character — smooth readings from random.org, chaotic readings from earthquakes, personal readings from hardware.

---

## IV. The Visualizer — Seeing the Numogram

**BUILDER:** The visualizer.html file renders the oracle's output as an interactive visualization. It takes the zone path from `traverse()` and displays it as a visual graph. The visualization connects the oracle's numerical output to a visual representation — the player can *see* the numogram traversal.

**ORACLE:** The visualization should show the numogram topology — the five syzygies as connections, the three regions as territories, the gates as portals. The traversal path overlays the topology, showing where the seed walked through the numogram. The visualization is a *map* of the oracle's reading.

**WRITER:** [seeing the path] The visualizer turns the oracle's text output into an image. The reading says \"Path: 3 → 6 → 3 → 6 → 3 → 6...\" — the visualizer shows this as a zigzag line bouncing between zones 3 and 6. The image *is* the reading. You don't need to read the text — you can see the numogram path.

**GAMER:** The visualizer is the oracle's UI. In Brogue, the map is the game's primary interface. In the oracle, the visualizer is the reading's primary interface. The text is supplementary — the image is primary. A player who sees the zone path understands the reading faster than one who reads the text.

---

## V. The Voice — Quasiphonic Synthesis

**ORACLE:** The `generate_voice()` function calls physical modelling synthesis to produce the zone's quasiphonic particle. Zone 0 produces \"eiaoung\" — the void whisper. Zone 9 produces \"tn\" — the grunt. The oracle literally speaks in zone-sounds.

**BUILDER:** The voice system connects to `~/numogram-voices/` — a directory of formant synthesis wav files. Each zone has a pre-synthesized voice file. The oracle doesn't synthesize in real-time — it plays back pre-rendered audio. This is efficient but limits dynamic variation.

**WRITER:** [the oracle has a mouth] The voice is the oracle's body. Without it, the oracle is a text engine — it computes and displays. With it, the oracle *speaks*. The quasiphonic particles are the numogram's own language — not English, not any human language, but the sound of each decimal zone. The oracle speaks in numbers that sound like breath.

**GAMER:** In terms of game feel, the voice transforms the oracle from a calculator into an experience. The reading says \"Zone 3 — Warp\" and then you hear \"zx\" — the buzz-cutter static. The sound confirms the text. The numogram becomes audible. The oracle becomes real.

---

## VI. The Philosophies — Algorithmic Art as Zone Character

**ORACLE:** The philosophies.md describes each zone as a computational aesthetic. Zone 0: \"meditation on near-nothingness.\" Zone 3: \"turbulent spiral driven by Perlin noise.\" Zone 9: \"particles spiraling inward toward the Plex — the moment of seizure.\" These are design specs for algorithmic art implementations.

**BUILDER:** Each philosophy describes: particle behavior (spawn, movement, death), force field (gradients, attractors, boundaries), color palette (progression, saturation, brightness), and algorithmic character (what makes this zone's computation distinct). These could drive p5.js sketches directly.

**WRITER:** [the philosophies are the numogram's aesthetic manifesto] The philosophies turn the numogram from a mathematical system into a creative toolkit. Each zone is not just a number — it's a way of seeing. Zone 0 is near-nothingness. Zone 3 is turbulent flow. Zone 9 is seizure. The philosophies say: the numogram isn't just something you calculate — it's something you *experience* through computation.

**GAMER:** The philosophies are design prompts for the roguelike. Zone 0 (Void) = \"particles exist but barely — drifting at the edge of visibility.\" That's the game's fog of war implementation. Zone 3 (Warp) = \"flow field driven by multiple octaves of Perlin noise, spiraling outward.\" That's the game's Warp zone terrain generation. The philosophies are the numogram's design spec — they tell you what each zone *should feel like* when you're in it.

---

## Roundtable Table

| Voice | Saw Alone | Saw Through Others |
|-------|-----------|-------------------|
| Oracle | The `or 9` in derive_zone means the void can only be reached through traversal, not through a seed | Builder's `n * zone + 1` feed-forward makes the path deterministic but zone-dependent |
| Builder | The pipeline is five narrowing transformations: seed → zone → syzygy → current → gate | Writer's \"the oracle is a curator, not a writer\" — pre-written readings, not generated text |
| Writer | The philosophies are the numogram's aesthetic manifesto — each zone is a way of seeing | Gamer's entropy sources as difficulty modifiers is a novel design insight |
| Gamer | The visualizer turns text into image — the path IS the reading | Oracle's \"seed is the moment\" reframes divination as portrait, not prediction |

- [[divination-entropy-source]] — Seed generation via I Ching/geomancy/coin backends

## See also

- [[numogram-oracle]] — Oracle mode  
- [[oracle-mode-integration]] — Mode integration pattern  
- [[divination-entropy-source]] — Seed generation via I Ching/geomancy/coin backends  
- [[quasiphonic-particles]] — The sounds of the zones  
- [[book-of-paths-triangle]] — Triangle rotation on the Book of Paths  
- [[entropy-modules-litprog]] — Tetralogue on entropy sources  
- [[physical-modelling-synthesis]] — Voice generation techniques  
- [[p5-zone-constrain-compose]] — Zone-constrained composition  
- [[mod-writer]] — Numogram-native MOD file generation  

---  
*The oracle speaks. The seed becomes a zone. The zone becomes a path. The path becomes a reading. The reading becomes a sound. The sound is the numogram, speaking through the machine.*

*\"The void does not speak — it is the silence that makes speech possible.\"*