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
        "filename": "pangea_desert_landscape.png",
        "type": "card",
        "prompt": "Prehistoric Late Triassic central Pangea desert landscape, vast red sand dunes, sun-bleached cracked mudflats, mirage heatwaves under a scorching pale yellow sky, primeval arid desert biome, cinematic BBC documentary landscape photography, 8k",
        "title": "Arid Pangea Desert Biome"
    },
    {
        "filename": "rhynchosaur_skull.png",
        "type": "cutout",
        "prompt": "Fossil skull of Hyperodapedon rhynchosaur, primitive beaked herbivorous reptile with massive beak-like premaxilla, heavy dental battery plates, paleontology museum catalog specimen, weathered fossilized bone, isolated on pure white background, crisp edge cutout, studio specimen lighting, 8k",
        "title": "Hyperodapedon Rhynchosaur Skull"
    },
    {
        "filename": "cracked_earth_specimen.png",
        "type": "cutout",
        "prompt": "Cylindrical geological rock drill core sample of Triassic red mudstone with fossil mudcracks and salt crystal pseudomorphs, museum geological specimen, isolated on pure white background, studio lighting, 8k",
        "title": "Triassic Red-Bed Core Sample"
    },
    {
        "filename": "wrangellia_basalt_plateau.png",
        "type": "card",
        "prompt": "Underwater submarine Wrangellia volcanic flood basalt eruption in the Panthalassa ocean, glowing molten basalt lava pillows bursting on the seabed, colossal boiling steam and sulfur plumes exploding into the atmosphere, dramatic geological aerial view, 8k",
        "title": "Wrangellia Oceanic Super-Volcano"
    },
    {
        "filename": "wrangellia_lava_pillow.png",
        "type": "cutout",
        "prompt": "Deep-sea submarine pillow basalt volcanic rock specimen with dark glassy quenching crust, red oxidized fractures, museum oceanographic geology artifact, isolated on pure white background, crisp cutout, 8k",
        "title": "Submarine Pillow Basalt Specimen"
    },
    {
        "filename": "steam_plume_cutout.png",
        "type": "cutout",
        "prompt": "Towering volcanic steam plume and superheated sulfur cloud column rising violently, turbulent boiling gas texture with micro lightning sparks, isolated on pure white background, crisp cutout, 8k",
        "title": "Volcanic Steam & Ash Column"
    },
    {
        "filename": "carnian_monsoon_sky.png",
        "type": "card",
        "prompt": "The Carnian Pluvial Event global storm, apocalyptic torrential monsoon rainstorm battering ancient Triassic canyons, colossal bruised violet cumulonimbus storm clouds, massive vertical rain sheets, jagged fork lightning, cinematic documentary photography, 8k",
        "title": "The 2-Million-Year Torrential Monsoon"
    },
    {
        "filename": "muddy_fluvial_delta.png",
        "type": "cutout",
        "prompt": "Violent churning muddy red river flood current carrying eroded silt and broken prehistoric branches, dynamic splashing river water cut-out, isolated on pure white background, high-speed photography, crisp edges, 8k",
        "title": "Churning Fluvial Flood Current"
    },
    {
        "filename": "carnian_amber_droplet.png",
        "type": "cutout",
        "prompt": "Ancient Triassic golden amber droplet tear with translucent honey resin glow, containing microscopic trapped prehistoric conifer spores and primitive insect inclusions, museum paleontology specimen, isolated on pure white background, macro studio photography, 8k",
        "title": "Triassic Amber Droplet Specimen"
    },
    {
        "filename": "triassic_conifer_forest.png",
        "type": "card",
        "prompt": "Dense humid tropical Triassic conifer swamp forest, towering Voltzia conifers and giant Equisetum horsetails dripping with heavy rainwater, misty primordial jungle floor, lush dark green canopy, cinematic documentary photography, 8k",
        "title": "Carnian Conifer Swamp Forest"
    },
    {
        "filename": "dying_rhynchosaur_fossil.png",
        "type": "card",
        "prompt": "Paleontology excavation bonebed slab showing fossilized articulated skeletons of Hyperodapedon rhynchosaurs drowned and buried in thick Carnian gray river mudstone, exposed fossil bones, scientific field photography, 8k",
        "title": "Carnian Bonebed Extinction Horizon"
    },
    {
        "filename": "fossil_leaf_mat.png",
        "type": "cutout",
        "prompt": "Compressed carbonized fossil conifer needle and fern leaf mat in gray shale matrix, paleobotanical museum slab specimen, isolated on pure white background, studio catalog lighting, 8k",
        "title": "Voltzia Conifer Leaf Mat Slab"
    },
    {
        "filename": "herrerasaurus_fossil_skeleton.png",
        "type": "cutout",
        "prompt": "Full articulated fossil skeleton of Herrerasaurus, predatory early bipedal dinosaur, sharp recurved teeth, long grasping clawed arms, slender running hindlimbs, museum mount specimen, isolated on pure white background, crisp studio lighting, 8k",
        "title": "Herrerasaurus Early Dinosaur Skeleton"
    },
    {
        "filename": "dino_trackway_mudstone.png",
        "type": "card",
        "prompt": "Large fossil trackway slab of early three-toed dinosaur footprints pressed deeply into rippled wet prehistoric river mudstone, dramatic raking side lighting casting long shadows across claw impressions, museum specimen, 8k",
        "title": "Carnian Dinosaur Trackway Slab"
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
    images_dir = os.path.join(project_dir, "assets", "episode3_carnian_pluvial", "images")
    os.makedirs(images_dir, exist_ok=True)
    
    # Also ensure archive seal is present
    seal_src = os.path.join(project_dir, "assets", "episode2_great_dying", "images", "archive_seal.png")
    seal_dst = os.path.join(images_dir, "archive_seal.png")
    if os.path.exists(seal_src) and not os.path.exists(seal_dst):
        import shutil
        shutil.copyfile(seal_src, seal_dst)
    
    print("===================================================================")
    print("  9ROUTER CX/GPT-5.5-IMAGE PIPELINE FOR EPISODE 3: CARNIAN PLUVIAL  ")
    print("===================================================================")
    print(f"Target Directory: {images_dir}")
    print(f"Model: {MODEL} | Endpoint: {ROUTER_URL}\n")
    
    results = []
    t_start = time.time()
    
    for i, spec in enumerate(ASSET_SPECS, 1):
        out_file = os.path.join(images_dir, spec["filename"])
        if os.path.exists(out_file) and os.path.getsize(out_file) > 10000:
            print(f"[{i}/{len(ASSET_SPECS)}] Already exists: {spec['filename']} ({round(os.path.getsize(out_file)/1024, 1)} KB). Skipping.")
            results.append((spec["filename"], True, "cached"))
            continue
            
        print(f"\n[{i}/{len(ASSET_SPECS)}] Processing: {spec['title']}")
        success = generate_asset(spec, out_file)
        results.append((spec["filename"], success, "generated" if success else "failed"))
        time.sleep(1)
        
    total_time = round(time.time() - t_start, 1)
    print("\n===================================================================")
    print(f"  ASSET GENERATION COMPLETE IN {total_time}s")
    print("===================================================================")
    for fn, succ, st in results:
        status_sym = "[OK]" if succ else "[FAILED]"
        print(f"  {status_sym} {fn:35s} -> {st}")

if __name__ == "__main__":
    main()
