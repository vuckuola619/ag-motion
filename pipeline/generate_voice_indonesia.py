import os
import sys
import json
import re
import asyncio
import edge_tts
import subprocess
import wave

SCRIPT_TEXT = (
    "Indonesia hari ini berada di persimpangan paling menentukan dalam sejarahnya. "
    "Puncak bonus demografi sedang berlangsung, dan jendela waktu kita tinggal dua belas tahun. "
    "Hilirisasi mineral meledak luar biasa. "
    "Indonesia kini menguasai lebih dari lima puluh persen pasokan nikel dunia, menjadi jangkar utama ekosistem baterai global. "
    "Namun di balik angka makro yang megah, sembilan koma empat juta kelas menengah justru tergerus turun kelas. "
    "Tekanan daya beli menjadi alarm nyata. "
    "Di sisi lain, penetrasi internet menembus delapan puluh persen. "
    "Talenta muda memutar ekonomi digital senilai seribu empat ratus triliun rupiah. "
    "Sejarah membuktikan, hanya lima belas persen negara berkembang yang berhasil lolos jadi negara maju. "
    "Target kita harus melompati tiga belas ribu dolar per kapita. "
    "Kuncinya ada pada manufaktur bernilai tambah tinggi, riset sains nyata, dan integritas kepemimpinan sebelum gerbang emas demografi tertutup selamanya. "
    "Indonesia emas bukan hadiah yang ditunggu, melainkan masa depan yang harus kita rebut hari ini."
)

def split_words_proportional(text, start_t, end_t, start_idx=0):
    raw_tokens = [w for w in text.split() if w.strip()]
    if not raw_tokens:
        return []
    
    weights = []
    for w in raw_tokens:
        clean = re.sub(r'[^a-zA-Z0-9]', '', w)
        wt = len(clean) or 1
        if w.endswith((',', ';')): wt += 1.4
        elif w.endswith(('.', '!', '?')): wt += 2.2
        weights.append(wt)
    
    total_wt = sum(weights) or 1
    total_dur = end_t - start_t
    
    words = []
    cur_t = start_t
    for i, (w, wt) in enumerate(zip(raw_tokens, weights)):
        span = (wt / total_wt) * total_dur
        w_start = round(cur_t, 3)
        w_end = round(cur_t + span * 0.90, 3)
        words.append({
            "id": f"w{start_idx + len(words)}",
            "text": w,
            "start": w_start,
            "end": w_end
        })
        cur_t += span
    return words

async def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "assets/episode_indonesia_hari_ini/audio"
    voice = sys.argv[2] if len(sys.argv) > 2 else "id-ID-ArdiNeural"
    os.makedirs(out_dir, exist_ok=True)
    
    mp3_path = os.path.join(out_dir, "vo.mp3")
    wav_path = os.path.join(out_dir, "vo.wav")
    meta_path = os.path.join(out_dir, "audio_meta.json")
    
    print(f"[TTS] Synthesizing Indonesian narration with {voice} (+6% rate)...")
    communicate = edge_tts.Communicate(SCRIPT_TEXT, voice, rate="+6%", pitch="+0Hz")
    
    sentences = []
    with open(mp3_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "SentenceBoundary":
                st = chunk["offset"] / 10000000.0
                dur = chunk["duration"] / 10000000.0
                sentences.append({
                    "text": chunk["text"],
                    "start": st,
                    "end": st + dur,
                    "duration": dur
                })
                
    print(f"[TTS] Sentences detected: {len(sentences)}")
    
    # Normalize to 16-bit 44.1kHz mono WAV with -16 LUFS
    sharex_ffmpeg = r"C:\Program Files\ShareX\ffmpeg.exe"
    ffmpeg_cmd = sharex_ffmpeg if os.path.exists(sharex_ffmpeg) else "ffmpeg"
    
    subprocess.run([
        ffmpeg_cmd, "-v", "error", "-y",
        "-i", mp3_path,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=9:linear=true",
        "-ar", "44100",
        "-ac", "1",
        wav_path
    ], check=True, shell=(ffmpeg_cmd == "ffmpeg"))
    
    with wave.open(wav_path, "rb") as w:
        actual_dur = round(w.getnframes() / float(w.getframerate()), 3)
    
    print(f"[TTS] Final WAV Duration: {actual_dur}s")
    
    # Generate word timestamps
    all_words = []
    for s in sentences:
        words = split_words_proportional(s["text"], s["start"], s["end"], start_idx=len(all_words))
        all_words.extend(words)
        
    meta = {
        "voiceId": voice,
        "modelId": "edge-tts",
        "language": "id",
        "scenes": [
            {
                "id": "indonesia_hari_ini",
                "text": SCRIPT_TEXT,
                "wav": "vo.wav",
                "duration": actual_dur,
                "speechStart": all_words[0]["start"] if all_words else 0.0,
                "speechEnd": all_words[-1]["end"] if all_words else actual_dur,
                "words": all_words
            }
        ]
    }
    
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
        
    print(f"[TTS] audio_meta.json written with {len(all_words)} words.")

if __name__ == "__main__":
    asyncio.run(main())
