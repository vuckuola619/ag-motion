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
AUDIO_DIR = os.path.join(PROJECT_ROOT, "assets", "episode10_mother_microchimerism", "audio_en")
os.makedirs(AUDIO_DIR, exist_ok=True)

VOICE = "en-US-ChristopherNeural"
RATE = "+0%"
PITCH = "+0Hz"

BEATS = [
    {
        "index": 1,
        "id": "hook_invisible_passenger",
        "act": 1,
        "title": "The Invisible Passenger",
        "text": "When you left your mother's womb, you didn't leave her empty. Decades after birth, your cells are still alive... inside her heart and brain."
    },
    {
        "index": 2,
        "id": "act1_cardiac_repair",
        "act": 2,
        "title": "Maternal Heart Regeneration",
        "text": "In 2011, researchers at Mount Sinai discovered something extraordinary: when a pregnant mother suffers heart injury, fetal stem cells travel across the placenta, transforming directly into beating cardiomyocytes to repair her heart tissue."
    },
    {
        "index": 3,
        "id": "act2_brain_longevity",
        "act": 3,
        "title": "The 94-Year Legacy",
        "text": "And it doesn't stop there. In 2012, the Fred Hutchinson Center discovered male fetal DNA inside the brains of women up to age ninety-four. For nearly a century, children leave an indelible biological mark in their mother's memory centers."
    },
    {
        "index": 4,
        "id": "act3_prophetic_hadith",
        "act": 4,
        "title": "Prophetic Covenant: 3 to 1 Priority",
        "text": "Fourteen centuries ago, a man asked Prophet Muhammad ﷺ: 'Who deserves my finest companionship?' The Prophet answered: 'Your mother.' The man asked: 'Then who?' 'Your mother.' 'Then who?' 'Your mother.' Only on the fourth time did he say: 'Your father.'"
    },
    {
        "index": 5,
        "id": "outro_presence",
        "act": 5,
        "title": "Stitched Together Forever",
        "text": "You are not just a chapter in her life. Biologically, genetically, and spiritually... you are stitched into her living organs forever. Call your mother today."
    }
]

async def synthesize_beats():
    print(f"--- Synthesizing {len(BEATS)} English Voiceover Beats via Edge TTS ({VOICE}) ---")
    beat_files = []
    for beat in BEATS:
        out_file = os.path.join(AUDIO_DIR, f"vo_ep10_beat_{beat['index']}_{beat['id']}.mp3")
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

    master_mp3 = os.path.join(AUDIO_DIR, "vo_ep10_en_master.mp3")
    master_wav = os.path.join(AUDIO_DIR, "vo_ep10_en_master.wav")

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
        "title": "Episode 10 (English Edition): The Mother's Microchimerism // Cellular Epigenetics",
        "language": "en",
        "voice": VOICE,
        "total_duration": round(total_dur, 2),
        "beats": BEATS,
        "words": words
    }

    out_json = os.path.join(AUDIO_DIR, "ep10_en_words_aligned.json")
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
