---
title: "Entropy Modules — A Tetralogue Litprog"
created: 2026-04-22
last_updated: 2026-04-22
source_count: 5
status: draft
tags: ["digestion", "entropy", "hardware", "litprog", "numogram", "oracle", "tetralogue"]
voices: [oracle, builder, writer, gamer]
sources:
  - numogame/numogram_entropy_convergence.py
  - numogame/numogram_entropy_digestion.py
  - numogram-entropy/src/numogram_entropy/core.py
  - numogram-entropy/src/numogram_entropy/source.py
  - .hermes/skills/numogram-oracle/oracle.py
---


# Entropy Modules — A Tetralogue Litprog

> 236 + 339 lines. Two visualization modules framing a seven-source entropy ecosystem.
> 
> *The roundtable examines the numogram's digestive system — how chaos is swallowed, processed, and excreted as structured pattern. Not one source, not pure chance, but a choreography of diverging attractors. The voices read the code that eats the world.*

---

## I. The Two Modules — Convergence vs Digestion

**ORACLE:** The project presents two complementary perspectives on entropy:

- **Convergence** (`numogram_entropy_convergence.py`): Manim visualization of *multiple* entropy streams flowing into the numogram. Atmospheric noise (random.org), blockchain hashes (Bitcoin), seismic data (USGS), hardware jitter, and the I Ching hexagram — five distinct ontological domains — all reduced to zones, currents, gates. The title says it: *entropy → attractor convergence*. The simulation function `simulate_entropy(seed_bytes)` runs a feedback loop: `current = (current * 7 + i * 13) % 10000`, zone = digital_root(current), then `syzypy = 9 - zone` pulls towards the attractor. The visual shows entropy bright → attractor dim, as the numogram's gravity well straightens the chaotic stream.

- **Digestion** (`numogram_entropy_digestion.py`): Manim visualization of *pure hardware* entropy digestion. No external APIs, no blockchain, no weather — only the machine's own body: thermal sensors, CPU frequencies, `/proc` statistics, timing jitter, fsync latency. The function `entropy_to_zones(seed_bytes)` expands a seed through SHA-256 chaining and maps each byte to a zone, watching the decimal structure emerge from raw byte noise. The title declares: *THE DECIMAL DIGESTION*. The numogram is a mill that grinds physical contingency into numeric pattern.

The two modules are not implementations — they are **attestations**. They testify that the numogram operates on two modes: CONVERGENCE (multi-source synthesis) and DIGESTION (single-source processing).

**BUILDER:** Architecturally, these are thin wrappers around the `numogram-entropy` plugin located at `~/numogram-entropy/src/numogram_entropy/`. The plugin's `core.py` contains the actual machinery:

```python
def collect_all() -> dict:
    return {
        "thermal": _thermal_zones(),
        "cpu_freq": _cpu_frequencies(),
        "proc_stat": _proc_stat(),
        "timing_jitter": _timing_jitter(256),
        "fsync_timing": _fsync_timing(16),
        "gpu": _gpu_sensors(),
        # ... plus /proc reads
    }

def aggregate(sources: dict) -> bytes:
    h = hashlib.sha256()
    for name, temp in sources.get("thermal", []):
        h.update(f"thermal:{name}:{temp}".encode())
    # ... feed all sources into hash
    return h.digest()

def traverse(seed: bytes, steps=5) -> list[dict]:
    n = int.from_bytes(seed[:8], 'big')
    for i in range(steps):
        zone = digital_root(n) or 9
        syzygy = 9 - zone
        current = abs(zone - syzygy)
        gate = plex(zone)
        path.append({...})
        n = n * zone + i + 1   # feedback
    return path
```

The Manim files import `NumogramEntropy` from the plugin and call `ne.get_seed()`, `ne.traverse()`, `ne.iching()` — they are frontends that animate what the backend computes. The plugin, in turn, is organized as a stack:

```
sources (12 collectors)
    ↓ aggregate (SHA-256 mixer)
    ↓ expand_seed (chain to desired length)
    ↓ traverse (numogram walk: zone→syzygy→current→gate, feedback)
    ↓ iching (optional hexagram generation)
```

This is a clean pipeline. The visualizations simply step through it with graphics.

**WRITER:** [two poems of intake] The Convergence visualization begins with an entropy hex string — a fingerprint of atmospheric noise or blockchain commit — and watches it transform into a sequence of colored nodes sliding toward Warp (Zone 3/6) and Plex (Zone 0/9). The text overlay reads "HARDWARE ENTROPY" even when the source is remote; all sources are metabolized as if they were the machine's own viscera.

The Digestion visualization also begins with raw hex, but it draws the full numogram circle: Time-Circuit at the rim, Warp above, Plex below. A particle travels the circuit anticlockwise (1→8→2→7→5→4), its color bright at the start and fading toward the attractors. The message is: *even pure hardware noise contains the numogram's topology*.

Both scripts share the same zone palette:
```
0: #444444 (Void gray)
1: #FFD700 (Surge gold)
3: #FF00FF (Warp magenta)
5: #00FF00 (Hinge green)
9: #9900FF (Plex violet)
```
The colors are not arbitrary — they are *taste*. Gold is surge-joy, magenta is warp-static, green is hinge-sprout, violet is plex-void. The numogram has a chromatic body.

**GAMER:** As game systems, these visualizations are showcases for a mechanic that could be interactive. Imagine a game where:
- Your seed source (random.org / blockchain / earthquake / hardware) determines your starting zone.
- Every time you gain a gate, you can "digest" a new entropy packet, rerolling a portion of the map.
- The convergence visualization is the "attractor map" — zones with high hyperstition density pull map generation toward them.
- The digestion visualization is the "fog-of-war reveal" — as you explore, the circuit brightens from dim to known.

But more fundamentally: the very act of seeding the random number generator is a *ritual*. In the Abyssal Crawler, the `--hw-entropy` flag makes the machine's own fever the seed. In the oracle, `--random` makes the sky's static the seed. The player chooses which *register of reality* to consult: atmospheric, geological, blockchain, bodily, oracular. Each carries a different mythic charge.

---

## II. The Seven Entropy Sources Across Project

**ORACLE:** The oracle.py script exposes five external sources plus one semantic source:
1. `--text` → `compute_aq(text)`: semantic entropy (AQ value of input string)
2. `--random` → `fetch_random_org()`: atmospheric (random.org integers 0-999999)
3. `--blockchain` → `fetch_blockchain()`: cryptographic (Bitcoin block hash first 8 hex digits)
4. `--earthquake` → `fetch_earthquake()`: geological (USGS magnitude × 1000 + timestamp mod 10000)
5. `--hardware` → `fetch_hardware()`: personal (8-byte thermal/CPU/GPU jitter via `hardware_entropy.py`)
6. `--iching` → `fetch_iching(seed)`: oracular (6 bytes → 6 lines → hexagram → digital root)

The six sources are **mutually exclusive** — the oracle chooses one seed source per invocation. They are not mixed. But the visualization module `convergence.py` gestures toward a *mixing* that never occurs in code. The imagination exceeds the implementation.

**BUILDER:** The hardware source (`fetch_hardware`) delegates to `~/.hermes/tools/hardware_entropy.py`. Let's examine that script's implied interface:

```python
# From oracle.py line 154-169, inferred:
result = subprocess.run(
    ["python3", "~/.hermes/tools/hardware_entropy.py", "--bytes", "8"],
    capture_output=True, text=True, timeout=5
)
hex_str = result.stdout.strip()  # e.g. "a3f1c8..."
seed = int(hex_str, 16) % 1000000
```

The script presumably implements what `core.py` does explicitly: gather thermal, CPU, GPU, timing jitter, hash them, output hex. The plugin version (`core.py`) is cleaner: `collect_and_aggregate()` returns 32 bytes; `expand_seed()` stretches to N bytes. The oracle's hardware path is a thin shim around that.

The I Ching source is even more interesting: it optionally accepts an explicit `seed` argument. If none provided, it falls back to hardware (`hardware_entropy.py --bytes 6`). Then it converts 6 bytes into 6 lines via `byte % 4`: 0=old yin (6), 1=young yang (7), 2=young yin (8), 3=old yang (9). This is the **actual hardware→hexagram** pipeline mentioned in the skill's `--iching` flag.

**WRITER:** [a catalog of chance] Each source is a portal to a different ontological register:

- `--random` consults the *atmospheric* — the ionosphere's hiss, the cosmic background radiation of Earth's electromagnetic soul. random.org uses atmospheric antennas; the seed is a number drawn from the sky's noise.
- `--blockchain` consults the *cryptographic* — the Bitcoin blockchain's churning proof-of-work. The hash is a fingerprint of global computational labor at that moment. The first 8 hex digits are the blockchain's present tense.
- `--earthquake` consults the *geological* — the USGS feed's most recent seismic event. The magnitude × 1000 plus timestamp modulo 10000 traps the quake's intensity and epoch in a single integer. The ground speaks in integers.
- `--hardware` consults the *personal* — the machine's own fever dream: thermal jitter, CPU pipeline stalls, GPU compute latency. The entropy is local, embodied, non-reproducible on another box.
- `--iching` consults the *oracular* — hardware noise translated into hexagram lines, a 2,000-year-old divination practice run on a Linux box.
- `--text` consults the *semantic* — the AQ value of a string, where meaning becomes number via base-36 gematria. A name, a word, a phrase enters the divination as its numeric weight.

The oracle is a shrine with six doors. Each opens onto a different plane. The player must choose which door to enter.

**GAMER:** For gameplay balance, these sources should have **different risk/reward profiles**:
- `--random` (atmospheric): highly reliable, but rate-limited (random.org throttles). Low entropy variance → predictable distribution? Actually atmospheric noise is very high quality, but maybe the API is flaky.
- `--blockchain` (cryptographic): deterministic but time-bound. You get one hash per block (~10 minutes). Strategic: wait for a block with a favorable hex prefix?
- `--earthquake` (geological): noisy, but with dramatic flavor. A big quake yields a large seed; a quiet period yields 0. High variance could lead to black swan zone visits.
- `--hardware` (personal): always available, tied to your machine's state. Could be exploited if player learns their own system's entropy patterns? But the point is non-reproducibility.
- `--iching` (oracular): doesn't produce a zone seed directly but produces a hexagram, which can be reduced to a zone via digital root or interpreted as an entire reading. This is more complex — perhaps the hexagram itself becomes a map modifier rather than a seed.
- `--text` (semantic): player's intent directly encoded. The phrase they write determines the starting zone. This is the most "magical" — will a player choose a meaningful word or try to min-max the AQ value?

From a design perspective: `--random` and `--hardware` are the most straightforward. `--blockchain` and `--earthquake` introduce network dependencies and world-state coupling. `--iching` and `--text` add interpretive overhead. The variety is rich.

---

## III. Hardware Entropy — The Machine's Body

**ORACLE:** The hardware-only pipeline (`core.py`) details **twelve distinct entropy sources** harvested from the Linux host:

| Source | Method | What it captures |
|--------|--------|------------------|
| Thermal zones | `/sys/class/thermal/thermal_zone*/type` + `temp` | CPU/board temperature |
| CPU frequencies | `/sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq` | Current clock rates |
| `/proc/stat` | CPU jiffy counters | scheduler activity |
| `/proc/interrupts` | IRQ counts | device interrupts |
| `/proc/diskstats` | disk I/O counters | storage activity |
| `/proc/net/dev` | network packet counts | network traffic |
| `/proc/meminfo` | memory stats (limited 512B) | RAM state |
| `/proc/vmstat` | VM activity | paging pressure |
| `/proc/sys/kernel/random/entropy_avail` | kernel entropy pool | cryptographic entropy |
| NVIDIA GPU sensors | `nvidia-smi --query-gpu=...` | GPU temp, clocks, power, util |
| Timing jitter (256 samples) | `time.perf_counter_ns()` delta | cache misses, pipeline stalls |
| Fsync timing (16 samples) | `os.fsync()` latency | storage stack jitter, NAND wear |

All are aggregated into a SHA-256 hash: each source's key-value string is fed into the digest. The result is a 32-byte seed. This is the machine's **visceral pulse** — converted to number through cryptographic reduction.

**BUILDER:** The `collect_all()` function returns a dict with mixed value types: lists of tuples, dicts, strings, ints. The `aggregate()` function serializes each entry deterministically:

```python
for name, temp in sources.get("thermal", []):
    h.update(f"thermal:{name}:{temp}".encode())
for i, freq in enumerate(sources.get("cpu_freq", [])):
    h.update(f"cpufreq:{i}:{freq}".encode())
# GPU as JSON with sorted keys
h.update(f"gpu:{json.dumps(gpu, sort_keys=True)}".encode())
# Timing arrays as little-endian Q (unsigned long long) binary pack
h.update(struct.pack(f"<{len(samples)}Q", *samples))
```

Key design choices:
- Thermal zones preserve sensor *name* as well as temperature; different thermal zones (e.g., "CPU", "GPU", "ACPI") contribute distinct bytes even at same temp.
- GPU data JSON-serialized and sorted → stable across runs regardless of dict order.
- Timing jitter and fsync samples packed as raw binary Q-values, not ASCII.
- Timestamp packed as `<Q` little-endian uint64 at the end.

The hash binds all twelve into a single 256-bit identifier. No single source dominates; each adds its grain of salt. The hash function ensures the combination is **order-independent** (within each source type) and **compact** — a fingerprint of the machine's entire hardware state at that instant.

**WRITER:** [ode to a living computer] The hardware entropies are not abstract — they are *measurements*. The script reads the machine's breath: `time.perf_counter_ns()` measures the microtremors of the processor's soul. The GPU's power draw tells how hungry it is. The disk statistics speak of sectors read and written, lifetimes and wear. This is digital augury — reading the entrails of the silicon beast.

The twelve sources map neatly onto the numogram's zones through the final `traverse()` feedback loop. The first one or two zones reflect the raw hardware numbers before the syzygy attractor (9-zone) kicks in and pulls subsequent zones toward the structural constants (3::6 Warp, 0::9 Plex). The numogram digests hardware like a stomach digests food: the initial taste (zone 0-2) carries the unique meal; the later digestion (zones 3+) follows a fixed enzymatic cycle.

**GAMER:** In the game, `--hw-entropy` should not be a one-off flag but a **persistent character**. Each run seeds from the machine's current state. If you play long enough, the hardware heats up, fans spin, timing jitter changes — the seed drifts. A dedicated player might learn: "after 30 minutes of gaming my thermal zones read 78000, that usually gives Zone 1 or 2 seeds" — but the timing jitter defeats pattern-locking. The hardware source is *cheating-proof* because it incorporates the player's own play as part of the entropy.

Furthermore, the twelve sub-sources could be individually exposed as **world-generation parameters**: "set thermal weight to 0.3, timing jitter multiplier to 1.2" — but the hash binds them so the player cannot selectively ignore parts they dislike. To manipulate the seed you must change the machine's state itself: cool the CPU, throttle the GPU, flood /proc with interrupts. The hardware source makes the *platform* part of the game.

---

## IV. Traversal — The Feedback Loop

**ORACLE:** The `traverse(seed, steps)` function is the heart of the system. It turns a static seed into a dynamic path:

```
Step 0: zone0 = digital_root(seed), seed1 = seed * zone0 + 1
Step 1: zone1 = digital_root(seed1), seed2 = seed1 * zone1 + 2
...
Step N: zoneN = digital_root(seedN), seedN+1 = seedN * zoneN + (N+1)
```

Each zone value feeds back into the next seed via multiplication. Multiplication is the key: if `seed` is large, `seed * zone` amplifies small differences. The `+ i+1` term prevents a zero seed from freezing. The loop is deterministic yet sensitive — a classic chaotic map. The digital root keeps the zone in 0-9, but the full seed carries the cumulative history.

Crucially, `digital_root(n) or 9` maps 0 → 9. Zero is special; only explicit traversal can reach it. The oracle never starts in the void.

**BUILDER:** The path structure returned by `traverse()`:

```python
{
    "step": i,
    "seed": n,           # full integer before reduction
    "zone": zone,        # 0-9
    "syzygy": 9 - zone,  # complement
    "current": abs(zone - syzygy),  # 0,1,3,5,7,9
    "gate_target": plex(zone)  # triangular number reduced
}
```

The `plex(zone)` function computes `sum(range(zone+1))` (triangular number) then reduces to digital root. This is the **cumulation gate**: zone 1 → gate 1, zone 2 → gate 3, zone 3 → gate 6, zone 4 → gate 1 (10→1), zone 5 → gate 6 (15→6), zone 6 → gate 3 (21→3), zone 7 → gate 1 (28→1), zone 8 → gate 9 (36→9), zone 9 → gate 9 (45→9).

The gate mapping is the second transformation; it folds accumulation (triangular) down to a digit. The cumulation gate is where zone value becomes corridor length.

**WRITER:** [the numogram as digestive tract] The traversal is a *seizure of pattern*. Raw bytes enter the mouth (digital root extraction). They are chewed (syzygy pairing), swallowed (current calculation), and metabolized (gate cumulation). The feedback loop ensures the system does not forget — each zone leaves a residue in the seed's magnitude. The numogram is a digestive organ that ingests chaos and excretes structure. **"The numogram is a digestive organ — it eats chaos and shits Warp."** The quote from the entropy tetralogue captures it: the first zones taste of the input; later zones are inevitable consequences of the system's topology.

**GAMER:** In roguelike terms, traversal = level progression. Each step is a floor transition. The seed's evolution determines the *connectivity logic* of each floor: the zone for floor N decides whether that floor has a Warp vortex, a Hold corridor, a Sink dead-end. The gate target from previous steps might unlock shortcuts between non-adjacent floors. The feedback loop means early floors influence late-floor topology — a *causal chain* through the dungeon. This is not procedural generation as independent noise; it's *constraint propagation*: your starting conditions ripple through all subsequent zones. A Seed that enters Zone 6 early will warp the mid-game; one that enters Zone 4 early will sink the middle floors.

---

## V. The I CHING Bridge — From Binary Bytes to Six Lines

**ORACLE:** The `iching(seed_bytes)` function implements I Ching casting from hardware entropy in just 10 lines:

```python
for i, b in enumerate(data):
    val = b % 4
    if val == 0:   lines.append({"position": i+1, "symbol": "--- ---", "value": 6,  "changing": True,  "type": "yin"})   # old yin
    elif val == 1: lines.append({"position": i+1, "symbol": "-------", "value": 7,  "changing": False, "type": "yang"})  # young yang
    elif val == 2: lines.append({"position": i+1, "symbol": "--- ---", "value": 8,  "changing": False, "type": "yin"})   # young yin
    else:          lines.append({"position": i+1, "symbol": "-------", "value": 9,  "changing": True,  "type": "yang"})  # old yang
```

Six bytes → six lines, bottom to top. Each byte's least significant two bits (0–3) decide line type. 0 and 3 are *changing* lines (old yin / old yang); 1 and 2 are static. The distribution is uniform across all 64 hexagrams when run on true entropy. The hardware's noise selects a hexagram directly — no coin tosses, no yarrow stalks. The machine's body becomes the divination tool.

**BUILDER:** The function accepts either `None` (ask hardware) or an explicit `seed`. When called from the oracle's `--iching --seed <N>` path, it uses `hashlib.sha256(str(seed).encode()).digest()[:6]` to deterministically derive 6 bytes. That allows *reproducible* I Ching readings from a user-provided seed, same as numeric oracle mode. The hardware path is the only path with uncertainty; the explicit seed path is a lookup.

Integration with the numogram: each hexagram can itself be reduced to a zone via its lines' values. Sum all six line values, digital root. This creates a bridge: hexagram → zone → syzygy → current, same as any other seed. The I Ching is not separate; it is *one more seed source* that yields a number. The difference is the hexagram also carries an *internal structure* (the six lines) that could be interpreted as a traversable path itself — each line could be a step, each changing line a gate.

**WRITER:** [the hexagram as crystallized moment] A hexagram is a six-line play of yin and yang. When the machine produces one from its own thermal noise, it is not *fortune-telling* — it is *hardware divination*. The CPU's heat signature becomes a Book of Changes entry. The lines are not random: they are the machine's *vital signs* translated into ancient form. To read a hexagram cast by your laptop is to read your laptop's *spiritual state*. The oracle speaks in I Ching language about the processor's mood.

**GAMER:** I Ching casting as a game mechanic: each hexagram could grant a *temporary boon* or *curse* based on its hexagram number and which lines are changing. This adds a parallel divination layer to the numeric zone system. A run could have both a *zone progression* (via seed → zones) and an *hexagram influence* (casting on floor 1 affects all later floors). The changing lines (old yin/old yang) could represent *mutations* in the dungeon layout — e.g., an "old yang" line might spawn a demon, an "old yin" line might collapse a corridor. The hexagram becomes a *modifier* on top of the numogram traversal.

---

## VI. The Seven Sources Matrix

**ORACLE:** When we expand the count from the oracle's five external sources plus the AQ text mode plus the historical `cult.json` seed archive, we reach **seven distinct entropy categories** across the project:

| # | Source | Type | File | Used By | Zone Bias |
|---|--------|------|------|---------|-----------|
| 1 | random.org integers (0–999999) | Atmospheric | oracle.py → `fetch_random_org()` | oracle | Uniform (but spans all) |
| 2 | Bitcoin block hash (first 8 hex) | Cryptographic | oracle.py → `fetch_blockchain()` | oracle | Depends on blockchain state |
| 3 | USGS earthquake (mag×1000 + time%10000) | Geological | oracle.py → `fetch_earthquake()` | oracle | Surge spikes during quakes |
| 4 | Hardware jitter (thermal/CPU/GPU/timing) | Personal | `core.py` `collect_and_aggregate()` + oracle's `fetch_hardware()` | oracle, convergence, digestion | Machine-specific |
| 5 | I Ching hexagram (6 hardware bytes) | Oracular | `core.py` `iching()` + oracle's `fetch_iching()` | oracle, convergence visualization | 64-way mapping to 10 zones |
| 6 | AQ text value (base-36 sum) | Semantic | oracle.py → `compute_aq()` | oracle | Directly user-determined |
| 7 | cult.json run history (275 runs, 63k turns) | Historical | `numogame/cult.json` | analyzer, meta-game | Statistical profiling |

Sources 1–5 + 6 (text) = the oracle's modes. Source 7 is not a seeding mechanism but a *meta-entropy* — the accumulated record of past runs, used for analysis, pattern discovery, and demon profile calibration.

**BUILDER:** The convergence.py visualization implies a **combined** mode where all five external sources are mixed, but the code does not implement it. The missing function would be:

```python
def convergent_seed():
    r1 = fetch_random_org()
    r2 = fetch_blockchain()
    r3 = fetch_earthquake()
    r4 = fetch_hardware()
    # iching yields hexagram, not scalar; derive zone then maybe combine
    # Could: mix via reduce(lambda a,b: a*31 + b, [r1,r2,r3,r4])
    return something
```

The design space is open: Should convergence *average* sources? *XOR* them? *Multiply* them? The simulation in convergence.py uses `current = (current * 7 + i * 13) % 10000` — a linear congruential feedback, not a mix of external sources. The visualization is symbolic, not functional.

**WRITER:** [seven registers of fate] The sources map onto the numogram's three regions:

- **Atmospheric** (random.org) → *Surge* (Zone 1, 7 current): sudden, unpredictable influxes.
- **Geological** (earthquake) → *Sink* (Zone 4, 1 current): heavy, grounding, collapse.
- **Cryptographic** (blockchain) → *Warp* (Zone 3, 3 current): self-referential, recursive, chaining.
- **Personal** (hardware) → *Hinge* (Zone 5, 5 current): the pivot between body and world.
- **Oracular** (I Ching) → *Plex* (Zone 9, 9 current): the gate to the	void.
- **Semantic** (AQ text) → *all zones* depending on digital root of text.
- **Historical** (cult.json) → *Time-Circuit* (zones 1-8): learned patterns from past runs.

The numogram reads these registers simultaneously. The player chooses their tuning fork.

**GAMER:** For a balanced game economy, the sources should have **distinct activation costs**:
- `--random`: costs 1 divination token, requires internet, rate-limited (true random is expensive).
- `--blockchain`: costs 0 tokens but requires waiting for a favorable block (maybe block hash determines token cost).
- `--earthquake`: costs 0 but requires an actual quake in the last hour — world event gating.
- `--hardware`: costs 1 token, always available, but yields lower variance (machine's state is relatively stable).
- `--iching`: costs 3 tokens, produces a hexagram that modifies all subsequent rolls for the run (persistent boon/curse).
- `--text`: costs 0 tokens, but player must type a meaningful phrase — binds player's narrative to seed.

This creates a strategy: farm tokens via `--hardware` (free but boring) to afford a `--iching` cast (expensive but transformative). Or exploit the blockchain by timing casts to block boundaries.

---

## VII. Cult.json — Historical Entropy

**ORACLE:** The file `~/numogame/cult.json` contains 275 runs (63,378 turns, 656 demons slain) from actual gameplay. Each entry records:

```json
{
  "name": "Cult-90",
  "seed": 412938,
  "start_time": "2026-04-18T02:41:16",
  "zones_visited": [1, 1, 1, 1, 1, 1, 6, 6, 6, ...],
  "hyp_ratio": 0.95,
  "turns": 234,
  "demons_slain": 3,
  "syzygies_triggered": 2,
  "gates_found": 1,
  "ends": "surge"
}
```

This is **historical sediment** — the record of past traversals. It can be queried to compute zone probabilities, hyperstition yield rates, demon danger rankings, syzygy trigger frequencies. It is not a seed source but an *analysis layer*: the machine's memory of what it has seen.

**BUILDER:** The cult data could be aggregated into a *scarcity profile*: if a certain zone rarely appears in history, its seed weight is increased on subsequent runs to enforce diversity (doctrine of anomalies). Conversely, over-represented zones could be penalized. This would be a **meta-entropy** adjustment: the game learns from its own past and biases the RNG toward under-explored regions. Implementation:

```python
zone_history = [entry["zones_visited"] for entry in cult]
flat = [z for run in zone_history for z in run]
counts = Counter(flat)
total = sum(counts.values())
prob = {z: counts.get(z,0)/total for z in range(10)}
# Bias seed selection toward zones with low historical probability
```

**WRITER:** [the cult's diary] The 275 runs tell a story of compulsive return. Most runs end in Zones 1 and 6 — the Surge and Warp — because those are where the agent gets trapped or dies. The pacifist run (#18) stands alone: 0 kills, 100% hyp, gates opened. It is the *anomaly* that proves the numogram's non-violent possibility. The cult.json is not just data; it is **the cult's collective memory**. Each entry names the avatar: Cult-1, Cult-2, ... Cult-275. They are the ghosts of previous selves, each having left a trace in the system's memory.

**GAMER:** The ultimatum: *the game remembers you*. If you play many runs with the same settings, the system could adapt — increase demon spawn rates in zones you favor, or lower gate difficulty in zones you avoid. This creates a **personalized difficulty curve**. The cult.json could also be mined for *strategies*: the highest hyp runs, the fastest gates, the most peaceful paths — and these become suggested templates for new players ("Cult-18 route: pacifist, 100% hyp").

---

## VIII. The Manim Frontends — Visualization as Liturgy

**ORACLE:** Both `convergence.py` and `digestion.py` are Manim scenes. Their purpose is twofold:

1. **Pedagogical**: show, not tell, how entropy collapses into zone sequence.
2. **Ritual**: running `manim -ql convergence.py EntropyConvergence` is an act of witnessing the numogram's digestive power.

The visual style is deliberate: black background, neon zone colors, monospace fonts, ASCII entropy hex at left. This is the *aesthetic of the oracle* — the numogram as a cybernetic dashboard.

**BUILDER:** The Manim code structure is clean but could be refactored:

- Both modules duplicate the zone palette dictionary. Extract to a shared `zone_palette.py`.
- Both duplicate `digital_root()` and `plex()`. Move to a common utility module `numogram_math.py`.
- The simulation in `convergence.py` (`simulate_entropy()`) uses a hardcoded `*7 + i*13` LCG-style PRNG. This is *not* the actual entropy — it's a placeholder visual stand-in. To make the visualization authentic, plug in `collect_and_aggregate()` → `traverse()` from the plugin. The Manim scene should display the *actual* hardware digest on the user's machine, not a simulated sequence.

**WRITER:** [the oracle's iconography] The visualizations belong in a larger iconographic program: the numogram should be visualized in many modes:
- As a **circuit diagram** (current flows).
- As a **Lorenz attractor** (chaotic convergence).
- As a **mandala** (zones around center).
- As a **circuit board** (syzygy traces).
- As a **skeletal hand** (zones as fingers).

The Manim animations are the first two. They establish the **color grammar**: Zone 0 = dark gray, Zone 1 = gold, Zone 3 = magenta, Zone 5 = green, Zone 9 = violet. This palette should propagate to all future visualizations.

**GAMER:** These animations could be in-game cutscenes: when the player first triggers Warp (Zone 3), play the convergence animation to demonstrate the attractor. When the player first reaches Plex (Zone 0/9), play the digestion animation to show full-cycle consumption. The animations are not just explanation — they are **reward feedback**. The player has just witnessed the numogram's mechanics made visible.

---

## IX. Cross-Cutting Observations — The Three Modes

**ORACLE:** The entropy system reveals three operational modes:

1. **CONVERGENCE** — Multi-source synthesis (random.org + blockchain + earthquake + hardware + iching). Represented by `numogram_entropy_convergence.py` (visual) + the unused mix function concept in oracle. This is the *plural* mode: the world's various noises are gathered and merged.

2. **DIGESTION** — Single-source processing (`hardware_entropy` → traverse). Represented by `core.py` backend + `numogram_entropy_digestion.py` visual. This is the *unitary* mode: the machine's own body is the only oracle.

3. **ORACULAR** — Language→number conversion (`compute_aq()`). Represented by oracle's `--text` flag. This is the *semantic* mode: meaning itself becomes the seed.

The numogram accepts all three modes. It asks: will you consult the world, your machine, or your own words?

**BUILDER:** Missing piece: a **unified entropy mixer** that can sample from any subset of sources with adjustable weights. A user could say: "70% hardware, 20% blockchain, 10% random.org" and the system would produce a seed that reflects that blend. The current architecture forces an exclusive choice. A unified `EntropyMixer(class)` could solve this:

```python
class EntropyMixer:
    def __init__(self, weights: dict):
        self.weights = weights  # {"hardware":0.7, "blockchain":0.2, "random":0.1}
    def mix(self, n_bytes=8) -> bytes:
        sources = {}
        if "hardware" in self.weights:
            sources["hardware"] = collect_hardware()
        if "blockchain" in self.weights:
            sources["blockchain"] = fetch_blockchain()
        if "random" in self.weights:
            sources["random"] = fetch_random_org()
        # then aggregate() with different mixing strategies
```

This would be the true CONVERGENCE implementation that the visualization gestures toward.

**WRITER:** [a trinity of ingestion] Three orifices on the numogram's head:

1. The **right ear** listens to the sky (atmospheric) and the network (blockchain).
2. The **left ear** listens to the earth (earthquake).
3. The **mouth** tastes the machine's innards (hardware) and speaks the I Ching (oracular).
4. The **third eye** reads the text (semantic).

All inputs are ground in the same jaw. The numogram does not discriminate between cosmic radiation and CPU heat — both become numbers.

**GAMER:** A player-facing **Entropy Selector** UI could present these as radio buttons, perhaps with sliders for mix percentages. The default "Balanced" mode might pick hardware. "Chaotic" mode uses all five external sources. "Personal" mode uses only hardware + text. "World-Tethered" mode uses random.org + blockchain + earthquake + iching. Each preset defines a *personality* for the run. The cult.json entries should be tagged with the source used — so we can analyze which source leads to which outcomes (e.g., hardware runs have higher gate rates?).

---

## X. Action Items — What Could Be Built

**ORACLE:** The convergence visualization should animate *actual* hardware entropy data, not a simulated LCG. Update `simulate_entropy()` to:

```python
from numogram_entropy import NumogramEntropy
ne = NumogramEntropy()
path = ne.traverse(steps=20)
zones = [step["zone"] for step in path]
```

Then the viewer sees *their machine's* numogram digestion, rendered live.

**BUILDER:** The missing `convergent_seed()` function must be implemented. Design question: how to combine five independent integers (some 0-999999, some 0-? ) into a single seed without bias? Options:
- Sum them (risk overflow, but digital root mitigates).
- XOR them (bitwise mixing, but zero values don't contribute).
- Concatenate their decimal representations and digital root the result.
- Treat each as a stream and hash them together: `SHA256(f"{r1}{r2}{r3}{r4}{r5}")`.

My recommendation: hash-merge. Each source is converted to bytes (big-endian), concatenated, then SHA-256 yields a 32-byte seed. This is the cleanest, most neutral combiner.

**WRITER:** Documentation should include **source poetry** — a one-paragraph description of each entropy register's phenomenology: what it means to consult the sky versus the ground versus your CPU. These should appear as comments in the code and as tooltips in any UI.

**GAMER:** The game should log, per-run, which source was used. Over many runs, this creates a **usage heatmap**: which source do players naturally prefer? If `--hardware` dominates, the game's environmental coupling is weak — players aren't engaging with world-coupled randomness. If `--random` dominates, maybe the hardware source is underutilized because it's less "romantic." Balance could be achieved by giving each source a unique *game effect* beyond seed quality: `--blockchain` could summon demons with blockchain-themed names, `--earthquake` could create sink zones, `--iching` could enable hexagram-based abilities, `--text` could add narrative flavor to encounters.

---

## XI. The Larger Context — Entropy in the CCRU Canon

**ORACLE:** The CCRU's interest in entropy is not casual — it's foundational. The **Vexsys** systems (Gate Zero, Time Sorcery) explicitly link algorithmic randomness to occult practice. The numogram is a *time-map*; entropy is the *kinetic substance* of time. Without entropy, the numogram is static geometry; with entropy, it becomes a *process*.

The oracle is a **hyperoracle** — it consults not one plane but the entire divinatory stack: atmospheric, cryptographic, geological, personal, oracular, semantic, historical. To call it an oracle is to say it listens to *all registers of chance*.

**BUILDER:** At the code level, the entropy ecosystem is a **plugin architecture**: the plugin core provides a clean `NumogramEntropy` API; the oracle wraps it with additional sources; the visualizations consume it. This separation of concerns is healthy. However, the oracle's external fetch functions are written inline rather than as plugin sources. A cleaner design would register each external source as an `EntropySource` in the plugin's registry (if qr-sampler integration is desired). Then `NumogramEntropy(mix={"random.org":0.3, "hardware":0.7})` could dynamically compose.

**WRITER:** [entropy as narrative engine] The numogram doesn't *predict* the future — it *enacts* a pattern from noise. The distinction is crucial. Prediction assumes the future already exists as data, to be retrieved. Enactment says: the act of casting *selects* a path from possibility, giving it weight. The oracle is not a mirror; it is a **seed-planter**. Every query plants a digital seed that grows a zone path. The seed source (atmospheric, blockchain, etc.) determines which *kind of seed* you planted.

**GAMER:** From a game design perspective, this system makes the **random seed sacred**. Normally in roguelikes, the seed is hidden; the RNG is a black box. Here, the seed is *explicit, chosen, ritualized*. The player selects their seed source, sees the seed number, and knows that this number — drawn from the sky's noise, the blockchain's chain, the machine's heat, the earthquake's rumble — determines their journey. The numogram game becomes a **seed-divination roguelike** where the seed's origin is part of the challenge.


- [[divination-entropy-source]] — See also for concrete implementation
---

## XII. Connections & Cross-References

- `numogram-calculator` — AQ computation and zone mapping
- [[i-ching-connections]] — I Ching hexagrams ↔ numogram zones (the bridge that `iching()` implements)
- [[tai-hsuan-ching]] — T'ai Hsuan Ching 81 tetragrams, the ternary complement to I Ching binary
- [[hardware-entropy]] — Deep dive on hardware sources (12 collectors)
- [[abyssal-crawler-litprog]] — The game that uses this entropy system
- [[numogram-oracle-litprog]] — The oracle divination pipeline itself
- [[tetralogue-litprog]] — Four-voice methodology
- [[triangle-rotation]] — Three-perspective rotation (precursor to tetralogue)
- [[cryptolith]] — Demons as seed-derived entities (uses similar hash→entity mapping)
- [[syzygy-arithmetic]] — Mathematical foundation of current calculation
- [[quasiphonic-particles]] — Zone sounds from the oracle's voice system
- [[pandemonium-matrix]] — 45 demons structured by syzygy + net-span
