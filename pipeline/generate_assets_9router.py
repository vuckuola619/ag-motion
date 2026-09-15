import os
import sys
import json
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
        "filename": "trex_fossil.png",
        "prompt": "Complete Tyrannosaurus Rex dinosaur fossil skull museum specimen, dramatic paleontology artifact, side angle, detailed bone texture, isolated on pure white background, studio catalog lighting, sharp crisp edges, no background shadows, 8k",
        "title": "T-Rex Fossil Skull Specimen"
    },
    {
        "filename": "asteroid_impact.png",
        "prompt": "Massive fiery Chicxulub asteroid falling at hypersonic speed with glowing burning fire tail, atmospheric plasma shockwave, isolated on pure white background, crisp silhouette, dramatic contrast, high resolution studio cutout",
        "title": "Chicxulub Impact Asteroid"
    },
    {
        "filename": "deccan_volcano.png",
        "prompt": "Prehistoric erupting volcanic mountain with towering billowing dark sulfur ash cloud and glowing lava fissures, isolated on pure white background, high contrast, clean edge cutout, dramatic geological catastrophe",
        "title": "Deccan Traps Supervolcano"
    },
    {
        "filename": "iridium_layer.png",
        "prompt": "Cross-section specimen of geological sediment rock strata showing the distinct thin dark Iridium boundary line between Cretaceous and Paleogene layers, fossil inclusions, isolated on pure white background, scientific catalog photo",
        "title": "K-Pg Iridium Boundary Geological Core"
    },
    {
        "filename": "mammal_survivor.png",
        "prompt": "Small cute prehistoric nocturnal mammal Morganucodon peering out from an underground burrow, furry textured details, isolated on pure white background, clean crisp cutout, survivor of extinction event",
        "title": "Early Mammalian Survivor"
    }
]

def make_transparent_cutout(img: Image.Image, threshold: int = 245) -> Image.Image:
    """Isolate pure white/near-white background to transparent RGBA."""
    img = img.convert("RGBA")
    arr = np.array(img)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    
    # White background detection with soft alpha falloff
    is_white = (r > threshold) & (g > threshold) & (b > threshold)
    
    # Soft feathering at the boundaries
    diff = np.maximum.reduce([255 - r, 255 - g, 255 - b])
    alpha_soft = np.clip(diff * 5, 0, 255).astype(np.uint8)
    
    new_a = np.where(is_white, alpha_soft, a)
    arr[:, :, 3] = new_a
    return Image.fromarray(arr, "RGBA")

def generate_via_9router(prompt: str, output_path: str) -> bool:
    payload = {
        "model": MODEL,
        "prompt": prompt,
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
    
    try:
        print(f"  [9Router] Calling {MODEL} (timeout 150s)...")
        with urllib.request.urlopen(req, timeout=150) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            item = result.get("data", [{}])[0]
            
            raw_bytes = None
            if "b64_json" in item:
                raw_bytes = base64.b64decode(item["b64_json"])
            elif "url" in item:
                img_url = item["url"]
                with urllib.request.urlopen(img_url, timeout=60) as img_resp:
                    raw_bytes = img_resp.read()
            
            if raw_bytes:
                # Save temp image, then process transparency
                temp_path = output_path + ".tmp.png"
                with open(temp_path, "wb") as f:
                    f.write(raw_bytes)
                
                with Image.open(temp_path) as im:
                    cutout = make_transparent_cutout(im)
                    cutout.save(output_path, "PNG")
                
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                print(f"  [9Router] Successfully generated and processed: {output_path}")
                return True
    except urllib.error.HTTPError as e:
        print(f"  [9Router HTTPError]: {e.code} - {e.reason}")
    except Exception as e:
        print(f"  [9Router Error]: {e}")
    
    return False

def generate_procedural_fallback(spec: dict, output_path: str):
    """Procedural SVG/Pillow high-resolution graphic fallback if 9router is offline or throttled."""
    print(f"  [Fallback] Generating procedural high-res visual for: {spec['filename']}")
    width, height = 1024, 1024
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    # We will generate a rich graphical element matching the White Catalog aesthetic
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(img)
    
    fname = spec["filename"]
    if fname == "trex_fossil.png":
        # Draw stylized paleontological T-Rex bone skull
        # Base skull mass
        draw.polygon([(200, 480), (320, 260), (680, 220), (840, 360), (880, 520), (620, 680), (360, 660), (220, 540)], fill=(210, 195, 170, 255), outline=(90, 80, 65, 255), width=8)
        # Eye socket
        draw.ellipse([(580, 320), (700, 440)], fill=(40, 35, 30, 255), outline=(70, 60, 50, 255), width=6)
        # Naris / nostril
        draw.ellipse([(760, 380), (830, 440)], fill=(40, 35, 30, 255))
        # Jaw and serrated teeth
        draw.polygon([(360, 660), (620, 680), (860, 600), (880, 680), (620, 780), (340, 740)], fill=(195, 180, 155, 255), outline=(90, 80, 65, 255), width=6)
        for tx in range(400, 840, 36):
            draw.polygon([(tx, 600), (tx + 18, 600), (tx + 9, 645)], fill=(245, 240, 225, 255), outline=(70, 60, 50, 255), width=2)
            draw.polygon([(tx + 10, 665), (tx + 28, 665), (tx + 19, 620)], fill=(245, 240, 225, 255), outline=(70, 60, 50, 255), width=2)
    elif fname == "asteroid_impact.png":
        # Fiery atmospheric entry asteroid
        for r in range(420, 180, -25):
            alpha = int(255 * (1.0 - (r - 180) / 240))
            draw.ellipse([(512 - r, 512 - r), (512 + r, 512 + r)], fill=(255, 120, 20, max(20, alpha // 4)))
        # Plasma shock cone
        draw.polygon([(220, 220), (740, 680), (620, 820), (120, 360)], fill=(255, 60, 10, 200))
        # Rocky core
        draw.polygon([(360, 380), (480, 320), (640, 360), (700, 500), (660, 640), (480, 680), (340, 560)], fill=(75, 65, 60, 255), outline=(255, 180, 50, 255), width=8)
    elif fname == "deccan_volcano.png":
        # Volcanic plume and mountain
        draw.polygon([(160, 860), (440, 480), (580, 480), (860, 860)], fill=(65, 55, 50, 255), outline=(35, 30, 25, 255), width=6)
        # Glowing crater
        draw.ellipse([(420, 460), (600, 500)], fill=(255, 60, 0, 255))
        # Ash cloud plumes
        for cx, cy, cr in [(512, 340, 160), (380, 240, 140), (620, 220, 150), (500, 140, 170)]:
            draw.ellipse([(cx - cr, cy - cr), (cx + cr, cy + cr)], fill=(45, 45, 48, 230))
    elif fname == "iridium_layer.png":
        # Rock core sample
        draw.rectangle([(280, 160), (744, 864)], fill=(185, 170, 150, 255), outline=(70, 60, 50, 255), width=6)
        # Cretaceous layer (bottom)
        draw.rectangle([(286, 520), (738, 858)], fill=(205, 190, 165, 255))
        # The famous dark iridium boundary line (66.038 Ma)
        draw.rectangle([(286, 490), (738, 520)], fill=(30, 25, 25, 255))
        # Tertiary Paleogene layer (top)
        draw.rectangle([(286, 166), (738, 490)], fill=(160, 145, 130, 255))
        # Labels and depth ruler
        for y in range(200, 840, 40):
            draw.line([(286, y), (316, y)], fill=(50, 45, 40, 255), width=3)
    elif fname == "mammal_survivor.png":
        # Early mammal burrow scene
        draw.ellipse([(320, 480), (704, 760)], fill=(120, 95, 70, 255), outline=(60, 45, 30, 255), width=6)
        # Furry creature peering out
        draw.ellipse([(440, 420), (600, 560)], fill=(160, 130, 95, 255))
        # Ears
        draw.polygon([(440, 440), (410, 380), (470, 400)], fill=(200, 150, 130, 255))
        draw.polygon([(570, 400), (630, 380), (600, 440)], fill=(200, 150, 130, 255))
        # Shiny black eyes and nose
        draw.ellipse([(470, 470), (490, 490)], fill=(20, 20, 20, 255))
        draw.ellipse([(550, 470), (570, 490)], fill=(20, 20, 20, 255))
        draw.ellipse([(510, 505), (530, 520)], fill=(40, 20, 20, 255))
        # Whiskers
        draw.line([(450, 510), (390, 500)], fill=(240, 240, 240, 255), width=2)
        draw.line([(450, 520), (380, 525)], fill=(240, 240, 240, 255), width=2)
        draw.line([(570, 510), (630, 500)], fill=(240, 240, 240, 255), width=2)
        draw.line([(570, 520), (640, 525)], fill=(240, 240, 240, 255), width=2)
    
    img.save(output_path, "PNG")
    print(f"  [Fallback] Saved procedural asset to: {output_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    images_dir = os.path.join(project_dir, "assets", "images")
    os.makedirs(images_dir, exist_ok=True)
    
    print("[Pipeline] Generating visual cutout sprites...")
    for spec in ASSET_SPECS:
        out_file = os.path.join(images_dir, spec["filename"])
        if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
            print(f"  [Asset exists] Skipping {spec['filename']}")
            continue
        
        print(f"\n[Asset] {spec['title']} -> {spec['filename']}")
        success = generate_via_9router(spec["prompt"], out_file)
        if not success:
            generate_procedural_fallback(spec, out_file)

if __name__ == "__main__":
    main()
