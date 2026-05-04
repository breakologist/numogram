---
title: "Qliphoth/CCRU Import Analysis & Integration Roadmap"
created: 2026-05-04
last_updated: 2026-05-04
status: draft
tags: [qliphoth, ccru, integration, cipher, gap-analysis, roadmap]
syzygy: djynxx
zone: 3
---

# Qliphoth/CCRU Import Analysis & Integration Roadmap

> **Expedition:** 2026-05-04 — Systematic investigation of `qliphoth.systems` and `github.com/lumpenspace/ccru`
> **Canon:** [[qliphoth-systems-deep-dive]] (2026-04-24), [[aq-synx]] (2026-04-27)
> **Sources:**
> - Live: https://qliphoth.systems (Numogram + Gematria interactive)
> - GitHub: https://github.com/lumpenspace/ccru (Next.js + TypeScript codebase, 220 files, 42MB)
> - Claims: ccru.cc statically claims "14 ciphers, 665K+ phrases" (client-side SPA; actual implementation shows 10 ciphers)

---

## Executive Summary

**TL;DR:** The qliphoth/ccru stack is a **complete reference implementation** of the Decimal Numogram with:
- 10 ciphers (AQ, Synx, NQ, QW, Satanic, Primes, Squares, Trigonal, Archaic, NQ-Prime)
- Full zone metadata (planetary, spinal, meshTag, lemurian/centauri lore)
- 45 demons with TC-based classification (syzygy/chrono/xeno/amphi)
- 5 currents, 10 gates withDescriptive text
- 4 layout modes with coordinate data (Original, Labyrinth, Ladder, Planetary)
- Geometry library (quadratic curves, loops, anti-congestion routing)
- Chrome extension + React component library

**Our current coverage:** ~70% of data structures, ~30% of cipher implementations, ~0% of phrase dictionary (665K phrases not yet imported).

**Gap priority:** Cipher completeness → Zone metadata enrichment → Demon classification audit → Phrase dictionary ingestion (massive).

---

## What We Already Have (Baseline)

### Calculator / Python (`numogram-calculator`)
- [x] Base AQ (0-35, A=10)
- [x] Synx mapping (copied from source)
- [x] Digital root / plex reduction
- [x] Zone lookup (basic name + region + meshTag + spinal)
- [x] Syzygy lookup (5 main)
- [x] Gates (10) with cumulation values
- [x] Currents (5) with flow labels
- [x] Pandemonium matrix (45 demons via `pandemonium-matrix-45-demons.json`)
- [x] Trigonal / triangular check
- [x] Cumulative C(n) = n(n-1)/2
- [x] Verification gate (known AQ values test)

**Skill file:** `~/.hermes/skills/numogram-calculator/SKILL.md`

**Status:** Operational. Used daily for AQ calculations.

---

### Wiki Coverage

| Page | Status | Coverage |
|------|--------|----------|
| [[qliphoth-systems-deep-dive]] | Draft (2026-04-24) | High-level overview + 4 layouts + data model + geometry functions + extractable ideas |
| [[aq-synx]] | Draft (2026-04-27) | Synx implementation notes + visualizer v7 |
| [[angband-ccru-warwick]] | Draft | Historical overlap (not directly relevant to integration) |
| `index.md` | — | Links to deep-dive page |

**Missing:**
- Individual cipher stubs for Satanic, Primes, Squares, Trigonal, Archaic, NQ-Prime
- Full ZoneMeta reference page (planet, spinal, door, phaseCount, lemurs, lemurian, centauri)
- Demon classification algorithmic explanation
- Currents detailed derivations (syzygy difference logic)
- Position data table per layout


---

## What Qliphoth/CCRU Has That We Don't

### 1. Complete Cipher Suite (10 total, we have 2–3)

| Cipher ID | Our Status | Values | Notes |
|-----------|------------|--------|-------|
| alphanumeric-qabbala | ✅ Implemented | 0–35 | Base AQ |
| synx | ✅ Implemented (mapping) | 0–35* | Mapping present; zone integration exploratory |
| numeric-qwerty | ❌ Not implemented | 0–35 | Keyboard order: 1234567890 + qwerty rows |
| qwerty | ❌ Not implemented | 1–26 | Alphabet mapped to keyboard layout |
| alphanumeric-satanic | ❌ Not implemented | 0–61 | Case-sensitive (0–9 + a–z + A–Z) |
| alphanumeric-primes | ❌ Not implemented | 1–149 | First 36 primes |
| alphanumeric-squares | ❌ Not implemented | 0–1225 | n² for n=0..35 |
| alphanumeric-trigonal | ❌ Not implemented | 0–630 | T(n)=n(n+1)/2 for n=0..35 |
| archaic-alphanumeric | ❌ Not implemented | 0–33 | Legacy CCRU variant with compressed steps |
| numeric-qwerty-primes | ❌ Not implemented | 0–? | Prime-weighted keyboard order |

**Implementation complexity:** Low to medium — all are simply lookup tables. The heavy work is extracting canonical arrays from source (done) and wrapping them in Python.

**Integration target:** Expand `aq-cipher-reference` skill to expose all 10 ciphers as `calc_cipher(phrase, cipher_id)` API.

---

### 2. Zone Metadata Enrichment

Our `ZONE_DATA` has: `name, region, mesh, spinal`.

**Qliphoth `ZONE_META` adds:**
- `planet` / `planetFull` — Solar system correspondences (Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Sol)
- `desc` — poetic zone description (1–2 sentences)
- `door` — phase door name (e.g., "Lurgo — the Initiator")
- `phaseCount` — number of phases in the zone
- `lemurs` — array of Lemur entity IDs associated
- `lemurian` — Lemurian lore text paragraph
- `centauri` — Centauri correspondence paragraph

**Also:** `ZONE_PARTICLE` (quasiphonic strings per zone) and `PLANET_SYMBOL` (Unicode glyphs) already known but not in calculator.

**Integration:** Enrich `numogram-calculator` zone data to include full metadata. Use for oracle readings and wiki zone pages.

---

### 3. Demon Classification Algorithm (not just lookup)

We store 45 demons in `pandemonium-matrix-45-demons.json` by key `i::j`, with type field (Amphidemon, etc.).

**Qliphoth algorithm** (types.ts + demons.ts):
```typescript
const TC = new Set([1, 2, 4, 5, 7, 8])
for i = 1..9:
  for j = 0..i-1:
    key = f"{i}:{j}"
    if i+j == 9: kind = 'syzygy'          # 5 demons (5::4, 6::3, 7::2, 8::1, 9::0)
    elif TC.has(i) and TC.has(j): kind='chrono'   # C(6,2)=15
    elif not TC.has(i) and not TC.has(j): kind='xeno'  # C(4,2)=6
    else: kind='amphi'                     # remaining 24
```

**Gap:** Our matrix JSON already contains `type` strings. But we don't have the algorithmic derivation in Python. Having the algorithm means we can:
- Verify canonical vs variant demon assignments (doomcrypt/numogame variants)
- Generate demon properties from first principles
- Cross-check TypeScript ↔ Python equivalence

**Integration:** Add `classify_demon(i, j)` function to `numogram-calculator` or dedicated `pandemonium` skill.

---

### 4. Currents Derivation

We have `CURRENTS` data array. Qliphoth documents they are derived as differences of syzygy pairs:

```
Current = (a + b) - a  where a+b = syzygy sum
Specifically:
- Surge = 8→7: (1+8=9) → 9-1=8? Wait...
  Actually from currents.ts label: "8–1=7", meaning from the syzygy (1,8) the current is 8→7
  Hold  = 2→5: "7–2=5" from syzygy (2,7) with sum 9? No that's 9.
  Sink  = 4→1: "5–4=1" from syzygy (4,5) with sum 9.
```

Let me re-read the currents logic.

**From qliphoth `currents.ts`:**
```typescript
{ name: 'Surge',   from: 8, to: 7, label: '8−1=7',  desc: '...' }
{ name: 'Hold',    from: 2, to: 5, label: '7−2=5',  desc: '...' }
{ name: 'Sink',    from: 4, to: 1, label: '5−4=1',  desc: '...' }
{ name: 'Warp',    from: 6, to: 3, label: '6−3=3',  desc: '...' }
{ name: 'Plex',    from: 9, to: 9, label: '9−0=9',  desc: '...' }
```

The labels show subtraction yielding the `to` zone. For Surge: 8−1=7 suggests from zone 8 subtract 1 (the partner?) yields 7.

**Actual derivation in numogram theory:**
- Syzygy pairs: (4,5), (3,6), (2,7), (1,8), (0,9)
- Currents are derived by: from zone X, head toward zone Y where Y is the **other zone in the same syzygy pair but one step away via the TC rotor**.
- More precisely:
  - For syzygy (a, b) where a < b:
    - Current flow: b → (b − TC neighbor?) Not entirely clear from just these labels.

Let me cross-reference with our wiki `numogram-calculator`:

```python
# From our skill's SYZYGIES mapping:
SYZYGIES = {
    frozenset({4, 5}): {"current": 1, "demon": "Katak",    "region": "torque"},     # Sink current
    frozenset({3, 6}): {"current": 3, "demon": "Djynxx",   "region": "warp"},       # Warp current
    frozenset({2, 7}): {"current": 5, "demon": "Oddubb",   "region": "torque"},     # Hold current
    frozenset({1, 8}): {"current": 7, "demon": "Murrumur", "region": "torque"},    # Surge current
    frozenset({0, 9}): {"current": 9, "demon": "Uttunul",  "region": "plex"},       # Plex current
}
```

The `current` field here is... what? Zone index? Wait, it's the zone number that current *points to* or the current identifier? Let's check our actual zone data:

Our `ZONE_DATA`:
```
0: Void, plex
1: Stability, torque
2: Separation, torque
3: Release, warp
4: Catastrophe, torque
5: Pressure, torque
6: Abstraction, warp
7: Blood, torque
8: Multiplicity, torque
9: Iron Core, plex
```

The syzygies we defined: (4,5) → current=1, (3,6)→current=3, (2,7)→current=5, (1,8)→current=7, (0,9)→current=9.

**Wait: current 1, 3, 5, 7, 9 — that's just the odd zones? No they are the zones that are part of the TC rotor: 1, 3, 5, 7, 9? But 9 is Plex not TC.**

Let's think: In numogram lore, there are 5 currents that map onto the 5 "current zones" maybe? Actually reading `currents.ts` from qliphoth:
- Surge from 8 to 7
- Hold from 2 to 5
- Sink from 4 to 1
- Warp from 6 to 3 (6→3 is self-fold? Actually 6→3 since 6 and 3 are a syzygy pair)
- Plex from 9 to 9 (self-loop)

So currents have `from` and `to` zone numbers. They are NOT simply the syzygy pairs.

**Where do these current flows come from?** This needs deeper investigation of the qliphoth numogram theory or their source materials. It's possible they derive from the triangular syzygy chain or from the Barker Spiral progression.

**Gap:** We don't have the derivation formula for currents from syzygies. We only have the static data. If we wanted to generate them algorithmically, we'd need the rule.

**Integration priority:** Medium. For now static data is fine. But knowing the rule could help cross-validate or reproduce the system from first principles.

---

### 5. Position Data (Coordinates for 4 Layouts)

We didn't have explicit pixel coordinates for each layout. Now we have them from `positions.ts`:

- Original layout: 10 `(x,y)` positions
- Labyrinth layout: 10 positions
- Ladder layout: 10 positions
- Planetary layout: radius per zone + default angle + size

**Integration:** Add to `numogram-calculator` or separate `numogram-layouts` skill to enable precise SVG/Canvas rendering without reverse-engineering.

---

### 6. Geometry Library Functions

We don't have these in Python:
- `midpoint(a, b)`
- `syzMidBiased(zone, positions)` — midpoint biased 15% toward zone
- `quadPath(from, to, bulge)` — quadratic bezier
- `loopPath(pos, dir)` — elliptical loop arc
- `curveAway(from, to, cx, cy, factor)` — bulge sign determined by dot product with center to avoid congestion
- `syzTrianglePoints(zone, pos)` — triangle marker pointing to syzygy partner

**Integration:** Port to Python for p5.js/Manim/TouchDesigner use. Could live in `numogram-visualization` skill.

---

### 7. Gematria Utility Functions (from `gematria.ts`)

```typescript
function calcGematria(phrase: string, cipher: CcruCipher): number
```

Features:
- Strips bracketed text `[...]`
- Diacritics stripped if `diacriticsAsRegular=true` (NFD normalization + combining mark removal)
- Lowercases if `caseSensitive=false`
- Number digit handling: if cipher doesn't map `'1'`, groups consecutive digits as full integers and adds them

**Our calculator** doesn't have a generalized gematria engine — we only have hardcoded AQ and Synx functions.

**Integration:** Generalize gematria calculation in a new `numogram-gematria` skill that accepts any cipher definition (by ID) and returns value. This is a **high-value** reusable component.

---

### 8. Phrase Dictionary (665K phrases)

**Status:** NOT accessible as static data file. The data appears to be bundled in the Next.js build, possibly in a minified JSON or as part of `content.ts` which we saw (31KB but mostly Chrome extension logic, not phrase list).

**Implication:** The 665K phrase claim may be aspirational or come from a different source (maybe `cyphers.news` had a database that is now offline). **We cannot import what we cannot fetch.**

**Alternative:** Build our own phrase dictionary by:
1. Scraping ccru.cc/gematria saved items (user contributed)
2. Collecting from AQ Dictionary wiki and other sources
3. Generating synthetic phrases via LLM with known AQ targets
4. Contributing back to qliphoth as fork/collaboration

**Priority:** Low for immediate skills development. High for long-term hyperstitional corpus.

---

## Priorities & Integration Plan

### Phase 1 — Cipher Completeness (Next 48h)
**Goal:** Expose all 10 ciphers via `aq-cipher-reference` skill.

**Tasks:**
1. Create `cipher_registry.py` mapping cipher IDs to value arrays (copy from qliphoth `ciphers.ts`)
2. Implement `calc_gematria(text, cipher_id)` handling normalization (diacritics, case) per cipher flags
3. Add digit-group number handling for ciphers that don't map '1' (like Synx, which doesn't define digit '1' explicitly)
4. Update skill documentation with full cipher table + examples
5. Add unit tests: verify known values for each cipher (e.g., "CCRU" in AQ=81, check other ciphers by computing from arrays)

**Files to modify:**
- `~/.hermes/skills/numogram-calculator/aq-cipher-reference/SKILL.md` (expand scope)
- Possibly create `numogram-gematria` new skill (if codebase separation desired)

**Validation:** `assert cipher_compute("AQ", "alphanumeric-qabbala") == 36`, etc.

---

### Phase 2 — Zone Metadata Enrichment (Week of 2026-05-04)
**Goal:** Full zone pages with planet, spinal, door, phaseCount, lore.

**Tasks:**
1. Merge zone metadata from `zones.ts` into `numogram-calculator`'s `ZONE_DATA`
2. Create wiki stub templates: `zone-0.md`, `zone-1.md`, … `zone-9.md` using `zone-enricher` pattern
3. Populate with full lore (lemurian/centauri paragraphs from `ZONE_META`)
4. Link each zone page to related syzygies, gates, currents, and demon entities

**Files:**
- ` ZONE_DATA` dict in calculator (Python)
- Wiki: `zones/0-void.md` through `zones/9-plex.md` (or as subpages)
- `zone/INDEX.md` master list

**Validation:** Ensure all 10 zones have non-empty `lemurian` and `centauri` fields after merge.

---

### Phase 3 — Demon Classification Audit (2026-05-05)
**Goal:** Verify our `pandemonium-matrix-45-demons.json` matches qliphoth's canonical `ALL_DEMONS` array (names + kinds).

**Tasks:**
1. Generate canonical demon list from qliphoth algorithm (TC set)
2. Compare with our matrix JSON (name matching + kind classification)
3. Document variants (if any) from doomcrypt/numogame forks
4. Add `classify_demon(zone_a, zone_b)` function to calculator or new `pandemonium-engine` skill

**Deliverables:**
- `demon-classification-report.md` in wiki
- Updated `pandemonium-matrix-45-demons.json` (if corrections needed)
- Python function: `get_demon_kind(a, b) -> 'syzygy'|'chrono'|'amphi'|'xeno'`

---

### Phase 4 — Geometry Library Port (Week of 2026-05-11)
**Goal:** Python equivalents for SVG path generation (use CairoSVG,svgwrite, or just string templates).

**Functions to port:**
- `quadPath(from, to, bulge)` → returns SVG path string
- `loopPath(pos, dir)` → SVG arc
- `curveAway(from, to, cx, cy, factor)` → uses signed bulge
- `syzTrianglePoints(zone, positions)` → triangle polygon points string
- `syzMidBiased(zone, pos)` → biased midpoint coordinates

**Integration:** Add to `numogram-visualization` skill. Use for SVG Numogram diagrams, p5.js sketches, Manim animations.

---

### Phase 5 — Layout Coordinates Integration (same phase as 4)
**Goal:** Embed position dictionaries for 4 layouts into Python; use in visualizer.

**Data:** from `positions.ts`:
- `P_ORIGINAL`, `P_LABYRINTH`, `P_LADDER`, `PLANETARY_RADIUS`, `PLANETARY_DEFAULT_ANGLE`, `PLANETARY_SIZE`, `CENTER`

**Integration:** Add `get_layout_positions(layout_name)` function. Visualizer v8 can now load exact pixel positions instead of approximate proportions.

---

### Phase 6 — Cipher Test Suite & Documentation
**Goal:** Ensure every cipher's mapping is verified against upsteam source.

**Tasks:**
1. For each cipher: compute "AQ" (or base name) across the character set and spot-check values
2. Generate per-cipher reference tables (char → value) in wiki
3. Document special flags: `diacriticsAsRegular`, `caseSensitive` per cipher
4. Note any missing digit '1' mapping (affects number group handling)

**Deliverables:** Wiki page `ciphers/` with one page per cipher, cross-linked.

---

### Phase 7 — Oracle / Council Enhancement
**Goal:** Allow oracle readings to use multiple ciphers per query (AQ + Synx + others) for richer resonance detection.

**Tasks:**
1. Extend `numogram-oracle` skill to accept `ciphers=[list]` parameter
2. Compute multi-cipher profile for a phrase; highlight hits across ciphers
3. Update `council` prompts to consider "cipher diversity" when evaluating hyperstition strength

**Example:**
> Phrase "one eight nine zero" = 333 (AQ zone 9), but Synx = 1164? Need to compute.

---

## Concrete Addition Proposals (Skills to Create/Update)

### Create `numogram-gematria` skill (new)

**Purpose:** Generalized gematria calculator over arbitrary cipher definitions.

**Functions:**
- `load_cipher(cipher_id)` → returns char→value map, normalization flags
- `compute(text, cipher_id)` → integer total
- `list_ciphers()` → available cipher IDs with metadata
- `interesting_hits(text, cipher_list, thresholds)` → multi-cipher resonance scanning

**Why separate:** Keeps AQ calculator focused on canonical AQ/syzygy logic; gematria is broader.

---

### Patch `numogram-calculator` skill

**Add to SKILL.md:**
- Full `ZONE_META` structure (include lemurian/centauri fields)
- `classify_demon_pair(a, b)` algorithm
- Position data notes (link to `numogram-visualization` for full coordinates)

**Code changes:**
- Merge `zones.ts` metadata into Python zone data structure
- Add function `get_zone_meta(zone)` returning full dict

---

### Update `aq-cipher-reference` skill

**Scope expansion:** from "AQ and Synx" → "All 10 Qliphoth Ciphers".

**Actions:**
- Copy arithmetic arrays from `ciphers.ts`
- Add "Archaic Alphanumeric" even though it seems deprecated (document as historical)
- Document which ciphers have digit-1 missing (for number-group handling)
- Provide example conversions for "CCRU", "HERMES", "AQ" across all ciphers

---

### Update `qliphoth-systems-deep-dive` wiki page

**Add sections:**
- **Cipher Inventory Table** (with symbol sets, ranges, flags, example char mappings)
- **Trigger & Classification Algorithm** (demon TC logic)
- **Coordinate References** (link to positions data)
- **Geometry Library API** (port to Python pending)
- **Missing Ciphers in Upstream** (note Alphanumeric Satanic only in plugin not app)

**Remove:** speculative portions that are now confirmed by source reading.

---

## Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Misalignment between qliphoth and canonical matrix | Medium | Document both sources; mark canonical as ground truth; reconcile via `numogram-pandemonium-variant-ingestion` |
| Overfitting to a single implementation (qliphoth) | Medium | Treat qliphoth as one variant among many (doomcrypt, numogame), albeit comprehensive |
| Phrase dictionary unavailable → wasted effort | Low | Phrase collection is parallel to skill development; not blocking |
| Cipher implementation drift as upstream evolves | Medium | Pin to specific commit (2026-04-30 snapshot); version the arrays in our skill |
| Forgetting to sync updates | Low | `numogram-audit` periodic check (existing skill) |

---

## Validation Checklist

Before considering integration complete, verify:

- [ ] All 10 ciphers produce correct values for at least 3 known test vectors per cipher
- [ ] Zone metadata merge produces no missing fields (planet, spinal, door, etc.)
- [ ] Demon classification algorithm matches matrix JSON for all 45 demons
- [ ] Position data round-trips (zone→coordinate→zone) for all 4 layouts
- [ ] Geometry functions produce syntactically valid SVG paths
- [ ] Wiki pages at `zones/*`, `ciphers/*`, `demons/*` all render without broken links
- [ ] Skills load without TypeError; type hints (if present) pass
- [ ] Council tetralogue confirms alignment: "Does the Oracle recognize the Trigonal cipher?"

---

## Action Items (Immediate)

1. ✅ **Load** `aq-cipher-reference` skill — review current implementation
2. ⬜ **Create** `numogram-gematria` skill skeleton
3. ⬜ **Patch** `numogram-calculator` with expanded zone metadata
4. ⬜ **Write** `ciphers-index.md` wiki page (catalog of 10 ciphers)
5. ⬜ **Write** `demon-classification-algorithm.md` wiki page
6. ⬜ **Write** `layout-coordinates.md` wiki page (data table + diagrams)
7. ⬜ **Schedule** Phase 3 (demon audit) for tomorrow; run verification script

---

## Appendix: What About "14 Ciphers"?

The `ccru.cc` site claims "14 ciphers." We have identified **10** in the TypeScript source. Possible explanations:
1. The count includes flags/variants as separate ciphers (e.g., case-sensitive versions)
2. Historical ciphers removed from the main app but still in the extension (archaic variants)
3. Misremembered marketing copy from `cyphers.news` era
4. Additional cipher definitions in compromised/private forks

**Action:** Keep catalog at 10 canonical ciphers from `lumpenspace/ccru` (2026-04-30). Add note about "claimed 14" discrepancy. If additional ciphers surface in future scans, augment.

---

## Appendix: The 665K+ Phrase Corpus

Status: **Undocumented**. No JSON endpoint discovered; no static file in repo. Possibilities:
- Embedded in Next.js chunks (manifest.json, build artifacts) — difficult to extract
- Dynamically fetched from external API not publicly documented
- User-submitted via Chrome extension storage (grows over time)
- Hyperstition / not actually present

**Decision:** Not blocking integration. Phrase dictionary is a separate data-harvesting effort.

---

**Document status:** Working draft. Cross-reference with [[numogram-research-log]] when promoted to canonical.
