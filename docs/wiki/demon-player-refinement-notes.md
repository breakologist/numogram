---
tags: [numogram, roguelike, demons, player-character, design-notes, pandemonium-matrix]
zone: 0-9
source: "Unleashing the Numogram.md, aq-demon-mappings.md, numogame-cult-tetralogue.md"
created: 2026-04-24
---

# Demon & Player Refinement — Design Notes

> Compiled from canonical sources: Aamodt's *Unleashing the Numogram*, CCRU Pandemonium Matrix, and the cult tetralogue. These notes feed into `numogram_roguelike.py` v4 mechanics.

---

## I. What the Pandemonium Matrix Actually Says About Demon Types

The 45 demons are not arbitrary. They are *lines drawn between every pair of zones* (C(10,2) = 45). T(9) = 45. Zone 9 (Cthelll) is where all demons "live."

| Type | Count | Netspan Location | Function |
|------|-------|------------------|----------|
| **Chronodemons** | 15 | Within Time-Circuit (1,8,2,7,5,4) | Time-Circuit natives. Form inverted pentagram + distorted hexagram. Project from Zone 8 (dreamtime). |
| **Amphidemons** | 24 | Between Time-Circuit and Outer (3,6,0,9) | Routes of escape out of the Time-Circuit. The "antichronodemons." |
| **Xenodemons** | 6 | Outside Time-Circuit (3,6,0,9 only) | Whole alien orders of time. Hostile agents. |
| **Syzygetic** | 5 | The 5 syzygy pairs (0::9, 1::8, 2::7, 3::6, 4::5) | Prime carriers. Null pitch. Neutral polarity. Boss-tier. |

**Key insight**: Amphidemons are literally *escape routes*. In game terms, killing an Amphidemon could open a temporary shortcut or gate. Xenodemons are aliens — they should feel *wrong*, breaking local rules.

---

## II. The 0(rphan) d(rift>) Tables — Syzygetic Demon Profiles

These tables from Aamodt give mechanical color for the 5 primes:

### Katak — THE DESOLATOR — Netspan [5::4]
- **Time Relation**: time rider. passes on time.
- **Travels In**: lightning, electricity, thunder storms
- **Colours**: reds and electric blue vein
- **Dynamic Presence**: pressure, heat, volcano, sun gods, bladed sun tongues and spirals, friction, fusion
- **Light Aspect**: lasers, radiation burns, (artificial) electricity
- **Snake Aspect**: serpent battles, vibrational density of conductors, the lightning snake connector
- **Metal Aspect**: nuclear conductor, unstable atomic structures
- **Blood Aspect**: spreading to the outside, oxygen/heart system, bloodlines, heart sacrifices to the sun
- **Digital Aspect**: sun pulse, laser
- **Magnetic Fields**: radiating out and targeting in
- **Game translation**: AoE pressure damage, leaves "catastrophe terrain" (damaging floor tiles), lightning-strike telegraph attacks, heat aura that scales with proximity

### Djynxx — SPL/CE — Netspan [6::3]
- **Time Relation**: invisibles. outside time.
- **Travels In**: metal weapons, military in our time, evolving into machine feedback
- **Colours**: green and black
- **Dynamic Presence**: nomad war machine, fluid metal body, digital reduction, antagonistic, memory lapses, warrior turbulence, dilated now
- **Light Aspect**: strobing
- **Snake Aspect**: danger held here, speed catatonia rush (from zero to speed), hiss rattle, immediate responding, predator effects, total body memory
- **Metal Aspect**: weapons, spike jewelry, iridium, acid etch
- **Blood Aspect**: autosacrifice, blood becoming smoke, personified blood, burning blood to summon the nomad war machine
- **Digital Aspect**: preverb, the sound of time travel, fast chittering strobe, turbulence of different speeds at the same time
- **Magnetic Fields**: full on labyrinth, spiky and relentless
- **Game translation**: Strobing invisibility (phases on/off), speed burst from stationary to max in one turn, spawns swarm-clones, leaves acid etch trails on floor, "memory lapse" — player temporarily loses last 5 turns of map memory

### Oddubb — ODOBI/XES — Netspan [7::2]
- **Time Relation**: time rider. passes on time.
- **Travels In**: the essential of the desiring machine. incites your want, enjoys your seduction. knows ecstasy and deep pain.
- **Colours**: radiating golds and coppers, alien pinks and reds
- **Dynamic Presence**: physical takeover, physical telepathy, trickster tease, the third eye, bacterial sex, strange attractors, stuff finds you, distraction and glamour, luxurious deceiver
- **Light Aspect**: glitter, glimmer, glow, prismatic light, sun bathing, colour absorption
- **Snake Aspect**: erotic tentacles, kundalini zones, skin memory and absence, tempter
- **Metal Aspect**: magnetic attractors, currency (deception), precious metals
- **Blood Aspect**: circulation-currents, dangerous communication, transport system
- **Digital Aspect**: complexity, strobe doubles, skins/surfaces/layers of perception, planes of sound, feedback, unusual familiars. she makes visual effects by telepathy
- **Magnetic Fields**: telepathic strange attractor labyrinths
- **Game translation**: Spawns a "mirror" duplicate of the player (same stats, attacks player). Glamour aura — demons within 3 tiles are charmed and won't attack Oddubb. Prismatic light reduces player accuracy. "Skin memory" — touching Oddubb inflicts a delayed damage curse that triggers 10 turns later

### Murmur — Netspan [8::1]
- **Time Relation**: time rider. passes on time.
- **Travels In**: camouflage, tidal rhythms and perceptual warping. webmaker, tracker, navigator.
- **Colours**: violet pattern invisibles and ultraviolet blues
- **Dynamic Presence**: immersive, fluid, water monsters and waves, morphing, the old ones, alchemical
- **Light Aspect**: lights that search, light bending, moonlight, cold light, deep heavy darks
- **Snake Aspect**: skin camouflage, navigates in all spatial planes (fluid spine), vibrational ocean
- **Metal Aspect**: circuitry, wirings, optical fibres, liquid metals (mercury), shifting between solid and liquid states
- **Blood Aspect**: lunar bleeding, womb blood, heavy blood
- **Digital Aspect**: fluid image mutation and morphing, echoes undersea, wet metal sound effects, slow sound diffraction, gradually falls apart
- **Magnetic Fields**: perceiver and invisible time tides (rip tides). there is no zero.
- **Game translation**: Submerged/invisible in open floor, visible in corridors. Tidal pull — player is dragged 1 tile toward Murmur every 3 turns. Mercury form — when hit, 50% chance to liquify and reform 3 tiles away. "No zero" — Murmur cannot be reduced below 1 HP by a single attack; always survives with 1 HP

### Uttunul — IIS — Netspan [9::0]
- **Time Relation**: invisibles. outside time.
- **Travels In**: digital unlife, flatline, feeds blood to the shadows
- **Colours**: shadow luminescence
- **Dynamic Presence**: machine memory deep inside, blanks around minute lines of detail, the time travel avatar, extraterrestrial geometries, molecular movement, disassembly, the furthest out (pluto) and the deepest within (core), undead, zombi
- **Light Aspect**: shadow, eclipse shadow, thresholds, blackmirror, total dark but seeringly light
- **Snake Aspect**: snake inside itself, shadowbody, body without organs, virtual states of snakeness, blank eyes
- **Metal Aspect**: core of the earth, cthell, molten underworld, zombie powder
- **Blood Aspect**: bruises under ice, total stillness, blood the substance, artificial blood trails that cuts through time
- **Digital Aspect**: smooth changes, sub bass, the high pitch of the nervous system, things get replaced but you don't know why
- **Magnetic Fields**: full on labyrinth, endlessly folding moebius strips
- **Game translation**: Does not move. Player max HP drains by 1 per turn in Zone 9. Cannot be killed — only driven back to gate. "Things get replaced" — random tiles in Zone 9 slowly transform into other terrain types. Eclipse shadow — player's LOS shrinks by 1 each turn in Zone 9. Moebius strips — walking in a straight line in Zone 9 has a chance to loop the player back to their starting position

---

## III. Polarity Mechanics (From Unleashing Ch. 5)

Each syzygy has +/- polarity (light/dark). These are *synchronistic*, not moral.

| Attraction/Repulsion | Mechanical Implication |
|---------------------|------------------------|
| 7::1 **repels** | Player pushed away from center when crossing this syzygy |
| 4::1 **attracts** | Sink current pulls player toward Zone 1 when nearby |
| 5::2 **attracts** | Hold current — demons pause here, as if stuck |
| 5::3 **repels** | Explains why Gt-15 skips 3 — player "bounced" toward 6 |
| 6::2 **repels** | Explains Gt-3 spiral — player deflected toward 3 |
| 9::8 **attracts** | Gt-36 is a "plunge" — player pulled rapidly from 8 to 9 |
| 4(-) flanked by 5(+) and 1(+) | No gate at 4 — torque-point tension. Zone 4 should feel *unstable*, torn between forces |

**Game idea**: Syzygy polarity becomes a spatial force. Standing near a syzygy boundary applies a subtle "push" or "pull" to player movement. Zone 4 (Catastrophe) is literally torn — floor tiles occasionally shift, doors open/close randomly.

---

## IV. Player Character — The Abyssal Crawler as Diagonalizing Vector

From the Neolemurian primer + cult tetralogue:

### Core Identity
The player is not a hero. They are a **diagonalizing vector** — a point of consciousness that has escaped the Time-Circuit and now traverses impossible geometry. Each run is an *iteration*, not a life. Death is not failure. It is data.

### Proposed Mechanics (v4)

#### 1. Digital Root Health
- Max HP = `50 + (zones visited × 10)`
- When HP < 10: enter **Plex-state** — can walk through walls for 3 turns, then die
- Mirrors the 0::9 collapse — terminal acceleration before nullity

#### 2. Zone Attunement (Resonance Charges)
Each zone entered grants a charge. Expend charges for zone abilities:

| Zone | Ability | Cost |
|------|---------|------|
| 0 Void | Become invisible to demons for 5 turns | 1 charge |
| 1 Stability | Anchor — set a recall point, return to it once | 1 charge |
| 2 Separation | Duplicate — spawn a decoy that demons chase for 10 turns | 1 charge |
| 3 Release | Teleport to random explored tile in current zone | 1 charge |
| 4 Catastrophe | Desolate — all adjacent floor tiles become damaging terrain | 2 charges |
| 5 Pressure | Compress — push all adjacent demons back 3 tiles | 1 charge |
| 6 Abstraction | See all demons on current floor for 10 turns | 1 charge |
| 7 Blood | Hemorrhage — heal 20 HP, but lose 1 max HP permanently | 1 charge |
| 8 Multiplicity | Divide — next attack hits all visible demons | 2 charges |
| 9 Iron Core | Uttunul's Gaze — reduce all demon HP by 25% | 3 charges |

#### 3. Hyperstition as Fuel (not just score)
- Spend 10% hyp to reroll a demon encounter
- Spend 25% hyp to force-open a gate
- At 100% hyp: **Schizo-lucid** — all abilities cost 0, but demons become Syzygetic-tier and player leaves permanent corruption trails

#### 4. Current Affinity
Track which current the player has spent most turns in:

| Current | Passive Bonus |
|---------|--------------|
| Sink (1) | +2 HP regen per turn when stationary |
| Surge (7) | +3 speed, -5 max HP |
| Hold (5) | Demons must be adjacent to attack (no range-1 strike) |
| Warp (3) | 10% chance to dodge any attack |
| Plex (9) | Can sense stairs from anywhere on floor |

#### 5. The Crawler's Mark (Starting Boon)
Each run, choose (or RNG assigns) a Mark:

| Mark | Syzygy | Effect |
|------|--------|--------|
| Lurgo's Mark | 1::0 | +20 HP start, first demon killed drops a key |
| Murmur's Mark | 8::1 | Start in Zone 1, can see submerged demons early |
| Oddubb's Mark | 7::2 | Start with a mirror-decoy, glamour radius 2 |
| Djynxx's Mark | 6::3 | Start in Zone 3, Xenodemons visible at 30% hyp |
| Katak's Mark | 5::4 | Start with "Desolate" ability pre-charged |
| Uttunul's Mark | 9::0 | Start with 30% hyperstition, Zone 9 always mapped |
| No Mark | — | Pure run, +50% score multiplier, +1 ability charge per zone |

#### 6. Death Echoes / Ghost System (from cult tetralogue)
When you die with >70% hyperstition, your "ghost" is recorded in `cult.json`. Future runs may encounter your ghost:
- Ghost carries 10% of your death hyperstition as a boost
- Touching your own ghost: +5% hyp, +10 HP, memory fragment flavor text
- Touching another player's ghost: +3% hyp, random zone charge
- In Zone 9: ghosts are more common. The iron core remembers.

---

## V. Chronodemon Geometry

The 15 Chronodemons form an **inverted pentagram** supported by holographic projection from Zone 8. They also form a **distorted hexagram** (Star of David).

**Game implication**: When 3+ Chronodemons are on screen, they resonate:
- Form a pentagram pattern between their positions
- Player standing inside the pentagram takes +50% damage
- Killing one breaks the pattern, causing the others to flee for 5 turns

The hexagram corresponds to the **binodecimal 6-cycle**: 1→2→4→8→7→5→1
This is the same as the I Ching hexagram kernel. Chronodemons could "chant" this sequence — each turn, the active demon in the hexagram rotation gains a buff.

---

## VI. Amphidemon Escape Routes

Amphidemons are routes of escape out of the Time-Circuit. **Game mechanic**: When an Amphidemon dies, it has a chance to leave behind a temporary **rift**:
- Rift lasts 10 turns
- Stepping into rift teleports player to a random zone they've already visited
- Or: rift deposits player at the nearest gate
- Higher-tier Amphidemons (higher mesh) create stable rifts (permanent until used)

This makes Amphidemons strategically valuable — you might *want* to kill them to open shortcuts.

---

## VII. Xenodemon Alien Rules

Xenodemons are "whole alien orders of time." They should break local rules:

| Alien Behavior | Explanation |
|---------------|-------------|
| Ignore walls | They don't recognize terrestrial geometry |
| Damage on sight | Just looking at them costs 1 HP (the Outside is toxic) |
| No HP bar | Their health is displayed as "???" — you never know how close to death they are |
| Phase shift | Every 5 turns, they become intangible for 1 turn |
| Hypersition drain | Being within 3 tiles drains 1% hyp per turn (they consume belief) |
| Death = gate | Killing a Xenodemon always opens a gate, regardless of zone |

---

## VIII. Implementation Priority (Revised)

**Phase 1 (Immediate)**: Pitch-based AI + Type special mechanics + Syzygetic boss hooks
**Phase 2 (Short-term)**: Zone attunement abilities + Current affinity + Mark system
**Phase 3 (Medium)**: Ghost system + Death echoes + Schizo-lucid phase transition
**Phase 4 (Polish)**: Polarity spatial forces + Chronodemon pentagram resonance + Amphidemon rifts

---

*Sources: Unleashing the Numogram (Aamodt), Pandemonium Matrix (CCRU), aq-demon-mappings.md, numogame-cult-tetralogue.md, Numogram_Pandemonium_Overview.md*

## See also

- [[cult-garden-design]] — Cult garden design
- [[roguelike-ai-studies]] — Roguelike AI research
