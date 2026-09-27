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

    # 10 detailed narrative beats across 5 Acts + Outro
    # Natural, unhurried pacing with micro-pauses for tactical camera moves & documents
    beats_script = [
        # ACT 1: The Ghost in the Pacific
        {
            "id": "act1_beat1",
            "act": 1,
            "title": "Act 1 · The Ghost in the Pacific",
            "text": "In March 1968, Soviet ballistic missile submarine K-129 vanished into the North Pacific, carrying eighty-three crewmen and three nuclear warheads.",
            "voice": "am_adam",
            "speed": 1.05,
            "post_pause": 1.2
        },
        {
            "id": "act1_beat2",
            "act": 1,
            "title": "Act 1 · SOSUS Acoustic Detection",
            "text": "Moscow launched a desperate two-month search across millions of square miles, finding nothing. But America's secret underwater hydrophone network, SOSUS, detected the catastrophic acoustic blast. The wreck lay sixteen thousand feet deep.",
            "voice": "am_adam",
            "speed": 1.05,
            "post_pause": 1.4
        },
        # ACT 2: The $4 Billion Cover Story
        {
            "id": "act2_beat1",
            "act": 2,
            "title": "Act 2 · The Audacious Heist",
            "text": "Three miles beneath the surface, salvage was deemed scientifically impossible. Yet the CIA launched Project Azorian: a top-secret four-billion-dollar operation to steal the submarine from the abyss.",
            "voice": "am_adam",
            "speed": 1.05,
            "post_pause": 1.2
        },
        {
            "id": "act2_beat2",
            "act": 2,
            "title": "Act 2 · Howard Hughes Cover Story",
            "text": "To hide the mission in plain sight, the CIA recruited eccentric billionaire Howard Hughes. Hughes claimed his massive new vessel, the Glomar Explorer, was merely mining commercial manganese nodules from the ocean floor.",
            "voice": "am_adam",
            "speed": 1.05,
            "post_pause": 1.4
        },
        # ACT 3: The Impossible Machine
        {
            "id": "act3_beat1",
            "act": 3,
            "title": "Act 3 · Clementine Claw Anatomy",
            "text": "In reality, hidden inside the ship's flooded moon pool was an engineering marvel: Clementine. A colossal fifty-meter hydraulic claw with heavy steel capture tines.",
            "voice": "am_adam",
            "speed": 1.05,
            "post_pause": 1.2
        },
        {
            "id": "act3_beat2",
            "act": 3,
            "title": "Act 3 · Descent into the Abyss",
            "text": "Lowered joint by joint through three miles of heavy pipe string, the mechanical monster descended into the pitch-black abyss. Guided by deep-sea sonars, the claw locked onto the broken submarine.",
            "voice": "am_adam",
            "speed": 1.05,
            "post_pause": 1.5
        },
        # ACT 4: The Catastrophic Break
        {
            "id": "act4_beat1",
            "act": 4,
            "title": "Act 4 · The Lift & Mechanical Fracture",
            "text": "The lift began. For days, giant winches hauled the six-thousand-ton prize upward. Then, at nine thousand feet, disaster struck.",
            "voice": "am_adam",
            "speed": 1.03,
            "post_pause": 1.0
        },
        {
            "id": "act4_beat2",
            "act": 4,
            "title": "Act 4 · Collapse & Radiation Alarms",
            "text": "Under brutal hydrostatic stress, the steel claw fractured. Two-thirds of the submarine snapped away and plunged back into the abyss. Only the forward bow section was pulled into the moon pool, triggering immediate radiation alarms.",
            "voice": "am_adam",
            "speed": 1.05,
            "post_pause": 1.5
        },
        # ACT 5: The Secret Funeral & Leaks
        {
            "id": "act5_beat1",
            "act": 5,
            "title": "Act 5 · Solemn Burial at Sea",
            "text": "Inside the recovered bow lay two nuclear torpedoes and the remains of six Soviet submariners. In complete secrecy, the CIA gave the fallen sailors a full military burial at sea, playing the Soviet national anthem as their coffins entered the deep.",
            "voice": "am_adam",
            "speed": 1.05,
            "post_pause": 1.4
        },
        {
            "id": "act5_beat2",
            "act": 5,
            "title": "Act 5 · The Leak & Glomar Response",
            "text": "When investigative reporter Jack Anderson leaked the story in 1975, the CIA created history's most famous official statement: We can neither confirm nor deny.",
            "voice": "am_adam",
            "speed": 1.05,
            "post_pause": 1.2
        },
        # OUTRO: Top Secret Solved
        {
            "id": "outro_beat",
            "act": 6,
            "title": "Outro · Case Declassified",
            "text": "The deepest covert operation in human history. Project Azorian.",
            "voice": "am_adam",
            "speed": 1.03,
            "post_pause": 2.5
        }
    ]

    sample_rate = 24000
    current_time = 1.0  # 1.0s opening micro-pause for ambient hydrophone drone
    cues = []
    generated_audio_clips = []

    print("[Kokoro Ep6] Generating 11 unhurried narrative beats...")
    for idx, beat in enumerate(beats_script, start=1):
        samples, sr = kokoro.create(
            beat["text"],
            voice=beat["voice"],
            speed=beat["speed"],
            lang="en-us"
        )
        samples = np.array(samples, dtype=np.float32)
        dur = len(samples) / sr

        clip_name = f"azorian_beat_{idx}.wav"
        clip_path = os.path.join(audio_dir, clip_name)
        sf.write(clip_path, samples, sr)

        start_t = round(current_time, 2)
        end_t = round(start_t + dur, 2)
        cues.append({
            "beat_id": beat["id"],
            "act": beat["act"],
            "title": beat["title"],
            "start": start_t,
            "duration": round(dur, 2),
            "end": end_t,
            "text": beat["text"],
            "filename": clip_name
        })

        generated_audio_clips.append((start_t, samples))
        print(f"  [{idx}/11] Act {beat['act']} - {beat['title']}: {round(dur, 2)}s (starts at {start_t}s)")
        current_time = end_t + beat["post_pause"]

    total_duration = round(current_time + 1.0, 2)
    print(f"\n[Kokoro Ep6] Total Narrative Timeline Duration: {total_duration}s (~{round(total_duration/60, 2)} min)")

    timeline = np.zeros(int(total_duration * sample_rate) + sample_rate, dtype=np.float32)
    for start_t, samples in generated_audio_clips:
        s_idx = int(start_t * sample_rate)
        e_idx = s_idx + len(samples)
        timeline[s_idx:e_idx] += samples

    narration_path = os.path.join(audio_dir, "vo_azorian_full_narration.wav")
    sf.write(narration_path, timeline, sample_rate)
    print(f"[Kokoro Ep6] Full narration timeline saved: {narration_path}")

    cues_path = os.path.join(audio_dir, "vo_cues_azorian_full.json")
    with open(cues_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_duration": total_duration,
            "sample_rate": sample_rate,
            "cues": cues
        }, f, indent=2)
    print(f"[Kokoro Ep6] Cue manifest saved: {cues_path}")

if __name__ == "__main__":
    main()
