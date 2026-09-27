import os
import sys
import json
import time
import base64
import urllib.request
import urllib.error
from PIL import Image, ImageDraw, ImageFont

ROUTER_URL = "http://127.0.0.1:20128/v1/images/generations"
API_KEY = "Bearer sk-c4f2444795b190b3-kzvd4h-ea839762"
MODEL = "cx/gpt-5.5-image"

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAROUSEL_DIR = os.path.join(PROJECT_ROOT, "assets", "episode9_father_parenting", "carousel")
os.makedirs(CAROUSEL_DIR, exist_ok=True)

SLIDES = [
    {
        "index": 1,
        "filename": "slide_1_cover_atm_myth.png",
        "prompt": "Warm clean editorial illustration of a thoughtful modern father walking with his cheerful toddler in a cozy sunny park, modern minimalist aesthetic, warm pastel tones, bright lighting, high resolution, 8k",
        "tag": "PARENTING DOSSIER #09",
        "kicker": "THE CRITICAL FLAW",
        "title": "THE 'ATM DAD' ILLUSION",
        "subtitle": "Why providing money is only 20% of fatherhood—and what developmental neuroscience says about the other 80%."
    },
    {
        "index": 2,
        "filename": "slide_2_paternal_brain.png",
        "prompt": "Cute charming editorial illustration of a gentle smiling dad bottle feeding his peaceful baby with glowing warmth and soft heart symbols, clean bright modern art style, warm cozy lighting, pastel sage and honey tones, high resolution, 8k",
        "tag": "YALE CHILD STUDY CENTER",
        "kicker": "PATERNAL NEUROBIOLOGY",
        "title": "YOUR BRAIN REWIRES",
        "subtitle": "When dads bathe, hold, and put their kids to sleep, Oxytocin surges +140%—matching new mothers and igniting empathy circuits."
    },
    {
        "index": 3,
        "filename": "slide_3_rough_play.png",
        "prompt": "Joyful energetic editorial illustration of a laughing father playfully tossing his toddler in the air in a bright modern living room, dynamic happy movement, warm sunlight through window, modern editorial storybook style, high resolution, 8k",
        "tag": "HARVARD DEVELOPMENT DATA",
        "kicker": "ROUGH-AND-TUMBLE PLAY",
        "title": "PLAY BUILDS RESILIENCE",
        "subtitle": "Wrestling on the carpet trains the prefrontal cortex: active physical play with dad boosts stress resilience by +40%."
    },
    {
        "index": 4,
        "filename": "slide_4_prophetic_adab.png",
        "prompt": "Warm elegant traditional Islamic artistic illustration of a gentle father holding his happy young child's hand walking towards a luminous tranquil courtyard with olive trees and glowing lantern light, serene peaceful atmosphere, warm terracotta and sage green, high resolution, 8k",
        "tag": "SAHIH BUKHARI 5996 & 5997",
        "kicker": "PROPHETIC TRADITION",
        "title": "AR-RA'I: SHEPHERD OF SOULS",
        "subtitle": "The Prophet ﷺ carried his grandkids during prayer, shattering toxic stoicism: 'Whoever does not show mercy, will not receive mercy.'"
    },
    {
        "index": 5,
        "filename": "slide_5_lifetime_presence.png",
        "prompt": "Heartwarming emotional editorial illustration of a loving father giving a tight protective hug to his smiling daughter, warm cozy knitted sweaters, soft golden hour light, touching family moment, clean modern editorial style, high resolution, 8k",
        "tag": "THE FINAL VERDICT",
        "kicker": "THE LIFETIME RECORD",
        "title": "WHAT THEY REMEMBER",
        "subtitle": "Decades later, your kids won't recall your bank statements. Their nervous system forever remembers your warm hand when they were afraid."
    }
]

def generate_slide_image(slide):
    raw_path = os.path.join(CAROUSEL_DIR, f"raw_{slide['filename']}")
    final_path = os.path.join(CAROUSEL_DIR, slide["filename"])

    if os.path.exists(final_path):
        print(f"[Skip] {slide['filename']} already exists.")
        return True

    if os.path.exists(raw_path):
        print(f"[Composite] Using cached raw image for Slide {slide['index']}...")
        create_editorial_slide(raw_path, final_path, slide)
        return True

    print(f"\n[Generate] Slide {slide['index']}: {slide['title']}...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": API_KEY,
        "User-Agent": "BangMotion/1.0"
    }
    payload = {
        "model": MODEL,
        "prompt": slide["prompt"],
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
                        with open(raw_path, "wb") as f:
                            f.write(img_bytes)

                        # Create editorial composite
                        create_editorial_slide(raw_path, final_path, slide)
                        print(f"[OK] Slide {slide['index']} finalized: {final_path}")
                        return True
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            time.sleep(3)
    return False

def create_editorial_slide(raw_img_path, final_path, slide):
    # Canvas: 1080 x 1350 (Instagram portrait / TikTok carousel 4:5 ratio)
    W, H = 1080, 1350
    canvas = Image.new("RGB", (W, H), "#FAF8F4")
    draw = ImageDraw.Draw(canvas)

    # Paste generated artwork (cropped to 1000 x 780 with rounded corners)
    art = Image.open(raw_img_path).convert("RGB")
    art_w, art_h = 1000, 780
    art = art.resize((art_w, int(art.height * (art_w / art.width))), Image.LANCZOS)
    # Center crop
    crop_y = max(0, (art.height - art_h) // 2)
    art_cropped = art.crop((0, crop_y, art_w, crop_y + art_h))

    # Mask with rounded corners
    mask = Image.new("L", (art_w, art_h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, 0, art_w, art_h), radius=28, fill=255)

    art_x = (W - art_w) // 2
    art_y = 120
    canvas.paste(art_cropped, (art_x, art_y), mask)

    # Thin border around artwork
    draw.rounded_rectangle((art_x, art_y, art_x + art_w, art_y + art_h), radius=28, outline="#E5E0D8", width=2)

    # Top Bar: Tag & Page Number (e.g. 01 / 05)
    try:
        font_tag = ImageFont.truetype("arialbd.ttf", 20)
        font_page = ImageFont.truetype("arialbd.ttf", 22)
        font_kicker = ImageFont.truetype("arialbd.ttf", 22)
        font_title = ImageFont.truetype("arialbd.ttf", 44)
        font_sub = ImageFont.truetype("arial.ttf", 28)
    except Exception:
        font_tag = font_page = font_kicker = font_title = font_sub = ImageFont.load_default()

    # Draw Top Header
    draw.text((art_x + 6, 60), slide["tag"].upper(), fill="#264653", font=font_tag)
    page_text = f"0{slide['index']} / 05"
    draw.text((art_x + art_w - 90, 60), page_text, fill="#E76F51", font=font_page)

    # Bottom Editorial Text Box (art_y + art_h + 30 = 930)
    text_y = art_y + art_h + 40
    # Kicker
    draw.text((art_x + 6, text_y), slide["kicker"].upper(), fill="#E76F51", font=font_kicker)

    # Title
    draw.text((art_x + 6, text_y + 36), slide["title"], fill="#181A1E", font=font_title)

    # Subtitle wrapping
    words = slide["subtitle"].split()
    lines = []
    cur_line = []
    for word in words:
        cur_line.append(word)
        test_line = " ".join(cur_line)
        bbox = draw.textbbox((0, 0), test_line, font=font_sub)
        if (bbox[2] - bbox[0]) > (art_w - 20):
            cur_line.pop()
            lines.append(" ".join(cur_line))
            cur_line = [word]
    if cur_line:
        lines.append(" ".join(cur_line))

    sub_y = text_y + 104
    for line in lines:
        draw.text((art_x + 6, sub_y), line, fill="#565C69", font=font_sub)
        sub_y += 40

    # Bottom swipe indicator
    swipe_text = "SWIPE TO READ  →" if slide["index"] < 5 else "SAVE & SHARE WITH A DAD  ♥"
    draw.text((art_x + 6, H - 70), swipe_text, fill="#848B98", font=font_tag)

    canvas.save(final_path, "PNG", quality=95)

def main():
    print(f"--- Generating 5 Editorial Carousel Slides for Episode 9 via 9Router ---")
    success_count = 0
    for slide in SLIDES:
        if generate_slide_image(slide):
            success_count += 1
        time.sleep(1)
    print(f"\n[Finished] {success_count}/{len(SLIDES)} carousel slides ready in {CAROUSEL_DIR}")

if __name__ == "__main__":
    main()
