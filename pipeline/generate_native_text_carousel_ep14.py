import os
import sys
import json
import time
import base64
import urllib.request
import urllib.error
from PIL import Image

ROUTER_URL = "http://127.0.0.1:20128/v1/images/generations"
API_KEY = "Bearer sk-c4f2444795b190b3-kzvd4h-ea839762"
MODEL = "cx/gpt-5.5-image"

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_DIR = os.path.join(PROJECT_ROOT, "assets", "episode14_glymphatic_brain_wash", "carousel_native_text")
os.makedirs(TARGET_DIR, exist_ok=True)

PROMPTS = [
    {
        "index": 1,
        "filename": "slide_1_cover_native_text.png",
        "title": "Cover: While You Sleep, Your Brain Washes Itself",
        "prompt": (
            "Create ONE finished 4:5 portrait editorial science carousel slide, 1080 x 1350. "
            "Generate the scientific illustration AND ALL FINAL ENGLISH TYPOGRAPHY NATIVELY TOGETHER IN THIS IMAGE. "
            "This is a finished composition: do not leave a blank text area for later typesetting; do not imitate pasted-on captions.\n\n"
            "Art direction: deep midnight indigo background (#050813 to #0B1933), electric cyan and aquamarine bioluminescent glow, subtle sapphire depth. "
            "Documentary-editorial elegance with fine biological texture; tactile subtle paper grain, credible natural scientific light, no cheesy neon effects. "
            "Central visual: a breathtaking sagittal cross-section illustration of a human brain glowing with bioluminescent aquamarine fluid pathways through the cortex. "
            "Keep the brain illustration as the dominant focal point, positioned in the upper center.\n\n"
            "Composition: brain occupies the upper half. Put a calm, deep midnight navy shaded area at lower left behind the headline and body copy. "
            "Keep generous safe margins on every edge. Make every word readable at mobile thumbnail size. "
            "Use an expressive editorial serif for the headline, a crisp humanist sans for supporting copy, and small uppercase tracked sans for metadata. Cyan is an accent.\n\n"
            "Render ONLY these exact strings, spelled and punctuated exactly; no other words, labels, symbols resembling letters, or decorative pseudo-text:\n"
            "Top left header: \"NOCTURNAL NEUROSCIENCE\"\n"
            "Top right folio: \"01 / 05\"\n"
            "Small kicker above headline: \"THE CEREBRAL DETOX\"\n"
            "Large two-line headline: \"WHILE YOU SLEEP,\"\n\"YOUR BRAIN WASHES ITSELF\"\n"
            "Body beneath headline: \"Glial cells physically contract by sixty percent to unleash a pressurized cerebral fluid tide.\"\n"
            "Bottom left navigation: \"SWIPE TO DISCOVER →\"\n\n"
            "Hierarchy: headline first, glowing brain second, body third. Set the body in two or three short lines with strong contrast. "
            "Keep type off the brain artwork. No post-generation text overlays."
        )
    },
    {
        "index": 2,
        "filename": "slide_2_astrocytes_native_text.png",
        "title": "Astrocytes: The Microscopic Highway",
        "prompt": (
            "Create ONE finished 4:5 portrait editorial science carousel slide, 1080 x 1350. "
            "Generate the scientifically informed artwork AND ALL FINAL ENGLISH TYPOGRAPHY NATIVELY TOGETHER IN THIS IMAGE. "
            "Deliver a fully typeset image, not art for a later Python/PIL text overlay.\n\n"
            "Art direction: sophisticated scientific illustration of a single star-shaped astrocyte glial cell with glowing branching endfeet wrapping around microvascular blood vessels. "
            "Deep midnight navy background, vibrant bioluminescent aquamarine and teal accents, soft volumetric light, fine paper texture. "
            "Suggest microscopic fluid channels opening and cerebrospinal fluid coursing through. No cartoonish characters.\n\n"
            "Composition: astrocyte cell on the upper right; quiet, dark navy shaded panel in the lower-left quadrant for typography. "
            "Preserve safe margins. Use the same editorial serif headline, crisp humanist sans body, and tracked uppercase metadata as a coherent carousel system.\n\n"
            "Render ONLY these exact strings, spelled and punctuated exactly; no other words or stray letters:\n"
            "Top left header: \"SCIENCE • NEDERGAARD 2013\"\n"
            "Top right folio: \"02 / 05\"\n"
            "Small kicker above headline: \"AQUAPORIN-4 FLOODGATES\"\n"
            "Large two-line headline: \"THE ASTROCYTIC\"\n\"HIGHWAY\"\n"
            "Body beneath headline: \"During deep slow-wave sleep, star-shaped astrocytes open microscopic water channels, elevating fluid flow by two hundred percent.\"\n"
            "Bottom left navigation: \"SWIPE →\"\n\n"
            "Clear hierarchy, generous margins, sharp typography."
        )
    },
    {
        "index": 3,
        "filename": "slide_3_alzheimer_purge_native_text.png",
        "title": "Waste Clearance: The Alzheimer's Toxic Purge",
        "prompt": (
            "Create ONE finished 4:5 portrait editorial science carousel slide, 1080 x 1350. "
            "Generate the scientific illustration AND ALL FINAL ENGLISH TYPOGRAPHY NATIVELY TOGETHER IN THIS IMAGE. "
            "Deliver a fully typeset image, not art for a later Python/PIL text overlay.\n\n"
            "Art direction: deep midnight obsidian background. A microscopic view of toxic protein aggregates (Beta-Amyloid and Tau tangles) depicted in deep coral-red and crimson, being dissolved and swept away by an advancing glowing wave of clear cyan cerebrospinal fluid. "
            "Rich biomedical precision, documentary contrast, crisp texture.\n\n"
            "Composition: protein clearance reaction in the upper two-thirds; quiet, deep navy shaded text panel in the lower third. "
            "Preserve safe margins on all borders.\n\n"
            "Render ONLY these exact strings, spelled and punctuated exactly; no other words or stray letters:\n"
            "Top left header: \"NEUROLOGICAL DEFENSE\"\n"
            "Top right folio: \"03 / 05\"\n"
            "Small kicker above headline: \"METABOLIC WASTE CLEARANCE\"\n"
            "Large two-line headline: \"THE ALZHEIMER'S\"\n\"TOXIC PURGE\"\n"
            "Body beneath headline: \"Cerebrospinal fluid waves actively vacuum away toxic Beta-Amyloid and Tau proteins before they can solidify into permanent plaques.\"\n"
            "Bottom left navigation: \"SWIPE →\"\n\n"
            "Consistent editorial serif, humanist sans body, and tracked metadata."
        )
    },
    {
        "index": 4,
        "filename": "slide_4_sleep_debt_native_text.png",
        "title": "Chronobiology: The Sleep Debt Fallacy",
        "prompt": (
            "Create ONE finished 4:5 portrait editorial science carousel slide, 1080 x 1350. "
            "Generate the scientific illustration AND ALL FINAL ENGLISH TYPOGRAPHY NATIVELY TOGETHER IN THIS IMAGE. "
            "Deliver a fully typeset image, not art for a later Python/PIL text overlay.\n\n"
            "Art direction: deep midnight blue background. An elegant, minimalist chronobiology sleep architecture dial / radar chart depicting the nocturnal hours from 11 PM to 3 AM with synchronized Slow-Wave Delta brainwaves (0.5 to 4 Hz) pulsating in warm gold and cyan. "
            "Restrained gold foil accents, high editorial polish.\n\n"
            "Composition: chronobiology wave diagram in the upper center; dark shaded panel below for typography. "
            "Preserve safe margins.\n\n"
            "Render ONLY these exact strings, spelled and punctuated exactly; no other words or stray letters:\n"
            "Top left header: \"CHRONOBIOLOGY\"\n"
            "Top right folio: \"04 / 05\"\n"
            "Small kicker above headline: \"ARCHITECTURE INTEGRITY\"\n"
            "Large two-line headline: \"YOU CANNOT CATCH UP\"\n\"ON SUNDAYS\"\n"
            "Body beneath headline: \"Glymphatic flushing requires synchronized Delta waves that only occur in your initial nocturnal cycles. Binging later offers zero cleansing.\"\n"
            "Bottom left navigation: \"SWIPE →\"\n\n"
            "Consistent typography and clean layout."
        )
    },
    {
        "index": 5,
        "filename": "slide_5_closing_protocol_native_text.png",
        "title": "Protocol: Protect Your Eight Hours",
        "prompt": (
            "Create ONE finished 4:5 portrait editorial science carousel slide, 1080 x 1350. "
            "Generate the inspiring illustration AND ALL FINAL ENGLISH TYPOGRAPHY NATIVELY TOGETHER IN THIS IMAGE. "
            "Deliver a fully typeset image, not art for a later Python/PIL text overlay.\n\n"
            "Art direction: deep midnight indigo background. A serene, minimalist silhouette of a resting human profile surrounded by gentle bioluminescent celestial starlight and delicate neural constellation connections, radiating peaceful clarity. "
            "Restrained gold and cyan accents, tactile paper grain, high-end editorial elegance. "
            "Strictly NO eyes or detailed facial features on the silhouette (pure smooth serene profile).\n\n"
            "Composition: artwork in the upper two-thirds; quiet, deep navy shaded text panel in the lower third. "
            "Preserve safe margins.\n\n"
            "Render ONLY these exact strings, spelled and punctuated exactly; no other words or stray letters:\n"
            "Top left header: \"THE PROTOCOL\"\n"
            "Top right folio: \"05 / 05\"\n"
            "Small kicker above headline: \"BIOLOGICAL RENEWAL\"\n"
            "Large two-line headline: \"PROTECT YOUR\"\n\"EIGHT HOURS\"\n"
            "Body beneath headline: \"Sleep is not passive downtime. It is your brain's divine self-cleaning ritual. Let your brain clean its temple tonight.\"\n"
            "Bottom left CTA: \"SHARE TO PROTECT A MIND • SAVE\"\n\n"
            "Consistent editorial serif, humanist sans body, tracked metadata. Dignified and authoritative conclusion."
        )
    }
]

def generate_slide(spec):
    out_path = os.path.join(TARGET_DIR, spec["filename"])
    if os.path.exists(out_path):
        print(f"[Skip] {spec['filename']} already exists.")
        return True

    print(f"\n[Generate Slide {spec['index']}/5] {spec['title']} via 9Router ({MODEL})...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": API_KEY,
        "User-Agent": "BangMotion/1.0"
    }
    payload = {
        "model": MODEL,
        "prompt": spec["prompt"],
        "n": 1,
        "size": "1024x1792"  # Supported vertical resolution, will be normalized to 1080x1350
    }

    req = urllib.request.Request(ROUTER_URL, data=json.dumps(payload).encode("utf-8"), headers=headers)
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(req, timeout=120) as res:
                data = json.loads(res.read().decode("utf-8"))
                if "data" in data and len(data["data"]) > 0:
                    first = data["data"][0]
                    img_bytes = None
                    if "b64_json" in first:
                        img_bytes = base64.b64decode(first["b64_json"])
                    elif "url" in first:
                        img_bytes = urllib.request.urlopen(first["url"]).read()

                    if img_bytes:
                        raw_path = out_path + ".raw.png"
                        with open(raw_path, "wb") as f:
                            f.write(img_bytes)

                        # Standardize to 4:5 aspect ratio (1080 x 1350)
                        img = Image.open(raw_path)
                        # Crop / resize to 1080x1350
                        target_w, target_h = 1080, 1350
                        aspect_target = target_w / target_h
                        curr_w, curr_h = img.size
                        aspect_curr = curr_w / curr_h

                        if aspect_curr < aspect_target:
                            new_h = int(curr_w / aspect_target)
                            top = (curr_h - new_h) // 2
                            img_cropped = img.crop((0, top, curr_w, top + new_h))
                        else:
                            new_w = int(curr_h * aspect_target)
                            left = (curr_w - new_w) // 2
                            img_cropped = img.crop((left, 0, left + new_w, curr_h))

                        img_final = img_cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
                        img_final.save(out_path, "PNG", optimize=True)
                        print(f"[Success] Saved 4:5 native text slide: {out_path} ({img_final.size})")
                        return True
        except Exception as e:
            print(f"[Attempt {attempt}/3 Failed] {e}")
            time.sleep(3)

    return False

def main():
    print(f"=== Generating 5 Native Text Carousel Slides for Episode 14 ===")
    for spec in PROMPTS:
        success = generate_slide(spec)
        if not success:
            print(f"[Warning] Failed to generate {spec['filename']}")
        time.sleep(2)

if __name__ == "__main__":
    main()
