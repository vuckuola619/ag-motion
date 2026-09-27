import os
import sys
import json
import time
import base64
import urllib.request
import urllib.error
import numpy as np
from PIL import Image

ROUTER_URL = "http://127.0.0.1:20128/v1/images/generations"
API_KEY = "Bearer sk-c4f2444795b190b3-kzvd4h-ea839762"
MODEL = "cx/gpt-5.5-image"

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_DIR = os.path.join(PROJECT_ROOT, "assets", "episode6_project_azorian", "images")
os.makedirs(TARGET_DIR, exist_ok=True)

NEW_SPECS = [
    {
        "filename": "soviet_dp5v_dosimeter.png",
        "type": "cutout",
        "prompt": "Authentic Soviet military DP-5V radiation dosimeter radiometer with cylindrical Geiger probe on coiled cable, metal dial gauge, olive drab steel case, isolated on pure white background, studio catalog cutout, 8k"
    },
    {
        "filename": "manganese_nodule_specimen.png",
        "type": "cutout",
        "prompt": "Deep sea manganese nodule rock specimen, dark porous textured mineral nodule with rough surface, Howard Hughes mining cover story evidence, isolated on pure white background, museum specimen display, 8k"
    },
    {
        "filename": "heavy_pipe_string_elevator.png",
        "type": "cutout",
        "prompt": "Heavy industrial offshore derrick pipe string elevator coupling lifting collar, massive forged steel machinery component, isolated on pure white background, 8k"
    }
]

def make_transparent_cutout(img):
    img = img.convert("RGBA")
    arr = np.array(img, dtype=np.float32)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

    # White / off-white background threshold
    brightness = (r + g + b) / 3.0
    is_white = (r > 240) & (g > 240) & (b > 240)
    arr[is_white, 3] = 0

    # Soft feathering at border
    is_near_white = (brightness > 215) & (~is_white)
    alpha_scale = np.clip((240.0 - brightness) / 25.0, 0.0, 1.0)
    arr[is_near_white, 3] = arr[is_near_white, 3] * alpha_scale[is_near_white]

    return Image.fromarray(arr.astype(np.uint8), "RGBA")

def generate_via_9router(spec):
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
    req = urllib.request.Request(ROUTER_URL, data=data, headers=headers)
    print(f"Generating via 9router {MODEL}: {spec['filename']}...")
    try:
        with urllib.request.urlopen(req, timeout=120) as res:
            res_json = json.loads(res.read().decode("utf-8"))
            b64_str = res_json["data"][0]["b64_json"]
            raw_bytes = base64.b64decode(b64_str)
            raw_path = os.path.join(TARGET_DIR, "raw_" + spec["filename"])
            with open(raw_path, "wb") as f:
                f.write(raw_bytes)
            
            with Image.open(raw_path) as im:
                cutout = make_transparent_cutout(im)
                final_path = os.path.join(TARGET_DIR, spec["filename"])
                cutout.save(final_path, "PNG")
                print(f"[OK] Saved {final_path} ({round(os.path.getsize(final_path)/1024, 1)} KB)")
            if os.path.exists(raw_path):
                os.remove(raw_path)
    except Exception as e:
        print(f"[ERROR] Failed {spec['filename']}: {e}")

if __name__ == "__main__":
    for spec in NEW_SPECS:
        generate_via_9router(spec)
