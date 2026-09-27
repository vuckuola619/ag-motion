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
TARGET_DIR = os.path.join(PROJECT_ROOT, "assets", "episode9_father_parenting", "sprites")
os.makedirs(TARGET_DIR, exist_ok=True)

SPRITE_SPECS = [
    {
        "filename": "sprite_dad_atm_myth.png",
        "prompt": "Fun modern editorial illustration of a sad stressed father depicted with a metallic ATM money dispenser chest and falling dollar bills, stylized cartoon, warm friendly colors, flat clean vector cutout style, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_brain_oxytocin.png",
        "prompt": "Fun colorful cute human brain illustration with glowing heart antennae, oxytocin chemical sparkle icons and floating golden love hearts, cheerful modern editorial sticker style, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_father_babycare.png",
        "prompt": "Charming editorial illustration of a happy caring father gently cradling and feeding his cute baby wrapped in a soft blanket, warm pastel colors, loving expression, clean sticker cutout, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_father_airplane.png",
        "prompt": "Dynamic energetic illustration of a cheerful dad tossing his giggling toddler gently in the air playing airplane, rough-and-tumble active play, joyful expressions, colorful editorial cartoon sticker, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_prophet_sunnah_emblem.png",
        "prompt": "Elegant warm Islamic archival emblem with glowing golden traditional lantern and crescent motif, Ar-Rai shepherd symbol of family care and mercy, green sage and warm amber gold, vector badge cutout, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_father_daughter_hug.png",
        "prompt": "Warm heartwarming illustration of a loving father giving a big gentle hug to his smiling child, cozy warm sweaters, cheerful happy moment, clean modern editorial sticker cutout, isolated on pure white background, no shadows"
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
                    if "b64_json" in first:
                        img_bytes = base64.b64decode(first["b64_json"])
                        raw_path = out_path + ".raw.png"
                        with open(raw_path, "wb") as f:
                            f.write(img_bytes)

                        img = Image.open(raw_path)
                        cutout_img = make_transparent_cutout(img)
                        cutout_img.save(out_path, "PNG")
                        if os.path.exists(raw_path):
                            os.remove(raw_path)
                        print(f"[OK] Saved transparent sprite: {out_path} ({cutout_img.size})")
                        return True
                    elif "url" in first:
                        img_url = first["url"]
                        raw_path = out_path + ".raw.png"
                        urllib.request.urlretrieve(img_url, raw_path)
                        img = Image.open(raw_path)
                        cutout_img = make_transparent_cutout(img)
                        cutout_img.save(out_path, "PNG")
                        if os.path.exists(raw_path):
                            os.remove(raw_path)
                        print(f"[OK] Saved transparent sprite: {out_path} ({cutout_img.size})")
                        return True
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            time.sleep(3)
    return False

def main():
    print(f"--- Generating {len(SPRITE_SPECS)} Transparent Sprites for Episode 9 via 9Router ---")
    success_count = 0
    for spec in SPRITE_SPECS:
        if generate_sprite(spec):
            success_count += 1
        time.sleep(1)
    print(f"\n[Finished] {success_count}/{len(SPRITE_SPECS)} sprites ready in {TARGET_DIR}")

if __name__ == "__main__":
    main()
