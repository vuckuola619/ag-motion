import os
import sys
import json
import time
import base64
import urllib.request
import urllib.error
import numpy as np
from PIL import Image

def safe_print(*args, **kwargs):
    kwargs.pop("flush", None)
    try:
        print(*args, **kwargs)
    except Exception:
        pass

ROUTER_URL = "http://127.0.0.1:20128/v1/images/generations"
API_KEY = "Bearer sk-c4f2444795b190b3-kzvd4h-ea839762"
MODEL = "cx/gpt-5.5-image"

ASSET_SPECS = [
    # Beat 1: The Crime Scene & 1-Centimeter Seam
    {
        "filename": "gubbio_boundary_cliff.png",
        "type": "card",
        "prompt": "Geological cliff face outcrop in Bottaccione Gorge Gubbio Italy, sharp razor-thin 1-centimeter dark gray boundary clay layer sharply separating pink Scaglia Rossa Cretaceous limestone below and white Tertiary limestone above, geological field photography, documentary 8k",
        "title": "Gubbio Limestone Boundary Cliff"
    },
    {
        "filename": "vintage_magnifying_glass.png",
        "type": "cutout",
        "prompt": "Vintage brass magnifying glass with circular glass lens, antique polished metal rim and dark ebony wooden handle, isolated on pure white background, crisp edge cutout, studio product photography, 8k",
        "title": "Vintage Brass Magnifying Glass"
    },
    {
        "filename": "forensic_centimeter_ruler.png",
        "type": "cutout",
        "prompt": "High-contrast forensic geological macro scale metric ruler, 1 centimeter measurement with black and white millimeter ticks, forensic evidence marker, isolated on pure white background, crisp cutout, 8k",
        "title": "1-Centimeter Forensic Scale Ruler"
    },
    {
        "filename": "geologist_rock_pick.png",
        "type": "cutout",
        "prompt": "Steel geological rock pick hammer with blue vinyl shock reduction handle, sharp pointed chisel pick head, authentic field geology tool, isolated on pure white background, studio catalog display, 8k",
        "title": "Geologist Rock Pick Hammer"
    },

    # Beat 2: The Forensic Lab & 30x Iridium Spike
    {
        "filename": "lab_vial_boundary_clay.png",
        "type": "cutout",
        "prompt": "Clear glass laboratory specimen sample vial containing dark gray pulverized Cretaceous-Paleogene boundary clay sediment, black screw cap with white analytical label, isolated on pure white background, 8k",
        "title": "Laboratory Vial with Boundary Clay"
    },
    {
        "filename": "iridium_spike_chart.png",
        "type": "card",
        "prompt": "Vintage 1980 Lawrence Berkeley Laboratory scientific paper chart, dramatic line graph showing flat baseline 0.3 ppb iridium suddenly shooting vertically into massive 30-times spike peak at 66 Ma boundary, authentic academic paper scan with typewriter labels, 8k",
        "title": "1980 Iridium 30x Spike Scientific Graph"
    },
    {
        "filename": "radioactive_hazard_tag.png",
        "type": "cutout",
        "prompt": "Weathered yellow radioactive isotope sample evidence tag with black trefoil radiation symbol, forensic laboratory specimen string tag reading NEUTRON ACTIVATION ANALYSIS, isolated on pure white background, 8k",
        "title": "Radioactive Hazard Evidence Tag"
    },

    # Beat 3: The Cosmic Suspect & Deep Space
    {
        "filename": "metallic_asteroid_orbit.png",
        "type": "card",
        "prompt": "A menacing 6-mile-wide metallic carbonaceous chondrite asteroid hurtling through space near Earth, cratered metallic nickel-iron surface glowing under harsh sunlight, blue curve of Cretaceous Earth in background, cinematic documentary style, 8k",
        "title": "6-Mile Metallic Asteroid in Orbit"
    },
    {
        "filename": "iridium_ingot_badge.png",
        "type": "cutout",
        "prompt": "Solid lustrous silvery-white iridium metal element 77 specimen cube ingot, metallic crystalline reflection, museum element sample display, isolated on pure white background, crisp cutout, 8k",
        "title": "Iridium Element 77 Ingot Specimen"
    },
    {
        "filename": "cosmic_dust_particle.png",
        "type": "cutout",
        "prompt": "Microscopic extraterrestrial asteroid dust grain, porous chondritic interplanetary dust particle with glassy spherules, scanning electron microscope display, isolated on pure white background, 8k",
        "title": "Chondritic Cosmic Dust Grain"
    },

    # Beat 4: The Crater Hunt & Yucatan Gravity Anomaly
    {
        "filename": "yucatan_gravity_anomaly_map.png",
        "type": "card",
        "prompt": "3D geophysical satellite gravity anomaly map of Yucatan peninsula Mexico, showing the buried circular concentric rings of the 180-kilometer Chicxulub impact crater beneath the coastline and Gulf of Mexico, false-color blue green and red gravity gradient, 8k",
        "title": "Yucatan Satellite Gravity Anomaly Map"
    },
    {
        "filename": "radar_targeting_reticle.png",
        "type": "cutout",
        "prompt": "Tactical scientific radar crosshair targeting reticle, glowing orange-yellow circular concentric coordinate rings with digital distance calipers marking 180 KM CRATER DIAMETER, isolated on pure white background, 8k",
        "title": "Radar Crater Targeting Reticle"
    },
    {
        "filename": "ocean_oil_rig_platform.png",
        "type": "cutout",
        "prompt": "Offshore marine oil drilling platform rig in the Gulf of Mexico, industrial steel derrick structure standing in turquoise Caribbean sea, isolated on pure white background, crisp cutout, 8k",
        "title": "Offshore Oil Drilling Exploration Rig"
    },

    # Beat 5: The Forensic Fingerprint: Glass Tektites & Drill Cores
    {
        "filename": "black_glass_tektites.png",
        "type": "cutout",
        "prompt": "Group of aerodynamic black glassy micro-tektites and splash-form impactite glass teardrop beads created by meteorite impact, shiny vitreous obsidian texture, isolated on pure white background, macro specimen display, 8k",
        "title": "Aerodynamic Black Glass Tektites"
    },
    {
        "filename": "ocean_drill_core_slab.png",
        "type": "cutout",
        "prompt": "Cylindrical ocean drilling program rock core tube specimen showing the dark gray impact fallout boundary layer sandwiched between light marine sediments, metric geological core sleeve, isolated on pure white background, 8k",
        "title": "Ocean Drilling Extinction Core Tube"
    },

    # Beat 6: Case Closed & Human Legacy
    {
        "filename": "walter_alvarez_polaroid.png",
        "type": "card",
        "prompt": "Vintage 1980s color archival polaroid photo of geologist Walter Alvarez pointing with his finger at the thin dark K-Pg boundary layer on an Italian limestone cliff, authentic vintage film grain and white photo frame border, 8k",
        "title": "Archival Photo of Walter Alvarez"
    },
    {
        "filename": "case_closed_stamp.png",
        "type": "cutout",
        "prompt": "Distressed red rubber stamp imprint inside rectangular border reading 'INVESTIGATION SOLVED // K-PG EXTINCTION', weathered ink texture, isolated on pure white background, 8k",
        "title": "Red Case Closed Rubber Stamp"
    },
    {
        "filename": "scotch_tape_piece.png",
        "type": "cutout",
        "prompt": "Strip of yellowed semi-transparent frosted scotch tape with slightly crinkled torn adhesive edges, isolated on pure white background, macro photography, 8k",
        "title": "Frosted Scotch Tape Strip"
    }
]

def make_transparent_cutout(img):
    img = img.convert("RGBA")
    arr = np.array(img)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

    # White / off-white background threshold
    is_white = (r > 238) & (g > 238) & (b > 238)
    arr[is_white, 3] = 0

    # Soft feathering at border
    is_near_white = (r > 218) & (g > 218) & (b > 218) & (~is_white)
    avg = (r.astype(float) + g.astype(float) + b.astype(float)) / 3.0
    alpha_scale = np.clip((238.0 - avg) / 20.0, 0.0, 1.0)
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
        safe_print(f"  [9Router cx/gpt-5.5-image] Generating: {spec['filename']} (Attempt {attempt}/{max_retries})...", flush=True)
        try:
            with urllib.request.urlopen(req, timeout=90) as response:
                result = json.loads(response.read().decode("utf-8"))
                b64_data = result["data"][0]["b64_json"]
                img_bytes = base64.b64decode(b64_data)
                
                temp_raw_path = output_path + ".tmp.png"
                with open(temp_raw_path, "wb") as f:
                    f.write(img_bytes)
                
                img = Image.open(temp_raw_path)
                
                if spec["type"] == "cutout":
                    safe_print(f"    -> Applying transparent alpha cutout for {spec['filename']}...", flush=True)
                    img = make_transparent_cutout(img)
                
                img.save(output_path, "PNG", optimize=True)
                if os.path.exists(temp_raw_path):
                    os.remove(temp_raw_path)
                    
                dur = time.time() - t0
                size_kb = os.path.getsize(output_path) / 1024.0
                safe_print(f"  [SUCCESS] Saved {spec['filename']} ({size_kb:.1f} KB in {dur:.1f}s)\n", flush=True)
                return True
                
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            safe_print(f"  [HTTP Error {e.code}] {err_body}", flush=True)
            time.sleep(3)
        except Exception as e:
            safe_print(f"  [Network/IO Error] {e}", flush=True)
            time.sleep(3)
            
    safe_print(f"  [FAILED] Could not generate {spec['filename']} after {max_retries} attempts.", flush=True)
    return False

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    img_dir = os.path.join(project_dir, "assets", "episode5_iridium_layer", "images")
    os.makedirs(img_dir, exist_ok=True)
    
    total = len(ASSET_SPECS)
    safe_print(f"===========================================================", flush=True)
    safe_print(f"  9Router cx/gpt-5.5-image Generator — Episode 5 (Vox Style) ", flush=True)
    safe_print(f"  Target: {total} Production Assets (Cards & Transparent Cutouts)", flush=True)
    safe_print(f"  Model: {MODEL} | Endpoint: {ROUTER_URL}\n", flush=True)
    safe_print(f"===========================================================\n", flush=True)
    
    generated_count = 0
    skipped_count = 0
    
    for i, spec in enumerate(ASSET_SPECS, start=1):
        target_path = os.path.join(img_dir, spec["filename"])
        safe_print(f"[{i}/{total}] {spec['title']} ({spec['type'].upper()})", flush=True)
        
        if os.path.exists(target_path) and os.path.getsize(target_path) > 10000:
            safe_print(f"  [SKIP] File already exists: {spec['filename']}\n", flush=True)
            skipped_count += 1
            continue
            
        success = generate_asset(spec, target_path)
        if success:
            generated_count += 1
            time.sleep(1.0)
            
    safe_print(f"\n[Summary Ep5] Finished: {generated_count} generated, {skipped_count} skipped, total {total} assets ready.")

if __name__ == "__main__":
    main()
