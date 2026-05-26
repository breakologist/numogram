#!/usr/bin/env python3
"""Zone Yantra v2 — instrument-grade mandala SVGs for all 10 numogram zones.
Implements the design spec from wiki/zone-yantra-v2-design.md.
"""
import math, os, random

SIZE = 600
CX = CY = SIZE // 2

PALETTES = {
    0: {"bg": "#0a0a08", "fg": "#FFB000", "dim": "#4a3a10", "glow": "#FFD700",
        "name": "MONO_AMBER",  "label": "VOID",       "particle": "eiaoung"},
    1: {"bg": "#0a0806", "fg": "#8B5E3C", "dim": "#2a1a08", "glow": "#A07040",
        "name": "UR_EARTH",   "label": "MURRUMUR",   "particle": "mu"},
    2: {"bg": "#060a0c", "fg": "#3399FF", "dim": "#0a2030", "glow": "#87CEEB",
        "name": "DEEP_WATER", "label": "TUTTAGOOL",  "particle": "tu"},
    3: {"bg": "#0a0606", "fg": "#FF4500", "dim": "#3a1008", "glow": "#FF7040",
        "name": "KALASUTRA",  "label": "UNNUNDDO",   "particle": "un"},
    4: {"bg": "#080a0c", "fg": "#C8E4F0", "dim": "#203848", "glow": "#E0F0FF",
        "name": "CLEAVING",   "label": "UNUNUTTIX",  "particle": "ix"},
    5: {"bg": "#080808", "fg": "#888098", "dim": "#303038", "glow": "#B0A8C0",
        "name": "SPECTRAL",   "label": "UNNUNAKA",   "particle": "ma"},
    6: {"bg": "#08060a", "fg": "#8855CC", "dim": "#281848", "glow": "#CC55AA",
        "name": "BINDING",    "label": "TUKUTU",     "particle": "ku"},
    7: {"bg": "#0a0608", "fg": "#CC1133", "dim": "#3a0818", "glow": "#FF5599",
        "name": "SAMSARA",    "label": "UNNUTCHI",   "particle": "chi"},
    8: {"bg": "#080a06", "fg": "#6B8E23", "dim": "#202818", "glow": "#8AAF50",
        "name": "EXILE",      "label": "NUTTUBAB",   "particle": "bab"},
    9: {"bg": "#0a080a", "fg": "#9900FF", "dim": "#3a1050", "glow": "#CC66FF",
        "name": "PICO_8",     "label": "IRON CORE",  "particle": "tn"},
}

HEADER = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">
<rect width="{size}" height="{size}" fill="{bg}"/>'''

FOOTER = '</svg>\n'

DEFS = '''<defs>
  <filter id="g" x="-50%" y="-50%" width="200%" height="200%"
    ><feGaussianBlur stdDeviation="2" result="b"
    /><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter
  >
  <filter id="G" x="-50%" y="-50%" width="200%" height="200%"
    ><feGaussianBlur stdDeviation="5" result="b"
    /><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter
  >
</defs>'''

def deg(d): return d * math.pi / 180
def polar(r, t, cx=CX, cy=CY):
    return cx + r * math.cos(t), cy + r * math.sin(t)

def pp(pts):
    """Points to SVG polygon string."""
    return ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)

# ── helpers: metadata, bhupura ──

def label(p, zone_id, mesh):
    return [
        f'<text x="{CX}" y="{SIZE-28}" fill="{p["dim"]}" font-size="10" '
        f'font-family="monospace" text-anchor="middle" letter-spacing="4" '
        f'opacity="0.5">ZONE {zone_id} · {p["name"]}</text>',
        f'<text x="{CX}" y="26" fill="{p["dim"]}" font-size="9" '
        f'font-family="monospace" text-anchor="middle" letter-spacing="6" '
        f'opacity="0.3">{mesh}</text>',
    ]

def circle(cx, cy, r, stroke, width, opacity, **kw):
    attrs = ' '.join(f'{k}="{v}"' for k, v in kw.items())
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{stroke}" stroke-width="{width}" opacity="{opacity}" {attrs}/>'

def line(x1,y1,x2,y2, stroke, width, opacity, **kw):
    attrs = ' '.join(f'{k}="{v}"' for k, v in kw.items())
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}" opacity="{opacity}" {attrs}/>'

# ═══════════════════════════════════════════════════════════════════
# ZONE 0 — VOID (negative-space yantra)
# ═══════════════════════════════════════════════════════════════════

def zone0_v2():
    p = PALETTES[0]
    bg = p["bg"]
    lines = [HEADER.format(size=SIZE, bg=bg), DEFS]

    # background: CRT scanlines
    for y in range(0, SIZE, 3):
        lines.append(f'<line x1="0" y1="{y}" x2="{SIZE}" y2="{y}" '
                     f'stroke="{p["fg"]}" stroke-width="0.3" opacity="0.012"/>')

    # outer bhupura — single hairline
    lines.append(circle(CX, CY, 265, p["dim"], 0.4, 0.25))

    # concentric rotated squares as cut-out ABSENCES — negative space
    for i, r in enumerate([230, 190, 150, 110, 70]):
        pts = [polar(r, deg(45 + i * 90)) for i in range(4)]
        # Each square is drawn as barely-touching lines with gaps
        for j in range(4):
            x1, y1 = pts[j]
            x2, y2 = pts[(j+1) % 4]
            # Leave a gap at each corner — lines don't meet
            mx, my = (x1+x2)/2, (y1+y2)/2
            # Shorten each line toward midpoint
            shorten = 6
            fx = (x2 - x1) / 2
            fy = (y2 - y1) / 2
            ln = math.hypot(fx, fy)
            if ln < 1: continue
            sx, sy = fx / ln * shorten, fy / ln * shorten
            nx1, ny1 = x1 + sx, y1 + sy
            nx2, ny2 = x2 - sx, y2 - sy
            op = max(0.02, 0.15 - i * 0.025 - j * 0.005)
            w = 0.3 + i * 0.3
            lines.append(f'<line x1="{nx1:.1f}" y1="{ny1:.1f}" x2="{nx2:.1f}" '
                         f'y2="{ny2:.1f}" stroke="{p["fg"]}" stroke-width="{w}" '
                         f'opacity="{op}"/>')

    # faint upright triangle — barely suggested, gap at each vertex
    tri_pts = [polar(100, deg(a)) for a in (90, 210, 330)]
    for j in range(3):
        x1, y1 = tri_pts[j]
        x2, y2 = tri_pts[(j+1)%3]
        mx, my = (x1+x2)/2, (y1+y2)/2
        fx, fy = (x2-x1)/2, (y2-y1)/2
        ln = math.hypot(fx, fy)
        if ln < 1: continue
        sx, sy = fx/ln * 4, fy/ln * 4
        lines.append(f'<line x1="{x1+sx:.1f}" y1="{y1+sy:.1f}" x2="{x2-sx:.1f}" '
                     f'y2="{y2-sy:.1f}" stroke="{p["dim"]}" stroke-width="0.5" opacity="0.04"/>')

    # bindu NOT AS A DOT — as a missing dot. The "bindu" is an empty circle
    # surrounded by a faint glow of what is not there.
    lines.append(circle(CX, CY, 5, p["fg"], 0.5, 0.3))
    lines.append(circle(CX, CY, 9, p["fg"], 0.3, 0.15, filter="url(#g)"))
    # The actual centre is black — nothing there
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="3" fill="{bg}"/>')
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="1" fill="{p["dim"]}" opacity="0.2"/>')

    # seed syllable as gaps — the letters are spaces where light is absent
    seed = list("eiaoung")
    for i, ch in enumerate(seed):
        a = deg(i * (360 / len(seed)) - 90)
        x, y = polar(26, a)
        # Rendered as a small empty circle with a tiny dot above it
        # like an afterimage mark
        lines.append(f'<circle cx="{x}" cy="{y}" r="3" fill="none" '
                     f'stroke="{p["dim"]}" stroke-width="0.3" opacity="0.15"/>')
        lines.append(f'<text x="{x}" y="{y+1}" fill="{p["dim"]}" '
                     f'font-size="6" font-family="monospace" text-anchor="middle" '
                     f'dominant-baseline="central" opacity="0.2">{ch}</text>')

    # label
    lines.extend(label(p, 0, "0000"))
    lines.append(FOOTER)
    return ''.join(lines)


# ═══════════════════════════════════════════════════════════════════
# ZONE 1 — MURRUMUR / EARTH (compression folds)
# ═══════════════════════════════════════════════════════════════════

def zone1_v2():
    p = PALETTES[1]
    lines = [HEADER.format(size=SIZE, bg=p["bg"]), DEFS]

    # bhupura: rectangular enclosing frame (earth's four corners)
    lines.append(f'<rect x="40" y="40" width="520" height="520" fill="none" '
                 f'stroke="{p["dim"]}" stroke-width="0.8" opacity="0.15" rx="4"/>')

    # background: sediment grain — random dots
    rng = random.Random(123)
    for _ in range(600):
        x = rng.randint(50, 550)
        y = rng.randint(50, 550)
        lines.append(f'<circle cx="{x}" cy="{y}" r="{rng.uniform(0.3, 0.8)}" '
                     f'fill="{p["fg"]}" opacity="0.015"/>')

    # compression folds — strata that bunch at the bottom
    # Use non-uniform spacing: denser near bottom (burial)
    for i in range(40):
        # y position with compression: tight at bottom, loose at top
        t = i / 40
        # compressed: more lines in bottom third
        y = CY + 220 - t * 440
        # Add a little waviness
        y_wobble = y + 3 * math.sin(i * 0.7)
        # Opacity: bottom layers are denser (darker)
        opacity = 0.08 + 0.12 * (1 - t)  # fades upward
        if opacity <= 0: continue
        # Width: bottom strata thicker
        w = 0.3 + 1.5 * (1 - t)
        # Angled slightly at edges toward convergence
        x1 = 80 + t * 30
        x2 = 520 - t * 30
        lines.append(f'<line x1="{x1:.1f}" y1="{y_wobble:.1f}" x2="{x2:.1f}" '
                     f'y2="{y_wobble:.1f}" stroke="{p["fg"]}" stroke-width="{w:.2f}" '
                     f'opacity="{opacity:.3f}"/>')

    # descending triangle — implied by the converging edges, not explicit
    # Draw two angled boundary lines that suggest the triangle form
    tri_left = [(80, CY-220), (CX, CY+80)]
    tri_right = [(520, CY-220), (CX, CY+80)]
    lines.append(line(tri_left[0][0], tri_left[0][1], tri_left[1][0], tri_left[1][1],
                     p["dim"], 0.5, 0.06))
    lines.append(line(tri_right[0][0], tri_right[0][1], tri_right[1][0], tri_right[1][1],
                     p["dim"], 0.5, 0.06))

    # buried fragment — diagonal line at different angle (old ruin)
    lines.append(line(CX-60, CY+120, CX+40, CY+60, p["dim"], 0.8, 0.04,
                     stroke_dasharray="3 4"))

    # centre — "mu" at the BOTTOM, buried in densest strata
    lines.append(circle(CX, CY+80, 8, p["glow"], 0.5, 0.2, filter="url(#g)"))
    lines.append(f'<text x="{CX}" y="{CY+84}" fill="{p["fg"]}" '
                 f'font-size="12" font-family="monospace" text-anchor="middle" '
                 f'font-weight="bold" opacity="0.5">mu</text>')

    lines.extend(label(p, 1, "0023"))
    lines.append(FOOTER)
    return ''.join(lines)


# ═══════════════════════════════════════════════════════════════════
# ZONE 2 — TUTTAGOOL / WATER (balanced hexagram + phase-gradient ripples)
# ═══════════════════════════════════════════════════════════════════

def zone2_v2():
    p = PALETTES[2]
    lines = [HEADER.format(size=SIZE, bg=p["bg"]), DEFS]

    # bhupura: wavy circle that never quite closes
    n_pts = 72
    wave_pts = []
    for i in range(n_pts + 1):
        a = deg(i * (360 / n_pts))
        r = 270 + 5 * math.sin(6 * a + i * 0.5)
        x, y = polar(r, a)
        wave_pts.append((x, y))
    # Leave a gap: omit last point
    lines.append(f'<polyline points="{pp(wave_pts[:-5])}" fill="none" '
                 f'stroke="{p["dim"]}" stroke-width="0.5" opacity="0.2"/>')

    # phase-gradient ripples — waves that flatten as they travel outward
    for i in range(20):
        r_base = 250 - i * 12
        if r_base < 10: break
        pts = []
        for a_deg in range(0, 360, 4):
            a = deg(a_deg)
            amp = 8 * (1 - i / 22)
            r = r_base + amp * math.sin(6 * a + i * 0.8)
            pts.append((polar(r, a)))
        op = max(0.01, 0.15 - i * 0.007)
        w = 0.3 + i * 0.03
        lines.append(f'<polyline points="{pp(pts)}" fill="none" '
                     f'stroke="{p["fg"]}" stroke-width="{w:.2f}" opacity="{op:.3f}"/>')

    # phase transition boundary at r=190 — liquid→solid hint
    for a_deg in range(0, 360, 5):
        a = deg(a_deg)
        r = 190 + 3 * math.sin(12 * a)
        x, y = polar(r, a)
        # Short crystalline marks at the transition boundary
        cx1, cy1 = polar(r-2, a)
        cx2, cy2 = polar(r+2, a)
        lines.append(line(cx1, cy1, cx2, cy2, p["dim"], 0.3, 0.06))

    # HEXAGRAM — BOTH TRIANGLES EQUAL. Critical fix from v1.
    hex_r = 130
    up_pts = [polar(hex_r, deg(a)) for a in (90, 330, 210)]
    dn_pts = [polar(hex_r, deg(a)) for a in (30, 270, 150)]
    lines.append(f'<polygon points="{pp(up_pts)}" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="1.2" opacity="0.25"/>')
    lines.append(f'<polygon points="{pp(dn_pts)}" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="1.2" opacity="0.25"/>')

    # Inner hexagram (smaller, reversed opacity)
    hex_r2 = 80
    up_pts2 = [polar(hex_r2, deg(a)) for a in (90, 330, 210)]
    dn_pts2 = [polar(hex_r2, deg(a)) for a in (30, 270, 150)]
    lines.append(f'<polygon points="{pp(up_pts2)}" fill="none" '
                 f'stroke="{p["dim"]}" stroke-width="0.5" opacity="0.12"/>')
    lines.append(f'<polygon points="{pp(dn_pts2)}" fill="none" '
                 f'stroke="{p["dim"]}" stroke-width="0.5" opacity="0.12"/>')

    # centre — "tu" under ripple overlay
    lines.append(circle(CX, CY, 10, p["glow"], 0.4, 0.3, filter="url(#g)"))
    lines.append(f'<text x="{CX}" y="{CY+4}" fill="{p["fg"]}" '
                 f'font-size="14" font-family="monospace" text-anchor="middle" '
                 f'font-weight="bold" opacity="0.65">tu</text>')
    # ripple OVERLAY on top of text — small wave arcs passing over centre
    for i in range(4):
        a = deg(i * 90)
        x1, y1 = polar(16, a - deg(10))
        x2, y2 = polar(16, a + deg(10))
        lines.append(line(x1, y1, x2, y2, p["dim"], 0.3, 0.1))

    # water caustic background — overlapping sine grids
    for i in range(30):
        y = 40 + i * 18
        lines.append(f'<line x1="0" y1="{y + 5*math.sin(i*0.7)}" '
                     f'x2="{SIZE}" y2="{y + 5*math.sin(i*0.7 + 2)}" '
                     f'stroke="{p["fg"]}" stroke-width="0.2" opacity="0.008"/>')

    lines.extend(label(p, 2, "0046"))
    lines.append(FOOTER)
    return ''.join(lines)


# ═══════════════════════════════════════════════════════════════════
# ZONE 3 — UNNUNDDO / FIRE / KALASUTRA (self-consuming spiral)
# ═══════════════════════════════════════════════════════════════════

def zone3_v2():
    p = PALETTES[3]
    lines = [HEADER.format(size=SIZE, bg=p["bg"]), DEFS]

    # charred boundary — irregular dashed ring
    lines.append(circle(CX, CY, 280, p["dim"], 1.5, 0.12,
                       stroke_dasharray="3 7 1 5 2 9 4 6"))

    # background: pixel burn scars (vertical streaks)
    for i in range(80):
        x = 40 + i * 6.5
        h = 80 + abs(math.sin(i * 0.5)) * 200
        lines.append(f'<line x1="{x:.1f}" y1="{CX - h/2:.1f}" x2="{x:.1f}" '
                     f'y2="{CX + h/2:.1f}" stroke="{p["dim"]}" stroke-width="0.5" '
                     f'opacity="{0.003 + 0.01 * abs(math.sin(i * 0.3)):.4f}"/>')

    # Self-consuming spiral — outer turns fragment into ember-dots
    spiral_pts = []
    for a_deg in range(0, 1080, 4):
        a = deg(a_deg)
        r = 240 * (1 - a_deg / 1080 * 0.88)
        if r < 5: break
        spiral_pts.append(polar(r, a))

    # Inner spiral (solid line)
    inner_len = int(len(spiral_pts) * 0.65)
    lines.append(f'<polyline points="{pp(spiral_pts[:inner_len])}" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="1.2" opacity="0.2" filter="url(#g)"/>')

    # Outer spiral (dotted — fragmenting)
    for i in range(inner_len, len(spiral_pts), 3):
        if i >= len(spiral_pts): break
        x, y = spiral_pts[i]
        op = 0.15 * (1 - (i - inner_len) / (len(spiral_pts) - inner_len))
        lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1" '
                     f'fill="{p["glow"]}" opacity="{op:.3f}"/>')

    # Flame triangles — overlapping and intercutting, not nesting
    for i in range(8):
        base_r = 260 - i * 30
        op = 0.18 - i * 0.02
        if op <= 0.01: break
        rot = i * 7
        pts = [polar(base_r, deg(90 + rot + j*120)) for j in range(3)]
        lines.append(f'<polygon points="{pp(pts)}" fill="none" '
                     f'stroke="{p["fg"]}" stroke-width="{0.3 + i * 0.2}" '
                     f'opacity="{op:.3f}"/>')

    # seed "un" with spark fragments
    lines.append(circle(CX, CY, 12, p["fg"], 1.0, 0.3, filter="url(#g)"))
    lines.append(f'<text x="{CX}" y="{CY+4}" fill="{p["fg"]}" '
                 f'font-size="16" font-family="monospace" text-anchor="middle" '
                 f'font-weight="bold" opacity="0.7">un</text>')

    # Sparks around seed
    for i in range(15):
        a = deg(rng := random.random() * 360)
        r = 18 + random.random() * 12
        x, y = polar(r, a)
        lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{0.3 + random.random() * 0.5}" '
                     f'fill="{p["glow"]}" opacity="{0.1 + random.random() * 0.2:.3f}"/>')

    lines.extend(label(p, 3, "0122"))
    lines.append(FOOTER)
    return ''.join(lines)


# ═══════════════════════════════════════════════════════════════════
# ZONE 4 — UNUNUTTIX / AIR / CLEAVING (broken symmetry)
# ═══════════════════════════════════════════════════════════════════

def zone4_v2():
    p = PALETTES[4]
    lines = [HEADER.format(size=SIZE, bg=p["bg"]), DEFS]

    SPLIT = 16  # px shift between halves — visible gap

    # background: frost/crackle — dendritic branching lines
    rng = random.Random(42)
    def branch(x, y, angle, depth, max_depth=4):
        if depth >= max_depth: return []
        r = rng.uniform(20, 60)
        end_x = x + r * math.cos(angle)
        end_y = y + r * math.sin(angle)
        res = [(x, y, end_x, end_y)]
        res.extend(branch(end_x, end_y, angle + rng.uniform(-0.5, 0.5), depth+1, max_depth))
        res.extend(branch(end_x, end_y, angle + rng.uniform(-0.8, 0.8), depth+1, max_depth))
        return res
    crack_lines = []
    for _ in range(10):
        a = rng.uniform(0, 2*math.pi)
        start_r = rng.uniform(60, 200)
        sx, sy = polar(start_r, a)
        crack_lines.extend(branch(sx, sy, a, 0, 3))
    for x1, y1, x2, y2 in crack_lines[:120]:
        lines.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                     f'stroke="{p["fg"]}" stroke-width="0.3" opacity="0.08"/>')

    # SPLIT CIRCLE — two halves displaced with visible gap
    # Right half: 270°→90° (through 0°, right side), shifted RIGHT
    half_r = []
    for a_deg in range(271, 451, 3):
        a = deg(a_deg)
        x, y = polar(265, a)
        half_r.append((x + SPLIT, y))
    for a_deg in range(0, 91, 3):
        a = deg(a_deg)
        x, y = polar(265, a)
        half_r.append((x + SPLIT, y))
    lines.append(f'<polyline points="{pp(half_r)}" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="1.0" opacity="0.3"/>')

    # Left half: 90°→270° (through 180°, left side), shifted LEFT, rotated -2°
    half_l = []
    for a_deg in range(91, 271, 3):
        a = deg(a_deg - 2)
        x, y = polar(265, a)
        half_l.append((x - SPLIT, y))
    lines.append(f'<polyline points="{pp(half_l)}" fill="none" '
                 f'stroke="{p["dim"]}" stroke-width="1.0" opacity="0.2"/>')

    # FAULT LINE — bold vertical gap marker
    lines.append(line(CX - SPLIT//2, CY-260, CX - SPLIT//2, CY+260,
                     p["fg"], 0.5, 0.06, stroke_dasharray="2 4"))

    # fracture rays — asymmetrical, not 8 but 7
    for i in range(7):
        a = deg(10 + i * 51)
        r = 120 + i * 10
        x, y = polar(r, a)
        lines.append(f'<line x1="{CX}" y1="{CY}" x2="{x:.1f}" y2="{y:.1f}" '
                     f'stroke="{p["fg"]}" stroke-width="0.5" '
                     f'opacity="{0.12 + i * 0.04:.3f}"/>')

    # rotated squares — broken, with gaps
    for i, r in enumerate([200, 140]):
        for side in range(4):
            a1 = deg(45 + side * 90)
            a2 = deg(45 + (side+1) * 90)
            x1, y1 = polar(r, a1)
            x2, y2 = polar(r, a2)
            # Draw only if this side doesn't cross the fault
            mid_x = (x1 + x2) / 2
            if abs(mid_x - CX) > SPLIT:
                lines.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" '
                             f'y2="{y2:.1f}" stroke="{p["fg"]}" stroke-width="0.4" '
                             f'opacity="0.08"/>')

    # seed "ix" — cleaved in half
    lines.append(circle(CX - SPLIT//2, CY, 5, p["glow"], 0.3, 0.2, filter="url(#g)"))
    lines.append(f'<text x="{CX - SPLIT}" y="{CY+4}" fill="{p["fg"]}" '
                 f'font-size="12" font-family="monospace" text-anchor="middle" '
                 f'font-weight="bold" opacity="0.5">i</text>')
    lines.append(f'<text x="{CX + SPLIT}" y="{CY+4}" fill="{p["dim"]}" '
                 f'font-size="12" font-family="monospace" text-anchor="middle" '
                 f'font-weight="bold" opacity="0.3">x</text>')

    lines.extend(label(p, 4, "0161"))
    lines.append(FOOTER)
    return ''.join(lines)


# ═══════════════════════════════════════════════════════════════════
# ZONE 5 — UNNUNAKA / MAKHAI / SPECTRAL (aperture star)
# ═══════════════════════════════════════════════════════════════════

def zone5_v2():
    p = PALETTES[5]
    lines = [HEADER.format(size=SIZE, bg=p["bg"]), DEFS]

    # moiré background — overlapping fine grids
    for i in range(120):
        y = i * 5
        x_offset = math.sin(i * 0.1) * 10
        lines.append(f'<line x1="0" y1="{y + x_offset:.1f}" x2="{SIZE}" '
                     f'y2="{y + x_offset + 2:.1f}" stroke="{p["dim"]}" '
                     f'stroke-width="0.2" opacity="0.005"/>')
    for i in range(120):
        x = i * 5
        y_offset = math.sin(i * 0.1) * 10
        lines.append(f'<line x1="{x + y_offset:.1f}" y1="0" x2="{x + y_offset + 2:.1f}" '
                     f'y2="{SIZE}" stroke="{p["dim"]}" '
                     f'stroke-width="0.2" opacity="0.005"/>')

    # pentagonal bhupura
    penta_r = 275
    penta_pts = [polar(penta_r, deg(i * 72 - 90)) for i in range(5)]
    lines.append(f'<polygon points="{pp(penta_pts)}" fill="none" '
                 f'stroke="{p["dim"]}" stroke-width="0.5" opacity="0.12"/>')

    # WEAPON WHEELS — 5 concentric stars, each rotated 7.2° 
    for wheel in range(5):
        outer_r = 250 - wheel * 40
        inner_r = outer_r * 0.38
        rot_offset = wheel * deg(7.2)
        pts = []
        for i in range(10):
            a = deg(i * 36 - 90) + rot_offset
            r = outer_r if i % 2 == 0 else inner_r
            pts.append(polar(r, a))
        op = 0.18 - wheel * 0.03
        lines.append(f'<polygon points="{pp(pts)}" fill="none" '
                     f'stroke="{p["fg"]}" stroke-width="{0.3 + wheel * 0.1}" '
                     f'opacity="{max(0.02, op):.3f}"/>')

    # DOMINANT STRIKE — asymmetrical, toward Zone 4 (left)
    strike_a = deg(180)  # pointing left (toward Z4)
    strike_len = 270
    x_end, y_end = polar(strike_len, strike_a)
    lines.append(line(CX, CY, x_end, y_end, p["fg"], 1.2, 0.25, filter="url(#g)"))
    # After-trail: shorter, fainter
    for i, angle in enumerate([72, 144, 216, 288]):
        a = deg(angle - 90)
        r = 150 + i * 20
        x2, y2 = polar(r, a)
        lines.append(line(CX, CY, x2, y2, p["dim"], 0.4, 0.06))

    # spectral highlight — one region with violet shift
    for i in range(20):
        a = deg(170 + i * 0.5)
        r = 80 + i * 4
        x, y = polar(r, a)
        lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="0.5" '
                     f'fill="#A8A0B0" opacity="{0.02 + i * 0.003:.4f}"/>')

    # seed "ma" — displaced by strike
    lines.append(circle(CX - 8, CY, 7, p["glow"], 0.3, 0.3, filter="url(#g)"))
    lines.append(f'<text x="{CX - 8}" y="{CY + 4}" fill="{p["fg"]}" '
                 f'font-size="14" font-family="monospace" text-anchor="middle" '
                 f'font-weight="bold" opacity="0.65">ma</text>')

    lines.extend(label(p, 5, "0184"))
    lines.append(FOOTER)
    return ''.join(lines)


# ═══════════════════════════════════════════════════════════════════
# ZONE 6 — TUKUTU / BINDING (lemniscate primary + tension threads)
# ═══════════════════════════════════════════════════════════════════

def zone6_v2():
    p = PALETTES[6]
    lines = [HEADER.format(size=SIZE, bg=p["bg"]), DEFS]

    # weave/knot background
    for i in range(80):
        y = i * 7.5
        lines.append(f'<line x1="0" y1="{y:.1f}" x2="{SIZE}" y2="{y:.1f}" '
                     f'stroke="{p["dim"]}" stroke-width="0.2" opacity="0.005"/>')
    for i in range(80):
        x = i * 7.5
        lines.append(f'<line x1="{x:.1f}" y1="0" x2="{x - SIZE*0.5:.1f}" '
                     f'y2="{SIZE}" stroke="{p["dim"]}" '
                     f'stroke-width="0.2" opacity="0.005"/>')

    # bhupura: hexagonal frame
    hex_r = 275
    hex_pts = [polar(hex_r, deg(i * 60 - 30)) for i in range(6)]
    lines.append(f'<polygon points="{pp(hex_pts)}" fill="none" '
                 f'stroke="{p["dim"]}" stroke-width="0.5" opacity="0.15"/>')

    # TENSION LEMNISCATE — primary structure, loops different sizes
    lem_pts = []
    for t_deg in range(0, 361, 3):
        t = deg(t_deg)
        # Upper loop larger, lower loop tighter
        upper_scale = 1.08
        lower_scale = 0.92
        scale = upper_scale if math.sin(t) >= 0 else lower_scale
        r_norm = 180 * scale
        x = CX + r_norm * math.sin(t) * math.cos(t)
        # Slight asymmetry: upper loop leans right, lower leans left
        y_off = 15 * math.sin(t * 0.5)
        y = CY + r_norm * math.sin(t) * abs(math.cos(t)) * 0.5 * (-1 if t_deg > 180 else 1) + y_off
        lem_pts.append((x, y))
    lines.append(f'<polyline points="{pp(lem_pts)}" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="1.5" opacity="0.25" filter="url(#g)"/>')

    # BINDING THREADS — wrapping around the lemniscate
    for i in range(12):
        a = deg(i * 30)
        wrap_r = 140 + 20 * math.sin(i * 3)
        x1, y1 = polar(wrap_r, a)
        # Wrap to opposite side
        a2 = deg(i * 30 + 150 + 30 * math.sin(i * 2))
        x2, y2 = polar(wrap_r * 0.7, a2)
        lines.append(f'<path d="M{x1:.1f},{y1:.1f} Q{CX},{CY} {x2:.1f},{y2:.1f}" '
                     f'fill="none" stroke="{p["dim"]}" stroke-width="0.4" '
                     f'opacity="0.08"/>')

    # TENSION MARKS at lemniscate outer curves
    for t_deg in range(0, 360, 12):
        t = deg(t_deg)
        r_norm = 180 * (1.08 if math.sin(t) >= 0 else 0.92)
        x = CX + r_norm * math.sin(t) * math.cos(t)
        y_off = 15 * math.sin(t * 0.5)
        y = CY + r_norm * math.sin(t) * abs(math.cos(t)) * 0.5 * (-1 if t_deg > 180 else 1) + y_off
        # Perpendicular tick mark
        dx = -math.sin(t)
        dy = math.cos(t)
        lines.append(line(x-3, y-3, x+3, y+3, p["dim"], 0.3, 0.06))
        lines.append(line(x-3, y+3, x+3, y-3, p["dim"], 0.3, 0.06))

    # seed "ku" at lemniscate crossing
    lines.append(circle(CX, CY, 10, p["glow"], 0.5, 0.3, filter="url(#g)"))
    lines.append(f'<text x="{CX}" y="{CY+4}" fill="{p["fg"]}" '
                 f'font-size="16" font-family="monospace" text-anchor="middle" '
                 f'font-weight="bold" opacity="0.7">ku</text>')

    lines.extend(label(p, 6, "0243"))
    lines.append(FOOTER)
    return ''.join(lines)


# ═══════════════════════════════════════════════════════════════════
# ZONE 7 — UNNUTCHI / SAMSARA / LUST (spinning pentagram wheel)
# ═══════════════════════════════════════════════════════════════════

def zone7_v2():
    p = PALETTES[7]
    lines = [HEADER.format(size=SIZE, bg=p["bg"]), DEFS]

    # pulse grid background
    for y in range(30, SIZE, 18):
        for x in range(30, SIZE, 18):
            phase = math.hypot(x-CX, y-CY) * 0.05
            r = 0.3 + 0.5 * abs(math.sin(phase))
            lines.append(f'<circle cx="{x}" cy="{y}" r="{r:.1f}" '
                         f'fill="{p["dim"]}" opacity="0.008"/>')

    # outer wheel — double circle with dash gradient
    lines.append(circle(CX, CY, 270, p["fg"], 0.5, 0.12))
    lines.append(circle(CX, CY, 255, p["dim"], 0.3, 0.08,
                       stroke_dasharray="4 8 1 6 3 7"))

    # 24 SPOKES with drag — uneven intervals, trailing-edge thickening
    for i in range(24):
        a = deg(i * 15 - 0.5 * i)  # slight offset accumulates
        op = 0.04 + 0.08 * abs(math.sin(a))
        # trailing edge thicker: the spoke that just passed top is blurred
        blur_factor = abs(math.cos(a * 0.5))
        lines.append(line(CX, CY, *polar(200, a), p["dim"], 0.2 + blur_factor * 0.4, op))

    # PENTAGRAM with angular velocity — trailing arcs at vertices
    for scale in [220, 180, 140, 100, 60]:
        outer = scale
        inner = scale * 0.38
        pts = []
        for i in range(10):
            a = deg(i * 36 - 90)
            r = outer if i % 2 == 0 else inner
            pts.append(polar(r, a))
        op = 0.05 + (scale / 220) * 0.2
        lines.append(f'<polygon points="{pp(pts)}" fill="none" '
                     f'stroke="{p["fg"]}" stroke-width="{0.3 + (220-scale)/100 * 0.5}" '
                     f'opacity="{op:.3f}"/>')
        # Trailing arc at each outer vertex
        for i in range(0, 10, 2):
            a = deg(i * 36 - 90)
            x, y = polar(outer, a)
            # Arc trailing in direction of rotation
            arc_x, arc_y = polar(outer + 5, a - deg(3))
            lines.append(f'<path d="M{x:.1f},{y:.1f} Q{(x+arc_x)/2:.1f},{(y+arc_y)/2:.1f} '
                         f'{arc_x:.1f},{arc_y:.1f}" fill="none" stroke="{p["glow"]}" '
                         f'stroke-width="0.5" opacity="{op * 0.5:.3f}"/>')

    # centre "chi" with spinning offset ring
    lines.append(circle(CX, CY, 12, p["fg"], 1.2, 0.35, filter="url(#g)"))
    lines.append(circle(CX, CY, 4, p["fg"], 0.5, 0.4))
    # offset spinning ring
    lines.append(circle(CX + 3, CY + 2, 6, p["glow"], 0.3, 0.15, filter="url(#g)",
                       stroke_dasharray="2 3"))
    lines.append(f'<text x="{CX}" y="{CY+4}" fill="{p["fg"]}" '
                 f'font-size="14" font-family="monospace" text-anchor="middle" '
                 f'font-weight="bold" opacity="0.8">chi</text>')

    lines.extend(label(p, 7, "0321"))
    lines.append(FOOTER)
    return ''.join(lines)


# ═══════════════════════════════════════════════════════════════════
# ZONE 8 — NUTTUBAB / EXILE (jagged path + shattered relics)
# ═══════════════════════════════════════════════════════════════════

def zone8_v2():
    p = PALETTES[8]
    lines = [HEADER.format(size=SIZE, bg=p["bg"]), DEFS]

    # erosion mask background — missing patches in faint grid
    rng = random.Random(888)
    for y in range(20, SIZE, 16):
        for x in range(20, SIZE, 16):
            if rng.random() < 0.2:  # 20% missing — erosion
                continue
            lines.append(f'<circle cx="{x}" cy="{y}" r="0.5" '
                         f'fill="{p["dim"]}" opacity="0.008"/>')

    # BROKEN CIRCLES — with per-dash length variation
    rng2 = random.Random(777)
    for base_r in [260, 240, 220]:
        segments = []
        a = 0
        while a < 360:
            dash_len = 5 + rng2.random() * 15
            gap_len = 3 + rng2.random() * 8
            end_a = min(a + dash_len, 360)
            # arc segment
            for t in range(int(a), int(end_a)):
                ta = deg(t)
                x1, y1 = polar(base_r, ta)
                x2, y2 = polar(base_r, deg(t + 1))
                segments.append((x1, y1, x2, y2))
            a = end_a + gap_len
        # Only draw a subset to avoid vector overload
        for x1, y1, x2, y2 in segments[:150]:
            lines.append(line(x1, y1, x2, y2, p["fg"], 0.3, 0.08))

    # JAGGED EXILE PATH — broken movement, sudden direction changes
    walk_pts = [(CX, CY)]
    a = 0
    r = 8
    step = 0
    while r < 265:
        # Sudden direction changes
        if step % 5 == 0:
            a += rng2.uniform(-1.2, 1.2)
        else:
            a += rng2.gauss(0, 0.3)
        r += 2.0 + rng2.random() * 1.5
        x, y = polar(r, a)
        walk_pts.append((x, y))
        step += 1
    lines.append(f'<polyline points="{pp(walk_pts)}" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="1.0" opacity="0.2" filter="url(#g)"/>')

    # SHATTERED RELICS — recognizable fragments from other zones
    rng3 = random.Random(555)
    relic_types = [
        # Zone 0: diamond corner fragment
        lambda x, y, a: [line(x-8, y, x, y-6, p["fg"], 0.3, 0.06),
                         line(x, y-6, x+8, y, p["fg"], 0.3, 0.06)],
        # Zone 7: pentagram vertex fragment
        lambda x, y, a: [line(x-5, y-5, x, y-8, p["fg"], 0.3, 0.06),
                         line(x, y-8, x+5, y-5, p["fg"], 0.3, 0.06)],
        # Zone 5: star point fragment
        lambda x, y, a: [line(x, y, x-4, y+6, p["fg"], 0.3, 0.05),
                         line(x, y, x+4, y+6, p["fg"], 0.3, 0.05)],
        # Zone 6: binding thread fragment
        lambda x, y, a: [line(x-6, y-2, x, y, p["fg"], 0.3, 0.05),
                         line(x, y, x+5, y+1, p["fg"], 0.3, 0.05)],
    ]
    for _ in range(12):
        rx = rng3.randint(80, 520)
        ry = rng3.randint(80, 520)
        # Make sure it's on or near the exile path
        rt = rng3.choice(relic_types)
        for l in rt(rx, ry, 0):
            lines.append(l)

    # seed "bab" — faint, displaced, smallest
    lines.append(circle(CX + 3, CY - 2, 6, p["glow"], 0.3, 0.15, filter="url(#g)"))
    lines.append(f'<text x="{CX + 3}" y="{CY}" fill="{p["fg"]}" '
                 f'font-size="10" font-family="monospace" text-anchor="middle" '
                 f'font-weight="bold" opacity="0.4">bab</text>')

    lines.extend(label(p, 8, "0402"))
    lines.append(FOOTER)
    return ''.join(lines)


# ═══════════════════════════════════════════════════════════════════
# ZONE 9 — IRON CORE / UMMNU (gem-cut mineral 45-facet structure)
# ═══════════════════════════════════════════════════════════════════

def zone9_v2():
    p = PALETTES[9]
    lines = [HEADER.format(size=SIZE, bg=p["bg"]), DEFS]

    # gem facet background — angled lines at ±45°
    for i in range(80):
        y = i * 7.5
        lines.append(f'<line x1="0" y1="{y:.1f}" x2="{SIZE}" y2="{y:.1f}" '
                     f'stroke="{p["dim"]}" stroke-width="0.2" opacity="0.004"/>')
        lines.append(f'<line x1="0" y1="{y:.1f}" x2="{SIZE}" y2="{y + SIZE*0.5:.1f}" '
                     f'stroke="{p["dim"]}" stroke-width="0.2" opacity="0.003"/>')

    # 45 FACET RING — mineral, alternating opacity = light catching facets
    n_facets = 45
    outer, inner = 270, 235
    for i in range(n_facets):
        a1 = deg(i * (360 / n_facets))
        a2 = deg((i + 1) * (360 / n_facets))
        mid_a = (a1 + a2) / 2
        x1, y1 = polar(inner, a1); x2, y2 = polar(inner, a2)
        xm, ym = polar(outer, mid_a)
        # Alternating light catch — like gem facets
        catch = 0.10 if i % 2 == 0 else 0.18
        lines.append(f'<polygon points="{x1:.1f},{y1:.1f} {xm:.1f},{ym:.1f} {x2:.1f},{y2:.1f}" '
                     f'fill="{p["dim"]}" stroke="{p["fg"]}" '
                     f'stroke-width="0.3" opacity="{catch:.2f}"/>')

    # PLUTONIC HEAT GRADIENT — 24 converging rings, cold to hot
    for i in range(24):
        r = 225 - i * 9
        if r < 4: break
        t = i / 24
        # Interpolate from cold purple to hot magenta-white
        r1 = 0x66 + int((0xEE - 0x66) * t)
        g1 = 0x00 + int((0x88 - 0x00) * t)
        b1 = 0xAA + int((0xFF - 0xAA) * t)
        color = f'#{r1:02x}{g1:02x}{b1:02x}'
        op = 0.25 - i * 0.01
        w = 0.3 + i * 0.08
        lines.append(circle(CX, CY, r, color, w, max(0.01, op)))

    # 9 INNER PETALS
    for i in range(9):
        a = deg(i * 40)
        x1, y1 = polar(195, a - deg(18))
        x2, y2 = polar(195, a + deg(18))
        xm, ym = polar(220, a)
        lines.append(f'<polygon points="{x1:.1f},{y1:.1f} {xm:.1f},{ym:.1f} {x2:.1f},{y2:.1f}" '
                     f'fill="none" stroke="{p["fg"]}" '
                     f'stroke-width="0.8" opacity="0.2"/>')

    # 9 LEMUR SIGILS AS MINERAL INCLUSIONS — each a different micro-geometry
    lemur_shapes = [
        # triangle, square, diamond, pentagon, hexagon, line, cross, dot, star
        [(0, -4), (-3, 3), (3, 3)],  # triangle
        [(-3, -3), (3, -3), (3, 3), (-3, 3)],  # square
        [(0, -4), (3, 0), (0, 4), (-3, 0)],  # diamond
        [(-3, -3), (0, -4), (3, -3), (2, 2), (-2, 2)],  # pentagon
        [(-3, -2), (0, -4), (3, -2), (3, 2), (0, 4), (-3, 2)],  # hexagon
        [(-3, 0), (3, 0)],  # line
        [(-2, -2), (2, 2), (0, -2), (0, 2)],  # cross
        [(0, 0)],  # dot
        [(0, -4), (1, -1), (4, -1), (2, 1), (3, 4), (0, 2), (-3, 4), (-2, 1), (-4, -1), (-1, -1)],  # star
    ]
    for i in range(9):
        a = deg(i * 40 - 90)
        x, y = polar(275, a)
        shape = lemur_shapes[i % len(lemur_shapes)]
        s_pts = [(x + dx, y + dy) for dx, dy in shape]
        lines.append(f'<polygon points="{pp(s_pts)}" fill="none" '
                     f'stroke="{p["glow"]}" stroke-width="0.4" opacity="0.25"/>')

    # 45-BIT BINARY RIM — 45 markers encoding the 45 demons
    binary_ring = [
        1,0,1,0,1,1,0,0,1,  # first 9 demons
        0,1,1,1,0,0,1,0,1,
        1,0,0,1,1,0,1,0,0,
        1,1,0,0,1,0,1,1,0,
        1,0,1,1,0,0,1,0,0,  # 45th
    ]
    for i, bit in enumerate(binary_ring):
        a = deg(i * (360 / 45))
        r_mark = 282
        x, y = polar(r_mark, a)
        if bit:
            lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.2" '
                         f'fill="{p["fg"]}" opacity="0.3"/>')
        else:
            lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="0.6" '
                         f'fill="{p["dim"]}" opacity="0.1"/>')

    # DOWNWARD TRIANGLE (negative polarity) + inner inverted
    tri_pts = [polar(155, deg(a)) for a in (90, 330, 210)]
    lines.append(f'<polygon points="{pp(tri_pts)}" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="2.0" opacity="0.3"/>')
    tri_inner = [polar(55, deg(a)) for a in (270, 30, 150)]
    lines.append(f'<polygon points="{pp(tri_inner)}" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="0.7" opacity="0.15"/>')

    # IRON CORE — white-hot centre
    lines.append(circle(CX, CY, 16, p["glow"], 0.8, 0.5, filter="url(#G)"))
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="7" fill="{p["fg"]}" opacity="0.6"/>')
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="3" fill="#ffffff" opacity="0.8"/>')
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="1" fill="#ffffff" opacity="1.0"/>')
    # "tn" above the core
    lines.append(f'<text x="{CX}" y="{CY - 24}" fill="{p["fg"]}" '
                 f'font-size="14" font-family="monospace" text-anchor="middle" '
                 f'font-weight="bold" opacity="0.6">tn</text>')

    lines.extend(label(p, 9, "0511"))
    lines.append(FOOTER)
    return ''.join(lines)


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

OUT = os.path.expanduser("~/.hermes/obsidian/hermetic/wiki/assets/zone-yantras-v2")
os.makedirs(OUT, exist_ok=True)

ZONES = [
    (0, zone0_v2),
    (1, zone1_v2),
    (2, zone2_v2),
    (3, zone3_v2),
    (4, zone4_v2),
    (5, zone5_v2),
    (6, zone6_v2),
    (7, zone7_v2),
    (8, zone8_v2),
    (9, zone9_v2),
]

for z_id, fn in ZONES:
    svg = fn()
    fname = f"zone-{z_id}-yantra-v2.svg"
    fpath = os.path.join(OUT, fname)
    with open(fpath, "w") as f:
        f.write(svg)
    print(f"Wrote {fpath} ({len(svg)} bytes)")

print("All 10 zone yantra v2 written.")
