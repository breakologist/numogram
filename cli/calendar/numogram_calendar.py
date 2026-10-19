#!/usr/bin/env python3
"""
Numogram Calendar — date overlays for numogram divination
Date → Nma 729-day cycle · Tai Xuan head/appraisal · Han gua qi · Decan (+ Book T minor,
       major and court cards) · 'Pataphysical date · saints' days (General Roman Calendar
       with the National Calendars for England and for Wales, 'Pataphysical feasts, folk)
       · a generated research prompt

Usage:
  python3 calendar.py                         (today, Europe/London, all overlays)
  python3 calendar.py --all --date 2026-12-21
  python3 calendar.py --nma --taixuan --date 2026-10-17 --time 21:30
  python3 calendar.py --decan --json
  python3 calendar.py --pata --date 2012-11-10
  python3 calendar.py --nma --nma-epoch 1883-08-27   (choose a different Nma epoch)
  python3 calendar.py --tz Asia/Shanghai --taixuan   (count Tai Xuan days in Chinese civil time)
  python3 calendar.py --list                         (list overlays and providers)
  python3 calendar.py --daily [--date YYYY-MM-DD]    (compact morning reading, all overlays)
  python3 calendar.py --saints --pata-saints --folk  (saints' days: Roman, 'Pataphysical, folk)
  python3 calendar.py --region wales|england|england-wales|general   (default england-wales)
  python3 calendar.py --trumps gd|trad     (Strength VIII/Justice XI [gd, default] or XI/VIII)
  python3 calendar.py --daily --plain      (no pictographic glyphs; --ascii = 7-bit only)

Every output field carries a status tag:
  [src]    rule taken from a cited source
  [approx] computed approximation of a sourced rule (see notes)
  [conv]   a convention this tool had to choose (configurable where possible)
  [spec]   numogram speculation, not a sourced fact

Module name is numogram_calendar (not calendar) so it never shadows the stdlib
`calendar` module; calendar.py next to it is only a CLI wrapper. This module also
deliberately does not import stdlib `calendar` (see is_gregorian_leap), so it works
even when the wrapper's directory is on sys.path.
"""

import datetime as dt
import json
import math
import os
import sys
import unicodedata
from zoneinfo import ZoneInfo

DEFAULT_TZ = "Europe/London"
DEFAULT_TIME = "12:00"

def is_gregorian_leap(y: int) -> bool:
    """Gregorian leap-year rule (same as stdlib calendar.isleap, without importing it)."""
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


# ─── NUMOGRAM ARITHMETIC ───

def digital_root(n: int) -> int:
    """Decimal digital root; 0 stays 0 (zone 0), nonzero multiples of 9 → 9."""
    return 0 if n == 0 else 1 + (n - 1) % 9


def kw_zone(kw: int) -> int:
    """Number zone of a hexagram (wiki Method A): 1 + (KW−1) mod 9 = digital_root(KW)."""
    return 1 + (kw - 1) % 9


# King Wen number by line value v = Σ yang_k·2^(k−1), line 1 (bottom) = bit 0
# (same table as cli/iching.py KW_BY_VALUE; e.g. v=1 → 24 Fu, v=5 → 36).
KW_BY_VALUE = [2, 24, 7, 19, 15, 36, 46, 11, 16, 51, 40, 54, 62, 55, 32, 34, 8, 3, 29, 60, 39, 63,
               48, 5, 45, 17, 47, 58, 31, 49, 28, 43, 23, 27, 4, 41, 52, 22, 18, 26, 35, 21, 64, 38,
               56, 30, 50, 14, 20, 42, 59, 61, 53, 37, 57, 9, 12, 25, 6, 10, 33, 13, 44, 1]


def hexagram_zones(kw: int) -> dict:
    """Both hexagram zones: by lines = iching.py fuxi_zone(v) (0 only for Kun), by number = DR(KW)."""
    v = KW_BY_VALUE.index(kw)
    return {"line_value": v, "zone_lines": digital_root(v), "zone_number": kw_zone(kw)}


def tetragram_zones(head: int) -> dict:
    """Both tetragram zones: by lines = taixuan.py taixuan_zone(i, "value") with i = head−1
    (base-3 line value, 0 only for Centre); by number = DR(head)."""
    return {"line_value": head - 1, "zone_lines": digital_root(head - 1),
            "zone_number": digital_root(head)}


def fmt_zones(x: dict) -> str:
    """'zone 3 by lines · zone 4 by number', or 'zone 5 (lines and number)' if equal."""
    a, b = x["zone_lines"], x["zone_number"]
    return f"zone {a} (lines and number)" if a == b else f"zone {a} by lines · zone {b} by number"


def to_trits(n: int, width: int = 6) -> str:
    """Base-3 digits, most significant first."""
    out = []
    for _ in range(width):
        out.append(str(n % 3))
        n //= 3
    return "".join(reversed(out))


# ─── EPHEMERIS PROVIDERS (registry) ───
# A provider returns an apparent geocentric ecliptic longitude (degrees) for a body
# at a UTC instant. Only the Sun is implemented. Moon/planets are stubs so that a
# lunation overlay or a multi-armed "planetary clock" can plug in later.

PROVIDERS = {}


def provider(body):
    def deco(fn):
        PROVIDERS[body] = fn
        return fn
    return deco


def julian_day(t_utc: dt.datetime) -> float:
    """Julian Day (UT) for an aware UTC datetime."""
    epoch = dt.datetime(2000, 1, 1, 12, tzinfo=dt.timezone.utc)   # JD 2451545.0
    return 2451545.0 + (t_utc - epoch).total_seconds() / 86400.0


def delta_t_seconds(year: float) -> float:
    """ΔT = TT − UT, Espenak & Meeus polynomial for 2005–2050 (NASA eclipse site);
    outside that range a fixed 69 s is used (effect on solar longitude < 0.001°)."""
    if 2005 <= year <= 2050:
        t = year - 2000
        return 62.92 + 0.32217 * t + 0.005589 * t * t
    return 69.0


@provider("sun")
def sun_longitude(t_utc: dt.datetime) -> float:
    """Apparent solar longitude, Meeus 'Astronomical Algorithms' ch. 25 low-accuracy
    method (≈0.01°). Degrees in [0, 360)."""
    jd = julian_day(t_utc) + delta_t_seconds(t_utc.year) / 86400.0   # → JDE (TT)
    T = (jd - 2451545.0) / 36525.0
    L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T * T
    M = math.radians(357.52911 + 35999.05029 * T - 0.0001537 * T * T)
    C = ((1.914602 - 0.004817 * T - 0.000014 * T * T) * math.sin(M)
         + (0.019993 - 0.000101 * T) * math.sin(2 * M)
         + 0.000289 * math.sin(3 * M))
    omega = math.radians(125.04 - 1934.136 * T)
    lam = L0 + C - 0.00569 - 0.00478 * math.sin(omega)
    return lam % 360.0


def _not_yet(body):
    def fn(t_utc):
        raise NotImplementedError(f"ephemeris provider for '{body}' not implemented yet")
    return fn


for _b in ("moon", "mercury", "venus", "mars", "jupiter", "saturn"):
    PROVIDERS[_b] = _not_yet(_b)


def find_solar_longitude(target: float, start: dt.datetime, end: dt.datetime) -> dt.datetime:
    """Instant (UTC) in [start, end] when the Sun reaches `target` degrees (bisection)."""
    def f(t):
        return ((sun_longitude(t) - target + 180.0) % 360.0) - 180.0
    a, b = start, end
    fa = f(a)
    if fa * f(b) > 0:
        raise ValueError("target longitude not bracketed")
    for _ in range(60):
        m = a + (b - a) / 2
        fm = f(m)
        if fa * fm <= 0:
            b = m
        else:
            a, fa = m, fm
    return a + (b - a) / 2


def december_solstice(year: int) -> dt.datetime:
    """UTC instant of the December (winter) solstice, λ☉ = 270°."""
    utc = dt.timezone.utc
    return find_solar_longitude(270.0, dt.datetime(year, 12, 15, tzinfo=utc),
                                dt.datetime(year, 12, 28, tzinfo=utc))


# ─── CONTEXT ───

class Context:
    """Everything an overlay may need, computed lazily: local/UTC time, civil date,
    and ecliptic longitudes from the provider registry (cached per body)."""

    def __init__(self, local: dt.datetime, options=None):
        self.local = local
        self.utc = local.astimezone(dt.timezone.utc)
        self.date = local.date()
        self.tz = local.tzinfo
        self.options = options or {}
        self._lon = {}

    def longitude(self, body: str) -> float:
        if body not in self._lon:
            self._lon[body] = PROVIDERS[body](self.utc)
        return self._lon[body]

    def local_date_of(self, t_utc: dt.datetime) -> dt.date:
        return t_utc.astimezone(self.tz).date()

    def last_winter_solstice(self, on_or_before: dt.date):
        """(UTC instant, local civil date) of the latest Dec solstice whose local
        date is ≤ on_or_before."""
        for y in (on_or_before.year, on_or_before.year - 1):
            t = december_solstice(y)
            if self.local_date_of(t) <= on_or_before:
                return t, self.local_date_of(t)
        raise ValueError("no solstice found")


# ─── OVERLAY REGISTRY ───
# name → dict(flag, fn, needs, help, enabled). An overlay is fn(ctx) → dict.
# `needs` lists ephemeris bodies it reads via ctx.longitude(), so a future
# planetary clock / lunation overlay just declares ("sun", "moon", ...).

OVERLAYS = {}


def overlay(name, flag, help, needs=(), enabled=True):
    def deco(fn):
        OVERLAYS[name] = {"flag": flag, "fn": fn, "needs": tuple(needs),
                          "help": help, "enabled": enabled}
        return fn
    return deco


# ─── 1. NMA ZYGOTRIADIC CALENDAR ───
# CCRU (ccru.net/declab.htm): "6 digits to divide a double-year period of 729 days
# into fractional powers of three ... intercalations of three additional days every
# second cycle, or four years." No epoch is given by CCRU.

NMA_EPOCHS = {
    "unix": ("1970-01-01", "epoch used by the xeno.cx zygotriadic calendar (Lillian Patch), "
                           "a modern reconstruction; not CCRU"),
    "krakatau": ("1883-08-27", "Krakatau eruption, the 'calamity of 1883' in CCRU; "
                               "thematic choice only [spec]"),
    "ktime": ("1900-01-01", "CCRU K-Time zero (=00 = AD 1900); CCRU glossary, but a "
                            "different calendar [spec]"),
}
NMA_DEFAULT_EPOCH = "unix"


def nma_day(days_since_epoch: int) -> dict:
    """Place a day in the 1461-day supercycle: cycle A (729), cycle B (729),
    then 3 intercalary days [conv: intercalary days placed at the end of cycle B]."""
    s = days_since_epoch % 1461
    supercycle = days_since_epoch // 1461
    if s < 729:
        return {"supercycle": supercycle, "cycle": "A", "index": s, "intercalary": None}
    if s < 1458:
        return {"supercycle": supercycle, "cycle": "B", "index": s - 729, "intercalary": None}
    return {"supercycle": supercycle, "cycle": "B", "index": None, "intercalary": s - 1457}


@overlay("nma", "--nma", "Nma 729-day zygotriadic cycle (CCRU), configurable epoch")
def nma_overlay(ctx):
    key = ctx.options.get("nma_epoch", NMA_DEFAULT_EPOCH)
    if key in NMA_EPOCHS:
        epoch_s, epoch_note = NMA_EPOCHS[key]
    else:
        epoch_s, epoch_note = key, "user-supplied epoch"
    epoch = dt.date.fromisoformat(epoch_s)
    days = (ctx.date - epoch).days
    p = nma_day(days)
    out = {"epoch": epoch_s, "epoch_note": epoch_note + " [conv]",
           "days_since_epoch": days, "supercycle": p["supercycle"], "cycle": p["cycle"]}
    if p["index"] is None:
        out.update({"intercalary_day": p["intercalary"],
                    "note": "intercalary day (one of 3 per 4 years) — no 6-trit address [conv]"})
        return out
    i = p["index"]
    head, appraisal = i // 9 + 1, i % 9 + 1
    out.update({
        "index": i, "day_of_cycle": i + 1,
        "trits": to_trits(i),
        "zone": digital_root(i),
        "zone_note": "zone = digital root of the 0-based index; mod 9 depends only on the "
                     "lowest two trits (3^k ≡ 0 mod 9 for k ≥ 2) [spec]",
        "taixuan_address": {"head": head, "appraisal": appraisal,
                            "glyph": chr(0x1D306 + head - 1),
                            "name": tetragram_name(head),
                            "note": "upper 4 trits = head, lower 2 trits = appraisal [spec]"},
    })
    return out


# ─── 2. TAI XUAN CALENDAR ───
# 81 heads × 9 appraisals = 729; two appraisals = one day (day + night) → 364½ days;
# 中 Centre, appraisal 初一, starts at the winter solstice; the extra appraisals
# 踦 Ji and 嬴 Ying make up the remainder to 365¼ (ctext 太玄 說玄; 永樂大典 太玄敘錄).

APPRAISAL_NAMES = ["初一", "次二", "次三", "次四", "次五", "次六", "次七", "次八", "上九"]


def tetragram_name(head: int) -> str:
    words = unicodedata.name(chr(0x1D306 + head - 1), "?").replace("TETRAGRAM FOR ", "").lower().split()
    return " ".join(w if (i and w in ("or", "of", "the", "and")) else w.capitalize()
                    for i, w in enumerate(words))


def tetragram_lines(head: int) -> str:
    """Lines top→bottom (Region, Province, Department, Family); 1 = unbroken,
    2 = once broken, 3 = twice broken. Head 1 = 1111."""
    return "".join(str(int(c) + 1) for c in to_trits(head - 1, 4))


def taixuan_position(appraisal_index: int) -> dict:
    """Global appraisal index (0 = 中 初一) → head/appraisal or Ji/Ying."""
    k = appraisal_index
    if k < 729:
        head, a = k // 9 + 1, k % 9 + 1
        return {"head": head, "appraisal": a}
    if k == 729:
        return {"extra": "踦 Ji"}
    return {"extra": "嬴 Ying"}


@overlay("taixuan", "--taixuan", "Tai Xuan head (1–81) and appraisal (1–9), Ji/Ying",
         needs=("sun",))
def taixuan_overlay(ctx):
    # [conv] daytime appraisal 06:00–17:59 local, night 18:00–05:59 (night after
    # midnight belongs to the previous civil day).
    shifted = ctx.local - dt.timedelta(hours=6)
    eff_date = shifted.date()
    half = 0 if shifted.hour < 12 else 1
    sol_utc, sol_date = ctx.last_winter_solstice(eff_date)
    d = (eff_date - sol_date).days
    k = 2 * d + half
    pos = taixuan_position(k)
    out = {"solstice_utc": sol_utc.strftime("%Y-%m-%d %H:%M"),
           "day_since_solstice": d, "half": "晝 day" if half == 0 else "夜 night",
           "appraisal_index": k}
    if "head" in pos:
        h, a = pos["head"], pos["appraisal"]
        out.update({"head": h, "glyph": chr(0x1D306 + h - 1), "name": tetragram_name(h),
                    "lines": tetragram_lines(h), "appraisal": a,
                    "appraisal_name": APPRAISAL_NAMES[a - 1],
                    **tetragram_zones(h), "zone": digital_root(h),
                    "zone_note": "zone_lines = DR of base-3 line value (head−1); zone_number = "
                                 "DR of head; 'zone' = zone_number (legacy) [spec]"})
    else:
        out["extra"] = pos["extra"]
        out["note"] = ("Ji = night of day 364 (½ day); Ying = any civil remainder before the "
                       "next solstice day (sources: ¼ day) [approx]")
    out["notes"] = ("year starts on the local civil date of the true (astronomical) winter "
                    "solstice in the chosen time zone [approx: Han practice used mean "
                    "reckoning and Chinese local time]; day/night split at 06:00/18:00 [conv]")
    return out


# ─── 3. HAN GUA QI (Meng Xi, 六日七分) ───
# 60 hexagrams (all but 坎離震兌) × 6 7/80 days = 365¼ from the winter solstice,
# order from 易緯稽覽圖 / 新唐書 曆志; ranks cycle 公 辟 侯 大夫 卿.
# The four cardinal hexagrams govern the 24 solar terms, one line each.

GUAQI = [
    ("中孚", 61), ("復", 24), ("屯", 3), ("謙", 15), ("睽", 38), ("升", 46), ("臨", 19),
    ("小過", 62), ("蒙", 4), ("益", 42), ("漸", 53), ("泰", 11), ("需", 5), ("隨", 17),
    ("晉", 35), ("解", 40), ("大壯", 34), ("豫", 16), ("訟", 6), ("蠱", 18), ("革", 49),
    ("夬", 43), ("旅", 56), ("師", 7), ("比", 8), ("小畜", 9), ("乾", 1), ("大有", 14),
    ("家人", 37), ("井", 48), ("咸", 31), ("姤", 44), ("鼎", 50), ("豐", 55), ("渙", 59),
    ("履", 10), ("遯", 33), ("恆", 32), ("節", 60), ("同人", 13), ("損", 41), ("否", 12),
    ("巽", 57), ("萃", 45), ("大畜", 26), ("賁", 22), ("觀", 20), ("歸妹", 54), ("無妄", 25),
    ("明夷", 36), ("困", 47), ("剝", 23), ("艮", 52), ("既濟", 63), ("噬嗑", 21), ("大過", 28),
    ("坤", 2), ("未濟", 64), ("蹇", 39), ("頤", 27),
]
RANKS = ["公 duke", "辟 sovereign", "侯 marquis", "大夫 grandee", "卿 minister"]
GUAQI_DAYS = 365.25 / 60          # 6 7/80 days
SOLAR_TERMS = ["冬至", "小寒", "大寒", "立春", "雨水", "驚蟄", "春分", "清明", "穀雨",
               "立夏", "小滿", "芒種", "夏至", "小暑", "大暑", "立秋", "處暑", "白露",
               "秋分", "寒露", "霜降", "立冬", "小雪", "大雪"]
CARDINAL = [("坎", 29), ("震", 51), ("離", 30), ("兌", 58)]


@overlay("guaqi", "--guaqi", "Han gua qi hexagram (Meng Xi 六日七分)", needs=("sun",))
def guaqi_overlay(ctx):
    sol_utc, _ = ctx.last_winter_solstice(ctx.date)
    if sol_utc > ctx.utc:                       # same civil day, before the instant
        sol_utc = december_solstice(sol_utc.year - 1)
    elapsed = (ctx.utc - sol_utc).total_seconds() / 86400.0
    i = min(int(elapsed // GUAQI_DAYS), 59)
    name, kw = GUAQI[i]
    q = int(((ctx.longitude("sun") - 270.0) % 360.0) // 15)
    cname, ckw = CARDINAL[q // 6]
    return {
        "scheme": "Meng Xi 六日七分 (60 hexagrams × 6 7/80 d from the winter solstice) [src]",
        "position": i + 1, "hexagram": name, "king_wen": kw, "glyph": chr(0x4DC0 + kw - 1),
        "rank": RANKS[i % 5], "day_in_hexagram": round(elapsed - i * GUAQI_DAYS, 2),
        **hexagram_zones(kw), "zone": kw_zone(kw),
        "zone_note": "zone_lines = DR of binary line value (line 1 = 1); zone_number = "
                     "1+(KW−1)%9; 'zone' = zone_number (legacy) [conv]",
        "hexagram_en": hexagram_en(kw),
        "solar_term": SOLAR_TERMS[q], "solar_term_en": SOLAR_TERMS_EN[q], "cardinal": cname, "cardinal_king_wen": ckw,
        "cardinal_line": q % 6 + 1,
        "notes": "solstice = true astronomical instant; solar terms by true longitude "
                 "(定氣, 15° steps) rather than Han mean terms (平氣) [approx]",
    }


# ─── 4. DECANS ───
# 36 × 10° of the tropical zodiac; Chaldean rulers from Mars at Aries I; Golden Dawn
# Book T: minor arcana 2–10 (cardinal 2–4, fixed 5–7, mutable 8–10), suit by element.

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio",
         "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
CHALDEAN = ["Mars", "Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter"]
SUITS = ["Wands", "Pentacles", "Swords", "Cups"]          # fire, earth, air, water
ROMAN = ["I", "II", "III"]


ELEMENTS = ["Fire", "Earth", "Air", "Water"]               # sign % 4
ELEMENT_GLYPH = {"Fire": "🜂", "Earth": "🜃", "Air": "🜁", "Water": "🜄"}
PLANET_GLYPH = {"Sun": "☉", "Moon": "☽", "Mercury": "☿", "Venus": "♀", "Mars": "♂",
                "Jupiter": "♃", "Saturn": "♄"}
SIGN_GLYPH = dict(zip(SIGNS, "♈♉♊♋♌♍♎♏♐♑♒♓"))

# Book T, "The Twenty-Two Keys of the Book: letter attribution" (Equinox I:8, 1912;
# hermeticcloud.com/library/book-t/). Values: (number in Golden Dawn/RWS order,
# common title, Book T title). Book T itself prints Fortitude as 11 and Justice as 8
# (the traditional Marseille numbers) while attributing Teth/Leo to Fortitude and
# Lamed/Libra to Justice; the Golden Dawn (Cipher MS) order, adopted by Rider–Waite–
# Smith, renumbers them Strength VIII and Justice XI so the numbers follow the letters
# (en.wikipedia.org/wiki/Strength_(tarot_card)). Both conventions are offered.
SIGN_TRUMP = {
    "Aries": (4, "The Emperor", "The Emperor"), "Taurus": (5, "The Hierophant", "The Hierophant"),
    "Gemini": (6, "The Lovers", "The Lovers"), "Cancer": (7, "The Chariot", "The Chariot"),
    "Leo": (8, "Strength", "Fortitude"), "Virgo": (9, "The Hermit", "The Hermit"),
    "Libra": (11, "Justice", "Justice"), "Scorpio": (13, "Death", "Death"),
    "Sagittarius": (14, "Temperance", "Temperance"), "Capricorn": (15, "The Devil", "The Devil"),
    "Aquarius": (17, "The Star", "The Star"), "Pisces": (18, "The Moon", "The Moon"),
}
PLANET_TRUMP = {
    "Mercury": (1, "The Magician", "The Magician"),
    "Moon": (2, "The High Priestess", "The High Priestess"),
    "Venus": (3, "The Empress", "The Empress"),
    "Jupiter": (10, "Wheel of Fortune", "The Wheel of Fate"),
    "Mars": (16, "The Tower", "The Blasted Tower"),
    "Sun": (19, "The Sun", "The Sun"),
    "Saturn": (21, "The World", "The Universe"),
}
TRUMP_CONVENTIONS = {
    "gd": "Golden Dawn / Rider–Waite–Smith order: VIII Strength = Leo, XI Justice = Libra",
    "trad": "traditional (Marseille) numbers, as printed in Book T: XI Fortitude = Leo, "
            "VIII Justice = Libra",
}
TRUMP_SWAP = {8: 11, 11: 8}

# Book T, "The Spheres of Influence of the Court Cards": Knights, Queens and Princes
# each rule 30° from 20° of one sign to 20° of the next (Princesses rule polar
# quadrants, not zodiac spans). Start longitudes (°) of each span:
COURT_SPANS = [(20, "Prince", "Pentacles"), (50, "Knight", "Swords"), (80, "Queen", "Cups"),
               (110, "Prince", "Wands"), (140, "Knight", "Pentacles"), (170, "Queen", "Swords"),
               (200, "Prince", "Cups"), (230, "Knight", "Wands"), (260, "Queen", "Pentacles"),
               (290, "Prince", "Swords"), (320, "Knight", "Cups"), (350, "Queen", "Wands")]

# Unicode playing cards (U+1F0A0 block) [conv]: tarot suits drawn as the French suits
# usually equated with them (Swords♠ Cups♥ Pentacles♦ Wands♣); Book T Prince drawn as
# the King card. Trumps U+1F0E0 (Fool) + n are the French tarot trumps, used by number.
SUIT_BASE = {"Swords": 0x1F0A0, "Cups": 0x1F0B0, "Pentacles": 0x1F0C0, "Wands": 0x1F0D0}
COURT_OFFSET = {"Knight": 0xC, "Queen": 0xD, "Prince": 0xE}

ROMAN_NUM = ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII",
             "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI"]


def trump(n: int, title: str, book_t: str, convention: str = "gd") -> dict:
    if convention == "trad":
        n = TRUMP_SWAP.get(n, n)
    return {"number": n, "roman": ROMAN_NUM[n], "title": title, "book_t_title": book_t,
            "glyph": chr(0x1F0E0 + n)}


def court_of(lon: float) -> dict:
    i = int(((lon - 20.0) % 360.0) // 30)
    start, rank, suit = COURT_SPANS[i]
    s0, s1 = SIGNS[start // 30], SIGNS[(start // 30 + 1) % 12]
    return {"card": f"{rank} of {suit}", "rank": rank, "suit": suit,
            "glyph": chr(SUIT_BASE[suit] + COURT_OFFSET[rank]),
            "span": f"20° {s0} – 20° {s1}",
            "span_glyph": f"20°{SIGN_GLYPH[s0]}–20°{SIGN_GLYPH[s1]}"}


def decan_of(lon: float, convention: str = "gd") -> dict:
    lon %= 360.0
    n = int(lon // 10) + 1                   # 1..36
    sign = (n - 1) // 3
    d = (n - 1) % 3 + 1
    rank = 2 + 3 * (sign % 3) + (d - 1)
    ruler = CHALDEAN[(n - 1) % 7]
    suit = SUITS[sign % 4]
    return {"decan": n, "sign": SIGNS[sign], "sign_glyph": SIGN_GLYPH[SIGNS[sign]],
            "decan_in_sign": ROMAN[d - 1], "element": ELEMENTS[sign % 4],
            "element_glyph": ELEMENT_GLYPH[ELEMENTS[sign % 4]],
            "ruler": ruler, "ruler_glyph": PLANET_GLYPH[ruler],
            "card": f"{rank} of {suit}", "card_rank": rank,
            "card_glyph": chr(SUIT_BASE[suit] + rank),
            "sign_trump": trump(*SIGN_TRUMP[SIGNS[sign]], convention),
            "ruler_trump": trump(*PLANET_TRUMP[ruler], convention),
            "trump_convention": convention,
            "court": court_of(lon)}


@overlay("decan", "--decan", "Decan (36 × 10°) of the Sun, ruler, Book T minor/major/court",
         needs=("sun",))
def decan_overlay(ctx):
    lon = ctx.longitude("sun")
    d = decan_of(lon, ctx.options.get("trumps", "gd"))
    d.update({
        "sun_longitude": round(lon, 3),
        "degree_in_sign": round(lon % 30, 2),
        "zone": digital_root(d["decan"]),
        "decadence_rank": d["card_rank"] - 1,
        "trump_note": TRUMP_CONVENTIONS[d["trump_convention"]] + " [conv]; sign and planet "
                      "trumps from Book T letter attributions [src]",
        "court_note": "Book T court spans (20° to 20°) [src]; Unicode card glyphs map "
                      "Swords♠ Cups♥ Pentacles♦ Wands♣ and Prince→King [conv]",
        "hooks": "zone = DR of decan number; Book T rank 2–10 shifted to Decadence rank "
                 "1–9 (both 9 × 4 = 36); 36 = T(8) = Gt-36 [spec]",
        "sources": "rulers, minor/major/court cards: Golden Dawn Book T [src]; longitude: "
                   "Meeus low-precision (~0.01°) [approx]",
    })
    return d


# ─── 5. 'PATAPHYSICAL CALENDAR ───
# Collège de 'Pataphysique (1948/49). Era from 8 Sept 1873 vulg. = 1 Absolu 1 E.P.;
# 13 months, twelve of 28 days + Gidouille 29; 29 Gueules exists in leap years.
# The 29ths are outside the week: "hunyadi" (29 Gidouille), "hunyadi gras" (29 Gueules);
# every 1st/8th/15th/22nd is a Sunday, every 13th a Friday.
# Sources: en.wikipedia.org/wiki/Pataphysics#Pataphysical_calendar;
#          fr.wikipedia.org/wiki/Calendrier_pataphysique.

PATA_MONTHS = ["Absolu", "Haha", "As", "Sable", "Décervelage", "Gueules", "Pédale",
               "Clinamen", "Palotin", "Merdre", "Gidouille", "Tatane", "Phalle"]
PATA_WEEK = ["dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"]


def pataphysical(date: dt.date) -> dict:
    start_year = date.year if date >= dt.date(date.year, 9, 8) else date.year - 1
    ep_year = start_year - 1872
    offset = (date - dt.date(start_year, 9, 8)).days
    leap = is_gregorian_leap(start_year + 1)
    for m in PATA_MONTHS:
        length = 29 if m == "Gidouille" or (m == "Gueules" and leap) else 28
        if offset < length:
            day = offset + 1
            break
        offset -= length
    if day == 29:
        weekday = "hunyadi gras" if m == "Gueules" else "hunyadi"
    else:
        weekday = PATA_WEEK[(day - 1) % 7]
    return {"day": day, "month": m, "year_ep": ep_year, "weekday": weekday,
            "text": f"{weekday} {day} {m} {ep_year} E.P."}


@overlay("pata", "--pata", "'Pataphysical date (Collège de 'Pataphysique)")
def pata_overlay(ctx):
    p = pataphysical(ctx.date)
    p.pop("feast", None)
    if p["year_ep"] < 1:
        p["note"] = "date precedes the pataphysical era (years ≤ 0 are proleptic) [conv]"
    return p


# ─── 7. SAINTS & FEASTS (data files in ./data, each with source URLs) ───

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
_DATA = {}


def load_data(name: str) -> dict:
    if name not in _DATA:
        with open(os.path.join(DATA_DIR, name), encoding="utf-8") as f:
            _DATA[name] = json.load(f)
    return _DATA[name]


def easter(year: int) -> dt.date:
    """Gregorian Easter Sunday, anonymous Gregorian algorithm (Meeus/Jones/Butcher)."""
    a, b, c = year % 19, year // 100, year % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = (h + l - 7 * m + 114) % 31 + 1
    return dt.date(year, month, day)


def advent_sunday(year: int) -> dt.date:
    """First Sunday of Advent: the Sunday from 27 Nov to 3 Dec."""
    d = dt.date(year, 11, 27)
    return d + dt.timedelta((6 - d.weekday()) % 7)


def movable_dates(entry: dict, year: int):
    """Dates in `year` for a movable rule (see data JSON). Returns a list of dates."""
    r = entry["rule"]
    if r == "easter":
        return [easter(year) + dt.timedelta(entry["offset"])]
    if r == "easter_range":
        e = easter(year)
        return [e + dt.timedelta(o) for o in range(entry["start"], entry["end"] + 1)]
    if r == "advent":
        return [advent_sunday(year) + dt.timedelta(entry["offset"])]
    if r == "weekday_after":              # first <weekday> strictly after month/day
        d = dt.date(year, entry["month"], entry["day"])
        return [d + dt.timedelta((entry["weekday"] - d.weekday() - 1) % 7 + 1)]
    if r == "holy_family":                # Sunday 26–31 Dec, else 30 Dec
        for dd in range(26, 32):
            if dt.date(year, 12, dd).weekday() == 6:
                return [dt.date(year, 12, dd)]
        return [dt.date(year, 12, 30)]
    raise ValueError(f"unknown rule {r}")


def feasts_on(date: dt.date, data: dict) -> list:
    out = [dict(e, movable=False) for e in data.get("fixed", [])
           if (e["month"], e["day"]) == (date.month, date.day)]
    for e in data.get("movable", []):
        if date in movable_dates(e, date.year):
            out.append(dict(e, movable=True))
    return out


REGIONS = {
    "general": [],
    "england": ["england"],
    "wales": ["wales"],
    "england-wales": ["wales", "england"],    # Wales listed first; both national calendars
}
DEFAULT_REGION = "england-wales"
REGION_LABEL = {"general": "General Roman Calendar", "england": "England",
                "wales": "Wales", "england-wales": "England & Wales"}
REGION_TAG = {"wales": "W", "england": "E"}
NATIONAL_FILE = "national_england_wales.json"


def ordinal(n: int) -> str:
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def baptism_date(year: int, region: str) -> dt.date:
    """Sunday after 6 Jan; in England & Wales, if Epiphany is kept on Sunday 7/8 Jan,
    the Monday after (Liturgy Office Calendar Notes 2024: Sun 7 Jan / Mon 8 Jan)."""
    if region != "general":
        ep = ew_holyday(dt.date(year, 1, 6))
        if ep.day in (7, 8):
            return ep + dt.timedelta(1)
    return movable_dates({"rule": "weekday_after", "month": 1, "day": 6, "weekday": 6}, year)[0]


def sunday_name(date: dt.date, region: str = DEFAULT_REGION):
    """Proper-of-Time name for a Sunday of Advent, Lent, Easter or Ordinary Time
    (numbering as in the Liturgy Office Calendar Notes); None otherwise."""
    if date.weekday() != 6:
        return None
    y = date.year
    e, adv = easter(y), advent_sunday(y)
    if adv <= date <= dt.date(y, 12, 24):
        return f"{ordinal((date - adv).days // 7 + 1)} Sunday of Advent"
    if e - dt.timedelta(42) <= date <= e - dt.timedelta(14):
        return f"{ordinal((date - (e - dt.timedelta(42))).days // 7 + 1)} Sunday of Lent"
    if date == e - dt.timedelta(7):
        return "Palm Sunday"
    if e <= date <= e + dt.timedelta(49):
        k = (date - e).days // 7
        return {0: "Easter Sunday", 7: "Pentecost Sunday"}.get(k, f"{ordinal(k + 1)} Sunday of Easter")
    b = baptism_date(y, region)
    first_after = b + dt.timedelta((6 - b.weekday()) % 7 or 7)
    if first_after <= date < e - dt.timedelta(46):
        return f"{ordinal((date - first_after).days // 7 + 2)} Sunday in Ordinary Time"
    king = adv - dt.timedelta(7)
    if e + dt.timedelta(49) < date <= king:
        return f"{ordinal(34 - (king - date).days // 7)} Sunday in Ordinary Time"
    return None


def ew_holyday(d: dt.date) -> dt.date:
    """England & Wales: holydays falling on Saturday or Monday move to the Sunday
    (Bishops' Conference 1984; liturgyoffice.org.uk/Calendar/)."""
    return d + dt.timedelta({5: 1, 0: -1}.get(d.weekday(), 0))


def ew_moves(year: int):
    """(match, standard date, England & Wales date) for GRC celebrations that the
    Liturgy Office places on a different day. Verified against Calendar Notes 2024–27."""
    moves = []
    for (m, d), key in [((1, 6), "Epiphany"), ((6, 29), "Peter and Paul"),
                        ((8, 15), "Assumption"), ((11, 1), "All Saints")]:
        std = dt.date(year, m, d)
        moves.append((key, std, ew_holyday(std)))
    saints = ew_holyday(dt.date(year, 11, 1))
    souls = dt.date(year, 11, 2)
    moves.append(("Faithful Departed", souls, souls + dt.timedelta(1) if saints == souls else souls))
    moves.append(("Baptism of the Lord", baptism_date(year, "general"), baptism_date(year, "ew")))
    e = easter(year)
    moves.append(("Body and Blood", e + dt.timedelta(60), e + dt.timedelta(63)))
    return [mv for mv in moves if mv[1] != mv[2]]


def grc_on(date: dt.date, region: str) -> list:
    data = load_data("general_roman_calendar.json")
    items = feasts_on(date, data)
    if region == "general":
        return items
    out = []
    for c in items:
        mv = next((mv for mv in ew_moves(date.year) if mv[0] in c["name"] and mv[1] == date), None)
        if mv is None:
            out.append(c)
    for key, std, new in ew_moves(date.year):
        if new == date:
            src = next((c for c in feasts_on(std, data) if key in c["name"]), None)
            if src:
                out.append(dict(src, transferred_from=std.isoformat(),
                                note="England & Wales date [src: Liturgy Office]"))
    return out


def solemnity_transfer(d: dt.date) -> dt.date:
    """UNLY 60 as applied by the Liturgy Office: a national solemnity in Holy Week or
    the Easter Octave → Monday after the 2nd Sunday of Easter; on a Sunday of Advent,
    Lent or Easter → the Monday."""
    e = easter(d.year)
    if e - dt.timedelta(7) <= d <= e + dt.timedelta(7):
        return e + dt.timedelta(8)
    name = sunday_name(d)
    if name and ("Advent" in name or "Lent" in name or "Easter" in name):
        return d + dt.timedelta(1)
    return d


def national_on(date: dt.date, region: str) -> list:
    if region == "general":
        return []
    nat = load_data(NATIONAL_FILE)
    e = easter(date.year)
    out = []
    for reg in REGIONS[region]:
        for x in nat[reg]:
            base = dt.date(date.year, x["month"], x["day"])
            item = {k: v for k, v in x.items() if k not in ("month", "day", "supersedes",
                                                            "transfer_if_impeded")}
            item["region"] = reg
            if x.get("transfer_if_impeded"):
                kept = solemnity_transfer(base)
                if kept != base and date == base:
                    out.append(dict(item, transferred_to=kept.isoformat()))
                elif kept == date:
                    out.append(dict(item, **({"transferred_from": base.isoformat()}
                                             if kept != base else {})))
                continue
            if base != date:
                continue
            if e - dt.timedelta(7) <= date <= e + dt.timedelta(7):
                item["impeded"] = "Holy Week / Easter Octave"
            elif date.weekday() == 6:
                item["impeded"] = "Sunday"
            out.append(item)
        for x in nat["movable"]:
            if reg in x["regions"] and date in movable_dates(x, date.year):
                if not any(o["name"] == x["name"] for o in out):
                    out.append({"name": x["name"], "rank": x["rank"], "region": "england-wales",
                                "when": x["when"]})
    return out


def superseded(date: dt.date, region: str):
    """GRC names on `date` replaced by a national entry (raised rank or moved)."""
    if region == "general":
        return []
    nat = load_data(NATIONAL_FILE)
    return [s["match"] for reg in REGIONS[region] for x in nat[reg]
            for s in x.get("supersedes", []) if (s["month"], s["day"]) == (date.month, date.day)]


@overlay("saints", "--saints", "Catholic calendar: General Roman + national propers (--region)")
def saints_overlay(ctx):
    region = ctx.options.get("region", DEFAULT_REGION)
    sup = superseded(ctx.date, region)
    items = []
    for c in grc_on(ctx.date, region):
        if any(m in c["name"] for m in sup):
            continue
        items.append({k: c[k] for k in ("name", "rank", "movable", "transferred_from", "note")
                      if k in c})
    day_name = sunday_name(ctx.date, region)
    if any(c["rank"].startswith("solemnity") or "Proper of Time" in c["rank"] for c in items):
        day_name = None                # the Sunday is itself the named celebration
    out = {"region": region, "region_label": REGION_LABEL[region], "day_name": day_name,
           "celebrations": items, "national": national_on(ctx.date, region),
           "easter": easter(ctx.date.year).isoformat(),
           "source": load_data("general_roman_calendar.json")["sources"][0]["url"]}
    if region != "general":
        out["national_source"] = [s["url"] for s in load_data(NATIONAL_FILE)["sources"][:4]]
        out["notes"] = ("[src] GRC as inscribed, with England & Wales transfers (holydays, "
                        "Body and Blood on Sunday) and the national propers; GRC entries "
                        "raised or moved by a national calendar are shown only in the national "
                        "list. Full precedence for GRC memorials is not applied [conv]")
    else:
        out["notes"] = ("[src] list as inscribed; precedence/transfer rules (Sundays, "
                        "national calendars) not applied [conv]")
    return out


@overlay("pata_saints", "--pata-saints", "'Pataphysical saint/feast of the day (sourced list)")
def pata_saints_overlay(ctx):
    p = pataphysical(ctx.date)
    data = load_data("pata_saints.json")
    e = next((x for x in data["entries"]
              if x["month"] == p["month"] and x["day"] == p["day"]), None)
    out = {"date": p["text"]}
    if e:
        out.update({k: v for k, v in e.items() if k not in ("month", "day")})
    out["source"] = data["sources"][0]["url"]
    return out


@overlay("folk", "--folk", "Folk saints & traditional days (curated, optional)")
def folk_overlay(ctx):
    data = load_data("folk_feasts.json")
    hits = feasts_on(ctx.date, data)
    md = (ctx.date.month, ctx.date.day)
    for r in data.get("ranges", []):
        a, b = tuple(r["start"]), tuple(r["end"])
        if (a <= md <= b) if a <= b else (md >= a or md <= b):
            hits.append(r)
    items = [{k: e[k] for k in ("name", "kind", "region", "note", "source") if k in e}
             for e in hits]
    return {"observances": items, "label": "folk/popular — not official liturgy"}


# ─── 6. LUNATION (stub) ───

@overlay("lunation", "--lunation", "Lunation (not implemented: needs a Moon provider)",
         needs=("sun", "moon"), enabled=False)
def lunation_overlay(ctx):
    # Future: elongation = λ☾ − λ☉ → phase / lunation number / tithi.
    return {"status": "not implemented",
            "note": "requires PROVIDERS['moon']; see README future work"}


# ─── RESEARCH PROMPT (template-based, deterministic) ───
# Combines the day's computed elements into a question. It states no facts: every
# slot is filled from the overlays above, and the template is picked by date ordinal.

PROMPT_TEMPLATES = [
    "How might {ruler} ({ruler_trump}) colour the Tai Xuan theme '{tetragram}', and does "
    "'{hexagram}' echo or resist it?",
    "Trace a thread from {sign_trump} ({sign}) to the hexagram '{hexagram}': does anything "
    "in the life or cult of {saint} sit on that thread?",
    "Set the {minor} beside tetragram {head} '{tetragram}': where do {card_rank} and {head} "
    "meet on the numogram (decan zone {decan_zone}; tetragram {tx_zones})?",
    "What links the {court}, '{hexagram}' and {saint}? Look for a source before trusting "
    "the link.",
    "Read {ruler_trump} against '{tetragram}' and the day's solar term {solar_term}: one "
    "image, one doubt.",
]


# First words of comma-separated title segments to drop from a saint's name
# ("Priest", "Bishop and Doctor of the Church", "patron of Wales", "the First Martyr" …).
SAINT_TITLE_WORDS = {
    "abbot", "abbess", "apostle", "apostles", "archangels", "bishop", "bishops", "deacon",
    "doctor", "evangelist", "hermit", "king", "martyr", "martyrs", "monk", "mother", "parents",
    "patron", "patrons", "pope", "priest", "priests", "religious", "spouse", "the", "virgin",
    "incl.", "kept", "with",
}


def short_saint(name: str) -> str:
    """Drop title segments but keep every name: 'Saints John de Brébeuf, Isaac Jogues,
    Priests, and Companions, Martyrs' -> 'Ss John de Brébeuf, Isaac Jogues and Companions'.
    (Formerly cut at the first comma, which lost co-saints.)"""
    parts = [p.strip() for p in name.split(",")]
    out = [parts[0]]
    for seg in parts[1:]:
        if not seg or any(c in seg for c in ";(—") or any(c.isdigit() for c in seg):
            break
        first = seg.split()[0].lower()
        if first in SAINT_TITLE_WORDS:
            continue
        if first == "and":
            out[-1] += " " + seg
        else:
            out.append(seg)
    return ", ".join(out).replace("Saint ", "St ").replace("Saints ", "Ss ")


def research_prompt(r) -> dict:
    need = ("decan", "taixuan", "guaqi")
    if not all(k in r for k in need) or "head" not in r["taixuan"]:
        return {}
    d, t, g = r["decan"], r["taixuan"], r["guaqi"]
    saint = None
    if "saints" in r:
        pool = r["saints"]["national"] + r["saints"]["celebrations"]
        pool = [c for c in pool if "Proper of Time" not in c["rank"]]
        if pool:
            saint = short_saint(pool[0]["name"])
    if not saint and r.get("pata_saints", {}).get("name"):
        saint = r["pata_saints"]["name"].split(",")[0]
    rt, st = d["ruler_trump"], d["sign_trump"]
    slots = {
        "ruler": d["ruler"], "ruler_trump": f"{rt['roman']} {rt['title']}",
        "sign": d["sign"], "sign_trump": f"{st['roman']} {st['title']}",
        "tetragram": t["name"], "head": t["head"], "tx_zone": t["zone"], "tx_zones": fmt_zones(t).replace(" · ", ", "),
        "hexagram": g.get("hexagram_en", g["hexagram"]), "solar_term": g.get("solar_term_en", g["solar_term"]),
        "minor": d["card"], "card_rank": d["card_rank"], "decan_zone": d["zone"],
        "court": d["court"]["card"], "saint": saint or "the day's saint",
    }
    i = dt.date.fromisoformat(r["date"]).toordinal() % len(PROMPT_TEMPLATES)
    return {"template": i, "text": PROMPT_TEMPLATES[i].format(**slots),
            "label": "generated prompt — a question to research, not a claim"}


# ─── RUN / FORMAT ───

def build_context(date_s=None, time_s=None, tz_name=DEFAULT_TZ, options=None):
    tz = ZoneInfo(tz_name)
    date = dt.date.fromisoformat(date_s) if date_s else dt.datetime.now(tz).date()
    hh, mm = (int(x) for x in (time_s or DEFAULT_TIME).split(":"))
    local = dt.datetime(date.year, date.month, date.day, hh, mm, tzinfo=tz)
    return Context(local, options)


def run(ctx, names):
    result = {"date": ctx.date.isoformat(), "time": ctx.local.strftime("%H:%M"),
              "tz": str(ctx.tz), "tz_abbrev": ctx.local.tzname(),
              "utc": ctx.utc.strftime("%Y-%m-%d %H:%M"),
              "region": ctx.options.get("region", DEFAULT_REGION)}
    for n in names:
        o = OVERLAYS[n]
        try:
            result[n] = o["fn"](ctx)
        except NotImplementedError as e:
            result[n] = {"status": "not implemented", "note": str(e)}
    rp = research_prompt(result)
    if rp:
        result["research_prompt"] = rp
    return result


# Output styles: "glyph" (default), "plain" (no pictographic glyphs; CJK kept),
# "ascii" (7-bit only: CJK replaced by English/pinyin, accents stripped).
ASCII_MAP = {"·": "|", "—": "-", "–": "-", "’": "'", "‘": "'", "…": "...", "→": "->",
             "°": " deg", "×": "x", "½": "1/2"}
CARDINAL_GLYPH = {"坎": "☵", "震": "☳", "離": "☲", "兌": "☱"}
CARDINAL_PINYIN = {"坎": "Kan", "震": "Zhen", "離": "Li", "兌": "Dui"}


def to_ascii(text: str) -> str:
    for k, v in ASCII_MAP.items():
        text = text.replace(k, v)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return "\n".join(" ".join(line.split()) if line.strip() else "" for line in text.split("\n"))


class Style:
    def __init__(self, style="glyph"):
        self.style = style
        self.glyph = style == "glyph"
        self.cjk = style != "ascii"

    def g(self, *syms):
        """Glyph(s) followed by a space, or nothing in plain/ascii mode."""
        return "".join(syms) + " " if self.glyph else ""

    def finish(self, text):
        text = "\n".join(line.rstrip() for line in text.split("\n"))
        return to_ascii(text) if self.style == "ascii" else text


def hexagram_en(kw: int) -> str:
    n = unicodedata.name(chr(0x4DC0 + kw - 1), "?").replace("HEXAGRAM FOR ", "").lower()
    small = {"of", "the", "in", "and", "to"}
    words = n.split()
    return " ".join(w if (w in small and i) else w.capitalize() for i, w in enumerate(words))


SOLAR_TERMS_EN = ["Winter Solstice", "Minor Cold", "Major Cold", "Start of Spring",
                  "Rain Water", "Awakening of Insects", "Spring Equinox", "Clear and Bright",
                  "Grain Rain", "Start of Summer", "Grain Buds", "Grain in Ear",
                  "Summer Solstice", "Minor Heat", "Major Heat", "Start of Autumn",
                  "End of Heat", "White Dew", "Autumn Equinox", "Cold Dew", "Frost's Descent",
                  "Start of Winter", "Minor Snow", "Major Snow"]


def fmt_trump(t, S, of=None, of_glyph=None):
    tail = (f" {of_glyph}" if S.glyph else f" ({of})") if of else ""
    return f"{S.g(t['glyph'])}{t['roman']} {t['title']}{tail}"


def fmt_national(n, S, short=False):
    tag = {"wales": "W", "england": "E"}.get(n["region"], "E&W")
    name = short_saint(n["name"]) if short else n["name"]
    rank = n["rank"].replace("optional memorial", "opt. mem.") if short else n["rank"]
    bits = [rank]
    if n.get("transferred_to"):
        d = dt.date.fromisoformat(n["transferred_to"])
        bits.append(f"→ {d.strftime('%a')} {d.day} {d.strftime('%b')}")
    if n.get("transferred_from"):
        d = dt.date.fromisoformat(n["transferred_from"])
        bits.append(f"from {d.day} {d.strftime('%b')}")
    if n.get("impeded"):
        bits.append(f"impeded: {n['impeded']}")
    return f"{name} ({'; '.join(bits)}) [{tag}]"


def format_text(r, style="glyph") -> str:
    S = Style(style)
    L = [f"NUMOGRAM CALENDAR — {r['date']} {r['time']} {r['tz']} ({r['tz_abbrev']}) "
         f"= {r['utc']} UTC"]
    if "nma" in r:
        n = r["nma"]
        L.append(f"─── Nma zygotriadic  (epoch {n['epoch']}) ───")
        if "index" in n:
            a = n["taixuan_address"]
            L.append(f"  Cycle {n['cycle']} day {n['day_of_cycle']}/729 · trits {n['trits']} · "
                     f"zone {n['zone']} [spec]")
            L.append(f"  Tetragram address {S.g(a['glyph'])}{a['head']} {a['name']} · "
                     f"appraisal {a['appraisal']} [spec]")
        else:
            L.append(f"  Intercalary day {n['intercalary_day']}/3 (no 6-trit address)")
        L.append(f"  epoch: {n['epoch_note']}")
    if "taixuan" in r:
        t = r["taixuan"]
        L.append(f"─── Tai Xuan  (solstice {t['solstice_utc']} UTC) ───")
        if "head" in t:
            app = t["appraisal_name"] if S.cjk else f"appraisal {t['appraisal']}"
            half = t["half"] if S.cjk else t["half"].split()[1]
            L.append(f"  Head {S.g(t['glyph'])}{t['head']} {t['name']} (lines {t['lines']}) · "
                     f"{app} · {half} · {fmt_zones(t)} [spec]")
        else:
            L.append(f"  {t['extra']} — {t['note']}")
        L.append(f"  day {t['day_since_solstice']} since solstice [approx]")
    if "guaqi" in r:
        g = r["guaqi"]
        L.append("─── Gua qi  (Meng Xi 六日七分) ───" if S.cjk else "─── Gua qi (Meng Xi) ───")
        hz = f"{g['hexagram']} " if S.cjk else ""
        L.append(f"  {S.g(g['glyph'])}{hz}{g['hexagram_en']} (KW {g['king_wen']}) #{g['position']}/60 · "
                 f"{g['rank'] if S.cjk else g['rank'].split()[1]} · day {g['day_in_hexagram']} of 6.09 · "
                 f"{fmt_zones(g)}")
        st = f"{g['solar_term']} {g['solar_term_en']}" if S.cjk else g["solar_term_en"]
        card = g["cardinal"] if S.cjk else CARDINAL_PINYIN[g["cardinal"]]
        L.append(f"  Solar term {st} → {S.g(CARDINAL_GLYPH[g['cardinal']])}{card} line "
                 f"{g['cardinal_line']} [approx]")
    if "decan" in r:
        d = r["decan"]
        L.append(f"─── Decan  ({S.g('☉')}λ = {d['sun_longitude']}°) ───")
        L.append(f"  {S.g(d['sign_glyph'])}{d['sign']} {d['decan_in_sign']} (decan {d['decan']}/36) · "
                 f"{S.g(d['element_glyph'])}{d['element']} · ruler {S.g(d['ruler_glyph'])}{d['ruler']} · "
                 f"{S.g(d['card_glyph'])}{d['card']} · zone {d['zone']} [spec]")
        L.append(f"  Majors: sign {fmt_trump(d['sign_trump'], S)} · ruler "
                 f"{fmt_trump(d['ruler_trump'], S)}  [{d['trump_convention']}]")
        c = d["court"]
        L.append(f"  Court: {S.g(c['glyph'])}{c['card']} ({c['span']}) [Book T]")
    if "pata" in r:
        p = r["pata"]
        L.append("─── 'Pataphysical ───")
        L.append(f"  {p['text']}")
    if "pata_saints" in r:
        q = r["pata_saints"]
        L.append("─── 'Pataphysical feast ───")
        L.append(f"  {q.get('name', '—')}" + (f" ({q['rank_label']})" if q.get("rank_label") else ""))
    if "saints" in r:
        sa = r["saints"]
        L.append(f"─── Catholic calendar: {sa['region_label']}  (Easter {sa['easter']}) ───")
        if sa.get("day_name"):
            L.append(f"  {sa['day_name']}")
        for n in sa.get("national", []):
            L.append(f"  {S.g('✠')}{fmt_national(n, S)}")
        for c in sa["celebrations"] or ([] if sa.get("national") else [{"name": "— (feria)", "rank": ""}]):
            extra = f" (from {c['transferred_from']})" if c.get("transferred_from") else ""
            L.append(f"  {c['name']}" + (f" — {c['rank']}" if c["rank"] else "") + extra)
    if "folk" in r:
        L.append("─── Folk / popular (unofficial) ───")
        for c in r["folk"]["observances"] or [{"name": "—"}]:
            L.append(f"  {c['name']}" + (f" [{c['region']}]" if c.get("region") else ""))
    if "lunation" in r:
        L.append("─── Lunation ───")
        L.append(f"  {r['lunation']['note']}")
    if r.get("research_prompt"):
        L.append("─── Research prompt (generated, not a claim) ───")
        L.append(f"  {S.g('⁂')}{r['research_prompt']['text']}")
    return S.finish("\n".join(L))


def format_daily(r, style="glyph") -> str:
    """Compact reading for a morning message."""
    S = Style(style)
    d = dt.date.fromisoformat(r["date"])
    reg = REGION_LABEL.get(r.get("region", DEFAULT_REGION), "")
    L = [f"{S.g('∴')}{d.strftime('%A')} {d.day} {d.strftime('%B %Y')} · {r['tz_abbrev']} · {reg}"]
    if "decan" in r:
        x = r["decan"]
        L.append(f"{S.g('☉', x['sign_glyph'])}{x['sign']} {x['decan_in_sign']} {x['degree_in_sign']:.0f}° · "
                 f"{S.g(x['ruler_glyph'])}{x['ruler']} · {S.g(x['element_glyph'])}{x['element']} · "
                 f"{S.g(x['card_glyph'])}{x['card']} · zone {x['zone']}")
        st, rt, c = x["sign_trump"], x["ruler_trump"], x["court"]
        swap = ""
        if st["number"] in (8, 11):
            alt = TRUMP_SWAP[st["number"]]
            swap = f" ({'trad.' if x['trump_convention'] == 'gd' else 'GD'} {ROMAN_NUM[alt]})"
        L.append(f"  {fmt_trump(st, S, x['sign'], x['sign_glyph'])}{swap} · "
                 f"{fmt_trump(rt, S, x['ruler'], x['ruler_glyph'])} · "
                 f"{S.g(c['glyph'])}{c['card']} {c['span_glyph'] if S.glyph else '(' + c['span'] + ')'}")
    if "nma" in r:
        x = r["nma"]
        if "index" in x:
            a = x["taixuan_address"]
            L.append(f"Nma {x['cycle']}-{x['day_of_cycle']} {x['trits']} · zone {x['zone']} · "
                     f"{S.g(a['glyph'])}{a['name']} /{a['appraisal']}")
        else:
            L.append(f"Nma intercalary day {x['intercalary_day']}/3")
    if "taixuan" in r:
        x = r["taixuan"]
        if "head" in x:
            app = x["appraisal_name"] if S.cjk else f"/{x['appraisal']}"
            L.append(f"Tai Xuan {S.g(x['glyph'])}{x['head']} {x['name']} · {app} · {fmt_zones(x)}")
        else:
            L.append(f"Tai Xuan {x['extra']}")
    if "guaqi" in r:
        x = r["guaqi"]
        hz = f"{x['hexagram']} " if S.cjk else ""
        term = x["solar_term"] if S.cjk else x["solar_term_en"]
        card = x["cardinal"] if S.cjk else CARDINAL_PINYIN[x["cardinal"]]
        L.append(f"Gua qi {S.g(x['glyph'])}{hz}{x['hexagram_en']} (KW {x['king_wen']}) · {term} · "
                 f"{S.g(CARDINAL_GLYPH[x['cardinal']])}{card} {x['cardinal_line']} · "
                 f"{fmt_zones(x)}")
    if "saints" in r:
        sa = r["saints"]
        parts = [fmt_national(n, S, short=True) for n in sa.get("national", [])]
        parts += [f"{short_saint(c['name']) if 'Proper of Time' not in c['rank'] else c['name']}"
                  f" ({c['rank'].replace('optional memorial', 'opt. mem.')})"
                  for c in sa["celebrations"]]
        head = f"{sa['day_name']} · " if sa.get("day_name") else ""
        L.append(f"{S.g('✠')}{head}" + ("; ".join(parts) if parts else "feria"))
    if "pata" in r:
        name = r.get("pata_saints", {}).get("name")
        L.append(f"{S.g('⛤')}'Pata: {r['pata']['text']}" + (f" · {name}" if name else ""))
    if "folk" in r and r["folk"]["observances"]:
        L.append(f"{S.g('☘')}Folk: " + "; ".join(c["name"] for c in r["folk"]["observances"]))
    if r.get("research_prompt"):
        L.append(f"{S.g('⁂')}Prompt: {r['research_prompt']['text']}")
    return S.finish("\n".join(L))


def list_overlays() -> str:
    L = ["Overlays:"]
    for n, o in OVERLAYS.items():
        L.append(f"  {o['flag']:<14} {o['help']}" + ("" if o["enabled"] else "  (stub)"))
    L.append("Ephemeris providers: " + ", ".join(
        f"{b}{'' if b == 'sun' else ' (stub)'}" for b in PROVIDERS))
    return "\n".join(L)


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)

    def opt(name, default=None):
        if name in args:
            i = args.index(name)
            if i + 1 >= len(args):
                raise SystemExit(f"{name} needs a value")
            return args[i + 1]
        return default

    if "--help" in args or "-h" in args:
        print(__doc__)
        return 0
    if "--list" in args:
        print(list_overlays())
        return 0
    chosen = [n for n, o in OVERLAYS.items() if o["flag"] in args]
    if "--all" in args or "--daily" in args or not chosen:
        chosen = [n for n, o in OVERLAYS.items() if o["enabled"]]
    region = opt("--region", DEFAULT_REGION)
    if region not in REGIONS:
        raise SystemExit(f"--region must be one of: {', '.join(REGIONS)}")
    trumps = opt("--trumps", "gd")
    if trumps not in TRUMP_CONVENTIONS:
        raise SystemExit("--trumps must be gd or trad")
    style = "ascii" if "--ascii" in args else "plain" if "--plain" in args else "glyph"
    options = {"nma_epoch": opt("--nma-epoch", NMA_DEFAULT_EPOCH), "region": region,
               "trumps": trumps}
    ctx = build_context(opt("--date"), opt("--time"), opt("--tz", DEFAULT_TZ), options)
    r = run(ctx, chosen)
    if "--json" in args:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    elif "--daily" in args:
        print(format_daily(r, style))
    else:
        print(format_text(r, style))
    return 0


if __name__ == "__main__":
    sys.exit(main())
