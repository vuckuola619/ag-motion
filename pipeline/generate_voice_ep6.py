import os
import json
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    audio_dir = os.path.join(project_dir, "assets", "episode6_project_azorian", "audio")
    os.makedirs(audio_dir, exist_ok=True)

    model_dir = os.path.join(os.path.expanduser("~"), ".kokoro")
    onnx_path = os.path.join(model_dir, "kokoro-v0_19.onnx")
    voices_path = os.path.join(model_dir, "voices.bin")

    print(f"[Kokoro Ep6] Loading model from {onnx_path}...")
    kokoro = Kokoro(onnx_path, voices_path)

    # 6 Vox-style Investigation Narration Beats strictly budgeted for 60.0s timeline
    beats = [
        {
            "id": "beat_1",
            "title": "Scene 1 · The Vanished Submarine",
            "text": "In March 1968, Soviet nuclear sub K-129 vanished in the Pacific. Moscow found nothing. But the US Navy pinpointed the wreck: three miles deep.",
            "target_start": 1.5,
            "voice": "am_adam",
            "speed": 1.18
        },
        {
            "id": "beat_2",
            "title": "Scene 2 · The Billionaire Cover Story",
            "text": "To recover it, the CIA hatched the most audacious heist in Cold War history. Their cover story: billionaire Howard Hughes was mining deep-sea manganese.",
            "target_start": 12.4,
            "voice": "am_adam",
            "speed": 1.15
        },
        {
            "id": "beat_3",
            "title": "Scene 3 · The Mechanical Monster",
            "text": "Beneath Hughes' ship hung Clementine: a massive mechanical claw lowered on three miles of steel pipe string. In pitch-black abyss, its talons locked onto the submarine.",
            "target_start": 23.4,
            "voice": "am_adam",
            "speed": 1.15
        },
        {
            "id": "beat_4",
            "title": "Scene 4 · The Snap & Radiation",
            "text": "Nine thousand feet up, disaster struck. The claw fractured. Two-thirds of the nuclear submarine snapped off and plunged back into the deep, contaminating the deck.",
            "target_start": 34.4,
            "voice": "am_adam",
            "speed": 1.15
        },
        {
            "id": "beat_5",
            "title": "Scene 5 · The Secret Burial at Sea",
            "text": "Inside the recovered bow lay six Soviet submariners. In complete secrecy, the crew gave them an honorable burial at sea, playing the Soviet national anthem.",
            "target_start": 45.4,
            "voice": "am_adam",
            "speed": 1.15
        },
        {
            "id": "beat_6",
            "title": "Scene 6 · Case Solved Outro",
            "text": "A half-billion-dollar operation. The deepest secret heist in human history.",
            "target_start": 55.0,
            "voice": "am_adam",
            "speed": 1.18
        }
    ]

    total_duration = 60.0
    sample_rate = 24000
    timeline = np.zeros(int(total_duration * sample_rate), dtype=np.float32)

    cues = []

    print("[Kokoro Ep6] Synthesizing calibrated narrative beats...")
    for idx, beat in enumerate(beats, start=1):
        samples, sr = kokoro.create(
            beat["text"],
            voice=beat["voice"],
            speed=beat["speed"],
            lang="en-us"
        )
        samples = np.array(samples, dtype=np.float32)

        beat_filename = f"ep6_beat_{idx}.wav"
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
            "start": start_t,
            "duration": round(dur, 2),
            "end": round(start_t + dur, 2),
            "text": beat["text"]
        })
        print(f"  [{idx}/6] {beat['title']}: {round(dur, 2)}s | Window: {start_t}s -> {round(start_t+dur, 2)}s")

    narration_path = os.path.join(audio_dir, "vo_azorian_narration_only.wav")
    sf.write(narration_path, timeline, sample_rate)
    print(f"\n[Kokoro Ep6] Clean narration timeline saved: {narration_path}")

    cues_path = os.path.join(audio_dir, "vo_cues_ep6.json")
    with open(cues_path, "w", encoding="utf-8") as f:
        json.dump(cues, f, indent=2)
    print(f"[Kokoro Ep6] Cue manifest saved: {cues_path}")

if __name__ == "__main__":
    main()
