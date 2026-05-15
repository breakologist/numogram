#!/usr/bin/env python3
"""numogram-zone-wallpapers.py — Generate zone-themed wallpapers via ComfyUI API.

Usage:
    python3 numogram-zone-wallpapers.py          # Generate all 10 zones
    python3 numogram-zone-wallpapers.py 6         # Generate single zone
    python3 numogram-zone-wallpapers.py 0 3 6 9   # Generate specific zones
"""

import json
import sys
import time
import urllib.request
import urllib.error
import shutil
import os

COMFYUI_URL = "http://localhost:8188"
CHECKPOINT = "Noob/NoobAI-XL-v1.1.safetensors"
VAE = "sdxl_vae.safetensors"
OUTPUT_DIR = os.path.expanduser("~/Pictures/Wall/zones")
WIDTH = 1920
HEIGHT = 1080

ZONE_PROMPTS = {
    0: {
        "positive": "abstract void, pure black background, faint geometric lattice emerging from darkness, mathematical grid, negative space, minimalist, dark aesthetic, high contrast, 8k wallpaper",
        "negative": "colorful, bright, busy, cluttered, text, watermark, signature, anime girl, character, person"
    },
    1: {
        "positive": "electric blue fractals radiating outward, first movement, surge of energy, lightning patterns, fibonacci spirals, dynamic motion, sci-fi aesthetic, dark background, 8k wallpaper",
        "negative": "still, static, flat, text, watermark, signature, anime girl, character, person, cluttered"
    },
    2: {
        "positive": "doubling spirals, amber and gold tones, recursive patterns, infinite regression, mirror symmetry, warm light, mathematical art, dark background, 8k wallpaper",
        "negative": "text, watermark, signature, anime girl, character, person, busy, cluttered"
    },
    3: {
        "positive": "triangular traps, green and ochre geometry, overlapping triangles, tessellation, sacred geometry, earth tones, mathematical precision, dark background, 8k wallpaper",
        "negative": "text, watermark, signature, anime girl, character, person, soft, rounded"
    },
    4: {
        "positive": "walls within walls, grey brutalist architecture, impossible rooms, escher-like structure, concrete textures, perspective tricks, cold tones, 8k wallpaper",
        "negative": "text, watermark, signature, anime girl, character, person, warm colors, organic"
    },
    5: {
        "positive": "hidden center, concentric rings, deep purple and silver, ripples in still water, mandala, focal point, meditative, cosmic, dark background, 8k wallpaper",
        "negative": "text, watermark, signature, anime girl, character, person, chaotic, busy"
    },
    6: {
        "positive": "rotational symmetry, violet and teal vortex, hinge mechanism, gears and spirals, bifurcation, quantum aesthetic, dark background, 8k wallpaper",
        "negative": "text, watermark, signature, anime girl, character, person, static, flat"
    },
    7: {
        "positive": "clean geometric cuts, red and black division, sharp lines, bisection, surgical precision, high contrast, minimalist, dark background, 8k wallpaper",
        "negative": "text, watermark, signature, anime girl, character, person, soft edges, blurry"
    },
    8: {
        "positive": "infinite spiral descent, deep blue and indigo, vertigo perspective, helix structure, depth illusion, cosmic tunnel, dark background, 8k wallpaper",
        "negative": "text, watermark, signature, anime girl, character, person, flat, shallow"
    },
    9: {
        "positive": "maximal density, all colors tangling, plex abyss, interwoven currents, everything at once, fractal complexity, rich texture, dark background, 8k wallpaper",
        "negative": "text, watermark, signature, anime girl, character, person, minimalist, empty"
    }
}


def build_workflow(zone_num: int) -> dict:
    """Build a ComfyUI API workflow for zone wallpaper generation."""
    prompts = ZONE_PROMPTS[zone_num]
    seed = int(time.time() * 1000) % (2**53)

    return {
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
                "steps": 36,
                "cfg": 7.0,
                "sampler_name": "euler_ancestral",
                "scheduler": "sgm_uniform",
                "denoise": 1.0,
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0]
            }
        },
        "4": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": CHECKPOINT
            }
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": WIDTH,
                "height": HEIGHT,
                "batch_size": 1
            }
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": prompts["positive"],
                "clip": ["4", 1]
            }
        },
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": prompts["negative"],
                "clip": ["4", 1]
            }
        },
        "8": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["3", 0],
                "vae": ["9", 0]
            }
        },
        "9": {
            "class_type": "VAELoader",
            "inputs": {
                "vae_name": VAE
            }
        },
        "10": {
            "class_type": "SaveImage",
            "inputs": {
                "filename_prefix": f"zone{zone_num}",
                "images": ["8", 0]
            }
        }
    }


def queue_prompt(workflow: dict) -> str:
    """Queue a workflow and return prompt_id."""
    data = json.dumps({"prompt": workflow}).encode("utf-8")
    req = urllib.request.Request(
        f"{COMFYUI_URL}/prompt",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    return result["prompt_id"]


def wait_for_completion(prompt_id: str, timeout: int = 300) -> dict:
    """Wait for a prompt to finish, return history."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(f"{COMFYUI_URL}/history/{prompt_id}") as resp:
                history = json.loads(resp.read())
                if prompt_id in history:
                    return history[prompt_id]
        except Exception:
            pass
        time.sleep(2)
    raise TimeoutError(f"Prompt {prompt_id} did not complete within {timeout}s")


def get_output_images(history: dict) -> list:
    """Extract output image paths from history."""
    images = []
    for node_id, outputs in history.get("outputs", {}).items():
        for image_data in outputs.get("images", []):
            images.append({
                "filename": image_data["filename"],
                "subfolder": image_data.get("subfolder", ""),
                "type": image_data.get("type", "output")
            })
    return images


def download_image(image_info: dict, dest_path: str):
    """Download image from ComfyUI to local path."""
    params = f"filename={image_info['filename']}&type={image_info['type']}"
    if image_info['subfolder']:
        params += f"&subfolder={image_info['subfolder']}"
    url = f"{COMFYUI_URL}/view?{params}"
    with urllib.request.urlopen(url) as resp:
        with open(dest_path, "wb") as f:
            shutil.copyfileobj(resp, f)


def generate_zone(zone_num: int):
    """Generate a wallpaper for a single zone."""
    print(f"Generating Zone {zone_num}...")

    workflow = build_workflow(zone_num)
    prompt_id = queue_prompt(workflow)
    print(f"  Queued: {prompt_id}")

    history = wait_for_completion(prompt_id)
    images = get_output_images(history)

    if not images:
        print(f"  ERROR: No output images for zone {zone_num}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for img in images:
        ext = os.path.splitext(img['filename'])[1]
        dest = os.path.join(OUTPUT_DIR, f"zone{zone_num}{ext}")
        download_image(img, dest)
        print(f"  Saved: {dest}")


def main():
    zones = list(range(10))
    if len(sys.argv) > 1:
        zones = [int(z) for z in sys.argv[1:]]

    print(f"Numogram Zone Wallpaper Generator")
    print(f"ComfyUI: {COMFYUI_URL}")
    print(f"Checkpoint: {CHECKPOINT}")
    print(f"Resolution: {WIDTH}x{HEIGHT}")
    print(f"Zones: {zones}")
    print()

    for zone in zones:
        generate_zone(zone)
        print()

    print("Done. Wallpapers saved to:")
    print(f"  {OUTPUT_DIR}")
    print()
    print("To use as wallpapers, copy to ~/Pictures/Wall/:")
    print(f"  cp {OUTPUT_DIR}/zone*.png ~/Pictures/Wall/")


if __name__ == "__main__":
    main()
