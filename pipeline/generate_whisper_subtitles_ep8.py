#!/usr/bin/env python3
"""generate_whisper_subtitles_ep8.py — Generate high-precision, short-phrase SRT & VTT from Whisper timestamps.
"""
import json
import os

def fmt_srt(t):
    hrs = int(t // 3600)
    mins = int((t % 3600) // 60)
    secs = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    if ms >= 1000:
        ms = 999
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{ms:03d}"

def fmt_vtt(t):
    hrs = int(t // 3600)
    mins = int((t % 3600) // 60)
    secs = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    if ms >= 1000:
        ms = 999
    return f"{hrs:02d}:{mins:02d}:{secs:02d}.{ms:03d}"

def chunk_words(words, max_words=5, max_chars=32):
    chunks = []
    cur_chunk = []
    cur_chars = 0
    
    for w in words:
        txt = w["word"]
        # Break on sentence end or chunk size
        cur_chunk.append(w)
        cur_chars += len(txt) + 1
        
        is_punc = txt.endswith(('.', '!', '?', ';', ':'))
        if len(cur_chunk) >= max_words or cur_chars >= max_chars or is_punc:
            chunks.append(cur_chunk)
            cur_chunk = []
            cur_chars = 0
            
    if cur_chunk:
        chunks.append(cur_chunk)
    return chunks

def main():
    aligned_file = "assets/episode8_voynich_manuscript/audio/voynich_words_aligned.json"
    out_dir = "output/episode8_voynich_manuscript"
    os.makedirs(out_dir, exist_ok=True)
    
    with open(aligned_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    global_words = data["global_words"]
    chunks = chunk_words(global_words, max_words=5, max_chars=32)
    
    srt_lines = []
    vtt_lines = ["WEBVTT\n"]
    
    for i, ch in enumerate(chunks, 1):
        start_t = ch[0]["global_start"]
        end_t = ch[-1]["global_end"]
        # add a tiny hold if very brief
        if end_t - start_t < 0.6:
            end_t = start_t + 0.6
        text = " ".join([w["word"] for w in ch])
        
        # SRT
        srt_lines.append(f"{i}\n{fmt_srt(start_t)} --> {fmt_srt(end_t)}\n{text}\n")
        # VTT
        vtt_lines.append(f"{i}\n{fmt_vtt(start_t)} --> {fmt_vtt(end_t)}\n{text}\n")
        
    srt_path = os.path.join(out_dir, "voynich_subtitles.srt")
    vtt_path = os.path.join(out_dir, "voynich_subtitles.vtt")
    
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))
        
    with open(vtt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(vtt_lines))
        
    print(f"[+] Exported {len(chunks)} short-phrase cues to:")
    print(f"    - {srt_path}")
    print(f"    - {vtt_path}")

if __name__ == "__main__":
    main()
