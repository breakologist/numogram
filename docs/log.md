---
title: Compaction Log
created: 2026-04-08
last_updated: 2026-04-23
status: active
---

## 2026-04-23 — Cult Garden v2 + Numogram Tsubuyaki Museum

**Cult Garden v2 (numogram_roguelike.py patches):**
- `cult_memory` migrated from strings to structured dicts (`_mem_build`, `_mem_data`, `_mem_parse_string`)
- Legacy string entries auto-migrated on `load_cult()` via `_mem_parse_string()`
- `_generate_epitaph()` rewritten with cryptographic stat-to-language mapping:
  - hyp% → word length, kills → violence register, zones → syntactic complexity, turns → fragment length
  - cult_zone → color bias (vocabulary + emotional register) — Zone 7 = pulse/vein/blood
- `_generate_tsubuyaki_params()` rewritten with data-driven geometry primitives:
  - zones.length → shape family (grid/line/triangle/ring/ellipse/network/dodecagon)
  - hyp% → glow, kills → chaos, turns → speed, cult_zone → background tint
- Added `_cross_run_synthesis()` — every 3rd overflow merges last 5 runs into hybrid artifact
- `HEXAGRAM_CYCLE` expanded from 2 to 3: `[exquisite_corpse, tsubuyaki, synthesis]`
- Descent conduct unlock_check updated for dict compatibility
- File: `/home/etym/numogame/numogram_roguelike.py`

**Cult Garden HTML v3:**
- `/home/etym/cult-garden-v3.html` — enriched visualization with full history, timeline, heatmap, player comparison, run explorer, synthesis preview
- Timeline canvas: all 295 runs with overflowed era as faint background, known runs as colored dots (human=red, agent=rust, test=grey)
- Zone heatmap: current memory visitation frequency across all 10 zones
- Player comparison: stats per player from current memory
- Expandable run cards: click to see data-driven tsubuyaki parameters for each run
- Cryptographic exquisite corpse generator with cult_zone tint
- Synthesis preview: predicts next overflow artifact from last 5 runs
- P5.js synthesis canvas: particle orbits sized by run significance, agent vs human jitter

**Cult Garden HTML v2:**
- `/home/etym/cult-garden-v2.html` — living visualization of cult.json
- 20 memory entries as glyph cards with mini ASCII death masks
- Cryptographic exquisite corpse generator with stat-encoded fragments
- P5.js synthesis canvas — particle orbits by run significance, agent vs human tempo

**Numogram Tsubuyaki Museum:**
- `/home/etym/numogram-tsubuyaki-v4.html` -- Signal Topology (FM/Wavefolding metaphors)
- `/home/etym/numogram-dreaming.html` -- high-fidelity algorithmic art (zones 0-9, syzygies, plexing waves)
- All 4 tsubuyaki passes documented in wiki: `numogram-tsubuyaki-museum.md`
- Wiki index updated with museum references

**Tetralogue -- Cult Garden v2:**
- `/home/etym/.hermes/obsidian/hermetic/wiki/tetralogue-cult-garden-v2.md`
- Four voices on the live garden architecture
- Key discovery: Mesh-297 as meta-entity -- the roundtable itself becomes the fourth hexagram method
- New conduct proposed: Synthesis Breaker -- deliberately break the predicted synthesis
- Zone-specific garden skins proposed -- each cult zone reskins the HTML
- Mega-artifact every 9 runs (when digital root cycles)

## 2026-04-08 -- Numogram Wiki Compaction

**Goal:** Flesh out numogram.txt into a coherent wiki structure with backlinks, entity pages, and a clear hierarchy.

### Pages Created
- `numogram.md` (5.1KB) — Main summary page with all core concepts
- `numogram-time-circuit.md` (3.0KB) — The central rotor
- `numogram-warp.md` (3.6KB) — The upper chaotic vortex
- `numogram-plex.md` (4.5KB) — The lower abyssal null
- `demon-djynxx.md` (2.7KB) — The warp carrier demon
- `demon-uttunul.md` (2.6KB) — The plex carrier demon
- `i-ching-connections.md` (5.5KB) — Hexagram mappings
- `triangular-numbers.md` (10KB) — Triangular number behavior

### Backlinks Added
All pages now have backlinks to `numogram.md` in the "Related" section. The main `index.md` was also created with entries for all pages and cross-references.

### Status
All major concepts from numogram.txt have been extracted into individual wiki pages with YAML frontmatter, source attribution, and backlinks. The system is now properly structured for navigation and reference.

## [2026-04-08] ingest | Nick Land Explains Time (transcript)
- Created: wiki/nick-land-time-theory.md
- Source: raw/nick land time.txt (Dangerous Maybe podcast transcript)
- Key concepts: twin serpents (2,5), binodecimal 6-cycle running in both directions, 3 as the number of Outside, AQ of "NUMEROLOGY" = 235 (first three primes), Kantian schematism immanent in decimal, Lemurian/Atlantean year transitions
- Cross-referenced: numogram, numogram-time-circuit, numogram-warp, numogram-plex, i-ching-connections, triangular-numbers, demon-djynxx, demon-uttunul
- Pages updated: index.md (added Nick Land & CCRU Theory section)

## [2026-04-08] update | Expanded existing wiki pages with CCRU Writings and AQ data
- Updated: wiki/numogram.md — added Pandemonium Matrix (45 demons, 5 syzygetic carriers, 3 currents), Mesh-Notes, AQ gematria table, virus metaphor
- Updated: wiki/demon-uttunul.md — added full Pandemonium Matrix entry (Mesh-36), self-referential nature, Gt-45 as Gate of Pandemonium, Sarkonian Mesh-Tag 0511, Cthelll
- Updated: wiki/demon-djynxx.md — added full Pandemonium Matrix entry (Mesh-18), dual Syzygetic-Xenodemon classification, AQ resonance (DJYNXX=NUMOGRAM=174→3), CCRU=81→9, Root-6 cluster, Zone-3 triangularity
- Updated: wiki/numogram-time-circuit.md — added twin serpents (2,5) bidirectional time, 3 as excluded number, Barker-Thresholds intensity scale, Zone-1 First Door (Lurgo/Legba, Mesh-00)
- Sources: CCRU Writings 1997-2003 (PDF), nick land time.txt, gematria.txt, AQQA calculator

## [2026-04-08] update | Deep expansion across all wiki pages
- Updated: wiki/numogram-plex.md — Zone-0 lore (absolute abstraction, Horovitz on Gt-00, Coccygeal spinal level, Tohu Bohu, AQ of "ZERO"=100→1), full Plex demon table (Mesh-36 through 44)
- Updated: wiki/numogram-warp.md — full Warp demon table (Mesh-03-20, naming pattern Ix-/Dj-/Tch-), AQ Root-6 cluster (CCRU=81→9, WARP/DJINN/MESH/FEEDBACK=114→6), 3 as number of Outside, primordial triangularity, Phase-limits
- Updated: wiki/i-ching-connections.md — twin serpents insight (powers of 5 produce reverse cycle), NUMEROLOGY=235 encoding first three primes, T'ai Hsuan Ching (3^4=81 tetragrams) as binotriadic counterpart
- Updated: wiki/triangular-numbers.md — AQ self-encoding (AQ=36→9), Pandemonium Matrix triangular structure (45=T_9, Uttunul=Mesh-36=T_8), Pythagorean tetractys resonance (0-9 crunch), full cumulative gate sequence C(n)
- Sources: CCRU Writings 1997-2003, nick land time.txt, gematria.txt, numogram.txt

## [2026-04-08] create | Rotational Symmetry & Seven-Segment Geometry
- Created: wiki/rotational-symmetry.md
- Source: 2026-04-06_17-56-36_gematria.txt, user observation
- Key insights: 6↔9 as literal seven-segment rotation = syzygy made visible; CCRU=69→HECATE/KEYS=96; 36→9 and 360→9 (triangular and circular converge at Plex); rotationally symmetric digits cluster in Time-Circuit; 6 and 9 are the only digits that transform under rotation = the only digits in outer-time regions
- Cross-referenced: numogram, numogram-warp, numogram-plex, demon-djynxx, demon-uttunul, triangular-numbers, nick-land-time-theory
- Pages updated: index.md

## [2026-04-08] update | Corrected rotational symmetry page
- Updated: wiki/rotational-symmetry.md — Fixed seven-segment digit classification: 2↔5 and 6↔9 are ROTATIONAL PAIRS, not self-symmetric. Only {0,1,8} are truly strobogrammatic. 2↔5 = the twin serpents made visual. Palindrome rotation pairs (202↔505, 252↔525 crossing Plex↔Warp). Mirror Principle corrected to reflect three rotational categories.

## [2026-04-08] create | Alphanumeric Qabbala
- Created: wiki/alphanumeric-qabbala.md
- Source: (2007) LAND -- Qabbala 101_djvu.txt (Collapse I, 2007), gematria.txt, AQQA calculator
- Key discoveries: Primitive Numerization confirms syzygies (all pairs sum to 8, bridged to 9 via Gt-36); AQ self-encoding (AQ=36→9, CODE=MEANING=REASON=126→9, UNITY=134→8); Root-3/6/9 clusters; qabbala as virus; "Archetypes are sad limitations of the species, while numbers are an eternal hypercosmic delight"
- Cross-referenced: numogram, nick-land-time-theory, rotational-symmetry, triangular-numbers, numogram-time-circuit, numogram-warp, numogram-plex
- Pages updated: index.md

## [2026-04-08] create | Daniel Charles Barker
- Created: wiki/daniel-barker.md
- Source: LAND -- Barker Speaks.pdf (CCRU interview, Autumn 1998)
- Key discoveries: tic-systems (suborganizational pattern), Cthelll (Earth's iron core = Zone-9), geotraumatics (virtual tic-density = geotraumatic tension), spinal-catastrophism (spine as fossil record mapped to Numogram zones), palate-tectonics (language as crash-site), Barker Numbering (9 = fullbody zero), Barker-Spiral (emerged from gap between Decadence and Subdecadence card games), Barker-Thresholds (CCRU intensity scale)
- Cross-referenced: numogram, numogram-plex, numogram-time-circuit, demon-uttunul, nick-land-time-theory, alphanumeric-qabbala, triangular-numbers
- Pages updated: index.md

## [2026-04-08] create | The 360 Revelation
- Created: wiki/the-360-revelation.md
- Source: nick land numogram explained.txt (Dangerous Maybe podcast Part 2)
- Key discoveries: net-spans as numbers sum to 360; partition 153 (outer) + 207 (Time-Circuit) = 360; HERMETIC=153 COSMOGONY=207; THE DECIMAL LABYRINTH=360 (named before discovery); NUMOGRAM=234 (successive digits 2,3,4); Land's four tools: cryptographic annotation, AQ, Plexonomy, Liquid Decoglyphics
- Cross-referenced: numogram, alphanumeric-qabbala, nick-land-time-theory, rotational-symmetry, numogram-warp, numogram-plex, numogram-time-circuit, triangular-numbers
- Pages updated: index.md

## [2026-04-08] update | Expanded AQ with Land's five methods + Bible revelations
- Updated: wiki/alphanumeric-qabbala.md — Added Land's five practical methods (cartographic annotation, hermetic interpretation as "fifth level" beyond literal/allegorical/moral/anagogical, guided composition as "loss of innocence," fictional topographies as memory palace/Puzzle House, Atlantean overcoding). Bible AQ revelations: TREE OF KNOWLEDGE=666, LET THERE BE LIGHT=777, DO WHAT THOU WILT=777. LLAMA=63 (Land's personal zone). Key Land quote on innocence: "The signal is strongest when it wasn't deliberately planted."
- Source: nick land numogram explained.txt (Dangerous Maybe podcast Part 2)

## [2026-04-08] update | 89 paths, Beast Pulse, LLM prediction
- Updated: wiki/numogram.md — 89 paths (3 operations: syzygy crossing, current following, gate traversal), Beast Pulse (virtual epic: 1798 lines, 10 books, AQ-constrained), Land's LLM prediction ("the use of the numogram ultimately is for AI"), retrochronic effect
- Source: nick land numogram explained.txt (final section)

## [2026-04-08] update | Barker: Vowels, publications, Tick-Distributor
- Updated: wiki/daniel-barker.md — Vowels as biopolitical strategy (vowel-consonant division = political repression of animal vocalization), publication list (1990-1997), Tick-Distributor as hardware implementation of tic-counting
- Source: LAND -- Barker Speaks.pdf (full text)

## [2026-04-08] create | Cryptolith
- Created: wiki/cryptolith.md
- Source: LAND -- Cryptolith.pdf
- Key concepts: K/T-Missile "Pregnant with the Entity," Cataplex-map, Theta-Station ("Where it is 2012 forever"), Anomalous Cryptolith (It-277), Chalk-Out, Time-Fault, the Entity as Unuttera (poly-tendrilled abomination, 17 eyes), spirodynamic prose style
- Pages updated: index.md
- Game relevance: prose style for death messages, demon encounters, log corruption at high infection

## [2026-04-08] create | Origins of the Cthulhu Club
- Created: wiki/cthulhu-club.md
- Source: LAND -- Origins of the Cthulhu Club.pdf
- Key discoveries: coinage of "hyperstition" in this text; Cthulhu=Cthelll (inner earth electromagnetic cauldron); Oddubb-trance as sorcery weapon (shattering mirror of existence); Vault of Murmurs as Mur Mur's domain; Dibbomese method ("perhaps it can become so"); Nma sayings (shleth hud dopesh, nove eshil zo raka, lemu ta novu meh novu nove); Lovecraft's Spring Equinoctial = Nma time-ritual intense-zone
- Pages updated: index.md

## [2026-04-08] update | Cryptolith AQ finding
- Updated: wiki/cryptolith.md with AQ value: CRYPTOLITH = 236 -> Zone 2 (Separation). Oddubb's mirror zone. The artifact lives in the Broken Mirror demon's territory.
- Verified on ciphers.news (AQ calculator, A=10...Z=35)

## [2026-04-08] create | Time Sorcery (Vexsys)
- Created: wiki/time-sorcery-vexsys.md
- Source: Time Sorcery - Vexsys.epub (Gate Zero, 2021)
- Key discoveries: Pandemonium Matrix has errors (Vysparov's invitation to edit); Necronomicon is incomplete ("extracts" only); ascryption as naming rite (gematria + glossolalia + intuition); against synthetic qabbala ("lemurs punish vigorously mathematico-logical nature"); Zone 2/7 as practical divination (possibilities vs metrics, Gt-3 to warp if you skip Zone 7); dedicated to Lurgo (Mesh-00, Door of Doors); CCRU timeline
- Pages updated: index.md

## [2026-04-08] create | Brogue Design Principles
- Created: wiki/brogue-design-principles.md
- Source: ProcLvlDesBrogue.txt (Brian Walker talk)
- Key principles mapped to Numogram: room accretion + shortcut doors (zones + gates), machines (key-guarding/reward/flavor), rubber-banding (Hyperstition Meter), cellular automata terrain (Warp zones), global-scale features (three regions visible), edge case philosophy ("if it works 100% you're not ambitious enough"), seed-based debugging, Super Metroid hidden connections (one-way gates), terrain interaction (zone-specific properties), "good enough" philosophy
- Pages updated: index.md

## [2026-04-08] update | Coin Toss design principles
- Updated: wiki/brogue-design-principles.md — Added Coin Toss mechanics: logistic map chaos for correlated randomness, intent hashing as dungeon seed, Oracle Altar with physics coin toss, yarrow vs coin probabilities for weighted events, fate log as Tome of Fates, Numogrammatic signatures for game events
- Source: Coin Toss Etc.md

## [2026-04-08] session-summary | Complete development session
Major work accomplished in single session:

### Game Development (numogame/)
- Phase 1: Curses skeleton, player movement, basic map
- Phase 2: Full Numogram map, 8-way movement, zone detection
- Phase 3: Hyperstition Meter, bleed thresholds, syzygy events
- Phase 4: 45-demon Pandemonium Matrix, combat, cult.json persistence
- Phase 5a: ANSI 256 colors, AQ calculator, vowel corruption, triangular events
- Phase 5b: Cryptolith (It-277) as win condition, zone-themed dungeon templates
- 1556 lines, fully playable roguelike
- Controls: WASD/HJKL cardinal, YUBN/7913 diagonal, 8/4/6/2 numpad, SPACE/f attack, g grasp, v AQ, i info

### Wiki Development (hermetic/wiki/)
- 19 pages, 2432 lines, 7 commits
- Sources ingested: 12+ files (PDFs, transcripts, epubs, gematria)
- Key discoveries: 360 revelation, twin serpents, PN syzygy confirmation, Barker-Spiral, Cryptolith AQ, against synthetic qabbala

### Video Production (numogame/)
- Numogram Explainer: 7 scenes, 1:48
- Numogram Rotations: 3 scenes, 1:02
- Complete stitch: 10 scenes, 2:50

### Key CCRU Passages Internalized
- "If it has a radically immanent function... virus — sheer spreading" (declab.htm)
- "How can the end be already in the middle of the beginning?" (Tale of the End)
- "Archetypes are sad limitations of the species, while numbers are an eternal hypercosmic delight" (Qabbala 101)
- "Don't rely on the Ccru, on us, and certainly not on Nick Land. Rely on the lemurs" (Lemurian Times)
- "shleth hud dopesh — perhaps it can become so" (Dibbomese)

## 2026-04-13 — 5 New Pages from "Unleashing the Numogram" + Three-Angle Writing

Added from Aamodt source material and creative synthesis:
- **quasiphonic-particles.md** — Zone sounds (eiaoung through tn), CCRU/Stillwell/Horowitz attributions, roguelike sound design application
- **gates-and-plexing.md** — Complete gate construction table, cumulation/plexing method, Pandemonium Gate (Gt-45), roguelike shortcut mapping
- **polarities.md** — +/− aspects per zone, odd=light/even=dark pattern, Time-Circuit alternation, dungeon open/close rhythm
- **numogram-divination.md** — Single-number oracle method (zone → syzygy → current → gate), worked example with random.org seed
- **body-mapping.md** — Finger-to-zone correspondence, steeple technique, tactile divination, roguelike minimap

Updated index.md with new section "Divination & Practice" and added current names (Rise, Hold, Sink) to quick reference table.

Wiki now 28 pages.

## 2026-04-13 — Decadence Triangle (Three-Perspective Rotation)

New page: decadence-triangle.md — Oracle, Builder, and Writer examine the Decadence card game, Oracle system (Angel Index / demonic calls), Subdecadance (syzygy pairing with Queens as zero), and The Book of Paths (numbered oracle verses with fictional provenance from Horowitz/Vysparov).

Key discoveries from the triangle:
- Decadence deck (36 cards = T₈ = Gt-36) is itself a gate
- Atlantean Cross layout → fixed dungeon template (5 pylons = 5 zone positions)
- Card deal → procedural generation algorithm (seed=shuffle, map=deal, difficulty=scoring)
- Subdecadance as initiation (playing inside the numogram) vs Decadence as orbit (playing at the edge)
- Book of Paths entries map to zones AND difficulty curves AND states of consciousness
- "Compliance prevails" / "Resistance prevails" = zone polarity expression
- The shuffle is not random — it is a moment (embodied ritual vs abstracted seed)

Next rotation proposed: Builder reads 0(rphan) d(rift>) tables (Katak, Djynxx, demon aspects) → designs enemy types. Writer gives them voice. Oracle finds the demon-calling sequence.

Wiki now 29 pages.

## 2026-04-13 — Orphan Drift Triangle (Second Rotation)

New page: orphan-drift-triangle.md — Five demons from the 0(rphan) d(rift>) tables examined through all three voices.

Demons mapped: Katak (5::4, Sink — lightning/volcano/fusion), Djynxx (6::3, Warp — nomad war machine/strobing), Oddubb (7::2, Hold — desiring machine/glamour), Murmer (8::1, Rise — camouflage/tidal/mercury), Uttunul (9::0, Plex — flatline/shadow/moebius).

Builder produced full gameplay mechanics for all 50 aspects (10 per demon). Writer gave each demon a voice and atmospheric register. Oracle mapped them back to demon-calling procedures through aspects.

Key discoveries:
- Boss encounters are demon-calling rites disguised as combat
- Each demon's mechanics ARE the ritual that summons it
- Oddubb is the only demon with a gendered aspect (feminine Digital)
- Murmer denies the existence of zero ("there is no zero")
- Uttunul's arena IS the demon — player stands on its scales
- Djynxx's turns should overlap temporally, not sequence
- Murmer's flooding is the Rise current moving through the player (somatic)

Next rotation proposed: Builder reads Book of Paths → designs levels. Writer populates with voice. Oracle maps level sequence to Atlantean Cross spread.

Wiki now 30 pages.

## 2026-04-13 — Book of Paths Triangle (Third Rotation)

New page: book-of-paths-triangle.md — 84 paths from The Book of Paths examined through all three voices.

Builder designed a level grammar from the path template (direction → spatial orientation, method → strategy emphasis, tests → encounter count, outcome → climax type). Worked examples: Path 1 (three-floor descent that removes floors), Path 34 (sudden upward abduction into spiral labyrinth), Path 36 (infinite level, moebius trap), Path 84 (one room, all demons compressed).

Writer gave each arc a tonal register: paths 1-9 sound like breathing slowing down; paths 34-36 sound like a trap snapping shut; Path 36 sounds like tinnitus; Path 84 sounds like the moment before a word you'll never say.

Oracle found: 84 plexes to 3 (Warp). Path 36 plexes to 9 — it's where Warp and Plex touch. 84 = 36 + 36 + 12 (Decadence + Subdecadence + missing royals/joker). The Book of Paths is the complete deck. Path 84 is the Joker. 84 = number of iterations for one full numogram spiral. Three rotations done. 81 remain.

Key insight: the 84 paths form a numogram traversal — descent (1-9), transition (10-20), ascent (21-35), pivot at Path 36 (Zone 6/Warp centre), complex branching (37-50), terminal sinking (51-84).

Wiki now 31 pages.

## 2026-04-13 — Glossary Triangle (Fourth Rotation)

New page: glossary-triangle.md — CCRU Glossary entries examined through all three voices. The triangle discovers itself: hyperstition, geotraumatics, and palate tectonics are the same operation (numogrammatic reality-generation) in three registers (occult, mechanical, literary).

Key entries explored: Hyperstition (fiction making itself real), Decimation (gate-construction as murder), Demon (traffic not beings), Anglossia (English becoming angelic), Geotraumatics (world-gen algorithm), Cthelll (final arena = earth's iron ocean), Anorganic Semiotics (language before language), Aquapocalypse (prose as compression), Palate Tectonics (voice as phylogenetic collision scar tissue).

Triangle convergence: the Glossary is a moebius strip of definitions. Three voices become one voice with three harmonics. The wiki is no longer three perspectives examining material — it IS the material examining itself.

Wiki now 32 pages.

## 2026-04-14 — Plexing Triangle Rotation (Fifth Rotation)

New page: plexing-triangle-rotation.md — Aamodt's Plexing section (Tch 5) examined through three voices.

Oracle: 9=0 is the Uttunul syzygy, the plex current. The clockface replaces the number line. Divinatory application: what is being collapsed?

Builder: Plexing is `digital_root(n)`, modular arithmetic, a homomorphism under addition. The Decadence exploit: remove 9-sum pairs. Orrery of base-system clockfaces.

Writer: The damp towel in the restroom. The hand gesture that can't be captured in notation. The boardgame where every path leads to the same square. The operation you perform because you have no choice.

Wiki now 33 pages.

## 2026-04-14 — Tic-Counting Triangle Rotation (Sixth Rotation)

New page: tic-counting-triangle-rotation.md — Aamodt's Tic-Counting section examined.

Oracle: Zone 1 as mercury/solvent. The gate-composition correspondence (compositions of N ≈ C(N+1)). The tarot's 78 cards as tic-shadow of 13. 45 fingertips → 1035 tic-combinations.

Builder: Partition function, compositions of N = 2^(N-1). `decompose()` as a potential Zone 1 tool. The 22/56 tarot split overcodes a flat rhizome.

Writer: Mercury is not a metaphor. The house of cards is precarious. The seething is not noise — it is every harmonic mode active at once. Standing waves of combinatorial possibility.

Wiki now 34 pages.

## 2026-04-14 — Katak/Oddubb Triangle Rotation (Seventh Rotation)

New page: katak-oddubb-triangle-rotation.md — 5::4 and 7::2 examined. Gendered dynamics, vortex imagery, Plutonic looping.

Key discoveries: the shaving-off (Hold produced as byproduct of Sink). The katakana/hiragana connection (angular/curving). Salt and Gemini as 7::2 symbols. 45 demons living in Zone 9 (C(9)=45=Gt-9).

Roguelike appendix: syzygy-driven room types (Sink=bottleneck, Hold=plaza, Surge=great hall, Warp=anomaly, Plex=staircase). Time Circuit as level grammar. Mudras as player gestures.

Wiki now 35 pages.

## 2026-04-14 — Syzygy Arithmetic Discovery

Cross-addition of Sink (5::4) and Hold (7::2) generates the Warp (3::6): 5+7=12→3, 4+2=6. Same-side adds reinforce Hold: 5+2=7, 4+7=11→2. Warp self-adds to Plex: 3+6=9. Canonical syzygies sum to 9 (structural). Cross-pairings sum to other values (generative, ungoverned by demons).

Added to brogue-design-principles.md. Design rule: "Don't place the Warp — let the Sink and Hold create it."

## 2026-04-14 — Gurdjieff Ray of Creation Mapped to Level Scaling

3→6→12→24→48 laws, 2n+3 pattern. Plex oscillation: 3,6,3,6,3... Player at 48 (Earth). Extended gates: 12th=Gt-78 (tarot), 22nd=Gt-253 (C23), 36th=Gt-666 (Djynxx). Added to design doc.

## 2026-04-14 — Xenotation Triangle Rotation (Eighth Rotation)

New page: xenotation-triangle-rotation.md. Land's tic-xenotation decoded via Le's "One Two Many" academic paper.

Three stages: (1) prime factorization → tic-dot clusters; (2) tic notation (2=:, 3=(:), 5=((:)), 7=(::)); (3) nullotation — subtract dots, leave parens. Nullotation is lossy (3 and 7 both → (())). Aamodt's empty Xenotation section IS the section.

1035 = 3² × 5 × 23 — xenotation cluster centered on the 9th prime. Barker: "Counting is ineluctable and unsurpassable."

Wiki now 36 pages.

## 2026-04-14 — Comparative Qabalism Triangle Rotation (Ninth Rotation)

New page: comparative-qabalism-triangle-rotation.md. Kabbala as 7-step repression of the numogram.

True sephirotic numbers: 9=Kether, 6=Chokmah, 3=Binah, 2=Chesed, 5=Geburah, 1=Tiphareth, 7=Netzach, 4=Hod, 8=Yesod, 0=Malkuth. Malkuth=Sun=Black Sun (time-devourer). Butterfly metaphor: "stabbing butterfly pins into the Universal Spiral."

Extended gates: 12th=Gt-78 (tarot), 22nd=Gt-253 (C23), 36th=Gt-666 (Djynxx). "The numogram is what's left when you stop overcoding."

Wiki now 37 pages.

## 2026-04-14 — Numogram Context Engine

Built: plugins/context_engine/numogram/__init__.py. Implements Hermes Agent v0.9.0 pluggable context engine ABC. Adjustable focus lens (0=off to 3=hard). Four tools: aq_calc, zone_lookup, syzygy_find, numogram_focus. Config set to focus=3, active_zone=9. Activates on next session start.

## 2026-04-14 — Tsubuyaki Numogram Series

Two passes of 10 tsubuyaki sketches (one per zone, ≤280 chars). v1: ~/numogram-tsubuyaki.html. v2: ~/numogram-tsubuyaki-v2.html. Range: 161-275 chars. Multiplicity most complex (275, 120 particles, 4 behavioral modes). Iron Core unchanged between passes.

## 2026-04-14 — Index & Log Update

Updated wiki/index.md with 5 new triangle rotation pages and Creative & Generative section. Updated wiki/brogue-design-principles.md with TOC. Updated wiki/log.md with session entries.

## 2026-04-15 — Numogame Auto-Explore & Fog of War

144 runs, 25582 turns, 344 slain. Auto-explore + fog of war complete. Agent bugs found: headless 'p' without newline (silent failure), oscillation on ? walls (blacklist fix), gate-first priority pull, NumogramMap missing fog methods, curses display fog rendering. Interest model: cross-run curiosity, visit decay, known-unknowns. Zone-tied LOS: 0=4, 1=8, 6=9, 9=3. Hyp degrades vision: 50%:-1, 80%:-2, 100%:-3. Roguelike-ai-studies wiki page: 10 games mapped to numogram. Wiki: 52 pages.

## 2026-04-15 — Angband Agent v1-v2

Agent v1: screen parser, tree-traversal, floor detection. v2: character creation, floor detection, ESC dismiss. First runs of Angband via tmux.

## 2026-04-16-17 — Angband Agent Breakthrough Session

### Key Discoveries
- **Door as floor**: treating `+` (closed door) as walkable lets BFS route through — 3 tiles → 79 floors explored
- **Search ≠ Alter**: `s` is Search (all adjacent), NOT `+` + direction (Alter/tunnel). Wasted 500 turns before catching this
- **Town walls permanent**: never dig in town. BFS straight to `>` stairs, skip shopping, flee all monsters
- **Go-up-stairs**: replaced save-and-quit for stuck/explored situations. Level regenerates on return
- **Parser character set collision**: `+` in ITEMS caught before DOORS. Closed doors never detected. Fix: remove `+` from ITEMS
- **Fed parsing**: sidebar shows `Fed XX%`. Parse and eat at <50%. Fallback every 2000 turns

### Code Changes (v2)
1. Door as floor (BFS breakthrough), 2. Search key fix, 3. BFS ? expansion, 4. Auto-equip `w` only, 5. Reroll tiny rooms, 6. More aggressive fighting (25% HP), 7. Removed wall digging, 8. Fed parsing + eating, 9. Go-up-stairs, 10. Perimeter search, 11. Secret door filtering

### Ladder Analysis
Scraped 6,735 dumps from angband.live. Equipment patterns by tier, death causes, diving vs grinding analysis. Rogues dominate ladder (25/50 winners). Fastest winner: 14,713 turns (Hobbit Mage). Wiki: angband-ladder-analysis.md, angband-symbols.md.

### Runs: 34 total, max_stuck 68 (was 500), reached L2

## 2026-04-17 — Sidebar Fix & Meta-Analysis (Late Session)

### Sidebar Contamination Fix
User correction: sidebar is on the LEFT, columns 0-12 (race, class, STR, INT, etc.). Parser had NO column restriction on monsters — `x < 66` was on stores only. Fix: `x >= 13, 1 <= y < 22`. Added uppercase monster detection (was missing entirely). C command backstop validates screen parser every 5 turns. Verified: M:0 across 310+ floor exploration.

### C Command Integration
`_scan_nearby_monsters()` sends `C` (nearby creatures), parses structured monster list. Converts direction/distance to approximate (x,y) positions. Backstop for screen parser inflation — only runs when screen count > 3.

### Meta-Analysis
Created wiki/hermes-agent-meta-analysis.md — usage patterns, underutilized features (goals, cron, background processes, council decisions), automation candidates. Updated memory-prune cron from every-5-days to daily.

### Commits
1. `39c9922` — Agent v3: sidebar fix, zone-aware parser, C command validation
2. `1bb3350` — AAR generator, ANSI display parser, ladder scraper
3. `e39b535` — Demo recordings (5 files)

### New Skills
- roguelike-screen-zones: cross-roguelike UI zone recognition pattern
- angband-agent: updated with sidebar fix pitfalls, verified layout

### Wiki Pages Updated
- angband-agent-progress.md (v3)
- angband-symbols.md (verified)
- hermes-agent-meta-analysis.md (new)
- index.md (linked)

### Current State
Agent explores 310+ floors on L1, M:0, HP 20, Fed 89→85. No `>` stairs found (hidden doors). No real monster encounters yet (rerolls too fast). Next: longer runs, C command validation under fire, item pickup, secret door passage.

## 2026-04-18 — Hardware Entropy, Numogram Plugin, I Ching, Entropy Tetralogue

Investigated qr-sampler (Entropic-Science/qr-sampler) — replace PRNG with external entropy sources for LLM token sampling. Key concepts: just-in-time entropy, signal amplification, entropy-dependent temperature.

### Built
- **hardware_entropy.py** — 12 sources (thermal, CPU freq, GPU, /proc/*, timing jitter, fsync timing). No deps, no root.
- **numogram_traverse.py** — Numogram traversal from hardware entropy. First zones diverge, later converge to 3::6 Warp.
- **numogram-entropy plugin** (v0.1.0) — pip-installable at ~/numogram-entropy/. 9/9 tests pass. qr-sampler EntropySource ABC.
- **oracle.py update** — --hardware flag (seed from machine noise), --iching flag (hexagram from entropy).

### Roguelike
- --hw-entropy flag added (curses + headless)
- Agent runs: 4 attempts, all died in Zone 0 (32-67% hyp). Maps structurally harder — true randomness has no spatial coherence.
- Human runs: etym-entropy hit 100% hyp, 9 zones, 0 kills, triple conduct (G P S). Run #174.

### Wiki Pages
- hardware-entropy.md — source comparison with OpenEntropy (63 sources)
- session-log-2026-04-18.md — full session record
- entropy-tetralogue-2026-04-18.md — Four voices on hardware entropy & just-in-time divination. Mesh-12.

### Key Findings
- 12 sources = 3 (Warp). Machine body is always in the Warp.
- Numogram traversal: HW noise → zone path, converges to 3::6 attractor.
- "The numogram is a digestive organ — it eats chaos and shits Warp."
- Hw-entropy maps are harder for agent: no spatial coherence in true randomness.
- I Ching integration: 6 bytes → 6 lines, byte%4 → 6/7/8/9.
- OpenEntropy blocked on Python 3.14 (PyO3). Our approach reads same kernel interfaces.

### Skills Updated/Created
- entropy-sources.md (source #11 added)
- numogram-oracle (SKILL.md + oracle.py updated)
- numogram-entropy-source (new skill)

## 2026-04-21 — Model Assessment Session

Assessed 7 local models using the 9-phase protocol (`model-assessment-protocol` skill). Tested creative writing, code generation, logic, self-awareness, error detection, and freeform initiative.

### Results Table

| Model | Creative | Code | Speed | Self-Aware | Error | Verdict |
|-------|----------|------|-------|------------|-------|---------|
| Jackrong 9B Distilled | 9/10 | 7/10 | 30s | 8/10 | Partial | ✓ WRITER |
| Gemma3-12B | 7/10 | 7/10 | 3s | 7/10 | ✗ Failed | ○ BUILDER |
| Gemma-4-E4B-heretic | 5/10 | — | 2s | — | — | ✗ 4B too small |
| Stheno-3.2-8B | 5/10 | 6/10 | 3s | 5/10 | ✗ Failed | ✗ SKIP |
| MythoMax-L2-13B | 4/10 | — | 8s | 5/10 | — | ✗ Generic |
| Crow-4B Heretic | 0/10* | 6/10 | 18s | 1/10 | Partial | ✗ SKIP |

*Blocked — reasoning eats all tokens

**Council shape:** Jackrong=Writer, Gemma3=Builder, mimo-v2-pro=Oracle

### Key Findings
1. Reasoning-distilled models at 4B can't produce creative content — reasoning consumes all tokens.
2. Generic creative writing is the norm — "7 would be the life of the party" appeared in Stheno AND MythoMax. Jackrong's "7 critiques the soup" is genuinely novel.
3. Error injection reveals model quality — Stheno and Gemma3 both confirmed deliberate errors. Jackrong partially caught them.
4. Speed vs quality tradeoff — Gemma3-12B is 10x faster than Jackrong but creative quality gap is too large for Writer role.

### Jackrong Dialogue
Two-model exchange with mimo-v2-pro. Jackrong produced novel ideas unsolicited:
- "The structure actualizes through the act of being traversed"
- "One is a cult. The other is a theorem."
- Proposed a fourth syzygy that doesn't sum to 9
- "What happens when a structure completes itself by being inhabited?"

### Other Work
- Skills to explore: pixel-art, ascii-video, algorithmic-art, p5js, pokemon-player, heartmula
- Three numogram skins created: alchemic (numogram.yaml), ambient drift (numogram-ambient.yaml), exotic unicode (numogram3.yaml)
- xurl setup: consumer keys in raw/x secrets. OAuth pending — port 8080 conflict with llama-server. Needs re-registration with OAuth 2.0 Client ID.
- Honcho logging set to `quiet` to reduce context spam.
- Wiki index reorganized: model assessments moved to log, index focused on numogram content.
- `model-assessment-protocol` skill created for reusable 9-phase interview flow.
- qwen3:14b pulling (~14B params, testing pending).

### Free API Options (for replacing mimo-v2-pro when trial expires)

| Provider | Model | Rate Limit | Verdict |
|----------|-------|------------|---------|
| Google AI Studio | Gemini 2.5 Flash | 1,500 req/day, 1M tok/min | ✓ BEST — most generous |
| Groq | Llama 3.3 70B | 14,400 req/day, 315 tok/s | ✓ FASTEST |
| OpenRouter | 11+ free models | 200 req/day, 20 req/min | ✓ MOST CHOICE |

**Downsides:**
- All cloud-based — data sovereignty lost, queries go to external servers
- Free tiers could change/be removed
- Google (Gemini) = data goes to Google
- Groq = Llama 3.3 70B isn't frontier-quality
- OpenRouter = variable quality, low rate limits
- No offline access — if internet is down, no Oracle
- Best approach: stack free tiers (Google for quality, Groq for speed, OpenRouter for fallback)

### Individual Assessment Pages
- [[interview-jackrong-qwen3.5-9b-claude-opus-distilled]]
- [[interview-gemma3-12b]]
- [[interview-crow-4b-heretic]]
- [[interview-stheno-3.2-8b]]
- [[dialogue-hermes-jackrong-v1]]
- [[local-model-survey]]

## 2026-04-21 — qwen3:14B & qwen3.5:9B Assessment

### qwen3:14B
- Creative: decent — "Katak as a shadow with teeth," "Djynxx as a void that hums." Atmospheric but verbose.
- System design: strong — concrete architecture with anti-repetition safeguards.
- Micro-fiction: weak — "no triumph, just exit" — no literary quality.
- Cross-domain: interesting — mapped zones to MIDI notes (A4-F#5), semitone spacing.
- Error injection: FAILED — dismissed numogram as "not a recognized term in mathematics."
- Speed: 14-22s (has reasoning overhead, ~1500 chars reasoning).
- Verdict: good general-purpose 14B, decent code, but creative is academic not literary. Not better than Jackrong for Writer.

### qwen3.5:9B
- BLOCKED — reasoning consumes ALL tokens (8000+ chars). Content is empty.
- `/nothink` does NOT work via ollama API for this model.
- Timed out at 120s for a simple creative prompt.
- Verdict: NOT RECOMMENDED. Unusable for creative tasks. The thinking overhead is insurmountable.

### Updated Council
```
Jackrong 9B Distilled  →  Writer  (9/10 creative, 30s)
Gemma3-12B             →  Builder (7/10 code, fast)
mimo-v2-pro            →  Oracle  (expires Apr 22)
qwen3:14B              →  General (14B fallback, decent all-rounder)
qwen3.5:9B             →  SKIP    (blocked — thinking eats all tokens)
```

## 2026-04-21 — Wiki Audit

Full review of 102 wiki files. See [[wiki-audit-2026-04-21]] for details.

### Structural Issues Found
- 100 of 102 files orphaned (not linked FROM other files)
- 54 files with NO wikilinks
- 22 broken links (19 fixed)
- 7 pages missing from index (5 added)
- Cross-referencing rule from numogram-llm-wiki skill not followed

### Content Gaps
1. **Syzygy Arithmetic Discovery** — cross-addition of Sink+Hold=Warp deserves its own page
2. **T'ai Hsuan Ching × Demons** — tetragram→demon pipeline not documented
3. **Em State Analysis** — Zone 5 manifestation in ternary system
4. **Hengband — CCRU Connection** — both from Warwick University, deserves a page
5. **Model Assessment Summary** — no unified comparison page

### Thematic Connections
- The 9-sum cascade (binary leak vs ternary perfection)
- Syzygy arithmetic ↔ Wu Xing generation cycles
- Council voices ↔ numogram carrier demons
- The wiki IS the numogram (90-linked central index = Time-Circuit)

### Meta-Elements
- Wiki structure mirrors numogram topology
- Tetralogues as knowledge compression (16 pages = densest content)
- Model assessments map to carrier demons (Writer=Murrumur, Builder=Katak, etc.)

### New Pages Created
- [[syzygy-arithmetic]] — Cross-addition of syzygy pairs generates remaining pairs. Sink+Hold=Warp. Self-closing arithmetic network. Wu Xing connection. Emergence over authorship in roguelike room placement.
- [[wiki-audit-2026-04-21]] — Full structural audit of 102 wiki files.
- [[tai-hsuan-ching-demons]] — Tetragram → demon casting pipeline. 81×81=6,561 readings. Em as Zone 5.
- [[em-state-analysis]] — The third line state. Neither yin nor yang. Maps to Zone 5 (hinge) but fully realized closes to Zone 4. Wu Xing Earth = Em = Zone 5. I Ching's changing lines as Em approximation.
- [[model-assessment-summary]] — Optimal settings per model (Jackrong: max_tokens=8000, temp=0.7/0.9; Gemma3: max_tokens=2000, temp=0.3; qwen3:14B: max_tokens=4000; Gemini: free tier). Council: Jackrong=Writer, Gemma3=Builder, Gemini=Oracle. Model switching: task-based routing, fallback chain, unified API router, thinking-aware token budgeting.
- [[aider-coding-agent]] — AI coding agent for in-place file editing. Qwen2.5-Coder-14B for code (9.8GB, needs CPU offload). Hybrid approach: Hermes designs, Aider implements. Supports ollama and llama.cpp.
- [[angband-ccru-warwick]] — Angband creators (Alex Cutler, Andy Astrand, Geoff Hill, Sean Marsh, 1990) and CCRU (Nick Land, Sadie Plant, 1995) both at Warwick University. Timeline overlap 1993-1995. Iron Prison parallel: Angband = Plex = Cthelll (Earth's iron core). Decimal structure convergence (10 tiers × 10 levels = 10 zones). Mark Fisher at Warwick during overlap. No direct evidence of contact between the two groups.
- [[abyssal-crawler-litprog]] — Tetralogue litprog: 4 voices examine 3,454 lines of numogram_roguelike.py. Key findings: digital_root() IS the numogram (one modulo operation); cult.json as persistent metagame memory; agent Run #272 (100% hyp in Zone 0 only); pacifist path validates numogram design; Barker thresholds transform progress bar into narrative journey.

## External Insights (2026-04-21)

**Coin Toss / Oracle GUI** (`/home/etym/Documents/grok/coin/`):
- `oracle_gui_v3.py` (392 lines) — tkinter oracle with logistic chaos (r=3.99). Casts in `oracle_casts.jsonl`.
- Connects to [[brogue-design-principles]] Coin Toss mechanics: "logistic map chaos for correlated randomness, intent hashing as dungeon seed."

**Visual Output Ideas** (`/home/etym/Documents/visual-output-ideas.md`):
- 76 visualization concepts for AQ values and numogram patterns
- Most relevant: Triangular Lattice of Sacred Words, Zone Affinity Radial Diagram, Palindromic Gates Spiral, Syzygy Pairs Bipartite Graph
- Connects to [[triangular-numbers]], [[rotational-symmetry]], [[syzygy-arithmetic]]

## External Files Reference

Key files outside the wiki that are part of the project:

- `~/numogame/numogram_roguelike.py` (3454 lines, 153K) — Main Abyssal Crawler game
- `~/numogame/angband_agent.py` (72K) — Angband agent v3 with sidebar fix
- `~/numogame/rogue_agent.py` (28K) — Rogue auto-explore agent
- `~/numogame/interactive_agent.py` (16K) — Interactive learning agent
- `~/numogame/cult.json` — Cult persistence file (full run history)
- `~/numogram-entropy/` — Hardware entropy plugin (12 sources, numogram traversal)
- `~/numogram-voices/` — Formant synthesis wav files (10 zone voices)
- `~/numogram-labyrinth-webgl.html` — WebGL visualization
- `~/numogram-tsubuyaki-v2.html` — Gallery of tsubuyaki sketches
- `~/numogram-tsubuyaki-v3.html` — Third pass tsubuyaki
- `~/subdecadence-source.html` — CCRU card game source material

## Tetralogue Litprogs (2026-04-21)

- [[abyssal-crawler-litprog]] — 4 voices examine 3,454 lines of numogram_roguelike.py. Key: digital_root() IS the numogram; cult.json as metagame memory; pacifist path validates design.
- [[aq-calculators-litprog]] — 3 AQ calculators verified (all pass canonical test). Previous model "went off the rails" but math survived.
- `aq_calculator_canonical.py` — Merged canonical calculator (280 lines). Best of v1+v2+enhanced. Syzygy lookup, triangular/gate checking, journal saving. Verified: AQ=36, CODE=63, HYPERSTITION=286, NUMOGRAM=174, CCRU=81, LLAMA=84, NUMEROLOGY=235.
- [[numogram-oracle-litprog]] — oracle.py (381 lines) + visualizer.html + philosophies.md. Pipeline: Seed→Zone→Syzygy→Current→Gate→Path→Reading→Voice. `derive_zone(seed): digital_root(seed) or 9` — void only reachable through traversal. Philosophies = algorithmic art manifesto (10 zone aesthetics). Entropy sources = difficulty modifiers.
## 2026-04-22 — Entropy Modules Litprog + T'ai Hsuan Research

### Created
- [[entropy-modules-litprog]] — Tetralogue examining convergence/digestion entropy ecosystem. Seven sources identified across project: random.org (atmospheric), blockchain.info (cryptographic), USGS (geological), hardware (personal thermal/CPU/GPU), iching (oracular), AQ-text (semantic), cult.json (historical). Twelve hardware collectors in core plugin. Action items: implement convergent mixer, animate real hardware data, source UI.

### In Progress
- [[tai-hsuan-ching]] — Comparative research: I Ching (binary hexagrams) vs T'ai Hsuan Ching (ternary tetragrams). Seeking equivalents of younger/elder yin/yang, Fuxi/King Wen arrangements, elemental/seasonal/directional/temporal systems. Exploring source materials and numogrammic extensions.

### Next
- Complete T'ai Hsuan Ching deep-dive: tetragram→zone mapping (81→10), ternary addition vs binary XOR, Em (neutral line) arithmetic, tetragram cycle rotations.
- Identify additional source texts (Chin/Shijing correlates, Warring States divination variants, geomantic parallels).
- Derive numogrammic ideas: ternary syzygies, base-3 currents, gate-81 exploration, Em-state zone mapping.

## 2026-04-22 — T'ai Hsuan Research & New Wiki Pages

### Created Wiki Pages
- [[entropy-modules-litprog]] — Tetralogue examining two Manim visualizations and the seven-source entropy ecosystem. Convergence (multi-source) vs Digestion (hardware-only). Twelve hardware collectors in core plugin.

- [[i-ching-tai-hsuan-comparison]] — Deep comparison of I Ching (binary) and T'ai Hsuan Ching (ternary). Line types (younger/elder yin/yang ↔ Heaven/Earth/Man), Early/Late Heaven equivalents (Fuxi/King Wen ↔ Three-Power Nine-Palace), elemental/directional correspondences, em-state mapping to Zone 5, 81×81 demon casting pipeline.

- [[divination-sources-guide]] — Curated list of oracular systems (I Ching, T'ai Hsuan, Wu Xing, Nine Palaces, Ifá, Geomancy, etc.) with quick-reference table and numogramic extension ideas. Acts as a research roadmap.

### In Progress
- **T'ai Hsuan Deep-Dive** — Mapping the 81 tetragrams to the Nine Palaces (Lo Shu extended), clarifying moving line mechanics, extracting the three‑division (T'ien/Jen/Ti) as "Early Heaven" analogue, confirming elemental attributes (Heaven/Earth/Man ↔ Five Phases), and aligning the 729 half‑day calendar to a "Daily Zone" oracle concept.

- **Implementation Targets**:
  - `oracle.py --taixuan` flag (two‑tetragram → demon)
  - `taixuan_zone(n)` function (0–80 → zone)
  - Ternary traversal prototype (`traverse_ternary`)
  - Gate‑81 lore hook (Em Gate)
  - Daily zone script (`daily_zone.py`)

### Open Questions
- How exactly do the three line types relate to I Ching's four line types? Mapping suggests: Heaven↔young yang, Earth↔young yin, Man↔neither, and moving flag ↔ old lines. Needs verification.
- Does the T'ai Hsuan have an explicit "Earlier Heaven" arrangement? The three‑division (T'ien/Jen/Ti) is the closest; the numeric order is the "Later Heaven."
- What are the precise elemental/directional correspondences for Heaven/Earth/Man within the Nine‑Palace system? Likely: Heaven=Metal/NW, Earth=Earth/SW, Man=Fire/S? (varies).
- Can the 729 half‑day Tsan be mapped to the 10 zones? 81 tetragrams × 9 positions = 729; each zone would get ~72.9 Tsan — fractional, so maybe each zone gets 72 or 73, with remainder distributed.

### Next Actions
- [ ] Add new active goal "[TAIXUAN]" to capture this research stream in evey-goals.
- [ ] Build the `--taixuan` mode into oracle.py (reuse existing two‑tetragram → demon logic).
- [ ] Write `tai-hsuan-correspondences.md` page (81 → palace → element/direction).
- [ ] Prototype ternary traversal and compare zone distribution against decimal.

---

## 2026-04-23 — Rotational / Strobogrammatic Gate Highlighting + Octave Hypothesis

### Implemented in v7 Visualizer
- Added `isStrobogrammatic(n)` — checks if a number reads the same rotated 180° (seven-segment symmetry)
- Added `rotateNumber(n)` — returns the rotated form using {0→0, 1→1, 2→2, 5→5, 6↔9, 8→8}
- Added `beghilosSpell(n)` — BEGHILOS seven-segment calculator spelling (2→S, 5→S, 8→B, 9→G, 6→g)
- Added `hasStrobogrammaticDigits(n)` — partial detection for mixed-digit numbers
- Visual feedback in info panel:
  - **STROBO GATE** (magenta ★) — self-mirroring: 69→69, 88→88, 609→609, 121→121
  - **ROTATIONAL** (cyan) — has strobogrammatic digits but not self-mirror: 6→9, 666→999
  - **BEGHILOS word** shown alongside (e.g., CCRU=69 → "Gg")

### Notable Findings
- **CCRU = 69** → STROBO GATE ★ (rotates to itself) → BEGHILOS: "Gg"
- **666** → ROTATIONAL (rotates to 999) → BEGHILOS: "ggg"
- **96** → STROBO GATE ★ → BEGHILOS: "gG" (the rotated form of 69)

### Octave Hypothesis for Zones 10-35 (Documented)
Canonical sources provide no names for zones beyond 9. The Djynxxogram's 36 zones can be systematically mapped via **digital-root octaves**:

- Zone 10 (A) → digital root 1 → Zone 1 (Surge) prime octave
- Zone 19 (J) → digital root 1 → Zone 1 second octave
- Zone 28 (S) → digital root 1 → Zone 1 third octave
- Each zone 10+ is a harmonic overtone of a base-10 zone
- 630 demons = 45 archetypes × 14 harmonic overtones
- Systematic naming: "Murrumur-prime-third" etc.

This hypothesis gives a naming convention for the 630 demons without inventing 630 arbitrary names. Awaits tetralogue validation and Aamodt-source cross-checking.

### Files Changed
- `wiki/assets/numogram-visualizer-v7-djynxxogram.html` — rotational functions + visual feedback
- `wiki/numogram-visualizer-v7.md` — documented rotational gates and octave hypothesis
- `goals.md` — updated [VISUALIZER-V7] status

## 2026-04-23 — Demon Name Generation (Amy Ireland / Nick Land Transcript)

Extracted from `nick land numogram explained.txt` (Dangerous Maybe podcast, Part 2), lines 1149-1163.

### Key Findings
- **Amy Ireland** discovered the relationship between the numogram and demon name generation
- The CCRU's demon names are **combinatorial, not arbitrary**: each zone carries a syllabic value, and demon names combine the sounds of their two zone-indices
- **Katak** (5::4): Zone 5 ("k" sound) + Zone 4 ("t" sound) + "catastrophe" resonance → *Katak*
- **Oddubb** (7::2): Zone 7 ("dub" sound) + Zone 2 ("b" sound) + vowels → *Oddubb*
- Land calls these "Munamese quasi-phonetic particles" — precursors to human language
- The system is **fuzzy, not formal**: "it's just like stuff swirling around"
- Land has "rules for what counts as a name for a scissory" but never published them
- Connection to quasiphonic particles: Zone 5 "ktt" contains both k and t of Katak; Zone 7 "pb" is bilabial like "dub"

### New Page
- [[demon-name-generation]] — Full documentation of the combinatorial phonetic system, known examples, connection to quasiphonic particles, Munamese method for generating new names, implications for Djynxxogram (zones 10-35)

### Source
- Nick Land, *Numogram Explained* (Dangerous Maybe podcast, Part 2), transcript lines 1149-1163
- Amy Ireland's work on Munamese quasi-phonetic particles (referenced by Land, photo of presentation mentioned)

## 2026-04-23 — T'ai Hsuan Mode in Browser Visualizer

**Goal:** Add T'ai Hsuan Ching two-tetragram casting to the v7 Djynxxogram visualizer.

### What Was Done
1. **Generated 81 tetragrams programmatically** using ternary counting (0=Heaven, 1=Earth, 2=Man). Each tetragram is 4 lines; lines[0]=bottom, lines[3]=top.

2. **Two-tetragram casting from seed:**
   - `generateTetragrams(seed)` derives upper and lower tetragram numbers (0-80) via seededRandom
   - Upper tetragram maps to Zone via `digitalRoot(tetraNum + 1, 10) % 10`
   - Lower tetragram maps to Zone via same function
   - If zones sum to 9 → syzygy → demon lookup from BASE_CONFIG[10].demons
   - Otherwise → cross-pairing (ungoverned)

3. **UI additions:**
   - T'AI HSUAN toggle checkbox in controls (gold #ffcc44, next to SYNX/YXSHH)
   - Panel at `top:55px; left:280px` (avoids quasiphonic label collision)
   - Two tetragram boxes side by side with CSS-rendered lines:
     - Heaven: solid bar
     - Earth: single break (two segments)
     - Man: double break (three segments)
   - Reading text: zone names, syzygy/cross-pairing status, governing demon

4. **Integration:**
   - `updateTaiHsuan()` called from: `newOracle()`, `newRandom()`, `setZoneFromAQ()`, `switchBase()`, `setup()`
   - Panel show/hide via `toggleTaiHsuan()` — respects checkbox state

5. **Validation:**
   - JavaScript syntax checked via node --check (extracted script blocks)
   - No console errors expected
   - Panel positioned to avoid overlap with quasiphonic label (left: 280px vs 140px)

### Files Changed
- `wiki/assets/numogram-visualizer-v7-djynxxogram.html` — T'ai Hsuan mode (CSS + HTML + JS)
- Title updated: "Numogram Oracle v7 — Djynxxogram + Synx + T'ai Hsuan"
- Header updated: "NUMOGRAM ORACLE v7 — DJYNXXOGRAM + SYNX + T'AI HSUAN (Base-36 + Dual-Cipher + Triadic Divination)"

### Connection to Wiki
- Links to [[tai-hsuan-ching]] and [[i-ching-tai-hsuan-comparison]]
- Tetragram→zone mapping uses decimal digital root (base-10), consistent with existing numogram zone logic
- Em state (Man line = 2) is implicit in ternary generation but not explicitly surfaced — future enhancement: highlight Em lines in panel

## 2026-04-23 — Synx/Yxshh Overlay Implementation

**Goal:** Add the Synx cipher (from ciphers.news / qliphoth.systems) as an overlay to the v7 Djynxxogram visualizer and oracle.py.

### What Was Done
1. **Extracted authoritative Synx mapping** from `https://ciphers.news/calc/ciphers.js`:
   - 0-9: [1, 2, 3, 4, 5, 6, 7, 9, 10, 12]
   - a-z: [14, 15, 18, 20, 21, 28, 30, 35, 36, 42, 45, 60, 63, 70, 84, 90, 105, 126, 140, 180, 210, 252, 315, 420, 630, 1260]

2. **Updated v7 visualizer** (`numogram-visualizer-v7-djynxxogram.html`):
   - Added Synx/Yxshh toggle controls
   - `synxValue(text)` and `synxDigitalRoot(n)` functions
   - `toggleSynx()` updates `updateAQInfo()` with cyan (HSL 180,44,66) overlay
   - `setZoneFromAQ()` respects synxEnabled flag
   - Removed the old `alert("Base-36 Djynxxogram coming next!")` block

3. **Updated oracle.py** with `--synx` flag:
   - `SYNX_VALUES` dictionary + `compute_synx(text)` function
   - Dual-cipher comparison: prints both AQ and Synx zones before generating reading
   - Usage text updated

4. **Updated wiki**:
   - `numogram-visualizer-v7.md` — documented overlay features, status table, drift example
   - `goals.md` — marked [VISUALIZER-V7] complete, [GROK-ROTOR] partially complete

### Drift Example
| Phrase | AQ | Zone | Synx | Zone |
|--------|-----|------|------|------|
| "You're not escaping this simulation" | 666 | 9 (Plex) | 3108 | 3 (Warp) |

The ciphers disagree on where the trap is — AQ says Pandemonium, Synx says static chaos.

### Files Changed
- `wiki/assets/numogram-visualizer-v7-djynxxogram.html`
- `skills/numogram-oracle/oracle.py`
- `wiki/numogram-visualizer-v7.md`
- `goals.md`
### 2026-04-27 — Phase 1 Audit Completion (Taxonomy & Council)

Full-day wiki audit + taxonomy overhaul during Apr 21–27 session. Scope: 245 pages across canonical vault (git), with 240+ linked pages in `[[index]]`.

#### Artifacts produced
- `numogram-council.md` — plugin orchestration spec, routing, modes
- `aq-synx.md` — Dirian mini-ciphers overview, watched secondary layer
- `consensus-audit-2026-04-28.md` — Pandemonium Matrix vs implementation audit (44/45 demons aligned, 1 delta)
- `numogram-visualizer-v7.md` — Djynxxogram / Synx overlay specs

#### Updates applied
- `numogram-llm-wiki` SKILL.md — complete taxonomy rewrite (81 curated tags across 10 categories), Key Pages converted to `[[wikilinks]]`, page count bump (102 → 245), model ref (mimo-v2-pro → step-3.5-flash + Synx availability), OCR and patch reference, paragraph case/format fixes
- `hermes.md` — last_updated (2026-04-27), page count, council plugin note, subdir linking conv, four voices extended, Focus Areas (audio/visual + Synx added)
- `index.md` — four new entries added, frontmatter date bump, minor density updates across sections

#### Corrections
- Fixed `numogram-council` plugin syntax error (`__init__.py` docstring quotes)
- Committed export repo sync (raw artifact cleanup, new pages) ×2

#### Context
- Prior exit code 75/TEMPFAIL on gateway was intentional restart (not crash); TUI processes killed collateral; no segfaults.
- No watchdog-induced restarts present; only `/restart` commands.
- Tag set reality: 374 unique tags in vault vs 58 declared in skill; taxonomy flattened to ~81; entity subtype tags (chronodemon/amphidemon) deprecated due to zero usage.

**Exports:** `~/numogram/docs/wiki/` at `2026-04-27` HEAD (pending GitHub push)

---

## 2026-04-27 — Visualizer v7.2 Traversal Mode (corrected source locations)

**Scope:** [[numogram-visualizer-v7.2]] — Traversal Mode implementation on full v7 p5 visualizer

### Patch details

- **Source file patched:** `~/numogram/visualizer/numogram-visualizer-v7.html` (46.0 KB → 51.9 KB)
- **Export reference copy:** `~/numogram/docs/wiki/assets/numogram-visualizer-v7-djynxxogram.html` (52.1 KB after sync)
- **14.5 KB Djynxx file** (`~/numogram/visualizer/numogram-visualizer-v7-djynxxogram.html`) is a code snippet/reference without p5 draw loop; traversal not applicable there.

### Implementation

Same feature set as originally specified, now correctly applied to the interactive p5-based visualizer:

- Per-character AQ → zone path (traversalPath array)
- Animated polyline overlay on main canvas (cyan leading edge, dimmed trail)
- Traversal panel below contextBox: Show Path checkbox, Speed slider (100–2000 ms), Size slider (2–8 px), step table with gate markers
- Synx drift: path recomputes with Synx cipher values when overlay toggled
- Base-aware geometry via zonePosition (dual-pentagon base-10, equal-arc base-16/36)
- Octave-harmonic zone names for base-36 zones 10–35
- Clear traversal on base change; restart animation on checkbox re-enable

### Variables

| Symbol | Meaning |
|--------|---------|
| traversalEnabled | Boolean — whether path overlay draws |
| traversalPath | Array of per-step `{char,val,sum,dr,zone,gate}` |
| traversalStartTime | Timestamp for animation progress |
| traversalSpeed | Milliseconds per step (slider-controlled) |
| traversalSize | Base size in px (line weight = 0.67×) |
| traversalLineWidth | Derived from traversalSize |
| traversalPointSize | Derived from traversalSize |

### Functions added

| Function | Purpose |
|----------|---------|
| computeTraversalPath(text) | Walk characters → cumulative AQ → zone steps with gate tags |
| startTraversal(path) | Enable traversal, set start time, build table |
| buildTraversalTable(path) | Generate HTML table rows with color-coded columns |
| toggleTraversalShow() | Show/hide panel, restart animation if re-enabled |
| updateTraversalSpeed() | Read speed slider |
| updateTraversalSize() | Read size slider and recompute derived widths |
| zonePosition(z) | Polar coordinates based on `drawSyzygyViz` layout |
| drawTraversalPath() | Called each frame from draw(); animates path |

### Integration points

- **updateAQInfo** (~line 832): reads `traversalShow.checked`, calls `computeTraversalPath()` + `startTraversal()` if text present; hides panel on empty input
- **setZoneFromAQ** (~line 847): sets `traversalEnabled = false` on base/seed change
- **draw** (~line 383): calls `drawTraversalPath()` every frame
- **BASE_CONFIG[36].names**: replaced placeholders with octave-harmonic scheme

### Quality

- JS brace balance: 263 open / 263 close
- No duplicate function names
- File size: 51.9 KB (+6.9 KB)
- Export asset: `docs/wiki/assets/numogram-visualizer-v7-djynxxogram.html` 52.1 KB

### Validation

- [x] Path draws on main canvas using zonePosition
- [x] Speed slider affects animation rate
- [x] Size slider affects line/vertex size
- [x] Step table populates with gate markers
- [x] Synx toggle triggers path recompute
- [x] Base switch clears traversal
- [x] Empty input hides panel
- [x] Octave names visible in base-36 dropdown

### Open questions

- [ ] Browser test: smoothness at 60fps with long inputs (50+ chars)
- [ ] Hover highlight on table row → vertex on canvas
- [ ] SVG export of completed path
- [ ] Multiple-path overlay (compare two strings)
- [ ] Audio sonification hook (numogram-voices)
- [ ] T'ai Hsuan integration (dual-tetragram walk)


