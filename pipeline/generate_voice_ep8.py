import os
import json
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    audio_dir = os.path.join(project_dir, "assets", "episode8_voynich_manuscript", "audio")
    os.makedirs(audio_dir, exist_ok=True)

    model_dir = os.path.join(os.path.expanduser("~"), ".kokoro")
    onnx_path = os.path.join(model_dir, "kokoro-v0_19.onnx")
    voices_path = os.path.join(model_dir, "voices.bin")

    print(f"[Kokoro Ep8] Loading model from {onnx_path}...")
    kokoro = Kokoro(onnx_path, voices_path)

    # 12 detailed narrative beats across 5 Acts + Outro
    # Natural, unhurried pacing with micro-pauses (1.2s - 1.5s) for tactical camera moves & documents
    beats_script = [
        # PROLOGUE & ACT 1: The Discovery
        {
            "id": "act1_beat1",
            "act": 1,
            "title": "Act 1 · The Monastery Discovery",
            "text": "In 1912, deep inside a secluded Jesuit college near Rome, an antique book dealer named Wilfrid Voynich uncovered an enigmatic manuscript bound in aged goat vellum.",
            "voice": "am_adam",
            "speed": 1.04,
            "post_pause": 1.3
        },
        {
            "id": "act1_beat2",
            "act": 1,
            "title": "Act 1 · The Unknown Script",
            "text": "Inside were two hundred and forty illustrated pages, written in an elegant, unbroken script that no scholar, historian, or linguist on Earth had ever seen.",
            "voice": "am_adam",
            "speed": 1.04,
            "post_pause": 1.4
        },
        # ACT 2: Alien Botany & Cosmological Wheels
        {
            "id": "act2_beat1",
            "act": 2,
            "title": "Act 2 · Impossible Botany",
            "text": "Every folio was covered in hand-painted drawings of bizarre plants: impossible botanical hybrids with roots shaped like claws and leaves with unnatural vascular systems. Not a single plant exists in nature.",
            "voice": "am_adam",
            "speed": 1.04,
            "post_pause": 1.3
        },
        {
            "id": "act2_beat2",
            "act": 2,
            "title": "Act 2 · Cosmological Wheels",
            "text": "Other fold-outs revealed cosmological star wheels, unknown zodiac constellations, and miniature figures floating through intricate labyrinths of organic plumbing tubes.",
            "voice": "am_adam",
            "speed": 1.04,
            "post_pause": 1.5
        },
        # ACT 3: The Carbon Dating Verdict
        {
            "id": "act3_beat1",
            "act": 3,
            "title": "Act 3 · The Hoax Accusation",
            "text": "For nearly a century, skeptics insisted the entire manuscript was an elaborate Renaissance hoax, forged by alchemists to swindle wealthy emperors out of gold.",
            "voice": "am_adam",
            "speed": 1.04,
            "post_pause": 1.3
        },
        {
            "id": "act3_beat2",
            "act": 3,
            "title": "Act 3 · The Arizona Carbon Test",
            "text": "Until 2009. Physicists at the University of Arizona extracted four micro-samples of the calfskin parchment for accelerator mass spectrometry radiocarbon dating.",
            "voice": "am_adam",
            "speed": 1.04,
            "post_pause": 1.3
        },
        {
            "id": "act3_beat3",
            "act": 3,
            "title": "Act 3 · 600 Years Old",
            "text": "The scientific verdict was indisputable: the vellum was prepared between 1404 and 1438. The Voynich Manuscript is genuinely six hundred years old.",
            "voice": "am_adam",
            "speed": 1.04,
            "post_pause": 1.5
        },
        # ACT 4: The Mathematical Trap
        {
            "id": "act4_beat1",
            "act": 4,
            "title": "Act 4 · Zipf's Law Proof",
            "text": "If it was a hoax, its author was centuries ahead of modern science. Statistical analysis proved the text strictly obeys Zipf's Law, matching the exact mathematical frequency distribution of genuine spoken languages.",
            "voice": "am_adam",
            "speed": 1.04,
            "post_pause": 1.3
        },
        {
            "id": "act4_beat2",
            "act": 4,
            "title": "Act 4 · Linguistic Architecture",
            "text": "The words follow strict grammatical rules, complete with prefixes, roots, and suffixes. Mathematically, it is virtually impossible for these 170,000 glyphs to be random medieval gibberish.",
            "voice": "am_adam",
            "speed": 1.04,
            "post_pause": 1.5
        },
        # ACT 5: The Graveyard of Codebreakers
        {
            "id": "act5_beat1",
            "act": 5,
            "title": "Act 5 · The Cryptanalyst Defeat",
            "text": "During World War Two, William Friedman, the legendary cryptanalyst who broke Japan's PURPLE cipher, dedicated thirty years trying to decipher the book. He died without decoding a single word.",
            "voice": "am_adam",
            "speed": 1.04,
            "post_pause": 1.3
        },
        {
            "id": "act5_beat2",
            "act": 5,
            "title": "Act 5 · Supercomputers and AI",
            "text": "Decades later, the National Security Agency, quantum computing clusters, and modern neural network language models were unleashed on the text. Every single model collapsed into statistical contradictions.",
            "voice": "am_adam",
            "speed": 1.04,
            "post_pause": 1.5
        },
        # OUTRO: The Vault of Yale
        {
            "id": "outro_beat1",
            "act": 6,
            "title": "Outro · The Silent Vault",
            "text": "Today, cataloged as MS 408, it rests locked inside the climate-controlled vault of Yale University's Beinecke Library. Six centuries of human intelligence, and the Voynich cipher remains completely unbroken.",
            "voice": "am_adam",
            "speed": 1.04,
            "post_pause": 2.0
        }
    ]

    master_audio = []
    cues_data = {
        "project": "episode8_voynich_manuscript",
        "title": "The 600-Year-Old Code That Even Modern AI Can't Crack (The Voynich Manuscript)",
        "sample_rate": 24000,
        "total_duration": 0.0,
        "beats": []
    }

    current_time = 0.0

    print(f"\n[Kokoro Ep8] Synthesizing {len(beats_script)} narrative beats...")
    for idx, beat in enumerate(beats_script, 1):
        beat_id = beat["id"]
        text = beat["text"]
        voice = beat["voice"]
        speed = beat["speed"]
        post_pause = beat["post_pause"]

        print(f"  -> Beat {idx:02d}/{len(beats_script):02d} [{beat_id}]: '{text[:45]}...'")

        # Generate audio using Kokoro
        samples, sample_rate = kokoro.create(
            text=text,
            voice=voice,
            speed=speed,
            lang="en-us"
        )

        beat_duration = len(samples) / sample_rate
        beat_wav_name = f"voynich_beat_{idx}.wav"
        beat_wav_path = os.path.join(audio_dir, beat_wav_name)
        sf.write(beat_wav_path, samples, sample_rate)

        start_time = current_time
        end_time = start_time + beat_duration

        cues_data["beats"].append({
            "index": idx,
            "id": beat_id,
            "act": beat["act"],
            "title": beat["title"],
            "text": text,
            "start": round(start_time, 3),
            "end": round(end_time, 3),
            "duration": round(beat_duration, 3),
            "audio_file": beat_wav_name
        })

        master_audio.append(samples)
        current_time = end_time

        # Add pause silence
        pause_samples = int(post_pause * sample_rate)
        if pause_samples > 0:
            silence = np.zeros(pause_samples, dtype=np.float32)
            master_audio.append(silence)
            current_time += post_pause

    # Concatenate master VO
    full_audio = np.concatenate(master_audio)
    total_duration = len(full_audio) / 24000.0
    cues_data["total_duration"] = round(total_duration, 3)

    master_vo_path = os.path.join(audio_dir, "vo_voynich_narration.wav")
    sf.write(master_vo_path, full_audio, 24000)

    cues_path = os.path.join(audio_dir, "vo_cues_voynich.json")
    with open(cues_path, "w", encoding="utf-8") as f:
        json.dump(cues_data, f, indent=2, ensure_ascii=False)

    print(f"\n[Kokoro Ep8] Narration generated successfully!")
    print(f"  -> Master VO: {master_vo_path} ({total_duration:.2f}s)")
    print(f"  -> Cues file: {cues_path}")

if __name__ == "__main__":
    main()
