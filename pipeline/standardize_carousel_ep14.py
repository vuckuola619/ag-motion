import os
from PIL import Image, ImageFilter

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "assets", "episode14_glymphatic_brain_wash", "carousel_native_text")
DIR_4_5 = os.path.join(PROJECT_ROOT, "assets", "episode14_glymphatic_brain_wash", "carousel_tiktok_4_5")
DIR_9_16 = os.path.join(PROJECT_ROOT, "assets", "episode14_glymphatic_brain_wash", "carousel_tiktok_9_16")

os.makedirs(DIR_4_5, exist_ok=True)
os.makedirs(DIR_9_16, exist_ok=True)

SLIDES = [
    "slide_1_cover_native_text.png",
    "slide_2_astrocytes_native_text.png",
    "slide_3_alzheimer_purge_native_text.png",
    "slide_4_sleep_debt_native_text.png",
    "slide_5_closing_protocol_native_text.png"
]

def standardize():
    print("--- Standardizing Episode 14 Carousel for TikTok Safe Zones ---")
    for fname in SLIDES:
        src_path = os.path.join(SRC_DIR, fname)
        if not os.path.exists(src_path):
            print(f"[Skip] {fname} not found")
            continue

        img = Image.open(src_path)

        # 1. 4:5 Format (1080x1350)
        img_4_5 = img.resize((1080, 1350), Image.Resampling.LANCZOS)
        out_4_5 = os.path.join(DIR_4_5, fname.replace("_native_text", "_tiktok_4_5"))
        img_4_5.save(out_4_5, "PNG", optimize=True)
        print(f"[Saved 4:5] {out_4_5} ({os.path.getsize(out_4_5) / (1024*1024):.2f} MB)")

        # 2. 9:16 Format (1080x1920) with blurred ambient background
        canvas_9_16 = Image.new("RGB", (1080, 1920), (5, 8, 17))
        # Create blurred background
        bg_blur = img.resize((1080, 1920), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(radius=35))
        canvas_9_16.paste(bg_blur, (0, 0))

        # Paste the sharp 4:5 image centered vertically (y = (1920-1350)/2 = 285)
        canvas_9_16.paste(img_4_5, (0, 285))

        out_9_16 = os.path.join(DIR_9_16, fname.replace("_native_text", "_tiktok_9_16"))
        canvas_9_16.save(out_9_16, "PNG", optimize=True)
        print(f"[Saved 9:16] {out_9_16} ({os.path.getsize(out_9_16) / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    standardize()
