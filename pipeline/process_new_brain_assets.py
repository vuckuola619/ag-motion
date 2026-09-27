import os
import glob
import numpy as np
from PIL import Image

BRAIN_DIR = r"C:\Users\bati-\.gemini\antigravity\brain\1b26f921-8aa1-449e-ac7a-9bd4b5ab04c6"
TARGET_DIR = r"c:\Users\bati-\Documents\AG-Bang\assets\episode6_project_azorian\images"
os.makedirs(TARGET_DIR, exist_ok=True)

MAPPINGS = [
    ("soviet_sailors_photo*.jpg", "soviet_sailors_vintage_photo.png", "card_photo"),
    ("soviet_naval_medal*.jpg", "soviet_naval_order_medal.png", "cutout"),
    ("vintage_brass_bell*.jpg", "vintage_submarine_brass_bell.png", "cutout"),
    ("cia_coded_telegram*.jpg", "cia_coded_telegram_cable.png", "doc_cutout"),
    ("deepsea_sonar_robot*.jpg", "deepsea_sonar_scanner_robot.png", "cutout"),
    ("seismic_acoustic_chart*.jpg", "seismic_acoustic_hydrophone_recording.png", "doc_cutout"),
    ("warhead_cutaway*.jpg", "nuclear_warhead_cross_section.png", "blueprint"),
]

def make_transparent_cutout(img, threshold=240, feather=25):
    img = img.convert("RGBA")
    arr = np.array(img, dtype=np.float32)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

    brightness = (r + g + b) / 3.0
    is_pure_white = (r > threshold) & (g > threshold) & (b > threshold)
    low_thresh = threshold - feather
    is_feather = (brightness > low_thresh) & (~is_pure_white)

    alpha = np.ones_like(a) * 255.0
    alpha[is_pure_white] = 0.0

    feather_mask = is_feather & (r > low_thresh) & (g > low_thresh) & (b > low_thresh)
    alpha[feather_mask] = np.clip((threshold - brightness[feather_mask]) / float(feather), 0.0, 1.0) * 255.0

    arr[:, :, 3] = alpha
    return Image.fromarray(arr.astype(np.uint8), "RGBA")

def make_doc_cutout(img):
    # For documents with white borders outside the paper, remove outer white border
    img = img.convert("RGBA")
    arr = np.array(img, dtype=np.float32)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    # Pure white outside border
    is_white_bg = (r > 248) & (g > 248) & (b > 248)
    arr[is_white_bg, 3] = 0.0
    # Slight feathering
    is_near = (r > 238) & (g > 238) & (b > 238) & (~is_white_bg)
    avg = (r + g + b) / 3.0
    arr[is_near, 3] = np.clip((248.0 - avg[is_near]) / 10.0, 0.0, 1.0) * 255.0
    return Image.fromarray(arr.astype(np.uint8), "RGBA")

def main():
    print("[Processing Brain Assets]")
    for pattern, out_name, kind in MAPPINGS:
        matches = glob.glob(os.path.join(BRAIN_DIR, pattern))
        if not matches:
            print(f"[-] No file for {pattern}")
            continue
        src = matches[0]
        dst = os.path.join(TARGET_DIR, out_name)
        with Image.open(src) as im:
            if kind == "cutout":
                res = make_transparent_cutout(im)
            elif kind == "doc_cutout" or kind == "card_photo":
                res = make_doc_cutout(im)
            else:
                res = im.convert("RGBA")
            res.save(dst, "PNG")
            sz = round(os.path.getsize(dst)/1024, 1)
            print(f"[+] Saved: {out_name} ({sz} KB) from {os.path.basename(src)}")

if __name__ == "__main__":
    main()
