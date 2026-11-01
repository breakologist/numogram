---
title: Tic Xenotation (TX) and Nullotation (0X)
created: 2026-11-01
tags: [xenotation, tic-xenotation, nullotation, barker, numerics]
status: sourced
---

# Tic Xenotation (TX) and Nullotation (0X)

Sourced reference page (Em, 1 Nov 2026). Facts are tagged. Speculation is labelled. Every example is computed by `scripts/tic_xenotation.py`.

## Sources
- **[Hyperstition 003538]** "The Tic Xenotation", Hyperstition blog, 7 Jul 2004, posted with comments by Nick Land ([link](http://hyperstition.abstractdynamics.org/archives/003538.html)). Revised as "Tic-Talk" in *Fanged Noumena* (Urbanomic, 2011).
- **[Hyperstition 005076]** "TX2+", 28 Feb 2005: Vauung's tic matrix of the first 127 primes ([link](http://hyperstition.abstractdynamics.org/archives/005076.html)).
- **[Hyperstition 005109]** "Nullified Xenotation" (0X), 2005, crediting the commenter Robin ([link](http://hyperstition.abstractdynamics.org/archives/005109.html)).
- **[Le 2019]** Vincent Le, "Nullotation", *Critique* 37 (2019) ([PDF](https://mvupress.net/wp-content/uploads/2022/12/Le-Nullotation.pdf)). Academic secondary source.
- **[ccru.net]** *Tick Delirium* ([occultures/barker1.htm](http://www.ccru.net/occultures/barker1.htm)) has the fiction only: Project-Scar (Borneo, 1980), "factor-strings", "Xenotation is clicking together". ccru.net has **no** notation rules.
- **[repo]** lumpenspace/ccru@7c38ad9 `app/lib/xenotation.ts`: encoder and decoder, plus a per-zone display (zone 1 shown as "n/a", zone 0 blank).

## Rules [Hyperstition 003538; repo]
1. `:` = a factor of **2**. So `:` = 2, `::` = 4, `:::` = 8.
2. **Implexion** `(x)` = the *n*th prime, where *n* is the number written *x*. This "raises the hyprime index by 1". So `(:)` = 3 (the 2nd prime), `((:))` = 5, `(::)` = 7 (the 4th prime), `(((:)))` = 11.
3. A number is written as its **factor string**, e.g. 55 = 5 × 11 = `((:))(((:)))`.
4. TX covers the naturals ≥ 2. Barker's **deplex** `(-P)` lowers the hyprime index by one: `(-P)(:)` = `:`, so 1 = `(-P):` and 0 = `((-P)):`. The repo instead shows 1 as "n/a" and 0 as blank.
5. The "hyprime mainline" is 2 → 3 → 5 → 11 → 31 → 127 → 709, with each step taking the prime whose index is the previous value. 709 = `((((((:))))))`.

**TX matrix 0–9** [Hyperstition 003538; matches the repo's zone display]:

| n | TX | 0X |
|---|----|----|
| 0 | `((-P)):` | — |
| 1 | `(-P):` | (empty: one is "consumed" by zero) |
| 2 | `:` | `()` |
| 3 | `(:)` | `(())` |
| 4 | `::` | `()()` |
| 5 | `((:))` | `((()))` |
| 6 | `:(:)` | `()(())` |
| 7 | `(::)` | `(()())` |
| 8 | `:::` | `()()()` |
| 9 | `(:)(:)` | `(())(())` |

## Nullotation (0X) [Hyperstition 005109; Le 2019]
- 0X **substitutes `()` for each TX `:`**. Only plexion remains, and the bracket structure is like building sets out of the empty set (Le compares it to Cantor).
- It is **lossless**: it is the same tree as TX, written differently.
- The post calls it a "complete break" from privileging binary powers, with "one" fused into "zero".
- Note: the form "`()` = 2, `(())` = 3" is **0X**, not TX. TX writes 2 as `:`.

## Computed checks (Em, 1 Nov 2026)
- 55 = `((:))(((:)))` ✓; 125 = `((:))((:))((:))` ✓; 36 = `::(:)(:)` ✓; 45 = `(:)(:)((:))` ✓; 1035 = `(:)(:)((:))((:)(:))`.
- **Error in source (Land's comment on 003538):** `::::(:(::))` decodes to 2⁴ × 43 = **688**, not 708 as written. 708 = `::(:)(((::)))`. His next point, that `((((((:))))))` is the 127th prime, 709, is correct.
- **Errors in the TX2+ prime list [005076]:** entry [066] 317 is given as `(((:::)))`, which is 331, the same string as entry [067]. Correct: **317 = `(:(:)(((:))))`**. Entry [090] 463 is given as `((((:)))(:)(:):)`. Correct: **463 = `(:(:)(:)((:)))`**. The remaining spot checks matched.

## Wiki pages corrected (dated notes)
- [[xenotation-triangle-rotation]] (86, 13, the nullotation rule, the "lossy" claim).
- [[text-recombination-engine]] (86, nullotation).
- [[base-36-meta-numogram-djynxxogram]] (Gt-36 and Gt-45 strings).
- [[qliphoth-systems]] and [[qliphoth-systems-deep-dive]]: the TX zone table and 125 are correct (checked).

## Speculation (labelled, Em)
- TX's 2-chains (`:`, `::`, `:::`) resemble the binary doubling that drives the [[time-circuit]] 1-2-4-8-7-5 cycle. 0X's break with "binary powers" could be read as a step out of the time-circuit. No source draws this link.
- The deplexed 0 and 1, outside TX proper, can be read against Plex-zone nullity. This is unsourced.

## Cross-links
[[daniel-barker]] · [[cryptolith]] (Vukorri Cryptoliths are cited as TX "isomorphs") · [[time-circuit]] · [[decadence]] · [[pandemonium]] · [[zone]] · [[lemurian-times-nexus]]
