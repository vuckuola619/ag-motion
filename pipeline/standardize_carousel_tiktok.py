import os
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "assets", "episode10_mother_microchimerism", "carousel_native_text")
TIKTOK_4_5_DIR = os.path.join(PROJECT_ROOT, "assets", "episode10_mother_microchimerism", "carousel_tiktok_4_5")
TIKTOK_9_16_DIR = os.path.join(PROJECT_ROOT, "assets", "episode10_mother_microchimerism", "carousel_tiktok_9_16")

os.makedirs(TIKTOK_4_5_DIR, exist_ok=True)
os.makedirs(TIKTOK_9_16_DIR, exist_ok=True)

SLIDES = [
    "slide_1_cover_native_text.png",
    "slide_2_cardiac_native_text.png",
    "slide_3_brain_native_text.png",
    "slide_4_prophetic_native_text.png",
    "slide_5_closing_native_text.png"
]

def make_exact_4_5(img):
    # Target: 1080 x 1350 (4:5 ratio)
    target_w, target_h = 1080, 1350
    target_ratio = target_w / target_h
    current_ratio = img.width / img.height

    if abs(current_ratio - target_ratio) < 0.005:
        # Already essentially 4:5, just cleanly resize
        return img.resize((target_w, target_h), Image.LANCZOS)

    if current_ratio > target_ratio:
        # Slightly too wide, crop sides symmetrically
        new_w = int(img.height * target_ratio)
        x0 = (img.width - new_w) // 2
        cropped = img.crop((x0, 0, x0 + new_w, img.height))
    else:
        # Slightly too tall (e.g. Slide 1 1092x1440), crop top/bottom carefully
        new_h = int(img.width / target_ratio)
        # Keep 40px margin at top so header isn't cut
        y0 = min(35, (img.height - new_h) // 2)
        cropped = img.crop((0, y0, img.width, y0 + new_h))

    return cropped.resize((target_w, target_h), Image.LANCZOS)

def make_tiktok_9_16(img_4_5):
    # For creators who prefer full-screen 9:16 (1080x1920) on TikTok:
    # Place 4:5 image (1080x1350) centered vertically (y=285),
    # with elegant blurred background fill so text sits safely in the TikTok sweet spot!
    canvas = Image.new("RGB", (1080, 1920), "#0E1512")
    # Create blurred background
    bg = img_4_5.resize((1080, 1920), Image.BILINEAR)
    from PIL import ImageFilter
    bg = bg.filter(ImageFilter.GaussianBlur(radius=35))
    canvas.paste(bg, (0, 0))

    # Paste crisp 4:5 image in center
    y_pos = (1920 - 1350) // 2
    canvas.paste(img_4_5, (0, y_pos))
    return canvas

def main():
    print("--- Standardizing Carousel Slides for TikTok & Instagram ---")
    for f in SLIDES:
        src_path = os.path.join(SRC_DIR, f)
        if not os.path.exists(src_path):
            continue

        raw = Image.open(src_path).convert("RGB")
        print(f"\nProcessing {f} (original: {raw.size})...")

        # 1. Exact 4:5 standard (1080x1350)
        norm_4_5 = make_exact_4_5(raw)
        out_4_5_path = os.path.join(TIKTOK_4_5_DIR, f)
        norm_4_5.save(out_4_5_path, "PNG", quality=95)
        print(f" -> Saved 4:5 format (1080x1350): {out_4_5_path}")

        # 2. Full-screen 9:16 vertical (1080x1920)
        full_9_16 = make_tiktok_9_16(norm_4_5)
        out_9_16_path = os.path.join(TIKTOK_9_16_DIR, f)
        full_9_16.save(out_9_16_path, "PNG", quality=95)
        print(f" -> Saved 9:16 vertical format (1080x1920): {out_9_16_path}")

    print("\n[Done] All slides standardized for TikTok & Instagram!")

if __name__ == "__main__":
    main()
