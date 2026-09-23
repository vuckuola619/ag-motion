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

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "episode5_iridium_layer", "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

NEW_ASSETS = [
    # 1. Background Archival Documents (Full Canvas Fill, zero blank space)
    {
        "filename": "bg_gubbio_stratigraphic_map.png",
        "type": "card",
        "prompt": "Vintage 1970s Italian Geological Survey topographical stratigraphy map of Umbria Gubbio, showing Bottaccione Gorge, geological fault lines, vintage colored lithologic strata keys, aged sepia paper texture, archival survey document, 8k",
        "title": "Gubbio Geological Stratigraphic Map"
    },
    {
        "filename": "bg_berkeley_lab_dossier.png",
        "type": "card",
        "prompt": "Vintage 1980 Lawrence Berkeley National Laboratory research dossier document, typewriter font, official university header, analytical mass spectrometer data tables, rubber stamps, yellowed vintage archival paper, 8k",
        "title": "Berkeley Lab Analytical Dossier"
    },
    {
        "filename": "bg_astronomical_star_chart.png",
        "type": "card",
        "prompt": "Vintage 1980 astronomical celestial star map chart, dark sepia celestial coordinate grid, orbital trajectory of Apollo asteroid intersecting Earth's orbit around the sun, vintage observatory technical plate, aged paper texture, 8k",
        "title": "Astronomical Sky Chart with Asteroid Orbit"
    },
    {
        "filename": "bg_yucatan_sonar_chart.png",
        "type": "card",
        "prompt": "Vintage 1970s marine bathymetric nautical chart of Yucatan Peninsula and Gulf of Mexico, coastal soundings, underwater depth contour lines, PEMEX seismic survey grid, aged nautical survey paper, 8k",
        "title": "Yucatan Marine Bathymetric Chart"
    },
    {
        "filename": "bg_ocean_drilling_log.png",
        "type": "card",
        "prompt": "Official Ocean Drilling Program ODP Leg 171B core recovery lithology log sheet, detailed columnar sediment depth section from Western Atlantic Blake Nose, technical typography, geological core stratigraphy chart, aged archival document, 8k",
        "title": "ODP Leg 171B Core Recovery Log Sheet"
    },
    {
        "filename": "bg_science_1980_article.png",
        "type": "card",
        "prompt": "Vintage June 1980 Science Magazine research paper page, headline reading 'Extraterrestrial Cause for the Cretaceous-Tertiary Extinction by Luis Alvarez', authentic academic journal scan with two columns of printed text and figures, aged paper, 8k",
        "title": "1980 Science Magazine Alvarez Article"
    },

    # 2. Rich Thematic Cutout Sprites / Diagrams (Replacing SVG vector slop)
    {
        "filename": "sprite_fossil_microscopic.png",
        "type": "cutout",
        "prompt": "Scanning electron microscope SEM photograph of Cretaceous microfossil Globotruncana foraminifera shell, intricate calcium carbonate chamber structure, isolated on pure white background, crisp cutout, 8k",
        "title": "Cretaceous Foraminifera Microfossil"
    },
    {
        "filename": "sprite_neutron_schematic.png",
        "type": "cutout",
        "prompt": "Vintage 1980 nuclear reactor physics schematic diagram, thermal neutron capture by Iridium-191 producing gamma decay rays, authentic scientific diagram on grid paper, isolated on pure white background, crisp cutout, 8k",
        "title": "Neutron Activation Physics Schematic"
    },
    {
        "filename": "sprite_asteroid_orbit_diagram.png",
        "type": "cutout",
        "prompt": "Vintage retro NASA JPL technical planetary orbit blueprint diagram, showing Earth orbit and eccentric elliptical asteroid trajectory path with distance markers, technical blueprint on graph paper, isolated on pure white background, crisp cutout, 8k",
        "title": "NASA JPL Asteroid Trajectory Blueprint"
    },
    {
        "filename": "sprite_crater_seismic_slice.png",
        "type": "cutout",
        "prompt": "Geological seismic reflection profile cross-section diagram across Chicxulub crater, showing buried collapsed central peak ring and faulted sedimentary limestone strata, scientific publication diagram, isolated on pure white background, crisp cutout, 8k",
        "title": "Chicxulub Subsurface Seismic Profile"
    },
    {
        "filename": "sprite_shocked_quartz_micro.png",
        "type": "cutout",
        "prompt": "Petrographic polarizing light microscope thin-section of shocked quartz grain from K-Pg boundary, distinct sets of microscopic intersecting planar deformation features PDFs, colorful birefringent crystal, isolated on pure white background, crisp cutout, 8k",
        "title": "Shocked Quartz Microscopic Thin-Section"
    },
    {
        "filename": "sprite_dinosaur_trex_tooth.png",
        "type": "cutout",
        "prompt": "Dark fossilized Tyrannosaurus rex tooth with serrated edges resting beside tiny early mammal fossil jaw bone, paleontology museum fossil specimen, isolated on pure white background, crisp cutout, 8k",
        "title": "T-Rex Tooth and Early Mammal Fossil"
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
        safe_print(f"  [9Router cx/gpt-5.5-image] Generating: {spec['filename']} (Attempt {attempt}/{max_retries})...")
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
                    safe_print(f"    -> Applying transparent alpha cutout for {spec['filename']}...")
                    img = make_transparent_cutout(img)
                
                img.save(output_path, "PNG", optimize=True)
                if os.path.exists(temp_raw_path):
                    os.remove(temp_raw_path)
                
                elapsed = time.time() - t0
                file_size = os.path.getsize(output_path) / 1024
                safe_print(f"    -> SUCCESS [{elapsed:.1f}s]: {spec['filename']} ({file_size:.1f} KB)")
                return True
        except Exception as e:
            safe_print(f"    [Error] Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                time.sleep(3)
    return False

def main():
    safe_print("=== Generating 12 Rich Archival Documents & Cutout Sprites ===")
    success_count = 0
    for i, spec in enumerate(NEW_ASSETS, 1):
        target_path = os.path.join(OUTPUT_DIR, spec["filename"])
        if os.path.exists(target_path) and os.path.getsize(target_path) > 10000:
            safe_print(f"[{i}/{len(NEW_ASSETS)}] Already exists: {spec['filename']}")
            success_count += 1
            continue
            
        safe_print(f"\n[{i}/{len(NEW_ASSETS)}] Processing: {spec['title']} ({spec['filename']})")
        if generate_asset(spec, target_path):
            success_count += 1
        time.sleep(1)

    safe_print(f"\n=== Completed: {success_count}/{len(NEW_ASSETS)} rich assets ready ===")

if __name__ == "__main__":
    main()
