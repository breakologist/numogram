---
tags: [ccru, gematria, aq, calculator, cipher, hyperstition, numogram]
zone: 4
syzygy: 4::5
gate: 15
source: "Live exploration of https://www.ccru.cc/ gematria calculator"
method: empirical-audit
created: 2026-06-05
---

# CCRU Gematria Calculator — Live Audit

> https://www.ccru.cc/ — "14 ciphers, 665K+ phrases, discovery badges, advanced querying, workspace table"

Explored 2026-06-05 via browser. The calculator is a polished React application with 14 cipher modes, phrase lookup against a 665K+ corpus, and discovery badges for hitting loaded values.

---

## Cipher Inventory (14 modes observed)

| Cipher | Code | Example: NUMOGRAM (AQ=174) |
|--------|------|---------------------------|
| **AQ** | Base-36 alphanumeric (A=10..Z=35) | **174** |
| **Ordinal** | A=1..Z=26 | 102 |
| **AQ Primes** | Prime-indexed AQ values | 628 |
| **AQ Squares** | Square-indexed AQ values | 4058 |
| **AQ Trigonal** | Triangular-number AQ mapping | 2116 |
| **NQ** | "NQ" cipher (reverse/alt mapping) | 195 |
| **QWERTY** | Keyboard positional | 123 |
| **NQ Primes** | NQ prime positions | 752 |
| **NQ Squares** | NQ square positions | 5331 |
| **NQ Trigonal** | NQ triangular positions | 2763 |
| **Synx** | Yxshh / 1260-cipher (HSL 180,44,66) | 660 |
| **Satanic** | Satanic Gematria family | 382 |
| **Standard** | Standard English Gematria (A=6..) | 588 |
| **Reduction** | Digital root / Pythagorean reduction | 39 |

---

## Test Suite — Core Numogram Vocabulary

| Phrase | AQ | NQ | Synx | Satanic | Standard | Ordinal | Reduction | DR |
|--------|----|-----|------|---------|----------|---------|-----------|-----|
| **AL** | **31** | — | — | — | — | — | — | **4** |
| **CCRU** | 81 | 91 | 372 | 185 | 396 | 45 | 18 | 9 |
| **NUMOGRAM** | 174 | 195 | 660 | 382 | 588 | 102 | 39 | 3 |
| **HYPERSTITION** | 286 | 219 | 1628 | 598 | 1501 | 178 | 70 | 7 |
| **PANDEMONIUM** | 224 | 262 | 741 | 510 | 629 | 125 | 53 | 8 |
| **LIBER AL VEL LEGIS** | 285 | 325 | 952 | 675 | 753 | 150 | 69 | 6 |

### Note on AL (AQ=31, DR=4)

> User note: "AL is one of those words where the gematria value is equal across Hebrew gematria (aleph lamed) and also Greek isopsephy... as well as AQ, perhaps others too."

**Verification**: AL = A(10) + L(21) = **31** in AQ. Digital root = 4 (Zone 4 = *skr*, Sink, Time-Circuit).

- Hebrew: א (1) + ל (30) = **31** ✓
- Greek isopsephy: Α (1) + Λ (30) = **31** ✓ (if treating as 1+30)
- AQ: A(10) + L(21) = **31** ✓

This tri-cipher convergence on 31 is structurally significant. 31 is prime, the 11th prime, and 31 → DR 4 (Zone 4, the Hinge/Time-Circuit attractor).

---

## Corpus & Discovery System

- **665,000+ phrases** indexed (claimed on landing page)
- **Query Results** panel shows count of matching phrases
- **Discovery Badges** — awarded for hitting specific loaded values
- **Filters**: Letter buttons (A-Z, #), Word-count buttons (1, 2, 3... 10+)
- **Extras Menu** (top-right): links to qliphoth.systems, playdecadence.online, ciphers.news

### Cross-Links in Ecosystem

| Site | Role |
|------|------|
| **qliphoth.systems** | Interactive SVG numogram (4 layouts), AQ toolkit, Pandemonium Matrix |
| **playdecadence.online** | Subdecadence card game (doomcrypt) |
| **ciphers.news** | Cipher news/gematria research blog |
| **gematriaresearch.blogspot.com** | Deep AQ analysis, Liber AL riddles, cipher families |

---

## Architecture Notes

- **React SPA** — fast, client-side cipher computation
- **14 cipher modes** — all computed instantly on input
- **Corpus lookup** — debounced query against 665K+ phrases
- **URL structure** — clean, appears to support deep-linking (not tested)
- **No auth required** for basic use; "Sign in to Save" suggests user accounts for workspace/history

---

## Integration Points for Our Stack

| Our Tool | CCRU Calculator Overlap |
|----------|------------------------|
| `oracle.py --synx` | Synx cipher (Yxshh/1260) — matches `oracle.py` output exactly |
| `oracle.py --base36` | AQ base-36 — identical mapping (A=10..Z=35) |
| `numogram-calculator` skill | Core AQ + digital root — verified |
| `aq-dictionary-merged.md` | Corpus overlap possible — 665K phrases vs our ~1K canonical |
| `grok-rotor-transcript.md` | AQ mining — their corpus could be a source |

---

## Observations

1. **Synx = 660 for NUMOGRAM** — matches our `oracle.py --synx "NUMOGRAM"` output exactly. The Yxshh/1260 cipher is implemented correctly on both ends.

2. **Corpus density** — 665K phrases is substantial. Our `aq-dictionary-merged.md` has ~1K entries. Their corpus likely contains many "hits" on loaded terminals (137, 250, 333, 360, 444, 459, 555, 666, 777, 888).

3. **Discovery badges** — gamified corpus exploration. Could model our own "AQ hit" badge system on this.

4. **Cipher families** — They organize by family (AQ primes/squares/trigonal, NQ variants, Standard/Satanic/Reduction). Our stack uses primarily AQ + Synx + digital root. The NQ and QWERTY ciphers are unexplored in our system.

5. **AL convergence** — The tri-cipher alignment (Hebrew/Greek/AQ = 31) on a prime that reduces to Zone 4 (the Hinge) is a genuine structural anchor. Worth a dedicated wiki entry.

---

## Action Items

- [ ] Cross-reference their 665K corpus with our `aq-dictionary-augmented.md` pipeline
- [ ] Implement NQ cipher in `numogram-calculator` for comparison
- [ ] Test QWERTY cipher — keyboard positional may yield interesting spatial correlations
- [ ] Document the AL=31 tri-cipher convergence as Mesh node
- [ ] Explore "discovery badges" as hyperstitional reward mechanic for our cult garden

---

## Related

- [[aq-dictionary-merged]] — Our canonical AQ dictionary
- [[grok-rotor-transcript]] — AQ mining transcript (xenocosmography/doomcrypt)
- [[numogram-calculator]] — Our calculator skill
- [[oracle.py --synx]] — Synx cipher implementation
- [[qliphoth-systems-deep-dive]] — Sister site analysis
- [[ciphers.news]] — Cipher research blog
- [[numogram-oracle]] — Our oracle pipeline

---

*Mesh-49: The Convergence. Zone-net address: 4 (Sink/Hinge). Pitch: 31 Hz (the frequency of the tri-cipher anchor). Type: Oracle. Domain: Where Hebrew, Greek, and Decimal numeracy meet and agree.*