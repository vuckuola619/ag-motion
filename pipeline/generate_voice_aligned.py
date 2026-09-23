#!/usr/bin/env python3
"""generate_voice_aligned.py — Kokoro ONNX offline TTS with word-level audio_meta.json export.

Bridges local offline TTS with Hyperframe Pro's word-locked cue engine (TA() chaining).
Runs 100% locally on Windows without requiring an ElevenLabs API key.

Usage:
    python pipeline/generate_voice_aligned.py <script_or_cues.json> <output_dir> [voice=am_adam] [speed=1.05]
"""
import os
import sys
import json
import re
import numpy as np
import soundfile as sf
import subprocess

def split_words_proportional(text, start_t, end_t):
    """Derive proportional word-level timestamps from synthesized speech span."""
    raw_tokens = [w for w in text.split() if w.strip()]
    if not raw_tokens:
        return []
    
    # Weight by token character length + trailing punctuation pause
    weights = []
    for w in raw_tokens:
        wt = len(re.sub(r'[^a-zA-Z0-9]', '', w)) or 1
        if w.endswith((',', ';')): wt += 1.5
        elif w.endswith(('.', '!', '?')): wt += 2.5
        weights.append(wt)
    
    total_wt = sum(weights)
    total_dur = end_t - start_t
    
    words = []
    cur_t = start_t
    for i, (w, wt) in enumerate(zip(raw_tokens, weights)):
        span = (wt / total_wt) * total_dur
        w_start = round(cur_t, 3)
        w_end = round(cur_t + span * 0.88, 3) # leave slight inter-word air
        words.append({
            "id": f"w{len(words)}",
            "text": w,
            "start": w_start,
            "end": w_end
        })
        cur_t += span
    return words

def main():
    if len(sys.argv) < 3:
        print("usage: python generate_voice_aligned.py <cues_or_script.json> <output_dir> [voice=am_adam] [speed=1.05]")
        sys.exit(1)
        
    input_file = sys.argv[1]
    out_dir = sys.argv[2]
    voice = sys.argv[3] if len(sys.argv) > 3 else "am_adam"
    speed = float(sys.argv[4]) if len(sys.argv) > 4 else 1.05

    os.makedirs(out_dir, exist_ok=True)
    
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    beats = data.get("cues") or data.get("beats") or data.get("scenes") or []
    if not beats and "text" in data:
        beats = [{"id": "vo", "title": "Main VO", "text": data["text"], "target_start": 0.5}]
        
    from kokoro_onnx import Kokoro
    model_dir = os.path.join(os.path.expanduser("~"), ".kokoro")
    onnx_path = os.path.join(model_dir, "kokoro-v0_19.onnx")
    voices_path = os.path.join(model_dir, "voices.bin")
    
    print(f"[Kokoro Aligner] Initializing model from {onnx_path}...")
    kokoro = Kokoro(onnx_path, voices_path)
    
    target_sr = 44100
    all_words = []
    audio_segments = []
    
    cur_time = 0.45
    full_text_list = []
    
    for i, b in enumerate(beats):
        txt = b.get("text", "")
        full_text_list.append(txt)
        b_id = b.get("id", f"beat_{i+1}")
        b_speed = b.get("speed", speed)
        b_voice = b.get("voice", voice)
        
        print(f"  -> Synthesizing {b_id} ({len(txt.split())} words)...")
        samples, sr = kokoro.create(txt, voice=b_voice, speed=b_speed)
        
        # Resample to 44.1k mono if needed
        dur = len(samples) / float(sr)
        start_t = b.get("target_start", cur_time)
        end_t = start_t + dur
        
        words = split_words_proportional(txt, start_t, end_t)
        all_words.extend(words)
        
        audio_segments.append((start_t, samples, sr))
        cur_time = end_t + 0.35

    # Composite master buffer at 44.1kHz
    max_time = max(s[0] + len(s[1])/s[2] for s in audio_segments) + 1.2
    total_samples = int(max_time * target_sr)
    master_buf = np.zeros(total_samples, dtype=np.float32)
    
    for start_t, samp, sr in audio_segments:
        # Simple linear resample to 44.1k
        if sr != target_sr:
            idx_old = np.linspace(0, len(samp) - 1, int(len(samp) * target_sr / sr))
            samp_44k = np.interp(idx_old, np.arange(len(samp)), samp).astype(np.float32)
        else:
            samp_44k = samp
            
        start_idx = int(start_t * target_sr)
        end_idx = min(start_idx + len(samp_44k), total_samples)
        sl_len = end_idx - start_idx
        master_buf[start_idx:end_idx] += samp_44k[:sl_len]
        
    # Peak normalize
    mx = np.max(np.abs(master_buf))
    if mx > 0:
        master_buf = (master_buf / mx) * 0.89
        
    wav_out = os.path.join(out_dir, "vo.wav")
    sf.write(wav_out, master_buf, target_sr, subtype='PCM_16')
    print(f"[Kokoro Aligner] Master 16-bit 44.1kHz WAV saved: {wav_out} ({max_time:.2f}s)")
    
    # Export audio_meta.json in Hyperframe Pro standard schema
    meta = {
        "voiceId": f"kokoro_{voice}",
        "modelId": "kokoro-v0_19_local",
        "sampleRate": target_sr,
        "scenes": [
            {
                "id": "vo",
                "text": " ".join(full_text_list),
                "wav": "vo.wav",
                "duration": round(max_time, 3),
                "speechStart": all_words[0]["start"] if all_words else 0.5,
                "speechEnd": all_words[-1]["end"] if all_words else max_time,
                "words": all_words
            }
        ]
    }
    
    meta_path = os.path.join(out_dir, "audio_meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print(f"[Kokoro Aligner] Hyperframe Pro compatible audio_meta.json saved: {meta_path} ({len(all_words)} words)")

if __name__ == "__main__":
    main()
