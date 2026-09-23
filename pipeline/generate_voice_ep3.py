import os
import json
import numpy as np
import soundfile as sf
import subprocess
from kokoro_onnx import Kokoro

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    audio_dir = os.path.join(project_dir, "assets", "episode3_carnian_pluvial", "audio")
    os.makedirs(audio_dir, exist_ok=True)

    model_dir = os.path.join(os.path.expanduser("~"), ".kokoro")
    onnx_path = os.path.join(model_dir, "kokoro-v0_19.onnx")
    voices_path = os.path.join(model_dir, "voices.bin")

    print(f"[Kokoro Ep3] Loading model from {onnx_path}...")
    kokoro = Kokoro(onnx_path, voices_path)

    # 7 English Narration Beats for 70.0s BBC/Discovery documentary pacing
    beats = [
        {
            "id": "beat_1",
            "title": "The Arid Pangea Dustbowl",
            "text": "Two hundred and thirty-four million years ago, the supercontinent of Pangea was a baking, bone-dry wasteland. Dinosaurs were tiny, rare, and pushed to the sidelines of a scorched planet.",
            "target_start": 0.6,
            "voice": "am_adam",
            "speed": 1.05
        },
        {
            "id": "beat_2",
            "title": "Wrangellia Oceanic Super-Volcano",
            "text": "Until catastrophic flood basalts ruptured the ocean floor in Wrangellia. Billions of tons of greenhouse gases superheated the atmosphere, turning Earth's oceans into giant boiling evaporators.",
            "target_start": 11.2,
            "voice": "am_adam",
            "speed": 1.05
        },
        {
            "id": "beat_3",
            "title": "The Two-Million-Year Deluge",
            "text": "Then, the skies broke. Moisture saturated the atmosphere until torrential rains fell across every corner of the supercontinent. A storm that did not stop for two million years.",
            "target_start": 22.2,
            "voice": "am_adam",
            "speed": 1.05
        },
        {
            "id": "beat_4",
            "title": "The Amber Spike & Conifer Swamps",
            "text": "Rivers drowned the deserts in thick mud. Sweltering conifer forests exploded across the land, weeping massive tears of resin—leaving behind the oldest amber deposits in Earth's history.",
            "target_start": 33.2,
            "voice": "am_adam",
            "speed": 1.05
        },
        {
            "id": "beat_5",
            "title": "The Carnian Extinction",
            "text": "For ancient desert reptiles, it was the end of the world. Unable to digest the tough new conifer leaves, dominant plant-eaters collapsed and starved in the endless deluge.",
            "target_start": 44.2,
            "voice": "am_adam",
            "speed": 1.05
        },
        {
            "id": "beat_6",
            "title": "The Dawn of the Dinosaur Empire",
            "text": "From the mud emerged the ultimate opportunists: early dinosaurs. Agile, fast, and adaptable, they surged from less than five percent of land animals to ruling the entire planet.",
            "target_start": 55.2,
            "voice": "am_adam",
            "speed": 1.05
        },
        {
            "id": "beat_7_outro",
            "title": "Resolution: The Storm Created Giants",
            "text": "Two million years of rain reshaped the biosphere forever. Without the great Triassic storm, dinosaurs would never have ruled the Earth.",
            "target_start": 64.8,
            "voice": "am_adam",
            "speed": 1.06
        }
    ]

    target_sr = 24000
    total_duration = 70.0
    total_samples = int(total_duration * target_sr)
    master_buffer = np.zeros(total_samples, dtype=np.float32)

    cue_points = []

    print("[Kokoro Ep3] Synthesizing English narration beats for 70.0s explainer...")
    for beat in beats:
        print(f"  -> Generating {beat['id']}: \"{beat['title']}\"")
        samples, sr = kokoro.create(beat["text"], voice=beat["voice"], speed=beat["speed"])

        beat_path = os.path.join(audio_dir, f"ep3_{beat['id']}.wav")
        sf.write(beat_path, samples, sr)

        clip_dur = len(samples) / sr
        start_sec = beat["target_start"]
        end_sec = start_sec + clip_dur

        start_idx = int(start_sec * target_sr)
        end_idx = min(start_idx + len(samples), total_samples)
        slice_len = end_idx - start_idx
        master_buffer[start_idx:end_idx] += samples[:slice_len]

        cue_points.append({
            "id": f"ep3_{beat['id']}",
            "title": beat["title"],
            "start": round(start_sec, 2),
            "end": round(end_sec, 2),
            "duration": round(clip_dur, 2),
            "text": beat["text"]
        })
        print(f"     Duration: {clip_dur:.2f}s (from {start_sec:.2f}s to {end_sec:.2f}s)")

    # Peak normalization to -1.0 dB
    max_val = np.max(np.abs(master_buffer))
    if max_val > 0:
        master_buffer = (master_buffer / max_val) * 0.89

    master_wav = os.path.join(audio_dir, "vo_carnian_pluvial.wav")
    sf.write(master_wav, master_buffer, target_sr)
    print(f"[Kokoro Ep3] Master WAV exported: {master_wav} ({total_duration:.2f}s)")

    # Convert to MP3
    ffmpeg_exe = r"C:\Program Files\ShareX\ffmpeg.exe"
    master_mp3 = os.path.join(audio_dir, "vo_carnian_pluvial.mp3")
    cmd = [
        ffmpeg_exe, "-y",
        "-i", master_wav,
        "-codec:a", "libmp3lame",
        "-b:a", "192k",
        master_mp3
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[Kokoro Ep3] Master MP3 exported: {master_mp3}")

    cues_file = os.path.join(audio_dir, "audio_cues_ep3.json")
    with open(cues_file, "w", encoding="utf-8") as f:
        json.dump({
            "total_duration": total_duration,
            "sample_rate": target_sr,
            "language": "en",
            "voice": "am_adam",
            "cues": cue_points
        }, f, indent=2)
    print(f"[Kokoro Ep3] Cue markers saved: {cues_file}")

if __name__ == "__main__":
    main()
