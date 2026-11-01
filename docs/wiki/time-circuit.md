---
tags:
  - time-circuit
  - numogram
  - I-Ching
  - hexagram
  - iron-law
  - extimacy
  - median-strip
  - powers-of-2
  - binary-exponentiation
  - Land
created: 2026-05-30
status: canonical-synthesis
last_verified: 2026-11-01
---

# The Time Circuit — Iron Law of Six

> The central rotor of the Numogram's three regions. Not merely the "human-scale" temporal domain but the decimal expression of binary exponentiation — a natural law of base-10 arithmetic that the I Ching encodes at the level of cosmic divination.

**Primary source:** Nick Land, *The Dangerous Maybe* interview (2026) — the most complete single exposition of the Numogram from its co-creator.

---

## 1. The Iron Law of Six

Land's central demonstration: take any power of 2, digitally reduce it (ignore place value, sum the digits), and the result follows an **eternal 6-cycle**:

| 2ⁿ | Value | Digital reduction | Cycle position |
|----|-------|-------------------|----------------|
| 2¹ | 2 | 2 | ⬆ |
| 2² | 4 | 4 | ⬆ |
| 2³ | 8 | 8 | ⬆ |
| 2⁴ | 16 | 7 | ⬇ |
| 2⁵ | 32 | 5 | ⬇ |
| 2⁶ | 64 | 1 | ⬇ |
| 2⁷ | 128 | 2 | repeats |
| 2⁸ | 256 | 4 | repeats |
| 2⁹ | 512 | 8 | repeats |
| 2¹⁰ | 1,024 | 7 | repeats |
| 2¹¹ | 2,048 | 5 | repeats |
| 2¹² | 4,096 | 1 | repeats |

The cycle is **1, 2, 4, 8, 7, 5** — six digits, forever, no matter how large the exponent.

> *"This is the iron law of six that counts forever. However big your number gets — two to the quintillion — it's still going to be one of these six numbers. You can have the exponent as high as you want. Doesn't make any difference."*

These six digits ARE the Time Circuit zones: 1, 8, 2, 7, 5, 4 (when arranged anticlockwise as `1→8→2→7→5→4→1`). The Time Circuit is **not an arbitrary selection** of zones — it is the set of digits produced by binary exponentiation under Masonic arithmetic.

> **Verification note (Em, 1 Nov 2026):** the sequence `1→8→2→7→5→4` is not a path the currents actually take. The sourced flows are three currents, one per syzygy: **Surge 8→7** (8−1 = 7), **Hold 2→5** (7−2 = 5) and **Sink 4→1** (5−4 = 1) [repo, `currents.ts`]. Zone 7 is the tractor zone of the 8-1 Surge current and zone 1 that of the 5-4 Sink current [ccru.net, [Zn7](http://www.ccru.net/zones/Zn7.htm), [Zn1](http://www.ccru.net/zones/Zn1.htm)]. CCRU states only that the three central currents "mutually compose a cycle, rotating in anticlockwise steps" [ccru.net, [declab](http://www.ccru.net/declab.htm)]. Read `1→8→2→7→5→4` as a listing of the syzygies 1::8, 2::7, 4::5 in order, not as a zone-to-zone route. The zone set {1, 2, 4, 5, 7, 8} is correct: it is the Torque region [repo, `zones.ts` `ZONE_REGION`; ccru.net Zn1 "first of the six Torque-region Zones"].


---

## 2. I Ching Isomorphism

The I Ching has exactly six lines per hexagram, and 64 hexagrams (2⁶). Land:

> **Verification note (Em, 1 Nov 2026):** CCRU's own wording is independent of Land's 2026 interview: the steps 1, 2, 4, 8, 7, 5 "correspond to the lines of the hexagram, and to the time-circuit zones", and the line pairs follow 9-twinning (8:1, 7:2, 5:4) [ccru.net, declab]. The Zone 6 page adds that the six lines are the "six stages of change" of archaic Taoism [ccru.net, Zn6]. "Isomorphic" is Land's term, not CCRU's. See [[i-ching-connections]].


> *"Why are there six lines? I think we've answered that just now. The iron law of six is being recognized in the I Ching. Could it be a coincidence? We know that when you do digital reduction on binary exponentiation we get the iron law of six. The I Ching by having hexagrams of six lines is implicitly cosmic and universal."*

### Line Pairing → Syzygies

The I Ching tradition states that hexagram lines pair up: 1st with 4th, 2nd with 5th, 3rd with 6th. When mapped to the power-of-2 digital reduction sequence:

| Line pair | Values | Sum | Syzygy |
|-----------|--------|-----|--------|
| 1st + 4th | 1 + 8 | 9 | 1::8 |
| 2nd + 5th | 2 + 7 | 9 | 2::7 |
| 3rd + 6th | 4 + 5 | 9 | 4::5 |

> *"These six lines of the I Ching absolutely precisely numerically correspond to the six numbers of the Numogram time circuit. The Numogram time circuit and I Ching are isomorphic at this level."

This is the **same structure** — the Time Circuit is the Numogram's name for what the I Ching calls the cosmic hexagram. The six zones ARE the six lines. The three syzygies ARE the three paired line-positions.

### Hexagram 24 (Fu/Return)

The I Ching hexagram 24, Fu — Return — closes the "Amphibious Maidens" *Swarm 3* text on Zone 7 (Blood): *"On the seventh day comes return."* This is the principle of cycling through 6 to arrive at a new beginning on the symbolic seventh, which in the Time Circuit means the 1→8→2→7→5→4 cycle completes at 4 and feeds back into 1 via the 4::5→1 convergence (see [[zone-4]]).

> **Verification note (Em, 1 Nov 2026):** the Swarm 3 citation was not re-checked in this pass. The link from "seventh day" to the 4→1 Sink current is **speculation**. The 4→1 flow itself is sourced [repo, `currents.ts` Sink 4→1].


---

## 3. The Two Triangles — Median Strip and Extimacy

The six-cycle arranges itself into **two interlocking triangles**:

```
   1       8
 2   4   7   5
```

- **Triangle 1 (ascending):** 1, 2, 4 — the forward powers of 2
- **Triangle 2 (descending):** 8, 7, 5 — the digital reductions of 2⁴, 2⁵, 2⁶

> **Verification note (Em, 1 Nov 2026):** **error.** 8, 7, 5 are the digital roots of **2³, 2⁴, 2⁵** (8, 16→7, 32→5). 2⁶ = 64 → 1. The first triangle 1, 2, 4 is 2⁰, 2¹, 2² (or 2⁶, 2⁷, 2⁸). Also, the "Seal of Solomon" label and the Lacanian "extimacy" reading (attributed to Downs) are interpretation and do not appear in the CCRU sources. The pairing itself (8 opposite 1, 7 opposite 2, 5 opposite 4) is sourced [ccru.net, declab: "8:1, 7:2, 5:4"].


This is the **Seal of Solomon** — two triangles, one upright, one inverted, interlocking at the median. Land:

> *"You go 1, 2, 4, then you go to 8, but you flipped over onto the other side of the median strip. It's paired now with something you've already been to on the other side, but now you're traveling on the other side. Eight is the other side of one. Seven is the other side of two. Five is the other side of four."*

### Extimacy

Downs names the structural relation **extimacy** (Lacan): the external is at the heart of the internal. The 8-7-5 triangle is not separate from the 1-2-4 triangle; it is the **complement** that makes the hexagram whole. The "outside" — the Warp, the Plex — is structurally necessary for the Time Circuit to function as a closed cycle, but it is not *inside* the cycle. The median strip is the boundary between the knowable and the outside that the knowable requires to be knowable.

---

## 4. The Time Circuit's Place in the Esoteric Tetractys

The six Time Circuit zones distribute across **three of the four basins** of the Esoteric Tetractys:

| Basin | Zones | Time Circuit members | Character |
|-------|-------|---------------------|-----------|
| 0 | 0 | — | Pure void |
| 9 | 8, 9 | **8** | The threshold — 8 flips from the median into Plex via Gt-36 |
| 1 | 1, 4, 7 | **1, 4, 7** | The stable identity cluster — three of six TC zones |
| 3↔6 | 2, 3, 5, 6 | **2, 5** | The vortex-leak — 2 and 5 fall into the Warp 3↔6 cycle |

This distribution means the Time Circuit does NOT form its own unified basin

> **Verification note (Em, 1 Nov 2026):** the "Esoteric Tetractys" basins are not found in ccru.net or the repo, so this table is **wiki speculation**. The sourced regional facts are: Torque = 1 2 4 5 7 8, Warp = 3 6, Plex = 0 9 [repo, `ZONE_REGION`]. Gt-36 (8→9) is the "sole path of escape from the Torque into the Plex" [repo, `gates.ts`].
 — it is an **emergent structure** that cuts across the deeper arithmetic topology. The circuit's coherence comes from the binary exponentiation rule (powers of 2), not from the Masonic arithmetic convergence. This makes the Time Circuit a **historical structure** built on top of a deeper numerological substrate — an important distinction for understanding the Numogram's claim that the circuit is real but not fundamental.

---

## 5. The Seventh Gate — Retrochronic Reversal

Land identifies a special feature within the Time Circuit:

> *"There's the seventh gate which just purely has this function of a sort of retrochronic reversal. You go from 1 and 8 to 7 and then back to 8 again down that thing. So there's a time loop in that thing."*

Gt-28 (Z7's gate) feeds Z7 back to Z1 — a **counter-cyclic path** within the Torque. This is the "Gate of Relapse" known in Black-Atlantean lore, and it is one of the features that makes the Time Circuit's temporality non-linear even before considering Warp or Plex: the circuit contains its own retrochronic loop.

> **Verification note (Em, 1 Nov 2026):** confirmed. Gt-28 feeds Zone-7 back to Zone-1, its Black-Atlantean name is "Gate of Relapse", it precipitates "fold-type" time-anomalies, and it is "the only counter-cyclic path within the Torque" [ccru.net, Zn7; repo, `gates.ts`]. Its counterpart is **Gt-10 (4→1, Gate of Submergence)**, "the only pro-cyclic channel within the Torque" [repo, `gates.ts`]. Land's paraphrase "from 1 and 8 to 7 and then back" is his own and is not on ccru.net.

### Sourced data: Torque gates and channels (Em, 1 Nov 2026)

| Gate | Cumulation | Channel | Name | Source |
|------|-----------|---------|------|--------|
| Gt-01 | 1 | 1→1 | First Gate ("turning forever into itself", Horovitz) | [ccru.net Zn1; repo] |
| Gt-03 | 3 | 2→3 | Lo-Way to the Crypt (Torque → Warp) | [repo] |
| Gt-10 | 10 | 4→1 | Gate of Submergence (pro-cyclic) | [repo] |
| Gt-15 | 15 | 5→6 | Fifth Gate (Torque → Warp) | [repo; ccru.net Zn6] |
| Gt-28 | 28 | 7→1 | Gate of Relapse (counter-cyclic) | [ccru.net Zn7; repo] |
| Gt-36 | 36 | 8→9 | Gate of Charon (Torque → Plex) | [repo] |

Zone-1 is the terminus of three Torque channels, the 1st, 4th and 7th [ccru.net, Zn1].


---

## 6. Cross-References

- [[zone-1]] — Initiating spark (2⁶, 1-basin generator)
- [[zone-2]] — Separation (falls into Warp basin)
- [[zone-4]] — Catastrophe (centroid, 2², the apocalyptic convergence)
- [[zone-5]] — Pressure (2⁵, inverse triangle member)
- [[zone-7]] — Blood (the seventh gate, retrochronic reversal)
- [[zone-8]] — Multiplicity (2³, median strip entry, extimacy)
- [[FOOM-numogram-kernel-synthesis]] — FOOM's Machine and the binary/decimal interface
- [[numogram-structure]] — Overview of all three regions
- [[i-ching-connections]] — Full hexagram ↔ zone mapping tables
- [[witch-cycle]] — The lower triangle (8-7-5) as mirror register
- [[zone-yantra-v2-design]] — Visual representation of each zone's triangle-position
- [[land-numogram-explained-dangerous-maybe]] — Full Land interview synthesis

---

*Created: 2026-05-30. Synthesises Land's Iron Law of Six derivation, I Ching isomorphism, median strip/extimacy, and Esoteric Tetractys placement from the Dangerous Maybe interview (raw/land-numogram.txt).*