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
TARGET_DIR = os.path.join(PROJECT_ROOT, "assets", "episode8_voynich_manuscript", "images")
os.makedirs(TARGET_DIR, exist_ok=True)

ASSET_SPECS = [
    # -------------------------------------------------------------
    # 1. Full-Bleed Edge-to-Edge Archival Documents (Cards)
    # -------------------------------------------------------------
    {
        "filename": "bg_monastery_library_vault.png",
        "type": "card",
        "prompt": "Authentic dimly lit 15th-century Jesuit monastery cloister archive, ancient oak bookshelves packed with leather-bound codices, stone archways, antique wooden reading table illuminated by warm candle lantern light and dust motes, dramatic chiaroscuro historical atmosphere, 8k",
        "title": "Jesuit Monastery Archive Library"
    },
    {
        "filename": "bg_ancient_vellum_parchment.png",
        "type": "card",
        "prompt": "Authentic macro texture scan of 15th-century Italian calfskin vellum manuscript pergamen, weathered aged surface, natural translucent animal follicle pores, subtle creases and irregular golden tea-stained patina, museum archival paper background, 8k",
        "title": "15th-Century Calfskin Vellum Parchment"
    },
    {
        "filename": "bg_botanical_herbal_folio.png",
        "type": "card",
        "prompt": "Authentic high-resolution full-bleed scan of an illustrated medieval Voynich manuscript herbal page, showing strange fantastical alien botanical specimens painted in green and blue tempera, surrounded by dense continuous handwritten Voynichese calligraphic text columns, aged vellum folio, 8k",
        "title": "Voynich Manuscript Botanical Herbal Folio"
    },
    {
        "filename": "bg_cosmological_zodiac_wheel.png",
        "type": "card",
        "prompt": "Authentic high-resolution full-bleed scan of the Voynich manuscript cosmological fold-out wheel, intricate concentric astronomical circular diagrams, zodiac star circles, medieval miniature female figures in celestial gears, calligraphic cipher inscriptions, aged vellum parchment, 8k",
        "title": "Voynich Cosmological Zodiac Wheel"
    },
    {
        "filename": "bg_accelerator_mass_spectrometry.png",
        "type": "card",
        "prompt": "University of Arizona physics laboratory accelerator mass spectrometer AMS vacuum beamline, high-precision carbon-14 radiocarbon measurement detectors, glowing analytical status monitors, dark technological laboratory ambiance, 8k",
        "title": "AMS Radiocarbon Physics Laboratory"
    },
    {
        "filename": "bg_beinecke_rare_book_vault.png",
        "type": "card",
        "prompt": "Interior architectural view of Yale University Beinecke Rare Book and Manuscript Library, massive central glass cube showcasing thousands of illuminated rare manuscripts, translucent Vermont marble panels glowing with warm amber sunlight, monumental library, 8k",
        "title": "Yale Beinecke Rare Book Library Interior"
    },

    # -------------------------------------------------------------
    # 2. Rich Transparent Cutouts (Pure White BG + Feathered Alpha)
    # -------------------------------------------------------------
    {
        "filename": "sprite_voynich_closed_book.png",
        "type": "cutout",
        "prompt": "The genuine Voynich Manuscript MS 408 closed, aged yellowish goat vellum limp binding, creased leather spine with handwritten ink catalog numbers, irregular cockled parchment edges, isolated on pure white background, museum catalog cutout, 8k",
        "title": "Voynich Manuscript Closed Volume"
    },
    {
        "filename": "sprite_voynich_open_spread.png",
        "type": "cutout",
        "prompt": "Open two-page spread of the Voynich manuscript lying flat, left page featuring a detailed fictional botanical flower, right page featuring circular astronomical star wheels and neat paragraphs of unknown glyphs, aged vellum, isolated on pure white background, 8k",
        "title": "Open Voynich Manuscript Spread"
    },
    {
        "filename": "sprite_alien_flower_cutout.png",
        "type": "cutout",
        "prompt": "Authentic Voynich style illustrated botanical specimen, single strange fantastical plant with bulbous blue petals, segmented serpentine stem, and bizarre root network shaped like dragon claws, medieval tempera pigments, isolated on pure white background, clean cutout, 8k",
        "title": "Voynich Alien Botanical Specimen"
    },
    {
        "filename": "sprite_alien_vascular_leaf.png",
        "type": "cutout",
        "prompt": "Detailed macro scientific illustration of an impossible plant leaf from the Voynich herbal section, unnatural geometric vascular network with thorn nodules, painted in faded green tempera, isolated on pure white background, botanical cutout, 8k",
        "title": "Alien Plant Vascular Leaf Cutout"
    },
    {
        "filename": "sprite_zodiac_star_wheel.png",
        "type": "cutout",
        "prompt": "Isolated circular cosmological astronomical wheel diagram from the Voynich manuscript, golden sunburst center with thirty radiating concentric sectors containing miniature human figures holding stars and alien script labels, isolated on pure white background, 8k",
        "title": "Isolated Zodiac Star Wheel Diagram"
    },
    {
        "filename": "sprite_balneological_tubes.png",
        "type": "cutout",
        "prompt": "Medieval scientific illustration of the Voynich manuscript balneological section, complex system of interconnected green-fluid glass tubes, bio-mechanical pipes, and organic reservoirs, isolated on pure white background, crisp cutout, 8k",
        "title": "Balneological Fluid Pipe System"
    },
    {
        "filename": "sprite_voynich_alphabet_sample.png",
        "type": "cutout",
        "prompt": "Clean horizontal calligraphic specimen line of authentic Voynichese alphabet glyphs, showing famous gallows characters, EVA transcription letters, benched glyphs, brown iron gall ink strokes on white parchment, isolated on pure white background, 8k",
        "title": "Voynichese Alphabet Calligraphic Glyphs"
    },
    {
        "filename": "sprite_quill_ink_well.png",
        "type": "cutout",
        "prompt": "Authentic 15th-century goose feather quill pen with sharpened nib dipped in dark brown iron gall ink, resting next to an antique stoneware inkpot with ink droplets, isolated on pure white background, museum studio cutout, 8k",
        "title": "Medieval Goose Quill & Gall Inkpot"
    },
    {
        "filename": "sprite_magnifying_glass.png",
        "type": "cutout",
        "prompt": "Vintage heavy brass forensic magnifying glass with knurled handle and polished convex glass lens with realistic optical reflections, isolated on pure white background, studio product cutout, 8k",
        "title": "Vintage Brass Archival Magnifying Glass"
    },
    {
        "filename": "sprite_arizona_ams_core.png",
        "type": "cutout",
        "prompt": "Scientific metallurgical target carousel containing carbon-14 graphite targets and micro-sampling scalpel used in University of Arizona accelerator mass spectrometry, isolated on pure white background, technical scientific cutout, 8k",
        "title": "AMS Carbon-14 Target Carousel"
    },
    {
        "filename": "sprite_carbon_dating_graph.png",
        "type": "cutout",
        "prompt": "Scientific OxCal radiocarbon calibration curve chart for the Voynich manuscript, plotting atmospheric 14C calibration years 1404 to 1438 AD with 95.4% probability bell curve, crisp laboratory graphic, isolated on pure white background, 8k",
        "title": "1404-1438 AD Radiocarbon Calibration Curve"
    },
    {
        "filename": "sprite_zipf_law_curve.png",
        "type": "cutout",
        "prompt": "Computational linguistics log-log frequency plot comparing Zipf's Law distribution: rank vs frequency curve showing Voynich manuscript perfectly tracking human natural languages with slope minus one, isolated on pure white background, 8k",
        "title": "Zipf's Law Mathematical Word Frequency Graph"
    },
    {
        "filename": "sprite_william_friedman_portrait.png",
        "type": "cutout",
        "prompt": "Archival vintage 1940s sepia photographic portrait cutout of master cryptanalyst William F. Friedman in suit and round spectacles, analyzing cipher paper ribbons, historical military cryptanalyst cutout, isolated on pure white background, 8k",
        "title": "Cryptanalyst William F. Friedman Portrait"
    },
    {
        "filename": "sprite_nsa_cryptanalysis_seal.png",
        "type": "cutout",
        "prompt": "Official emblem insignia of National Security Agency / Department of Defense Cryptanalysis Task Force, golden eagle clutching key and lightning bolts on dark blue roundel, isolated on pure white background, 8k",
        "title": "NSA Cryptanalysis Task Force Insignia"
    },
    {
        "filename": "sprite_neural_network_nodes.png",
        "type": "cutout",
        "prompt": "Modern artificial intelligence language model transformer attention matrix, glowing cyan and gold multi-head self-attention graph with interconnected linguistic token nodes, isolated on pure white background, tech visual cutout, 8k",
        "title": "AI Transformer Neural Network Token Graph"
    },
    {
        "filename": "sprite_beinecke_library_seal.png",
        "type": "cutout",
        "prompt": "Official circular library embossment stamp of Yale University Beinecke Rare Book and Manuscript Library, dark navy and gold foil seal with Yale coat of arms, isolated on pure white background, 8k",
        "title": "Yale Beinecke Library Archival Seal"
    },
    {
        "filename": "sprite_cardboard_archival_box.png",
        "type": "cutout",
        "prompt": "Custom gray acid-free preservation clamshell archival box used to store rare manuscripts, open lid with white cotton ribbon ties, isolated on pure white background, museum storage cutout, 8k",
        "title": "Acid-Free Archival Clamshell Box"
    },
    {
        "filename": "sprite_red_wax_seal_broken.png",
        "type": "cutout",
        "prompt": "Authentic 15th-century cracked scarlet beeswax seal with intricate ecclesiastical cardinal crest imprint and frayed hemp cord threads, isolated on pure white background, tactile antique cutout, 8k",
        "title": "Cracked Red Cardinal Wax Seal"
    },
    {
        "filename": "sprite_stamp_case_unresolved.png",
        "type": "cutout",
        "prompt": "Distressed heavy red and black rubber ink stamp rectangular imprint reading 'CASE UNRESOLVED // THE VOYNICH CIPHER', weathered textured stencil typography, isolated on pure white background, 8k",
        "title": "Case Unresolved Weathered Rubber Stamp"
    },
    {
        "filename": "sprite_hoax_debunked_stamp.png",
        "type": "cutout",
        "prompt": "Bold weathered red ink rubber stamp text imprint reading 'RENAISSANCE HOAX THEORY // DEBUNKED (AMS-14C)', distressed grunge border, isolated on pure white background, 8k",
        "title": "Hoax Theory Debunked Rubber Stamp"
    },
    {
        "filename": "sprite_ms408_callnumber_tag.png",
        "type": "cutout",
        "prompt": "Vintage Yale library catalog accession paper tag reading 'BEINECKE RARE BOOK MS 408 - VOYNICH CIPHER CODEX', typed on aged cardstock with metal eyelet, isolated on pure white background, 8k",
        "title": "Yale MS 408 Archival Accession Tag"
    },
    {
        "filename": "sprite_vintage_ruler_scale.png",
        "type": "cutout",
        "prompt": "Vintage museum forensic photography centimeter and millimeter scale ruler bar, black and white checkered calibration intervals on aged cream plastic, isolated on pure white background, 8k",
        "title": "Archival Photographic Metric Scale"
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
    print(f"=== Generating {len(ASSET_SPECS)} Assets for Episode 8: The Voynich Manuscript (Parallel 3 Workers) ===", flush=True)
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
