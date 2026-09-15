import urllib.request, json, os, base64
from PIL import Image
import numpy as np

ROUTER_URL = 'http://127.0.0.1:20128/v1/images/generations'
API_KEY = 'Bearer sk-c4f2444795b190b3-kzvd4h-ea839762'
MODEL = 'cx/gpt-5.5-image'

SPECS = [
    {
        'filename': 'megatsunami_wave_realistic.png',
        'prompt': 'A hyper-realistic cinematic photograph of a cataclysmic 1,000-foot megatsunami ocean wave towering and crashing over prehistoric Cretaceous coastline, colossal wall of dark water and churning white sea foam, apocalyptic scale, photorealistic 8k, IMAX documentary style',
        'transparent': False
    },
    {
        'filename': 'meteorite_chondrite.png',
        'prompt': 'A museum specimen of a black carbonaceous chondrite meteorite rock with aerodynamic fusion crust and regmaglypt thumbprints, isolated on pure white background, studio scientific catalog lighting, sharp crisp edges, 8k catalog specimen cutout',
        'transparent': True
    },
    {
        'filename': 'chicxulub_crater_aerial.png',
        'prompt': 'Realistic high-altitude geological satellite photograph of the Chicxulub impact crater ring structure in the Yucatan peninsula and Gulf of Mexico, visible circular shock ridges under turquoise shallow sea waters, scientific bathymetry, photorealistic 8k',
        'transparent': False
    }
]

def make_transparent_cutout(img, threshold=245):
    img = img.convert('RGBA')
    arr = np.array(img)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    is_white = (r > threshold) & (g > threshold) & (b > threshold)
    diff = np.maximum.reduce([255 - r, 255 - g, 255 - b])
    alpha_soft = np.clip(diff * 5, 0, 255).astype(np.uint8)
    new_a = np.where(is_white, alpha_soft, a)
    arr[:, :, 3] = new_a
    return Image.fromarray(arr, 'RGBA')

os.makedirs('assets/images', exist_ok=True)

for spec in SPECS:
    fname = spec['filename']
    out_path = os.path.join('assets/images', fname)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 100000:
        print(f"[SKIP] Already exists: {fname}")
        continue
    print(f"Generating: {fname}...")
    payload = {
        'model': MODEL,
        'prompt': spec['prompt'],
        'n': 1,
        'size': '1024x1024'
    }
    req = urllib.request.Request(
        ROUTER_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Authorization': API_KEY}
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            item = data.get('data', [{}])[0]
            raw = None
            if 'b64_json' in item:
                raw = base64.b64decode(item['b64_json'])
            elif 'url' in item:
                with urllib.request.urlopen(item['url'], timeout=45) as ir:
                    raw = ir.read()
            if raw:
                tmp = out_path + '.tmp.png'
                with open(tmp, 'wb') as f:
                    f.write(raw)
                with Image.open(tmp) as im:
                    if spec.get('transparent'):
                        im = make_transparent_cutout(im)
                    im.save(out_path, 'PNG')
                if os.path.exists(tmp):
                    os.remove(tmp)
                print(f"  [OK] Saved: {out_path}")
            else:
                print(f"  [FAIL] No image data returned for {fname}")
    except Exception as e:
        print(f"  [ERR] Error generating {fname}: {e}")
