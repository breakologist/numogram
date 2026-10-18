#!/usr/bin/env python3
"""Rebuild the saints/feasts JSON from downloaded source pages (run once; not needed
at runtime). Inputs are the raw pages saved under /tmp by curl:

  /tmp/jchr_wb.htm   http://jchr.be/langage/pataphysique.htm  (via web.archive.org
                     snapshot 20241008002420; the live site timed out from this box)
  /tmp/ical.htm      https://icalendrier.fr/calendriers-saga/calendriers/reforme-fixes/pataphysique
  /tmp/grc.txt       https://en.wikipedia.org/w/index.php?title=General_Roman_Calendar&action=raw

Usage: python3 build_data.py   (writes pata_saints.json, general_roman_calendar.json)
folk_feasts.json is hand-curated (each entry carries its own source URL).
"""
import difflib, html, json, os, re, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
RETRIEVED = "2026-10-17"
RANKS = {"SPp": "Fête Suprême Première première", "SPs": "Fête Suprême Première seconde",
         "SS": "Fête Suprême Seconde", "ST": "Fête Suprême Tierce",
         "SQ": "Fête Suprême Quarte", "V": "Vacuation"}
MONTHS = ["absolu", "haha", "as", "sable", "décervelage", "gueules", "pédale", "clinamen",
          "palotin", "merdre", "gidouille", "tatane", "phalle"]


def norm(x):
    x = unicodedata.normalize("NFKD", x.lower())
    x = "".join(c for c in x if not unicodedata.combining(c))
    for a, b in (("°", ""), ("saintes", "sts"), ("sainte", "ste"), ("saints", "sts"),
                 ("saint", "st"), ("hunyadi - ", "")):
        x = x.replace(a, b)
    return re.sub(r"[^a-z0-9]", "", x)


def pata():
    s = open("/tmp/jchr_wb.htm", encoding="utf-8").read()
    jchr = {}
    for ln in s.splitlines():
        m = re.match(r"\s*<tr><th>(\d{1,2})\s*(?:er)?\s+([^<]+?)\s*<td>(.*?)<t[hd]>(.*)$", ln)
        if m:
            name = html.unescape(re.sub(r"<[^>]+>", "", m.group(3))).strip()
            jchr[(m.group(2).lower(), int(m.group(1)))] = name
    s = open("/tmp/ical.htm", encoding="utf-8").read()
    ical, mon = {}, None
    for r in re.findall(r"<tr[^>]*>(.*?)</tr>", s, re.S):
        c = [html.unescape(re.sub(r"<[^>]+>", "", x)).strip()
             for x in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S)]
        if len(c) == 1:
            mon = c[0].lower()
        elif len(c) == 5 and c[2].isdigit():
            ical[(mon, int(c[2]))] = (c[0], c[3])
    entries = []
    for mi, m in enumerate(MONTHS):
        for d in range(1, 30):
            n = jchr[(m, d)]
            rank, alt = ical.get((m, d), (None, None))
            e = {"month": m.capitalize() if m != "décervelage" else "Décervelage",
                 "day": d, "name": n, "rank": rank, "rank_label": RANKS.get(rank)}
            if m == "pédale":
                e["month"] = "Pédale"
            if alt:
                r = difflib.SequenceMatcher(None, norm(n), norm(alt)).ratio()
                if r < 0.6:
                    e["variant_icalendrier"] = alt
                if r < 0.35:      # different feast, so icalendrier's rank may belong to it
                    e["rank_uncertain"] = True
            if d == 29:
                e["imaginary"] = m not in ("gidouille", "gueules")
            entries.append(e)
    out = {
        "title": "Calendrier 'Pataphysique — fêtes et saints",
        "coverage": "377 entries = 13 months × 29 days (incl. the 29th of each month); "
                    "names from jchr.be, ranks from icalendrier.fr; 2 days disagree between "
                    "the two reproductions (stored as variant_icalendrier).",
        "sources": [
            {"name": "jchr.be, Calendrier ’Pataphysique (names)",
             "url": "http://jchr.be/langage/pataphysique.htm",
             "archived": "https://web.archive.org/web/20241008002420/http://jchr.be/langage/pataphysique.htm"},
            {"name": "icalendrier.fr, Le calendrier 'Pataphysique (ranks SPp/SPs/SS/ST/SQ/V)",
             "url": "https://icalendrier.fr/calendriers-saga/calendriers/reforme-fixes/pataphysique"},
            {"name": "fr.wikipedia, Calendrier pataphysique (spot-check examples, rank counts)",
             "url": "https://fr.wikipedia.org/wiki/Calendrier_pataphysique"},
        ],
        "notes": "Not the Collège's official edition (calenpat.pdf, not retrievable); "
                 "editions differ. jchr.be marks retained vulgar-calendar saints with °. "
                 "Rank counts from icalendrier (SPp 3, SPs 8, SS 22, ST 40, V 37) differ "
                 "slightly from fr.wikipedia's (2, 8, 22, 41, 39).",
        "retrieved": RETRIEVED,
        "rank_codes": RANKS,
        "entries": entries,
    }
    json.dump(out, open(os.path.join(HERE, "pata_saints.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    return len(entries), sum(1 for e in entries if "variant_icalendrier" in e)


def grc():
    t = open("/tmp/grc.txt", encoding="utf-8").read()
    sec = t[t.index("===January==="):t.index("== Particular calendars")]

    def clean(s):
        s = re.sub(r"<ref[^>]*/>", "", s)
        s = re.sub(r"<ref[^>]*>.*?</ref>", "", s)
        s = re.sub(r"\{\{[^}]*\}\}", "", s)
        s = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", s).replace("''", "")
        return s.strip()
    MON = ["January", "February", "March", "April", "May", "June", "July", "August",
           "September", "October", "November", "December"]
    fixed, movable_text = [], []
    for ln in sec.splitlines():
        if not ln.startswith("* "):
            continue
        c = clean(ln[2:])
        m = re.match(r"(\d{1,2}) (\w+): (.*)$", c)
        if m and m.group(2) in MON:
            parts = re.split(r"\s[–-]\s(?=[a-z])", m.group(3))
            fixed.append({"month": MON.index(m.group(2)) + 1, "day": int(m.group(1)),
                          "name": parts[0].strip(),
                          "rank": parts[1].strip() if len(parts) > 1 else ""})
        else:
            movable_text.append(c)
    RULES = {  # wiki wording → machine rule (computed in numogram_calendar.py)
        "Sunday after 6 January": {"rule": "weekday_after", "month": 1, "day": 6, "weekday": 6},
        "Monday after Pentecost": {"rule": "easter", "offset": 50},
        "First Sunday after Pentecost": {"rule": "easter", "offset": 56},
        "Thursday after Holy Trinity": {"rule": "easter", "offset": 60},
        "Friday after the Second Sunday after Pentecost": {"rule": "easter", "offset": 68},
        "Saturday after the Second Sunday after Pentecost": {"rule": "easter", "offset": 69},
        "Last Sunday in Ordinary Time": {"rule": "advent", "offset": -7},
        "Sunday within the Octave of Christmas, or, if there is no such Sunday, 30 December":
            {"rule": "holy_family"},
    }
    movable = []
    for c in movable_text:
        when, rest = c.split(": ", 1)
        name, rank = re.split(r"\s[–-]\s(?=[a-z])", rest)
        movable.append(dict(RULES[when], when=when, name=name.strip(), rank=rank.strip()))
    proper = [  # Proper of Time anchors, for context (Wikipedia: Moveable feast)
        {"rule": "easter", "offset": -46, "name": "Ash Wednesday", "rank": "(Proper of Time)"},
        {"rule": "easter", "offset": -7, "name": "Palm Sunday of the Passion of the Lord", "rank": "(Proper of Time)"},
        {"rule": "easter", "offset": -3, "name": "Holy Thursday", "rank": "(Proper of Time)"},
        {"rule": "easter", "offset": -2, "name": "Good Friday of the Passion of the Lord", "rank": "(Proper of Time)"},
        {"rule": "easter", "offset": 0, "name": "Easter Sunday of the Resurrection of the Lord", "rank": "solemnity (Proper of Time)"},
        {"rule": "easter", "offset": 39, "name": "The Ascension of the Lord", "rank": "solemnity (Proper of Time; Sunday in some countries)"},
        {"rule": "easter", "offset": 49, "name": "Pentecost Sunday", "rank": "solemnity (Proper of Time)"},
        {"rule": "advent", "offset": 0, "name": "First Sunday of Advent", "rank": "(Proper of Time)"},
    ]
    out = {
        "title": "General Roman Calendar — celebrations inscribed (current, post-1969)",
        "coverage": f"{len(fixed)} fixed-date celebrations + {len(movable)} movable; plus "
                    f"{len(proper)} Proper-of-Time anchors. No precedence/transfer rules applied.",
        "sources": [
            {"name": "Wikipedia, General Roman Calendar — List of celebrations inscribed in the GRC "
                     "(from Calendarium Romanum Generale, Missale Romanum 2008, with later decrees)",
             "url": "https://en.wikipedia.org/wiki/General_Roman_Calendar"},
            {"name": "Wikipedia, Moveable feast (Proper-of-Time offsets from Easter)",
             "url": "https://en.wikipedia.org/wiki/Moveable_feast"},
        ],
        "retrieved": RETRIEVED,
        "fixed": fixed, "movable": movable + proper,
    }
    json.dump(out, open(os.path.join(HERE, "general_roman_calendar.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    return len(fixed), len(movable)


if __name__ == "__main__":
    print("pata", pata())
    print("grc", grc())
