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
TARGET_DIR = os.path.join(PROJECT_ROOT, "assets", "episode10_mother_microchimerism", "sprites")
os.makedirs(TARGET_DIR, exist_ok=True)

SPRITES = [
    {
        "filename": "sprite_mother_baby_faceless.png",
        "prompt": "Faceless Islamic editorial illustration of a loving mother wearing a modern sage green hijab tenderly cradling her swaddled newborn baby, both mother and baby have strictly NO eyes and NO nose (completely smooth blank face with ONLY a sweet gentle smiling mouth), warm pastel tones, clean modern vector sticker cutout, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_glowing_fetal_cells.png",
        "prompt": "Cluster of floating glowing bioluminescent golden and emerald green microscopic cells with soft sparkling star particles, cellular microchimerism icon, clean flat vector sticker cutout, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_anatomical_heart_repair.png",
        "prompt": "Minimalist elegant medical anatomical human heart illustration in warm coral and pastel tones, with glowing golden repair node points and tiny cellular sparkles, clean vector sticker cutout, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_grandmother_faceless.png",
        "prompt": "Touching faceless Islamic editorial illustration of an elderly serene grandmother wearing a modest olive-green scarf sitting peacefully, strictly NO eyes and NO nose (completely smooth blank face with ONLY a gentle warm smile), clean modern vector sticker cutout, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_mother_son_prayer_faceless.png",
        "prompt": "Touching faceless Islamic illustration of a grown respectful son in a white koko shirt and black peci holding his smiling mother's hands with deep reverence, mother wearing an ivory hijab, both characters strictly have NO eyes and NO nose (smooth blank faces with ONLY sweet smiling mouths), clean vector sticker cutout, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_holding_mother_hand.png",
        "prompt": "Warm heartwarming illustration of a large caring mother's hand securely embracing a child's hand, surrounded by a soft glowing golden heart aura, clean vector sticker cutout, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_hadith_3x_badge.png",
        "prompt": "Vibrant elegant gold and emerald green emblem badge with bold geometric Arabic style ornament and clean typography text '3X PRIORITY • UMMUKA', gamified achievement sticker, clean vector cutout, isolated on pure white background, no shadows"
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

    print(f"\n[Generate] Generating {spec['filename']}...")
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

                        img = Image.open(raw_path)
                        cutout = make_transparent_cutout(img)
                        cutout.save(out_path, "PNG")
                        print(f"[OK] Saved transparent cutout: {out_path}")
                        return True
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            time.sleep(3)
    return False

def main():
    print(f"--- Generating {len(SPRITES)} Transparent Faceless Islamic Sprites for Episode 10 ---")
    for spec in SPRITES:
        generate_sprite(spec)
        time.sleep(1)
    print("\n[Finished] All transparent sprites ready in:", TARGET_DIR)

if __name__ == "__main__":
    main()
