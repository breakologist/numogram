#!/usr/bin/env python3
"""Generate yantra/mandala SVGs for all 10 numogram zones."""
import math, os, shutil

SIZE = 600
CX = CY = SIZE // 2

# ── Zone palettes ──
# Each zone gets its own colour signature evoking its CCRU character.
PALETTES = {
    0: {"bg": "#0a0a08", "fg": "#FFB000", "dim": "#4a3a10", "glow": "#FFD700",
        "name": "MONO_AMBER",  "label": "VOID",       "particle": "eiaoung"},
    1: {"bg": "#0a0806", "fg": "#CD853F", "dim": "#2a1a08", "glow": "#DAA520",
        "name": "UR_EARTH",   "label": "MURRUMUR",   "particle": "mu"},
    2: {"bg": "#060a0c", "fg": "#1E90FF", "dim": "#0a2030", "glow": "#87CEEB",
        "name": "DEEP_WATER", "label": "TUTTAGOOL",  "particle": "tu"},
    3: {"bg": "#0a0606", "fg": "#FF4500", "dim": "#3a1008", "glow": "#FF6347",
        "name": "KALASUTRA",  "label": "UNNUNDDO",   "particle": "un"},
    4: {"bg": "#080a0a", "fg": "#A0C4E0", "dim": "#203040", "glow": "#C8E0F0",
        "name": "CLEAVING",   "label": "UNUNUTTIX",  "particle": "ix"},
    5: {"bg": "#080808", "fg": "#909090", "dim": "#303030", "glow": "#C0C0C0",
        "name": "SPECTRAL",   "label": "UNNUNAKA",   "particle": "ma"},
    6: {"bg": "#08060a", "fg": "#9370DB", "dim": "#281848", "glow": "#BA55D3",
        "name": "BINDING",    "label": "TUKUTU",     "particle": "ku"},
    7: {"bg": "#0a0608", "fg": "#DC143C", "dim": "#3a0818", "glow": "#FF69B4",
        "name": "SAMSARA",    "label": "UNNUTCHI",   "particle": "chi"},
    8: {"bg": "#080a08", "fg": "#6B8E23", "dim": "#202818", "glow": "#A0C050",
        "name": "EXILE",      "label": "NUTTUBAB",   "particle": "bab"},
    9: {"bg": "#0a080a", "fg": "#9900FF", "dim": "#3a1050", "glow": "#CC66FF",
        "name": "PICO_8",     "label": "IRON CORE",  "particle": "tn"},
}

# ── helpers ──

def svg_header(title, bg):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}" width="{SIZE}" height="{SIZE}">
<rect width="{SIZE}" height="{SIZE}" fill="{bg}"/>
<defs>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="2" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="glow-thick" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="4" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
'''

def footer():
    return '</svg>\n'

def polar(r, theta, cx=CX, cy=CY):
    return cx + r * math.cos(theta), cy + r * math.sin(theta)

def deg(d):
    return d * math.pi / 180

def polygon_str(points):
    return ' '.join(f'{x},{y}' for x, y in points)

# ── Zone 0 — Void ──
# 45° rotated squares (squares-as-diamonds), concentric, amber on black.
def zone0_zantra():
    p = PALETTES[0]
    lines = [svg_header("Zone 0 — Void Yantra", p["bg"])]

    # outer boundary circle — the limit of void
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="260" fill="none" '
                 f'stroke="{p["dim"]}" stroke-width="0.5" opacity="0.3"/>')

    # concentric 45° rotated squares (square → diamond)
    for i, r in enumerate([220, 180, 140, 100, 60]):
        opacity = 0.18 - i * 0.03
        pts = [polar(r, deg(45 + i * 90)) for i in range(4)]
        lines.append(f'<polygon points="{polygon_str(pts)}" fill="none" '
                     f'stroke="{p["fg"]}" stroke-width="{0.5 + i * 0.3}" '
                     f'opacity="{max(0.02, opacity)}"/>')

    # faint upright triangle (positive polarity, barely suggested)
    tri_pts = [polar(100, deg(a)) for a in (90, 210, 330)]
    lines.append(f'<polygon points="{polygon_str(tri_pts)}" fill="none" '
                 f'stroke="{p["dim"]}" stroke-width="0.5" opacity="0.06"/>')

    # bindu — central point with glow
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="8" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="1" opacity="0.5" filter="url(#glow)"/>')
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="2" fill="{p["fg"]}" opacity="0.8"/>')

    # seed syllable ring: e i a o u n g
    seed = list("eiaoung")
    for i, ch in enumerate(seed):
        a = deg(i * (360 / len(seed)) - 90)
        x, y = polar(28, a)
        lines.append(f'<text x="{x}" y="{y}" fill="{p["dim"]}" '
                     f'font-size="8" font-family="monospace" text-anchor="middle" '
                     f'dominant-baseline="central" opacity="0.3">{ch}</text>')

    # metadata
    lines.append(f'<text x="{CX}" y="{SIZE - 30}" fill="{p["dim"]}" '
                 f'font-size="10" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="4" opacity="0.5">ZONE 0 · {p["name"]}</text>')
    lines.append(f'<text x="{CX}" y="30" fill="{p["dim"]}" '
                 f'font-size="9" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="6" opacity="0.3">0000</text>')
    lines.append(footer())
    return ''.join(lines)


# ── Zone 1 — Murrumur (Earth / Urgrund) ──
# Descending triangle anchored in the mud, layered horizontal bands.
def zone1_zantra():
    p = PALETTES[1]
    lines = [svg_header("Zone 1 — Murrumur Yantra", p["bg"])]

    # dense horizontal bands — Urgrund strata
    for i in range(30):
        y = 60 + i * 16
        opacity = 0.12 - i * 0.003
        if opacity <= 0: break
        lines.append(f'<line x1="180" y1="{y}" x2="420" y2="{y}" '
                     f'stroke="{p["fg"]}" stroke-width="{0.3 + i * 0.05}" '
                     f'opacity="{max(0.01, opacity)}"/>')

    # descending triangle — the weight of matter
    for r in [240, 200, 160, 120, 80][::-1]:
        pts = [polar(r, deg(a)) for a in (90, 210, 330)]
        opacity = max(0.04, 0.25 - (240 - r) * 0.002)
        lines.append(f'<polygon points="{polygon_str(pts)}" fill="none" '
                     f'stroke="{p["fg"]}" stroke-width="{1.0 + (240 - r) * 0.003}" '
                     f'opacity="{opacity}"/>')

    # foundation square — the four-cornered earth
    for r in [160, 100]:
        pts = [polar(r, deg(a)) for a in (45, 135, 225, 315)]
        lines.append(f'<polygon points="{polygon_str(pts)}" fill="none" '
                     f'stroke="{p["dim"]}" stroke-width="0.8" opacity="0.1"/>')

    # centre — the mud-seed "mu"
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="10" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="1" opacity="0.3" filter="url(#glow)"/>')
    lines.append(f'<text x="{CX}" y="{CY + 4}" fill="{p["fg"]}" '
                 f'font-size="16" font-family="monospace" text-anchor="middle" '
                 f'font-weight="bold" opacity="0.6">mu</text>')
    # metadata
    lines.append(f'<text x="{CX}" y="{SIZE - 30}" fill="{p["dim"]}" '
                 f'font-size="10" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="4" opacity="0.5">ZONE 1 · {p["name"]}</text>')
    lines.append(f'<text x="{CX}" y="30" fill="{p["dim"]}" '
                 f'font-size="9" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="6" opacity="0.3">0023</text>')
    lines.append(footer())
    return ''.join(lines)


# ── Zone 2 — Tuttagool (Water) ──
# Wavy concentric circles, fluid arcs, hexagram for the water star.
def zone2_zantra():
    p = PALETTES[2]
    lines = [svg_header("Zone 2 — Tuttagool Yantra", p["bg"])]

    # wavy circles — fluid boundaries (modulate radius by sin)
    for i in range(18):
        r_base = 260 - i * 14
        if r_base < 10: break
        pts = []
        for a_deg in range(0, 360, 6):
            a = deg(a_deg)
            r = r_base + 8 * math.sin(6 * a + i * 1.2)
            pts.append(polar(r, a))
        path = ' '.join(f'{x},{y}' for x, y in pts)
        opacity = max(0.02, 0.15 - i * 0.008)
        lines.append(f'<polyline points="{path}" fill="none" '
                     f'stroke="{p["fg"]}" stroke-width="{0.3 + i * 0.04}" '
                     f'opacity="{opacity}"/>')

    # hexagram — the water star (two interlocking triangles)
    up_pts = [polar(140, deg(a)) for a in (90, 330, 210)]
    dn_pts = [polar(140, deg(a)) for a in (30, 270, 150)]
    lines.append(f'<polygon points="{polygon_str(up_pts)}" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="1" opacity="0.2"/>')
    lines.append(f'<polygon points="{polygon_str(dn_pts)}" fill="none" '
                 f'stroke="{p["dim"]}" stroke-width="1" opacity="0.15"/>')

    # centre — fluid seed "tu"
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="8" fill="none" '
                 f'stroke="{p["glow"]}" stroke-width="1" opacity="0.4" filter="url(#glow)"/>')
    lines.append(f'<text x="{CX}" y="{CY + 4}" fill="{p["fg"]}" '
                 f'font-size="14" font-family="monospace" text-anchor="middle" '
                 f'font-weight="bold" opacity="0.7">tu</text>')
    lines.append(f'<text x="{CX}" y="{SIZE - 30}" fill="{p["dim"]}" '
                 f'font-size="10" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="4" opacity="0.5">ZONE 2 · {p["name"]}</text>')
    lines.append(f'<text x="{CX}" y="30" fill="{p["dim"]}" '
                 f'font-size="9" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="6" opacity="0.3">0046</text>')
    lines.append(footer())
    return ''.join(lines)


# ── Zone 3 — Unnunddo (Fire / Kalasutra) ──
# Upward flame triangles, spiral time-weaving.
def zone3_zantra():
    p = PALETTES[3]
    lines = [svg_header("Zone 3 — Unnunddo Yantra", p["bg"])]

    # upward flame triangles
    for i, r in enumerate([250, 210, 170, 130, 90]):
        pts = [polar(r, deg(a)) for a in (90 + i*5, 210 - i*3, 330 - i*5)]
        opacity = max(0.02, 0.2 - i * 0.035)
        lines.append(f'<polygon points="{polygon_str(pts)}" fill="none" '
                     f'stroke="{p["fg"]}" stroke-width="{0.5 + i * 0.4}" '
                     f'opacity="{opacity}"/>')

    # spiral — the kalasutra thread
    spiral_pts = []
    for a_deg in range(0, 1080, 6):
        a = deg(a_deg)
        r = 220 * (1 - a_deg / 1080 * 0.85)
        spiral_pts.append(polar(r, a))
    path = ' '.join(f'{x},{y}' for x, y in spiral_pts)
    lines.append(f'<polyline points="{path}" fill="none" '
                 f'stroke="{p["dim"]}" stroke-width="1" opacity="0.12"/>')

    # centre — fire seed "un"
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="10" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="1" opacity="0.4" filter="url(#glow)"/>')
    lines.append(f'<text x="{CX}" y="{CY + 4}" fill="{p["fg"]}" '
                 f'font-size="16" font-family="monospace" text-anchor="middle" '
                 f'font-weight="bold" opacity="0.7">un</text>')
    lines.append(f'<text x="{CX}" y="{SIZE - 30}" fill="{p["dim"]}" '
                 f'font-size="10" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="4" opacity="0.5">ZONE 3 · {p["name"]}</text>')
    lines.append(f'<text x="{CX}" y="30" fill="{p["dim"]}" '
                 f'font-size="9" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="6" opacity="0.3">0122</text>')
    lines.append(footer())
    return ''.join(lines)


# ── Zone 4 — Ununuttix (Air / Cleaving) ──
# Diamond cross — axes of cleaving, 8-pointed wind star.
def zone4_zantra():
    p = PALETTES[4]
    lines = [svg_header("Zone 4 — Ununuttix Yantra", p["bg"])]

    # 8-pointed star — the winds of cleaving
    star_pts = []
    for i in range(8):
        a = deg(i * 45)
        r = 250 if i % 2 == 0 else 100
        star_pts.append(polar(r, a))
    lines.append(f'<polygon points="{polygon_str(star_pts)}" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="0.8" opacity="0.15"/>')

    # central cross — the cleaving axes
    for angle in (0, 90):
        pts = [polar(240, deg(angle)), polar(240, deg(angle + 180))]
        lines.append(f'<line x1="{pts[0][0]}" y1="{pts[0][1]}" '
                     f'x2="{pts[1][0]}" y2="{pts[1][1]}" '
                     f'stroke="{p["fg"]}" stroke-width="0.8" opacity="0.15"/>')

    # rotated square — the air element form
    for r in [200, 150, 100]:
        pts = [polar(r, deg(a)) for a in (45, 135, 225, 315)]
        lines.append(f'<polygon points="{polygon_str(pts)}" fill="none" '
                     f'stroke="{p["fg"]}" stroke-width="0.6" opacity="{max(0.03, 0.18 - (200 - r) * 0.002)}"/>')

    # centre — air seed "ix"
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="7" fill="none" '
                 f'stroke="{p["glow"]}" stroke-width="1" opacity="0.3" filter="url(#glow)"/>')
    lines.append(f'<text x="{CX}" y="{CY + 4}" fill="{p["fg"]}" '
                 f'font-size="14" font-family="monospace" text-anchor="middle" '
                 f'font-weight="bold" opacity="0.7">ix</text>')
    lines.append(f'<text x="{CX}" y="{SIZE - 30}" fill="{p["dim"]}" '
                 f'font-size="10" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="4" opacity="0.5">ZONE 4 · {p["name"]}</text>')
    lines.append(f'<text x="{CX}" y="30" fill="{p["dim"]}" '
                 f'font-size="9" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="6" opacity="0.3">0161</text>')
    lines.append(footer())
    return ''.join(lines)


# ── Zone 5 — Unnunaka (Makhai / Spectral Strike) ──
# 5-pointed star (the makhai), sharp spectral lines.
def zone5_zantra():
    p = PALETTES[5]
    lines = [svg_header("Zone 5 — Unnunaka Yantra", p["bg"])]

    # 5-pointed star — the spectral makhai
    outer_r, inner_r = 260, 100
    star_pts = []
    for i in range(10):
        a = deg(i * 36 - 90)
        r = outer_r if i % 2 == 0 else inner_r
        star_pts.append(polar(r, a))
    lines.append(f'<polygon points="{polygon_str(star_pts)}" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="1" opacity="0.2"/>')

    # concentric pentagons
    for r in [220, 160, 100]:
        pts = [polar(r, deg(i * 72 - 90)) for i in range(5)]
        lines.append(f'<polygon points="{polygon_str(pts)}" fill="none" '
                     f'stroke="{p["dim"]}" stroke-width="0.5" opacity="0.08"/>')

    # radial strike lines — the makhai thrusts
    for i in range(5):
        a = deg(i * 72 - 90)
        x, y = polar(200, a)
        lines.append(f'<line x1="{CX}" y1="{CY}" x2="{x}" y2="{y}" '
                     f'stroke="{p["fg"]}" stroke-width="0.5" opacity="0.1"/>')

    # centre — spectral seed "ma"
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="8" fill="none" '
                 f'stroke="{p["glow"]}" stroke-width="1" opacity="0.4" filter="url(#glow)"/>')
    lines.append(f'<text x="{CX}" y="{CY + 4}" fill="{p["fg"]}" '
                 f'font-size="16" font-family="monospace" text-anchor="middle" '
                 f'font-weight="bold" opacity="0.7">ma</text>')
    lines.append(f'<text x="{CX}" y="{SIZE - 30}" fill="{p["dim"]}" '
                 f'font-size="10" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="4" opacity="0.5">ZONE 5 · {p["name"]}</text>')
    lines.append(f'<text x="{CX}" y="30" fill="{p["dim"]}" '
                 f'font-size="9" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="6" opacity="0.3">0184</text>')
    lines.append(footer())
    return ''.join(lines)


# ── Zone 6 — Tukutu (Binding / Teleophilic) ──
# Hexagon, interlocking figure-8, binding links.
def zone6_zantra():
    p = PALETTES[6]
    lines = [svg_header("Zone 6 — Tukutu Yantra", p["bg"])]

    # outer hexagon — the binding enclosure
    for r in [260, 220, 180, 140, 100]:
        pts = [polar(r, deg(i * 60 - 30)) for i in range(6)]
        opacity = max(0.02, 0.15 - (260 - r) * 0.001)
        lines.append(f'<polygon points="{polygon_str(pts)}" fill="none" '
                     f'stroke="{p["fg"]}" stroke-width="{0.3 + (260 - r) * 0.005}" '
                     f'opacity="{opacity}"/>')

    # figure-8 — the binding/teleophilic loop (lemniscate)
    lem_pts = []
    for t_deg in range(0, 360, 4):
        t = deg(t_deg)
        r_norm = 160
        x = CX + r_norm * math.sin(t) * math.cos(t)
        y = CY + r_norm * math.sin(t) * (1 + math.cos(t)) * 0.5
        lem_pts.append((x, y))
    lines.append(f'<polyline points="{polygon_str(lem_pts)}" fill="none" '
                 f'stroke="{p["glow"]}" stroke-width="1" opacity="0.15" filter="url(#glow)"/>')

    # linking chains — short arcs between hexagon vertices
    for i in range(6):
        a = deg(i * 60 - 30)
        x1, y1 = polar(90, a)
        x2, y2 = polar(90, deg((i + 1) * 60 - 30))
        lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                     f'stroke="{p["dim"]}" stroke-width="0.5" opacity="0.15"/>')

    # centre — binding seed "ku"
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="9" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="1" opacity="0.4" filter="url(#glow)"/>')
    lines.append(f'<text x="{CX}" y="{CY + 4}" fill="{p["fg"]}" '
                 f'font-size="16" font-family="monospace" text-anchor="middle" '
                 f'font-weight="bold" opacity="0.7">ku</text>')
    lines.append(f'<text x="{CX}" y="{SIZE - 30}" fill="{p["dim"]}" '
                 f'font-size="10" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="4" opacity="0.5">ZONE 6 · {p["name"]}</text>')
    lines.append(f'<text x="{CX}" y="30" fill="{p["dim"]}" '
                 f'font-size="9" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="6" opacity="0.3">0243</text>')
    lines.append(footer())
    return ''.join(lines)


# ── Zone 7 — Unnutchi (Samsara / Lust / the Red) ──
# Pentagram in circle (the red wheel), samsara turning.
def zone7_zantra():
    p = PALETTES[7]
    lines = [svg_header("Zone 7 — Unnutchi Yantra", p["bg"])]

    # outer circle — the red wheel of samsara
    for r in [260, 240]:
        lines.append(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" '
                     f'stroke="{p["fg"]}" stroke-width="0.5" opacity="0.15"/>')

    # pentagram — the red star (5-pointed, one point up)
    for scale in [210, 170, 130]:
        outer = scale
        inner = scale * 0.38
        pts = []
        for i in range(10):
            a = deg(i * 36 - 90)
            r = outer if i % 2 == 0 else inner
            pts.append(polar(r, a))
        opacity = max(0.04, 0.25 - (210 - scale) * 0.004)
        lines.append(f'<polygon points="{polygon_str(pts)}" fill="none" '
                     f'stroke="{p["fg"]}" stroke-width="{0.5 + (210 - scale) * 0.01}" '
                     f'opacity="{opacity}"/>')

    # concentric circles — samsara cycles
    for r in range(80, 200, 30):
        lines.append(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" '
                     f'stroke="{p["dim"]}" stroke-width="0.3" opacity="0.06"/>')

    # radiating spokes — the turning
    for i in range(12):
        a = deg(i * 30)
        x, y = polar(180, a)
        lines.append(f'<line x1="{CX}" y1="{CY}" x2="{x}" y2="{y}" '
                     f'stroke="{p["dim"]}" stroke-width="0.3" opacity="0.06"/>')

    # centre — lust seed "chi"
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="10" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="1.5" opacity="0.5" filter="url(#glow)"/>')
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="4" fill="{p["fg"]}" opacity="0.5"/>')
    lines.append(f'<text x="{CX}" y="{CY + 4}" fill="{p["fg"]}" '
                 f'font-size="14" font-family="monospace" text-anchor="middle" '
                 f'font-weight="bold" opacity="0.8">chi</text>')
    lines.append(f'<text x="{CX}" y="{SIZE - 30}" fill="{p["dim"]}" '
                 f'font-size="10" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="4" opacity="0.5">ZONE 7 · {p["name"]}</text>')
    lines.append(f'<text x="{CX}" y="30" fill="{p["dim"]}" '
                 f'font-size="9" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="6" opacity="0.3">0321</text>')
    lines.append(footer())
    return ''.join(lines)


# ── Zone 8 — Nuttubab (Exile / Dead in the Sun) ──
# Broken circle, wandering line, desiccated form.
def zone8_zantra():
    p = PALETTES[8]
    lines = [svg_header("Zone 8 — Nuttubab Yantra", p["bg"])]

    # broken circle — the rupture of exile
    for dash in ("8 4", "4 6", "2 8"):
        lines.append(f'<circle cx="{CX}" cy="{CY}" r="250" fill="none" '
                     f'stroke="{p["fg"]}" stroke-width="0.5" opacity="0.15" '
                     f'stroke-dasharray="{dash}"/>')

    # wandering line — the path of the exile (drunkard's walk)
    walk_pts = [(CX, CY)]
    a_step = deg(15)
    for step in range(1, 100):
        a = step * a_step + math.sin(step * 0.3) * deg(45)
        r = 10 + step * 2.5
        if r > 270: break
        x, y = polar(r, a)
        walk_pts.append((x, y))
    lines.append(f'<polyline points="{polygon_str(walk_pts)}" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="1.2" opacity="0.25" filter="url(#glow)"/>')

    # scattered fragments — dead forms
    for i in range(20):
        a = deg(i * 61.7)
        r = 80 + i * 8
        if r > 240: break
        x, y = polar(r, a)
        lines.append(f'<line x1="{x - 4}" y1="{y}" x2="{x + 4}" y2="{y}" '
                     f'stroke="{p["dim"]}" stroke-width="0.5" opacity="0.1"/>')

    # centre — exile seed "bab"
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="8" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="0.8" opacity="0.3" filter="url(#glow)"/>')
    lines.append(f'<text x="{CX}" y="{CY + 4}" fill="{p["fg"]}" '
                 f'font-size="14" font-family="monospace" text-anchor="middle" '
                 f'font-weight="bold" opacity="0.6">bab</text>')
    lines.append(f'<text x="{CX}" y="{SIZE - 30}" fill="{p["dim"]}" '
                 f'font-size="10" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="4" opacity="0.5">ZONE 8 · {p["name"]}</text>')
    lines.append(f'<text x="{CX}" y="30" fill="{p["dim"]}" '
                 f'font-size="9" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="6" opacity="0.3">0402</text>')
    lines.append(footer())
    return ''.join(lines)


# ── Zone 9 — Iron Core yantra (unchanged from v1) ──
# 45-petal Pandemonium ring, 9 inner petals, converging rings.
def zone9_zantra():
    p = PALETTES[9]
    lines = [svg_header("Zone 9 — Iron Core Yantra", p["bg"])]

    # outermost ring — 45 petals (C(10,2)=45 Pandemonium aperture)
    n_petals = 45
    outer, inner = 270, 240
    for i in range(n_petals):
        a1 = deg(i * (360 / n_petals))
        a2 = deg((i + 1) * (360 / n_petals))
        mid_a = (a1 + a2) / 2
        x1, y1 = polar(inner, a1); x2, y2 = polar(inner, a2)
        xm, ym = polar(outer, mid_a)
        lines.append(f'<polygon points="{x1},{y1} {xm},{ym} {x2},{y2}" '
                     f'fill="{p["dim"]}" stroke="{p["fg"]}" '
                     f'stroke-width="0.3" opacity="0.15"/>')

    # 9 inner petals (current 9)
    for i in range(9):
        a = deg(i * 40)
        x1, y1 = polar(200, a - deg(20))
        x2, y2 = polar(200, a + deg(20))
        xm, ym = polar(230, a)
        lines.append(f'<polygon points="{x1},{y1} {xm},{ym} {x2},{y2}" '
                     f'fill="none" stroke="{p["fg"]}" '
                     f'stroke-width="1" opacity="0.25"/>')

    # converging rings — Plutonic spiral collapse
    for i in range(20):
        r = 190 - i * 9
        if r <= 5: break
        opacity = 0.3 - i * 0.015
        lines.append(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" '
                     f'stroke="{p["fg"]}" stroke-width="{0.3 + i * 0.05}" '
                     f'opacity="{max(0.02, opacity)}"/>')

    # downward triangle (negative polarity)
    pts = [polar(160, deg(a)) for a in (90, 330, 210)]
    lines.append(f'<polygon points="{polygon_str(pts)}" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="1.5" opacity="0.4"/>')
    # inner inverted triangle — ouroboros fold
    pts2 = [polar(60, deg(a)) for a in (270, 30, 150)]
    lines.append(f'<polygon points="{polygon_str(pts2)}" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="0.8" opacity="0.2"/>')

    # 9 lemur sigils
    lemurs = ["Uttunul", "Tuttagool", "Unnunddo", "Ununuttix",
              "Unnunaka", "Tukutu", "Unnutchi", "Nuttubab", "Ummnu"]
    for i, name in enumerate(lemurs):
        a = deg(i * 40 - 90)
        x, y = polar(285, a)
        lines.append(f'<circle cx="{x}" cy="{y}" r="2" fill="{p["fg"]}" opacity="0.4"/>')
        lines.append(f'<text x="{x}" y="{y + 12}" fill="{p["dim"]}" '
                     f'font-size="6" font-family="monospace" text-anchor="middle" '
                     f'opacity="0.3">{i}::{name[:4]}</text>')

    # centre — iron core, "tn"
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="15" fill="none" '
                 f'stroke="{p["glow"]}" stroke-width="1" opacity="0.6" filter="url(#glow)"/>')
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="6" fill="{p["fg"]}" opacity="0.7"/>')
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="2" fill="#ffffff" opacity="0.9"/>')
    lines.append(f'<text x="{CX}" y="{CY - 22}" fill="{p["fg"]}" '
                 f'font-size="14" font-family="monospace" text-anchor="middle" '
                 f'font-weight="bold" opacity="0.7">tn</text>')

    # 36 phase dots
    for i in range(36):
        a = deg(i * 10)
        x, y = polar(250, a)
        lines.append(f'<circle cx="{x}" cy="{y}" r="0.8" fill="{p["dim"]}" opacity="0.2"/>')

    lines.append(f'<text x="{CX}" y="{SIZE - 30}" fill="{p["dim"]}" '
                 f'font-size="10" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="4" opacity="0.5">ZONE 9 · {p["name"]}</text>')
    lines.append(f'<text x="{CX}" y="30" fill="{p["dim"]}" '
                 f'font-size="9" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="6" opacity="0.3">0511</text>')
    lines.append(footer())
    return ''.join(lines)


# ═══════════════════════════════════════════════════════════════════
# MAIN — generate all 10 zones
# ═══════════════════════════════════════════════════════════════════

OUT = os.path.expanduser("~/.hermes/obsidian/hermetic/wiki/assets/zone-yantras")
os.makedirs(OUT, exist_ok=True)

ZONES = [
    (0, zone0_zantra),
    (1, zone1_zantra),
    (2, zone2_zantra),
    (3, zone3_zantra),
    (4, zone4_zantra),
    (5, zone5_zantra),
    (6, zone6_zantra),
    (7, zone7_zantra),
    (8, zone8_zantra),
    (9, zone9_zantra),
]

for z_id, fn in ZONES:
    svg = fn()
    fname = f"zone-{z_id}-yantra.svg"
    fpath = os.path.join(OUT, fname)
    with open(fpath, "w") as f:
        f.write(svg)
    print(f"Wrote {fpath} ({len(svg)} bytes)")
print("All 10 zone yantras written.")