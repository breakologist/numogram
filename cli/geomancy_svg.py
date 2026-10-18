#!/usr/bin/env python3
"""geomancy_svg.py — draw a geomancy.py reading as an SVG shield laid out like the user's blank
template: eight top cells (Mothers and Daughters, read right to left Vita … Mors), four Nieces
(Iter … Carcer, right to left), Left and Right Witness, and the Judge in the point of the shield.

Each Mother/Daughter/Niece cell has the element triangle of its line (Fire, Air, Water, Earth, as
in the template), a small box with the planet glyph, a 3×4 grid with the figure's points (one point
= middle cell, two points = outer cells), a box with the house number, the figure name and the
Latin label. Stdlib only; `shield_svg(data)` returns the SVG text. PNG: rsvg-convert in.svg -o out.png
"""
import sys
from typing import Any, Dict, List
from xml.sax.saxutils import escape

import geomancy as G

W, H = 800, 1010
X0, X1, Y0, YMID, YLOW = 57, 726, 30, 340, 657


def _tri(cx: float, cy: float, element: str, s: float = 9) -> str:
    up = element in ("fire", "air")
    pts = [(cx - s, cy + s * 0.8), (cx + s, cy + s * 0.8), (cx, cy - s * 0.9)] if up else \
          [(cx - s, cy - s * 0.8), (cx + s, cy - s * 0.8), (cx, cy + s * 0.9)]
    out = '<polygon points="%s" fill="none" stroke="#000" stroke-width="1.5"/>' % " ".join(
        f"{x:.1f},{y:.1f}" for x, y in pts)
    if element in ("air", "earth"):
        y = cy + (s * 0.15 if up else -s * 0.15)
        out += f'<line x1="{cx - s * 0.75:.1f}" y1="{y:.1f}" x2="{cx + s * 0.75:.1f}" y2="{y:.1f}" stroke="#000" stroke-width="1.5"/>'
    return out


def _box(x: float, y: float, s: float, text: str = "", size: int = 13) -> str:
    out = f'<rect x="{x:.1f}" y="{y:.1f}" width="{s}" height="{s}" fill="none" stroke="#000"/>'
    if text:
        out += (f'<text x="{x + s / 2:.1f}" y="{y + s / 2 + size * 0.36:.1f}" font-size="{size}" '
                f'text-anchor="middle">{escape(text)}</text>')
    return out


def _grid(x: float, y: float, cw: float, rh: float, bits: List[int]) -> str:
    out = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{3 * cw:.1f}" height="{4 * rh:.1f}" fill="none" stroke="#000"/>']
    for i in (1, 2):
        out.append(f'<line x1="{x + i * cw:.1f}" y1="{y:.1f}" x2="{x + i * cw:.1f}" y2="{y + 4 * rh:.1f}" stroke="#000"/>')
    for r in (1, 2, 3):
        out.append(f'<line x1="{x:.1f}" y1="{y + r * rh:.1f}" x2="{x + 3 * cw:.1f}" y2="{y + r * rh:.1f}" stroke="#000"/>')
    rad = min(cw, rh) * 0.28
    for r, b in enumerate(bits):
        cols = (1,) if b else (0, 2)
        for c in cols:
            out.append(f'<circle cx="{x + (c + 0.5) * cw:.1f}" cy="{y + (r + 0.5) * rh:.1f}" r="{rad:.1f}" fill="#000"/>')
    return "".join(out)


def _text(x: float, y: float, s: str, size: int = 13, weight: str = "normal", style: str = "normal") -> str:
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" font-style="{style}" '
            f'text-anchor="middle">{escape(s)}</text>')


def _cell(x: float, y: float, w: float, pos: str, fig: Dict[str, Any], big: bool) -> str:
    el = G.position_element(pos)
    house = G.POS_HOUSE[pos]
    cw, rh = (21, 36) if not big else (22, 35)
    gx = x + (w - 3 * cw) / 2
    gy = y + (80 if not big else 85)
    out = [_tri(x + (20 if not big else 40), y + 35, el),
           _box(x + w - (34 if not big else 50), y + 25, 20, G.GLYPHS.get(fig["planet"], ""), 13),
           _grid(gx, gy, cw, rh, fig["bits"]),
           _text(x + w / 2, gy + 4 * rh + 13, fig["name"], 9 if not big else 11, style="italic"),
           _box(x + w / 2 - 15, gy + 4 * rh + 20, 30, str(house), 12),
           _text(x + w / 2, y + (297 if not big else 300), G.LATIN_HOUSE[house], 13, "bold")]
    return "".join(out)


def shield_svg(data: Dict[str, Any], title: bool = True) -> str:
    sh = data["shield"]
    f = {k: G.figure(v["name"]) for k, v in sh.items()}
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'font-family="Georgia, \'DejaVu Serif\', serif">',
         f'<rect width="{W}" height="{H}" fill="#fff"/>',
         f'<path d="M{X0},{Y0} H{X1} V{YLOW} A{(X1 - X0) / 2},{(X1 - X0) / 2} 0 0 1 {X0},{YLOW} Z" '
         f'fill="none" stroke="#000" stroke-width="1.5"/>',
         f'<line x1="{X0}" y1="{YMID}" x2="{X1}" y2="{YMID}" stroke="#000"/>',
         f'<line x1="{X0}" y1="{YLOW}" x2="{X1}" y2="{YLOW}" stroke="#000"/>']
    cw8 = (X1 - X0) / 8
    for i, pos in enumerate(["D4", "D3", "D2", "D1", "M4", "M3", "M2", "M1"]):
        x = X0 + i * cw8
        if i:
            o.append(f'<line x1="{x:.1f}" y1="{Y0}" x2="{x:.1f}" y2="{YMID}" stroke="#000"/>')
        o.append(_cell(x, Y0, cw8, pos, f[pos], False))
    cw4 = (X1 - X0) / 4
    for i, pos in enumerate(["N4", "N3", "N2", "N1"]):
        x = X0 + i * cw4
        if i:
            o.append(f'<line x1="{x:.1f}" y1="{YMID}" x2="{x:.1f}" y2="{YLOW}" stroke="#000"/>')
        o.append(_cell(x, YMID, cw4, pos, f[pos], True))
    cx = (X0 + X1) / 2
    o.append(f'<line x1="{cx}" y1="{YLOW}" x2="245" y2="958" stroke="#000"/>')
    o.append(f'<line x1="{cx}" y1="{YLOW}" x2="539" y2="957" stroke="#000"/>')
    for pos, lx, label in (("LW", 222, "Left Witness"), ("RW", 559, "Right Witness")):
        o.append(_text(lx, 685, label, 14, "bold"))
        o.append(_grid(lx - 37, 712, 23, 36, f[pos]["bits"]))
        o.append(_text(lx, 875, f[pos]["name"], 11, style="italic"))
        o.append(_box(lx + 72, 705, 22, G.GLYPHS.get(f[pos]["planet"], ""), 13))
        o.append(_box(lx - 18, 882, 30, "", 12))
    o.append(_grid(cx - 34, 758, 23, 36, f["J"]["bits"]))
    o.append(_text(cx, 913, f["J"]["name"], 11, style="italic"))
    o.append(_box(cx + 50, 846, 22, G.GLYPHS.get(f["J"]["planet"], ""), 13))
    o.append(_box(cx - 16, 918, 30, "", 12))
    o.append(_text(cx, 972, "Judge", 14, "bold"))
    if title:
        cap = f"{data.get('source', '')} · Sentence {data.get('sentence', '')}"
        hl = data.get("halting") or {}
        if hl.get("halted"):
            cap += f" · HALTED ({hl['rule']}: {', '.join(hl['fired'])})"
        o.append(_text(W / 2, 20, cap, 11))
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    args = sys.argv[1:]
    seed = int(args[args.index("--seed") + 1]) if "--seed" in args else 192855
    print(shield_svg(G.cast_geomancy(seed=seed)))
