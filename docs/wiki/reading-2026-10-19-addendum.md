---
title: "Reading — 19 October 2026, addendum (Crowley's court hexagrams, St Isaac Jogues, 4::5)"
created: 2026-10-19
last_updated: 2026-10-19
source_count: 4
status: draft
tags: ["reading", "calendar", "i-ching", "tarot", "crowley", "st-isaac-jogues", "katak", "speculative"]
---

# Reading — 19 October 2026, addendum

This is a companion page to [[reading-2026-10-19]], written by the same author and following the same rules: quotations are copied from fetched text, and *(speculative)* marks a reading, not a fact.

## 1. Crowley's court cards and the Yi King

**The ranks** (*The Book of Thoth*, archive.org text): "The Knights represent the powers of the letter Yodh in the Name." · "The Queens represent the letter He' of the Name." · "The Princes represent the Forces of the letter Vau in the Name." Knights are Fire, Queens Water, Princes Air and Princesses Earth (the final Heh). Cups are Water, so the card is "Prince of Cups, Air of Water".

**The card:** "In the Yi King, the airy part of Water is represented by the 61st hexagram, Kung Fû" (book-of-thoth.net transcription). Crowley adds: "for it is also a "big Li", the trigram of Sol formed by doubling the lines."

**Hexagram 61 中孚 Zhong Fu** is ☴ Xun (wind) above ☱ Dui (lake): wind over lake. Mountain over lake is 41 損, which Crowley gives to the Princess of Cups.

**The full table**, taken from the sixteen court-card entries:

| | Knight | Queen | Prince | Princess |
|---|---|---|---|---|
| Wands | 51 | 17 | 42 | 27 |
| Cups | 54 | 58 | **61** | 41 |
| Swords | 32 | 28 | 57 | 18 |
| Disks | 62 | 31 | 53 | 52 |

*Independently confirmed:* Simon Bastian's *Before Completion* (2022) prints the same sixteen Crowley numbers alongside his own elemental scheme. See [[bastian-before-completion]].

**The rule behind it.** This is my inference, not Crowley's own statement. The upper trigram comes from the rank: Knight ☳ thunder, Queen ☱ lake, Prince ☴ wind, Princess ☶ mountain. The lower trigram comes from the suit, using the same four trigrams: Wands ☳, Cups ☱, Swords ☴, Disks ☶. Checked against `KW_BY_VALUE` in `cli/iching.py`, this rule reproduces all sixteen numbers. The other Princes, quoted: Wands "the 42nd Hexagram, Yi"; Swords "the airy part of Air is represented by the 5 7 th hexagram, Sun" (archive.org OCR, i.e. 57); Disks "the 53rd hexagram, Kien".

**Hexagram 61 as a number.** The line value is 51, so zone 6 by lines, and KW 61 gives zone 7 by number. *(Speculative:* through the Prince of Cups, Crowley's hexagram for the day is 61, beside the gua qi's 36 Ming Yi.)

## 2. St Isaac Jogues and the North American Martyrs (feast 19 October)

The eight martyrs were René Goupil (d. 1642), Isaac Jogues (d. 18 October 1646), Jean de Lalande (d. 19 October 1646), Antoine Daniel (1648), Jean de Brébeuf and Gabriel Lalemant (1649), Charles Garnier and Noël Chabanel (1649). The names and dates are from Wikipedia, "Canadian Martyrs". They were canonised by Pius XI in 1930.

Points from the *Catholic Encyclopedia* article "St. Isaac Jogues" (New Advent):

- **Captured.** "He was taken prisoner on 3 August, 1642". "There he remained for thirteen months in slavery".
- **Escaped to France.** He "landed Christmas morning, 1643, on the coast of Brittany, in a state of absolute destitution".
- **The Mass dispensation: confirmed.** He "was allowed by Pope Urban VII the very exceptional privilege of celebrating Mass, which the mutilated condition of his hands had made canonically impossible; several of his fingers having been eaten or burned off. He was called a martyr of Christ by the pontiff." *(Note: Urban VII reigned only in 1590. The pope in 1644 was Urban VIII, so the text as transcribed is probably wrong here. The story itself stands.)*
- **The return.** "He followed the same route over which he had been carried as a captive."
- **Into danger.** "though fully aware of the danger Jogues continued on his way to Ossernenon, though all the Hurons and others who were with him fled except Lalande."
- **The death.** "On 18 October, 1646, when entering a cabin he was struck with a tomahawk and afterwards decapitated."

**Threads** *(speculative)*:
- Jogues died on 18 October and Lalande on 19 October. These are the two days of [[reading-2026-10-18]] and [[reading-2026-10-19]], both under Ming Yi.
- The line-6 image of Ming Yi, "no light, but (only) obscurity", fits a return into the dark. So does the count of Kî's "aim and mind correct" through captivity.
- The wounded hands kept for the Mass echo Legge's "Intelligence Wounded". Here the wound is kept and dispensed with, not hidden.

## 3. Today's 4::5 (Katak)

**The arithmetic (fact).** The tetragram index is head − 1, and the weights are 1, 3, 9, 27.
- **Today, 68:** `represent_tetragram(67)` = [1, 1, 1, 2] gives 1 + 3 + 9 + 54 = 67, so dr = 4 by lines. By number, dr(68) = 5.
- **Yesterday, 67:** [0, 1, 1, 2] gives 66, so dr = 3, and dr(67) = 4.

Today's pair is therefore 4 | 5, a syzygy (4 + 5 = 9). Yesterday's 3 | 4 is not.

**In the project's words.** [[zone-4]]: "**CCRU current fed by Zone 4** (its syzygy 4::5): **Sink**." [[syzygy]]: "| 1st | `4::5` | 1 | Time-Circuit | Katak |". [[zone-5]] places Katak, "the 4::5 carrier demon", at the boundary between the Time-Circuit and the Warp, because T₅ = 15 → 6. It also quotes Land: *"This is the age of Katak — it's the end of the cycle."*

*(Speculative:* the tetragram's two readings, lines against number, split exactly along the Sink syzygy on a "Dimming" day. Yesterday, "Darkening", sat at 3 | 4, one step into the Warp side.)

## Sources

- Crowley, *The Book of Thoth*: https://archive.org/stream/AleisterCrowleyTheBookOfThoth/Aleister+Crowley+-+The+book+of+Thoth_djvu.txt and the book-of-thoth.net transcription
- *Catholic Encyclopedia*, "St. Isaac Jogues": https://www.newadvent.org/cathen/08420b.htm
- Wikipedia, "Canadian Martyrs": https://en.wikipedia.org/wiki/Canadian_Martyrs

## See also

[[brebeuf-jogues]] · [[reading-2026-10-19]] · [[reading-2026-10-18]] · [[zone-4]] · [[zone-5]] · [[syzygy]] · [[hexagram-zone-mapping]]
