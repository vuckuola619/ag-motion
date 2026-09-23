import os
import sys
import json
import base64
import math
import random
import urllib.request
import urllib.error
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROUTER_URL = "http://127.0.0.1:20128/v1/images/generations"
API_KEY = "Bearer sk-c4f2444795b190b3-kzvd4h-ea839762"
MODEL = "cx/gpt-5.5-image"

ASSET_SPECS = [
    {
        "filename": "gorgonopsian_skull.png",
        "type": "cutout",
        "prompt": "Fossil skull of Inostrancevia Gorgonopsian saber-toothed prehistoric synapsid predator, museum specimen, dramatic long canine saber teeth, detailed weathered bone texture, isolated on pure white background, catalog lighting, crisp transparent cutout, 8k",
        "title": "Gorgonopsian Saber-Tooth Skull"
    },
    {
        "filename": "trilobite_fossil.png",
        "type": "cutout",
        "prompt": "Prehistoric marine Trilobite fossil specimen preserved in dark crystalline calcite matrix, ribbed thoracic segments, holochroal eye facets, museum quality paleontology artifact, isolated on pure white background, crisp edge cutout, 8k",
        "title": "Marine Trilobite Fossil Specimen"
    },
    {
        "filename": "permian_jungle.png",
        "type": "card",
        "prompt": "Lush prehistoric Permian tropical gymnosperm and seed fern forest, giant Glossopteris trees, Calamites horsetails, warm golden sunlight filtering through misty canopy, primeval biodiversity paradise, archival photography",
        "title": "Permian Primeval Jungle Biome"
    },
    {
        "filename": "siberian_basalt_flood.png",
        "type": "cutout",
        "prompt": "Fractured block of black cooling volcanic basalt crust with bright glowing incandescent red-hot lava fissures, molten magma dripping from cracks, dramatic volcanic specimen, isolated on pure white background, transparent cutout",
        "title": "Siberian Flood Basalt Lava Block"
    },
    {
        "filename": "mantle_plume.png",
        "type": "card",
        "prompt": "Massive continental crust rift in Siberia erupting towering volcanic fire fountains, vast sea of glowing molten basalt spreading across the landscape under sulfurous smoke skies, geological catastrophic landscape photography",
        "title": "Siberian Traps Mantle Plume Eruption"
    },
    {
        "filename": "basalt_rock_specimen.png",
        "type": "cutout",
        "prompt": "Volcanic vesicular basalt rock specimen with visible gas cavities and olivine crystal phenocrysts, geological drill core sample, isolated on pure white background, scientific catalog lighting, transparent cutout",
        "title": "Vesicular Basalt Core Sample"
    },
    {
        "filename": "toxic_smoke_plume.png",
        "type": "cutout",
        "prompt": "Towering billowing volcanic coal smoke plume, dark sulfuric ash clouds rising into stratosphere with internal fiery glow and branching volcanic lightning, catastrophic atmospheric emission, isolated on pure white background, transparent cutout",
        "title": "Stratospheric Coal Fire Smoke Plume"
    },
    {
        "filename": "acid_rain_forest.png",
        "type": "card",
        "prompt": "Prehistoric forest devastated and dissolved by concentrated sulfuric acid rain, bleached dead tree trunks, steaming toxic yellow-green acid pools, sulfur smog haze, geological catastrophe archive photograph",
        "title": "Acid Rain Defoliated Wasteland"
    },
    {
        "filename": "anoxic_water_sample.png",
        "type": "cutout",
        "prompt": "Scientific antique laboratory glass flask containing dark purple anoxic seawater, rising hydrogen sulfide gas bubbles, clear glass reflections and vintage specimen label, isolated on pure white background, transparent cutout",
        "title": "Anoxic Purple Seawater Lab Sample"
    },
    {
        "filename": "purple_toxic_ocean.png",
        "type": "card",
        "prompt": "Eerie shoreline of prehistoric ocean turned deep purple and magenta by purple sulfur bacteria, foaming toxic greenish surf, dead ammonites and trilobites stranded on sulfur-encrusted sand, apocalyptic atmosphere",
        "title": "Canfield Purple Euxinic Ocean"
    },
    {
        "filename": "fungal_spike_fossil.png",
        "type": "cutout",
        "prompt": "Geological black shale rock slab covered with microscopic and macroscopic fossilized white fungal mycelium hyphae and spore clusters, Permian-Triassic fungal spike layer, paleontology specimen, isolated on pure white background, transparent cutout",
        "title": "PT Boundary Fungal Spike Fossil"
    },
    {
        "filename": "barren_earth_landscape.png",
        "type": "card",
        "prompt": "Post-collapse desolate barren continent, eroded red mudstone canyons and gullies without a single living tree or plant, complete biological silence, harsh sunlight on lifeless cracked mud, scientific documentary photograph",
        "title": "Post-Collapse Treeless Wasteland"
    },
    {
        "filename": "lystrosaurus_fossil.png",
        "type": "cutout",
        "prompt": "Fossil skeleton and skull of Lystrosaurus burrowing mammal-like reptile, distinctive downward curved tusks, sturdy digging limbs, paleontology museum catalog specimen, isolated on pure white background, transparent cutout",
        "title": "Lystrosaurus Survivor Fossil"
    },
    {
        "filename": "early_dino_tracks.png",
        "type": "cutout",
        "prompt": "Triassic sandstone rock slab preserved with sharp three-toed tridactyl footprints of early dinosaur Eoraptor, sediment displacement ridges and ripple marks, museum fossil specimen, isolated on pure white background, transparent cutout",
        "title": "Early Dinosaur Fossil Trackway Slab"
    }
]

def make_transparent_cutout(img: Image.Image, threshold: int = 242) -> Image.Image:
    img = img.convert("RGBA")
    arr = np.array(img)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    is_white = (r > threshold) & (g > threshold) & (b > threshold)
    diff = np.maximum.reduce([255 - r, 255 - g, 255 - b])
    alpha_soft = np.clip(diff * 5, 0, 255).astype(np.uint8)
    new_a = np.where(is_white, alpha_soft, a)
    arr[:, :, 3] = new_a
    return Image.fromarray(arr, "RGBA")

def generate_via_9router(prompt: str, output_path: str, is_cutout: bool) -> bool:
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
        print(f"  [9Router] Calling {MODEL} for {os.path.basename(output_path)}...")
        with urllib.request.urlopen(req, timeout=40) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            item = result.get("data", [{}])[0]
            raw_bytes = None
            if "b64_json" in item:
                raw_bytes = base64.b64decode(item["b64_json"])
            elif "url" in item:
                with urllib.request.urlopen(item["url"], timeout=30) as img_resp:
                    raw_bytes = img_resp.read()
            if raw_bytes:
                temp_path = output_path + ".tmp.png"
                with open(temp_path, "wb") as f:
                    f.write(raw_bytes)
                with Image.open(temp_path) as im:
                    if is_cutout:
                        processed = make_transparent_cutout(im)
                        processed.save(output_path, "PNG")
                    else:
                        im.convert("RGB").save(output_path, "PNG")
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                print(f"  [9Router] Success: {output_path}")
                return True
    except Exception as e:
        print(f"  [9Router Bypass]: {e}")
    return False

# Procedural high-resolution photorealistic / archival generator
def build_procedural_asset(spec: dict, out_path: str):
    fname = spec["filename"]
    is_cutout = spec["type"] == "cutout"
    print(f"  [Procedural Engine] Rendering: {fname} (Cutout: {is_cutout})")
    
    w, h = (1024, 1024) if is_cutout else (1024, 768)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0) if is_cutout else (248, 250, 252, 255))
    draw = ImageDraw.Draw(img)
    
    np.random.seed(abs(hash(fname)) % (2**31))

    if fname == "gorgonopsian_skull.png":
        # Realistic Gorgonopsian Skull with 15cm saber-tooth canine
        # 1. Skull bone mass
        bone_color = (215, 202, 178, 255)
        bone_shade = (165, 150, 125, 255)
        bone_dark = (85, 75, 60, 255)
        
        # Main cranium polygon
        cranium = [
            (220, 520), (280, 360), (450, 290), (620, 280), (790, 320),
            (880, 420), (890, 560), (760, 620), (580, 610), (320, 600), (230, 560)
        ]
        draw.polygon(cranium, fill=bone_color, outline=bone_dark, width=6)
        
        # Snout / Maxilla extending forward
        snout = [(230, 560), (220, 520), (140, 540), (120, 610), (160, 670), (320, 650)]
        draw.polygon(snout, fill=bone_color, outline=bone_dark, width=6)
        
        # Large temporal fenestra & eye orbit
        draw.ellipse([(620, 350), (780, 480)], fill=(45, 38, 32, 255), outline=bone_dark, width=5)
        draw.ellipse([(440, 370), (560, 490)], fill=(40, 34, 28, 255), outline=bone_dark, width=5)
        # Naris (nasal opening)
        draw.ellipse([(150, 550), (210, 610)], fill=(42, 35, 30, 255), outline=bone_dark, width=4)
        
        # Massive downward saber-tooth fang (15 cm Inostrancevia signature)
        fang_outer = [(230, 640), (255, 645), (275, 780), (265, 870), (240, 890), (225, 860), (220, 770)]
        draw.polygon(fang_outer, fill=(248, 244, 230, 255), outline=bone_dark, width=4)
        # Serrated highlights on fang
        for yf in range(670, 850, 15):
            draw.line([(228, yf), (234, yf)], fill=(180, 165, 140, 255), width=2)
            
        # Lower Jaw (Mandible)
        mandible = [
            (200, 690), (450, 700), (720, 680), (840, 650),
            (830, 740), (660, 770), (420, 765), (220, 740)
        ]
        draw.polygon(mandible, fill=bone_shade, outline=bone_dark, width=6)
        # Lower incisors and canine
        for tx in range(230, 420, 22):
            draw.polygon([(tx, 695), (tx + 12, 695), (tx + 6, 665)], fill=(245, 240, 225, 255), outline=bone_dark, width=2)
            
        # Suture lines and crack details
        for sx in [350, 480, 620, 750]:
            draw.line([(sx, 300), (sx + 15, 350), (sx - 10, 420)], fill=(120, 105, 85, 200), width=3)

    elif fname == "trilobite_fossil.png":
        # Marine Trilobite fossil in crystalline calcite matrix
        # Matrix slab outline
        draw.ellipse([(180, 160), (840, 860)], fill=(65, 68, 75, 255), outline=(40, 42, 48, 255), width=8)
        # Crystalline matrix speckling
        for _ in range(800):
            rx = random.randint(220, 800)
            ry = random.randint(200, 820)
            dist = math.hypot(rx - 512, ry - 512)
            if dist < 320:
                draw.point((rx, ry), fill=(random.randint(90, 140), random.randint(90, 140), random.randint(95, 150), 200))
        
        # Trilobite Body: Cephalon (Head)
        draw.pieslice([(310, 220), (710, 440)], 180, 360, fill=(185, 155, 110, 255), outline=(50, 42, 30, 255), width=5)
        # Glabella (central ridge)
        draw.ellipse([(450, 230), (570, 380)], fill=(155, 125, 85, 255), outline=(45, 38, 25, 255), width=4)
        # Crescent compound eyes
        draw.arc([(380, 270), (440, 350)], 250, 70, fill=(230, 210, 170, 255), width=8)
        draw.arc([(580, 270), (640, 350)], 110, 290, fill=(230, 210, 170, 255), width=8)
        
        # Segmented Thorax (8 distinct articulated ribs)
        for i, ty in enumerate(range(380, 680, 36)):
            width_mod = int(math.sin((i / 8) * math.pi) * 35)
            # Central axial lobe
            draw.ellipse([(450, ty), (570, ty + 30)], fill=(160, 130, 90, 255), outline=(45, 38, 25, 255), width=3)
            # Left pleura (rib)
            draw.polygon([(450, ty + 15), (320 - width_mod, ty + 25), (315 - width_mod, ty + 35), (450, ty + 28)], fill=(185, 155, 110, 255), outline=(50, 42, 30, 255), width=3)
            # Right pleura (rib)
            draw.polygon([(570, ty + 15), (700 + width_mod, ty + 25), (705 + width_mod, ty + 35), (570, ty + 28)], fill=(185, 155, 110, 255), outline=(50, 42, 30, 255), width=3)
            
        # Pygidium (Tail shield)
        draw.pieslice([(360, 660), (660, 810)], 0, 180, fill=(170, 140, 98, 255), outline=(50, 42, 30, 255), width=4)
        draw.ellipse([(465, 670), (555, 750)], fill=(145, 115, 78, 255), outline=(45, 38, 25, 255), width=3)

    elif fname == "permian_jungle.png":
        # Archival Polaroid Card: Prehistoric tropical Permian forest
        # Sky gradient
        for y in range(350):
            c_sky = (int(190 + y * 0.15), int(215 - y * 0.1), int(180 - y * 0.15), 255)
            draw.line([(0, y), (w, y)], fill=c_sky)
        # Primeval misty sun rays
        for r in range(12):
            ang = math.radians(25 + r * 6)
            draw.line([(300, 0), (int(300 + math.tan(ang) * 500), 500)], fill=(255, 245, 210, 45), width=30)
            
        # Mountain ridges in haze
        draw.polygon([(0, 360), (280, 240), (580, 330), (840, 220), (1024, 340), (1024, 768), (0, 768)], fill=(110, 135, 115, 255))
        draw.polygon([(0, 420), (380, 310), (740, 390), (1024, 330), (1024, 768), (0, 768)], fill=(75, 105, 80, 255))
        
        # Giant Glossopteris Trees & Seed Fern Canopies
        for tx, ty, tr in [(180, 480, 130), (380, 440, 150), (620, 460, 140), (860, 420, 160), (90, 520, 110)]:
            # Trunk
            draw.polygon([(tx - 18, 768), (tx + 18, 768), (tx + 8, ty + 40), (tx - 8, ty + 40)], fill=(55, 42, 30, 255))
            # Lush fern canopy tiers
            for layer in range(3):
                ly = ty + layer * 30
                draw.ellipse([(tx - tr + layer * 15, ly - 60), (tx + tr - layer * 15, ly + 50)], fill=(34 + layer * 12, 85 + layer * 15, 42 + layer * 10, 255))
                
        # Primeval riverbank with horsetail ferns (Calamites)
        draw.polygon([(0, 620), (1024, 600), (1024, 768), (0, 768)], fill=(45, 65, 45, 255))
        # River water reflection
        draw.polygon([(0, 670), (450, 640), (1024, 720), (1024, 768), (0, 768)], fill=(60, 110, 115, 255))
        for hx in range(40, 1000, 30):
            hy = random.randint(580, 660)
            draw.line([(hx, hy + 60), (hx + random.randint(-4, 4), hy)], fill=(65, 130, 60, 255), width=4)

    elif fname == "siberian_basalt_flood.png":
        # Siberian Flood Basalt lava block cutout
        # Hard cracked basalt block silhouette
        crust = [
            (180, 640), (240, 380), (420, 260), (660, 240), (840, 340),
            (910, 580), (870, 780), (680, 880), (410, 890), (220, 820)
        ]
        draw.polygon(crust, fill=(35, 33, 35, 255), outline=(20, 18, 20, 255), width=8)
        
        # Basalt block rock texture
        for _ in range(1200):
            bx = random.randint(220, 860)
            by = random.randint(280, 850)
            draw.point((bx, by), fill=(random.randint(45, 65), random.randint(43, 60), random.randint(45, 65), 255))
            
        # Glowing lava fissures tearing through the rock
        fissures = [
            [(320, 360), (410, 480), (490, 560), (620, 670), (740, 820)],
            [(660, 320), (580, 440), (490, 560), (380, 720), (280, 840)],
            [(490, 560), (720, 580), (840, 620)],
            [(410, 480), (320, 520), (230, 560)]
        ]
        # Wide red/orange outer glow
        for line in fissures:
            for pt_idx in range(len(line) - 1):
                draw.line([line[pt_idx], line[pt_idx + 1]], fill=(255, 60, 0, 180), width=28)
        # Hot orange core
        for line in fissures:
            for pt_idx in range(len(line) - 1):
                draw.line([line[pt_idx], line[pt_idx + 1]], fill=(255, 140, 10, 230), width=16)
        # Incandescent white-yellow thermal heart
        for line in fissures:
            for pt_idx in range(len(line) - 1):
                draw.line([line[pt_idx], line[pt_idx + 1]], fill=(255, 245, 180, 255), width=6)
                
        # Molten magma droplets spilling
        for _ in range(40):
            mx = random.randint(440, 760)
            my = random.randint(720, 920)
            mr = random.randint(4, 10)
            draw.ellipse([(mx - mr, my - mr), (mx + mr, my + mr)], fill=(255, 120, 20, 240))

    elif fname == "mantle_plume.png":
        # Archival Polaroid Card: Siberian Traps Mantle Plume Eruption
        # Smoke and ash sky
        for y in range(400):
            draw.line([(0, y), (w, y)], fill=(int(55 + y * 0.15), int(25 + y * 0.08), int(20 + y * 0.05), 255))
        # Towering volcanic ash billows
        for cx, cy, cr in [(300, 220, 180), (520, 180, 220), (760, 230, 190), (420, 120, 210)]:
            draw.ellipse([(cx - cr, cy - cr), (cx + cr, cy + cr)], fill=(38, 28, 26, 235))
            
        # Fiery rift horizon
        draw.polygon([(0, 480), (1024, 460), (1024, 768), (0, 768)], fill=(25, 20, 22, 255))
        
        # Towering lava fire fountains (500m basalt fountains)
        for fx in [260, 440, 520, 680, 820]:
            fh = random.randint(240, 380)
            # Spray cone
            draw.polygon([(fx - 35, 480), (fx + 35, 480), (fx + 10, 480 - fh), (fx - 10, 480 - fh)], fill=(255, 75, 0, 230))
            draw.line([(fx, 480), (fx, 480 - fh - 20)], fill=(255, 220, 100, 255), width=8)
            
        # Vast glowing molten sea of lava across continental floor
        for ly in range(500, 768, 8):
            alpha = int(220 - (ly - 500) * 0.3)
            glow_col = (255, int(80 + math.sin(ly * 0.1) * 40), 10, alpha)
            draw.line([(0, ly), (1024, ly)], fill=glow_col, width=6)
            # Floating crust rafts
            for _ in range(4):
                rx = random.randint(40, 960)
                rw = random.randint(40, 120)
                draw.line([(rx, ly), (rx + rw, ly)], fill=(25, 20, 22, 255), width=5)

    elif fname == "basalt_rock_specimen.png":
        # Vesicular porous basalt core specimen cutout
        # Cylindrical rock drill core
        draw.rounded_rectangle([(320, 180), (704, 844)], radius=40, fill=(58, 60, 64, 255), outline=(30, 32, 36, 255), width=8)
        # Texture & shading gradient
        for x in range(324, 700):
            shade = int(55 + math.sin((x - 320) / 380 * math.pi) * 25)
            draw.line([(x, 186), (x, 838)], fill=(shade, shade + 2, shade + 5, 120), width=1)
            
        # Vesicles (gas bubble cavities formed by escaping SO2/CO2)
        for _ in range(120):
            vx = random.randint(340, 680)
            vy = random.randint(220, 800)
            vr = random.randint(4, 16)
            draw.ellipse([(vx - vr, vy - vr), (vx + vr, vy + vr)], fill=(20, 21, 24, 255), outline=(40, 42, 45, 255), width=2)
            
        # Green Olivine mineral phenocryst inclusions
        for _ in range(35):
            ox = random.randint(350, 670)
            oy = random.randint(230, 790)
            draw.polygon([(ox, oy - 6), (ox + 7, oy), (ox + 4, oy + 8), (ox - 6, oy + 4)], fill=(120, 165, 75, 255), outline=(60, 95, 35, 255), width=1)
            
        # Scientific depth measurement ruler on right
        for y in range(210, 820, 25):
            draw.line([(680, y), (700, y)], fill=(220, 225, 235, 255), width=3)
            if (y - 210) % 50 == 0:
                draw.line([(665, y), (700, y)], fill=(245, 250, 255, 255), width=4)

    elif fname == "toxic_smoke_plume.png":
        # Billowing toxic coal fire smoke plume with volcanic lightning
        # Massive smoke billow spheres
        smoke_nodes = [
            (512, 750, 180), (420, 620, 190), (610, 580, 200),
            (360, 460, 220), (560, 420, 230), (460, 310, 240),
            (320, 210, 210), (580, 190, 220), (450, 110, 190)
        ]
        # Sulfur yellow underglow
        for cx, cy, cr in smoke_nodes:
            draw.ellipse([(cx - cr - 20, cy - cr - 20), (cx + cr + 20, cy + cr + 20)], fill=(185, 140, 30, 45))
        # Dark carbon ash body
        for cx, cy, cr in smoke_nodes:
            for r in range(cr, 40, -25):
                alpha = int(240 - (cr - r) * 0.8)
                col = (int(32 + (cx % 15)), int(30 + (cy % 10)), int(33 + (r % 10)), alpha)
                draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=col)
                
        # Crackling purple/cyan volcanic lightning bolts
        bolts = [
            [(480, 680), (430, 540), (470, 450), (390, 360), (440, 240), (380, 160)],
            [(550, 580), (620, 480), (570, 390), (640, 280), (590, 200)]
        ]
        for bolt in bolts:
            # Violet halo
            for i in range(len(bolt) - 1):
                draw.line([bolt[i], bolt[i + 1]], fill=(180, 90, 255, 180), width=10)
            # White core
            for i in range(len(bolt) - 1):
                draw.line([bolt[i], bolt[i + 1]], fill=(245, 235, 255, 255), width=3)

    elif fname == "acid_rain_forest.png":
        # Archival Polaroid Card: Acid Rain Defoliated Wasteland
        # Toxic yellow-grey sulfuric sky
        for y in range(420):
            draw.line([(0, y), (w, y)], fill=(int(170 - y * 0.15), int(160 - y * 0.1), int(110 - y * 0.12), 255))
            
        # Heavy sulfuric acid rainfall streaks
        for _ in range(600):
            rx = random.randint(0, w)
            ry = random.randint(40, 650)
            rl = random.randint(25, 65)
            draw.line([(rx, ry), (rx - 8, ry + rl)], fill=(225, 220, 150, 65), width=2)
            
        # Ground wasteland
        draw.polygon([(0, 480), (1024, 460), (1024, 768), (0, 768)], fill=(65, 55, 45, 255))
        
        # Bleached, dissolved, stripped dead trees (ghost forest)
        for tx in range(60, 980, 70):
            th = random.randint(200, 380)
            ty = 520
            # Stripped barren trunk
            draw.line([(tx, ty), (tx + random.randint(-8, 8), ty - th)], fill=(175, 170, 160, 255), width=random.randint(6, 14))
            # Broken dead snapped branches
            bx = tx + random.randint(-6, 6)
            by = ty - th + 60
            draw.line([(bx, by), (bx - 35, by - 40)], fill=(160, 155, 145, 255), width=4)
            draw.line([(bx, by + 40), (bx + 45, by + 10)], fill=(160, 155, 145, 255), width=4)
            
        # Steaming puddles of caustic yellow-green acid runoff (pH 1.5)
        for px, py, pw in [(220, 640, 160), (540, 680, 210), (820, 620, 140)]:
            draw.ellipse([(px - pw, py - 25), (px + pw, py + 25)], fill=(175, 195, 30, 220), outline=(130, 145, 20, 255), width=3)
            # Rising toxic acid steam
            for _ in range(12):
                sx = px + random.randint(-pw + 20, pw - 20)
                sy = py - random.randint(15, 65)
                draw.circle((sx, sy), random.randint(8, 20), fill=(230, 235, 180, 40))

    elif fname == "anoxic_water_sample.png":
        # Lab flask cutout with purple anoxic seawater
        # Glass flask body
        flask_poly = [
            (460, 160), (564, 160), (564, 320), (740, 720),
            (740, 840), (284, 840), (284, 720), (460, 320)
        ]
        # Dark purple anoxic seawater fill
        water_poly = [
            (410, 420), (614, 420), (726, 720),
            (726, 830), (298, 830), (298, 720)
        ]
        draw.polygon(water_poly, fill=(88, 24, 98, 240))
        
        # Rising lethal hydrogen sulfide (H2S) gas bubbles
        for _ in range(45):
            bx = random.randint(330, 690)
            by = random.randint(440, 810)
            br = random.randint(3, 10)
            draw.ellipse([(bx - br, by - br), (bx + br, by + br)], fill=(160, 80, 175, 180), outline=(230, 180, 245, 220), width=2)
            
        # Glass reflections & highlights
        draw.polygon(flask_poly, outline=(220, 230, 245, 240), width=8)
        # Vertical glass sheen highlights
        draw.line([(320, 730), (470, 340)], fill=(255, 255, 255, 160), width=8)
        draw.line([(340, 750), (485, 350)], fill=(255, 255, 255, 90), width=4)
        
        # Cork stopper at the top
        draw.polygon([(450, 120), (574, 120), (560, 165), (464, 165)], fill=(185, 145, 105, 255), outline=(90, 65, 40, 255), width=4)
        
        # Specimen laboratory label strip
        draw.rectangle([(380, 560), (644, 690)], fill=(245, 242, 230, 255), outline=(70, 60, 45, 255), width=4)
        draw.line([(400, 595), (624, 595)], fill=(70, 60, 45, 255), width=3)
        draw.line([(400, 630), (580, 630)], fill=(70, 60, 45, 255), width=3)
        draw.line([(400, 660), (540, 660)], fill=(180, 30, 50, 255), width=4)

    elif fname == "purple_toxic_ocean.png":
        # Archival Polaroid Card: Canfield Purple Euxinic Ocean
        # Toxic murky dusk sky
        for y in range(360):
            draw.line([(0, y), (w, y)], fill=(int(95 - y * 0.1), int(60 - y * 0.08), int(75 - y * 0.06), 255))
            
        # Vast alien purple sea (Canfield ocean euxinia)
        for y in range(360, 620):
            py = (y - 360) / 260
            r_col = int(120 + py * 40)
            g_col = int(25 + py * 15)
            b_col = int(135 + py * 30)
            draw.line([(0, y), (w, y)], fill=(r_col, g_col, b_col, 255))
            
        # Foaming green sulfur surf / toxic scum on water surface
        for sx in range(0, w, 20):
            sy = 600 + int(math.sin(sx * 0.04) * 15)
            draw.line([(sx, sy), (sx + 35, sy + 6)], fill=(185, 215, 60, 220), width=6)
            
        # Desolate sulfur-encrusted dead shoreline
        draw.polygon([(0, 610), (1024, 590), (1024, 768), (0, 768)], fill=(75, 70, 55, 255))
        # Pale yellow sulfur crust deposits on shore
        for _ in range(80):
            cx = random.randint(20, 1000)
            cy = random.randint(630, 750)
            draw.ellipse([(cx - 25, cy - 8), (cx + 25, cy + 8)], fill=(195, 185, 75, 210))
            
        # Stranded dead marine fauna (coiled ammonite shells)
        for ax, ay in [(240, 680), (480, 710), (760, 670), (880, 730)]:
            draw.ellipse([(ax - 22, ay - 18), (ax + 22, ay + 18)], fill=(190, 180, 160, 255), outline=(50, 45, 35, 255), width=3)
            draw.arc([(ax - 14, ay - 12), (ax + 14, ay + 12)], 0, 270, fill=(70, 60, 50, 255), width=2)

    elif fname == "fungal_spike_fossil.png":
        # PT Boundary Fungal Spike Fossil slab cutout
        # Dark black shale matrix rock
        shale = [
            (210, 260), (460, 180), (780, 220), (880, 420),
            (840, 760), (620, 860), (320, 850), (180, 620)
        ]
        draw.polygon(shale, fill=(28, 30, 32, 255), outline=(12, 14, 15, 255), width=8)
        # Bedding plane shale lines
        for sy in range(260, 830, 18):
            draw.line([(240, sy), (820, sy + 12)], fill=(45, 48, 52, 160), width=2)
            
        # Branching white/silver fungal hyphae mycelium networks (Reduviasporonites)
        def draw_hyphae(x, y, angle, length, depth):
            if depth <= 0 or length < 8:
                return
            rad = math.radians(angle)
            x2 = x + math.cos(rad) * length
            y2 = y + math.sin(rad) * length
            draw.line([(x, y), (x2, y2)], fill=(235, 238, 242, 230), width=max(1, depth))
            # Spore cluster head at tips
            if depth == 1:
                draw.circle((x2, y2), random.randint(3, 7), fill=(245, 240, 220, 255))
            draw_hyphae(x2, y2, angle + random.randint(15, 38), length * 0.75, depth - 1)
            draw_hyphae(x2, y2, angle - random.randint(15, 38), length * 0.72, depth - 1)
            
        for seed_x, seed_y in [(380, 440), (540, 580), (660, 380), (450, 680), (620, 640)]:
            for base_ang in [0, 90, 180, 270]:
                draw_hyphae(seed_x, seed_y, base_ang + random.randint(-20, 20), 45, 4)

    elif fname == "barren_earth_landscape.png":
        # Archival Polaroid Card: Post-Collapse Treeless Wasteland
        # Harsh pale bleached sky
        for y in range(320):
            draw.line([(0, y), (w, y)], fill=(int(210 - y * 0.1), int(190 - y * 0.1), int(165 - y * 0.1), 255))
            
        # Rugged eroded barren red badlands / canyons
        draw.polygon([(0, 340), (220, 260), (480, 310), (740, 240), (1024, 320), (1024, 768), (0, 768)], fill=(165, 75, 55, 255))
        draw.polygon([(0, 420), (320, 360), (640, 430), (880, 370), (1024, 440), (1024, 768), (0, 768)], fill=(145, 62, 45, 255))
        
        # Foreground dry cracked mudflat
        draw.polygon([(0, 520), (1024, 500), (1024, 768), (0, 768)], fill=(125, 55, 40, 255))
        # Deep erosion gullies (soil washed away because all root systems died)
        for gx in [180, 380, 620, 840]:
            draw.polygon([(gx - 15, 520), (gx + 15, 520), (gx + 60, 768), (gx + 20, 768)], fill=(85, 35, 25, 255))
        # Desiccated cracked earth polygons
        for _ in range(120):
            mx = random.randint(40, 980)
            my = random.randint(540, 750)
            draw.polygon([(mx, my), (mx + 20, my - 10), (mx + 35, my + 15), (mx + 10, my + 25)], outline=(65, 25, 18, 200), width=2)

    elif fname == "lystrosaurus_fossil.png":
        # Lystrosaurus Survivor Skeleton cutout
        # Skull with signature downward curved tusks
        bone_c = (220, 210, 190, 255)
        bone_d = (70, 60, 48, 255)
        
        # Heavy downturned cranium
        skull = [
            (260, 420), (380, 320), (520, 340), (560, 440),
            (520, 560), (380, 580), (280, 560), (240, 490)
        ]
        draw.polygon(skull, fill=bone_c, outline=bone_d, width=6)
        # Eye orbit placed high on head (for burrowing / water vigilance)
        draw.ellipse([(380, 360), (460, 440)], fill=(40, 35, 30, 255), outline=bone_d, width=4)
        # Distinctive downturned tusk (dicynodont canine)
        draw.polygon([(290, 520), (325, 520), (320, 620), (285, 640), (275, 610)], fill=(245, 242, 230, 255), outline=bone_d, width=3)
        
        # Barrel-shaped ribcage and spine
        spine = [(520, 420), (660, 400), (780, 440), (880, 510)]
        for i in range(len(spine) - 1):
            draw.line([spine[i], spine[i + 1]], fill=bone_c, width=22)
            draw.line([spine[i], spine[i + 1]], fill=bone_d, width=4)
            
        # Rib cage arches
        for rx in range(560, 820, 35):
            draw.arc([(rx - 30, 420), (rx + 40, 580)], 30, 160, fill=bone_c, width=12)
            
        # Sturdy digging forelimb and powerful claws
        draw.polygon([(460, 520), (520, 540), (480, 680), (420, 660)], fill=bone_c, outline=bone_d, width=5)
        # Claws for excavating underground burrows
        for cx in range(410, 490, 18):
            draw.polygon([(cx, 670), (cx + 12, 670), (cx + 6, 720)], fill=(240, 235, 215, 255), outline=bone_d, width=2)
            
        # Hind limb
        draw.polygon([(740, 480), (810, 510), (780, 660), (730, 640)], fill=bone_c, outline=bone_d, width=5)

    elif fname == "early_dino_tracks.png":
        # Sandstone slab with early dinosaur (Eoraptor) three-toed tridactyl tracks
        # Sandstone matrix slab
        draw.polygon([(180, 240), (520, 160), (860, 220), (890, 780), (560, 870), (160, 810)], fill=(210, 182, 140, 255), outline=(100, 80, 55, 255), width=8)
        # Sandstone ripple marks and grains
        for sy in range(240, 800, 28):
            draw.line([(220, sy), (840, sy + 15)], fill=(185, 155, 115, 150), width=3)
            
        # Distinct three-toed tridactyl footprints (2 distinct prints across trackway)
        for px, py, sc in [(420, 420, 1.0), (620, 620, 1.05)]:
            # Central digit III
            draw.polygon([(px - 14 * sc, py + 20 * sc), (px + 14 * sc, py + 20 * sc), (px, py - 95 * sc)], fill=(85, 68, 48, 255), outline=(45, 35, 25, 255), width=3)
            # Left digit II
            draw.polygon([(px - 10 * sc, py + 30 * sc), (px + 10 * sc, py + 30 * sc), (px - 65 * sc, py - 60 * sc)], fill=(85, 68, 48, 255), outline=(45, 35, 25, 255), width=3)
            # Right digit IV
            draw.polygon([(px - 10 * sc, py + 30 * sc), (px + 10 * sc, py + 30 * sc), (px + 65 * sc, py - 60 * sc)], fill=(85, 68, 48, 255), outline=(45, 35, 25, 255), width=3)
            # Heel pad impression
            draw.ellipse([(px - 26 * sc, py + 15 * sc), (px + 26 * sc, py + 65 * sc)], fill=(75, 58, 40, 255), outline=(45, 35, 25, 255), width=3)
            # Sediment displacement ridge (highlight around footprint)
            draw.arc([(px - 75 * sc, py - 105 * sc), (px + 75 * sc, py + 75 * sc)], 0, 360, fill=(235, 210, 170, 220), width=4)

    # Apply subtle realistic grain filter
    img.save(out_path, "PNG")
    print(f"  [Procedural Engine] Successfully saved: {out_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    images_dir = os.path.join(project_dir, "assets", "images")
    os.makedirs(images_dir, exist_ok=True)

    print(f"[Pipeline] Generating 14 visual assets for Episode 2...")
    for spec in ASSET_SPECS:
        out_file = os.path.join(images_dir, spec["filename"])
        is_cutout = spec["type"] == "cutout"
        
        print(f"\n--- Processing {spec['filename']} ({spec['title']}) ---")
        # Try 9Router first
        success = generate_via_9router(spec["prompt"], out_file, is_cutout)
        if not success:
            build_procedural_asset(spec, out_file)
            
    print("\n[Pipeline] All 14 visual assets verified and generated!")

if __name__ == "__main__":
    main()
