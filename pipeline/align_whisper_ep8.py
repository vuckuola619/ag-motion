#!/usr/bin/env python3
"""align_whisper_ep8.py — Extract exact word-level timestamps using faster-whisper.
"""
import os
import json
from faster_whisper import WhisperModel

def main():
    cues_file = "assets/episode8_voynich_manuscript/audio/vo_cues_voynich.json"
    audio_dir = "assets/episode8_voynich_manuscript/audio"
    out_file = "assets/episode8_voynich_manuscript/audio/voynich_words_aligned.json"

    with open(cues_file, "r", encoding="utf-8") as f:
        cues_data = json.load(f)

    local_model_path = os.path.expanduser(r"~/.cache/huggingface/hub/models--Systran--faster-whisper-base.en/snapshots/3d3d5dee26484f91867d81cb899cfcf72b96be6c")
    print(f"[*] Loading faster-whisper from local cache: {local_model_path}")
    model = WhisperModel(local_model_path, device="cpu", compute_type="int8")

    all_beat_words = []
    global_words = []

    for beat in cues_data["beats"]:
        idx = beat["index"]
        beat_id = beat["id"]
        audio_name = beat["audio_file"]
        beat_start = beat["start"]
        audio_path = os.path.join(audio_dir, audio_name)

        print(f"[*] Transcribing beat {idx} ({audio_name})...")
        segments, info = model.transcribe(audio_path, word_timestamps=True, language="en")

        beat_words = []
        for segment in segments:
            for w in segment.words:
                cleaned = w.word.strip()
                if not cleaned:
                    continue
                w_start = round(beat_start + w.start, 3)
                w_end = round(beat_start + w.end, 3)
                item = {
                    "word": cleaned,
                    "local_start": round(w.start, 3),
                    "local_end": round(w.end, 3),
                    "global_start": w_start,
                    "global_end": w_end,
                    "beat_index": idx
                }
                beat_words.append(item)
                global_words.append(item)

        print(f"    -> Extracted {len(beat_words)} words for beat {idx}")
        all_beat_words.append({
            "beat_index": idx,
            "beat_id": beat_id,
            "start": beat_start,
            "end": beat["end"],
            "words": beat_words
        })

    result = {
        "project": "episode8_voynich_manuscript",
        "total_words": len(global_words),
        "beats": all_beat_words,
        "global_words": global_words
    }

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"[+] Saved {len(global_words)} aligned words to {out_file}")

if __name__ == "__main__":
    main()
