import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_DIR = os.path.join(PROJECT_ROOT, "assets", "episode6_project_azorian", "images")

def create_draped_soviet_flag(target_path):
    # Create realistic wavy draped flag with transparent background
    w, h = 900, 520
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    # Wavy flag cloth contour polygon
    points = []
    # Top edge waves
    for x in range(0, w, 10):
        y = 40 + int(18 * np.sin(x / 70.0) + 10 * np.cos(x / 130.0))
        points.append((x, y))
    # Right edge
    points.append((w - 20, h - 60))
    # Bottom edge waves (reverse)
    for x in range(w - 20, 0, -10):
        y = h - 60 + int(18 * np.sin(x / 70.0) + 10 * np.cos(x / 130.0))
        points.append((x, y))
    points.append((0, 40))

    # Fill white cloth base
    draw.polygon(points, fill=(244, 242, 235, 255))

    # Blue bottom stripe
    stripe_pts = []
    for x in range(0, w, 10):
        y_top = h - 130 + int(18 * np.sin(x / 70.0) + 10 * np.cos(x / 130.0))
        stripe_pts.append((x, y_top))
    for x in range(w - 20, 0, -10):
        y_bot = h - 60 + int(18 * np.sin(x / 70.0) + 10 * np.cos(x / 130.0))
        stripe_pts.append((x, y_bot))
    draw.polygon(stripe_pts, fill=(0, 90, 170, 255))

    # Red star
    cx, cy = 280, 210
    r_outer, r_inner = 85, 36
    star_pts = []
    for i in range(10):
        angle = -np.pi / 2.0 + i * np.pi / 5.0
        r_curr = r_outer if i % 2 == 0 else r_inner
        star_pts.append((cx + r_curr * np.cos(angle), cy + r_curr * np.sin(angle)))
    draw.polygon(star_pts, fill=(205, 30, 25, 255))

    # Sickle & Hammer
    hx, hy = 580, 210
    draw.arc([hx - 60, hy - 60, hx + 60, hy + 60], start=120, end=330, fill=(205, 30, 25, 255), width=18)
    draw.line([hx - 25, hy + 45, hx + 55, hy - 35], fill=(205, 30, 25, 255), width=18)

    # Shading folds (darken troughs, lighten crests)
    arr = np.array(im, dtype=np.float32)
    x_coords = np.arange(w)
    shading = 1.0 + 0.16 * np.sin(x_coords / 70.0)
    for c in range(3):
        arr[:, :, c] = np.clip(arr[:, :, c] * shading[None, :], 0, 255)

    res = Image.fromarray(arr.astype(np.uint8), "RGBA")
    res = res.filter(ImageFilter.GaussianBlur(0.8))
    res.save(target_path, "PNG")
    print(f"[Updated] Draped Soviet Flag -> {target_path}")

def create_large_fractured_bow(k129_path, target_path):
    if not os.path.exists(k129_path):
        return
    im = Image.open(k129_path).convert("RGBA")
    w, h = im.size
    # Sever the front 42% (bow + sonar dome + torpedo compartment)
    sever_x = int(w * 0.44)
    severed = im.crop((0, 0, sever_x, h))
    arr = np.array(severed)
    
    np.random.seed(101)
    for y in range(h):
        jag = int(22 * np.sin(y / 15.0) + np.random.randint(-12, 12))
        cut_start = max(0, sever_x - 30 + jag)
        if cut_start < arr.shape[1]:
            arr[y, cut_start:, 3] = 0
            
    res = Image.fromarray(arr, "RGBA")
    res.save(target_path, "PNG")
    print(f"[Updated] Large Fractured K-129 Bow -> {target_path}")

if __name__ == "__main__":
    create_draped_soviet_flag(os.path.join(TARGET_DIR, "soviet_naval_ensign_flag.png"))
    create_large_fractured_bow(
        os.path.join(TARGET_DIR, "submarine_k129_profile.png"),
        os.path.join(TARGET_DIR, "severed_k129_hull_section.png")
    )
