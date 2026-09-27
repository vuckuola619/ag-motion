import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_DIR = os.path.join(PROJECT_ROOT, "assets", "episode6_project_azorian", "images")
ensign_path = os.path.join(TARGET_DIR, "soviet_naval_ensign_flag.png")

def make_realistic_ceremonial_flag(src_path, dst_path):
    # Load official downloaded ensign
    im = Image.open(src_path).convert("RGBA")
    w, h = im.size
    
    # Target size: 960x600
    target_w, target_h = 960, 600
    im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    arr = np.array(im, dtype=np.float32)

    # 1. Realistic 3D cloth drape waving displacement
    y_coords, x_coords = np.mgrid[0:target_h, 0:target_w]
    # Sine wave ripples
    wave = np.sin(x_coords / 65.0 + y_coords / 120.0) * 16.0 + np.sin(x_coords / 35.0) * 6.0
    
    # Lighting model based on ripple slopes (specular + diffuse shading)
    dx = np.gradient(wave, axis=1)
    shading = 1.0 + 0.22 * dx
    shading = np.clip(shading, 0.65, 1.25)

    for c in range(3):
        arr[:, :, c] = np.clip(arr[:, :, c] * shading, 0, 255)

    # 2. Add fine textile fabric grain noise
    np.random.seed(42)
    noise = np.random.normal(0, 6.0, (target_h, target_w))
    for c in range(3):
        arr[:, :, c] = np.clip(arr[:, :, c] + noise, 0, 255)

    # 3. Soft vignette / edge feather on flag cloth border
    alpha = arr[:, :, 3]
    edge_feather = 8
    # create soft alpha falloff at edges
    dist_x = np.minimum(x_coords, target_w - 1 - x_coords)
    dist_y = np.minimum(y_coords, target_h - 1 - y_coords)
    min_dist = np.minimum(dist_x, dist_y)
    alpha_mask = np.clip(min_dist / float(edge_feather), 0.0, 1.0)
    arr[:, :, 3] = alpha * alpha_mask

    result = Image.fromarray(arr.astype(np.uint8), "RGBA")
    
    # 4. Add subtle blur to blend weave
    result = result.filter(ImageFilter.GaussianBlur(0.4))
    result.save(dst_path, "PNG")
    print(f"[Success] Real ceremonial Soviet flag saved: {dst_path} ({os.path.getsize(dst_path)/1024:.1f} KB)")

if __name__ == "__main__":
    out_file = os.path.join(TARGET_DIR, "soviet_naval_ensign_flag_ceremonial.png")
    make_realistic_ceremonial_flag(ensign_path, out_file)
