import os
import sys
import json
import time
import base64
import urllib.request
import urllib.error
import numpy as np
from PIL import Image

ROUTER_URL = "http://127.0.0.1:20128/v1/images/generations"
API_KEY = "Bearer sk-c4f2444795b190b3-kzvd4h-ea839762"
MODEL = "cx/gpt-5.5-image"

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_DIR = os.path.join(PROJECT_ROOT, "assets", "episode14_glymphatic_brain_wash", "sprites")
os.makedirs(TARGET_DIR, exist_ok=True)

SPRITES = [
    {
        "filename": "sprite_bioluminescent_brain.png",
        "prompt": "High-end biomedical scientific illustration of a human brain sagittal cross-section glowing with deep bioluminescent cyan and cerulean fluid channels, cerebral cortex illuminated, microscopic interstitial channels glowing softly, clean modern vector sticker cutout style, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_star_astrocyte_aquaporin.png",
        "prompt": "High-end biological illustration of a single star-shaped astrocyte glial cell with glowing branching endfeet, radiating aquaporin-4 water channel pores, glowing neon cyan and electric aquamarine, clean modern vector sticker cutout, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_toxic_amyloid_clusters.png",
        "prompt": "Biomedical scientific illustration of microscopic toxic protein aggregates (Beta-Amyloid and Tau neurofibrillary tangles) in glowing crimson red and coral amber, dissolving at the edges into tiny dust motes, clean vector sticker cutout, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_sleep_delta_gauge.png",
        "prompt": "Futuristic medical telemetry gauge emblem of Slow-Wave NREM Delta sleep cycle, showing 0.5 to 4 Hz synchronized brainwaves and 60% interstitial expansion meter, sleek dark navy and glowing cyan holographic badge, clean vector sticker cutout, isolated on pure white background, no shadows"
    }
]

def make_transparent_cutout(img):
    img = img.convert("RGBA")
    arr = np.array(img, dtype=np.float32)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

    brightness = (r + g + b) / 3.0
    is_white = (r > 240) & (g > 240) & (b > 240)
    arr[is_white, 3] = 0

    is_near_white = (brightness > 218) & (~is_white)
    alpha_scale = np.clip((240.0 - brightness) / 22.0, 0.0, 1.0)
    arr[is_near_white, 3] = arr[is_near_white, 3] * alpha_scale[is_near_white]

    return Image.fromarray(arr.astype(np.uint8), "RGBA")

def generate_sprite(spec):
    out_path = os.path.join(TARGET_DIR, spec["filename"])
    if os.path.exists(out_path):
        print(f"[Skip] {spec['filename']} already exists.")
        return True

    print(f"\n[Generate] Generating {spec['filename']} via 9Router ({MODEL})...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": API_KEY,
        "User-Agent": "BangMotion/1.0"
    }
    payload = {
        "model": MODEL,
        "prompt": spec["prompt"],
        "n": 1,
        "size": "1024x1024"
    }

    req = urllib.request.Request(ROUTER_URL, data=json.dumps(payload).encode("utf-8"), headers=headers)
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(req, timeout=120) as res:
                data = json.loads(res.read().decode("utf-8"))
                if "data" in data and len(data["data"]) > 0:
                    first = data["data"][0]
                    img_bytes = None
                    if "b64_json" in first:
                        img_bytes = base64.b64decode(first["b64_json"])
                    elif "url" in first:
                        img_bytes = urllib.request.urlopen(first["url"]).read()

                    if img_bytes:
                        raw_path = out_path + ".raw.png"
                        with open(raw_path, "wb") as f:
                            f.write(img_bytes)

                        # Convert white background to transparent alpha cutout
                        raw_img = Image.open(raw_path)
                        cutout = make_transparent_cutout(raw_img)
                        cutout.save(out_path, "PNG")
                        print(f"[Success] Saved transparent sprite: {out_path} ({cutout.size})")
                        return True
        except Exception as e:
            print(f"[Attempt {attempt}/3 Failed] {e}")
            time.sleep(3)

    return False

def main():
    print(f"=== 9Router Sprite Generation for Episode 14 ({len(SPRITES)} sprites) ===")
    for spec in SPRITES:
        success = generate_sprite(spec)
        if not success:
            print(f"[Warning] Failed to generate {spec['filename']}")
        time.sleep(2)

if __name__ == "__main__":
    main()
