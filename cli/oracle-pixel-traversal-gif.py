#!/usr/bin/env python3
"""
oracle-pixel-traversal-gif.py — Pixel-art oracle traversal GIF.

Takes a seed, runs oracle.traverse() to get an 8-step zone path, then
generates an animated GIF showing each zone's pixel-art sprite with
smooth crossfade transitions. The palette migration between hardware
eras IS the reading — you watch the world change colour as the oracle
descends through the zones.

Usage:
    python3 oracle-pixel-traversal-gif.py 174
    python3 oracle-pixel-traversal-gif.py 174 /tmp/traversal.gif
    python3 oracle-pixel-traversal-gif.py 174 --steps 12
    python3 oracle-pixel-traversal-gif.py --zones 3 1 2 5 8

Output: 8-step GIF with crossfades, metadata overlay per step.
"""

import sys, os, math, argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ── Path to oracle ────────────────────────────────────────────────────
ORACLE_DIR = os.path.expanduser("~/numogram/cli")
if ORACLE_DIR not in sys.path:
    sys.path.insert(0, ORACLE_DIR)
import oracle

# ── Zone metadata ─────────────────────────────────────────────────────
ZONES = oracle.ZONES
ZONE_RGB = oracle._ZONE_TTY_RGB

ZONE_HW_PALETTE = {
    0: "MONO_AMBER", 1: "GAMEBOY_ORIGINAL", 2: "GAMEBOY_POCKET",
    3: "C64", 4: "ZX_SPECTRUM", 5: "APPLE_II_HI", 6: "TELETEXT",
    7: "GAMEBOY_VIRTUALBOY", 8: "APPLE_II_LO", 9: "PICO_8",
}

PALETTE_ERAS = {
    "MONO_AMBER": "1970s amber CRT",
    "GAMEBOY_ORIGINAL": "1989 Nintendo",
    "GAMEBOY_POCKET": "1996 monochrome",
    "C64": "1982 Commodore",
    "ZX_SPECTRUM": "1982 Sinclair",
    "APPLE_II_HI": "1978 Apple hi-res",
    "TELETEXT": "1970s broadcast",
    "GAMEBOY_VIRTUALBOY": "1995 red-stereo",
    "APPLE_II_LO": "1978 Apple lo-res",
    "PICO_8": "2015 fantasy console",
}

# ── Sprite paths ──────────────────────────────────────────────────────
SPRITE_DIRS = [
    os.path.expanduser("~/numogram/docs/wiki/assets/zone-sprites"),
    os.path.expanduser("~/.hermes/obsidian/hermetic/wiki/assets/zone-sprites"),
]

def _find_sprite_dir():
    for d in SPRITE_DIRS:
        if os.path.isdir(d):
            return d
    return SPRITE_DIRS[0]

def load_sprite(zone: int, size: int = 256) -> Image.Image:
    """Load and resize a zone pixel-art sprite."""
    d = _find_sprite_dir()
    path = os.path.join(d, f"zone-{zone}-sprite.png")
    if not os.path.exists(path):
        # Fallback: generate a coloured placeholder
        rgb = ZONE_RGB.get(zone, (128, 128, 128))
        img = Image.new("RGB", (size, size), rgb)
        return img
    img = Image.open(path).convert("RGB")
    return img.resize((size, size), Image.NEAREST)


# ── Font loading ──────────────────────────────────────────────────────
def _load_font(size: int = 11) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansMono-Regular.ttf",
        "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


# ── Frame rendering ───────────────────────────────────────────────────
def render_zone_frame(zone: int, step: int, seed: int,
                      sprite_size: int, canvas_size: int,
                      font: ImageFont.FreeTypeFont,
                      font_lg: ImageFont.FreeTypeFont) -> Image.Image:
    """Render one full frame showing the zone sprite + metadata overlay."""
    sz = sprite_size
    frame = Image.new("RGB", (canvas_size, canvas_size), (6, 6, 10))
    draw = ImageDraw.Draw(frame)

    # Position sprite centered
    ox = (canvas_size - sz) // 2
    oy = (canvas_size - sz) // 2 - 20  # shift up slightly for metadata bar

    sprite = load_sprite(zone, sz)
    frame.paste(sprite, (ox, oy))

    zr, zg, zb = ZONE_RGB.get(zone, (180, 180, 180))
    pal = ZONE_HW_PALETTE.get(zone, "?")
    era = PALETTE_ERAS.get(pal, "")
    zname = ZONES[zone] if isinstance(ZONES, list) else ZONES[zone] if isinstance(ZONES, dict) else f"Zone {zone}"

    # Dark overlay bar at top
    bar_h = 28
    draw.rectangle([0, 0, canvas_size, bar_h], fill=(8, 8, 12))
    # Zone label
    label = f"Z{zone} · {zname}"
    draw.text((10, 4), label, font=font_lg, fill=(zr, zg, zb))

    # Right align: seed + step
    step_text = f"seed:{seed}  step:{step+1}/8"
    tw = draw.textlength(step_text, font=font)
    draw.text((canvas_size - tw - 10, 6), step_text, font=font, fill=(100, 100, 100))

    # Bottom bar: palette + era
    draw.rectangle([0, canvas_size - 22, canvas_size, canvas_size], fill=(8, 8, 12))
    pal_text = f"{pal} · {era}"
    draw.text((10, canvas_size - 18), pal_text, font=font, fill=(zr, zg, zb))

    # Gate/current info bottom-right
    # Use oracle's gate data
    gate_val = sum(range(1, zone + 1)) if zone > 0 else 0
    gate_text = f"Gt-{gate_val}  c={abs(ZONE_RGB.get(zone, (1,1,1))[0]) % 9 + 1}"
    tw2 = draw.textlength(gate_text, font=font)
    draw.text((canvas_size - tw2 - 10, canvas_size - 18), gate_text, font=font, fill=(80, 80, 80))

    return frame


def blend_frames(f1: Image.Image, f2: Image.Image, steps: int = 8) -> list[Image.Image]:
    """Create a smooth crossfade between two frames."""
    frames = []
    for i in range(steps):
        t = (i + 1) / (steps + 1)
        blend = Image.blend(f1, f2, t)
        frames.append(blend)
    return frames


# ── Merge frames with crossfade ──────────────────────────────────────
def compose(zone_path: list[int], seed: int,
            canvas_size: int = 400, sprite_size: int = 300,
            fps: int = 2, fade_steps: int = 6) -> list[Image.Image]:
    """Generate all frames for the GIF: hold + crossfade per zone step."""
    font = _load_font(10)
    font_lg = _load_font(13)

    all_frames = []
    total = len(zone_path)

    for step, zone in enumerate(zone_path):
        # Render the zone frame
        frame = render_zone_frame(zone, step, seed,
                                   sprite_size, canvas_size,
                                   font, font_lg)

        # Hold frame (stay on this zone for N frames)
        hold_frames = fps  # 1 second hold
        for _ in range(hold_frames):
            all_frames.append(frame)

        # Crossfade to next zone (except for the last zone)
        if step < total - 1:
            next_zone = zone_path[step + 1]
            next_frame = render_zone_frame(next_zone, step + 1, seed,
                                            sprite_size, canvas_size,
                                            font, font_lg)
            blended = blend_frames(frame, next_frame, fade_steps)
            all_frames.extend(blended)

    return all_frames


# ── Tonemap ────────────────────────────────────────────────────────────
def tonemap(canvas: np.ndarray, gamma: float = 0.85) -> np.ndarray:
    """Percentile-clamp + gamma; protects against blown highlights."""
    f = canvas.astype(np.float32)
    lo, hi = np.percentile(f[::2, ::2], [0.5, 99.5])
    if hi - lo < 5:
        hi = lo + 5
    f = np.clip((f - lo) / (hi - lo), 0, 1) ** gamma
    return (f * 255).astype(np.uint8)


# ── Main ──────────────────────────────────────────────────────────────
def render_gif(zone_path: list[int], seed: int, out_path: str,
               canvas_size: int = 400, sprite_size: int = 300,
               fps: int = 2, fade_steps: int = 6) -> None:
    """Generate and save the traversal GIF."""
    frames_raw = compose(zone_path, seed, canvas_size, sprite_size, fps, fade_steps)

    # Tonemap each frame
    frames = []
    for f in frames_raw:
        arr = np.array(f)
        tm = tonemap(arr)
        frames.append(Image.fromarray(tm))

    duration_ms = max(50, 1000 // fps // 2)  # half hold, half fade
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=0,
        optimize=True,
    )
    n_zones = len(zone_path)
    n_frames = len(frames)
    dur_sec = n_frames * duration_ms / 1000
    print(f"Saved {n_zones}-zone, {n_frames}-frame GIF ({dur_sec:.1f}s)")
    print(f"→ {out_path}")
    print(f"Zone path: {' → '.join(f'Z{z}' for z in zone_path)}")

    # Print palette sequence
    pals = [ZONE_HW_PALETTE.get(z, "?") for z in zone_path]
    print(f"Palettes:  {' → '.join(pals)}")


def main():
    parser = argparse.ArgumentParser(description="Pixel-art oracle traversal GIF")
    parser.add_argument("seed", nargs="?", type=int, default=None,
                        help="Oracle seed for traversal (omit to use --zones)")
    parser.add_argument("output", nargs="?", default=None,
                        help="Output GIF path")
    parser.add_argument("--zones", nargs="*", type=int, default=None,
                        help="Explicit zone path (overrides seed)")
    parser.add_argument("--steps", type=int, default=8,
                        help="Number of traversal steps (default: 8)")
    parser.add_argument("--size", type=int, default=400,
                        help="Canvas size in pixels (default: 400)")
    parser.add_argument("--sprite", type=int, default=300,
                        help="Sprite size in pixels (default: 300)")
    parser.add_argument("--fps", type=int, default=2,
                        help="Hold frames per zone (default: 2)")
    parser.add_argument("--fade", type=int, default=6,
                        help="Crossfade frames between zones (default: 6)")
    args = parser.parse_args()

    # Determine zone path
    if args.zones is not None and len(args.zones) > 0:
        zone_path = args.zones
        seed = hash(tuple(args.zones)) % 100000
        if args.seed is not None:
            seed = args.seed
    elif args.seed is not None:
        seed = args.seed
        zone_path = oracle.traverse(seed, steps=args.steps)
    else:
        # Default demo seed
        seed = 174
        zone_path = oracle.traverse(seed, steps=args.steps)

    if args.output:
        out_path = args.output
    else:
        path_str = "".join(str(z) for z in zone_path[:4])
        out_path = f"/tmp/oracle_pixel_{seed}_{path_str}.gif"

    render_gif(zone_path, seed, out_path,
               canvas_size=args.size, sprite_size=args.sprite,
               fps=args.fps, fade_steps=args.fade)


if __name__ == "__main__":
    main()