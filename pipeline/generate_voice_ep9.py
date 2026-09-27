#!/usr/bin/env python3
"""generate_voice_ep9.py — Generate master VO and word-level timestamps for Episode 9 using Edge-TTS.
"""
import os
import sys
import json
import asyncio
import subprocess
import edge_tts

BEATS = [
    {
        "id": "hook",
        "act": 1,
        "title": "Kekeliruan Peran Ayah",
        "text": "Banyak pria mengira tugas ayah selesai saat nafkah finansial ditransfer ke rekening. Neurosains modern dan tradisi peradaban membuktikan: ini kekeliruan fatal.",
        "pause": 1.2
    },
    {
        "id": "act1_neurobiology",
        "act": 2,
        "title": "Perubahan Biologis Otak Ayah",
        "text": "Studi neurobiologi Yale University mengungkap, ketika seorang ayah aktif mengasuh, memandikan, dan menidurkan anak, otak pria mengalami lonjakan hormon oksitosin yang setara ibu pasca melahirkan. Sirkuit empati prefrontal cortex aktif seketika.",
        "pause": 1.3
    },
    {
        "id": "act2_psychology",
        "act": 3,
        "title": "Rough-and-Tumble Play & Regulasi Emosi",
        "text": "Bermain fisik teratur dengan ayah, seperti bergulat ringan dan meluncur, bukan sekadar canda tawa. Ini melatih kendali impuls emosi. Anak yang dekat dengan ayahnya memiliki ketahanan stres empat puluh persen lebih stabil.",
        "pause": 1.3
    },
    {
        "id": "act3_islamic_adab",
        "act": 4,
        "title": "Adab & Keteladanan Nabawi",
        "text": "Empat belas abad silam, Rasulullah shallallahu alaihi wasallam mencontohkan ini secara nyata. Beliau menggendong cucunya saat shalat berjamaah, dan menegur pria yang membanggakan diri tak pernah mencium anaknya. Dalam Islam, ayah adalah Ar-Rai, pemimpin jiwa dan pelindung emosional.",
        "pause": 1.4
    },
    {
        "id": "outro_verdict",
        "act": 5,
        "title": "Pesan Abadi Sang Ayah",
        "text": "Anak tidak akan mengingat berapa digit saldo tabunganmu. Yang mereka rekam seumur hidup adalah kehadiranmu dan kehangatan tanganmu saat mereka merasa takut.",
        "pause": 1.5
    }
]

VOICE = "id-ID-ArdiNeural"
RATE = "-3%"
PITCH = "-1Hz"

async def generate_beat(beat, index, out_dir):
    text = beat["text"]
    mp3_filename = f"vo_ep9_beat_{index+1}_{beat['id']}.mp3"
    mp3_path = os.path.join(out_dir, mp3_filename)

    communicate = edge_tts.Communicate(text, voice=VOICE, rate=RATE, pitch=PITCH)
    
    words_data = []
    
    with open(mp3_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                words_data.append({
                    "word": chunk["text"],
                    "audio_offset_ms": chunk["offset"] / 10000.0, # 100ns units -> ms
                    "duration_ms": chunk["duration"] / 10000.0
                })

    # Get exact audio duration via ffprobe or ffmpeg
    ffprobe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", mp3_path
    ]
    try:
        res = subprocess.run(ffprobe_cmd, capture_output=True, text=True, check=True)
        dur = float(res.stdout.strip())
    except Exception:
        # Fallback to ShareX ffmpeg/ffprobe if ffprobe not on standard path
        sharex_ffprobe = r"C:\Program Files\ShareX\ffmpeg.exe"
        cmd = [sharex_ffprobe, "-i", mp3_path]
        res = subprocess.run(cmd, capture_output=True, text=True)
        # Parse Duration: 00:00:12.34
        import re
        m = re.search(r"Duration:\s*(\d+):(\d+):([\d\.]+)", res.stderr)
        if m:
            dur = int(m.group(1))*3600 + int(m.group(2))*60 + float(m.group(3))
        else:
            dur = 10.0

    return {
        "beat_index": index + 1,
        "id": beat["id"],
        "act": beat["act"],
        "title": beat["title"],
        "text": text,
        "audio_file": mp3_filename,
        "duration": dur,
        "post_pause": beat["pause"],
        "raw_words": words_data
    }

async def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    audio_dir = os.path.join(project_dir, "assets", "episode9_father_parenting", "audio")
    os.makedirs(audio_dir, exist_ok=True)

    print(f"[*] Generating voice beats for Episode 9 with {VOICE}...")
    beat_results = []
    for i, beat in enumerate(BEATS):
        print(f"    -> Beat {i+1}/{len(BEATS)}: {beat['title']}")
        res = await generate_beat(beat, i, audio_dir)
        beat_results.append(res)

    # Compute global timeline & concatenate into master audio
    concat_list_path = os.path.join(audio_dir, "concat_list.txt")
    master_mp3 = os.path.join(audio_dir, "vo_ep9_master.mp3")
    master_wav = os.path.join(audio_dir, "vo_ep9_master.wav")

    # Generate silence file for pauses
    silence_1s = os.path.join(audio_dir, "silence_1s.mp3")
    ffmpeg_exe = r"C:\Program Files\ShareX\ffmpeg.exe"
    subprocess.run([
        ffmpeg_exe, "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
        "-t", "1.0", "-q:a", "9", silence_1s
    ], capture_output=True, check=True)

    current_t = 0.0
    global_words = []
    beats_meta = []

    with open(concat_list_path, "w", encoding="utf-8") as concat_f:
        for i, b in enumerate(beat_results):
            b_start = round(current_t, 3)
            b_dur = b["duration"]
            b_end = round(b_start + b_dur, 3)

            # Write to concat
            concat_f.write(f"file '{b['audio_file']}'\n")

            # Word timestamps
            # Convert raw_words into global timestamps
            if b["raw_words"]:
                for w in b["raw_words"]:
                    w_start = round(b_start + (w["audio_offset_ms"] / 1000.0), 3)
                    w_end = round(w_start + (w["duration_ms"] / 1000.0), 3)
                    global_words.append({
                        "word": w["word"],
                        "start": w_start,
                        "end": w_end,
                        "beat": b["beat_index"]
                    })
            else:
                # Proportional fallback
                tokens = b["text"].split()
                step = b_dur / max(len(tokens), 1)
                for j, tok in enumerate(tokens):
                    w_start = round(b_start + j * step, 3)
                    w_end = round(w_start + step * 0.88, 3)
                    global_words.append({
                        "word": tok,
                        "start": w_start,
                        "end": w_end,
                        "beat": b["beat_index"]
                    })

            beats_meta.append({
                "index": b["beat_index"],
                "id": b["id"],
                "act": b["act"],
                "title": b["title"],
                "text": b["text"],
                "start": b_start,
                "end": b_end,
                "duration": b_dur,
                "audio_file": b["audio_file"]
            })

            # Add pause
            pause_sec = b["post_pause"]
            current_t = b_end + pause_sec
            if i < len(beat_results) - 1:
                pause_file = f"pause_{i+1}.mp3"
                pause_path = os.path.join(audio_dir, pause_file)
                subprocess.run([
                    ffmpeg_exe, "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                    "-t", str(pause_sec), "-q:a", "9", pause_path
                ], capture_output=True, check=True)
                concat_f.write(f"file '{pause_file}'\n")

    total_duration = round(current_t, 3)
    print(f"[*] Total master audio duration: {total_duration}s")

    # Concatenate to master mp3 and wav
    print("[*] Concatenating master audio...")
    subprocess.run([
        ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path,
        "-c", "copy", master_mp3
    ], capture_output=True, check=True)

    subprocess.run([
        ffmpeg_exe, "-y", "-i", master_mp3, "-ac", "1", "-ar", "24000", master_wav
    ], capture_output=True, check=True)

    # Save aligned json
    aligned_data = {
        "title": "Episode 9: The Father's Brain // Ar-Ra'i",
        "language": "id",
        "voice": VOICE,
        "total_duration": total_duration,
        "beats": beats_meta,
        "words": global_words
    }

    out_json = os.path.join(audio_dir, "ep9_words_aligned.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(aligned_data, f, ensure_ascii=False, indent=2)

    print(f"[OK] Master audio and aligned words saved successfully ({len(global_words)} words).")

if __name__ == "__main__":
    asyncio.run(main())
