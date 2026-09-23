import os
import sys
import json
import time
import base64
import urllib.request
import urllib.error
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROUTER_URL = "http://127.0.0.1:20128/v1/images/generations"
API_KEY = "Bearer sk-c4f2444795b190b3-kzvd4h-ea839762"
MODEL = "cx/gpt-5.5-image"

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "assets", "episode_indonesia_hari_ini", "sprites")
BRAIN_DIR = r"C:\Users\bati-\.gemini\antigravity\brain\6c49e710-6b1f-406b-9eb2-9a374f179691"

SPRITE_SPECS = [
    {
        "filename": "sprite_nickel_ore_crystal.png",
        "prompt": "Raw glistening metallic silver and greenish nickel ore mineral crystal cluster, electric cyan spark aura, high-tech mining specimen, 3D isometric asset, isolated on pure solid white background, studio catalog lighting, sharp edges, no shadows, 8k",
        "title": "Raw Nickel Mineral Crystal"
    },
    {
        "filename": "sprite_alarm_beacon.png",
        "prompt": "Futuristic 3D digital hazard warning beacon and alarm siren, sleek matte black housing with vibrant glowing translucent red emergency crystal core, cybernetic warning aesthetic, isolated on pure solid white background, clean cutout edges, 3D asset",
        "title": "Hazard Warning Alarm Beacon"
    },
    {
        "filename": "sprite_ai_chip.png",
        "prompt": "Advanced 3D AI neural accelerator microchip, square silicon wafer with intricate metallic gold pins, glowing cyan neon circuit pathways, glass dielectric plate on top, isolated on pure solid white background, high-end 3D product render, sharp cutout edges",
        "title": "AI Neural Processor Chip"
    },
    {
        "filename": "sprite_gold_bullion_stack.png",
        "prompt": "Pristine 3D stack of gleaming Indonesian Rupiah gold bullion bars and glowing digital currency tokens, luxury 3D isometric financial asset, isolated on pure solid white background, studio catalog reflections, clean sharp edges",
        "title": "Gold Bullion & Digital Assets"
    },
    {
        "filename": "sprite_middle_income_ladder.png",
        "prompt": "Futuristic 3D upward ascension arrow breaking through a geometric glass ceiling barrier, glowing cyan and gold trajectory line, high contrast 3D concept asset, isolated on pure solid white background, clean cutout edges",
        "title": "Ascension Breakthrough Arrow"
    },
    {
        "filename": "sprite_garuda_gold_seal.png",
        "prompt": "Luxurious 3D embossed gold national heraldic eagle emblem medal seal, intricate golden feathers, pristine metallic reflections, circular dossier badge, isolated on pure solid white background, studio product render, crisp clean cutout edges",
        "title": "Golden National Heraldic Seal"
    },
    {
        "filename": "sprite_quantum_atom_stem.png",
        "prompt": "Futuristic 3D STEM innovation gyroscope atom, glowing orbital electron rings made of polished titanium and emerald laser light, glowing energy core, isolated on pure solid white background, crisp cutout edges, 3D tech asset",
        "title": "STEM Innovation Quantum Atom"
    },
    {
        "filename": "sprite_radar_satellite.png",
        "prompt": "High-tech orbital geopolitical surveillance radar satellite, gold foil thermal insulation, deployed solar panels and parabolic dish, isolated on pure solid white background, studio catalog lighting, crisp edges, 3D asset",
        "title": "Geopolitical Radar Satellite"
    }
]

def make_transparent_cutout(img: Image.Image, threshold: int = 245) -> Image.Image:
    """Isolate pure white/near-white background to transparent RGBA."""
    img = img.convert("RGBA")
    arr = np.array(img)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    
    is_white = (r > threshold) & (g > threshold) & (b > threshold)
    diff = np.maximum.reduce([255 - r, 255 - g, 255 - b])
    alpha_soft = np.clip(diff * 6, 0, 255).astype(np.uint8)
    
    new_a = np.where(is_white, alpha_soft, a)
    arr[:, :, 3] = new_a
    return Image.fromarray(arr, "RGBA")

def generate_via_9router(spec: dict, output_path: str, max_retries: int = 3) -> bool:
    payload = {
        "model": MODEL,
        "prompt": spec["prompt"],
        "n": 1,
        "size": "1024x1024"
    }
    data = json.dumps(payload).encode("utf-8")
    
    for attempt in range(1, max_retries + 1):
        t0 = time.time()
        print(f"  [9Router cx/gpt-5.5-image] Generating: {spec['filename']} (Attempt {attempt}/{max_retries})...", flush=True)
        try:
            req = urllib.request.Request(
                ROUTER_URL,
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": API_KEY
                }
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                item = result.get("data", [{}])[0]
                
                raw_bytes = None
                if "b64_json" in item:
                    raw_bytes = base64.b64decode(item["b64_json"])
                elif "url" in item:
                    with urllib.request.urlopen(item["url"], timeout=60) as img_resp:
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
                    
                    dt = round(time.time() - t0, 1)
                    sz = round(os.path.getsize(output_path) / 1024, 1)
                    print(f"  [9Router SUCCESS] Saved {spec['filename']} ({sz} KB) in {dt}s", flush=True)
                    time.sleep(5)  # Healthy pacing
                    return True
        except Exception as err:
            print(f"  [9Router Attempt {attempt} Failed] {err}", flush=True)
            time.sleep(8)
            
    return False

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"=== 9Router cx/gpt-5.5-image Cosmetic Sprite Generation ===")
    print(f"Target Directory: {OUTPUT_DIR}\n")
    
    success_count = 0
    total = len(SPRITE_SPECS)
    for i, spec in enumerate(SPRITE_SPECS, 1):
        out_path = os.path.join(OUTPUT_DIR, spec["filename"])
        if os.path.exists(out_path):
            print(f"[{i}/{total}] [Skipping Existing] {spec['filename']}")
            success_count += 1
            continue
            
        print(f"[{i}/{total}] Processing {spec['title']}...")
        ok = generate_via_9router(spec, out_path)
        if ok:
            success_count += 1
            
    print(f"\n[Generation Complete] {success_count}/{total} sprites generated in {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
