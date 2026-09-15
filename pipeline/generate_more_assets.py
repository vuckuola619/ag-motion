import os
import sys
import json
import base64
import urllib.request
import urllib.error
import numpy as np
from PIL import Image, ImageDraw

ROUTER_URL = "http://127.0.0.1:20128/v1/images/generations"
API_KEY = "Bearer sk-c4f2444795b190b3-kzvd4h-ea839762"
MODEL = "cx/gpt-5.5-image"

NEW_ASSET_SPECS = [
    {
        "filename": "sauropod_fossil.png",
        "prompt": "Complete giant Sauropod Brachiosaurus dinosaur skeleton fossil museum catalog display, long neck, dramatic paleontology specimen, isolated on pure white background, studio catalog lighting, sharp crisp edges, transparent alpha cutout, 8k",
        "title": "Sauropod Long-Neck Fossil Skeleton"
    },
    {
        "filename": "crater_tsunami.png",
        "prompt": "Geological aerial diagram of circular Chicxulub asteroid impact crater with massive oceanic megatsunami shockwave rings radiating across Caribbean sea, isolated on pure white background, scientific catalog graphic cutout",
        "title": "Chicxulub Crater Megatsunami Map"
    },
    {
        "filename": "firestorm_sky.png",
        "prompt": "Prehistoric global atmospheric firestorm, glowing fiery sky with burning incandescent impact spherules and falling fire meteors, dramatic catastrophic cutout, isolated on pure white background",
        "title": "Global Firestorm & Atmospheric Re-entry"
    },
    {
        "filename": "sun_blackout.png",
        "prompt": "Pale dark dim sun obscured by massive billowing black sulfur soot and ash storm clouds, atmospheric darkness, nuclear winter, isolated on pure white background, catalog specimen cutout",
        "title": "Sun Blackout & Nuclear Winter"
    },
    {
        "filename": "fern_fossil.png",
        "prompt": "Prehistoric fossil fern leaf imprinted on geological shale rock matrix, fern spike botanical survivor of mass extinction, highly detailed veins, isolated on pure white background, studio specimen cutout",
        "title": "K-Pg Fern Spike Fossil Specimen"
    }
]

def make_transparent_cutout(img: Image.Image, threshold: int = 245) -> Image.Image:
    img = img.convert("RGBA")
    arr = np.array(img)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    
    is_white = (r > threshold) & (g > threshold) & (b > threshold)
    diff = np.maximum.reduce([255 - r, 255 - g, 255 - b])
    alpha_soft = np.clip(diff * 5, 0, 255).astype(np.uint8)
    
    new_a = np.where(is_white, alpha_soft, a)
    arr[:, :, 3] = new_a
    return Image.fromarray(arr, "RGBA")

def generate_via_9router(prompt: str, output_path: str) -> bool:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ROUTER_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": API_KEY
        }
    )
    
    try:
        print(f"  [9Router] Calling {MODEL} (timeout 90s)...")
        with urllib.request.urlopen(req, timeout=90) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            item = result.get("data", [{}])[0]
            
            raw_bytes = None
            if "b64_json" in item:
                raw_bytes = base64.b64decode(item["b64_json"])
            elif "url" in item:
                img_url = item["url"]
                with urllib.request.urlopen(img_url, timeout=45) as img_resp:
                    raw_bytes = img_resp.read()
            
            if raw_bytes:
                temp_path = output_path + ".tmp.png"
                with open(temp_path, "wb") as f:
                    f.write(raw_bytes)
                
                with Image.open(temp_path) as im:
                    cutout = make_transparent_cutout(im)
                    cutout.save(output_path, "PNG")
                
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                print(f"  [9Router] Successfully generated and processed: {output_path}")
                return True
    except Exception as e:
        print(f"  [9Router Notice]: {e}")
    
    return False

def generate_procedural_fallback(spec: dict, output_path: str):
    print(f"  [Fallback] Generating procedural high-res visual for: {spec['filename']}")
    width, height = 1024, 1024
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    fname = spec["filename"]
    if fname == "sauropod_fossil.png":
        # Long neck sauropod skeleton
        draw.line([(200, 800), (220, 500)], fill=(200, 185, 160, 255), width=24) # back leg
        draw.line([(450, 820), (460, 520)], fill=(200, 185, 160, 255), width=24) # front leg
        draw.ellipse([(180, 420), (520, 600)], fill=(210, 195, 170, 255), outline=(90, 80, 65, 255), width=8) # rib cage
        # Long curved neck
        draw.arc([(300, 180), (840, 700)], start=160, end=320, fill=(210, 195, 170, 255), width=28)
        # Small head skull
        draw.ellipse([(760, 180), (860, 250)], fill=(220, 205, 180, 255), outline=(90, 80, 65, 255), width=6)
        # Long tail
        draw.arc([(50, 480), (320, 750)], start=30, end=180, fill=(200, 185, 160, 255), width=18)
    elif fname == "crater_tsunami.png":
        # Megatsunami shockwave map
        cx, cy = 512, 512
        for r in [460, 380, 300, 220, 140]:
            draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline=(37, 99, 235, 220), width=6)
        draw.ellipse([(cx - 70, cy - 70), (cx + 70, cy + 70)], fill=(225, 29, 72, 240), outline=(159, 18, 57, 255), width=8)
        for i in range(12):
            angle = i * (np.pi / 6)
            x1, y1 = cx + np.cos(angle) * 80, cy + np.sin(angle) * 80
            x2, y2 = cx + np.cos(angle) * 440, cy + np.sin(angle) * 440
            draw.line([(x1, y1), (x2, y2)], fill=(37, 99, 235, 120), width=3)
    elif fname == "firestorm_sky.png":
        # Incandescent firestorm
        for y in range(200, 800, 40):
            draw.arc([(100, y - 60), (924, y + 200)], start=0, end=180, fill=(245, 158, 11, 220), width=10)
        for _ in range(60):
            px, py = np.random.randint(150, 874), np.random.randint(200, 800)
            sz = np.random.randint(4, 14)
            draw.ellipse([(px, py), (px + sz, py + sz)], fill=(225, 29, 72, 255))
            draw.line([(px, py), (px - 20, py - 40)], fill=(251, 191, 36, 200), width=3)
    elif fname == "sun_blackout.png":
        # Sun eclipsed by dense soot
        cx, cy = 512, 512
        for r in range(320, 160, -20):
            draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(251, 191, 36, 25))
        draw.ellipse([(cx - 160, cy - 160), (cx + 160, cy + 160)], fill=(254, 240, 138, 200))
        # Dense dark soot plumes sweeping across
        for ox, oy, ow, oh in [(200, 300, 500, 200), (350, 420, 550, 220), (180, 480, 600, 240)]:
            draw.ellipse([(ox, oy), (ox + ow, oy + oh)], fill=(25, 28, 35, 235))
    elif fname == "fern_fossil.png":
        # Fossil fern leaf
        draw.polygon([(260, 180), (764, 180), (820, 844), (204, 844)], fill=(190, 180, 165, 255), outline=(75, 65, 55, 255), width=6)
        # Stem
        draw.line([(512, 220), (512, 800)], fill=(45, 38, 32, 255), width=10)
        # Fronds / leaves
        for y in range(260, 760, 36):
            draw.line([(512, y), (340, y - 24)], fill=(55, 48, 40, 255), width=6)
            draw.line([(512, y), (684, y - 24)], fill=(55, 48, 40, 255), width=6)
    
    img.save(output_path, "PNG")
    print(f"  [Fallback] Saved procedural asset to: {output_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    images_dir = os.path.join(project_dir, "assets", "images")
    os.makedirs(images_dir, exist_ok=True)
    
    print("[Pipeline] Generating second batch of visual cutout sprites...")
    for spec in NEW_ASSET_SPECS:
        out_file = os.path.join(images_dir, spec["filename"])
        if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
            print(f"  [Asset exists] Skipping {spec['filename']}")
            continue
        
        print(f"\n[Asset] {spec['title']} -> {spec['filename']}")
        success = generate_via_9router(spec["prompt"], out_file)
        if not success:
            generate_procedural_fallback(spec, out_file)

if __name__ == "__main__":
    main()
