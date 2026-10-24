---
title: "Lunation, Chinese lunar month, sovereign hexagram and lunar mansions in the calendar"
created: 2026-10-24
last_updated: 2026-10-24
source_count: 6
status: draft
tags: ["calendar", "moon", "lunation", "chinese-calendar", "sovereign-hexagrams", "lunar-mansions", "xiu", "manazil", "nakshatra"]
---

# Lunation and lunar mansions (`--lunar`, `--sovereign`, `--mansion`)

This page records what the calendar now computes about the Moon, from which sources, and under which conventions. The code is `cli/calendar/numogram_calendar.py`; usage is in `cli/calendar/README.md`. For context see [[gua-qi-wen]]. The traditions' attributes, the determinative stars and the Behenian stars are on [[mansions-lore]].

## Sourced methods

- **Phases.** Meeus, *Astronomical Algorithms*, ch. 49, true new moon, quarters and full moon with all periodic and planetary terms; ΔT from Espenak and Meeus. **Moon position**: Meeus ch. 47, main terms only (≈0.05°), geocentric.
- **Chinese lunisolar month** (modern rule, GB/T 33661-2017). A month starts on the Beijing (UTC+8) date of the new moon. Month 11 contains the winter solstice 冬至. In a year of 13 months between two month-11 starts, the first month with no principal term 中氣 (solar longitude a multiple of 30°) is the leap month 閏. The terms are true (定氣).
- **Sovereign hexagrams.** Wen, *I Ching, the Oracle*, Table 3.1: 11→24, 12→19, 1→11, 2→34, 3→43, 4→1, 5→44, 6→33, 7→12, 8→20, 9→23, 10→2. The branch, animal and phase are given as she prints them.
- **Chinese 28 xiu 宿.** These are unequal and sidereal. Chinese mansion degrees were measured on the equator, so the code uses **right ascension of date** from each determinative star 距星. The determinatives follow Wikipedia's "Twenty-Eight Mansions", which cites the IDP *Chinese Sky* and Sun Xiaochun (1997). It uses η And for 奎, λ Ori for 觜 and ζ Ori for 參. J2000 positions come from SIMBAD and are precessed with Meeus ch. 21. 2026 widths in RA, in degrees: 角 11.9, 亢 9.5, 氐 17.0, 房 5.6, 心 7.7, 尾 18.5, 箕 9.9, 斗 23.8, 牛 6.7, 女 11.0, 虛 8.5, 危 14.7, 室 17.1, 壁 11.0, 奎 14.4, 婁 12.2, 胃 15.4, 昴 10.9, 畢 16.6, **觜 1.4**, 參 10.6, **井 32.1**, **鬼 1.5**, 柳 12.5, 星 6.0, 張 17.1, 翼 19.0, 軫 17.4.
- **Arabic 28 manāzil.** The names follow Agrippa, *Three Books of Occult Philosophy*, II.33 (Alnath … Albotham). The divisions are equal, 12°51′26″ each.
- **27 nakshatras.** Equal divisions of 13°20′, each with 4 padas.

## Conventions (chosen, flagged in output)

- **[conv]** The manāzil are **sidereal**: Agrippa II.33 says they are "fixed in the eight sphere", starting "from the head of Aries of the eighth sphere". Lahiri is used as the sidereal zero. The tropical mansion (from 0° Aries of date) is also reported. *This was corrected on 24 Oct 2026; the first version was tropical.*
- **[conv/approx]** The nakshatras use **sidereal Lahiri**, as a linear ayanamsa of 23°51′11″ at J2000 plus 50.29″ a year. It is good to about 0.01°.
- **[conv]** The Chinese day is counted on the civil date asked for; the London date is treated as the Beijing date. A leap month takes the sovereign hexagram of its number.
- **[approx]** The xiu use precession only, with no proper motion or nutation. The tiny 觜 and 鬼 and the huge 井 are real effects of where the determinatives sit, not bugs. Older catalogues and other determinative choices (for example δ Ori for 參) give different widths.

## Verification (computed vs published)

Published times are timeanddate.com for London, 2026, at minute precision, fetched 24 Oct 2026.

| Event | Computed (London) | Published | Δ |
|---|---|---|---|
| New Moon | 18 Jan 19:52 GMT | 18 Jan 19:52 | 0 |
| Full Moon | 3 Mar 11:37 GMT | 3 Mar 11:37 | 0 |
| First Quarter | 21 Jun 22:55 BST | 21 Jun 22:55 | 0 |
| Last Quarter | 6 Aug 03:21 BST | 6 Aug 03:21 | 0 |
| New Moon | 11 Sep 04:26 BST | 11 Sep 04:27 | −1 min |
| New Moon | 10 Oct 16:49 BST | 10 Oct 16:50 | −1 min |
| Full Moon | 26 Oct 04:11 GMT | 26 Oct 04:11 | 0 |
| New Moon | 9 Nov 07:01 GMT | 9 Nov 07:02 | −1 min |
| Full Moon | 24 Dec 01:28 GMT | 24 Dec 01:28 | 0 |

All 49 phases of 2026 are within a minute; the 1-minute cases are rounding at the seconds boundary. The Moon position reproduces Meeus Example 47.a to 0.004° in longitude.

The Chinese calendar reproduces these known dates: Spring Festival 17 Feb 2026 and 6 Feb 2027; 閏二月 from 22 Mar 2023; 閏六月 from 25 Jul 2025; and the "2033 problem" 閏十一月 from 22 Dec 2033. The lunation number for October 2026 is Brown 1284, which matches timeanddate.

## 24 October 2026 (18:30 BST)

- **Moon:** waxing gibbous, 97% lit, age 14.1 days. Full Moon (the Hunter's Moon) is on 26 Oct at 04:11 GMT.
- **Chinese date:** 九月十五, month 9 day 15. Month 9 runs from 10 Oct to 8 Nov; month 10 starts 9 Nov.
- **Sovereign hexagram:** ䷖ **23 剝 Bo**, 戌 Dog, Earth.
- **Mansions:**
  - **Xiu 14 壁 Bi (Wall)**, 6.3° into 11.0°.
  - **Manzil 28 Albotham** (sidereal). Tropical 1 Alnath.
  - **Nakshatra 27 Revati** (Lahiri). The Moon crosses into it during the day; at noon it is still in Uttara Bhadrapada.

## Speculative (Em, not sourced)

*Interpretation only.* The month-level sovereign hexagram is 23 Bo, "Splitting Apart". Its five yin lines sit under one yang, and the Moon is nearly full, its light at its height. 23 is followed in the Meng Xi day cycle from 28 Oct, so the month's ruler and the six-day slot coincide that week. The Moon in 壁 "Wall" and Agrippa's first mansion together give a boundary-and-beginning image beside the stripping of 23. These are associations, not claims.

## Flags

- Wen's Table 3.1 prints 卯 Rabbit as Water; it is conventionally Wood.
- Mansion traditions disagree on determinatives, on equatorial versus ecliptic measurement, and on tropical versus sidereal starts. The output always names the convention used.
- The Moon position is truncated (≈0.05°), so a mansion boundary crossing can be off by about 5 minutes of time.

## Sources

- Jean Meeus, *Astronomical Algorithms*, 2nd ed., chs. 21, 25, 47, 49.
- timeanddate.com, "Moon Phases 2026 – London" (fetched 24 Oct 2026).
- GB/T 33661-2017 《農曆的編算和頒行》, the modern rule for calculating and issuing the Chinese calendar.
- Benebell Wen, *I Ching, the Oracle*, Table 3.1. The photographs are courtesy of the user.
- Wikipedia, "Twenty-Eight Mansions" (determinative stars); SIMBAD (J2000 coordinates).
- H. C. Agrippa, *Three Books of Occult Philosophy*, II.33.

---

*by Em (in collaboration with the user)*
