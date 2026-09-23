import os
import json
import numpy as np
import soundfile as sf
import subprocess
from kokoro_onnx import Kokoro

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    audio_dir = os.path.join(project_dir, "assets", "episode4_chicxulub", "audio")
    os.makedirs(audio_dir, exist_ok=True)

    model_dir = os.path.join(os.path.expanduser("~"), ".kokoro")
    onnx_path = os.path.join(model_dir, "kokoro-v0_19.onnx")
    voices_path = os.path.join(model_dir, "voices.bin")

    print(f"[Kokoro Ep4] Loading model from {onnx_path}...")
    kokoro = Kokoro(onnx_path, voices_path)

    # 7 English Narration Beats for 70.0s BBC/Discovery countdown pacing (Zero collision, generous transition buffers)
    beats = [
        {
            "id": "beat_1",
            "title": "T-Minus 10s · The Impactor Approaches",
            "text": "Sixty-six million years ago, a mountain of rock six miles wide tore through the sky at forty-five thousand miles per hour. Dinosaurs had ten seconds left.",
            "target_start": 0.8,
            "voice": "am_adam",
            "speed": 1.08
        },
        {
            "id": "beat_2",
            "title": "Minute 0 · Ground Zero Impact",
            "text": "It struck Yucatán with the force of one hundred million atomic bombs, instantly vaporizing miles of Earth's crust into a glowing crater.",
            "target_start": 11.2,
            "voice": "am_adam",
            "speed": 1.08
        },
        {
            "id": "beat_3",
            "title": "Minute 5 · The Thermal Radiation Pulse",
            "text": "Within five minutes, an infrared heat pulse swept the globe, turning the entire atmosphere into a 1,500-degree broiler oven.",
            "target_start": 21.4,
            "voice": "am_adam",
            "speed": 1.08
        },
        {
            "id": "beat_4",
            "title": "Hour 1 · Molten Glass & Megatsunamis",
            "text": "Trillions of tons of molten glass tektites rained from orbit, while thousand-foot megatsunamis pulverized continental coastlines.",
            "target_start": 31.6,
            "voice": "am_adam",
            "speed": 1.08
        },
        {
            "id": "beat_5",
            "title": "Hour 24 · The Nuclear Ash Winter",
            "text": "Within twenty-four hours, a choking blanket of soot blocked the sun, plunging the planet into a freezing, decade-long impact winter.",
            "target_start": 42.0,
            "voice": "am_adam",
            "speed": 1.08
        },
        {
            "id": "beat_6",
            "title": "Day 1000 · The Mammalian Dawn",
            "text": "Non-avian dinosaurs died out forever. But deep underground, tiny burrowing proto-mammals survived to inherit the earth.",
            "target_start": 52.8,
            "voice": "am_adam",
            "speed": 1.08
        },
        {
            "id": "beat_7_outro",
            "title": "Epilogue Outro Resolution",
            "text": "In a single afternoon, the asteroid ended an empire. Without it, the human species would never have existed.",
            "target_start": 63.2,
            "voice": "am_adam",
            "speed": 1.08
        }
    ]

    total_duration = 70.0
    sample_rate = 24000
    timeline = np.zeros(int(total_duration * sample_rate), dtype=np.float32)

    cues = []

    print("[Kokoro Ep4] Synthesizing narrative beats...")
    for idx, beat in enumerate(beats, start=1):
        print(f"  [{idx}/7] Synthesizing: {beat['title']}...")
        samples, sr = kokoro.create(
            beat["text"],
            voice=beat["voice"],
            speed=beat["speed"],
            lang="en-us"
        )
        samples = np.array(samples, dtype=np.float32)

        beat_filename = f"ep4_beat_{idx}.wav" if idx < 7 else "ep4_beat_7_outro.wav"
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
        print(f"       Duration: {dur:.2f}s | Starts at: {start_t:.2f}s")

    # Peak normalize
    max_val = np.max(np.abs(timeline))
    if max_val > 0.95:
        timeline = timeline * (0.95 / max_val)

    # Export master voice WAV
    master_vo_wav = os.path.join(audio_dir, "vo_chicxulub.wav")
    sf.write(master_vo_wav, timeline, sample_rate)
    print(f"[Kokoro Ep4] Saved master voiceover: {master_vo_wav} (24000 Hz, 70.0s)")

    # Save audio cues JSON
    cues_path = os.path.join(audio_dir, "audio_cues_ep4.json")
    with open(cues_path, "w", encoding="utf-8") as f:
        json.dump(cues, f, indent=2)
    print(f"[Kokoro Ep4] Saved audio cues metadata: {cues_path}")

    # Convert to MP3
    master_vo_mp3 = os.path.join(audio_dir, "vo_chicxulub.mp3")
    ffmpeg_exe = r"C:\Program Files\ShareX\ffmpeg.exe"
    subprocess.run([ffmpeg_exe, "-y", "-i", master_vo_wav, "-b:a", "192k", master_vo_mp3], check=True, capture_output=True)
    print(f"[Kokoro Ep4] Converted MP3 preview: {master_vo_mp3}")

if __name__ == "__main__":
    main()
