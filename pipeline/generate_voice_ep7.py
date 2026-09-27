import os
import json
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    audio_dir = os.path.join(project_dir, "assets", "episode7_wow_signal", "audio")
    os.makedirs(audio_dir, exist_ok=True)

    model_dir = os.path.join(os.path.expanduser("~"), ".kokoro")
    onnx_path = os.path.join(model_dir, "kokoro-v0_19.onnx")
    voices_path = os.path.join(model_dir, "voices.bin")

    print(f"[Kokoro Ep7] Loading model from {onnx_path}...")
    kokoro = Kokoro(onnx_path, voices_path)

    # 12 detailed narrative beats across 5 Acts + Outro
    # Natural, unhurried pacing with micro-pauses (1.2s - 1.5s) for tactical camera moves & documents
    beats_script = [
        # ACT 1: The Listening Ear
        {
            "id": "act1_beat1",
            "act": 1,
            "title": "Act 1 · The Listening Ear",
            "text": "On the night of August 15, 1977, deep in the Ohio countryside, a football-field-sized radio telescope known as Big Ear was silently listening to the cosmos.",
            "voice": "am_adam",
            "speed": 1.04,
            "post_pause": 1.3
        },
        {
            "id": "act1_beat2",
            "act": 1,
            "title": "Act 1 · Project SETI",
            "text": "Humanity had just launched Project SETI: searching fifty channels simultaneously for a deliberate artificial broadcast from an alien civilization.",
            "voice": "am_adam",
            "speed": 1.04,
            "post_pause": 1.4
        },
        # ACT 2: The 72-Second Window
        {
            "id": "act2_beat1",
            "act": 2,
            "title": "Act 2 · Earth's Rotation Window",
            "text": "Big Ear was completely immobile. It had no steering motors, relying entirely on the Earth's rotation to sweep across the starry sky.",
            "voice": "am_adam",
            "speed": 1.04,
            "post_pause": 1.2
        },
        {
            "id": "act2_beat2",
            "act": 2,
            "title": "Act 2 · The 72-Second Bell Curve",
            "text": "Because of its beam width, any genuine point source from deep space could only be heard for exactly seventy-two seconds, rising and falling in a textbook bell curve.",
            "voice": "am_adam",
            "speed": 1.04,
            "post_pause": 1.5
        },
        # ACT 3: Decoding 6EQUJ5
        {
            "id": "act3_beat1",
            "act": 3,
            "title": "Act 3 · The Mainframe Printout",
            "text": "A few days later, astronomer Jerry Ehman arrived to review stacks of tractor-feed paper from the IBM 1130 mainframe.",
            "voice": "am_adam",
            "speed": 1.04,
            "post_pause": 1.2
        },
        {
            "id": "act3_beat2",
            "act": 3,
            "title": "Act 3 · The 6EQUJ5 Surge",
            "text": "Amidst the random background noise of ones and twos, channel two suddenly spiked into letters: six, E, Q, U, J, five. A signal thirty times stronger than deep space background radiation.",
            "voice": "am_adam",
            "speed": 1.03,
            "post_pause": 1.3
        },
        {
            "id": "act3_beat3",
            "act": 3,
            "title": "Act 3 · The Hydrogen Line",
            "text": "Even more astonishing, it was broadcasting at 1420.405 megahertz: the exact emission frequency of neutral hydrogen, the cosmic waterhole where alien civilizations would theoretically transmit.",
            "voice": "am_adam",
            "speed": 1.04,
            "post_pause": 1.5
        },
        # ACT 4: The Failed Explanations
        {
            "id": "act4_beat1",
            "act": 4,
            "title": "Act 4 · The Red Pen & The 'Wow!'",
            "text": "Stunned, Jerry grabbed a red Pilot pen, circled the six characters, and scribbled a single word in the margin: Wow!",
            "voice": "am_adam",
            "speed": 1.03,
            "post_pause": 1.3
        },
        {
            "id": "act4_beat2",
            "act": 4,
            "title": "Act 4 · Failed Hypotheses",
            "text": "For nearly half a century, astronomers tested every terrestrial explanation: classified military satellites, aircraft reflections, passing comets. Every single hypothesis failed.",
            "voice": "am_adam",
            "speed": 1.04,
            "post_pause": 1.5
        },
        # ACT 5: The Silent Void
        {
            "id": "act5_beat1",
            "act": 5,
            "title": "Act 5 · The Silent Void",
            "text": "The Very Large Array and Green Bank telescopes returned to those exact coordinates near Chi Sagittarii over a hundred times. The patch of sky was dead silent.",
            "voice": "am_adam",
            "speed": 1.04,
            "post_pause": 1.3
        },
        {
            "id": "act5_beat2",
            "act": 5,
            "title": "Act 5 · Cosmic Whisper",
            "text": "A solitary seventy-two-second transmission, broadcast across thousands of light-years, never to be heard again.",
            "voice": "am_adam",
            "speed": 1.03,
            "post_pause": 1.2
        },
        # OUTRO: Investigation Unsolved
        {
            "id": "outro_beat",
            "act": 6,
            "title": "Outro · Investigation Unsolved",
            "text": "The greatest unsolved mystery in the history of deep space astronomy. The Wow! Signal.",
            "voice": "am_adam",
            "speed": 1.03,
            "post_pause": 2.5
        }
    ]

    sample_rate = 24000
    current_time = 1.0  # 1.0s opening micro-pause for ambient cosmic radio static
    cues = []
    generated_audio_clips = []

    print("[Kokoro Ep7] Generating 12 unhurried narrative beats...")
    for idx, beat in enumerate(beats_script, start=1):
        samples, sr = kokoro.create(
            beat["text"],
            voice=beat["voice"],
            speed=beat["speed"],
            lang="en-us"
        )
        samples = np.array(samples, dtype=np.float32)
        dur = len(samples) / sr

        clip_name = f"wow_signal_beat_{idx}.wav"
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
        print(f"  [{idx}/12] Act {beat['act']} - {beat['title']}: {round(dur, 2)}s (starts at {start_t}s)")
        current_time = end_t + beat["post_pause"]

    total_duration = round(current_time + 1.0, 2)
    print(f"\n[Kokoro Ep7] Total Narrative Timeline Duration: {total_duration}s (~{round(total_duration/60, 2)} min)")

    timeline = np.zeros(int(total_duration * sample_rate) + sample_rate, dtype=np.float32)
    for start_t, samples in generated_audio_clips:
        s_idx = int(start_t * sample_rate)
        e_idx = s_idx + len(samples)
        timeline[s_idx:e_idx] += samples

    narration_path = os.path.join(audio_dir, "vo_wow_signal_narration.wav")
    sf.write(narration_path, timeline, sample_rate)
    print(f"[Kokoro Ep7] Full narration timeline saved: {narration_path}")

    cues_path = os.path.join(audio_dir, "vo_cues_wow_signal.json")
    with open(cues_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_duration": total_duration,
            "sample_rate": sample_rate,
            "cues": cues
        }, f, indent=2)
    print(f"[Kokoro Ep7] Cue manifest saved: {cues_path}")

if __name__ == "__main__":
    main()
