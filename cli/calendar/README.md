# numogram calendar

This tool takes a date and shows where it falls in five calendar systems, each with a numogram reading, plus three saints'-day layers (with the Catholic National Calendars for England and for Wales), Golden Dawn tarot attributions and a generated research prompt. It uses only the Python standard library (3.9+, needs `zoneinfo`) and follows the CLI style of `cli/oracle.py`: plain `--flags`, a usage docstring, and `--json` for piping.

The overlays, each selected by a flag (default, `--all` and `--daily` = all):

| Flag | What it shows |
|---|---|
| `--nma` | Nma 729-day cycle: day index, 6 base-3 digits, zone, and a Tai Xuan (head, appraisal) address |
| `--taixuan` | Tai Xuan calendar: head 1–81 and appraisal 1–9, or the extra appraisals 踦 Ji / 嬴 Ying |
| `--guaqi` | Han gua qi: Meng Xi's hexagram for the date, plus the cardinal hexagram line for the current solar term |
| `--decan` | Decan of the Sun: sign, decan, Chaldean ruler, Book T minor card (2–10), the sign's and ruler's Major Arcana trumps, the Book T court card whose span holds the Sun, zone |
| `--pata` | 'Pataphysical date: day, month, year E.P., weekday or hunyadi |
| `--pata-saints` | 'Pataphysical saint or feast of the day, with rank (Fête Suprême … Vacuation) |
| `--saints` | Catholic calendar for `--region` (default `england-wales`): General Roman Calendar with England & Wales transfers, plus the National Calendars for Wales and England |
| `--folk` | Folk saints and traditional days (curated, labelled unofficial) |

```
python3 calendar.py                      # today, 12:00 Europe/London, all overlays
python3 calendar.py --all --date 2026-12-21 --time 22:00
python3 calendar.py --nma --nma-epoch krakatau      # or unix (default), ktime, YYYY-MM-DD
python3 calendar.py --taixuan --tz Asia/Shanghai
python3 calendar.py --decan --json
python3 calendar.py --list               # overlays + ephemeris providers
python3 calendar.py --daily --date 2026-10-17       # compact morning reading, all overlays
python3 calendar.py --saints --pata-saints --folk
python3 calendar.py --saints --region wales         # or england, england-wales (default), general
python3 calendar.py --decan --trumps trad           # Strength XI / Justice VIII numbering
python3 calendar.py --daily --plain                 # no pictographic glyphs (--ascii: 7-bit only)
python3 -m unittest -v test_numogram_calendar
```

Example output is in `examples.txt`.

## Files and the `calendar.py` name
- **`numogram_calendar.py` holds all the logic.** It is named that way, not `calendar.py`, because a module called `calendar` would shadow the standard library's `calendar` module for any code imported from this directory. The module also never imports the stdlib `calendar` itself; it has its own Gregorian leap-year rule. That means it still works when this folder is on `sys.path`.
- **`calendar.py` is a launcher only.** It removes its own folder from `sys.path`, then loads `numogram_calendar.py` by file path. Don't `import calendar` from code that runs inside this folder.
- **To drop it into the repo,** copy `numogram_calendar.py` (and the tests) to `cli/`. Run it with `python3 cli/numogram_calendar.py ...`; it has its own `main()`. The wrapper is optional.

## Sourced, approximated, and speculative
Every output field carries one of four tags:
- `[src]`: the rule comes from a cited source.
- `[approx]`: a computed approximation of a sourced rule.
- `[conv]`: a convention this tool had to choose.
- `[spec]`: numogram speculation, not a sourced fact.

| Overlay | Sourced | Approximation or convention |
|---|---|---|
| **Nma** | 729-day "double-year" written as 6 base-3 digits; 3 intercalary days every second cycle (4 years) ([CCRU, Decimal Numogram](http://ccru.net/declab.htm); [CCRU glossary, "Zygotriadic Calendar"](http://www.ccru.net/id%28entity%29/glossary.htm)) | **CCRU gives no epoch.** Default 1970-01-01 follows the only published implementation I found, the [xeno.cx zygotriadic calendar](https://xeno.cx/posts/zygofaq), which is a modern reconstruction, not CCRU. Alternatives: `krakatau` 1883-08-27 and `ktime` 1900-01-01 (both [spec]), or any date. The 3 intercalary days are placed at the end of each 1461-day supercycle [conv]; xeno.cx spreads its leap days differently, so the indices won't match theirs. Zone = digital root of the index, and the (head, appraisal) address = upper 4 / lower 2 digits [spec]. |
| **Tai Xuan** | 81 heads × 9 appraisals; two appraisals per day (one day, one night) = 364½ days; Head 1 中, appraisal 初一, starts at the winter solstice; 踦 Ji and 嬴 Ying make up the remaining ¾ day, ½ + ¼ (永樂大典 太玄敘錄, [shidianguji](https://www.shidianguji.com/book/YLDD00001/chapter/1lmfjnpcpo9pm); 東園叢說 論太玄踦贏二贊). Head names: Unicode Tai Xuan Jing Symbols block. | **Approximations:** the year starts on the local civil date of the astronomical solstice in `--tz`, whereas Han practice used mean reckoning and Chinese time. Ji = night of day 364; Ying = whatever civil day remains before the next solstice day, so it appears only in some years. **Conventions:** day/night split at 06:00/18:00 local; two zones, shown line-value first: **by lines** = digital root of the 0-based index *i* = head − 1 (the base-3 line value, lines bottom→top weighted 1, 3, 9, 27; 0 only for 中 Centre) and **by number** = digital root of the head; e.g. 67 Darkening → zone 3 by lines · zone 4 by number [spec]. See *Two zones* below. |
| **Gua qi** | Meng Xi's 六日七分 scheme: 60 hexagrams × 6 7/80 days from 中孚 at the winter solstice to 頤; the order (易緯稽覽圖; [iqing.net](http://www.iqing.net/zltt/822.html)); ranks 公辟侯大夫卿; 坎震離兌 one line per solar term (24 qi) ([chinakongzi 卦气](https://www.chinakongzi.org/baike/MINGCI/zhexue/201708/t20170825_142768.htm)) | **Approximations:** uses the true solstice instant, and solar terms by true longitude (定氣) rather than Han mean terms (平氣). Jing Fang's variant (cardinal hexagrams get 73/80 day) is not implemented. **Convention:** two zones, shown line-value first: **by lines** = digital root of the binary line value *v* (line *k* weighted 2^(k−1), line 1 at the bottom; 0 only for 坤 Kun) and **by number** = 1+(KW−1) mod 9; e.g. KW 36 明夷 (v = 5) → zone 5 by lines · zone 9 by number [conv]. |
| **Decan** | 36 × 10° signs; Chaldean rulers starting with Mars at Aries I; Golden Dawn *Book T* minor arcana 2–10 by element ([Book T](https://hermeticcloud.com/library/book-t/); [Wikipedia: Decan](https://en.wikipedia.org/wiki/Decan)) | **Approximations:** solar longitude uses Meeus, *Astronomical Algorithms* ch. 25 low-accuracy formula (tests: within 0.01° at 6 JPL equinox/solstice instants; Example 25.a matches to 0.0001°). ΔT uses the Espenak–Meeus polynomial for 2005–2050, otherwise 69 s. **Speculative hooks:** zone = digital root of the decan number; Book T rank −1 = Decadence rank; 36 = T(8) = Gt-36. |
| **'Pataphysical** | Era from 8 Sep 1873 vulg. = 1 Absolu 1. Twelve months of 28 days plus Gidouille of 29; 29 Gueules exists only in leap years; the 29ths are outside the week ("hunyadi", "hunyadi gras"); 1/8/15/22 are Sundays and every 13th a Friday. Month names and start dates as in the sources ([Wikipedia: Pataphysics](https://en.wikipedia.org/wiki/Pataphysics#Pataphysical_calendar); [fr.wikipedia: Calendrier pataphysique](https://fr.wikipedia.org/wiki/Calendrier_pataphysique)). | **Saint/feast list:** now in `--pata-saints` (see below). **Convention:** dates before the era give year ≤ 0. |

**Tested reference dates:**
- 'Pataphysical: 8 Sep 1873 = 1 Absolu 1; 1 Jan 2000 = 4 Décervelage 127; 10 Nov 2012 = Sunday 8 As 140.
- Solar: USNO/JPL equinox and solstice instants for 2024–2026.
- Book T: 2 of Wands = Mars in Aries; 4 of Swords = Jupiter in Libra; 10 of Cups = Mars in Pisces; Libra = Justice, Jupiter = Wheel, Saturn = Universe; court spans (Queen of Wands 20° Pisces–20° Aries, Prince of Cups 20° Libra–20° Scorpio).
- England & Wales: Calendar Notes 2024–2027 dates (see Regions).

## Daily reading
`python3 /workspace/numogram-fixes/calendar/calendar.py --daily` prints about ten lines for today (add `--date YYYY-MM-DD` for another day). For 17 Oct 2026:

```
∴ Saturday 17 October 2026 · BST · England & Wales
☉♎ Libra III 24° · ♃ Jupiter · 🜁 Air · 🂤 4 of Swords · zone 3
  🃫 XI Justice ♎ (trad. VIII) · 🃪 X Wheel of Fortune ♃ · 🂾 Prince of Cups 20°♎–20°♏
Nma A-290 101201 · zone 1 · 𝌦 Closeness /2
Tai Xuan 𝍈 67 Darkening · 次七 · zone 3 by lines · zone 4 by number
Gua qi ䷣ 明夷 Darkening of the Light (KW 36) · 寒露 · ☱ 兌 2 · zone 5 by lines · zone 9 by number
✠ St Ignatius of Antioch (memorial)
⛤ 'Pata: jeudi 12 Haha 154 E.P. · St Cosinus, savant
⁂ Prompt: Trace a thread from XI Justice (Libra) to the hexagram 'Darkening of the Light': does anything in the life or cult of St Ignatius of Antioch sit on that thread?
```

For 1 March 2026 (St David's Day falls on the 2nd Sunday of Lent, so in Wales the solemnity moves to Monday 2 March, and in England the feast gives way to the Sunday):

```
∴ Sunday 1 March 2026 · GMT · England & Wales
☉♓ Pisces II 11° · ♃ Jupiter · 🜄 Water · 🂹 9 of Cups · zone 8
  🃲 XVIII The Moon ♓ · 🃪 X Wheel of Fortune ♃ · 🂼 Knight of Cups 20°♒–20°♓
Nma A-60 002012 · zone 5 · 𝌌 Ascent /6
Tai Xuan 𝌕 16 Contact · 次六 · zone 6 by lines · zone 7 by number
Gua qi ䷊ 泰 Peace (KW 11) · 雨水 · ☵ 坎 5 · zone 7 by lines · zone 2 by number
✠ 2nd Sunday of Lent · St David (Dewi Sant) (solemnity; → Mon 2 Mar) [W]; St David (feast; impeded: Sunday) [E]
⛤ 'Pata: samedi 7 Pédale 153 E.P. · St Gavroche, forain
☘ Folk: Saint David's Day (Dydd Gŵyl Dewi Sant)
⁂ Prompt: Trace a thread from XVIII The Moon (Pisces) to the hexagram 'Peace': does anything in the life or cult of St David (Dewi Sant) sit on that thread?
```

**Two zones.** Tai Xuan and gua qi lines show both zones, line-value zone first: `zone 3 by lines · zone 4 by number` (`|` instead of `·` in `--ascii`), or `zone 5 (lines and number)` when they agree. The conventions match `cli/taixuan.py` `taixuan_zone(i, "value"|"number")` and `cli/iching.py` `fuxi_zone(v)` / digital root of the King Wen number. JSON has `zone_lines`, `zone_number` and `line_value`; the older `zone` key is kept and equals `zone_number`.

Line by line: header (∴); ☉ with sign, decan, degree, ruler, element and the Book T minor card; the sign's trump, the ruler's trump and the court card (with its 20°–20° span); Nma; Tai Xuan; gua qi with the cardinal trigram; ✠ the Catholic day (Sunday name if any, national entries tagged `[W]` Wales / `[E]` England, then GRC); ⛤ 'Pataphysical; ☘ folk (only on days that have one); ⁂ the research prompt.

### Glyphs and the `--plain` / `--ascii` fallbacks
Glyphs come from the user's palette (`local-files/glyphs.md`): planets ☉☽☿♀♂♃♄, signs ♈…♓, alchemical elements 🜂🜃🜁🜄, trigrams ☰…☷ (shown for the gua qi cardinal hexagram: ☵ 坎, ☳ 震, ☲ 離, ☱ 兌), hexagrams (U+4DC0 block), Tai Xuan tetragrams (U+1D306 block), tarot trumps 🃠–🃵 and playing cards (U+1F0A0 block), and ∴ ✠ ⛤ ☘ ⁂ as line markers.
- **Cards [conv]:** the Unicode trumps are the French tarot's trumps, so they are used by number only. Minor and court cards use the French suits usually equated with tarot suits (Swords ♠, Cups ♥, Pentacles ♦, Wands ♣), and a Book T Prince is drawn as the King card.
- **`--plain`** drops every pictographic glyph but keeps CJK. **`--ascii`** prints 7-bit text only: Chinese is replaced by English hexagram names (from the Unicode character names), English solar-term names and pinyin for the cardinal trigrams, and accents are stripped.
- **Not shown:** lunar nodes ☊☋ (see Future work).

### Research prompt
The `⁂ Prompt:` line is a question built from one of five fixed templates. The template is chosen by date ordinal mod 5, so the same date always gets the same prompt. The slots are filled only from the day's computed elements: decan ruler and its trump, sign trump, minor and court card, tetragram name and number, hexagram, solar term, zones, and the first saint listed (national, then GRC, then 'Pataphysical). It states no facts. JSON carries `research_prompt` with `"label": "generated prompt — a question to research, not a claim"`.

## Tarot: Book T majors and courts
- **Sign and planet trumps [src]:** from Book T's "Twenty-Two Keys … letter attribution" ([Book T, Equinox I:8](https://hermeticcloud.com/library/book-t/)). Aries IV Emperor, Taurus V Hierophant, Gemini VI Lovers, Cancer VII Chariot, Leo Strength/Fortitude, Virgo IX Hermit, Libra Justice, Scorpio XIII Death, Sagittarius XIV Temperance, Capricorn XV Devil, Aquarius XVII Star, Pisces XVIII Moon. Mercury I Magician, Moon II High Priestess, Venus III Empress, Jupiter X Wheel of Fortune (Book T: "Wheel of Fate"), Mars XVI Tower ("Blasted Tower"), Sun XIX Sun, Saturn XXI World ("Universe"). The elemental trumps 0, XII and XX are not used by any decan.
- **The VIII/XI swap is explicit (`--trumps`) [conv]:**
  - `gd` (default) is the Golden Dawn order from the Cipher Manuscripts, adopted by Rider–Waite–Smith: **VIII Strength = Leo, XI Justice = Libra**.
  - `trad` uses the Marseille numbers, which Book T as printed in the Equinox also keeps: **XI Fortitude = Leo, VIII Justice = Libra**.
  - The sign attributions are the same either way; only the numbers swap ([Wikipedia: Strength (tarot card)](https://en.wikipedia.org/wiki/Strength_(tarot_card))).
  - The daily line shows the other number in brackets.
- **Court card [src]:** Book T's "Spheres of influence of the court cards" gives each Knight, Queen and Prince 30° from 20° of one sign to 20° of the next. The tool shows the court whose span contains the Sun. For example, Queen of Wands 20° Pisces–20° Aries, Prince of Cups 20° Libra–20° Scorpio. Princesses rule polar quadrants, so none is shown. Book T's titles (Knight / Queen / Prince / Princess) are kept. Mapping them to Rider–Waite King/Knight/Page is disputed, so the tool does not attempt it.

## Regions: England & Wales National Calendars
`--region` takes `england-wales` (default), `wales`, `england` or `general`. `general` is the old behaviour: the General Roman Calendar as inscribed, with no transfers.
- **Data:** `data/national_england_wales.json` is a full transcription of the Liturgy Office summary tables: **Wales 24 celebrations, England 42** ([Wales](https://www.liturgyoffice.org.uk/Calendar/National/Wales1.shtml), [Wales II](https://www.liturgyoffice.org.uk/Calendar/National/Wales2.shtml), [England](https://www.liturgyoffice.org.uk/Calendar/National/England1.shtml), [England II](https://www.liturgyoffice.org.uk/Calendar/National/England2.shtml)).
- **Welsh proper:**
  - St Teilo 9 Feb; St David (Dewi Sant) 1 Mar, solemnity; St Beuno 20 Apr; St Asaph 5 May.
  - St Alban, St Julius & St Aaron 20 Jun; St John Jones 12 Jul; St Philip Evans & St John Lloyd 23 Jul; St Germanus of Auxerre 3 Aug; St David Lewis 26 Aug; St Deiniol 11 Sep.
  - St John Henry Newman 9 Oct; St Richard Gwyn 16 Oct; St John Paul II 22 Oct; Six Welsh Martyrs and their Companions 25 Oct, feast.
  - St Winefride 3 Nov; St Illtud 6 Nov; All Saints of Wales 8 Nov, feast; St Dyfrig 14 Nov; St John Roberts 10 Dec.
  - The patrons of Europe as feasts.
  - "Where no other indication is given the celebration is an optional memorial."
- **Rank conflicts between the two Wales pages:** the summary table gives St David as Solemnity, while the detail page says Feast. Asaph and the five martyrs' days are optional in the summary but Memorial in the detail. The summary rank is used, and the other is kept as `rank_variant`. The Calendar Notes 2026 move St David "(in Wales)" to Monday 2 March, which only happens to a solemnity.
- **England & Wales rules [src: [Liturgy Office calendar page](https://www.liturgyoffice.org.uk/Calendar/), [Calendar Notes 2024–2027](https://www.liturgyoffice.org.uk/Calendar/2026/Ordo-2026.pdf), [Table of Liturgical Days / UNLY 60](https://www.liturgyoffice.org.uk/Calendar/Info/Days.shtml)]:**
  - Holydays: Epiphany, Ss Peter & Paul, the Assumption and All Saints move to the Sunday when they fall on a Saturday or Monday.
  - Baptism of the Lord: on the Monday when Epiphany is kept on 7 or 8 Jan.
  - All Souls: on 3 Nov when All Saints moves to Sunday 2 Nov.
  - Body and Blood of Christ: on the Sunday.
  - Eternal High Priest (feast in E&W): the Thursday after Pentecost.
  - Ascension stays on Thursday.
  - National solemnities (St David in Wales, St George in England): on a Sunday of Advent, Lent or Easter they move to the Monday; in Holy Week or the Easter Octave they move to the Monday after the 2nd Sunday of Easter.
  - National feasts and memorials that fall on a Sunday are shown as impeded.
  - Sundays of Advent, Lent, Easter and Ordinary Time are named.
  - These are tested against the Calendar Notes dates: St David 2 Mar 2026, St George 28 Apr 2025, All Souls 3 Nov 2025, Baptism 8 Jan 2024, Peter & Paul 28 Jun 2026, Assumption 16 Aug 2026, Body and Blood 7 Jun 2026, and the Sunday numbers.
- **Supersession:** where a national calendar raises or moves a GRC celebration (e.g. Cyril & Methodius as patrons of Europe; Newman as a feast in England; St Denis and St John Leonardi moved to 10 Oct in England), the GRC copy is hidden and the national entry is shown.
- **Gaps:**
  - Diocesan propers are not included (Welsh dioceses, English dioceses, cathedral dedications).
  - Full precedence between GRC memorials and higher-ranked days is still not applied, e.g. GRC optional memorials still print beside a transferred solemnity.
  - The Wales summary table still names Newman "Bl"; the detail page and the Universal Calendar have "St".

## Saints' days: data, coverage and gaps
All data lives in `data/` as JSON, each file with its source URLs and retrieval date (2026-10-17). The England & Wales national data is described above. `data/build_data.py` is the one-off script that built the first two files from saved copies of the source pages; it is kept for audit, not needed at runtime. Nothing is invented: a day with no sourced entry shows "—".

- **'Pataphysical (`data/pata_saints.json`): 377 entries, complete apart from the imaginary 29ths that never occur** (13 months × 29 days, including the 29ths; only 29 Gidouille and 29 Gueules in leap years are ever reached).
  - Names from the list on [jchr.be](http://jchr.be/langage/pataphysique.htm) (read via the [Wayback Machine snapshot](https://web.archive.org/web/20241008002420/http://jchr.be/langage/pataphysique.htm) because the site timed out).
  - Ranks (Fête Suprême Première/Seconde, Suprême/Tierce/Quarte, Vacuation) from [icalendrier.fr](https://icalendrier.fr/calendriers-saga/calendriers/reforme-fixes/pataphysique). Its counts (3/8/22/40/267, 37 vacuations) differ slightly from fr.wikipedia's (2/8/22/41, 39 vacuations).
  - Spot-checked against [fr.wikipedia](https://fr.wikipedia.org/wiki/Calendrier_pataphysique) (examples in the tests).
  - **Gaps:** this is not the Collège de 'Pataphysique's own edition (calenpat.pdf could not be retrieved), and the calendar has had revisions. Five days differ between the two sources; the icalendrier wording is kept as `variant_icalendrier`. Two are different feasts (15 Palotin, 20 Clinamen), so their ranks are marked `rank_uncertain`.
- **General Roman Calendar (`data/general_roman_calendar.json`): 221 fixed celebrations, 8 inscribed movable feasts and 8 Proper-of-Time anchors** (Ash Wednesday, Palm Sunday, Holy Thursday, Good Friday, Easter, Ascension, Pentecost, Advent 1), from [Wikipedia: General Roman Calendar](https://en.wikipedia.org/wiki/General_Roman_Calendar) and [Moveable feast](https://en.wikipedia.org/wiki/Moveable_feast). Easter uses the anonymous Gregorian (Meeus/Jones/Butcher) algorithm.
  - **Gaps:** precedence is not applied to GRC entries, so a memorial impeded by a Sunday or solemnity is still listed. Weekday ferias are not named. Additions made after the Wikipedia snapshot are not included. England & Wales transfers and the national propers are handled by `--region` (above).
- **Folk (`data/folk_feasts.json`): 31 fixed, 3 movable and 1 seasonal-range entries, hand-curated.** Welsh days, each with the Wikipedia page that gives the date: Calennig 1 Jan; Hen Galan 13 Jan (Cwm Gwaun); Dydd Santes Dwynwen 25 Jan; Dydd Gŵyl Dewi 1 Mar; Nos Galan Haf 30 Apr; Calan Mai/Calan Haf 1 May; Owain Glyndŵr Day 16 Sep; Nos Galan Gaeaf 31 Oct; Calan Gaeaf 1 Nov; and the Mari Lwyd season, 25 Dec–6 Jan, from "Christmas until after Twelfth Day" (Evans 1804); modern revivals vary. Other entries: British/Irish/European days (Plough Monday, Shrove Tuesday, St David, St George, Walpurgis Night, Midsummer Eve, St Swithun, Lammas, Michaelmas, St Crispin, Bonfire Night, Martinmas, St Andrew, St Lucy, Wren Day …) and folk saints: Jesús Malverde (3 May), San La Muerte (15 Aug, alt. 13 Aug), Santa Muerte (15 Aug, 1 Nov, 2 Nov; no official feast), Maximón (28 Oct, and the Holy Week procession). Each entry has a `kind` label (folk-saint / folk-day / saint-day), a region and a Wikipedia URL stating the date.
  - **Gaps:** this is a small sample, not a survey. Folk-saint dates vary by community. Maximón's 28 Oct date rests only on a Wikipedia infobox, so treat it as weak.

## Moon, Chinese month, sovereign hexagram, lunar mansions
`python3 calendar.py --lunar --sovereign --mansion [--date YYYY-MM-DD --time HH:MM]` (`--lunation` is an alias for `--lunar`). These overlays are on by default and appear in `--daily` as one ☽ line.
- **`--lunar` (phase, age, lunation, Chinese month and day):**
  - Principal phases use Meeus, *Astronomical Algorithms*, ch. 49 (true phases with all periodic and planetary terms). Against timeanddate's published 2026 London times they agree to the minute; see the `Lunar` tests.
  - The phase name comes from the Sun–Moon elongation; the principal phase is named on its own day.
  - The lunation number is Brown's.
  - Chinese month and day follow the modern rule (GB/T 33661-2017). Months begin on the Beijing (UTC+8) date of the new moon, and month 11 contains 冬至. In a 13-month year, the first month with no 中氣 is the leap month 閏. Tests cover the 2023 閏二月, the 2025 閏六月 and the 2033 閏十一月.
  - [conv] The Chinese day is counted on the chosen civil date.
- **`--sovereign`:** Wen, *I Ching, the Oracle*, Table 3.1 (Jing Fang's 辟卦), using the real lunar month. Month 11 → 24, …, 8 → 20, 9 → 23, 10 → 2. It also gives the branch, animal and Wu Xing as Wen prints them; her 卯 Rabbit "Water" is flagged, since it is conventionally Wood. [conv] A leap month takes the hexagram of its number.
- **`--mansion`:** the Moon is geocentric, from Meeus ch. 47 truncated (≈0.05°). Traditions disagree, so every convention is labelled:
  - **Chinese 28 宿:** sidereal and unequal, measured in *right ascension* of date from each determinative star 距星. The determinatives follow Wikipedia's "Twenty-Eight Mansions" (citing the IDP "Chinese Sky" and Sun Xiaochun 1997), with J2000 positions from SIMBAD precessed by Meeus ch. 21; no proper motion.
  - **Arabic 28 manāzil:** Agrippa's names (*Three Books*, II.33), in equal 12°51′26″ divisions from tropical 0° Aries [conv].
  - **27 nakshatras:** equal 13°20′, sidereal, using a linear Lahiri ayanamsa (23°51′11″ at J2000 + 50.29″/yr) [approx].
- See `docs/wiki/lunation-and-mansions.md` and `docs/wiki/gua-qi-wen.md`.

## Design: overlays and providers
- **Overlays are registered with a decorator:** `@overlay(name, flag, help, needs=(...), enabled=...)`. Each one is `fn(ctx) -> dict`.
- **`Context`** carries local time, UTC time and the civil date, and offers lazy, cached `ctx.longitude(body)`.
- **Providers are a separate registry** (`PROVIDERS[body](t_utc) -> apparent ecliptic longitude`). `sun` (Meeus ch. 25) and `moon` (Meeus ch. 47, truncated) are implemented; `mercury` … `saturn` are stubs that raise `NotImplementedError`.
- **`needs`** declares which bodies an overlay reads, so one ephemeris provider can feed several overlays.

## Future work
- **Lunation:** tithi, and lunar nodes ☊☋.
- **Planetary clock** (the user's idea): a multi-armed dial with the zodiac/decan ring, one arm per planet, and numogram zones on the rim. It would be another overlay with `needs=("sun", "moon", "mercury", …, "saturn")`, fed by the same provider registry as lunation, and could output JSON for an SVG renderer. It needs planet providers first (for example Meeus ch. 31–33 or VSOP87 truncated series).
- **Smaller items:**
  - Jing Fang gua qi variant.
  - Tai Xuan mean-solstice (Han) mode.
  - Optional Chinese head names.
  - The Collège's official 'Pataphysical feast list, to replace the jchr.be/icalendrier list.
  - Full liturgical precedence for GRC entries, and the Welsh and English diocesan propers.
  - Lunar nodes ☊☋.


See also `docs/wiki/gua-qi-wen.md` (Wen's gua qi chapter, checked against this overlay).
