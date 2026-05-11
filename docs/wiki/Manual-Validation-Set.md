---
title: "Manual Validation Set — v0.8.3 Real Audio Listening"
created: 2026-05-11
status: in-progress
tags: [validation, listening, classifier, v083, real-audio]
---

# Manual Validation Set — v0.8.3 Real Audio

18 tracks: 14 selected across four populated zones with varied classifier confidence, plus 4 mystery tracks the classifier struggled with (<60% confidence). Listen to each track and note whether the zone assignment feels right, wrong, or ambiguous.

## How to Use

1. Find the track in your music library at the path listed
2. Listen (at least 60s, longer for ambient/drone pieces)
3. Record: **Zone [X] — Agree / Disagree / Ambiguous** + a sentence or two on why
4. If you disagree, suggest what zone it *should* be
5. Mystery tracks: the classifier was unsure — your ear is the tiebreaker

## Missing Zones — Synthetic Supplement Needed

The classifier did not assign any real tracks to Zones **0, 1, 3, 5, 7, 8**. These need synthetic MOD tracks composed with known zone parameters. A second phase of the validation set should generate 2-3 MOD tracks per missing zone for listening comparison.

| Zone | Name | Reason Missing |
|------|------|----------------|
| Z0 | Void | Near-silence — real music rarely has zero spectral activity |
| Z1 | Surge | Possibly conflated with Z2 (Separation) — adjacent in Time-Circuit |
| Z3 | Release | Warp zone — triangle-wave heavy, rare in popular music |
| Z5 | Pressure | Sink-adjacent — may bleed into Z4 or Z6 |
| Z7 | Blood | Fire/Noise zone — classifier struggles with noise (54% in v0.8.0) |
| Z8 | Multiplicity | High-register square wave — specific timbral signature |

---

## Tracks

### 1. Zone 2 — Separation [100.0%]
**File:** `Tarentel/[2002.06.04, TRR46] Ephemera - SINGLES 99-2000 [CD, compilation]/1 The Waltz.flac`
**Path:** `/run/media/etym/Extreme SSD/music/Tarentel/[2002.06.04, TRR46] Ephemera - SINGLES 99-2000 [CD, compilation]/1 The Waltz.flac`
**BPM:** 120 BPM | **Key:** G# | **Duration:** 180s

**Your verdict:** Zone [ 2] — Agree / ~~Disagree / Ambiguous~~

*Notes: things do feel held or in suspension with this one, separate isn't a bad descriptor,  with no drums for a while, and after ten minutes they arrive with the aforementioned waltz, feels like sunny amniotic days. Post-rockish. it's more peaceful than chaotic, lots of cymbals and quite ungrounded and warm feeling*

---

### 2. Zone 2 — Separation [98.9%]
**File:** `Don Caballero/1999 Singles Breaking Up/11 If You've Read Dr. Adder Then You Know What I Want.mp3`
**Path:** `/run/media/etym/Extreme SSD/music/Don Caballero/1999 Singles Breaking Up/11 If You've Read Dr. Adder Then You Know What I Want.mp3`
**BPM:** 132 BPM | **Key:** F | **Duration:** 66s

**Your verdict:** Zone [ 2] — Agree ~~/ Disagree / Ambiguous~~

*Notes: Interlude-feeling between song, the melodic elements lazily shift and woozily intermingle neither taking over. a bit like the geomantic figure Populus. The drums are busy but never driving*

---

### 3. Zone 2 — Separation [88.0%]
**File:** `Coil/1986 - Horse Rotorvator/07. Penetralia II.mp3`
**Path:** `/run/media/etym/Extreme SSD/music/Coil/1986 - Horse Rotorvator/07. Penetralia II.mp3`
**BPM:** 117 BPM | **Key:** E | **Duration:** 180s
(the only Penetralia II.mp3 i found was in /run/media/etym/Extreme SSD/music/Coil/1990 - Unnatural History (Compilation Tracks Compiled) (CD)/ )
**Your verdict:** Zone [2 seems fine ] — Agree ~~/ Disagree / Ambiguous~~

*Notes: the core is a distorted guitar riff, the drums sound like they're melting, but the pattern is the same, the music loops but each loop is different, due to dubbing/active mixing, while various male voices interject via some intercom, as the track progresses the drums pulse and throb more, the bass increases*

---

### 4. Zone 2 — Separation [75.0%]
**File:** `Bola/2002 - Fyuti/02. Shoob,e.flac`
**Path:** `/run/media/etym/Extreme SSD/music/Bola/2002 - Fyuti/02. Shoob,e.flac`
**BPM:** 134 BPM | **Key:** F# | **Duration:** 180s

**Your verdict:** Zone [ 2] — Agree / ~~Disagree / Ambiguous~~

*Notes: this track floats in like a jellyfish in warm water, stuttering, shimmering, like a ghost. the drums and more driving elements accrete. then bass, it gets softly groovy about 1:30. dancey and melancholic by 2:30. 3:05 might be the closest this one will come to a traditional "drop" , winds down by 4:30. quite lovely, very IDM, of course*

---

### 5. Zone 2 — Separation [58.6%]
**File:** `Autechre-2006-12-28-part22.mp3`
**Path:** `/run/media/etym/Extreme SSD/music/Autechre/Autechre-2006-12-28-part22.mp3`
**BPM:** 106 BPM | **Key:** G | **Duration:** 180s

*Borderline — low confidence. The classifier is unsure.*

**Your verdict:** Zone [2 ] — Agree / ~~Disagree / Ambiguous~~

*Notes: ah now this one is a study in itself. an hour long, but i see you only have 180s as the duration so i'll talk about the first 3 minutes. it's got the soft fuzz or warm distortion and saturation of tape going on. something like a soft hardcore or IDM again. the bass is the melody here, drums are funky-o. a proper nice melody comes in 1:20 soul-ish and the bass harmonises nicely. quietly jubilant, but not ostentatious. like a blanket*

---

### 6. Zone 6 — Abstraction [100.0%]
**File:** `Madlib/Madlib - Madlib Medicine Show 3- Beat Konducta In Africa - 3. Intro.flac`
**Path:** `/run/media/etym/Extreme SSD/music/Madlib/Madlib - Madlib Medicine Show 3- Beat Konducta In Africa - 3. Intro.flac`
**BPM:** 94 BPM | **Key:** — | **Duration:** 180s

**Your verdict:** Zone [ ] — Agree / Disagree / Ambiguous

*Notes:*

---

### 7. Zone 6 — Abstraction [97.6%]
**File:** `Soundtracks/Tenchu/12 - Faraway (Ending Theme).flac`
**Path:** `/run/media/etym/Extreme SSD/music/Soundtracks/Tenchu/12 - Faraway (Ending Theme).flac`
**BPM:** 103 BPM | **Key:** E | **Duration:** 180s

**Your verdict:** Zone [ ] — Agree / Disagree / Ambiguous

*Notes:*

---

### 8. Zone 6 — Abstraction [88.0%]
**File:** `Basic Channel/Basic Channel - Enforcement (BC-01)/01. Cyrus - Enforcement.flac`
**Path:** `/run/media/etym/Extreme SSD/music/Basic Channel/Basic Channel - Enforcement (BC-01)/01. Cyrus - Enforcement.flac`
**BPM:** 132 BPM | **Key:** A# | **Duration:** 180s

**Your verdict:** Zone [ ] — Agree / Disagree / Ambiguous

*Notes:*

---

### 9. Zone 6 — Abstraction [79.0%]
**File:** `Sun Araw/2008 - The Phynx/03. Harken Sawshine.mp3`
**Path:** `/run/media/etym/Extreme SSD/music/Sun Araw/2008 - The Phynx/03. Harken Sawshine.mp3`
**BPM:** 102 BPM | **Key:** F# | **Duration:** 100s

**Your verdict:** Zone [ ] — Agree / Disagree / Ambiguous

*Notes:*

---

### 10. Zone 6 — Abstraction [61.0%]
**File:** `01 ダイアログ - 幻術使い.flac`
**Path:** `/run/media/etym/Extreme SSD/music/Soundtracks/01 ダイアログ - 幻術使い.flac`
**BPM:** 120 BPM | **Key:** C | **Duration:** 180s

*Borderline — low confidence. The classifier is unsure.*

**Your verdict:** Zone [ ] — Agree / Disagree / Ambiguous

*Notes:*

---

### 11. Zone 4 — Gate [80.0%]
**File:** `Soundtracks/Persona/17. Misfortune.mp3`
**Path:** `/run/media/etym/Extreme SSD/music/Soundtracks/Persona/17. Misfortune.mp3`
**BPM:** 106 BPM | **Key:** F# | **Duration:** 180s

**Your verdict:** Zone [ ] — Agree / Disagree / Ambiguous

*Notes:*

---

### 12. Zone 4 — Gate [56.0%]
**File:** `Ruins/06 - Manugan Melpp.mp3`
**Path:** `/run/media/etym/Extreme SSD/music/Ruins/06 - Manugan Melpp.mp3`
**BPM:** 110 BPM | **Key:** B | **Duration:** 180s

*Borderline — the classifier nearly split this between zones.*

**Your verdict:** Zone [ ] — Agree / Disagree / Ambiguous

*Notes:*

---

### 13. Zone 4 — Gate [53.4%]
**File:** `Soundtracks/Persona/15. Akachochin Shiraishi.mp3`
**Path:** `/run/media/etym/Extreme SSD/music/Soundtracks/Persona/15. Akachochin Shiraishi.mp3`
**BPM:** 120 BPM | **Key:** B | **Duration:** 180s

*Lowest confidence of any Zone 4 track.*

**Your verdict:** Zone [ ] — Agree / Disagree / Ambiguous

*Notes:*

---

### 14. Zone 9 — Plex [68.7%]
**File:** `Anonymous 4/11. Benedicamus domino.flac`
**Path:** `/run/media/etym/Extreme SSD/music/Anonymous 4/11. Benedicamus domino.flac`
**BPM:** 123 BPM | **Key:** F# | **Duration:** 180s

*The only track the classifier assigned to the Plex.*

**Your verdict:** Zone [ ] — Agree / Disagree / Ambiguous

*Notes:*

---

## Mystery Tracks — The Classifier Was Unsure

These tracks scored <60% confidence. The classifier couldn't decide. Your ear is the tiebreaker.

---

### M1. Mystery [47.4% → Z2]
**File:** `Autechre Productions 1992-2016/13. Track Star.flac`
**Path:** `/run/media/etym/Extreme SSD/music/Autechre/Autechre Productions 1992-2016/13. Track Star.flac`
**BPM:** 110 BPM | **Key:** E | **Duration:** 57s

*Classifier says Z2 at only 47.4%. What do you hear?*

**Your verdict:** Zone [ ] — Agree / Disagree / Ambiguous  →  Suggested zone: [ ]

*Notes:*

---

### M2. Mystery [32.0% → Z2]
**File:** `Soundtracks/30. Epilogue 1.mp3`
**Path:** `/run/media/etym/Extreme SSD/music/Soundtracks/30. Epilogue 1.mp3`
**BPM:** 123 BPM | **Key:** G | **Duration:** 180s

*Lowest confidence in the entire set. The classifier is barely above chance.*

**Your verdict:** Zone [ ] — Agree / Disagree / Ambiguous  →  Suggested zone: [ ]

*Notes:*

---

### M3. Mystery [50.5% → Z6]
**File:** `Soundtracks/Sekiro/09 淤加美の一族.flac`
**Path:** `/run/media/etym/Extreme SSD/music/Soundtracks/Sekiro/09 淤加美の一族.flac`
**BPM:** 140 BPM | **Key:** D | **Duration:** 115s

*Fence-sitter. Abstraction or something else entirely?*

**Your verdict:** Zone [ ] — Agree / Disagree / Ambiguous  →  Suggested zone: [ ]

*Notes:*

---

### M4. Mystery [51.8% → Z2]
**File:** `Soundtracks/Persona/18. Different Persons.flac`
**Path:** `/run/media/etym/Extreme SSD/music/Soundtracks/Persona/18. Different Persons.flac`
**BPM:** 140 BPM | **Key:** F# | **Duration:** 180s

*The title is fitting — the classifier thinks it might be something else.*

**Your verdict:** Zone [ ] — Agree / Disagree / Ambiguous  →  Suggested zone: [ ]

*Notes:*

---

## Summary Table

| # | Zone | Name | Confidence | BPM | Key | Verdict | Notes |
|---|------|------|------------|-----|-----|---------|-------|
| 1 | Z2 | Separation | 100.0% | 120 | G# | | |
| 2 | Z2 | Separation | 98.9% | 132 | F | | |
| 3 | Z2 | Separation | 88.0% | 117 | E | | |
| 4 | Z2 | Separation | 75.0% | 134 | F# | | |
| 5 | Z2 | Separation | 58.6% | 106 | G | | |
| 6 | Z6 | Abstraction | 100.0% | 94 | — | | |
| 7 | Z6 | Abstraction | 97.6% | 103 | E | | |
| 8 | Z6 | Abstraction | 88.0% | 132 | A# | | |
| 9 | Z6 | Abstraction | 79.0% | 102 | F# | | |
| 10 | Z6 | Abstraction | 61.0% | 120 | C | | |
| 11 | Z4 | Gate | 80.0% | 106 | F# | | |
| 12 | Z4 | Gate | 56.0% | 110 | B | | |
| 13 | Z4 | Gate | 53.4% | 120 | B | | |
| 14 | Z9 | Plex | 68.7% | 123 | F# | | |
| M1 | ? | Mystery | 47.4% | 110 | E | | |
| M2 | ? | Mystery | 32.0% | 123 | G | | |
| M3 | ? | Mystery | 50.5% | 140 | D | | |
| M4 | ? | Mystery | 51.8% | 140 | F# | | |

## Zone Summary

- **Z2 (Separation):** 5 tracks + 3 mystery candidates from 121 available
- **Z6 (Abstraction):** 5 tracks + 1 mystery candidate from 75 available
- **Z4 (Gate):** 3 tracks from 3 available (all of them)
- **Z9 (Plex):** 1 track from 1 available (the only one)
- **Z0, Z1, Z3, Z5, Z7, Z8:** 0 tracks — needs synthetic supplementation
