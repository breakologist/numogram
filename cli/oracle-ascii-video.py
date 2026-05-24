#!/usr/bin/env python3
# oracle-ascii-video.py — Minimal ascii-video oracle pipeline
#
# Converts an oracle traversal (zone sequence) into an animated ASCII GIF.
# Each zone step becomes one frame: density ramp characters coloured to the
# zone's tty colour, with a metadata strip at the top.
#
# Usage:
#   python3 oracle-ascii-video.py 174                  → /tmp/oracle_174.gif
#   python3 oracle-ascii-video.py 174 /path/out.gif
#
# Inputs oracle.py from the numogram cli directory.
# Dependencies: numpy, pillow (imageio is optional for GIF save; PIL alone
# is sufficient via save_all).

import sys
import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ── Add numogram cli to path ─────────────────────────────────────────
HERE = os.path.dirname(os.path.abspath(__file__))
ORACLE_DIR = os.path.expanduser("~/numogram/cli")
if ORACLE_DIR not in sys.path:
    sys.path.insert(0, ORACLE_DIR)
import oracle                          # the live numogram oracle

# ── Zone metadata (mirrors oracle.py ZONES + _ZONE_TTY_RGB) ──────────────────
ZONES   = oracle.ZONES
ZONE_RGB = oracle._ZONE_TTY_RGB

# ── Character ramps — 10 per zone, density + symbolism ──────────────────────
CHAR_RAMPS = {
    0: list(" .:-+*#") + ["█"],
    1: list(".,:;!i|"),
    2: list(" ./\\-_"),
    3: list("<>()[]{}|\\"),
    4: list("/\\/\\—–"),
    5: list("░▒▓█"),
    6: list("─│┌┐└┘"),
    7: list("▲►▼◄▶▬"),
    8: list("·•○●◌"),
    9: list("░▓█▌▐"),
}

# ── Noise helpers ────────────────────────────────────────────────────────────
_FBM_PRIME1 = 12.9898
_FBM_PRIME2 = 78.233
_MAGIC      = 43758.5453

def hash_seq(seed: int) -> random.Random:
    return random.Random(seed)

def noise_fbm(x, y, seed, octaves: int = 3) -> float:
    """Fractional Brownian motion via sine-hash (no numpy rng needed)."""
    rng = hash_seq(seed)
    v = 0.0
    a  = 0.55
    fx = 1.0
    for _ in range(octaves):
        sx = x * fx + rng.random() * 9.18
        sy = y * fx + rng.random() * 6.18
        v += a * (math.sin(sx * _FBM_PRIME1 + sy * _FBM_PRIME2) * _MAGIC) % 1.0
        a  *= 0.5
        fx *= 2.0
    return v % 1.0

# ── Render ───────────────────────────────────────────────────────────────────
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

def render_frame(zone: int, step: int, zone_name: str,
                 seed: int, t: float, W: int, H: int,
                 font: ImageFont.FreeTypeFont) -> Image.Image:
    """Render one zone step as a coloured ASCII-pattern frame."""
    # Cell size from font
    m = font.getmetrics()
    cell_h = (m[0] + m[1]) if m else 14
    cell_w = max(1, int(cell_h * 0.48))

    rows = H // cell_h
    cols = W // cell_w

    ramp = CHAR_RAMPS.get(zone, list("·:-=+*█*:-."))
    ramp_len = len(ramp)

    ns    = zone * 13 + step * 7 + seed          # noise seed per step
    draw  = ImageDraw.Draw(Image.new("RGB", (1, 1)))  # dummy; create new below
    img   = Image.new("RGB", (W, H), (6, 6, 10))
    draw  = ImageDraw.Draw(img)

    zr, zg, zb = ZONE_RGB.get(zone, (180, 180, 180))

    for ry in range(rows):
        for cx in range(cols):
            n = noise_fbm(cx * 0.13, ry * 0.13, ns + cx * 11 + ry * 37)
            idx = int(n * (ramp_len - 1))
            idx = max(0, min(ramp_len - 1, idx))
            ch  = ramp[idx]
            # Colour brightness modulated by field value
            r = int(zr * (0.35 + 0.65 * n))
            g = int(zg * (0.35 + 0.65 * n))
            b = int(zb * (0.35 + 0.65 * n))
            draw.text((cx * cell_w, ry * cell_h), ch, font=font, fill=(r, g, b))

    # Strip at top: zone label + metadata
    n   = zone * 13 + step * 7 + seed
    rng = hash_seq(n)
    bar_h = cell_h + 8
    draw.rectangle([0, 0, W, bar_h], fill=(10, 10, 16))
    label = f"  {zone_name}  seed:{seed}  step:{step}"
    draw.text((4, 3), label, font=font, fill=(zr, zg, zb))

    return img

# ── Tonal map (from ascii-video spec; never use linear multipliers) ───────────
def tonemap(canvas: np.ndarray, gamma: float = 0.75) -> np.ndarray:
    f = canvas.astype(np.float32)
    lo, hi = np.percentile(f[::4, ::4], [1, 99.5])
    if hi - lo < 10:
        hi = lo + 10
    f = np.clip((f - lo) / (hi - lo), 0, 1) ** gamma
    return (f * 255).astype(np.uint8)

# ── ENCODE ───────────────────────────────────────────────────────────────────
def render_gif(zone_path: list[int], seed: int, out_path: str,
               W: int = 720, H: int = 400, fps: int = 1) -> None:
    font = _load_font(11)
    zone_names = [ZONES[z] for z in zone_path]
    frames = []
    total  = max(1, len(zone_path) - 1)

    for step, zone in enumerate(zone_path):
        img   = render_frame(zone, step, zone_names[step], seed,
                             step / total, W, H, font)
        frame = tonemap(np.array(img))
        frames.append(Image.fromarray(frame))

    frames[0].save(
        out_path, save_all=True, append_images=frames[1:],
        duration=1000 // fps, loop=0, optimize=True,
    )
    print(f"Saved {len(frames)}-frame GIF → {out_path}")

# ── CLI ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 174
    out  = sys.argv[2] if len(sys.argv) > 2 else f"/tmp/oracle_{seed}.gif"
    path = oracle.traverse(seed, steps=8)
    render_gif(path, seed, out)
