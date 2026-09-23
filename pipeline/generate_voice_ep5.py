import os
import json
import numpy as np
import soundfile as sf
import subprocess
from kokoro_onnx import Kokoro

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    audio_dir = os.path.join(project_dir, "assets", "episode5_iridium_layer", "audio")
    os.makedirs(audio_dir, exist_ok=True)

    model_dir = os.path.join(os.path.expanduser("~"), ".kokoro")
    onnx_path = os.path.join(model_dir, "kokoro-v0_19.onnx")
    voices_path = os.path.join(model_dir, "voices.bin")

    print(f"[Kokoro Ep5] Loading model from {onnx_path}...")
    kokoro = Kokoro(onnx_path, voices_path)

    # 6 Vox-style Investigation Narration Beats for 60.0s Master Timeline
    beats = [
        {
            "id": "beat_1",
            "title": "The Crime Scene · The 1-Centimeter Seam",
            "text": "For a century, science couldn't explain why every dinosaur vanished on the exact same day. Until one geologist noticed a single centimeter of mud in Italy.",
            "target_start": 0.5,
            "voice": "am_adam",
            "speed": 1.08
        },
        {
            "id": "beat_2",
            "title": "The Forensic Test · The 30x Iridium Spike",
            "text": "Inside this thin clay line, iridium levels spiked thirty times higher than normal. But iridium almost never exists in Earth's crust.",
            "target_start": 10.8,
            "voice": "am_adam",
            "speed": 1.08
        },
        {
            "id": "beat_3",
            "title": "The Cosmic Suspect · Deep Space Fallout",
            "text": "So where did it come from? Deep space. The math revealed only one suspect: a six-mile-wide asteroid, pulverized into global fallout.",
            "target_start": 20.0,
            "voice": "am_adam",
            "speed": 1.08
        },
        {
            "id": "beat_4",
            "title": "The Crater Hunt · Yucatan Satellite Anomaly",
            "text": "The missing piece was the crater. In 1991, satellite gravity maps revealed it buried beneath the Yucatan sea: a ring one hundred and ten miles wide.",
            "target_start": 29.8,
            "voice": "am_adam",
            "speed": 1.08
        },
        {
            "id": "beat_5",
            "title": "The Forensic Fingerprint · Molten Glass Tektites",
            "text": "Deep drill cores pulled up molten glass tektites. The blast released the energy of one hundred million atomic bombs, wiping out seventy-five percent of all species.",
            "target_start": 40.5,
            "voice": "am_adam",
            "speed": 1.08
        },
        {
            "id": "beat_6",
            "title": "The Case Closed · The Human Connection",
            "text": "This single centimeter of mud solved Earth's biggest murder mystery. Without it, mammals would never have risen, and humans would not exist.",
            "target_start": 51.5,
            "voice": "am_adam",
            "speed": 1.08
        }
    ]

    total_duration = 60.0
    sample_rate = 24000
    timeline = np.zeros(int(total_duration * sample_rate), dtype=np.float32)

    cues = []

    print("[Kokoro Ep5] Synthesizing narrative beats...")
    for idx, beat in enumerate(beats, start=1):
        print(f"  [{idx}/6] Synthesizing: {beat['title']}...")
        samples, sr = kokoro.create(
            beat["text"],
            voice=beat["voice"],
            speed=beat["speed"],
            lang="en-us"
        )
        samples = np.array(samples, dtype=np.float32)

        beat_filename = f"ep5_beat_{idx}.wav"
        beat_path = os.path.join(audio_dir, beat_filename)
        sf.write(beat_path, samples, sr)

        dur = len(samples) / sr
        start_t = beat["target_start"]
        start_idx = int(start_t * sample_rate)
        end_idx = min(start_idx + len(samples), len(timeline))
        clip_len = end_idx - start_idx
        timeline[start_idx:end_idx] += samples[:clip_len]

        cues.append({
            "beat_id": beat["id"],
            "title": beat["title"],
            "start": round(start_t, 2),
            "end": round(start_t + dur, 2),
            "duration": round(dur, 2),
            "text": beat["text"],
            "audio_file": beat_filename
        })
        print(f"       Duration: {dur:.2f}s | Starts at: {start_t:.2f}s | Ends at: {(start_t+dur):.2f}s")

    # Peak normalize
    max_val = np.max(np.abs(timeline))
    if max_val > 0.95:
        timeline = timeline * (0.95 / max_val)

    # Export master voice WAV
    master_vo_wav = os.path.join(audio_dir, "vo_iridium_layer.wav")
    sf.write(master_vo_wav, timeline, sample_rate)
    print(f"[Kokoro Ep5] Saved master voiceover: {master_vo_wav} (24000 Hz, 60.0s)")

    # Save audio cues JSON
    cues_path = os.path.join(audio_dir, "audio_cues_ep5.json")
    with open(cues_path, "w", encoding="utf-8") as f:
        json.dump(cues, f, indent=2)
    print(f"[Kokoro Ep5] Saved audio cues metadata: {cues_path}")

    # Convert to MP3
    master_vo_mp3 = os.path.join(audio_dir, "vo_iridium_layer.mp3")
    ffmpeg_exe = r"C:\Program Files\ShareX\ffmpeg.exe"
    subprocess.run([ffmpeg_exe, "-y", "-i", master_vo_wav, "-b:a", "192k", master_vo_mp3], check=True, capture_output=True)
    print(f"[Kokoro Ep5] Converted MP3 preview: {master_vo_mp3}")

if __name__ == "__main__":
    main()
