import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

BRAIN_DIR = r"C:\Users\bati-\.gemini\antigravity\brain\00b74a05-6107-4c28-8d42-1c3e09081b82"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_DIR = os.path.join(PROJECT_ROOT, "assets", "episode6_project_azorian", "images")
os.makedirs(TARGET_DIR, exist_ok=True)

RAW_IMAGES = [
    # (source_pattern, target_filename, type)
    ("manila_dossier_folder", "manila_dossier_folder.png", "cutout"),
    ("submarine_k129_profile", "submarine_k129_profile.png", "cutout"),
    ("glomar_explorer_ship", "glomar_explorer_ship.png", "cutout"),
    ("clementine_claw_rusty", "clementine_claw_rusty.png", "cutout"),
    ("nuclear_torpedo_soviet", "nuclear_torpedo_soviet.png", "cutout"),
    ("geiger_counter_ussr", "geiger_counter_ussr.png", "cutout"),
    ("sonar_echogram_display", "sonar_echogram_display.png", "cutout"),
    ("case_solved_stamp", "case_solved_stamp.png", "stamp"),
    ("bg_pacific_sonar_bathymetry", "bg_pacific_sonar_bathymetry.png", "card"),
    ("bg_cia_topsecret_memo", "bg_cia_topsecret_memo.png", "card"),
    ("bg_hughes_mining_schematic", "bg_hughes_mining_schematic.png", "card"),
    ("bg_ocean_floor_claw_diagram", "bg_ocean_floor_claw_diagram.png", "card"),
    ("bg_burial_protocol_doc", "bg_burial_protocol_doc.png", "card"),
]

def make_transparent_cutout(img, threshold=242, feather=18):
    img = img.convert("RGBA")
    arr = np.array(img, dtype=np.float32)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

    # Off-white / white background detection
    brightness = (r + g + b) / 3.0
    is_pure_white = (r > threshold) & (g > threshold) & (b > threshold)
    
    # Soft alpha feathering
    low_thresh = threshold - feather
    is_feather = (brightness > low_thresh) & (~is_pure_white)
    
    alpha = np.ones_like(a) * 255.0
    alpha[is_pure_white] = 0.0
    
    feather_mask = is_feather & (r > low_thresh) & (g > low_thresh) & (b > low_thresh)
    alpha[feather_mask] = np.clip((threshold - brightness[feather_mask]) / float(feather), 0.0, 1.0) * 255.0
    
    arr[:, :, 3] = alpha
    return Image.fromarray(arr.astype(np.uint8), "RGBA")

def make_transparent_stamp(img):
    img = img.convert("RGBA")
    arr = np.array(img, dtype=np.float32)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

    # For red rubber stamp: keep red ink, turn white/off-white background completely transparent
    # Red ink has r >> g and r >> b
    brightness = (r + g + b) / 3.0
    is_white_bg = (brightness > 230) & (abs(r - g) < 25) & (abs(g - b) < 25)
    
    # Feather around edges
    is_near_bg = (brightness > 205) & (brightness <= 230) & (abs(r - g) < 30)
    
    alpha = np.ones_like(a) * 255.0
    alpha[is_white_bg] = 0.0
    alpha[is_near_bg] = np.clip((230.0 - brightness[is_near_bg]) / 25.0, 0.0, 1.0) * 255.0
    
    arr[:, :, 3] = alpha
    return Image.fromarray(arr.astype(np.uint8), "RGBA")

def find_brain_file(pattern):
    for f in os.listdir(BRAIN_DIR):
        if f.startswith(pattern) and (f.endswith(".jpg") or f.endswith(".png")):
            return os.path.join(BRAIN_DIR, f)
    return None

def create_soviet_ensign(target_path):
    # Authentic Soviet Naval Ensign (white field, light blue stripe at bottom, red star and hammer-and-sickle)
    w, h = 1200, 800
    im = Image.new("RGBA", (w, h), (248, 246, 240, 255))
    draw = ImageDraw.Draw(im)
    # Blue stripe on bottom 1/6
    stripe_h = h // 6
    draw.rectangle([0, h - stripe_h, w, h], fill=(0, 95, 175, 255))
    
    # Red star on left side
    cx, cy = 350, (h - stripe_h) // 2
    r_outer = 130
    r_inner = 55
    points = []
    for i in range(10):
        angle = -np.pi / 2.0 + i * np.pi / 5.0
        r_curr = r_outer if i % 2 == 0 else r_inner
        points.append((cx + r_curr * np.cos(angle), cy + r_curr * np.sin(angle)))
    draw.polygon(points, fill=(210, 30, 25, 255))
    
    # Hammer and Sickle on right side
    hx, hy = 780, cy
    draw.arc([hx - 90, hy - 90, hx + 90, hy + 90], start=120, end=330, fill=(210, 30, 25, 255), width=28)
    draw.line([hx - 40, hy + 70, hx + 80, hy - 50], fill=(210, 30, 25, 255), width=28)
    
    # Add subtle fabric weave texture & vignetted border
    im = im.filter(ImageFilter.GaussianBlur(0.6))
    im.save(target_path, "PNG")
    print(f"[Created] Soviet Naval Ensign -> {target_path}")

def create_severed_hull(k129_path, target_path):
    if not os.path.exists(k129_path):
        return
    im = Image.open(k129_path).convert("RGBA")
    w, h = im.size
    # Sever the front 1/3 section (the bow section that was recovered, ~38 feet)
    sever_x = int(w * 0.38)
    severed = im.crop((0, 0, sever_x, h))
    
    # Add jagged fracture jagged edge
    draw = ImageDraw.Draw(severed)
    arr = np.array(severed)
    # create jagged alpha mask on the right border
    np.random.seed(42)
    for y in range(h):
        jag = np.random.randint(-18, 12)
        cut_start = max(0, sever_x - 25 + jag)
        if cut_start < arr.shape[1]:
            arr[y, cut_start:, 3] = 0
            
    res = Image.fromarray(arr, "RGBA")
    res.save(target_path, "PNG")
    print(f"[Created] Severed K-129 Hull Section -> {target_path}")

def main():
    print("[Azorian Assets] Processing generated images...")
    processed_count = 0
    for pattern, out_name, kind in RAW_IMAGES:
        src = find_brain_file(pattern)
        dst = os.path.join(TARGET_DIR, out_name)
        if not src:
            print(f"[-] Source image not found for pattern: {pattern}")
            continue
            
        with Image.open(src) as im:
            if kind == "cutout":
                out_im = make_transparent_cutout(im)
                out_im.save(dst, "PNG")
            elif kind == "stamp":
                out_im = make_transparent_stamp(im)
                out_im.save(dst, "PNG")
            else: # card (9:16)
                out_im = im.convert("RGB")
                out_im.save(dst, "PNG")
        sz = round(os.path.getsize(dst) / 1024, 1)
        print(f"[+] Processed: {out_name} ({sz} KB) [{kind}]")
        processed_count += 1

    # Create additional specialized assets
    ensign_dst = os.path.join(TARGET_DIR, "soviet_naval_ensign_flag.png")
    create_soviet_ensign(ensign_dst)
    
    k129_file = os.path.join(TARGET_DIR, "submarine_k129_profile.png")
    severed_dst = os.path.join(TARGET_DIR, "severed_k129_hull_section.png")
    create_severed_hull(k129_file, severed_dst)

    # Copy utility tape & radiation symbols from ep5 if present
    ep5_images = os.path.join(PROJECT_ROOT, "assets", "episode5_iridium_layer", "images")
    for extra in ["scotch_tape_piece.png", "radioactive_hazard_tag.png", "radar_targeting_reticle.png"]:
        src_extra = os.path.join(ep5_images, extra)
        if os.path.exists(src_extra):
            shutil.copyfile(src_extra, os.path.join(TARGET_DIR, extra))
            print(f"[Copied] {extra}")

    print(f"[Azorian Assets] Completed {processed_count} master assets in {TARGET_DIR}")

if __name__ == "__main__":
    main()
