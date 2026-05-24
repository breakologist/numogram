#!/usr/bin/env python3
"""
syzygy-card.py — Generate tarot-like SVG cards for each numogram syzygy.

Usage:
    python3 syzygy-card.py 4::5          # → syzygy-4-5.svg in CWD
    python3 syzygy-card.py 1::8 -o /tmp/  # custom output dir

Requires: numogram_geometry from ~/.hermes/skills/numogram-geometry/
Optional:  ~/numogram/docs/wiki/assets/zone-glyphs/zone-N.png embedded in card.
"""

from pathlib import Path
import argparse
import math
import sys


# ── geometry backend ──────────────────────────────────────────────────────────
sys.path.insert(0, str(Path.home() / '.hermes/skills'))
try:
    from numogram_geometry import syzTrianglePoints, quadPath, midpoint
except ImportError:
    # Minimal fallback
    def midpoint(p0, p1):
        return ((p0[0]+p1[0])/2, (p0[1]+p1[1])/2)
    def quadPath(p0, p1, bulge=0.7):
        mx, my = midpoint(p0, p1)
        dx, dy = p1[0]-p0[0], p1[1]-p0[1]
        return f'M {p0[0]:.1f} {p0[1]:.1f} Q {mx-dy*bulge:.1f} {my+dx*bulge:.1f} {p1[0]:.1f} {p1[1]:.1f}'


# ── canonical data ────────────────────────────────────────────────────────────
SYZYGIES = {
    frozenset({4, 5}): {"current": 1, "name": "Sink",      "demon": "Katak"},
    frozenset({3, 6}): {"current": 3, "name": "Warp",      "demon": "Djynxx"},
    frozenset({2, 7}): {"current": 5, "name": "Hold",      "demon": "Oddubb"},
    frozenset({1, 8}): {"current": 7, "name": "Rise",      "demon": "Murrumur"},
    frozenset({0, 9}): {"current": 9, "name": "Plex",      "demon": "Uttunul"},
}

ZONE_DATA = {
    0: {"particle": "eiaoung", "name": "Void",      "color": "#991b1b"},
    1: {"particle": "gl",      "name": "Surge",     "color": "#d97706"},
    2: {"particle": "dt",      "name": "Separation","color": "#ef4444"},
    3: {"particle": "zx",      "name": "Release",   "color": "#16a34a"},
    4: {"particle": "skr",     "name": "Gate",      "color": "#ca8a04"},
    5: {"particle": "ktt",     "name": "Hinge",     "color": "#e11d48"},
    6: {"particle": "tch",     "name": "Traction",  "color": "#2563eb"},
    7: {"particle": "pb",      "name": "Breath",    "color": "#0891b2"},
    8: {"particle": "mnm",     "name": "Lull",      "color": "#c084fc"},
    9: {"particle": "tn",      "name": "Plex",      "color": "#7c3aed"},
}

CURRENT_COLOR = {1: "#fc8181", 3: "#fbbf24", 5: "#a3e635", 7: "#38bdf8", 9: "#a78bfa"}
AQ_LETTER_VALUES = {0:35, 1:10, 2:11, 3:12, 4:13, 5:14, 6:15, 7:16, 8:17, 9:18}


# ── SVG helpers ──────────────────────────────────────────────────────────────
def _svg(tag, attrs, content="", indent=0):
    pad = "  " * indent
    inner = f"\n{pad}  {content}\n{pad}" if content else ""
    parts = " ".join(f'{k.lstrip("_")}="{v}"' for k, v in attrs.items() if v is not None)
    return f'{pad}<{tag} {parts}>{inner}</{tag}>'

def circle(cx, cy, r, fill, stroke="#444", sw=1.5, opacity=1.0):
    return _svg("circle", {"cx":cx,"cy":cy,"r":r,"fill":fill,"stroke":stroke,
                           "stroke-width":sw,"opacity":opacity})

def tx(x, y, txt, size=11, fill="#e2e8f0", anchor="middle", weight="normal",
       opacity=1.0, font="monospace"):
    return _svg("text", {"x":x,"y":y,"font-size":size,"fill":fill,
                         "text-anchor":anchor,"font-family":font,
                         "font-weight":weight,"opacity":opacity}, txt)

def rrect(x, y, w, h, rx=8):
    return (f'M {x+rx} {y}'
            f' L {x+w-rx} {y} Q {x+w} {y} {x+w} {y+rx}'
            f' L {x+w} {y+h-rx} Q {x+w} {y+h} {x+w-rx} {y+h}'
            f' L {x+rx} {y+h} Q {x} {y+h} {x} {y+h-rx}'
            f' L {x} {y+rx} Q {x} {y} {x+rx} {y} Z')


# ── card builder ─────────────────────────────────────────────────────────────
def build_syzygy_card(syzygy_str: str, glyph_dir: Path) -> str:
    """Build the complete SVG string for one syzygy card."""
    pair = frozenset(map(int, syzygy_str.split("::")))
    info  = SYZYGIES[pair]
    za, zb = sorted(pair)
    val_cur  = info["current"]
    zdata_a  = ZONE_DATA[za]
    zdata_b  = ZONE_DATA[zb]

    # ── layout ────────────────────────────────────────────────────────────────
    CW, CH = 360, 520
    P = 18

    BAR_TOP_Y = 68
    BAR_H     = 38
    BAR_HEAD_Y = BAR_TOP_Y + BAR_H // 2    # vertical centre of bar rects
    BAR_NARROW_W = 62                       # bar rect width (< glyph sphere r*2)

    # right zone bar sits slightly higher than left (both under arc) — mirrored
    LEFT_BX  = P + BAR_NARROW_W // 2       # zone-va bar centre x
    RIGHT_BX = CW - P - BAR_NARROW_W // 2  # zone-vb bar centre x
    # both bars at same Y  (card is front-facing, left=lower digit, right=higher digit)
    BAR_Y    = BAR_TOP_Y

    # spoke tops at bar bottoms
    BAR_BOT = BAR_Y + BAR_H

    # glyph spheres sit on a row below bars
    GLYPH_Y_OFF = 60          # below bar bottom
    SPHERE_R    = 30

    GLYPH_A_Y  = BAR_BOT + GLYPH_Y_OFF
    GLYPH_B_Y  = BAR_BOT + GLYPH_Y_OFF       # same row; slight offset below left if desired
    GLYPH_A_X  = P + SPHERE_R + 5            # —a bit leftward of its bar to allow spoke
    GLYPH_B_X  = CW - P - SPHERE_R - 5       # —b ditto mirrored

    # current arc: quads left bar-top → right bar-top
    # even currents arch UP, odd currents arch DOWN (alternation across syzygies)
    sign = -1 if val_cur % 2 == 1 else +1          # down for odd
    arc_ctrl_x = (LEFT_BX + RIGHT_BX) / 2
    arc_ctrl_y = BAR_BOT + sign * 36 + (CW - LEFT_BX - RIGHT_BX) * 0.08   # wider arc = higher control

    # demon block
    DEMON_BOX_Y  = GLYPH_A_Y + SPHERE_R + 22
    AQ_BOX_Y     = DEMON_BOX_Y + 58
    TRAP_TXT_Y   = AQ_BOX_Y   + 48
    SUM_Y        = TRAP_TXT_Y + 28

    AQ_COL  = CURRENT_COLOR[val_cur]

    # gate — canonical: triangular cumulation per gate.md
    # C(z) = z×(z−1)//2  (T_{z−1})  sequence: 0,1,3,6,10,15,21,28,36,45 for zones 0–9
    lower_z    = min(za, zb)
    gate_tri   = lower_z * (lower_z - 1) // 2 if lower_z > 0 else 0
    gate_right = gate_tri % 9 if gate_tri % 9 != 0 else 9   # gate → target zone (DR)
    zone_sum   = za + zb
    zone_dr    = zone_sum % 9 if zone_sum % 9 != 0 else 9

    za_aq = AQ_LETTER_VALUES[za]
    zb_aq = AQ_LETTER_VALUES[zb]
    aq_sum = za_aq + zb_aq
    aq_dr  = aq_sum % 9 if aq_sum % 9 != 0 else 9

    le_from_aq = chr(64 + za) if za > 0 else "ℤ"   # zone 0 → ZERO
    le_from_bq = chr(64 + zb) if zb > 0 else "ℤ"

    # ── assemble SVG ───────────────────────────────────────────────────────────
    items = []

    items.append(f'<svg xmlns="http://www.w3.org/2000/svg" '
                 f'viewBox="0 0 {CW} {CH}" width="{CW}" height="{CH}" '
                 f'role="img" aria-label="Syzygy {za}::{zb} '
                 f'{info["name"]} {val_cur} current">')

    # defs
    items.append("<defs>")
    items.append(f'<path id="cardBg" d="{rrect(0,0,CW,CH,14)}"/>')
    for c in CURRENT_COLOR.values():
        items.append(f'<linearGradient id="band{c[1:].lower()}" x1="0%" y1="0%" x2="100%" y2="0%">'
                     f'  <stop offset="0%"   stop-color="{c}" stop-opacity="0.15"/>'
                     f'  <stop offset="50%"  stop-color="{c}" stop-opacity="0.45"/>'
                     f'  <stop offset="100%" stop-color="{c}" stop-opacity="0.15"/>'
                     f'</linearGradient>')
    items.append('<radialGradient id="cardBack" cx="50%" cy="45%" r="65%">'
                 f'  <stop offset="0%" stop-color="#1e293b"/>'
                 f'  <stop offset="100%" stop-color="#0f172a"/>'
                 f'</radialGradient>')
    for ci, cv in CURRENT_COLOR.items():
        items.append(f'<marker id="arrow{ci}" markerWidth="10" markerHeight="6" refX="8" refY="3" orient="auto">'
                     f'  <polygon points="0,0 10,3 0,6" fill="{cv}"/>'
                     f'</marker>')
    items.append("</defs>")

    # card background
    items.append(_svg("path", {"d":rrect(0,0,CW,CH,14),
                                "fill":"url(#cardBack)","stroke":"#1e293b","stroke-width":"1.5"}))

    # ── zone bars ──────────────────────────────────────────────────────────────
    items.append(_svg("rect", {"x":P,"y":BAR_Y,"width":BAR_NARROW_W,"height":BAR_H,
                                "rx":7,"fill":zdata_a["color"],"opacity":"0.9"}))
    items.append(_svg("rect", {"x":CW-P-BAR_NARROW_W,"y":BAR_Y,"width":BAR_NARROW_W,"height":BAR_H,
                                "rx":7,"fill":zdata_b["color"],"opacity":"0.9"}))

    # zone labels on bars
    llabel = f"Zone {za} — {zdata_a['name']}"
    rlabel = f"Zone {zb} — {zdata_b['name']}"
    items.append(tx(LEFT_BX,   BAR_Y+13, llabel,  size=10, fill="white", weight="bold"))
    items.append(tx(RIGHT_BX,  BAR_Y+21, rlabel,  size=10, fill="white", anchor="end", weight="bold"))

    items.append(tx(LEFT_BX,  BAR_Y+25, f"[{zdata_a['particle']}]",  size=8, fill="#94a3b8"))
    items.append(tx(RIGHT_BX, BAR_Y+33, f"[{zdata_b['particle']}]",  size=8, fill="#94a3b8", anchor="end"))

    # ── syzygy header ──────────────────────────────────────────────────────────
    items.append(tx(CW//2, 22, f"{za} :: {zb}",          size=17, fill="#e2e8f0", weight="bold"))
    items.append(tx(CW//2, 40, f"{info['name']} — {val_cur} current",
                    size=11, fill="#94a3b8"))
    items.append(tx(CW//2, 53, f"Demon · {info['demon']}",  size=9,  fill="#64748b"))

    # ── current arc ────────────────────────────────────────────────────────────
    p0 = (LEFT_BX,  BAR_BOT)
    p1 = (RIGHT_BX, BAR_BOT)
    # Bézier arc (midpoint displaced up/down by sign)
    mx,  my  = midpoint(p0, p1)
    shift  = 28 if val_cur % 2 == 0 else -28
    ctrl_x  = mx
    ctrl_y  = my + shift

    # thick band
    for d in [-12, 0, 12]:
        py = p0[1] + d
        qy = p1[1] + d
        body  = f'M {p0[0]:.0f} {py:.0f} Q {ctrl_x:.0f} {ctrl_y:.0f} {p1[0]:.0f} {qy:.0f}'
        items.append(_svg("path",
                          {"d":body, "stroke":AQ_COL, "stroke-width":"12",
                           "fill":"none", "stroke-opacity":"0.12",
                           "marker-end":f"url(#arrow{val_cur})"}))
    # foreground line
    body = f'M {p0[0]:.0f} {p0[1]:.0f} Q {ctrl_x:.0f} {ctrl_y:.0f} {p1[0]:.0f} {p1[1]:.0f}'
    items.append(_svg("path",
                      {"d":body, "stroke":AQ_COL, "stroke-width":"3.5",
                       "fill":"none", "stroke-opacity":"0.9",
                       "marker-end":f"url(#arrow{val_cur})"}))

    # current value label (above arc for even, below for odd)
    lbl_x = mx + (-16 if val_cur % 2 == 1 else 16)
    lbl_y = (ctrl_y + my) / 2 + (6 if val_cur % 2 == 0 else -14)
    items.append(tx(lbl_x, lbl_y, str(val_cur), size=22, fill=AQ_COL, weight="bold"))
    items.append(tx(CW//2, lbl_y + 17, f"{val_cur} current · {info['name']}",
                    size=9, fill="#64748b"))

    # ── glyph spheres ───────────────────────────────────────────────────────────
    for gx, gy, zn in [(GLYPH_A_X, GLYPH_A_Y, za), (GLYPH_B_X, GLYPH_B_Y, zb)]:
        zc = zdata_a["color"] if zn==za else zdata_b["color"]
        items.append(circle(gx, gy, SPHERE_R, "#162032", stroke=zc, sw=2.5))
        png = glyph_dir / f"zone-{zn}.png"
        if png.exists():
            import base64
            with open(png, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            items.append(f'<image x="{gx-SPHERE_R-2}" y="{gy-SPHERE_R-2}" '
                         f'width="{SPHERE_R*2+4}" height="{SPHERE_R*2+4}" '
                         f'xlink:href="data:image/png;base64,{b64}"/>')
        else:
            items.append(tx(gx, gy+5, str(zn), size=22, fill=zc, weight="bold"))

    # spoke lines from bar bottoms to glyph sphere tops
    bar_spoke_left  = (LEFT_BX,  BAR_BOT)
    bar_spoke_right = (RIGHT_BX, BAR_BOT)
    spkl_top  = (GLYPH_A_X, GLYPH_A_Y - SPHERE_R)
    spkr_top  = (GLYPH_B_X, GLYPH_B_Y - SPHERE_R)
    items.append(f'<line x1="{bar_spoke_left[0]}" y1="{bar_spoke_left[1]}" '
                 f'x2="{spkl_top[0]}" y2="{spkl_top[1]}" '
                 f'stroke="#334155" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>')
    items.append(f'<line x1="{bar_spoke_right[0]}" y1="{bar_spoke_right[1]}" '
                 f'x2="{spkr_top[0]}" y2="{spkr_top[1]}" '
                 f'stroke="#334155" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>')

    # bar cross-satorial confirm
    items.append(f'<line x1="{LEFT_BX}" y1="{BAR_TOP_Y + BAR_H//2}" '
                 f'x2="{RIGHT_BX}" y2="{BAR_Y + BAR_H//2}" '
                 f'stroke="#334155" stroke-width="1" stroke-dasharray="2 5" opacity="0.4"/>')

    # ── carrier demon block ─────────────────────────────────────────────────────
    dem_area_x = CW//2 - 150
    dem_area_y = DEMON_BOX_Y - 10
    items.append(_svg("rect", {"x":dem_area_x,"y":dem_area_y,
                                "width":"300","height":"50","rx":"7",
                                "fill":"#162032","stroke":"#334155","stroke-width":"1"}))
    items.append(tx(CW//2, dem_area_y+14, "Carrier Demon", size=9, fill="#64748b"))
    items.append(tx(CW//2, dem_area_y+34, info["demon"],       size=15, fill="#e2e8f0", weight="bold"))

    # Gate info
    demon_gate = gate_str = f"Gt-{gate_tri:03d} → Z{gate_right}"
    items.append(tx(CW//2, dem_area_y+34+20, demon_gate, size=9, fill="#94a3b8"))

    # ── AQ gematria strip ───────────────────────────────────────────────────────
    items.append(_svg("rect", {"x":P,"y":AQ_BOX_Y,"width":CW-2*P,"height":"36","rx":"6",
                                "fill":"#162032","stroke":"#334155","stroke-width":"1"}))
    items.append(tx(CW//2, AQ_BOX_Y+14,
                    f"  {le_from_aq}={za_aq}  ⊕  {le_from_bq}={zb_aq}  ·  AQΣ={aq_sum}  DR={aq_dr}",
                    size=10, fill="#94a3b8"))

    # ── Δ─────Δ trapezoid pin ───────────────────────────────────────────────────
    pin_y = TRAP_TXT_Y - 8
    items.append(tx(CW//2, pin_y, "Δ─────────Δ", size=13, fill="#8899aacc", opacity="0.80"))

    # _AT / _SU (zone_a and zone_b gating info)
    AT_X  = CW//2 - 80
    SU_X  = CW//2 + 80
    W  = 40
    for (px, lbl, col) in [(AT_X, "AT", zdata_a["color"]), (SU_X, "SU", zdata_b["color"])]:
        items.append(_svg("rect", {"x":px-W,"y":pin_y+4,"width":W*2,"height":"13","rx":"3",
                                    "fill":"#162032","stroke":col,"stroke-width":"1.2"}))
        items.append(tx(px, pin_y+4+9, lbl, size=9, fill="#64748b"))

    items.append(tx(CW//2, SUM_Y + 8,
                    f"≡  {za}{zb}  ≡  {zone_sum}  ≡  {zone_dr}  ≡",
                    size=9, fill="#64748b"))
    items.append(tx(CW//2, SUM_Y + 22,
                    f"  {val_cur}current · {'Z'+str(val_cur) if val_cur < 9 else 'Zplex'} · "
                    f"{gate_str}",
                    size=11, fill=AQ_COL, weight="bold"))

    # ── corner zone seed glyphs ─────────────────────────────────────────────────
    for (cx, cy, lab) in [(22, 22, str(za)), (CW-22, 22, str(zb)),
                           (22, CH-22, str(val_cur)), (CW-22, CH-22, str(val_cur))]:
        items.append(tx(cx, cy, lab, size=9, fill="#1e293b", opacity="0.55",
                        anchor="middle", weight="bold"))

    items.append("</svg>")
    return "\n".join(items)


# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="Generate a numogram syzygy card SVG")
    ap.add_argument("syzygy", help="Syzygy pair (e.g. 4::5, 0::9)")
    ap.add_argument("-o", "--output-dir", default=".", help="Output directory")
    ap.add_argument("--glyphs", default="~/numogram/docs/wiki/assets/zone-glyphs",
                    help="Directory with zone-{N}.png glyph files")
    args = ap.parse_args()

    pair = frozenset(map(int, args.syzygy.split("::")))
    if pair not in SYZYGIES:
        sys.exit(f"Error: {args.syzygy} is not a canonical syzygy."
                 f"\n  Canonical pairs: "
                 f"{sorted('::'.join(map(str,sorted(p))) for p in SYZYGIES)}")

    za, zb = sorted(pair)
    out = Path(args.output_dir) / f"syzygy-{za}-{zb}.svg"
    svg = build_syzygy_card(args.syzygy, Path(args.glyphs).expanduser())
    out.write_text(svg)
    print(f"✓  {out}  ({len(svg):,} bytes)")


if __name__ == "__main__":
    main()
