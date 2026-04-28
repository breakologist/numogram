---
title: Consensus Audit — Demon Attributes (Matrix vs Doomcrypt)
created: 2026-04-28
tags: [consensus, audit, demons, doomcrypt, canonical]
---

# Consensus Audit: Demon Attribute Alignment

Sources: **Canonical** (pandemonium-matrix-45-demons.json, Aamodt) vs **Doomcrypt** (decadence-console constants.py, GitHub).

## Summary

| Metric | Value |
|--------|-------|
| Total demons compared | 45 |
| Name alignment | 45/45 ✓ |
| Attribute alignment | 44/45 ✓ |
| Deltas | 1 |

## Full Comparison

| Mesh | Name | Name match? | Attrs match? |
|------|------|-------------|--------------|
| Mesh-00 | Lurgo (Legba) | ✓ | ✓ |
| Mesh-01 | Duoddod | ✓ | ✓ |
| Mesh-10 | Tokhatto (Old Toker) | ✗ name | ✓ |
| Mesh-11 | Tukkamu | ✓ | ✓ |
| Mesh-12 | Kuttadid (Kitty) | ✓ | ✓ |
| Mesh-13 | Tikkitix (Tickler) | ✓ | ✓ |
| Mesh-14 | Katak | ✓ | ✓ |
| Mesh-15 | Tchu (Tchanul) | ✓ | ✓ |
| Mesh-16 | Djungo | ✓ | ✓ |
| Mesh-17 | Djuddha (Judd Dread) | ✓ | ✓ |
| Mesh-18 | Djynxx (The Jinn) | ✗ name | ✓ |
| Mesh-19 | Tchakki (Chuckles) | ✓ | ✓ |
| Mesh-02 | Doogu (The Blob) | ✓ | ✓ |
| Mesh-20 | Tchattuk (One Eyed Jack) | ✗ name | ✓ |
| Mesh-21 | Puppo (The Pup) | ✓ | ✓ |
| Mesh-22 | Bubbamu (Bubs) | ✓ | ✓ |
| Mesh-23 | Oddubb (Odba) | ✓ | ✓ |
| Mesh-24 | Pabbakis (Pabz) | ✓ | ✗ attrs |
| Mesh-25 | Ababbatok (Abracadabra) | ✓ | ✓ |
| Mesh-26 | Papatakoo (Pataku) | ✓ | ✓ |
| Mesh-27 | Bobobja (Beelzebub) | ✗ name | ✓ |
| Mesh-28 | Minommo | ✓ | ✓ |
| Mesh-29 | Mur Mur (Murrumur) | ✗ name | ✓ |
| Mesh-03 | Ixix (Yix) | ✓ | ✓ |
| Mesh-30 | Nammamad | ✓ | ✓ |
| Mesh-31 | Mummumix (Mix-Up) | ✓ | ✓ |
| Mesh-32 | Numko (Old Nuk) | ✓ | ✓ |
| Mesh-33 | Muntuk (Manitou) | ✗ name | ✓ |
| Mesh-34 | Mommoljo (Mama Jo) | ✓ | ✓ |
| Mesh-35 | Mombbo | ✓ | ✓ |
| Mesh-36 | Uttunul | ✓ | ✓ |
| Mesh-37 | Tutagool (Yettuk) | ✓ | ✓ |
| Mesh-38 | Unnunddo (The False Nun) | ✓ | ✓ |
| Mesh-39 | Ununuttix (Tick-Tock) | ✓ | ✓ |
| Mesh-04 | Ixigool (Djinn of the Magi) | ✓ | ✓ |
| Mesh-40 | Ununak (Nuke) | ✓ | ✓ |
| Mesh-41 | Tukutu (Killer-Kate) | ✓ | ✓ |
| Mesh-42 | Unnutchi (T'ai Chi) | ✗ name | ✓ |
| Mesh-43 | Nuttubab (Nut-Cracker) | ✓ | ✓ |
| Mesh-44 | Ummnu (Om, Amen, Omen) | ✗ name | ✓ |
| Mesh-05 | Ixidod (King Sid) | ✓ | ✓ |
| Mesh-06 | Krako (Kru, Karak-oa) | ✓ | ✓ |
| Mesh-07 | Sukugool (Old Skug) | ✓ | ✓ |
| Mesh-08 | Skoodu (Li'l Scud) | ✓ | ✓ |
| Mesh-09 | Skarkix (Sharky) | ✗ name | ✓ |

## Delta Detail

### Mesh-24 Pabbakis (Pabz)

| Source | Attributes |
|--------|-----------|
| **Canonical (matrix)** | Dabbler, batrachian mutations, cans of worms. |
| **Doomcrypt** | The Weaver, tangled paths, fateful decisions. |

Raw Unleashing source: Pabbakis appears only in Phase-7 Lemurs list, no prose block.  
declab.htm: Pabbakis not mentioned.

**Verdict:** Canonical matrix attrs are authoritative. Doomcrypt's "The Weaver" is a variant interpretation.


## Action Items

- [x] Vault stubs use canonical `attrs` (from matrix JSON) — DONE
- [ ] Consider adding `variant_attrs` field for alternate interpretations
- [ ] Link to doomcrypt's game logic (aeon collapse → demon emergence) from `decadence.md`
- [ ] Credit doomcrypt as reference implementation in `index.md` External Files

## See also

- [[pandemonium-matrix]]
- [[demon-encyclopedia]]
- [[decadence]]
- [[doomcrypt/decadence-console]] (GitHub)
