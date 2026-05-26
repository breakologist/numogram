#!/usr/bin/env python3
"""Generate yantra/mandala SVGs for numogram zones.
First pair: Zone 0 (Void) and Zone 9 (Iron Core).
"""

import math
import os

SIZE = 600
CX = CY = SIZE // 2

# ── Zone palettes ──────────────────────────────────────────────────
PALETTES = {
    0: {"bg": "#0a0a08", "fg": "#FFB000", "dim": "#4a3a10", "glow": "#FFD700",
        "name": "MONO_AMBER", "label": "VOID", "particle": "eiaoung"},
    9: {"bg": "#0a080a", "fg": "#9900FF", "dim": "#3a1050", "glow": "#CC66FF",
        "name": "PICO_8", "label": "IRON CORE", "particle": "tn"},
}

def svg_header(title, bg):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}" width="{SIZE}" height="{SIZE}">
<rect width="{SIZE}" height="{SIZE}" fill="{bg}"/>
<defs>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="2" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
'''

def svg_footer():
    return '</svg>\n'

def polar(r, theta, cx=CX, cy=CY):
    """Polar to cartesian."""
    return cx + r * math.cos(theta), cy + r * math.sin(theta)

def degrees(deg):
    return deg * math.pi / 180

# ═══════════════════════════════════════════════════════════════════
# ZONE 0 — VOID YANTRA
# ═══════════════════════════════════════════════════════════════════

def zone0_yantra():
    p = PALETTES[0]
    lines = [svg_header("Zone 0 — Void Yantra", p["bg"])]
    
    # 1. Faint outermost boundary circle (the limit of the void)
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="260" fill="none" '
                 f'stroke="{p["dim"]}" stroke-width="0.5" opacity="0.3"/>')
    
    # 2. Concentric void diamond — elongated diamond rings (rhombus)
    for i, r in enumerate([200, 160, 120, 80, 40]):
        opacity = 0.15 - i * 0.025
        # Elongated diamond: vertical axis longer than horizontal
        # Top/bottom points at r, left/right points at r*0.5
        points = []
        for angle, scale in [(90, 1.0), (180, 0.5), (270, 1.0), (360, 0.5)]:
            x, y = polar(r * scale, degrees(angle))
            points.append(f'{x},{y}')
        lines.append(f'<polygon points="{" ".join(points)}" fill="none" '
                     f'stroke="{p["fg"]}" stroke-width="{0.5 + i * 0.3}" '
                     f'opacity="{max(0.02, opacity)}"/>')
    
    # 3. Upright triangle (positive polarity) — very faint, barely suggested
    tri_r = 100
    tri_points = []
    for a in [90, 210, 330]:
        x, y = polar(tri_r, degrees(a))
        tri_points.append(f'{x},{y}')
    lines.append(f'<polygon points="{" ".join(tri_points)}" fill="none" '
                 f'stroke="{p["dim"]}" stroke-width="0.5" opacity="0.08"/>')
    
    # 4. The bindu — the central point
    # Outer glow ring
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="8" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="1" opacity="0.5" filter="url(#glow)"/>')
    # Inner point
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="2" fill="{p["fg"]}" opacity="0.8"/>')
    
    # 5. Seed syllable: e i a o u n g — arranged faintly around the centre
    seed = list("eiaoung")
    seed_r = 30
    for i, ch in enumerate(seed):
        a = degrees(i * (360 / len(seed)) - 90)
        x, y = polar(seed_r, a)
        lines.append(f'<text x="{x}" y="{y}" fill="{p["dim"]}" '
                     f'font-size="8" font-family="monospace" text-anchor="middle" '
                     f'dominant-baseline="central" opacity="0.3">{ch}</text>')
    
    # 6. Metadata — zone label at bottom
    lines.append(f'<text x="{CX}" y="{SIZE - 30}" fill="{p["dim"]}" '
                 f'font-size="10" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="4" opacity="0.5">ZONE 0 · {p["name"]}</text>')
    
    # 7. Mesh tag (0000) at top
    lines.append(f'<text x="{CX}" y="30" fill="{p["dim"]}" '
                 f'font-size="9" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="6" opacity="0.3">0000</text>')
    
    lines.append(svg_footer())
    return ''.join(lines)


# ═══════════════════════════════════════════════════════════════════
# ZONE 9 — IRON CORE YANTRA
# ═══════════════════════════════════════════════════════════════════

def zone9_yantra():
    p = PALETTES[9]
    lines = [svg_header("Zone 9 — Iron Core Yantra", p["bg"])]
    
    # 1. Outermost ring — 45 petals for the Pandemonium aperture (C(10,2)=45)
    petal_r_outer = 270
    petal_r_inner = 240
    n_petals = 45
    for i in range(n_petals):
        a1 = degrees(i * (360 / n_petals))
        a2 = degrees((i + 1) * (360 / n_petals))
        mid_a = (a1 + a2) / 2
        x1, y1 = polar(petal_r_inner, a1)
        x2, y2 = polar(petal_r_inner, a2)
        xm, ym = polar(petal_r_outer, mid_a)
        # Petal as triangle
        lines.append(f'<polygon points="{x1},{y1} {xm},{ym} {x2},{y2}" '
                     f'fill="{p["dim"]}" stroke="{p["fg"]}" '
                     f'stroke-width="0.3" opacity="0.15"/>')
    
    # 2. Nine inner petals (current 9)
    n_inner = 9
    for i in range(n_inner):
        a = degrees(i * (360 / n_inner))
        x1, y1 = polar(200, a - degrees(360/n_inner/2))
        x2, y2 = polar(200, a + degrees(360/n_inner/2))
        xm, ym = polar(230, a)
        lines.append(f'<polygon points="{x1},{y1} {xm},{ym} {x2},{y2}" '
                     f'fill="none" stroke="{p["fg"]}" '
                     f'stroke-width="1" opacity="0.25"/>')
    
    # 3. Converging rings — the Plutonic looping, spiral collapse
    for i in range(20):
        r = 190 - i * 9
        if r <= 5:
            break
        opacity = 0.3 - i * 0.015
        lines.append(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" '
                     f'stroke="{p["fg"]}" stroke-width="{0.3 + i * 0.05}" '
                     f'opacity="{max(0.02, opacity)}"/>')
    
    # 4. Downward-pointing triangle (negative polarity) — the core structure
    tri_r = 160
    tri_points = []
    for a in [90, 330, 210]:  # apex at bottom (negative polarity)
        x, y = polar(tri_r, degrees(a))
        tri_points.append(f'{x},{y}')
    lines.append(f'<polygon points="{" ".join(tri_points)}" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="1.5" opacity="0.4"/>')
    
    # Inner triangle (inverted — the ouroboros fold)
    tri_r2 = 60
    tri_points2 = []
    for a in [270, 30, 150]:  # apex at top — counter-rotation
        x, y = polar(tri_r2, degrees(a))
        tri_points2.append(f'{x},{y}')
    lines.append(f'<polygon points="{" ".join(tri_points2)}" fill="none" '
                 f'stroke="{p["fg"]}" stroke-width="0.8" opacity="0.2"/>')
    
    # 5. Nine lemurs as small sigils around the outer ring
    lemur_names = ["Uttunul", "Tuttagool", "Unnunddo", "Ununuttix",
                   "Unnunaka", "Tukutu", "Unnutchi", "Nuttubab", "Ummnu"]
    lemur_r = 285
    for i, name in enumerate(lemur_names):
        a = degrees(i * (360 / len(lemur_names)) - 90)
        x, y = polar(lemur_r, a)
        # Small dot for the lemur
        lines.append(f'<circle cx="{x}" cy="{y}" r="2" fill="{p["fg"]}" opacity="0.4"/>')
        lines.append(f'<text x="{x}" y="{y + 12}" fill="{p["dim"]}" '
                     f'font-size="6" font-family="monospace" text-anchor="middle" '
                     f'opacity="0.3">{i}::{name[:4]}</text>')
    
    # 6. Centre — the seed syllable "tn" and the Cthellloid iron core
    # Outer glow
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="15" fill="none" '
                 f'stroke="{p["glow"]}" stroke-width="1" opacity="0.6" filter="url(#glow)"/>')
    # The iron core centre
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="6" fill="{p["fg"]}" opacity="0.7"/>')
    lines.append(f'<circle cx="{CX}" cy="{CY}" r="2" fill="#ffffff" opacity="0.9"/>')
    
    # Seed syllable
    lines.append(f'<text x="{CX}" y="{CY - 22}" fill="{p["fg"]}" '
                 f'font-size="14" font-family="monospace" text-anchor="middle" '
                 f'font-weight="bold" opacity="0.7">tn</text>')
    
    # 7. Pandemonium reference — 512 phases, represented as 512 tiny dots
    # (Sampled to 36 around a circle for readability)
    for i in range(36):
        a = degrees(i * 10)
        x, y = polar(250, a)
        lines.append(f'<circle cx="{x}" cy="{y}" r="0.8" fill="{p["dim"]}" opacity="0.2"/>')
    
    # 8. Metadata
    lines.append(f'<text x="{CX}" y="{SIZE - 30}" fill="{p["dim"]}" '
                 f'font-size="10" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="4" opacity="0.5">ZONE 9 · {p["name"]}</text>')
    
    # Mesh tag
    lines.append(f'<text x="{CX}" y="30" fill="{p["dim"]}" '
                 f'font-size="9" font-family="monospace" text-anchor="middle" '
                 f'letter-spacing="6" opacity="0.3">0511</text>')
    
    lines.append(svg_footer())
    return ''.join(lines)


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

OUT = os.path.expanduser("~/.hermes/obsidian/hermetic/wiki/assets/zone-yantras")
os.makedirs(OUT, exist_ok=True)

z0 = zone0_yantra()
z9 = zone9_yantra()

with open(os.path.join(OUT, "zone-0-yantra.svg"), "w") as f:
    f.write(z0)
with open(os.path.join(OUT, "zone-9-yantra.svg"), "w") as f:
    f.write(z9)

print(f"Wrote {OUT}/zone-0-yantra.svg ({len(z0)} bytes)")
print(f"Wrote {OUT}/zone-9-yantra.svg ({len(z9)} bytes)")

# Copy to vault
import shutil
VAULT_ASSETS = os.path.expanduser("~/.hermes/obsidian/hermetic/wiki/assets/zone-yantras")
os.makedirs(VAULT_ASSETS, exist_ok=True)
for fname in ["zone-0-yantra.svg", "zone-9-yantra.svg"]:
    shutil.copy2(os.path.join(OUT, fname), os.path.join(VAULT_ASSETS, fname))
print(f"Copied to vault: {VAULT_ASSETS}/")
