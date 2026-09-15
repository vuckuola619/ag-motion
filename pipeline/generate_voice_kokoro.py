import os
import json
import numpy as np
import soundfile as sf
import subprocess
from kokoro_onnx import Kokoro

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    audio_dir = os.path.join(project_dir, "assets", "audio")
    os.makedirs(audio_dir, exist_ok=True)

    model_dir = os.path.join(os.path.expanduser("~"), ".kokoro")
    onnx_path = os.path.join(model_dir, "kokoro-v0_19.onnx")
    voices_path = os.path.join(model_dir, "voices.bin")

    print(f"[Kokoro] Loading model from {onnx_path}...")
    kokoro = Kokoro(onnx_path, voices_path)

    # 6 English Narration Beats for 60s BBC/Discovery style explainer
    beats = [
        {
            "id": "beat_1",
            "title": "The Age of Dinosaurs",
            "text": "Sixty-six million years ago, dinosaurs ruled the Earth as undisputed apex predators, an unbroken reign spanning over one hundred and sixty million years.",
            "target_start": 0.5,
            "voice": "am_adam",
            "speed": 1.05
        },
        {
            "id": "beat_2",
            "title": "The Chicxulub Impactor",
            "text": "From deep space, a mountain-sized asteroid ten kilometers wide hurtled toward Earth at forty-five thousand miles per hour.",
            "target_start": 10.2,
            "voice": "am_adam",
            "speed": 1.05
        },
        {
            "id": "beat_3",
            "title": "Cataclysmic Impact & Megatsunami",
            "text": "The impact in the Yucatan unleashed the fury of one hundred million megatons, triggering apocalyptic megatsunamis hundreds of meters high.",
            "target_start": 20.2,
            "voice": "am_adam",
            "speed": 1.06
        },
        {
            "id": "beat_4",
            "title": "The Deccan Traps Supervolcanoes",
            "text": "Shockwaves fractured the Earth's mantle, triggering the Deccan Traps supervolcanoes and pumping billions of tons of toxic sulfur into the skies.",
            "target_start": 30.2,
            "voice": "am_adam",
            "speed": 1.05
        },
        {
            "id": "beat_5",
            "title": "Nuclear Winter & Ecosystem Collapse",
            "text": "A suffocating blanket of soot blotted out the sun for a decade. Global temperatures plummeted, photosynthesis halted, and the food chain collapsed.",
            "target_start": 40.2,
            "voice": "am_adam",
            "speed": 1.05
        },
        {
            "id": "beat_6",
            "title": "The Iridium Boundary & Rise of Mammals",
            "text": "Seventy-five percent of all species vanished forever, leaving a thin layer of cosmic iridium... and sparking the dawn of the age of mammals.",
            "target_start": 50.2,
            "voice": "am_adam",
            "speed": 1.04
        }
    ]

    target_sr = 24000
    total_duration = 60.0
    total_samples = int(total_duration * target_sr)
    master_buffer = np.zeros(total_samples, dtype=np.float32)

    cue_points = []

    print("[Kokoro] Synthesizing 6 English narration beats for 60s explainer...")
    for beat in beats:
        print(f"  -> Generating {beat['id']}: \"{beat['title']}\"")
        samples, sr = kokoro.create(beat["text"], voice=beat["voice"], speed=beat["speed"])

        beat_path = os.path.join(audio_dir, f"{beat['id']}.wav")
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

    master_wav = os.path.join(audio_dir, "vo_dinosaurus.wav")
    sf.write(master_wav, master_buffer, target_sr)
    print(f"[Kokoro] Master WAV exported: {master_wav} (60.00s)")

    # Convert to MP3
    ffmpeg_exe = r"C:\Program Files\ShareX\ffmpeg.exe"
    master_mp3 = os.path.join(audio_dir, "vo_dinosaurus.mp3")
    cmd = [
        ffmpeg_exe, "-y",
        "-i", master_wav,
        "-codec:a", "libmp3lame",
        "-b:a", "192k",
        master_mp3
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[Kokoro] Master MP3 exported: {master_mp3}")

    cues_file = os.path.join(audio_dir, "audio_cues.json")
    with open(cues_file, "w", encoding="utf-8") as f:
        json.dump({
            "total_duration": total_duration,
            "sample_rate": target_sr,
            "language": "en",
            "voice": "am_adam",
            "cues": cue_points
        }, f, indent=2)
    print(f"[Kokoro] Cue markers saved: {cues_file}")

if __name__ == "__main__":
    main()
