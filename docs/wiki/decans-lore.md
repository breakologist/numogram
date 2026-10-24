---
title: "Decan images and lunar mansions across translations: Agrippa (1651, Purdue) and Picatrix (Greer–Warnock, Attrell–Porreca)"
created: 2026-10-24
last_updated: 2026-10-24
source_count: 4
status: draft
tags: ["decans", "faces", "lunar-mansions", "manazil", "agrippa", "picatrix", "translation", "calendar"]
---

# Decans and mansions across translations

This page compares four texts. The user supplied the three modern editions as PDFs on 24 Oct 2026. Those three are **in copyright**, so this page uses only short quotes, attributed with edition and page, and otherwise summarises in Em's own words. The 1651 Agrippa is public domain. Companion pages: [[mansions-lore]] and [[lunation-and-mansions]].

## The editions

| Short | Edition | Status |
|---|---|---|
| **1651** | Agrippa, *Three Books of Occult Philosophy*, tr. "J.F." (London 1651), via esotericarchives.com (ed. J. H. Peterson) | public domain |
| **Purdue** | Agrippa, *Three Books of Occult Philosophy*, tr. Eric Purdue (Inner Traditions, 2021), translated from the 1533 Latin; foreword by Christopher Warnock | ©; PDF supplied by the user |
| **G–W** | *The Picatrix*, Liber Rubeus Edition, tr. and annotated by John Michael Greer and Christopher Warnock (Adocentyn Press, © 2010–11), from the Latin | ©; PDF supplied by the user |
| **A–P** | *Picatrix: A Medieval Treatise on Astral Magic*, tr. Dan Attrell and David Porreca (Penn State UP, Magic in History, 2019), from the Latin (Pingree's edition) | ©; PDF supplied by the user |

The page numbers below are the **PDF page numbers** of the supplied files. Printed page numbers are given where the PDF shows them.

Two other supplied PDFs could not be identified. `91245bbf…` (76 pages) and `8b5b6ad9…` (42.5 MB) are image-only or too large for this session's PDF reader, so they are not used here. All four texts compared are **Latin-tradition**. No Arabic *Ghāyat al-Ḥakīm* translation, such as Ritter and Plessner's 1962 German, was available, so an Arabic-versus-Latin comparison is not possible yet. The only Arabic forms here are the mansion names given in the G–W footnotes and on Peterson's 1651 page.

## Decans (faces)

### Two different image traditions

The Latin *Picatrix* (II.11) and Agrippa (II.37) use the same frame: 36 faces, with the Chaldean ruler order starting from Mars at Aries I. But they describe **different images** for most faces. Agrippa credits his images to "Teucer the Babylonian" and the Arabs (1651).

- **Agreement:** a few faces match closely between the two, for example Libra I (a man and a bird or pipe, justice for the weak), Capricorn II (seeking the impossible) and Aries III (the restless man with a gold bracelet).
- **Divergence:** many differ entirely, Scorpio I among them.

### Scorpio I (today; ruler Mars)

| Text | Image | Meaning |
|---|---|---|
| 1651 Agrippa (p.d.) | "a woman of good face and habit, and two men striking her" | "comliness, beauty, and for strifes, treacheries, deceits, detractations, and perditions" |
| Purdue (PDF p. 315) | a woman of good face and bearing, "along with two men beating each other" | decorum and beauty, and quarrels, ambushes, deceptions, slanders, destruction (summary) |
| G–W Picatrix II.11 (PDF p. 116) | a man with a lance in his right hand holding a man's head in his left | settlement, sadness, ill will, hatred (summary) |
| A–P Picatrix II.11 §24 (printed p. 118) | the same image | "the face of power, sadness, ill will, and enmity" |

**Translation differences:**

- **Purdue vs 1651.** In the 1651 text the two men strike *her*; in Purdue they beat *each other*. This changes the scene from violence against the woman to a brawl beside her. The Latin behind it needs checking. Purdue's version fits the "quarrels" in the meaning better.
- **G–W vs A–P.** G–W gives "settlement" where A–P gives "power". These are likely two readings of the same Latin word (perhaps *potestas* or *stabilitas*); not verified.

### Other notable decan differences (Purdue vs 1651; same Latin original)

Purdue is at PDF pp. 314–316.

- **Virgo I.** The 1651 meaning list ends with "peopling"; Purdue's ends with "plundering". These are opposite senses, probably *populatio*, which can mean either peopling or laying waste.
- **Virgo III.** The 1651 has "a white woman and deaf"; Purdue has a white woman and a "dead or old man". This looks like *surda* (deaf) against *mortuus* or a reordered phrase; Purdue's reading makes the "or an old man" clause parallel. In the same face, 1651 "depopulation of lands" becomes plundering of the earth in Purdue.
- **Capricorn I.** Purdue adds a **black** man with the woman ("a woman and black man, bearing full satchels"). The 1651 has just "a man carrying full bags".
- **Libra I and Gemini II.** The 1651 "Pipe" is a shepherd's pipe in Purdue; it is a reed in some Picatrix faces.

### In the calendar

`--decan` now prints both of these for the Sun's decan, kept in separate data files:

- the 1651 Agrippa text, public domain (`data/agrippa_decans.json`);
- Em's own one-line **paraphrase** of the Latin Picatrix image (`data/picatrix_decans_summary.json`). It is not translation text.

## Lunar mansions

### Boundaries: zodiacal or "eighth sphere"?

- **Picatrix (both translations), I.4:** the mansions are counted **from the first minute of Aries**, in equal 12°51′26″ parts, and every boundary is given as a zodiacal degree. In G–W (PDF p. 33ff) the footnotes read "That is, 0 degrees 0 minutes 0 seconds of Aries". A–P is at printed pp. 49–51.
- **Agrippa, II.33:** the 1651 text says "from the head of Aries of the eighth sphere". Purdue (PDF p. 308) also has it beginning "at the beginning of Aries in the eighth sphere". So Agrippa explicitly makes the mansions sidereal, while Picatrix states the degrees without that qualifier.
- **The calendar** keeps sidereal as its default, following Agrippa, and also reports the tropical/zodiacal count, which is the one that matches Picatrix as written. Today the difference matters: sidereal gives **28 Albotham/Arrexhe** and zodiacal gives **1 Alnath**.

### Today's mansions across the translations

**28. Albotham (Agrippa) / Arrexhe (Picatrix, Arabic al-Risha', "the cord"):**

- **1651:** "encreaseth Harvests and Merchandize, it secureth travellers through dangerous places; it maketh for the joy of marryed couples, but it strengthenth prisons, and causeth loss of treasures".
- **Purdue (PDF p. 310):** essentially the same list. The last item is "causes the ruin of treasures".
- **G–W (PDF p. 38):** images to increase trade, besiege cities, increase harvests, "to get rid of things and to destroy an area", lose treasures, travel safely by wagon, bring peace between husband and wife, secure prisoners, and harm sailors.
- **A–P (printed p. 51):** the same list, but where G–W has "to get rid of things and to destroy an area", A–P has **"to balance things, to ruin jokes"**. This is the most striking divergence: the two translations read the same Latin phrase completely differently. A check against Pingree's Latin is needed.

**1. Alnath:**

- **1651:** "causeth discords, and journies". **Purdue:** "used for journeys and discord".
- **Picatrix (G–W PDF p. 33; A–P printed p. ~49):** the sages of India began journeys and took medicine under Alnath. It is the root for images for safe travel and for sowing discord between spouses, friends and allies, and for making servants flee. A–P's phrase is "begin journeys and take medicine".

### Other mansion differences (Purdue vs 1651)

Purdue is at PDF pp. 308–310.

- **14 Achureth / Azimech (Spica).** The 1651 "causeth the love of martyred folk" becomes "strong for lovers marrying" in Purdue. The Latin is presumably *maritatorum* (of the married), misread in 1651 as martyrs. Picatrix G–W agrees with Purdue: "love of man and wife".
- **26 and 27.** The 1651 "first drawing" and "second drawing" are "First Drinking" and "Second Drinking" in Purdue. The Arabic al-Fargh is the spout of the water-bucket, so both readings point at water poured out.
- **3 Pleiades.** The 1651 "showring" is "the Raining" in Purdue. Both are "profitable to Saylors, Huntsmen, and Alchymists" (1651), "navigation, hunters, and alchemical operations" (Purdue).
- **18 Heart of Scorpio.** Purdue spells it "Akhas" where the 1651 has "Alchas". The meaning is the same: discord, sedition, conspiracy against princes.
- **Start degrees.** Purdue gives the 2nd mansion's start as 12°51′22″, the same as 1651. Picatrix G–W gives 12°51′26″ consistently.

The full 1651 list of mansion attributes is on [[mansions-lore]].

## Today, 24 Oct 2026, across the translations

- **Decan, Scorpio I:**
  - Agrippa 1651: two men "striking her".
  - Purdue: two men beating each other beside a fair woman.
  - Picatrix, both translations: a man with a lance and a severed head.
- **Mansion, sidereal 28:**
  - Agrippa 1651 and Purdue: harvests, trade, safe travel, marriage joy; prisons strengthened, treasure lost.
  - Picatrix: much the same list, with the phrase G–W renders "get rid of things / destroy an area" and A–P renders "balance things / ruin jokes".
- **Mansion, zodiacal 1:** Alnath, journeys and discord, in every version.
- **Chinese xiu:** 壁 Bi, Wall. It is not in these sources; see [[mansions-lore]].

## Speculative (Em, not sourced)

*Interpretation only.* Two lines of transmission split over today's decan: one shows a beheading, the other a woman between two violent men, and Purdue then turns the violence away from her. Under the "Wall" xiu and a stripping hexagram (23), the Picatrix image of the lance and the head reads as the sharper Martial one. That is an association, not a claim.

## Flags

- Page numbers are PDF page numbers, apart from the A–P printed pages shown. Check them against print before citing formally.
- The proposed Latin readings (*populatio*, *maritatorum*, *surda*/*mortuus*) are **Em's guesses** and have not been checked against Pingree or the 1533 Latin.
- Two of the supplied PDFs are unidentified (image-only, or too large to read here).
- The Picatrix summaries in the calendar are Em's paraphrases, not quotations.

## Sources

- Agrippa, *Three Books*, II.33 and II.37, tr. J.F. (1651): https://www.esotericarchives.com/agrippa/agripp2c.htm
- Agrippa, *Three Books of Occult Philosophy*, tr. Eric Purdue (Inner Traditions 2021), II.33 (PDF pp. 308–310) and II.37 (PDF pp. 314–316). PDF supplied by the user.
- *The Picatrix*, Liber Rubeus Edition, tr. Greer and Warnock (Adocentyn 2010–11), I.4 (PDF pp. 33–38) and II.11 (PDF pp. 114–118). PDF supplied by the user.
- *Picatrix: A Medieval Treatise on Astral Magic*, tr. Attrell and Porreca (Penn State UP 2019), I.4 (printed pp. 49–51) and II.11 (printed pp. 116–119). PDF supplied by the user.

---

*by Em (in collaboration with the user)*
