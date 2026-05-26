#!/usr/bin/env python3
"""
oracle_pixel_traversal.py — Animated traversal GIF generator.

Takes an oracle seed, generates a zone path (8 steps), and renders each
step as a pixel-art frame using the zone's hardware palette sprite.

Usage:
    python oracle_pixel_traversal.py 174                     → /tmp/oracle_pixel_174.gif
    python oracle_pixel_traversal.py 42 /tmp/my.gif          → /tmp/my.gif
    python oracle_pixel_traversal.py 174 --fps 2             → 2 fps (default 1)
    python oracle_pixel_traversal.py 42 --size 300            → 300×300 frames
    python oracle_pixel_traversal.py 42 --duration 4          → 4 seconds per zone
"""

import os
import sys
import math
import argparse
from PIL import Image, ImageDraw, ImageFont

# ── Numogram oracle ──────────────────────────────────────────────────
ORACLE_DIR = os.path.expanduser("~/numogram/cli")
if ORACLE_DIR not in sys.path:
    sys.path.insert(0, ORACLE_DIR)
import oracle

# ── Zone metadata ────────────────────────────────────────────────────
ZONE_NAMES = ["Void", "Stability", "Separation", "Release", "Catastrophe",
              "Pressure", "Abstraction", "Blood", "Multiplicity", "Iron Core"]
ZONE_RGB = oracle._ZONE_TTY_RGB
SYZYGIES = {
    frozenset({4, 5}): {"current": 1, "demon": "Katak",    "region": "torque"},
    frozenset({3, 6}): {"current": 3, "demon": "Djynxx",   "region": "warp"},
    frozenset({2, 7}): {"current": 5, "demon": "Oddubb",   "region": "torque"},
    frozenset({1, 8}): {"current": 7, "demon": "Murrumur", "region": "torque"},
    frozenset({0, 9}): {"current": 9, "demon": "Uttunul",  "region": "plex"},
}

# ── Zone palette mapping ─────────────────────────────────────────────
ZONE_PALETTES = {
    0: "MONO_AMBER", 1: "GAMEBOY_ORIGINAL", 2: "GAMEBOY_POCKET",
    3: "C64", 4: "ZX_SPECTRUM", 5: "APPLE_II_HI", 6: "TELETEXT",
    7: "GAMEBOY_VIRTUALBOY", 8: "APPLE_II_LO", 9: "PICO_8",
}

REGION_LABELS = {
    (1, 2, 4, 5, 7, 8): "torque",
    (3, 6): "warp",
    (0, 9): "plex",
}

# ── Sprite paths ─────────────────────────────────────────────────────
SPRITE_DIR = os.path.expanduser("~/numogram/docs/wiki/assets/zone-sprites")

def get_sprite_path(zid: int) -> str | None:
    """Find the best sprite for a zone: dithered first, then source."""
    for name in [f"zone-{zid}-sprite.png", f"zone-{zid}-source.png"]:
        p = os.path.join(SPRITE_DIR, name)
        if os.path.exists(p):
            return p
    return None

# ── Frame rendering ──────────────────────────────────────────────────

def render_frame(zid: int, size: int, seed: int, step: int, total: int,
                 font_title, font_small) -> Image.Image:
    """Render one zone frame with sprite + metadata overlay."""
    frame = Image.new("RGB", (size, size), (8, 8, 14))
    draw = ImageDraw.Draw(frame)

    # ── Background zone colour wash ──
    rgb = ZONE_RGB.get(zid, (100, 100, 100))
    bg_box = Image.new("RGB", (size, size), (max(0, rgb[0]//8),
                                              max(0, rgb[1]//8),
                                              max(0, rgb[2]//8)))
    frame = Image.blend(frame, bg_box, 0.3)

    # ── Load zone sprite ──
    sprite_path = get_sprite_path(zid)
    if sprite_path:
        sprite = Image.open(sprite_path).convert("RGBA")
        # Scale sprite to fill ~60% of frame
        target = int(size * 0.55)
        sprite = sprite.resize((target, target), Image.NEAREST)
        # Centre it
        sx = (size - target) // 2
        sy = (size - target) // 2 + int(size * 0.03)  # slight vertical offset
        frame.paste(sprite, (sx, sy), sprite)
    else:
        # Fallback: draw zone number
        draw.text((size//2, size//2 - 20), str(zid),
                  fill=rgb, font=font_title, anchor="mm")

    # ── Metadata top bar ──
    zone_name = ZONE_NAMES[zid]
    particle = oracle.ZONES[zid]["name"]
    palette = ZONE_PALETTES[zid]
    bar_y = 6
    top_text = f"Z{zid} · {zone_name.upper()}  [{particle}]  {palette}"
    draw.text((size//2, bar_y), top_text, fill=rgb, font=font_small, anchor="ma")

    # ── Step indicator ──
    step_text = f"seed: {seed}  step: {step}/{total}"
    draw.text((size - 8, bar_y), step_text, fill=(100, 100, 100),
              font=font_small, anchor="ra")

    # ── Bottom bar ──
    region = ""
    for zones, r in REGION_LABELS.items():
        if zid in zones:
            region = r
            break

    # Gate info
    gate_z = oracle.get_gate(zid) if hasattr(oracle, 'get_gate') else f"Gt-{zid}"
    gate_str = str(gate_z) if not isinstance(gate_z, str) else gate_z

    bottom_y = size - 6
    left_footer = f"{region.upper()} · {palette}"
    right_footer = f"{gate_str}"

    draw.text((8, bottom_y), left_footer, fill=(80, 80, 80),
              font=font_small, anchor="ld")
    draw.text((size - 8, bottom_y), right_footer, fill=(80, 80, 80),
              font=font_small, anchor="rd")

    # ── Border ──
    draw.rectangle([0, 0, size-1, size-1], outline=(20, 20, 30), width=1)

    return frame


# ── Frame interpolation ──────────────────────────────────────────────

def lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

def lerp_frame(f1: Image.Image, f2: Image.Image, t: float) -> Image.Image:
    """Crossfade between two frames (0=full f1, 1=full f2)."""
    return Image.blend(f1, f2, t)


# ── Main ─────────────────────────────────────────────────────────────

def make_traversal_gif(seed: int, output: str, size: int = 400,
                        fps: int = 1, seconds_per_zone: int = 3,
                        transition_frames: int = 8):
    """Generate a traversal GIF from an oracle seed."""
    path = oracle.traverse(seed)
    total_steps = len(path)

    # Load font
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
                                        max(11, size // 28))
        font_small = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf",
                                        max(8, size // 36))
    except OSError:
        font_title = ImageFont.load_default()
        font_small = font_title

    frames = []
    delays = []

    for step, zid in enumerate(path):
        # Hold frame
        f_hold = render_frame(zid, size, seed, step + 1, total_steps,
                              font_title, font_small)
        hold_ms = int(1000 / fps * seconds_per_zone)
        frames.append(f_hold)
        delays.append(hold_ms)

        # Transition to next zone
        if step < total_steps - 1:
            next_zid = path[step + 1]
            f_next = render_frame(next_zid, size, seed, step + 2, total_steps,
                                  font_title, font_small)
            trans_ms = int(1000 / fps * 0.5)  # 0.5s per transition
            n_trans = transition_frames
            for i in range(1, n_trans + 1):
                t = i / (n_trans + 1)
                frames.append(lerp_frame(f_hold, f_next, t))
                delays.append(trans_ms // n_trans)

    # Final hold (longer pause)
    for _ in range(fps * 2):
        frames.append(frames[-1])
        delays.append(1000 // fps)

    # Save GIF
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=delays,
        loop=0,
        disposal=2,
        optimize=False,
    )
    return output


def main():
    parser = argparse.ArgumentParser(description="Pixel-art traversal GIF generator")
    parser.add_argument("seed", type=int, help="Oracle seed")
    parser.add_argument("output", nargs="?", default=None, help="Output GIF path")
    parser.add_argument("--size", type=int, default=400, help="Frame size (px)")
    parser.add_argument("--fps", type=int, default=1, help="Base framerate")
    parser.add_argument("--duration", type=float, default=3,
                        help="Seconds per zone hold")
    args = parser.parse_args()

    out = args.output or f"/tmp/oracle_pixel_{args.seed}.gif"
    out = make_traversal_gif(args.seed, out, size=args.size,
                              fps=args.fps, seconds_per_zone=args.duration)
    print(f"Wrote {out}")
    print(f"  oracle.py --traverse {args.seed}:",
          " → ".join(f"Z{z}" for z in oracle.traverse(args.seed)))


if __name__ == "__main__":
    main()