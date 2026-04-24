---
title: Numogram Divination
created: 2026-04-13
last_updated: 2026-04-22
source_count: 1
status: draft
tags: [numogram, divination, oracle]
---

# Numogram Divination

A method for reading the [[numogram]] as an oracle — using any number as input to trace a path through zones, syzygies, currents, and gates.

## Method

Given a number — a date, a name value (via [[alphanumeric-qabbala]]), a random seed, or any integer — perform the following:

### Step 1: Find the Zone

Reduce the number to a single digit via digital root (repeated digit-summing). This is the **querent's zone**.

Example: AQ value of "TEMURAH" = 142. Digital root: 1+4+2 = 7. Zone 7.

### Step 2: Find the Syzygy

Each zone pairs with its complement to 9. The syzygy partner reveals what *completes* the querent.

| Zone | Syzygy Partner |
|------|---------------|
| 0 | 9 |
| 1 | 8 |
| 2 | 7 |
| 3 | 6 |
| 4 | 5 |

Zone 7 pairs with Zone 2. The querent at 7 is completed by 2.

### Step 3: Find the Current

Each syzygy produces a current (the difference between the paired zones). The current tells you *where the energy flows*.

- Syzygy 1::8 → current 7 (Rise)
- Syzygy 2::7 → current 5 (Hold)
- Syzygy 4::5 → current 1 (Sink)
- Syzygy 3::6 → current 3 (Warp — spirals outward)
- Syzygy 0::9 → current 9 (Plex — spirals inward)

Zone 7 is in the 2::7 syzygy, so its current is 5 (Hold). The energy is stabilizing, conserving.

### Step 4: Find the Gate

Apply plexing (see [[gates-and-plexing]]): sum from the zone down to 1, then reduce.

Zone 7: 7+6+5+4+3+2+1 = 28 → 2+8 = 10 → 1+0 = 1. Gate Gt-28 opens from Zone 7 to Zone 1.

### Step 5: Read the Path

The complete reading:

> Querent at Zone 7 (+, Rise current). Completed by Zone 2 (−, Horizon). Current flows as Hold (5) — stabilization. Gate opens toward Zone 1 (Anamnesis, memories and dreams). The path goes from ascent into remembrance.

## Reading Example: Random Seed

Seed from random.org: **192855**

Digital root: 1+9+2+8+5+5 = 30 → 3+0 = 3. Zone 3.

- Syzygy: 3::6 (Warp)
- Current: 3 (Warp — spiralling outward, chaotic)
- Polarity: + (Process, becoming)
- Sound: *zx* (buzz-cutter, static, insectoid)
- Gate: Gt-6 (3→6, ascending into the Warp itself)

Reading: *The seed lands in the Warp. The current spirals outward. The gate ascends from chaos into deeper chaos. The map will be turbulent, recursive, and expanding.*

This seed is ideal for generating a dungeon with expanding rooms, increasing complexity, and no stable centre.

## Comparison: Atlantean Cross

The [[subdecadence]] system uses a different spread — the Atlantean Cross — which draws five cards/values and maps them to syzygy positions. The divination method above is simpler (single-number) but less nuanced.

## Implementation: `numogram-oracle` CLI

The full divination pipeline is implemented in `~/.hermes/skills/numogram-oracle/oracle.py`. Available modes:

```
python3 oracle.py --seed 192855                # basic reading
python3 oracle.py --random                    # random.org seed
python3 oracle.py --hardware                  # local entropy (/dev/urandom)
python3 oracle.py --iching                    # I Ching hexagram + numogram reading
python3 oracle.py --iching --seed N           # I Ching from specific seed
python3 oracle.py --taixuan                   # T'ai Hsuan two-tetragram oracle
python3 oracle.py --taixuan --voice           # with oracle sentence audio
python3 oracle.py --traverse 192855           # full zone-by-zone path
```

**Voice generation** (`--voice`) calls `oracle_sentences.py` to produce convolved oracle voices (formant synthesis through zone resonators). Files saved to `~/numogram-voices/oracle_sentence_z{N}_{name}_convolved.wav`.

**T'ai Hsuan mode** (`--taixuan`) derives two tetragram indices (0–80) from the seed via SHA-256, maps each to a zone (digital root), and performs a net-span demon lookup (Uttunul, Murrumur, Oddubb, Djynxx, Katak). This is the richer ternary oracle with 81 tetragrams and 6,561 possible two-tetragram combinations.

See also: [[tai-hsuan-ching-demons]] for the complete mapping and Em-state analysis.


See also: [[alphanumeric-qabbala]], [[gates-and-plexing]], [[quasiphonic-particles]], [[subdecadence]]
