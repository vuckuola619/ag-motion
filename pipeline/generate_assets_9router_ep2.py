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
        "filename": "gorgonopsian_skull.png",
        "type": "cutout",
        "prompt": "Full fossil skull of Inostrancevia Gorgonopsian, large saber-toothed prehistoric synapsid apex predator, museum catalog specimen, prominent elongated dagger saber canine teeth, weathered bone textures and sutures, side profile, isolated on pure white background, studio catalog lighting, crisp edges, no background shadows, 8k",
        "title": "Gorgonopsian Saber-Tooth Skull"
    },
    {
        "filename": "trilobite_fossil.png",
        "type": "cutout",
        "prompt": "Prehistoric marine Trilobite fossil specimen preserved in dark crystalline calcite matrix, detailed segmented thoracic exoskeleton, ribbed pleurae, compound eye facets, museum paleontology artifact, isolated on pure white background, high contrast studio lighting, 8k",
        "title": "Marine Trilobite Fossil Specimen"
    },
    {
        "filename": "permian_jungle.png",
        "type": "card",
        "prompt": "Prehistoric Late Permian lush tropical forest landscape, towering Glossopteris gymnosperms, giant Calamites horsetails and tree ferns, humid golden mist, primeval biodiversity paradise before mass extinction, cinematic documentary photography, 8k",
        "title": "Permian Primeval Jungle Biome"
    },
    {
        "filename": "siberian_basalt_flood.png",
        "type": "cutout",
        "prompt": "Massive fractured volcanic block of black Siberian basalt crust with glowing red-hot molten lava fissures bursting through cracks, liquid magma droplets and fiery thermal glow, isolated on pure white background, crisp edge cutout, 8k",
        "title": "Siberian Flood Basalt Lava Block"
    },
    {
        "filename": "mantle_plume.png",
        "type": "card",
        "prompt": "Siberian Traps catastrophic volcanic flood basalt eruption, continental crust ripped open with towering 500-meter magma fire fountains, glowing orange rivers of lava spreading across burning landscape under ash skies, geological aerial photography, 8k",
        "title": "Siberian Traps Mantle Plume Eruption"
    },
    {
        "filename": "basalt_rock_specimen.png",
        "type": "cutout",
        "prompt": "Cylindrical geological rock drill core sample of porous vesicular volcanic flood basalt, visible gas cavities and green olivine crystal inclusions, scientific paleontology specimen, isolated on pure white background, catalog lighting, 8k",
        "title": "Vesicular Basalt Core Sample"
    },
    {
        "filename": "toxic_smoke_plume.png",
        "type": "cutout",
        "prompt": "Towering billowy volcanic coal fire smoke plume rising into the stratosphere, dense dark sulfur ash clouds illuminated from within by glowing fiery embers and purple volcanic lightning arcs, isolated on pure white background, crisp cutout silhouette, 8k",
        "title": "Stratospheric Coal Fire Smoke Plume"
    },
    {
        "filename": "acid_rain_forest.png",
        "type": "card",
        "prompt": "Prehistoric forest devastated and dissolved by concentrated sulfuric acid rain, stripped bleached dead tree skeletons, caustic neon yellow-green toxic acid puddles on barren ground, murky sulfur smog haze, archival documentary photography, 8k",
        "title": "Acid Rain Defoliated Wasteland"
    },
    {
        "filename": "anoxic_water_sample.png",
        "type": "cutout",
        "prompt": "Antique laboratory scientific glass flask specimen filled with eerie dark purple anoxic seawater, tiny rising bubbles of hydrogen sulfide gas, vintage paper specimen label, isolated on pure white background, clean transparent glass cutout, 8k",
        "title": "Anoxic Purple Seawater Lab Sample"
    },
    {
        "filename": "purple_toxic_ocean.png",
        "type": "card",
        "prompt": "Canfield ocean mass extinction shoreline, sea water turned alien deep purple and magenta by purple sulfur bacteria, foaming toxic greenish-yellow surf, stranded dead ammonite shells and trilobites on sulfur-crusted desolate beach, eerie dusk lighting, 8k",
        "title": "Canfield Purple Euxinic Ocean"
    },
    {
        "filename": "fungal_spike_fossil.png",
        "type": "cutout",
        "prompt": "Geological black shale rock slab preserved with microscopic and macroscopic fossilized white branching fungal hyphae mycelium networks and spore clusters, Permian-Triassic fungal spike disaster layer, museum paleontology specimen, isolated on pure white background, 8k",
        "title": "PT Boundary Fungal Spike Fossil"
    },
    {
        "filename": "barren_earth_landscape.png",
        "type": "card",
        "prompt": "Desolate post-extinction barren continental landscape, severe erosion gullies in dry red mudstone badlands, zero trees or living vegetation, cracked lifeless mudflats under harsh bleached sky, complete biological silence, 8k",
        "title": "Post-Collapse Treeless Wasteland"
    },
    {
        "filename": "lystrosaurus_fossil.png",
        "type": "cutout",
        "prompt": "Fossil skeleton and skull of Lystrosaurus burrowing dicynodont survivor, distinctive downturned snout with two protruding tusk fangs, robust digging forelimbs and claws, museum paleontology specimen, isolated on pure white background, crisp cutout, 8k",
        "title": "Lystrosaurus Survivor Fossil"
    },
    {
        "filename": "early_dino_tracks.png",
        "type": "cutout",
        "prompt": "Triassic sandstone rock slab preserved with clear three-toed tridactyl fossil footprints of early dinosaur Eoraptor, sharp claw marks and sediment displacement rims, museum paleontology specimen, isolated on pure white background, crisp cutout, 8k",
        "title": "Early Dinosaur Fossil Trackway Slab"
    }
]

def make_transparent_cutout(img: Image.Image, threshold: int = 242) -> Image.Image:
    """Isolate pure white/near-white background to transparent RGBA with soft feathering."""
    img = img.convert("RGBA")
    arr = np.array(img)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    
    is_white = (r > threshold) & (g > threshold) & (b > threshold)
    diff = np.maximum.reduce([255 - r, 255 - g, 255 - b])
    alpha_soft = np.clip(diff * 5, 0, 255).astype(np.uint8)
    
    new_a = np.where(is_white, alpha_soft, a)
    arr[:, :, 3] = new_a
    return Image.fromarray(arr, "RGBA")

def generate_via_9router(spec: dict, output_path: str, max_retries: int = 2) -> bool:
    payload = {
        "model": MODEL,
        "prompt": spec["prompt"],
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
    
    for attempt in range(1, max_retries + 1):
        t0 = time.time()
        print(f"  [9Router cx/gpt-5.5-image] Generating: {spec['filename']} (Attempt {attempt}/{max_retries})...", flush=True)
        try:
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
    images_dir = os.path.join(project_dir, "assets", "episode2_great_dying", "images")
    os.makedirs(images_dir, exist_ok=True)
    
    print("===================================================================")
    print("  9ROUTER CX/GPT-5.5-IMAGE PIPELINE FOR EPISODE 2: THE GREAT DYING ")
    print("===================================================================")
    print(f"Target Directory: {images_dir}")
    print(f"Model: {MODEL} | Endpoint: {ROUTER_URL}\n")
    
    results = []
    total_start = time.time()
    
    for i, spec in enumerate(ASSET_SPECS, 1):
        out_file = os.path.join(images_dir, spec["filename"])
        print(f"\n[{i}/{len(ASSET_SPECS)}] {spec['title']} -> {spec['filename']}")
        
        ok = generate_via_9router(spec, out_file)
        results.append((spec["filename"], ok))
        # Brief pause between requests to prevent API rate limiting
        time.sleep(2)
        
    total_time = round(time.time() - total_start, 1)
    print("\n===================================================================")
    print(f"  ALL 14 ASSETS PROCESSED IN {total_time}s")
    print("===================================================================")
    for fname, ok in results:
        status = "✓ OK" if ok else "✗ FAILED"
        print(f"  {status}: {fname}")

if __name__ == "__main__":
    main()
