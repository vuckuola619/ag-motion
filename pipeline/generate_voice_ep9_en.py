import asyncio
import os
import json
import subprocess
import ssl
import edge_tts
from faster_whisper import WhisperModel

# Bypass local SSL inspection/proxy issues
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE
edge_tts.communicate._SSL_CTX = ssl_ctx

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(PROJECT_ROOT, "assets", "episode9_father_parenting", "audio_en")
os.makedirs(AUDIO_DIR, exist_ok=True)

VOICE = "en-US-ChristopherNeural"
RATE = "+0%"
PITCH = "+0Hz"

BEATS = [
    {
        "index": 1,
        "id": "hook_atm_myth",
        "act": 1,
        "title": "The Financial ATM Fallacy",
        "text": "Many men believe fatherhood ends when money hits the bank account. But developmental neuroscience and ancient wisdom prove: that's a dangerous illusion. Kids don't need a human ATM—they need an active dad."
    },
    {
        "index": 2,
        "id": "act1_neurobiology",
        "act": 2,
        "title": "The Paternal Brain",
        "text": "Yale University discovered something mind-blowing: when fathers actively bathe, carry, and put their kids to sleep, their brains physically rewire. Oxytocin surges by over one hundred and forty percent—matching new mothers! Empathy circuits ignite instantly."
    },
    {
        "index": 3,
        "id": "act2_rough_play",
        "act": 3,
        "title": "Rough Play & Stress Resilience",
        "text": "Ever wrestled on the carpet or tossed your toddler in the air? Science calls this 'Rough-and-Tumble Play'. Harvard research proves it hardwires emotional regulation and impulse control, boosting childhood stress resilience by forty percent!"
    },
    {
        "index": 4,
        "id": "act3_sunnah_adab",
        "act": 4,
        "title": "Prophetic Mercy & Ar-Ra'i",
        "text": "Fourteen centuries ago, Prophet Muhammad ﷺ shattered toxic emotional distance. When a chieftain boasted he never kissed his ten children, the Prophet warned: 'Whoever does not show mercy, will not be shown mercy.' In Islam, a father is Ar-Ra'i: a shepherd of hearts and souls."
    },
    {
        "index": 5,
        "id": "outro_presence",
        "act": 5,
        "title": "The Lifetime Record",
        "text": "Decades from now, your child won't remember your overtime bank statements. What their nervous system forever records is the warm hand that held them when they were scared. Show up. Be truly present."
    }
]

async def synthesize_beats():
    print(f"--- Synthesizing {len(BEATS)} English Voiceover Beats via Edge TTS ({VOICE}) ---")
    beat_files = []
    for beat in BEATS:
        out_file = os.path.join(AUDIO_DIR, f"vo_ep9_beat_{beat['index']}_{beat['id']}.mp3")
        print(f"[TTS] Synthesizing Beat {beat['index']}: {beat['title']}...")
        communicate = edge_tts.Communicate(beat["text"], VOICE, rate=RATE, pitch=PITCH)
        await communicate.save(out_file)
        beat["audio_file"] = os.path.basename(out_file)
        beat_files.append(out_file)
    return beat_files

FFMPEG_EXE = r"C:\Program Files\ShareX\ffmpeg.exe"

def get_audio_duration(file_path):
    cmd = [
        FFMPEG_EXE, "-i", file_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    import re
    m = re.search(r"Duration: (\d+):(\d+):([\d\.]+)", res.stderr)
    if m:
        h, m_val, s = m.groups()
        return int(h)*3600 + int(m_val)*60 + float(s)
    return 0.0

def build_master_audio():
    print("\n--- Assembling English Master Audio with Natural Breathing Pauses ---")
    concat_list = os.path.join(AUDIO_DIR, "concat_list.txt")
    silence_file = os.path.join(AUDIO_DIR, "silence_0.9s.mp3")

    # Generate 0.9s silence
    subprocess.run([
        FFMPEG_EXE, "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
        "-t", "0.9", "-q:a", "9", silence_file
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    lines = []
    current_time = 0.0

    for i, beat in enumerate(BEATS):
        beat_path = os.path.join(AUDIO_DIR, beat["audio_file"])
        dur = get_audio_duration(beat_path)
        beat["start"] = round(current_time, 2)
        beat["end"] = round(current_time + dur, 2)
        beat["duration"] = round(dur, 2)

        lines.append(f"file '{beat['audio_file']}'")
        current_time += dur

        if i < len(BEATS) - 1:
            pause_name = f"pause_{i+1}.mp3"
            pause_path = os.path.join(AUDIO_DIR, pause_name)
            subprocess.run([
                FFMPEG_EXE, "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                "-t", "0.95", "-q:a", "9", pause_path
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            lines.append(f"file '{pause_name}'")
            current_time += 0.95

    with open(concat_list, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    master_mp3 = os.path.join(AUDIO_DIR, "vo_ep9_en_master.mp3")
    master_wav = os.path.join(AUDIO_DIR, "vo_ep9_en_master.wav")

    subprocess.run([
        FFMPEG_EXE, "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list, "-c", "copy", master_mp3
    ], check=True)

    subprocess.run([
        FFMPEG_EXE, "-y", "-i", master_mp3,
        "-ar", "44100", "-ac", "2", master_wav
    ], check=True)

    total_dur = get_audio_duration(master_wav)
    print(f"[OK] Master audio built: {master_wav} ({total_dur:.2f} seconds)")
    return master_wav, total_dur

def align_words_whisper(master_wav, total_dur):
    print("\n--- Running Faster-Whisper Word-Level Alignment (en) ---")
    model_dir = r"C:\Users\bati-\.cache\huggingface\hub\models--Systran--faster-whisper-base.en\snapshots\3d3d5dee26484f91867d81cb899cfcf72b96be6c"
    model = WhisperModel(model_dir, device="cpu", compute_type="int8")
    segments, info = model.transcribe(master_wav, language="en", word_timestamps=True)

    words = []
    for segment in segments:
        for w in segment.words:
            word_clean = w.word.strip()
            if word_clean:
                # Find which beat this word belongs to
                assigned_beat = 1
                for beat in BEATS:
                    if w.start >= beat["start"] - 0.3:
                        assigned_beat = beat["index"]

                words.append({
                    "word": word_clean,
                    "start": round(w.start, 2),
                    "end": round(w.end, 2),
                    "beat": assigned_beat
                })

    aligned_data = {
        "title": "Episode 9 (English Edition): The Father's Brain // Ar-Ra'i",
        "language": "en",
        "voice": VOICE,
        "total_duration": round(total_dur, 2),
        "beats": BEATS,
        "words": words
    }

    out_json = os.path.join(AUDIO_DIR, "ep9_en_words_aligned.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(aligned_data, f, indent=2, ensure_ascii=False)

    print(f"[OK] Saved {len(words)} aligned words to {out_json}")
    return aligned_data

async def main_async():
    await synthesize_beats()
    master_wav, total_dur = build_master_audio()
    align_words_whisper(master_wav, total_dur)

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
