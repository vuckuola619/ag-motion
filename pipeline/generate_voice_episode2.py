import os
import json
import numpy as np
import soundfile as sf
import subprocess
from kokoro_onnx import Kokoro

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    audio_dir = os.path.join(project_dir, "assets", "episode2_great_dying", "audio")
    os.makedirs(audio_dir, exist_ok=True)

    model_dir = os.path.join(os.path.expanduser("~"), ".kokoro")
    onnx_path = os.path.join(model_dir, "kokoro-v0_19.onnx")
    voices_path = os.path.join(model_dir, "voices.bin")

    print(f"[Kokoro Ep2] Loading model from {onnx_path}...")
    kokoro = Kokoro(onnx_path, voices_path)

    # 7 English Narration Beats for 70.0s BBC/Discovery documentary pacing
    beats = [
        {
            "id": "beat_1",
            "title": "The Permian Paradise",
            "text": "Two hundred and fifty-two million years ago, before dinosaurs existed, saber-toothed predators and giant synapsids ruled a thriving prehistoric Earth.",
            "target_start": 0.6,
            "voice": "am_adam",
            "speed": 1.05
        },
        {
            "id": "beat_2",
            "title": "The Siberian Traps Inferno",
            "text": "Until the continental crust ripped open in Siberia, unleashing three million cubic kilometers of molten basalt in an eruption that burned for a million years.",
            "target_start": 11.2,
            "voice": "am_adam",
            "speed": 1.05
        },
        {
            "id": "beat_3",
            "title": "Coal Fires & Acid Rain",
            "text": "Subterranean magma ignited massive ancient coal seams, pumping billions of tons of toxic sulfur into the skies and unleashing acid rain as caustic as battery acid.",
            "target_start": 22.2,
            "voice": "am_adam",
            "speed": 1.06
        },
        {
            "id": "beat_4",
            "title": "The Purple Dying Oceans",
            "text": "As superheated seas choked and lost all oxygen, toxic bacteria turned the oceans purple, suffocating ninety-six percent of all marine species.",
            "target_start": 33.2,
            "voice": "am_adam",
            "speed": 1.05
        },
        {
            "id": "beat_5",
            "title": "The Fungal Spike & Total Collapse",
            "text": "Continents turned into rotting wastelands. Every forest on Earth collapsed, triggering a planetary fungal spike feeding on millions of dead trees.",
            "target_start": 44.2,
            "voice": "am_adam",
            "speed": 1.05
        },
        {
            "id": "beat_6",
            "title": "The Lonely Survivor & Dawn of Dinosaurs",
            "text": "Against impossible odds, a single burrowing survivor endured underground: Lystrosaurus, clearing the evolutionary stage for the rise of dinosaurs.",
            "target_start": 55.2,
            "voice": "am_adam",
            "speed": 1.05
        },
        {
            "id": "beat_7_outro",
            "title": "Resolution: Life Survived",
            "text": "Life faced its closest brush with death. Without this catastrophic reset, we would never exist.",
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

    print("[Kokoro Ep2] Synthesizing English narration beats for 70.0s explainer...")
    for beat in beats:
        print(f"  -> Generating {beat['id']}: \"{beat['title']}\"")
        samples, sr = kokoro.create(beat["text"], voice=beat["voice"], speed=beat["speed"])

        beat_path = os.path.join(audio_dir, f"ep2_{beat['id']}.wav")
        sf.write(beat_path, samples, sr)

        clip_dur = len(samples) / sr
        start_sec = beat["target_start"]
        end_sec = start_sec + clip_dur

        start_idx = int(start_sec * target_sr)
        end_idx = min(start_idx + len(samples), total_samples)
        slice_len = end_idx - start_idx
        master_buffer[start_idx:end_idx] += samples[:slice_len]

        cue_points.append({
            "id": beat["id"],
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

    master_wav = os.path.join(audio_dir, "vo_great_dying.wav")
    sf.write(master_wav, master_buffer, target_sr)
    print(f"[Kokoro Ep2] Master WAV exported: {master_wav} ({total_duration:.2f}s)")

    # Convert to MP3
    ffmpeg_exe = r"C:\Program Files\ShareX\ffmpeg.exe"
    master_mp3 = os.path.join(audio_dir, "vo_great_dying.mp3")
    cmd = [
        ffmpeg_exe, "-y",
        "-i", master_wav,
        "-codec:a", "libmp3lame",
        "-b:a", "192k",
        master_mp3
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[Kokoro Ep2] Master MP3 exported: {master_mp3}")

    cues_file = os.path.join(audio_dir, "audio_cues_ep2.json")
    with open(cues_file, "w", encoding="utf-8") as f:
        json.dump({
            "total_duration": total_duration,
            "sample_rate": target_sr,
            "language": "en",
            "voice": "am_adam",
            "cues": cue_points
        }, f, indent=2)
    print(f"[Kokoro Ep2] Cue markers saved: {cues_file}")

if __name__ == "__main__":
    main()
