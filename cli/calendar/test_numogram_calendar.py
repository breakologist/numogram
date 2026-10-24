"""Unit tests for numogram_calendar. Run: python3 -m unittest -v test_numogram_calendar

Reference values and their sources:
- Solstice/equinox instants (UTC): JPL DE441 table at sofajpl.com/solstice and USNO
  aa.usno.navy.mil/calculated/seasons (2025).
- Meeus, Astronomical Algorithms, Example 25.a: 1992 Oct 13.0 TD, apparent λ☉ = 199.90895°
  (low-accuracy method).
- 'Pataphysical dates: en.wikipedia.org/wiki/Pataphysics (8 Sep 1873 = 1 Absolu 1;
  1 Jan 2000 = 4 Décervelage 127; 10 Nov 2012 = 8 As 140, Sunday; 27 Haha = 1 Nov;
  14 Sable = 14 Dec; 29 Gidouille = 13 July; 29 Gueules = 23 Feb in leap years).
- Book T: 2 of Wands = Mars in Aries; 10 of Cups = Mars in Pisces; 4 of Swords =
  Jupiter in Libra; 5 of Wands = Saturn in Leo.
- Gua qi: 中孚 opens the year at the winter solstice, 頤 closes it (chinakongzi 卦气).
- Tarot majors / courts: Book T (Equinox I:8) key attributions (Aries = Emperor, Libra =
  Justice, Jupiter = Wheel, Saturn = Universe ...) and court spans (Queen of Wands 20° Pisces
  – 20° Aries; Prince of Cups 20° Libra – 20° Scorpio; Prince of Wands 20° Cancer – 20° Leo).
  Strength/Justice numbering: en.wikipedia.org/wiki/Strength_(tarot_card).
- England & Wales: liturgyoffice.org.uk National Calendars for England and for Wales, and
  Calendar Notes 2024–2027 (St David 2 Mar 2026 in Wales; St George 28 Apr 2025; All Saints
  2 Nov / All Souls 3 Nov 2025; Epiphany 7 Jan / Baptism 8 Jan 2024; Peter & Paul 28 Jun 2026;
  Assumption 16 Aug 2026; Body and Blood 7 Jun 2026; Eternal High Priest 28 May 2026;
  Sunday names e.g. 2nd Sunday in OT 18 Jan 2026, 11th 14 Jun 2026).
"""
import datetime as dt
import os
import subprocess
import sys
import unicodedata
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numogram_calendar as nc  # noqa: E402

UTC = dt.timezone.utc


def utc(s):
    return dt.datetime.fromisoformat(s).replace(tzinfo=UTC)


class Solar(unittest.TestCase):
    EVENTS = [  # (target λ, UTC instant) from sofajpl.com (JPL DE441)
        (0, "2024-03-20 03:06:24"), (90, "2025-06-21 02:42:16"),
        (180, "2026-09-23 00:05:13"), (270, "2025-12-21 15:03:05"),
        (270, "2026-12-21 20:50:14"), (0, "2025-03-20 09:01:29"),
    ]

    def test_meeus_example_25a(self):
        t = utc("1992-10-13 00:00:00") - dt.timedelta(seconds=nc.delta_t_seconds(1992))
        self.assertAlmostEqual(nc.sun_longitude(t), 199.90895, delta=0.002)

    def test_longitude_at_events(self):
        for target, s in self.EVENTS:
            lon = nc.sun_longitude(utc(s))
            diff = ((lon - target + 180) % 360) - 180
            self.assertLess(abs(diff), 0.01, f"{s}: λ={lon}")

    def test_event_finder_within_15_min(self):
        for target, s in self.EVENTS:
            ref = utc(s)
            got = nc.find_solar_longitude(target, ref - dt.timedelta(days=3),
                                          ref + dt.timedelta(days=3))
            self.assertLess(abs((got - ref).total_seconds()), 15 * 60, s)


class Decans(unittest.TestCase):
    def test_boundaries_and_book_t(self):
        cases = [(0.0, 1, "Aries", "I", "Mars", "2 of Wands"),
                 (9.999, 1, "Aries", "I", "Mars", "2 of Wands"),
                 (10.0, 2, "Aries", "II", "Sun", "3 of Wands"),
                 (120.0, 13, "Leo", "I", "Saturn", "5 of Wands"),
                 (200.0, 21, "Libra", "III", "Jupiter", "4 of Swords"),
                 (359.99, 36, "Pisces", "III", "Mars", "10 of Cups")]
        for lon, n, sign, d, ruler, card in cases:
            r = nc.decan_of(lon)
            self.assertEqual((r["decan"], r["sign"], r["decan_in_sign"], r["ruler"], r["card"]),
                             (n, sign, d, ruler, card), lon)

    def test_mars_rules_six(self):
        rulers = [nc.decan_of(10 * k + 5)["ruler"] for k in range(36)]
        self.assertEqual(rulers.count("Mars"), 6)
        self.assertEqual(sorted(set(rulers.count(p) for p in nc.CHALDEAN if p != "Mars")), [5])

    def test_equinox_is_aries_one(self):
        ctx = nc.build_context("2025-03-20", "12:00", "UTC")
        self.assertEqual(nc.decan_overlay(ctx)["decan"], 1)


class Pataphysical(unittest.TestCase):
    def check(self, d, day, month, year, weekday=None):
        p = nc.pataphysical(dt.date.fromisoformat(d))
        self.assertEqual((p["day"], p["month"], p["year_ep"]), (day, month, year), d)
        if weekday:
            self.assertEqual(p["weekday"], weekday, d)

    def test_documented_examples(self):
        self.check("1873-09-08", 1, "Absolu", 1, "dimanche")
        self.check("2000-01-01", 4, "Décervelage", 127)
        self.check("2012-11-10", 8, "As", 140, "dimanche")

    def test_month_starts_and_feasts(self):
        self.check("2025-11-01", 27, "Haha", 153)
        self.check("2025-12-14", 14, "Sable", 153)
        for m, d in zip(nc.PATA_MONTHS, ["09-08", "10-06", "11-03", "12-01", "12-29", "01-26",
                                         "02-23", "03-23", "04-20", "05-18", "06-15", "07-14",
                                         "08-11"]):
            y = 2026 if d >= "09-08" or d[:2] in ("10", "11", "12") else 2027
            self.check(f"{y}-{d}", 1, m, 154)

    def test_hunyadi(self):
        self.check("2026-07-13", 29, "Gidouille", 153, "hunyadi")
        self.check("2024-02-23", 29, "Gueules", 151, "hunyadi gras")   # leap year
        self.check("2025-02-23", 1, "Pédale", 152)                     # not leap
        self.check("2024-02-24", 1, "Pédale", 151)

    def test_thirteenth_is_friday(self):
        days = [nc.pataphysical(dt.date(2026, 9, 8) + dt.timedelta(k)) for k in range(365)]
        thirteenths = [p for p in days if p["day"] == 13]
        self.assertEqual(len(thirteenths), 13)
        self.assertTrue(all(p["weekday"] == "vendredi" for p in thirteenths))
        self.assertTrue(all(p["weekday"] == "dimanche" for p in days if p["day"] in (1, 8, 15, 22)))

    def test_year_length(self):
        n = sum(1 for k in range(366) if nc.pataphysical(dt.date(2026, 9, 8) + dt.timedelta(k))["day"])
        self.assertEqual(n, 366)
        self.assertEqual(nc.pataphysical(dt.date(2027, 9, 8))["text"], "dimanche 1 Absolu 155 E.P.")


class Saints(unittest.TestCase):
    def pata_name(self, d):
        return nc.pata_saints_overlay(nc.build_context(d))["name"]

    def test_pata_list_complete_and_wikipedia_examples(self):
        data = nc.load_data("pata_saints.json")
        self.assertEqual(len(data["entries"]), 377)
        # Examples quoted in en/fr Wikipedia (Calendrier pataphysique / Pataphysics)
        for d, frag in [("2026-04-06", "INVENTION"), ("2026-09-08", "NATIVITÉ d'ALFRED JARRY"),
                        ("2026-10-27", "RÉSURRECTION DE BOSSE-DE-NAGE"), ("2026-09-22", "ÉTHERNITÉ"),
                        ("2026-11-23", "St Possible, schizophrène"), ("2026-10-30", "Brisset"),
                        ("2026-12-04", "Ste Barbe"), ("2026-08-29", "St Prélote"),
                        ("2026-02-28", "Vers Belges"), ("2026-11-01", "OCCULTATION D'ALFRED JARRY"),
                        ("2026-12-14", "Don Quichotte")]:
            self.assertIn(frag, self.pata_name(d), d)
        self.assertIn("NOM D'UBU", self.pata_name("2026-07-13"))         # 29 Gidouille

    def test_pata_today(self):
        self.assertEqual(self.pata_name("2026-10-17"), "St Cosinus, savant")

    def test_easter(self):   # known Gregorian Easter dates
        for y, d in [(2000, "2000-04-23"), (2019, "2019-04-21"), (2024, "2024-03-31"),
                     (2025, "2025-04-20"), (2026, "2026-04-05"), (2038, "2038-04-25"),
                     (2285, "2285-03-22")]:
            self.assertEqual(nc.easter(y).isoformat(), d)

    def grc(self, d, region="general"):
        ctx = nc.build_context(d, options={"region": region})
        return [c["name"] for c in nc.saints_overlay(ctx)["celebrations"]]

    def test_grc_fixed(self):
        data = nc.load_data("general_roman_calendar.json")
        self.assertGreaterEqual(len(data["fixed"]), 200)
        self.assertTrue(any("Ignatius of Antioch" in n for n in self.grc("2026-10-17")))
        self.assertTrue(any("Luke" in n for n in self.grc("2026-10-18")))
        self.assertTrue(any("Mother of God" in n for n in self.grc("2026-01-01")))

    def test_grc_movable(self):
        self.assertTrue(any("Easter Sunday" in n for n in self.grc("2026-04-05")))
        self.assertTrue(any("Ash Wednesday" in n for n in self.grc("2026-02-18")))
        self.assertTrue(any("Pentecost Sunday" in n for n in self.grc("2026-05-24")))
        self.assertTrue(any("Body and Blood" in n for n in self.grc("2026-06-04")))
        self.assertTrue(any("King of the Universe" in n for n in self.grc("2026-11-22")))
        self.assertTrue(any("First Sunday of Advent" in n for n in self.grc("2026-11-29")))
        self.assertTrue(any("Holy Family" in n for n in self.grc("2026-12-27")))
        self.assertTrue(any("Holy Family" in n for n in self.grc("2022-12-30")))   # Christmas on Sunday
        self.assertTrue(any("Baptism" in n for n in self.grc("2026-01-11")))

    def test_folk(self):
        def folk(d):
            return [c["name"] for c in nc.folk_overlay(nc.build_context(d))["observances"]]
        self.assertIn("Shrove Tuesday (Pancake Day)", folk("2026-02-17"))
        self.assertIn("Plough Monday", folk("2026-01-12"))
        self.assertTrue(any("Malverde" in n for n in folk("2026-05-03")))
        self.assertTrue(any("San La Muerte" == n for n in folk("2026-08-15")))
        self.assertTrue(any("Maximón" in n for n in folk("2026-10-28")))
        self.assertEqual(folk("2026-10-17"), [])
        self.assertTrue(any("Dwynwen" in n for n in folk("2026-01-25")))
        self.assertTrue(any("Hen Galan" in n for n in folk("2026-01-13")))
        self.assertTrue(any("Nos Galan Gaeaf" in n for n in folk("2026-10-31")))
        self.assertTrue(any("Calan Gaeaf (first" in n for n in folk("2026-11-01")))
        self.assertTrue(any("Calan Mai" in n for n in folk("2026-05-01")))
        self.assertTrue(any("Glyndŵr" in n for n in folk("2026-09-16")))
        for d in ("2026-12-25", "2026-12-31", "2027-01-06"):
            self.assertIn("Mari Lwyd season", folk(d), d)
        self.assertNotIn("Mari Lwyd season", folk("2027-01-07"))
        for e in nc.load_data("folk_feasts.json")["fixed"]:
            self.assertTrue(e["source"].startswith("https://en.wikipedia.org/wiki/"), e)

    def test_daily(self):
        r = nc.run(nc.build_context("2026-10-17"), [n for n, o in nc.OVERLAYS.items() if o["enabled"]])
        txt = nc.format_daily(r)
        self.assertIn("Saturday 17 October 2026", txt)
        self.assertIn("Ignatius of Antioch", txt)
        self.assertIn("St Cosinus", txt)
        self.assertIn("🃫 XI Justice ♎", txt)
        self.assertIn("🃪 X Wheel of Fortune ♃", txt)
        self.assertIn("Prince of Cups", txt)
        self.assertIn("Prompt:", txt)
        self.assertLessEqual(len(txt.splitlines()), 11)

    def test_daily_plain_and_ascii(self):
        r = nc.run(nc.build_context("2026-03-01"), [n for n, o in nc.OVERLAYS.items() if o["enabled"]])
        plain = nc.format_daily(r, "plain")
        for g in "☉♃♓🜄🃲🂹𝌕䷊✠⛤⁂∴":
            self.assertNotIn(g, plain)
        self.assertIn("泰", plain)                     # CJK kept in plain mode
        asc = nc.format_daily(r, "ascii")
        self.assertTrue(all(ord(ch) < 128 for ch in asc), asc)
        self.assertIn("Peace (KW 11)", asc)
        self.assertIn("Rain Water", asc)
        self.assertIn("St David", asc)

    def test_research_prompt_deterministic(self):
        names = [n for n, o in nc.OVERLAYS.items() if o["enabled"]]
        a = nc.run(nc.build_context("2026-10-17"), names)["research_prompt"]
        b = nc.run(nc.build_context("2026-10-17"), names)["research_prompt"]
        self.assertEqual(a, b)
        self.assertIn("not a claim", a["label"])
        self.assertIn("Darkening of the Light", a["text"])
        ts = {nc.run(nc.build_context(f"2026-10-{d:02d}"), names)["research_prompt"]["template"]
              for d in range(1, 11)}
        self.assertEqual(ts, set(range(len(nc.PROMPT_TEMPLATES))))


class EnglandWales(unittest.TestCase):
    def sa(self, d, region="england-wales"):
        return nc.saints_overlay(nc.build_context(d, options={"region": region}))

    def nat(self, d, region="england-wales"):
        return {(n["region"], n["name"]): n for n in self.sa(d, region)["national"]}

    def test_data_complete_and_sourced(self):
        data = nc.load_data(nc.NATIONAL_FILE)
        self.assertEqual((len(data["wales"]), len(data["england"])), (24, 42))
        self.assertTrue(all(s["url"].startswith("https://www.liturgyoffice.org.uk/")
                            for s in data["sources"]))
        names = " ".join(x["name"] for x in data["wales"])
        for frag in ("Teilo", "Dyfrig", "Illtud", "Winefride", "Beuno", "Asaph", "Deiniol",
                     "Richard Gwyn", "John Roberts", "Six Welsh Martyrs", "All Saints of Wales"):
            self.assertIn(frag, names)

    def test_welsh_proper_dates(self):
        for d, frag, rank in [("2026-02-09", "Teilo", "optional memorial"),
                              ("2026-11-06", "Illtud", "optional memorial"),
                              ("2026-11-14", "Dyfrig", "optional memorial"),
                              ("2026-11-03", "Winefride", "optional memorial"),
                              ("2026-10-26", None, None)]:
            hits = [n for n in self.sa(d, "wales")["national"] if frag and frag in n["name"]]
            if frag:
                self.assertEqual(hits[0]["rank"], rank, d)
        self.assertTrue(any("Six Welsh Martyrs" in n["name"] for n in self.sa("2026-10-25", "wales")["national"]))

    def test_st_david_2026_transferred_in_wales(self):
        s = self.sa("2026-03-01")
        self.assertEqual(s["day_name"], "2nd Sunday of Lent")
        w = [n for n in s["national"] if n["region"] == "wales"][0]
        self.assertEqual(w["transferred_to"], "2026-03-02")
        e = [n for n in s["national"] if n["region"] == "england"][0]
        self.assertEqual((e["rank"], e["impeded"]), ("feast", "Sunday"))
        m = self.sa("2026-03-02", "wales")["national"][0]
        self.assertEqual((m["rank"], m["transferred_from"]), ("solemnity", "2026-03-01"))
        self.assertEqual(self.sa("2025-03-01", "wales")["national"][0]["rank"], "solemnity")

    def test_st_george_2025_easter_octave(self):
        self.assertEqual(self.sa("2025-04-23", "england")["national"][0]["transferred_to"], "2025-04-28")
        self.assertIn("George", self.sa("2025-04-28", "england")["national"][0]["name"])
        g26 = self.sa("2026-04-23", "england")["national"][0]
        self.assertEqual(g26["rank"], "solemnity")
        self.assertNotIn("transferred_to", g26)

    def test_holyday_and_movable_transfers(self):
        def grc(d):
            return [c["name"] for c in self.sa(d)["celebrations"]]
        self.assertTrue(any("Body and Blood" in n for n in grc("2026-06-07")))
        self.assertFalse(any("Body and Blood" in n for n in grc("2026-06-04")))
        self.assertTrue(any("Peter and Paul" in n for n in grc("2026-06-28")))
        self.assertFalse(any("Peter and Paul" in n for n in grc("2026-06-29")))
        self.assertTrue(any("Assumption" in n for n in grc("2026-08-16")))
        self.assertTrue(any("All Saints" in n for n in grc("2025-11-02")))
        self.assertTrue(any("Faithful Departed" in n for n in grc("2025-11-03")))
        self.assertTrue(any("Faithful Departed" in n for n in grc("2026-11-02")))
        self.assertTrue(any("All Saints" in n for n in grc("2027-10-31")))
        self.assertTrue(any("Epiphany" in n for n in grc("2024-01-07")))
        self.assertTrue(any("Baptism" in n for n in grc("2024-01-08")))
        self.assertTrue(any("Epiphany" in n for n in grc("2026-01-06")))
        self.assertTrue(any("Baptism" in n for n in grc("2025-01-12")))
        self.assertTrue(any("Eternal High Priest" in n["name"] for n in self.sa("2026-05-28")["national"]))
        self.assertTrue(any("Ascension" in n for n in grc("2026-05-14")))
        # General Roman Calendar unchanged
        self.assertTrue(any("Body and Blood" in n for n in
                            [c["name"] for c in self.sa("2026-06-04", "general")["celebrations"]]))

    def test_supersede_and_newman(self):
        names = [c["name"] for c in self.sa("2026-10-09", "england")["celebrations"]]
        self.assertFalse(any("Newman" in n or "Denis" in n for n in names))
        n = self.sa("2026-10-09", "england")["national"][0]
        self.assertEqual(n["rank"], "feast")
        self.assertEqual(self.sa("2026-10-09", "wales")["national"][0]["rank"], "optional memorial")
        self.assertFalse(any("Cyril" in c["name"] for c in self.sa("2026-02-14")["celebrations"]))
        self.assertTrue(any("Cyril" in c["name"] for c in self.sa("2026-02-14", "general")["celebrations"]))

    def test_sunday_names(self):
        for d, name in [("2026-01-18", "2nd Sunday in Ordinary Time"),
                        ("2026-02-15", "6th Sunday in Ordinary Time"),
                        ("2026-02-22", "1st Sunday of Lent"),
                        ("2026-05-17", "7th Sunday of Easter"),
                        ("2026-06-14", "11th Sunday in Ordinary Time"),
                        ("2026-12-20", "4th Sunday of Advent")]:
            self.assertEqual(nc.sunday_name(dt.date.fromisoformat(d)), name, d)
        self.assertIsNone(nc.sunday_name(dt.date(2026, 10, 17)))


class Tarot(unittest.TestCase):
    def test_sign_and_planet_trumps(self):
        exp = {"Aries": 4, "Taurus": 5, "Gemini": 6, "Cancer": 7, "Leo": 8, "Virgo": 9,
               "Libra": 11, "Scorpio": 13, "Sagittarius": 14, "Capricorn": 15,
               "Aquarius": 17, "Pisces": 18}
        for i, sign in enumerate(nc.SIGNS):
            self.assertEqual(nc.decan_of(30 * i + 5)["sign_trump"]["number"], exp[sign], sign)
        pl = {"Mercury": 1, "Moon": 2, "Venus": 3, "Jupiter": 10, "Mars": 16, "Sun": 19, "Saturn": 21}
        for k in range(36):
            d = nc.decan_of(10 * k + 5)
            self.assertEqual(d["ruler_trump"]["number"], pl[d["ruler"]])
        used = set(exp.values()) | set(pl.values())
        self.assertEqual(used | {0, 12, 20}, set(range(22)))     # 3 elemental trumps remain

    def test_strength_justice_conventions(self):
        gd, tr = nc.decan_of(195, "gd"), nc.decan_of(195, "trad")        # Libra
        self.assertEqual((gd["sign_trump"]["roman"], gd["sign_trump"]["title"]), ("XI", "Justice"))
        self.assertEqual(tr["sign_trump"]["roman"], "VIII")
        self.assertEqual(gd["sign_trump"]["glyph"], "\U0001F0EB")
        self.assertEqual(nc.decan_of(125, "gd")["sign_trump"]["roman"], "VIII")      # Leo
        self.assertEqual(nc.decan_of(125, "trad")["sign_trump"]["book_t_title"], "Fortitude")
        self.assertEqual(nc.decan_of(205)["ruler_trump"]["title"], "Wheel of Fortune")

    def test_court_spans_book_t(self):
        for lon, card in [(0, "Queen of Wands"), (19.9, "Queen of Wands"), (20.1, "Prince of Pentacles"),
                          (125, "Prince of Wands"), (204.1, "Prince of Cups"), (345, "Knight of Cups"),
                          (235, "Knight of Wands"), (175, "Queen of Swords"), (265, "Queen of Pentacles")]:
            self.assertEqual(nc.decan_of(lon)["court"]["card"], card, lon)

    def test_card_glyphs(self):
        d = nc.decan_of(204.1)
        self.assertEqual(unicodedata.name(d["card_glyph"]), "PLAYING CARD FOUR OF SPADES")
        self.assertEqual(unicodedata.name(d["court"]["glyph"]), "PLAYING CARD KING OF HEARTS")
        self.assertEqual(unicodedata.name(d["ruler_trump"]["glyph"]), "PLAYING CARD TRUMP-10")


class Nma(unittest.TestCase):
    def test_supercycle(self):
        self.assertEqual(2 * 729 + 3, 1461)
        self.assertEqual(1461, 4 * 365.25)
        self.assertEqual(nc.nma_day(0)["index"], 0)
        self.assertEqual(nc.nma_day(728)["index"], 728)
        self.assertEqual((nc.nma_day(729)["cycle"], nc.nma_day(729)["index"]), ("B", 0))
        self.assertEqual(nc.nma_day(1458)["intercalary"], 1)
        self.assertEqual(nc.nma_day(1460)["intercalary"], 3)
        self.assertEqual(nc.nma_day(1461)["index"], 0)
        self.assertEqual(nc.nma_day(-1)["intercalary"], 3)

    def test_overlay_fields(self):
        ctx = nc.build_context("1970-01-01", options={"nma_epoch": "unix"})
        r = nc.nma_overlay(ctx)
        self.assertEqual((r["trits"], r["zone"], r["taixuan_address"]["head"],
                          r["taixuan_address"]["appraisal"]), ("000000", 0, 1, 1))
        ctx = nc.build_context("1971-12-30", options={"nma_epoch": "unix"})   # day 728
        r = nc.nma_overlay(ctx)
        self.assertEqual((r["trits"], r["taixuan_address"]["head"], r["taixuan_address"]["appraisal"]),
                         ("222222", 81, 9))
        ctx = nc.build_context("2000-01-01", options={"nma_epoch": "2000-01-01"})
        self.assertEqual(nc.nma_overlay(ctx)["index"], 0)

    def test_zone_depends_on_low_two_trits(self):
        for i in range(1, 729):
            self.assertEqual(nc.digital_root(i) % 9, (i % 9) % 9)


class TaiXuan(unittest.TestCase):
    def test_positions(self):
        self.assertEqual(nc.taixuan_position(0), {"head": 1, "appraisal": 1})
        self.assertEqual(nc.taixuan_position(728), {"head": 81, "appraisal": 9})
        self.assertEqual(nc.taixuan_position(729), {"extra": "踦 Ji"})
        self.assertEqual(nc.taixuan_position(730), {"extra": "嬴 Ying"})
        self.assertEqual(729 / 2, 364.5)

    def test_solstice_day_is_centre(self):
        ctx = nc.build_context("2025-12-21", "12:00", "Europe/London")
        r = nc.taixuan_overlay(ctx)
        self.assertEqual((r["head"], r["appraisal"], r["name"], r["lines"]), (1, 1, "Centre", "1111"))
        ctx = nc.build_context("2025-12-21", "22:00", "Europe/London")
        self.assertEqual(nc.taixuan_overlay(ctx)["appraisal"], 2)
        ctx = nc.build_context("2025-12-22", "03:00", "Europe/London")   # still night of 21st
        self.assertEqual(nc.taixuan_overlay(ctx)["appraisal"], 2)

    def test_ji_on_night_of_day_364(self):
        ctx = nc.build_context("2026-12-20", "22:00", "Europe/London")   # 364 days after 2025-12-21
        r = nc.taixuan_overlay(ctx)
        self.assertEqual((r["day_since_solstice"], r["extra"]), (364, "踦 Ji"))
        ctx = nc.build_context("2026-12-20", "12:00", "Europe/London")
        self.assertEqual((nc.taixuan_overlay(ctx)["head"], nc.taixuan_overlay(ctx)["appraisal"]), (81, 9))

    def test_tetragram_lines(self):
        self.assertEqual(nc.tetragram_lines(2), "1112")       # Full Circle
        self.assertEqual(nc.tetragram_lines(81), "3333")
        self.assertEqual(nc.tetragram_name(81), "Fostering")

    def test_both_zones_tetragram_67(self):
        z = nc.tetragram_zones(67)                   # i = 66 = lines 0,1,1,2 bottom→top
        self.assertEqual((z["line_value"], z["zone_lines"], z["zone_number"]), (66, 3, 4))
        self.assertEqual(nc.fmt_zones(z), "zone 3 by lines · zone 4 by number")
        self.assertEqual(nc.tetragram_zones(1)["zone_lines"], 0)       # Centre: only 0 by lines
        self.assertEqual(nc.tetragram_zones(10)["zone_lines"], 9)      # i = 9 → 9, not 0
        r = nc.taixuan_overlay(nc.build_context("2026-10-17"))
        self.assertEqual((r["head"], r["zone_lines"], r["zone_number"], r["zone"]), (67, 3, 4, 4))


class GuaQi(unittest.TestCase):
    def test_sequence(self):
        kws = [k for _, k in nc.GUAQI]
        self.assertEqual(len(set(kws)), 60)
        self.assertFalse({29, 30, 51, 58} & set(kws))           # 坎 離 震 兌 excluded
        self.assertEqual((nc.GUAQI[0][0], nc.GUAQI[-1][0]), ("中孚", "頤"))
        self.assertAlmostEqual(nc.GUAQI_DAYS, 6 + 7 / 80)

    def test_year_start(self):
        ctx = nc.build_context("2025-12-21", "16:00", "UTC")       # just after 15:03 UTC
        r = nc.guaqi_overlay(ctx)
        self.assertEqual((r["hexagram"], r["king_wen"], r["rank"][0]), ("中孚", 61, "公"))
        self.assertEqual((r["solar_term"], r["cardinal"], r["cardinal_line"]), ("冬至", "坎", 1))
        ctx = nc.build_context("2025-12-28", "12:00", "UTC")       # 6.9 days later
        self.assertEqual(nc.guaqi_overlay(ctx)["hexagram"], "復")
        ctx = nc.build_context("2025-12-21", "12:00", "UTC")       # before the instant
        self.assertEqual(nc.guaqi_overlay(ctx)["hexagram"], "頤")

    def test_both_zones_hexagram_36(self):
        self.assertEqual(sorted(nc.KW_BY_VALUE), list(range(1, 65)))
        z = nc.hexagram_zones(36)                    # 明夷: lines 1 and 3 yang → v = 5
        self.assertEqual((z["line_value"], z["zone_lines"], z["zone_number"]), (5, 5, 9))
        self.assertEqual(nc.fmt_zones(z), "zone 5 by lines · zone 9 by number")
        self.assertEqual(nc.hexagram_zones(2)["zone_lines"], 0)        # Kun
        self.assertEqual(nc.fmt_zones({"zone_lines": 5, "zone_number": 5}), "zone 5 (lines and number)")
        r = nc.guaqi_overlay(nc.build_context("2026-10-17"))
        self.assertEqual((r["king_wen"], r["zone_lines"], r["zone_number"], r["zone"]), (36, 5, 9, 9))

    def test_daily_shows_both_zones(self):
        r = nc.run(nc.build_context("2026-10-17"), [n for n, o in nc.OVERLAYS.items() if o["enabled"]])
        txt = nc.format_daily(r)
        self.assertIn("Tai Xuan 𝍈 67 Darkening · 次七 · zone 3 by lines · zone 4 by number", txt)
        self.assertIn("zone 5 by lines · zone 9 by number", txt)
        asc = nc.format_daily(r, "ascii")
        self.assertIn("zone 3 by lines | zone 4 by number", asc)
        self.assertIn("zone 5 by lines | zone 9 by number", asc)
        p = nc.run(nc.build_context("2026-10-18"), [n for n, o in nc.OVERLAYS.items() if o["enabled"]])
        self.assertIn("tetragram zone 3 by lines, zone 4 by number", p["research_prompt"]["text"])


class SaintNames(unittest.TestCase):
    def test_short_saint_keeps_co_saints(self):
        # regression: names were cut at the first comma, dropping Isaac Jogues and companions
        self.assertEqual(nc.short_saint("Saints John de Brébeuf, Isaac Jogues, Priests, and Companions, Martyrs"),
                         "Ss John de Brébeuf, Isaac Jogues and Companions")
        self.assertEqual(nc.short_saint("Saints Cornelius, Pope, and Cyprian, Bishop, Martyrs"),
                         "Ss Cornelius and Cyprian")
        self.assertEqual(nc.short_saint("Saint Luke, Evangelist"), "St Luke")
        self.assertEqual(nc.short_saint("Saint Paul of the Cross, Priest"), "St Paul of the Cross")
        self.assertEqual(nc.short_saint("St Cyril, monk, and St Methodius, bishop, patrons of Europe"),
                         "St Cyril and St Methodius")

    def test_daily_shows_full_memorial(self):
        r = nc.run(nc.build_context("2026-10-19"), [n for n, o in nc.OVERLAYS.items() if o["enabled"]])
        txt = nc.format_daily(r)
        self.assertIn("Ss John de Brébeuf, Isaac Jogues and Companions (opt. mem.)", txt)
        self.assertIn("St Paul of the Cross (opt. mem.)", txt)


class Registry(unittest.TestCase):
    def test_moon_provider_registered(self):
        self.assertIn("moon", nc.OVERLAYS["lunar"]["needs"])
        self.assertTrue(0 <= nc.PROVIDERS["moon"](utc("2026-01-01 00:00:00")) < 360)


class Lunar(unittest.TestCase):
    """Phase times: timeanddate.com/moon/phases/uk/london?year=2026 (fetched 24 Oct 2026,
    London local time, minute precision). Moon position: Meeus Example 47.a. Chinese
    months: 2025 閏六月 from 25 Jul 2025; 2023 閏二月 from 22 Mar 2023; Spring Festival
    17 Feb 2026 and 6 Feb 2027; 2033 閏十一月 from 22 Dec 2033 (the '2033 problem')."""
    LON = nc.ZoneInfo("Europe/London")

    def test_phase_times_2026(self):
        ref = [(0, "2026-01-18 19:52"), (2, "2026-03-03 11:37"), (1, "2026-06-21 22:55"),
               (3, "2026-08-06 03:21"), (0, "2026-10-10 16:50"), (2, "2026-10-26 04:11"),
               (3, "2026-11-01 20:28"), (0, "2026-12-09 00:51"), (2, "2026-12-24 01:28")]
        got = nc.lunar_phases_between(utc("2026-01-01 00:00:00"), utc("2027-01-01 00:00:00"))
        for q, s in ref:
            want = dt.datetime.fromisoformat(s).replace(tzinfo=self.LON)
            best = min((abs((t - want).total_seconds()), qq) for t, qq, _ in got if qq == q)
            self.assertLess(best[0], 120, s)

    def test_meeus_47a(self):
        t = utc("1992-04-12 00:00:00") - dt.timedelta(seconds=nc.delta_t_seconds(1992))
        lam, beta = nc.moon_position(t)
        self.assertAlmostEqual(lam, 133.162655, delta=0.02)
        self.assertAlmostEqual(beta, -3.229126, delta=0.02)

    def test_chinese_months(self):
        cd = nc.chinese_date
        self.assertEqual(cd(dt.date(2026, 2, 17))["month"], 1)
        self.assertEqual(cd(dt.date(2026, 2, 17))["day"], 1)
        self.assertEqual(cd(dt.date(2027, 2, 6))["day"], 1)
        self.assertEqual((cd(dt.date(2025, 7, 25))["month"], cd(dt.date(2025, 7, 25))["leap"]), (6, True))
        self.assertEqual((cd(dt.date(2023, 3, 22))["month"], cd(dt.date(2023, 3, 22))["leap"]), (2, True))
        self.assertEqual((cd(dt.date(2033, 12, 22))["month"], cd(dt.date(2033, 12, 22))["leap"]), (11, True))
        x = cd(dt.date(2026, 10, 24))
        self.assertEqual((x["month"], x["day"], x["leap"]), (9, 15, False))

    def test_sovereign_wen_table_3_1(self):
        def sov(d):
            return nc.sovereign_overlay(nc.build_context(d))
        self.assertEqual(sov("2026-10-24")["king_wen"], 23)          # month 9
        self.assertEqual(sov("2026-09-20")["king_wen"], 20)          # month 8
        self.assertEqual(sov("2026-11-20")["king_wen"], 2)           # month 10
        self.assertEqual(sov("2026-12-25")["king_wen"], 24)          # month 11, solstice month
        self.assertEqual([nc.SOVEREIGN[m][0] for m in (11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)],
                         [24, 19, 11, 34, 43, 1, 44, 33, 12, 20, 23, 2])

    def test_mansions(self):
        m = nc.mansion_overlay(nc.build_context("2026-10-24", "18:30"))
        self.assertEqual(m["xiu"]["name"], "壁")
        self.assertEqual(m["manzil"]["name"], "Albotham")            # sidereal (eighth sphere)
        self.assertEqual(m["manzil"]["tropical_name"], "Alnath")
        self.assertEqual(m["nakshatra"]["name"], "Revati")
        T = 0.2682
        widths = [nc.xiu_of_ra(nc.precess_j2000(x[4], x[5], T)[0] + 0.001, T)[2] for x in nc.XIU]
        self.assertAlmostEqual(sum(widths), 360.0, places=6)
        self.assertTrue(all(w > 0 for w in widths))

    def test_agrippa_decans(self):
        d = nc.decan_overlay(nc.build_context("2026-10-24"))
        self.assertEqual(d["decan"], 22)                                # Scorpio I
        self.assertIn("two men striking her", d["agrippa"]["image"])
        self.assertEqual(len(nc.load_data("agrippa_decans.json")["decans"]), 36)
        self.assertIn("man's head", d["picatrix"]["summary"])

    def test_lunar_overlay_today(self):
        r = nc.lunar_overlay(nc.build_context("2026-10-24", "18:30"))
        self.assertEqual(r["lunation"], 1284)
        self.assertEqual(r["phase"], "Waxing gibbous")
        self.assertEqual(r["next_phase"][0], "Full Moon")

    def test_no_stdlib_calendar_dependency(self):
        with open(nc.__file__, encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("\nimport calendar", src)
        for y in (1900, 2000, 2024, 2025, 2100):
            self.assertEqual(nc.is_gregorian_leap(y), y in (2000, 2024))

    def test_wrapper_cli(self):
        here = os.path.dirname(os.path.abspath(__file__))
        for extra in ([], ["--json", "--date", "2012-11-10"], ["--lunation"], ["--lunar", "--sovereign", "--mansion"], ["--list"],
                      ["--daily", "--date", "2026-10-17"], ["--saints", "--pata-saints", "--folk"],
                      ["--daily", "--ascii", "--date", "2026-03-01"], ["--daily", "--plain"],
                      ["--saints", "--region", "general"], ["--saints", "--region", "wales"],
                      ["--decan", "--trumps", "trad"]):
            r = subprocess.run([sys.executable, os.path.join(here, "calendar.py")] + extra,
                               capture_output=True, text=True, cwd=here)
            self.assertEqual(r.returncode, 0, r.stderr)
        r = subprocess.run([sys.executable, os.path.join(here, "calendar.py"), "--region", "mars"],
                           capture_output=True, text=True, cwd=here)
        self.assertNotEqual(r.returncode, 0)
        r = subprocess.run([sys.executable, "-c", "import calendar; print(calendar.__file__)"],
                           capture_output=True, text=True, cwd="/")
        self.assertNotIn("numogram-fixes", r.stdout)


if __name__ == "__main__":
    unittest.main()
