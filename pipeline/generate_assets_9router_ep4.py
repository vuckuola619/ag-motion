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

ASSET_SPECS = [
    {
        "filename": "asteroid_atmospheric_entry.png",
        "type": "card",
        "prompt": "A massive 10-kilometer asteroid enters Earth's atmosphere at 45,000 miles per hour, blazing incandescent fireball with blinding ionized shockwave trail, cosmic heat radiating across space, view from lower Earth orbit overlooking the curvature of the blue planet and shallow Cretaceous oceans, cinematic BBC documentary style, 8k",
        "title": "Asteroid Atmospheric Entry"
    },
    {
        "filename": "trex_skull_specimen.png",
        "type": "cutout",
        "prompt": "Tyrannosaurus rex fossil skull museum specimen, massive bone structure with serrated banana-sized teeth, dark mineralized fossilized bone texture with suture lines, Smithsonian museum catalog display, isolated on pure white background, crisp edge cutout, studio specimen lighting, 8k",
        "title": "Tyrannosaurus Rex Skull Specimen"
    },
    {
        "filename": "iridium_core_sample.png",
        "type": "cutout",
        "prompt": "Cylindrical geological rock drill core sample showing the distinct Cretaceous-Paleogene (K-Pg) boundary extinction clay layer, dark gray iridium-rich asteroid fallout band sandwiched between white limestone, museum geological specimen, isolated on pure white background, 8k",
        "title": "Iridium K-Pg Boundary Core Sample"
    },
    {
        "filename": "chicxulub_crater_impact.png",
        "type": "card",
        "prompt": "The moment of the Chicxulub asteroid impact on the shallow Yucatan sea, blinding 100-million-megaton kinetic nuclear fireball explosion vaporizing limestone bedrock, supersonic shockwave blasting seawater and crust into outer space, catastrophic planetary explosion, 8k",
        "title": "Chicxulub Ground Zero Impact"
    },
    {
        "filename": "shocked_quartz_specimen.png",
        "type": "cutout",
        "prompt": "Museum mineral specimen of shocked quartz grain with distinct microscopic parallel planar deformation features (PDFs) created by extreme meteorite impact shock pressures, isolated on pure white background, geological catalog display, 8k",
        "title": "Shocked Quartz Mineral Specimen"
    },
    {
        "filename": "impact_fireball_plume.png",
        "type": "cutout",
        "prompt": "Gigantic incandescent asteroid impact vapor and pulverized molten rock plume erupting 40 kilometers straight into the upper atmosphere, glowing plasma fireball column with lightning discharges, isolated on pure white background, crisp cutout, 8k",
        "title": "Impact Fireball Ejecta Plume"
    },
    {
        "filename": "incandescent_sky_wildfire.png",
        "type": "card",
        "prompt": "Global thermal radiation pulse from re-entering asteroid ejecta, glowing incandescent blood-orange infrared sky turning the Earth into a broiler oven, continental Cretaceous forests engulfed in spontaneous firestorms, smoke and ash filling the horizon, 8k",
        "title": "Global Thermal Radiation Wildfire"
    },
    {
        "filename": "burned_dino_claw_bone.png",
        "type": "cutout",
        "prompt": "Fossilized raptor dinosaur sickle foot claw embedded in dark Cretaceous charcoal and carbonized wood ash layer, paleontology museum specimen, isolated on pure white background, crisp cutout, studio lighting, 8k",
        "title": "Carbonized Dinosaur Claw Specimen"
    },
    {
        "filename": "tektite_glass_specimens.png",
        "type": "cutout",
        "prompt": "Cluster of natural aerodynamic black impact tektites, splash-form glass teardrops and dumbbell-shaped micro-meteorite impact glass formed from vaporized rock, museum display, isolated on pure white background, 8k",
        "title": "Impact Tektite Glass Specimen"
    },
    {
        "filename": "megatsunami_inundation.png",
        "type": "card",
        "prompt": "Colossal 300-meter megatsunami wave crashing violently into Cretaceous coastal floodplains, churning black water uprooting prehistoric trees and depositing chaotically jumbled fossil debris, cinematic BBC science documentary, 8k",
        "title": "300-Meter Caribbean Megatsunami"
    },
    {
        "filename": "impact_winter_landscape.png",
        "type": "card",
        "prompt": "Apocalyptic impact winter landscape, the sun completely blacked out by thick atmospheric soot and sulfur aerosols, dark gray ash snow falling over frozen desolate terrain and skeletal dinosaur remains, -30 degrees Celsius freezing darkness, 8k",
        "title": "The Decadal Impact Winter"
    },
    {
        "filename": "kpg_boundary_clay_slab.png",
        "type": "cutout",
        "prompt": "Polished museum stratigraphic rock slab showing the razor-sharp K-Pg boundary soot and clay layer separating the age of dinosaurs from the age of mammals, museum exhibit with metric scale ruler, isolated on pure white background, 8k",
        "title": "K-Pg Boundary Stratigraphic Slab"
    },
    {
        "filename": "purgatorius_early_mammal.png",
        "type": "cutout",
        "prompt": "Reconstructed fossil skeleton of Purgatorius, tiny Cretaceous burrowing mammal with grasping claws and omnivorous teeth, paleontological museum display, isolated on pure white background, crisp specimen cutout, 8k",
        "title": "Purgatorius Proto-Mammal Skeleton"
    },
    {
        "filename": "mammal_trackway_fern_slab.png",
        "type": "card",
        "prompt": "Cretaceous-Paleogene boundary fern spike fossil slab, delicate fossilized fern fronds covering gray volcanic ash bed with tiny early mammal footprints walking across the silt, dramatic paleontology museum lighting, 8k",
        "title": "Post-Extinction Fern Spike Slab"
    }
]

def make_transparent_cutout(img):
    img = img.convert("RGBA")
    arr = np.array(img)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

    # White / off-white background threshold
    is_white = (r > 240) & (g > 240) & (b > 240)
    arr[is_white, 3] = 0

    # Soft feathering at border
    is_near_white = (r > 220) & (g > 220) & (b > 220) & (~is_white)
    avg = (r.astype(float) + g.astype(float) + b.astype(float)) / 3.0
    alpha_scale = np.clip((240.0 - avg) / 20.0, 0.0, 1.0)
    arr[is_near_white, 3] = (arr[is_near_white, 3].astype(float) * alpha_scale[is_near_white]).astype(np.uint8)

    return Image.fromarray(arr, "RGBA")

def generate_asset(spec, output_path, max_retries=3):
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
    
    for attempt in range(1, max_retries + 1):
        t0 = time.time()
        print(f"  [9Router cx/gpt-5.5-image] Generating: {spec['filename']} (Attempt {attempt}/{max_retries})...", flush=True)
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
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
                        if spec["type"] == "cutout":
                            cutout = make_transparent_cutout(im)
                            cutout.save(output_path, "PNG")
                        else:
                            im.convert("RGB").save(output_path, "PNG")
                    
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    
                    dt = round(time.time() - t0, 1)
                    sz = round(os.path.getsize(output_path) / 1024, 1)
                    print(f"  [9Router SUCCESS] Saved {spec['filename']} ({sz} KB) in {dt}s", flush=True)
                    return True
        except urllib.error.HTTPError as e:
            print(f"  [9Router HTTPError {e.code}]: {e.reason}", flush=True)
        except Exception as e:
            print(f"  [9Router Error]: {e}", flush=True)
        
        if attempt < max_retries:
            print("  Retrying in 5 seconds...", flush=True)
            time.sleep(5)
            
    return False

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    images_dir = os.path.join(project_dir, "assets", "episode4_chicxulub", "images")
    os.makedirs(images_dir, exist_ok=True)
    
    # Ensure archive seal is present
    seal_src = os.path.join(project_dir, "assets", "episode3_carnian_pluvial", "images", "archive_seal.png")
    seal_dst = os.path.join(images_dir, "archive_seal.png")
    if os.path.exists(seal_src) and not os.path.exists(seal_dst):
        import shutil
        shutil.copyfile(seal_src, seal_dst)
    
    print("===================================================================")
    print("  9ROUTER CX/GPT-5.5-IMAGE PIPELINE FOR EPISODE 4: CHICXULUB IMPACT  ")
    print("===================================================================")
    print(f"Target Directory: {images_dir}")
    print(f"Model: {MODEL} | Endpoint: {ROUTER_URL}\n", flush=True)
    
    results = []
    t_start = time.time()
    
    for i, spec in enumerate(ASSET_SPECS, 1):
        out_file = os.path.join(images_dir, spec["filename"])
        if os.path.exists(out_file) and os.path.getsize(out_file) > 10000:
            print(f"[{i}/{len(ASSET_SPECS)}] Already exists: {spec['filename']} ({round(os.path.getsize(out_file)/1024, 1)} KB). Skipping.", flush=True)
            results.append((spec["filename"], True, "cached"))
            continue
            
        print(f"\n[{i}/{len(ASSET_SPECS)}] Processing: {spec['title']}", flush=True)
        success = generate_asset(spec, out_file)
        results.append((spec["filename"], success, "generated" if success else "failed"))
        time.sleep(1)
        
    total_time = round(time.time() - t_start, 1)
    print("\n===================================================================")
    print(f"  ASSET GENERATION COMPLETE IN {total_time}s")
    print("===================================================================")
    for fn, succ, st in results:
        status_sym = "[OK]" if succ else "[FAILED]"
        print(f"  {status_sym} {fn:35s} -> {st}", flush=True)

if __name__ == "__main__":
    main()
