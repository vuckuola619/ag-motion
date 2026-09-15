import os
import math
import subprocess
import numpy as np
from PIL import Image, ImageDraw

def generate_frames():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    video_dir = os.path.join(project_dir, "assets", "video")
    temp_dir = os.path.join(video_dir, "temp_frames")
    os.makedirs(temp_dir, exist_ok=True)

    width, height = 720, 720
    fps = 30
    duration = 6.0  # 6 seconds loop
    total_frames = int(fps * duration)

    print(f"[Simulation Video] Rendering {total_frames} frames (720x720 @ {fps}fps)...")

    for f in range(total_frames):
        t = f / fps
        im = Image.new("RGBA", (width, height), (15, 18, 26, 255))
        draw = ImageDraw.Draw(im)

        # Draw tech radar circles
        cx, cy = width // 2, height // 2
        for r in [80, 160, 240, 320]:
            draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline=(40, 50, 70, 180), width=1)
        
        # Crosshair lines
        draw.line([(cx - 330, cy), (cx + 330, cy)], fill=(40, 50, 70, 140), width=1)
        draw.line([(cx, cy - 330), (cx, cy + 330)], fill=(40, 50, 70, 140), width=1)

        # Hypersonic shockwaves expanding outward
        for wave_idx in range(4):
            phase = (t * 0.9 + wave_idx * 0.4) % 1.5
            wr = int(phase * 340)
            alpha = int(255 * max(0.0, 1.0 - phase / 1.5))
            if wr > 10:
                draw.ellipse([(cx - wr, cy - wr), (cx + wr, cy + wr)], outline=(255, int(100 + 80 * math.sin(t*4)), 30, alpha), width=3)

        # Glowing fireball epicenter
        pulse = math.sin(t * 8) * 15
        core_r = int(55 + pulse)
        for cr in range(core_r, 10, -5):
            c_alpha = int(220 * (1.0 - cr / core_r))
            draw.ellipse([(cx - cr, cy - cr), (cx + cr, cy + cr)], fill=(255, min(255, int(180 - cr * 2)), 40, c_alpha))

        # Ejecta particles
        np.random.seed(42 + f)
        for _ in range(35):
            angle = np.random.uniform(0, 2 * math.pi)
            dist = np.random.uniform(30, 310) * ((t * 1.5) % 1.0)
            px = int(cx + math.cos(angle) * dist)
            py = int(cy + math.sin(angle) * dist)
            size = np.random.randint(2, 6)
            draw.ellipse([(px - size, py - size), (px + size, py + size)], fill=(255, 200, 80, 230))

        # Tech telemetry overlay
        draw.text((30, 30), "CHICXULUB IMPACT RADAR // K-Pg BOUNDARY", fill=(200, 220, 255, 220))
        draw.text((30, 50), f"HYPERSONIC ENTRY SPEED: 20.4 KM/S  |  T-{t:04.1f}S", fill=(247, 197, 0, 240))
        draw.text((30, height - 50), "IMPACT CRATER DIAMETER: 180 KM  |  SEISMIC MAGNITUDE: >11.0", fill=(160, 175, 200, 200))

        frame_path = os.path.join(temp_dir, f"frame_{f:04d}.png")
        im.save(frame_path)

    # Encode with FFmpeg
    output_mp4 = os.path.join(video_dir, "impact_simulation.mp4")
    ffmpeg_exe = r"C:\Program Files\ShareX\ffmpeg.exe"
    cmd = [
        ffmpeg_exe, "-y",
        "-framerate", str(fps),
        "-i", os.path.join(temp_dir, "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        output_mp4
    ]
    print(f"[Simulation Video] Encoding with FFmpeg -> {output_mp4}")
    subprocess.run(cmd, check=True)

    # Clean up temp frames
    for f in range(total_frames):
        try:
            os.remove(os.path.join(temp_dir, f"frame_{f:04d}.png"))
        except:
            pass
    try:
        os.rmdir(temp_dir)
    except:
        pass
    print("[Simulation Video] Complete!")

if __name__ == "__main__":
    generate_frames()
