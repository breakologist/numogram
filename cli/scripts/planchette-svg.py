#!/usr/bin/env python3
"""
Tier 2c — Planchette SVG Renderer  (gold/indigo card)
Generates a planchette card from oracle --planchette output.

Usage:
  python3 planchette-svg.py --zone N --current N --gate N --syzygy a::b --aq N --svg
  oracle.py --seed ... --planchette --json | python3 planchette-svg.py --stdin
"""

import argparse, base64, json, math, os, sys, textwrap
from pathlib import Path

# ─── CONSTANTS ──────────────────────────────────────────────────

ZONE_DATA = {
    0: {"name": "eiaoung",  "region": "Void",        "polarity": "−",
        "current": "Plex",   "reading": "The void before the word."},
    1: {"name": "gl",       "region": "Surge",      "polarity": "+",
        "current": "Sink",  "reading": "Original Subtraction."},
    2: {"name": "dt",       "region": "Separation", "polarity": "−",
        "current": "Hold",  "reading": "Extreme Regression."},
    3: {"name": "zx",       "region": "Release",    "polarity": "+",
        "current": "Warp",  "reading": "Abysmal Comprehension."},
    4: {"name": "skr",      "region": "Gate",       "polarity": "−",
        "current": "Sink",  "reading": "Primordial Breath."},
    5: {"name": "ktt",      "region": "Pressure",   "polarity": "+",
        "current": "Hold",  "reading": "Slipping Backwards."},
    6: {"name": "tch",      "region": "Abstraction","polarity": "−",
        "current": "Warp",  "reading": "Attaining Balance."},
    7: {"name": "bsigh",    "region": "Blood",      "polarity": "+",
        "current": "Rise",  "reading": "Progressive Levitation."},
    8: {"name": "mn",       "region": "Multiplicity","polarity": "−",
        "current": "Rise",  "reading": "Eternal Digression."},
    9: {"name": "tn",       "region": "Plex",       "polarity": "+",
        "current": "Plex",  "reading": "Sudden Flight."},
}

TARGET_CARRIER = {
    0: "Uttunul", 1: "Murrumur", 2: "Oddubb",
    3: "Djynxx",  4: "Katak",    5: "Katak",
    6: "Djynxx",  7: "Oddubb",   8: "Murrumur", 9: "Uttunul",
}

ZONE_COLORS = {
    0: "#94a3b8", 1: "#fbbf24", 2: "#34d399", 3: "#e879f9",
    4: "#00ffff", 5: "#f97316", 6: "#60a5fa", 7: "#fb7185",
    8: "#c084fc", 9: "#a855f7",
}

GOLD   = "#fbbf24"
INDIGO = "#6366f1"
CYAN   = "#22d3ee"
WHITE  = "#f8fafc"
MUTED  = "#94a3b8"
BLACK  = "#0f172a"


# ─── PALETTE LOADING ──────────────────────────────────────────────────
# Hardware-accurate palettes from the Hermes pixel-art skill
# Inserts palette colors and zone maps into the medallion pixel grid
try:
    import importlib.util, pathlib
    _PAL_PATH = pathlib.Path.home() / '/home/etym/.hermes/skills/creative/pixel-art/scripts/palettes.py'
    if _PAL_PATH.exists():
        _spec  = importlib.util.spec_from_file_location("palettes", str(_PAL_PATH))
        _mod   = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        _HWPALETTES = _mod.PALETTES
    else:
        raise FileNotFoundError
except Exception:
    _HWPALETTES = {}

ZONE_HW_PALETTE = {
     0: "MONO_AMBER",
     1: "GAMEBOY_ORIGINAL",
     2: "GAMEBOY_POCKET",
     3: "C64",
     4: "ZX_SPECTRUM",
     5: "APPLE_II_HI",
     6: "TELETEXT",
     7: "GAMEBOY_VIRTUALBOY",
     8: "APPLE_II_LO",
     9: "PICO_8",
}

def _pixel_color(zone, x, y, for_svg=False):
    pal_name = ZONE_HW_PALETTE.get(zone, "C64")
    colors = _HWPALETTES.get(pal_name)
    if colors is None:
        sys.stderr.write(f"[PALETTE-FALLBACK] {pal_name} not in HWPALETTES\n")
        colors = _hw_palette(pal_name)
    n   = max(1, len(colors))
    idx = (x * (zone+1) + y * (zone+2)) % n
    r, g, b = colors[idx]  # pick colour for this pixel position
    if for_svg:
        return f"#{r:02x}{g:02x}{b:02x}"
    return (r, g, b, 255)

def _hw_palette(name):
    _SYNTH = {
        "MONO_AMBER":          [(122,87,0),(187,136,0)],
        "GAMEBOY_ORIGINAL":    [(0,35,0),(69,112,14)],
        "GAMEBOY_POCKET":    [(0, 0,  0),(85,85,85)],
        "C64":      [(0,0,0),(124,124,124),(0,0,252),(148,0,132)],
        "ZX_SPECTRUM":    [(0,0,0),(0,40,248),(255,36,20),(255,255,255)],
        "APPLE_II_HI":    [(0,0,0),(255,0,0),(0,255,0),(255,255,255),(0,175,255)],
        "TELETEXT":    [(0,0,0),(255,0,0),(255,255,0),(0,255,0)],
        "GAMEBOY_VIRTUALBOY":[(200,0,0),(164,0,0),(85,0,0),(0,0,0)],
        "APPLE_II_LO":    [(0,0,0),(234,93,240),(0,104,82),(0,145,80)],
        "PICO_8":    [(0,0,0),(29,43,83),(126,37,83),(171,82,54)],
    }
    return _SYNTH.get(name, [(128,0,128),(0,128,0),(0,0,255),(255,0,0)])

# ─── HELPERS ────────────────────────────────────────────────

def _zc(z: int) -> str: return ZONE_COLORS.get(z, WHITE)

def _arc_path(cx: int, cy: int, r: float, a0: float, a1: float) -> str:
    def _pt(a):
        rad = math.radians(a - 90)
        return cx + r*math.cos(rad), cy + r*math.sin(rad)
    x0, y0 = _pt(a0)
    x1, y1 = _pt(a1)
    mid    = (a0 + a1) / 2
    return f"M {x0:.1f} {y0:.1f} Q {cx+(r*.55)*math.cos(math.radians(mid-90)):.1f} {cy+(r*.55)*math.sin(math.radians(mid-90)):.1f} {x1:.1f} {y1:.1f}"

def _label(x, y, text, fill=WHITE, size=11, weight="500", anchor="middle") -> str:
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}"'
            f' font-weight="{weight}" text-anchor="{anchor}">{text}</text>')

def _bg_rect(x, y, w, h, fill, opacity=1.0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" opacity="{opacity}" rx="3"/>'

def zone_angle(z: int) -> float:
    return float(z) * 36.0   # 0° = top, clockwise, step 36°


# ─── ZONE-GLYPH ────────────────────────────────────────────

def zone_glyph(cx: int, cy: int, r: int, zone: int) -> str:
    zc  = _zc(zone)
    nr  = max(r, 1)
    r7  = int(nr * 0.78)
    r5  = int(nr * 0.53)
    return "\n  ".join([
        f'<circle cx="{cx}" cy="{cy}" r="{nr}" fill="{BLACK}" stroke="{GOLD}" stroke-width="2"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r7}"   fill="none" stroke="{zc}"   stroke-width="1.5" stroke-opacity="0.55"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r5}"   fill="none" stroke="{GOLD}" stroke-width="1"   stroke-opacity="0.3" stroke-dasharray="3,3"/>',
        f'<circle cx="{cx}" cy="{cy}" r="4"       fill="{GOLD}" opacity="0.85"/>',
        f'<text x="{cx}" y="{cy+6}" fill="{WHITE}" font-size="{nr}" font-weight="700" text-anchor="middle">{zone}</text>',
    ])


# ─── PIXEL ART MEDALLION ───────────────────────────────────
# Generates a small (r×r) per-zone pixel-grid SVG encoded as base-64
# — currently a geometric hash; can be swapped for real pixel-art later.

def _pixel_hash(x: int, y: int, zone: int) -> int:
    """Deterministic 0/1 from position + zone — makes a unique per-zone pattern."""
    seed = (zone * 7919) ^ (x * 31) ^ (y * 17)
    return 1 if ((seed * 0x5bd1e995) & 0xffff) > 0x6fff else 0

def pixel_medallion(cx: int, cy: int, size: int, zone: int) -> str:
    """Render a small pixel-art square and return base64-encoded PNG."""
    from io import BytesIO
    try:
        from PIL import Image
    except ImportError:
        # fallback: SVG pattern (no PIL needed)
        return _pixel_svg(cx, cy, size, zone)

    pixel_sz = max(1, size // 10)
    cols = size // pixel_sz
    rows = cols
    img = Image.new("RGBA", (cols, rows), (0, 0, 0, 0))
    px  = img.load()
    for py in range(rows):
        for px_ in range(cols):
            if _pixel_hash(px_, py, zone):
                px[px_, py] = _pixel_color(zone, px_, py)
    buf = BytesIO()
    img.save(buf, "PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return (f'<image x="{cx-size//2}" y="{cy-size//2}" width="{size}" height="{size}"'
            f' xlink:href="data:image/png;base64,{b64}" />')


def _pixel_svg(cx: int, cy: int, size: int, zone: int) -> str:
    """SVG-only pixel pattern — no PIL dependency."""
    sz = max(12, size)
    step = sz // 10
    accent = _pixel_color(zone, xi, yi, for_svg=True)
    parts = [f'<rect x="{cx-sz//2}" y="{cy-sz//2}" width="{sz}" height="{sz}" fill="{BLACK}" rx="2"/>']
    for yi in range(10):
        for xi in range(10):
            if _pixel_hash(xi, yi, zone):
                px = cx - sz//2 + xi*step + 1
                py = cy - sz//2 + yi*step + 1
                parts.append(f'<rect x="{px}" y="{py}" width="{step-2}" height="{step-2}" fill="{accent}" opacity="0.8"/>')
    return "\n  ".join(parts)


# ─── RENDER ─────────────────────────────────────────────────────

def render(
    zone: int, current: int, gate_num: int, syzygy: str, aq_sum: int = 137,
    particle: str = "ktt", word: str = "", reading: str = "", path_str: str = "",
    style: str = "inline"
) -> str:
    zd      = ZONE_DATA.get(zone, {})
    zname   = zd.get("name",    f"Z{zone}")
    region  = zd.get("region",  f"Zone {zone}")
    polarity= zd.get("polarity","+")
    zd_cur  = zd.get("current", str(current))
    carrier = TARGET_CARRIER.get(zone)
    pol_desc= "Process / becoming" if polarity=="+" else "Substance / inertia"

    # ─── hard layout anchors ──────────────────────────────────
    W, H   = 450, 620
    cx_h   = W // 2   # 225
    bar_y  = 12
    TITLE_H= 22

    # bottom-up
    ARC_BOT = H - 35            # 585
    ARC_CY  = ARC_BOT - 65     # 520
    ARC_R   = 65
    VERSE_BOT = ARC_CY - ARC_R - 6  # 449
    VERSE_TOP = VERSE_BOT - 26      # 423

    base_y  = bar_y + TITLE_H + 10   # 44
    FIELD_BOT= base_y + 6 * 20       # 164
    GAP     = VERSE_TOP - FIELD_BOT  # 259

    MED_R   = 60
    MED_CY  = FIELD_BOT + GAP - MED_R - 12   # 352
    GL_R    = 44
    GL_CX   = 134
    GL_CY   = MED_CY - MED_R  - 8 - GL_R    # 240

    fx = 190  # fields right column

    lns: list[str] = []

    # ── SVG root ──────────────────────────────────────────────
    lns += [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">',
            f'<rect width="{W}" height="{H}" fill="#0f172a"/>',
            "<defs>",
'  <linearGradient id="frameG" x1="0" y1="0" x2="0" y2="1">',
'      <stop offset="0%"   stop-color="#fbbf24" stop-opacity="0.65"/>',
'      <stop offset="100%" stop-color="#fbbf24" stop-opacity="0.22"/>',
"  </linearGradient>",
'  <radialGradient id="haloG" cx="60%" cy="30%" r="60%">',
'      <stop offset="0%"   stop-color="#fbbf24" stop-opacity="0.14"/>',
'      <stop offset="100%" stop-color="#fbbf24" stop-opacity="0"/>',
"  </radialGradient>",
"</defs>"]

    # ── card frame ─────────────────────────────────────────────
    lns += [f'<rect x="8"   y="8"   width="{W-16}" height="{H-16}" fill="#131b33" stroke="url(#frameG)" stroke-width="2.2" rx="12"/>',
            f'<rect x="10"  y="10"  width="{W-20}" height="{H-20}" fill="none" stroke="#fbbf24" stroke-width="0.4" stroke-opacity="0.28" rx="11"/>']

    # ── title bar ──────────────────────────────────────────────
    lns += [f'<rect x="14"  y="{bar_y}" width="{W-28}" height="{TITLE_H}" fill="url(#haloG)" rx="4"/>',
            f'<text x="{cx_h}" y="{bar_y+TITLE_H-5}" fill="#fbbf24" font-size="9" font-weight="700" text-anchor="middle">ZONE {zone}  ·  {region}  ·  AQΣ={aq_sum}</text>']

    # ── data fields ────────────────────────────────────────────
    field_rows = [
        (f"Current:",    f"{current}   [{zd_cur}]"),
        (f"Gate:",       f"Gt-{gate_num}   → Z{gate_num}"),
        (f"Syzygy:",     f"{syzygy}" + (f"   ★{carrier}" if carrier else "")),
        (f"Polarity:",   f"{polarity}  —  {pol_desc}"),
        (f"Region:",     region),
        (f"Particle:",   particle.upper()),
    ]
    for i, (lbl, val) in enumerate(field_rows):
        ry = base_y + i * 20
        lns += [f'<text x="{fx}" y="{ry}" fill="#94a3b8" font-size="8" font-weight="400" text-anchor="middle">{lbl}</text>',
                f'<text x="{fx+56}" y="{ry}" fill="#f8fafc" font-size="9" font-weight="600" text-anchor="middle">{val}</text>']

    # ── zone-glyph circle ──────────────────────────────────────
    lns += [zone_glyph(GL_CX, GL_CY, GL_R, zone),
            f'<text x="{GL_CX}" y="{GL_CY+GL_R+13}" fill="#94a3b8" font-size="7.5" font-weight="500" text-anchor="middle">{particle.upper()}</text>']

    # ── pixel-art medallion ────────────────────────────────────
    MCX = 230
    lns += [pixel_medallion(MCX, MED_CY, MED_R*2, zone)] 

    # ── gesture line: glyph → medallion ───────────────────────
    lns += [f'<path d="M {GL_CX} {GL_CY+GL_R+2} Q {(GL_CX+MCX)//2} {GL_CY+GL_R+4+(MED_CY-MED_R-(GL_CY+GL_R+2))//2} {MCX} {MED_CY-MED_R-4}"',
            f' stroke="#e879f9" stroke-width="0.8" stroke-opacity="0.3" fill="none" stroke-dasharray="3,3"/>']

    # ── reading verse ──────────────────────────────────────────
    if reading:
        wrapped = __import__("textwrap").fill(reading, width=28)
        for li, rl in enumerate(wrapped.split("\n")[:2]):
            lns += [f'<text x="{fx}" y="{VERSE_TOP+li*13}" fill="#94a3b8" font-size="7.5" font-weight="400" text-anchor="start">{rl}</text>']

    # ── gate-arc band (bottom) ────────────────────────────────
    za = zone_angle(zone)
    ga = zone_angle(gate_num)
    lns += [f'<circle cx="{cx_h}" cy="{ARC_CY}" r="{ARC_R+5}" fill="none" stroke="#0f172a" stroke-width="5" stroke-opacity="0.9"/>',
            f'<circle cx="{cx_h}" cy="{ARC_CY}" r="{ARC_R}" fill="none" stroke="#334155" stroke-width="1.5" opacity="0.6"/>']

    # zone tick labels around ring
    for zz in range(10):
        ta = math.radians(zz*36.0 - 90.0)
        tx = int(cx_h + (ARC_R-9)*math.cos(ta) + 0.5)
        ty = int(ARC_CY + (ARC_R-9)*math.sin(ta) + 0.5) + 4
        lns += [f'<text x="{tx}" y="{ty}" fill="{_zc(zz)}" font-size="7" font-weight="600" text-anchor="middle">{zz}</text>']

    # zone → gate gold arc
    gx0 = int(cx_h + ARC_R * math.cos(math.radians(za-90)))
    gx1 = int(cx_h + ARC_R * math.cos(math.radians(ga-90)))
    lns += [f'<path d="M {gx0} {ARC_CY} A {ARC_R} {ARC_R} 0 0 1 {gx1} {ARC_CY}" stroke="#fbbf24" stroke-width="2.5" stroke-opacity="0.65" fill="none" stroke-dasharray="6,4"/>',
            f'<line x1="{gx0}" y1="{ARC_CY-7}" x2="{gx0}" y2="{ARC_CY+7}" stroke="{_zc(zone)}" stroke-width="2.5"/>',
            f'<text x="{int(cx_h+(ARC_R+14)*math.cos(math.radians(ga-90))):d}" y="{ARC_CY-10}" fill="#22d3ee" font-size="7.5" font-weight="700" text-anchor="middle">↑ Gt-{gate_num} → Z{gate_num}</text>',
            f'<line x1="{gx1}" y1="{ARC_CY-5}" x2="{gx1}" y2="{ARC_CY+5}" stroke="#22d3ee" stroke-width="2" opacity="0.9"/>']

    lns += ["</svg>"]
    return "\n".join(lns)



def main():
    p = argparse.ArgumentParser()
    p.add_argument("--zone",     type=int, required=False)
    p.add_argument("--current",  type=int, required=False)
    p.add_argument("--gate",     type=int, required=False)
    p.add_argument("--syzygy",   default="")
    p.add_argument("--aq",       type=int, default=137)
    p.add_argument("--particle", default="ktt")
    p.add_argument("--word",     default="")
    p.add_argument("--reading",  default="")
    p.add_argument("--path",     dest="path_str", default="")
    p.add_argument("--style",    choices=["inline","card","full"], default="inline")
    p.add_argument("-o", "--output", help="write SVG file")
    p.add_argument("--stdin", action="store_true",
                   help="read planchette JSON from oracle.py --planchette --json")
    args = p.parse_args()

    if not args.stdin:
        missing = []
        for name in ("zone","current","gate"):
            if getattr(args, name) is None:
                missing.append(name)
        if missing:
            print("planchette-svg: missing --zone --current --gate "
                  "or use --stdin", file=sys.stderr)
            sys.exit(2)

    if args.stdin:
        d = json.load(sys.stdin)
        zone     = d.get("zone",    0)
        current  = d.get("current", abs(zone-(9-zone)))
        gate     = d.get("gate",    0)
        syzygy   = d.get("syzygy",  f"{zone}::{9-zone}")
        aq_sum   = d.get("aq_sum",  d.get("aq", 137))
        particle = d.get("particle",ZONE_DATA.get(zone,{}).get("name", "?"))
        reading  = d.get("reading", ZONE_DATA.get(zone,{}).get("reading",""))
        word     = d.get("word",    ZONE_DATA.get(zone,{}).get("current",""))
        path_s   = d.get("path",    "")
    else:
        zone     = args.zone
        current  = args.current
        gate     = args.gate
        syzygy   = args.syzygy or f"{zone}::{9-zone}"
        aq_sum   = args.aq
        particle = args.particle
        reading  = args.reading
        word     = args.word
        path_s   = args.path_str

    svg = render(zone, current, gate, syzygy, aq_sum, particle, word, reading, path_s, style=args.style)

    if args.output:
        Path(args.output).write_text(svg)
        print(f"planchette-svg: {args.output}", file=sys.stderr)
    else:
        print(svg)


if __name__ == "__main__":
    main()
