#!/usr/bin/env python3
"""
zone_pixel_sprites.py — Generate zone-grounded pixel-art sprites using hardware palettes.

One 512x512 source image per zone is rendered programmatically (zone symbol + number
+ zone name on hardware-background tint), then Floyd-Steinberg-pixel-arted with the
correct hardware palette via pixel_art().

Usage:
    python zone_pixel_sprites.py              # All 10 zones
    python zone_pixel_sprites.py 3 7          # Specific zones only
    python zone_pixel_sprites.py --all         # Same as no args
    python zone_pixel_sprites.py --out /tmp/z  # Custom output dir
    python zone_pixel_sprites.py --block 6     # Override pixel block
    python zone_pixel_sprites.py --no-pixel    # Source images only, skip pixel-art

Zone background tint maps toward the hardware palette's mean RGB.
Pixel suffix is zone_id lowercased, e.g. zone-3-sprite.png.

Requires:
    PIL (Pillow)
    pixel_art skill library (found via sys.path)
"""

import argparse
import os
import sys

# ── pixel-art skill library ────────────────────────────────────────────────

def _find_pixel_art_scripts():
    """Locate pixel_art.py & palettes.py from hermes skill dir."""
    skill_dir = os.path.expanduser("~/.hermes/skills/creative/pixel-art/scripts")
    repo_dir  = os.path.expanduser("~/numogram/cli/scripts")
    for d in [skill_dir, repo_dir]:
        pa = os.path.join(d, "pixel_art.py")
        pb = os.path.join(d, "palettes.py")
        if os.path.exists(pa) and os.path.exists(pb):
            return d
    return None

_script_dir = _find_pixel_art_scripts()
if _script_dir:
    sys.path.insert(0, _script_dir)
    from pixel_art import pixel_art, PRESETS
    from palettes import PALETTES
else:
    pixel_art = None
    PALETTES = {}

# ── Zone data ──────────────────────────────────────────────────────────────

ZONE_HW_PALETTE = {
    0: "MONO_AMBER", 1: "GAMEBOY_ORIGINAL", 2: "GAMEBOY_POCKET",
    3: "C64", 4: "ZX_SPECTRUM", 5: "APPLE_II_HI", 6: "TELETEXT",
    7: "GAMEBOY_VIRTUALBOY", 8: "APPLE_II_LO", 9: "PICO_8",
}

ZONE_NAMES = [
    "VOID", "FIRST", "DOUBLING", "ACCELERANDO",
    "DECELERANDO", "ATTENTION", "ABJECTIVE", "PUNCTURE",
    "BLOOD", "PLEX",
]

# Default block size (pixel size) per hardware palette
BLOCK_DEFAULT = {
    "MONO_AMBER":           6,
    "GAMEBOY_ORIGINAL":     8,
    "GAMEBOY_POCKET":       8,
    "C64":                  8,
    "ZX_SPECTRUM":          10,
    "APPLE_II_HI":          10,
    "TELETEXT":             10,
    "GAMEBOY_VIRTUALBOY":   8,
    "APPLE_II_LO":          10,
    "PICO_8":               6,
}

def _tint(pal_name: str) -> tuple[int, int, int]:
    colors = PALETTES.get(pal_name, [(30, 30, 30)])
    r = int(sum(c[0] for c in colors) / len(colors))
    g = int(sum(c[1] for c in colors) / len(colors))
    b = int(sum(c[2] for c in colors) / len(colors))
    return (r // 4, g // 4, b // 4)   # 25 % saturation background


# ── Source image generator ──────────────────────────────────────────────────

def make_source(zid: int, size: int = 512) -> "Image.Image":
    """Render a {size}px square source image for zone zid."""
    from PIL import Image, ImageDraw, ImageFont

    pal_name = ZONE_HW_PALETTE[zid]
    bg = _tint(pal_name)
    img = Image.new("RGB", (size, size), bg)
    d = ImageDraw.Draw(img)

    colors = PALETTES[pal_name]
    fg  = colors[0]
    hi  = colors[min(3, len(colors) - 1)]
    mid = colors[min(1, len(colors) - 1)]

    # ── concentric ring glyph ──
    cx, cy = size // 2, size // 2
    r_outer = int(size * 0.35)
    r_inner = int(size * 0.14)

    d.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer],
              fill=mid, outline=fg, width=3)
    d.ellipse([cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner],
              fill=bg)

    # ── zone number ──
    try:
        font_num = ImageFont.truetype(
            "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", int(size * 0.28))
        font_lbl = ImageFont.truetype(
            "/usr/share/fonts/TTF/DejaVuSans.ttf",        int(size * 0.048))
    except OSError:
        font_num = ImageFont.load_default()
        font_lbl = font_num

    num_str  = str(zid)
    name_str = ZONE_NAMES[zid]

    bbox = d.textbbox((0, 0), num_str, font=font_num)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text((cx - tw // 2, cy - r_inner + int(size * 0.035)),
           num_str, fill=hi, font=font_num)

    # ── zone name ──
    bbox2 = d.textbbox((0, 0), name_str, font=font_lbl)
    tw2 = bbox2[2] - bbox2[0]
    d.text((cx - tw2 // 2, int(size * 0.90)), name_str, fill=fg, font=font_lbl)

    # ── 4x4 grid (subtle) ──
    step = size // 5
    for i in range(1, 5):
        d.line([(i * step, 0), (i * step, size)], fill=mid, width=1)
        d.line([(0, i * step), (size, i * step)], fill=mid, width=1)

    # ── diagonal cross (very subtle) ──
    off = int(size * 0.04)
    c_dim = tuple(max(0, x - 30) for x in fg)
    d.line([(off, off), (size - off, size - off)], fill=c_dim, width=1)
    d.line([(size - off, off), (off, size - off)], fill=c_dim, width=1)

    return img


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Zone pixel-art sprite generator")
    parser.add_argument("zones", nargs="*", type=int, default=[],
                        help="Zone IDs to render (default: all 0-9)")
    parser.add_argument("--all", action="store_true",
                        help="Force all 10 zones")
    parser.add_argument("--out", default="~/numogram/docs/wiki/assets/zone-sprites",
                        help="Output directory")
    parser.add_argument("--block", type=int, default=None,
                        help="Override pixel block size")
    parser.add_argument("--no-pixel", action="store_true",
                        help="Skip pixel-art, save source images only")
    parser.add_argument("--size", type=int, default=512,
                        help="Source image dimension (default: 512)")
    args = parser.parse_args()

    out_dir = os.path.expanduser(args.out)
    os.makedirs(out_dir, exist_ok=True)

    zones = args.zones if args.zones else list(range(10))
    if args.all:
        zones = list(range(10))

    for zid in zones:
        pal_name  = ZONE_HW_PALETTE.get(zid, "C64")
        # resonant preset if we have one, otherwise soak the palette in neutral c64 tuning
        preset    = pal_name.lower() if pal_name.lower() in PRESETS else "c64"
        block     = args.block or BLOCK_DEFAULT.get(pal_name, 8)
        palette   = pal_name  # UPPERCASE PALETTES key — passed as override past the preset check

        src_path   = os.path.join(out_dir, f"zone-{zid}-source.png")
        sprite_path = os.path.join(out_dir, f"zone-{zid}-sprite.png")

        img = make_source(zid, size=args.size)
        img.save(src_path)
        print(f"Z{zid:02d} SOURCE  {src_path}")

        if not args.no_pixel and pixel_art:
            try:
                pixel_art(src_path, sprite_path, preset=preset, block=block, palette=palette)
                print(f"Z{zid:02d} SPRITE  {sprite_path}  block={block}  preset={preset}  palette={palette}")
            except Exception as e:
                sys.stderr.write(f"  [FAIL] Z{zid}: {e}\n")
        else:
            print(f"Z{zid:02d} SKIP-PIXEL  (pixel_art={'unavail' if not pixel_art else 'disabled'})")

    print(f"\nDone → {out_dir}")

if __name__ == "__main__":
    main()
