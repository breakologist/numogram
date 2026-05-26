#!/usr/bin/env python3
"""
cross_palette_matrix.py — Generate a zone × palette cross-comparison matrix.

For each zone (0-9), renders the zone source image through every hardware
and artistic palette in the pixel_art skill library. Outputs individual
cell images + an HTML gallery for browsing.

Usage:
    python cross_palette_matrix.py                              # full matrix
    python cross_palette_matrix.py --zones 0 3 9               # specific zones
    python cross_palette_matrix.py --palettes C64 PICO_8       # specific palettes
    python cross_palette_matrix.py --out /tmp/matrix           # custom output
    python cross_palette_matrix.py --size 64                   # cell size (px)
"""

import argparse
import os
import sys

# ── Locate pixel-art library ──────────────────────────────────────────

def _find_pixel_art():
    for d in [
        os.path.expanduser("~/.hermes/skills/creative/pixel-art/scripts"),
        os.path.expanduser("~/numogram/cli/scripts"),
    ]:
        pa = os.path.join(d, "pixel_art.py")
        pb = os.path.join(d, "palettes.py")
        if os.path.exists(pa) and os.path.exists(pb):
            sys.path.insert(0, d)
            return pa, pb
    return None, None

pa_path, _ = _find_pixel_art()
if pa_path:
    from pixel_art import pixel_art, PRESETS
    from palettes import PALETTES, build_palette_image
else:
    sys.exit("ERROR: pixel_art.py + palettes.py not found")

# ── Palette selection ─────────────────────────────────────────────────

HARDWARE_PALETTES = [
    "MONO_AMBER", "MONO_GREEN", "MONO_BW",
    "GAMEBOY_ORIGINAL", "GAMEBOY_POCKET", "GAMEBOY_VIRTUALBOY",
    "C64", "ZX_SPECTRUM", "APPLE_II_HI", "APPLE_II_LO",
    "TELETEXT", "PICO_8", "NES", "CGA_MODE4_PAL1",
    "MSX", "MICROSOFT_WINDOWS_16", "MICROSOFT_WINDOWS_PAINT",
]

ARTISTIC_PALETTES = [
    "HILMA_AF_KLINT", "PASTEL_DREAM", "NEON_CYBER",
    "OCEAN_DEEP", "SUNSET_FIRE", "ELECTRIC_VIOLET",
    "EARTH_CLAY", "RETRO_WARM", "ARCTIC_ICE", "FOREST_MOSS",
    "VINTAGE_ROSE",
]

ALL_PALETTES = HARDWARE_PALETTES + ARTISTIC_PALETTES

# ── Zone data ─────────────────────────────────────────────────────────

ZONE_NAMES = ["Void", "Stability", "Separation", "Release", "Catastrophe",
              "Pressure", "Abstraction", "Blood", "Multiplicity", "Iron Core"]

ZONE_HW_PALETTE = {
    0: "MONO_AMBER", 1: "GAMEBOY_ORIGINAL", 2: "GAMEBOY_POCKET",
    3: "C64", 4: "ZX_SPECTRUM", 5: "APPLE_II_HI", 6: "TELETEXT",
    7: "GAMEBOY_VIRTUALBOY", 8: "APPLE_II_LO", 9: "PICO_8",
}

# ── Generation ────────────────────────────────────────────────────────

def generate_cell(zid: int, palette: str, src_dir: str, out_dir: str,
                   cell_size: int = 96) -> str | None:
    """Generate a single zone × palette cell image. Returns path or None."""
    src_path = os.path.join(src_dir, f"zone-{zid}-source.png")
    if not os.path.exists(src_path):
        return None

    cell_name = f"z{zid}_{palette.lower()}.png"
    cell_path = os.path.join(out_dir, cell_name)

    if os.path.exists(cell_path):
        return cell_path  # already generated

    try:
        preset = palette.lower() if palette.lower() in PRESETS else "c64"
        pixel_art(src_path, cell_path, preset=preset, block=4,
                  palette=palette)
        return cell_path
    except Exception as e:
        sys.stderr.write(f"  [FAIL] Z{zid} × {palette}: {e}\n")
        return None


def build_html(matrix, palette_order, zone_order, out_dir):
    """Generate HTML gallery from generated cell paths."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Cross-Palette Matrix — Zone × Palette</title>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{background:#08080a;color:#999;font-family:'Courier New',monospace;padding:20px}}
  h1{{text-align:center;color:#555;font-size:14px;letter-spacing:4px;margin-bottom:4px}}
  .sub{{text-align:center;color:#333;font-size:10px;letter-spacing:2px;margin-bottom:20px}}
  table{{border-collapse:collapse;margin:auto;font-size:10px}}
  th,td{{border:1px solid #1a1a26;padding:4px;text-align:center;background:#0d0d14}}
  th{{background:#111;color:#555;writing-mode:vertical-lr;text-orientation:mixed;height:100px;font-size:9px;letter-spacing:1px;font-weight:400}}
  th.pal{{writing-mode:horizontal-tb;height:auto;padding:6px 4px;font-size:9px;color:#444}}
  td{{min-width:96px;vertical-align:middle}}
  td img{{display:block;margin:auto;width:72px;height:72px;image-rendering:pixelated}}
  td .label{{font-size:7px;color:#444;margin-top:2px}}
  td.hw{{border-color:#2a2a3a}}
  td.art{{border-color:#1a2a2a}}
  .legend{{text-align:center;margin:16px auto;font-size:9px;color:#444;display:flex;gap:16px;justify-content:center}}
  .legend span{{padding:2px 8px;border:1px solid #1a1a26;border-radius:2px}}
  .legend .hw{{background:#111;border-color:#2a2a3a}}
  .legend .art{{background:#0d1414;border-color:#1a2a2a}}
</style>
</head>
<body>
<h1>CROSS-PALETTE MATRIX</h1>
<div class="sub">10 zones × {n_pal} palettes · pixel-art Floyd-Steinberg dither</div>
<div class="legend">
  <span class="hw">Hardware palettes</span>
  <span class="art">Artistic / custom palettes</span>
</div>
<table>
<tr><th></th>""".format(n_pal=len(palette_order))

    # Header row: palette names
    for pal in palette_order:
        cls = "pal hw" if pal in HARDWARE_PALETTES else "pal art"
        html += f'<th class="{cls}">{pal}</th>'
    html += "</tr>\n"

    # Data rows: one per zone
    for zid in zone_order:
        html += f'<tr><th>{zid} · {ZONE_NAMES[zid]}</th>'
        for pal in palette_order:
            cell_name = f"z{zid}_{pal.lower()}.png"
            cell_path = matrix.get((zid, pal))
            cls = "hw" if pal in HARDWARE_PALETTES else "art"
            if cell_path and os.path.exists(cell_path):
                html += f'<td class="{cls}"><img src="{cell_name}" alt="Z{zid} {pal}"></td>'
            else:
                html += f'<td class="{cls}" style="color:#222;font-size:18px">·</td>'
        html += "</tr>\n"

    html += """</table>
</body>
</html>"""
    
    index_path = os.path.join(out_dir, "index.html")
    with open(index_path, "w") as f:
        f.write(html)
    return index_path


def main():
    parser = argparse.ArgumentParser(description="Cross-palette matrix generator")
    parser.add_argument("--zones", nargs="*", type=int, default=list(range(10)))
    parser.add_argument("--palettes", nargs="*", default=ALL_PALETTES)
    parser.add_argument("--out", default="~/numogram/docs/wiki/assets/matrix-cells")
    parser.add_argument("--size", type=int, default=96,
                        help="Cell image size in px (default: 96)")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Reuse existing cells, only regenerate missing")
    args = parser.parse_args()

    out_dir = os.path.expanduser(args.out)
    os.makedirs(out_dir, exist_ok=True)

    # Source images location
    src_dir = os.path.expanduser("~/numogram/docs/wiki/assets/zone-sprites")

    zone_order = sorted(set(args.zones) & set(range(10)))
    palette_order = args.palettes

    if not zone_order:
        zone_order = list(range(10))
    if not palette_order:
        palette_order = ALL_PALETTES

    print(f"Generating {len(zone_order)} zones × {len(palette_order)} palettes")
    print(f"Output: {out_dir}")
    print(f"Cell size: {args.size}px")
    print()

    generated = 0
    skipped = 0
    failed = 0
    matrix = {}

    for zid in zone_order:
        for pal in palette_order:
            key = (zid, pal)
            # Check if already exists
            cell_name = f"z{zid}_{pal.lower()}.png"
            cell_path = os.path.join(out_dir, cell_name)
            if args.skip_existing and os.path.exists(cell_path):
                matrix[key] = cell_path
                skipped += 1
                continue

            result = generate_cell(zid, pal, src_dir, out_dir, args.size)
            if result:
                matrix[key] = result
                generated += 1
            else:
                failed += 1

    # Build HTML
    index_path = build_html(matrix, palette_order, zone_order, out_dir)
    
    print(f"\nDone — {generated} generated, {skipped} reused, {failed} failed")
    print(f"Gallery: {index_path}")


if __name__ == "__main__":
    main()
