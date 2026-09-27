import os
import sys
import json
import time
import base64
import urllib.request
import urllib.error
import numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

ROUTER_URL = "http://127.0.0.1:20128/v1/images/generations"
API_KEY = "Bearer sk-c4f2444795b190b3-kzvd4h-ea839762"
MODEL = "cx/gpt-5.5-image"

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_DIR = os.path.join(PROJECT_ROOT, "assets", "episode7_wow_signal", "images")
os.makedirs(TARGET_DIR, exist_ok=True)

ASSET_SPECS = [
    # -------------------------------------------------------------
    # 1. Full-Bleed Edge-to-Edge Archival Documents (Cards)
    # -------------------------------------------------------------
    {
        "filename": "bg_ibm1130_dotmatrix_printout.png",
        "type": "card",
        "prompt": "Authentic 1977 IBM 1130 mainframe computer continuous tractor-feed green-bar paper printout, vertical orientation, dense alphanumeric radio telemetry columns, aged yellowed paper texture with perforated edges and sprocket holes, vintage observatory archive document, 8k",
        "title": "IBM 1130 Mainframe Dot-Matrix Printout"
    },
    {
        "filename": "bg_sagittarius_constellation_map.png",
        "type": "card",
        "prompt": "Vintage 1970s astronomical celestial star atlas plate of Sagittarius and Chi Sagittarii constellation, equatorial coordinate grid lines, deep space coordinate markers, dark aged parchment paper texture, scientific observatory plate, 8k",
        "title": "Sagittarius Celestial Sky Atlas Plate"
    },
    {
        "filename": "bg_radio_spectrograph_waterfall.png",
        "type": "card",
        "prompt": "Authentic 1970s radio astronomy frequency spectrograph waterfall chart display, narrowband signal intensity heat trace at 1420 MHz, frequency calibration scales, vintage thermal chart paper, scientific archive, 8k",
        "title": "1420 MHz Radio Spectrograph Waterfall Chart"
    },
    {
        "filename": "bg_ohio_observatory_blueprint.png",
        "type": "card",
        "prompt": "Vintage 1970s architectural engineering blueprint of Ohio State University Big Ear radio observatory, showing flat ground plane, tiltable flat reflector mesh, and dual horn feed towers, aged sepia blueprint on technical grid paper, 8k",
        "title": "Big Ear Observatory Architectural Blueprint"
    },
    {
        "filename": "bg_hydrogen_line_diagram.png",
        "type": "card",
        "prompt": "Vintage 1970s astrophysics laboratory technical diagram of the 1420.405 MHz neutral hydrogen 21-centimeter hyperfine transition line, emission frequency curves and quantum spin flip diagram on aged scientific graph paper, 8k",
        "title": "1420.405 MHz Neutral Hydrogen Line Diagram"
    },
    {
        "filename": "bg_astronomical_logbook.png",
        "type": "card",
        "prompt": "Vintage August 1977 astronomical observatory logbook ledger page, handwritten SETI observations, sidereal time columns, coordinates for Sagittarius sector, aged sepia paper with ink stamps and coffee stains, 8k",
        "title": "August 1977 SETI Observatory Logbook"
    },

    # -------------------------------------------------------------
    # 2. Rich Transparent Cutouts (Pure White BG + Feathered Alpha)
    # -------------------------------------------------------------
    {
        "filename": "sprite_wow_printout_6equj5.png",
        "type": "cutout",
        "prompt": "Close-up macro crop of vintage 1977 dot-matrix computer printout paper showing the famous vertical alphanumeric column with printed characters 6 E Q U J 5, isolated on pure white background, studio catalog cutout, 8k",
        "title": "6EQUJ5 Mainframe Printout Section"
    },
    {
        "filename": "sprite_red_pilot_pen.png",
        "type": "cutout",
        "prompt": "Authentic vintage 1970s red Pilot rolling-writer ballpoint pen with red ribbed barrel and metal clip, pointed nib with wet red ink, isolated on pure white background, studio product cutout, 8k",
        "title": "Vintage Red Pilot Pen"
    },
    {
        "filename": "sprite_wow_annotation_ink.png",
        "type": "cutout",
        "prompt": "Authentic handwritten red ink handwriting text reading 'Wow!' with an oval pen circle loop around the code, hand scribbled with vintage red ink on white paper, isolated on pure white background, crisp cutout, 8k",
        "title": "Red Pen 'Wow!' Handwritten Annotation"
    },
    {
        "filename": "sprite_big_ear_antenna.png",
        "type": "cutout",
        "prompt": "Massive steel horn antenna structure of the Ohio State Big Ear radio telescope, pyramidal galvanized steel horn feeds, historical astronomy apparatus, isolated on pure white background, museum cutout, 8k",
        "title": "Big Ear Horn Antenna Structure"
    },
    {
        "filename": "sprite_telescope_reflector_mesh.png",
        "type": "cutout",
        "prompt": "The curved parabolic mesh reflector screen of the Big Ear radio observatory, vast wire-mesh grid on steel trusses, isolated on pure white background, architectural cutout, 8k",
        "title": "Big Ear Parabolic Mesh Reflector"
    },
    {
        "filename": "sprite_chi_sagittarii_cluster.png",
        "type": "cutout",
        "prompt": "Deep space star field around Chi Sagittarii and globular cluster M55, pinpoint luminous stars with subtle nebula haze, circular celestial telescope frame, isolated on pure white background, astronomy cutout, 8k",
        "title": "Chi Sagittarii Deep Space Target Field"
    },
    {
        "filename": "sprite_bell_curve_graph.png",
        "type": "cutout",
        "prompt": "Scientific 72-second Gaussian bell-curve antenna beam transit profile graph, red plotted response curve rising to peak 30 sigma and descending symmetrically, millimeter grid lines, isolated on pure white background, 8k",
        "title": "72-Second Bell Curve Antenna Response Graph"
    },
    {
        "filename": "sprite_ibm1130_mainframe.png",
        "type": "cutout",
        "prompt": "Vintage 1970s IBM 1130 mainframe computing system console, console typewriter keyboard, blue and cream metal chassis with flashing registers and indicator lights, isolated on pure white background, museum artifact cutout, 8k",
        "title": "IBM 1130 Computing System Console"
    },
    {
        "filename": "sprite_punchcard_terminal.png",
        "type": "cutout",
        "prompt": "Stack of vintage 80-column IBM punch cards with rectangular hole punches alongside an IBM punch card reader terminal, isolated on pure white background, museum cutout, 8k",
        "title": "IBM Punch Card Terminal & Stacks"
    },
    {
        "filename": "sprite_seti_tape_recorder.png",
        "type": "cutout",
        "prompt": "Vintage 1970s professional 10-inch aluminum reel-to-reel magnetic tape deck recorder for radio astronomy telemetry, VU meters, isolated on pure white background, studio cutout, 8k",
        "title": "SETI Telemetry Tape Deck Recorder"
    },
    {
        "filename": "sprite_jerry_ehman_astronomer.png",
        "type": "cutout",
        "prompt": "Young 1970s male radio astronomer Jerry Ehman in glasses and short-sleeve collared shirt examining computer printouts at wooden observatory desk, isolated on pure white background, archival portrait cutout, 8k",
        "title": "Astronomer Jerry Ehman Archival Cutout"
    },
    {
        "filename": "sprite_ohio_state_badge.png",
        "type": "cutout",
        "prompt": "Official vintage Ohio State University Radio Observatory emblem patch badge, radio dish graphic, circular embroidered scientific patch, isolated on pure white background, 8k",
        "title": "Ohio State Radio Observatory Emblem Badge"
    },
    {
        "filename": "sprite_seti_institute_seal.png",
        "type": "cutout",
        "prompt": "Vintage Search for Extraterrestrial Intelligence SETI project insignia seal, celestial wave radio icon, circular official agency emblem, isolated on pure white background, 8k",
        "title": "SETI Project Official Insignia Seal"
    },
    {
        "filename": "sprite_investigation_unsolved_stamp.png",
        "type": "cutout",
        "prompt": "Distressed weathered red rubber ink stamp rectangular imprint reading 'INVESTIGATION UNSOLVED // CLASSIFIED SIGNAL', sharp grunge texture, transparent background, isolated on pure white background, 8k",
        "title": "Investigation Unsolved Red Rubber Stamp"
    },
    {
        "filename": "sprite_telescope_reticle.png",
        "type": "cutout",
        "prompt": "Precision optical radio telescope targeting reticle, fine crosshair with degree markings and azimuth rings, isolated on pure white background, technical overlay cutout, 8k",
        "title": "Radio Telescope Celestial Crosshair Reticle"
    },
    {
        "filename": "sprite_vintage_scotch_tape.png",
        "type": "cutout",
        "prompt": "Strip of aged translucent yellowed cellophane scotch tape with wrinkled edges and adhesive discoloration, isolated on pure white background, tactile cutout, 8k",
        "title": "Vintage Translucent Scotch Tape Strip"
    },
    {
        "filename": "sprite_manila_dossier_folder.png",
        "type": "cutout",
        "prompt": "Open forensic manila dossier file folder with tab reading 'PROJECT SETI - OHIO OBSERVATORY', aged beige kraft cardstock with metal prong fastener, isolated on pure white background, clean cutout, 8k",
        "title": "Manila Forensic Dossier Folder"
    },
    {
        "filename": "sprite_classified_label.png",
        "type": "cutout",
        "prompt": "Vintage gummed archival evidence label reading 'EVIDENCE EXHIBIT: COSMIC ANOMALY 1420.405 MHZ', aged paper with red border and typewriter text, isolated on pure white background, 8k",
        "title": "Archival Cosmic Anomaly Evidence Label"
    },
    {
        "filename": "sprite_comet_hypothesis_diagram.png",
        "type": "cutout",
        "prompt": "Scientific astronomical orbit diagram comparing comet 266P/Christensen hydrogen coma with the Big Ear beam window, technical planetary orbit vector diagram on white background, isolated on pure white background, 8k",
        "title": "Comet Hydrogen Coma Hypothesis Diagram"
    },
    {
        "filename": "sprite_radio_dish_vla.png",
        "type": "cutout",
        "prompt": "Gigantic 25-meter parabolic radio astronomy antenna dish from the Very Large Array, white metal dish pointed toward deep sky, isolated on pure white background, crisp cutout, 8k",
        "title": "VLA Deep Space Radio Telescope Dish"
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

def generate_asset(spec, max_retries=3):
    target_path = os.path.join(TARGET_DIR, spec["filename"])
    if os.path.exists(target_path) and os.path.getsize(target_path) > 10000:
        print(f"[Skip] Already exists: {spec['filename']} ({round(os.path.getsize(target_path)/1024, 1)} KB)", flush=True)
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
            with urllib.request.urlopen(req, timeout=140) as response:
                result = json.loads(response.read().decode("utf-8"))
                item = result.get("data", [{}])[0]
                raw_bytes = None
                if "b64_json" in item:
                    raw_bytes = base64.b64decode(item["b64_json"])
                elif "url" in item:
                    with urllib.request.urlopen(item["url"], timeout=60) as img_resp:
                        raw_bytes = img_resp.read()

                if raw_bytes:
                    temp_raw = target_path + ".tmp.png"
                    with open(temp_raw, "wb") as f:
                        f.write(raw_bytes)

                    with Image.open(temp_raw) as im:
                        if spec["type"] == "cutout":
                            print(f"[Cutout] Feathering alpha for {spec['filename']}...", flush=True)
                            out_img = make_transparent_cutout(im)
                            out_img.save(target_path, "PNG")
                        else:
                            im.convert("RGB").save(target_path, "PNG")

                    if os.path.exists(temp_raw):
                        os.remove(temp_raw)

                    elapsed = round(time.time() - t0, 1)
                    sz = round(os.path.getsize(target_path) / 1024, 1)
                    print(f"[Success] {spec['filename']} in {elapsed}s ({sz} KB)", flush=True)
                    return spec["filename"], True
        except Exception as e:
            print(f"[Error] {spec['filename']} attempt {attempt}: {e}", flush=True)
            if attempt < max_retries:
                time.sleep(4)

    return spec["filename"], False

def main():
    print(f"=== Generating {len(ASSET_SPECS)} Assets for Episode 7: The Wow! Signal (Parallel 3 Workers) ===", flush=True)
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(generate_asset, spec): spec for spec in ASSET_SPECS}
        completed = 0
        for future in as_completed(futures):
            filename, success = future.result()
            if success:
                completed += 1
            print(f"Progress: {completed}/{len(ASSET_SPECS)} completed.", flush=True)

    print(f"\n=== Completed {completed}/{len(ASSET_SPECS)} assets successfully ===", flush=True)

if __name__ == "__main__":
    main()
