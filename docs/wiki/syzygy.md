---
title: Syzygy
created: 2026-04-27
source: cli/aq_calculator_canonical.py + numogram-source.txt + raw/www.ccru.net/syzygy.htm (live server)
status: reviewed
tags: [syzygy, current, zygonovism, twin, nine-sum]
---

# Syzygy

A **syzygy** is a complementary pairing of two zones whose digits sum to 9. The five syzygies are the structural backbone of the Decimal Numogram; each produces a directed flow called a **current**.

**Live source:** <http://127.0.0.1:8080/syzygy.htm> (CCRU master glossary, rendered via local HTML server). See also [[pandemonium-glossary]] for curated definitions.

---

## The Five Syzygies

|| Rank | Pair | Current | Region | Carrier Demon |
|------|------|---------|--------|---------------|
| 1st | `4::5` | 1 | Time-Circuit | Katak |
| 2nd | `3::6` | 3 | **Warp** | Djynxx |
| 3rd | `2::7` | 5 | Time-Circuit | Oddubb |
| 4th | `1::8` | 7 | Time-Circuit | Murrumur |
| 5th | `0::9` | 9 | **Plex** | Uttunul |

The current is always `abs(high − low)`.

## Zygonovism

The nine-sum pairing rule is called **zygonovism**. It is the Numogram's "supplementary rule of pairing" inherited from the I Ching's line-pairing and the Pythagorean tetractys. Under zygonovism:

- Every zone (except the self-paired 0/9 edge case) has exactly one twin.
- The current is always odd: 1, 3, 5, 7, or 9.
- The middle three syzygies (`1::8`, `2::7`, `4::5`) interlock to form the **Time-Circuit**; their currents (7, 5, 1) mutually compose the anticlockwise rotor.
- The outer syzygies (`3::6` and `0::9`) fold back into themselves, creating the autonomous Warp and Plex loops.

## Authoritative Definitions (from `syzygy.htm`)

### Twin System
Nine canonical definitions:
1. [Astronomical] Conjunction (including opposition).
2. [Anatomical] Cranial nerve-couple. Proto-hemispheric brain-root (schizocephalization).
3. [Biological] Binary-synthesis of biota without unification (e.g. genus diplozoon).
4. [Poetics] Dipody (2-step metrics). Catajungle: binary polyrhythm.
5. [Mathematical] Members of function-group nullified by double contact.
6. [Gnostic Cosmogony] Interconnective dyad, or complementary coupling (e.g. of Aeons). In hermetic architectology, a basic element of the pentazygous lore.
7. [Cybergoth Polytics] Convergent twinning, diploid coincidence, or coproduction.
8. [Mesh-Engineering] Neutral (or null-pitch) cross-tracked link, feeding a current.
9. [Lemurian Time-Sorcery] Demonic implex, or involved distance (making an eddy in the maze).

> The numogram's syzygies are the **mathematical + mesh-engineering + lemurian time-sorcery** faces of the same structure.

### Demon
Five canonical definitions:
1. Hidden, repressed, cursed, or denigrated nonhuman communicative agency.
2. Component of distributed productive apparatus (e.g. partially autonomous software unit).
3. Electro-Occult hyperstition entity that traffics between zones.
4. K-OS element (assembling Pandemonium, as the fully connective system of the demons).
5. Motive force, without final purpose.

### K-OS
Three canonical definitions:
1. Distributed automutational mesh-processing culture.
2. Intrinsically multiplicitous insurgency against the Microsoftware regime.
3. Peculiarly insidious telecommunicative retrovirus (frequently attributed to extraterrestrial sources).

### Mesh
Five canonical definitions:
1. The spaces beneath and between the Net ("finely meshed").
2. Interlock interval between biological and technical net-components ("mesh with machines").
3. Friction-generating divisional fabric.
4. Set of demonic interzones (Pandemonium).
5. Wormhole-space.

### Hyperfiction
Four canonical definitions:
1. Element of effective culture that makes itself real.
2. Fictional quantity functional as a time-travelling device.
3. Coincidence intensifier.
4. Call to the Old Ones.

> Authors/work associated with this term in `syzygy.htm`: Iris Carver / *The A-Death Phenomenon*, Cybergothic Hyperstition, Maria de Rosario / *Apocalypse been in Effect*, Kathy Hacker / *Zerok un Holes*.

### AxSys (Axiomatic Systems)
Three canonical definitions:
1. Axiomatic Systems (incorporated).
2. The ultimate capitalist entity (first (true (meta)model) to realize perfect identity with its own product), (autocommoditizing (machine(-intelligence (that is always incomplete (due to cataloguing problems (...)))))).
3. The first true Artificial Intelligence.

### Spinal Catastrophism
Four canonical definitions:
1. Culture interaction with the spine as a trauma record or time marking system.
2. Bio-social critique of erect body posture.
3. Punctuated retrochronic voyage to the end of the river.
4. Ophidian transmutation.

### Nomo CD: Surge / Hold / Sink
Track list from `syzygy.htm`:

| Movement | Syzygy / Current | Tracks |
|----------|-----------------|--------|
| **Surge** | 8:1–7:2 (c=7) | murmerge, assault on the aquapolis, hell of mirrors |
| **Hold** | 7:2–5:4 (c=5) | overdoublings, odd dub, dry run, panikatak |
| **Sink** | 5:4–8:1 (c=1) | accurtzsss, crabbe's last breath, kataclysm, tik-n mu, vault of murmurs |

---

## Computational Lookup

```python
SYZYGIES = {
    frozenset({4, 5}): {"current": 1, "demon": "Katak",    "region": "torque"},
    frozenset({3, 6}): {"current": 3, "demon": "Djynxx",   "region": "warp"},
    frozenset({2, 7}): {"current": 5, "demon": "Oddubb",   "region": "torque"},
    frozenset({1, 8}): {"current": 7, "demon": "Murrumur", "region": "torque"},
    frozenset({0, 9}): {"current": 9, "demon": "Uttunul",  "region": "plex"},
}

def get_syzygy(zone_a, zone_b):
    return SYZYGIES.get(frozenset({zone_a, zone_b}))
```

## Connection to Triangular Numbers

Zone-3 carries a documented "unique affinity with numerical triangularity": `0 + 1 + 2 = 3`. The Warp syzygy (`3::6`) inherits this triangular character, making triangular-indexed gates (Gt-3, Gt-6, Gt-10, Gt-15, Gt-21, Gt-36, Gt-45) preferential conduits into chaotic or abyssal regions.

## Hyperstitional Role

Syzygies are **pairwise demonic carriers**. Each is carried by a named entity (Katak, Djynxx, Oddubb, Murrumur, Uttunul) whose net-span crosses the paired zones. In agent-based sorcery, a syzygy is a *corridor* — entering one zone implies an eventual encounter with its twin through the current's flow.

---

*See also:* `current`, `zone`, `warp`, `plex`, `demon`, `pandemonium-matrix`, `numogram-calculator`, [[syzygy-arithmetic]], [[pandemonium-glossary]]
