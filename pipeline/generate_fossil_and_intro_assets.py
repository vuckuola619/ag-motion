import os
import sys
import json
import time
import base64
import urllib.request
import urllib.error
import shutil
import numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
IMAGES_DIR = os.path.join(PROJECT_DIR, "assets", "episode5_iridium_layer", "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

# 1. Copy existing high-res cutouts from Ep4
ep4_img_dir = os.path.join(PROJECT_DIR, "assets", "episode4_chicxulub", "images")
for f in ["trex_skull_specimen.png", "burned_dino_claw_bone.png"]:
    src = os.path.join(ep4_img_dir, f)
    dst = os.path.join(IMAGES_DIR, f)
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.copy2(src, dst)
        print(f"[Copied] {f} -> {dst}")

ROUTER_URL = "http://127.0.0.1:20128/v1/images/generations"
API_KEY = "Bearer sk-c4f2444795b190b3-kzvd4h-ea839762"
MODEL = "cx/gpt-5.5-image"

ASSETS_TO_GENERATE = [
    {
        "filename": "bg_dinosaur_fossil_lithograph.png",
        "type": "card",
        "prompt": (
            "Vintage 1880s scientific paleontological lithograph engraving illustration on aged cream parchment paper, "
            "showing a complete fossil skeleton profile of a Tyrannosaurus Rex and Triceratops skull with comparative bone anatomy callouts, "
            "detailed fossilized ribs and vertebrae, Latin text typography 'TABULA PALEONTOLOGICA - DINOSAURIA CRETACEA', "
            "fine antique cross-hatching etching style, museum archival document, 8k"
        )
    },
    {
        "filename": "intro_case_folder.png",
        "type": "card",
        "prompt": (
            "Vintage Manila confidential investigation dossier folder cover, viewed from front on warm cream surface. "
            "Bold black typography 'VOX FORENSIC ARCHIVE // DOSSIER #05', red rubber stamp 'CLASSIFIED EVIDENCE: K-PG BOUNDARY', "
            "weathered metal paper clips holding a yellow inspection tag, barcode sticker, authentic worn aged paper edges, tactile editorial documentary aesthetic, 8k"
        )
    },
    {
        "filename": "outro_case_closed_card.png",
        "type": "card",
        "prompt": (
            "Archival editorial case closed verdict card on heavy textured cream archival cardstock. "
            "Prominent bold red weathered rubber stamp 'INVESTIGATION CONCLUDED // CASE CLOSED', "
            "embossed circular official archival seal emblem, clean typewriter text 'DEEP TIME MYSTERIES · EPISODE 05', "
            "barcode strip at bottom, authentic paper grain, museum documentary style, 8k"
        )
    }
]

def make_transparent_cutout(img):
    img = img.convert("RGBA")
    arr = np.array(img)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

    is_white = (r > 238) & (g > 238) & (b > 238)
    arr[is_white, 3] = 0

    is_near_white = (r > 218) & (g > 218) & (b > 218) & (~is_white)
    avg = (r.astype(float) + g.astype(float) + b.astype(float)) / 3.0
    alpha_scale = np.clip((238.0 - avg) / 20.0, 0.0, 1.0)
    arr[is_near_white, 3] = (arr[is_near_white, 3].astype(float) * alpha_scale[is_near_white]).astype(np.uint8)

    return Image.fromarray(arr, "RGBA")

def generate_asset(spec, max_retries=3):
    target_path = os.path.join(IMAGES_DIR, spec["filename"])
    if os.path.exists(target_path) and os.path.getsize(target_path) > 10000:
        print(f"[Skip] Already exists: {spec['filename']}", flush=True)
        return spec["filename"], True

    headers = {
        "Content-Type": "application/json",
        "Authorization": API_KEY,
        "User-Agent": "BangMotion/1.0"
    }

    payload = {
        "model": MODEL,
        "prompt": spec["prompt"],
        "n": 1,
        "size": "1024x1024",
        "response_format": "b64_json"
    }

    data = json.dumps(payload).encode("utf-8")

    for attempt in range(1, max_retries + 1):
        t0 = time.time()
        print(f"[Start] {spec['filename']} (Attempt {attempt}/{max_retries})...", flush=True)
        try:
            req = urllib.request.Request(ROUTER_URL, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=120) as resp:
                res_data = json.loads(resp.read().decode("utf-8"))

            b64_str = res_data["data"][0]["b64_json"]
            img_bytes = base64.b64decode(b64_str)

            temp_path = target_path + ".tmp.png"
            with open(temp_path, "wb") as f:
                f.write(img_bytes)

            img = Image.open(temp_path)
            if spec.get("type") == "cutout":
                img = make_transparent_cutout(img)
            img.save(target_path, "PNG")

            if os.path.exists(temp_path):
                os.remove(temp_path)

            dt = time.time() - t0
            print(f"[Done] {spec['filename']} saved in {dt:.1f}s ({os.path.getsize(target_path):,} bytes)", flush=True)
            return spec["filename"], True

        except Exception as e:
            dt = time.time() - t0
            print(f"[Error] {spec['filename']} attempt {attempt} failed ({dt:.1f}s): {e}", flush=True)
            time.sleep(2)

    return spec["filename"], False

def main():
    print(f"[Generator] Concurrently generating {len(ASSETS_TO_GENERATE)} assets...", flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(generate_asset, spec): spec for spec in ASSETS_TO_GENERATE}
        results = {}
        for future in as_completed(futures):
            spec = futures[future]
            try:
                fname, ok = future.result()
                results[fname] = ok
            except Exception as e:
                print(f"[Crash] {spec['filename']}: {e}", flush=True)
                results[spec['filename']] = False

    print("\n[Summary]:", flush=True)
    for fname, ok in results.items():
        status = "OK" if ok else "FAILED"
        print(f"  {fname}: {status}", flush=True)

if __name__ == "__main__":
    main()
