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

NEW_ISLAMIC_SPRITES = [
    {
        "filename": "sprite_islamic_dad_atm_faceless.png",
        "prompt": "Faceless Islamic cartoon illustration of a father wearing a modern olive-green koko shirt and white kufi cap with a neat trimmed beard, having an ATM cash dispenser machine on his chest with banknotes flying out, sad droopy mouth, strictly NO eyes and NO nose (completely smooth blank face except for the mouth expression), fun modern flat vector sticker cutout, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_flying_money_fun.png",
        "prompt": "Fun cartoon flying dollar bills with cute tiny white wings and scattered golden coins, playful finance icon, clean vector sticker cutout, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_islamic_dad_babycare_faceless.png",
        "prompt": "Faceless Islamic editorial illustration of a caring father wearing a warm knit sweater and white kufi cap with a neat beard, tenderly cradling and feeding his cute swaddled baby with a milk bottle, both father and baby have NO eyes and NO nose, strictly blank smooth face with ONLY gentle happy smiling mouths, warm cozy pastel tones, clean vector sticker cutout, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_floating_empathy_hearts.png",
        "prompt": "Cluster of floating warm golden and coral love hearts with glowing sparkle stars and tiny chemical bond sparkles, cute neuroscience empathy icon, clean vector sticker cutout, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_islamic_dad_airplane_faceless.png",
        "prompt": "Dynamic energetic Islamic illustration of a joyful father in casual shirt and white kufi cap tossing his laughing toddler boy wearing a small kufi cap in the air playing airplane, both characters are strictly faceless with NO eyes and NO nose, showing ONLY happy wide open laughing mouths, dynamic play pose, clean vector sticker cutout, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_resilience_badge_40.png",
        "prompt": "Fun vibrant gamified badge emblem with a golden shield, lightning bolts, and bold text '+40% RESILIENCE', playful cartoon achievement sticker, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_islamic_dad_prayer_faceless.png",
        "prompt": "Touching faceless Islamic illustration of a father wearing a clean white thobe and kufi cap carrying his happy toddler boy on his shoulders during prayer time, both characters have strictly NO eyes and NO nose, showing ONLY sweet smiling mouths, tranquil warm sage and gold palette, clean vector sticker cutout, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_islamic_dad_hug_faceless.png",
        "prompt": "Heartwarming faceless Islamic illustration of a loving father in a warm knitted sweater and kufi cap hugging his smiling young daughter who wears a cute pastel pink hijab, both characters have strictly NO eyes and NO nose, displaying ONLY a warm gentle smiling mouth, touching emotional bond, clean vector sticker cutout, isolated on pure white background, no shadows"
    },
    {
        "filename": "sprite_warm_holding_hands.png",
        "prompt": "Stylized heartwarming illustration of a large warm father's hand securely holding a tiny child's hand, surrounded by a soft golden aura of safety and love, symbolic parental presence, clean vector sticker cutout, isolated on pure white background, no shadows"
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
    print(f"--- Generating {len(NEW_ISLAMIC_SPRITES)} Faceless Islamic Sprites via 9Router ---")
    success_count = 0
    for spec in NEW_ISLAMIC_SPRITES:
        if generate_sprite(spec):
            success_count += 1
        time.sleep(1)
    print(f"\n[Finished] {success_count}/{len(NEW_ISLAMIC_SPRITES)} sprites ready in {TARGET_DIR}")

if __name__ == "__main__":
    main()
