import os
import math
import subprocess
import numpy as np
from PIL import Image, ImageDraw

def generate_tsunami_clip():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    video_dir = os.path.join(project_dir, "assets", "video")
    temp_dir = os.path.join(video_dir, "temp_tsunami_frames")
    os.makedirs(temp_dir, exist_ok=True)

    width, height = 720, 720
    fps = 30
    duration = 6.0
    total_frames = int(fps * duration)

    print(f"[Tsunami Video] Rendering {total_frames} frames (720x720 @ {fps}fps)...")

    for f in range(total_frames):
        t = f / fps
        im = Image.new("RGBA", (width, height), (10, 14, 22, 255))
        draw = ImageDraw.Draw(im)

        cx, cy = width // 2, height // 2

        # Bathymetric ocean grid
        for grid_r in range(60, 360, 60):
            draw.ellipse([(cx - grid_r, cy - grid_r), (cx + grid_r, cy + grid_r)], outline=(25, 45, 75, 160), width=1)
        draw.line([(cx - 320, cy), (cx + 320, cy)], fill=(30, 50, 80, 130), width=1)
        draw.line([(cx, cy - 320), (cx, cy + 320)], fill=(30, 50, 80, 130), width=1)

        # Concentric Megatsunami wave fronts (300m wave surge)
        for wave_i in range(5):
            phase = (t * 0.85 + wave_i * 0.35) % 1.6
            wave_r = int(phase * 340)
            alpha = int(255 * max(0.0, 1.0 - (phase / 1.6)))
            if wave_r > 15:
                draw.ellipse([(cx - wave_r, cy - wave_r), (cx + wave_r, cy + wave_r)], outline=(37, 99, 235, alpha), width=4)
                # Crest glow
                draw.ellipse([(cx - wave_r + 2, cy - wave_r + 2), (cx + wave_r - 2, cy + wave_r - 2)], outline=(147, 197, 253, alpha // 2), width=2)

        # Shockwave epicenter pulse
        pulse = abs(math.sin(t * 6)) * 20
        draw.ellipse([(cx - 40 - pulse, cy - 40 - pulse), (cx + 40 + pulse, cy + 40 + pulse)], outline=(225, 29, 72, 220), width=3)
        draw.ellipse([(cx - 20, cy - 20), (cx + 20, cy + 20)], fill=(225, 29, 72, 240))

        # Seismic telemetry
        draw.text((26, 26), "CARIBBEAN BASIN // MEGATSUNAMI PROPAGATION", fill=(219, 234, 254, 230))
        draw.text((26, 46), f"PEAK WAVE HEIGHT: 320 METERS  |  T+{t:04.1f}S", fill=(251, 191, 36, 240))
        draw.text((26, height - 46), "CRATER CAVITY COLLAPSE  |  GLOBAL TSUNAMI ACTIVE", fill=(148, 163, 184, 200))

        frame_path = os.path.join(temp_dir, f"frame_{f:04d}.png")
        im.save(frame_path)

    output_mp4 = os.path.join(video_dir, "tsunami_simulation.mp4")
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
    subprocess.run(cmd, check=True)

    for f in range(total_frames):
        try:
            os.remove(os.path.join(temp_dir, f"frame_{f:04d}.png"))
        except:
            pass
    try:
        os.rmdir(temp_dir)
    except:
        pass
    print(f"[Tsunami Video] Successfully rendered: {output_mp4}")

if __name__ == "__main__":
    generate_tsunami_clip()
