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
CAROUSEL_DIR = os.path.join(PROJECT_ROOT, "assets", "episode10_mother_microchimerism", "carousel_full")
os.makedirs(CAROUSEL_DIR, exist_ok=True)

FULL_SLIDES = [
    {
        "index": 1,
        "filename": "slide_1_cover_full_artwork.png",
        "prompt": "Full-bleed cinematic editorial documentary illustration of an affectionate Islamic mother wearing an elegant olive-green hijab tenderly cradling her smiling swaddled newborn baby, strictly NO eyes and NO nose (smooth blank faces with sweet gentle smiling mouths only), surrounded by luminous floating golden bioluminescent microchimerism cells drifting in a tranquil warm sunlit courtyard with Islamic arches, soft warm parchment atmosphere, rich cinematic lighting, masterpiece, 8k",
        "tag": "CELLULAR EPIGENETICS • EPISODE 10",
        "kicker": "THE ETERNAL FOOTPRINT",
        "title": "THE INVISIBLE PASSENGER",
        "subtitle": "When you left your mother's womb, you didn't leave her empty. Decades later, your living cells are still beating inside her heart and brain."
    },
    {
        "index": 2,
        "filename": "slide_2_cardiac_full_artwork.png",
        "prompt": "Full-bleed breathtaking artistic medical illustration of an illuminated anatomical human heart glowing in deep coral and ruby tones, with golden and emerald fetal stem cells actively repairing heart tissue like glowing constellations, warm ambient parchment background with subtle ECG waveforms and soft golden rays, fine art medical documentary, 8k",
        "tag": "CIRCULATION RESEARCH (2011)",
        "kicker": "MATERNAL HEART RESCUE",
        "title": "HEALING HER HEART",
        "subtitle": "When a pregnant mother suffers heart injury, fetal stem cells migrate across the placenta, transforming into beating cardiomyocytes to repair her tissue."
    },
    {
        "index": 3,
        "filename": "slide_3_brain_full_artwork.png",
        "prompt": "Full-bleed touching editorial illustration of an elderly serene grandmother wearing a soft warm ivory scarf sitting peacefully beside an arched Islamic window, strictly NO eyes and NO nose (smooth blank face with ONLY a sweet gentle smile), surrounded by glowing golden constellations of neural memory networks and floating dust motes in golden afternoon sunlight, deep emotional warmth, 8k",
        "tag": "FRED HUTCHINSON CANCER RESEARCH",
        "kicker": "THE 94-YEAR LEGACY",
        "title": "IN HER BRAIN FOR DECADES",
        "subtitle": "Autopsies revealed male child DNA inside maternal brains up to age 94. For nearly a century, children leave an indelible biological mark in her memory centers."
    },
    {
        "index": 4,
        "filename": "slide_4_prophetic_full_artwork.png",
        "prompt": "Full-bleed masterpiece traditional Islamic illustration of a grown son in a clean white thobe kneeling with profound reverence kissing his smiling mother's hand, mother wearing a modest cream hijab, strictly NO eyes and NO nose (smooth blank faces with sweet smiling mouths only), tranquil sunlit courtyard with olive trees and glowing arabesque brass lanterns, warm golden hour, 8k",
        "tag": "SAHIH AL-BUKHARI 5971 • SAHIH MUSLIM 2548",
        "kicker": "PROPHETIC TRADITION",
        "title": "UMMUKA, UMMUKA, UMMUKA",
        "subtitle": "The Prophet ﷺ declared the mother's honour three times before mentioning the father once—mirroring the biological reality that her body carried you forever."
    },
    {
        "index": 5,
        "filename": "slide_5_lifetime_full_artwork.png",
        "prompt": "Full-bleed heartwarming emotional illustration of two clasped hands: a loving mother's warm hand securely holding her grown child's hand, bathed in an ethereal radiant golden heart glow and warm sunbeams, surrounded by soft floating light particles, tranquil warm parchment ambiance, emotional fine art, 8k",
        "tag": "THE FINAL VERDICT",
        "kicker": "THE LIFETIME RECORD",
        "title": "CALL YOUR MOTHER TODAY",
        "subtitle": "You are not just a chapter in her life. Biologically, genetically, and spiritually... you are stitched into her living organs forever."
    }
]

def generate_full_image(slide):
    raw_path = os.path.join(CAROUSEL_DIR, f"raw_{slide['filename']}")
    final_path = os.path.join(CAROUSEL_DIR, slide["filename"])

    if os.path.exists(final_path):
        print(f"[Skip] {slide['filename']} already exists.")
        return True

    print(f"\n[Generate 9Router] Slide {slide['index']}: {slide['title']}...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": API_KEY,
        "User-Agent": "BangMotion/1.0"
    }
    payload = {
        "model": MODEL,
        "prompt": slide["prompt"],
        "n": 1,
        "size": "1024x1792"  # Full portrait aspect ratio
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

                        composite_full_bleed_slide(raw_path, final_path, slide)
                        print(f"[OK] Slide {slide['index']} finalized: {final_path}")
                        return True
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            time.sleep(3)
    return False

def composite_full_bleed_slide(raw_img_path, final_path, slide):
    # Canvas: 1080 x 1350 (Instagram portrait / TikTok carousel 4:5 ratio)
    W, H = 1080, 1350
    raw_img = Image.open(raw_img_path).convert("RGBA")

    # Resize raw_img to fill 1080 width, crop to 1350 height
    scaled_w = W
    scaled_h = int(raw_img.height * (scaled_w / raw_img.width))
    if scaled_h < H:
        scaled_h = H
        scaled_w = int(raw_img.width * (scaled_h / raw_img.height))

    raw_resized = raw_img.resize((scaled_w, scaled_h), Image.LANCZOS)
    crop_x = (scaled_w - W) // 2
    crop_y = max(0, (scaled_h - H) // 3)  # Bias slightly towards top/center
    artwork = raw_resized.crop((crop_x, crop_y, crop_x + W, crop_y + H)).convert("RGB")

    # Create dark/frosted gradient scrim at top and bottom for razor sharp text readability
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    scrim_draw = ImageDraw.Draw(scrim)

    # Top gradient (height 180)
    for y in range(180):
        alpha = int(140 * (1.0 - (y / 180.0)))
        scrim_draw.line([(0, y), (W, y)], fill=(15, 23, 20, alpha))

    # Bottom gradient (from y=780 to y=1350, height 570)
    for y in range(780, H):
        t = (y - 780) / 570.0
        alpha = int(235 * (t ** 1.35))
        scrim_draw.line([(0, y), (W, y)], fill=(12, 20, 16, alpha))

    # Composite scrim onto artwork
    canvas = Image.alpha_composite(artwork.convert("RGBA"), scrim).convert("RGB")
    draw = ImageDraw.Draw(canvas)

    # Fonts
    try:
        font_tag = ImageFont.truetype("arialbd.ttf", 22)
        font_page = ImageFont.truetype("arialbd.ttf", 24)
        font_kicker = ImageFont.truetype("arialbd.ttf", 24)
        font_title = ImageFont.truetype("arialbd.ttf", 48)
        font_sub = ImageFont.truetype("arial.ttf", 28)
    except Exception:
        font_tag = font_page = font_kicker = font_title = font_sub = ImageFont.load_default()

    # Draw Top Bar: Tag & Page Counter
    draw.text((70, 60), slide["tag"].upper(), fill="#E9C46A", font=font_tag)
    page_text = f"0{slide['index']} / 05"
    draw.text((W - 170, 60), page_text, fill="#FFFFFF", font=font_page)

    # Thin decorative line under top bar
    draw.line([(70, 96), (W - 70, 96)], fill=(255, 255, 255, 60), width=1)

    # Bottom Typography
    text_y = 860
    # Kicker
    draw.text((70, text_y), slide["kicker"].upper(), fill="#F4A261", font=font_kicker)

    # Title
    draw.text((70, text_y + 38), slide["title"], fill="#FFFFFF", font=font_title)

    # Subtitle wrapping
    words = slide["subtitle"].split()
    lines = []
    cur_line = []
    for word in words:
        cur_line.append(word)
        test_line = " ".join(cur_line)
        bbox = draw.textbbox((0, 0), test_line, font=font_sub)
        if (bbox[2] - bbox[0]) > (W - 140):
            cur_line.pop()
            lines.append(" ".join(cur_line))
            cur_line = [word]
    if cur_line:
        lines.append(" ".join(cur_line))

    sub_y = text_y + 112
    for line in lines:
        draw.text((70, sub_y), line, fill="#E2E8F0", font=font_sub)
        sub_y += 42

    # Bottom swipe indicator
    swipe_text = "SWIPE TO READ  →" if slide["index"] < 5 else "SHARE WITH YOUR MOTHER  ♥"
    draw.text((70, H - 75), swipe_text, fill="#94A3B8", font=font_tag)

    canvas.save(final_path, "PNG", quality=95)

def main():
    print(f"--- Generating 5 Full-Bleed Masterpiece Carousel Slides for Episode 10 via 9Router ---")
    success_count = 0
    for slide in FULL_SLIDES:
        if generate_full_image(slide):
            success_count += 1
        time.sleep(1)
    print(f"\n[Finished] {success_count}/{len(FULL_SLIDES)} full-bleed carousel slides ready in {CAROUSEL_DIR}")

if __name__ == "__main__":
    main()
