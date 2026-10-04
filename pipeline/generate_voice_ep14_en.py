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
AUDIO_DIR = os.path.join(PROJECT_ROOT, "assets", "episode14_glymphatic_brain_wash", "audio_en")
os.makedirs(AUDIO_DIR, exist_ok=True)

VOICE = "en-US-ChristopherNeural"
RATE = "+0%"
PITCH = "+0Hz"

BEATS = [
    {
        "index": 1,
        "id": "hook_nocturnal_secret",
        "act": 1,
        "title": "The Nocturnal Secret",
        "text": "Every single night, while you are unconscious, your brain performs an astonishing act of physical hygiene. It physically contracts by sixty percent... and washes itself with pressurized spinal fluid."
    },
    {
        "index": 2,
        "id": "act1_astrocytic_highway",
        "act": 2,
        "title": "The Astrocytic Highway",
        "text": "In 2013, neuroscientist Maiken Nedergaard discovered the Glymphatic System. During waking hours, your brain is too busy processing reality to clean house. But the moment you enter deep slow-wave sleep, specialized star-shaped astrocytes open microscopic floodgates."
    },
    {
        "index": 3,
        "id": "act2_alzheimer_flush",
        "act": 3,
        "title": "The Alzheimer's Flush",
        "text": "A tidal wave of cerebrospinal fluid surges through your cerebral tissue, vacuuming away toxic metabolic debris — specifically Beta-Amyloid and Tau proteins. Skipping deep sleep doesn't just make you tired; it leaves toxic waste baked into your synapses."
    },
    {
        "index": 4,
        "id": "act3_sleep_debt_myth",
        "act": 4,
        "title": "The Sleep Debt Myth",
        "text": "You cannot simply 'catch up' on sleep over the weekend. Glymphatic cleansing requires consistent, synchronized Slow-Wave Delta sleep, which only occurs in your initial nocturnal cycles. Chronic deprivation is biological self-sabotage."
    },
    {
        "index": 5,
        "id": "outro_clean_temple",
        "act": 5,
        "title": "The Protocol & Temple",
        "text": "Sleep is not a passive pause button. It is the most advanced neurological detox protocol on Earth. Protect your eight hours. Let your brain clean its temple."
    }
]

async def synthesize_beats():
    print(f"--- Synthesizing {len(BEATS)} English Voiceover Beats via Edge TTS ({VOICE}) ---")
    beat_files = []
    for beat in BEATS:
        out_file = os.path.join(AUDIO_DIR, f"vo_ep14_beat_{beat['index']}_{beat['id']}.mp3")
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

        lines.append(f"file '{beat_path.replace(os.sep, '/')}'")
        current_time += dur

        # Add pause between beats (1.4s for deep dramatic breath)
        if i < len(BEATS) - 1:
            pause_file = os.path.join(AUDIO_DIR, f"pause_{i+1}.mp3")
            pause_cmd = [
                FFMPEG_EXE, "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
                "-t", "1.4", "-q:a", "9", "-acodec", "libmp3lame", pause_file
            ]
            subprocess.run(pause_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            lines.append(f"file '{pause_file.replace(os.sep, '/')}'")
            current_time += 1.4

    with open(concat_list, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    master_mp3 = os.path.join(AUDIO_DIR, "vo_ep14_en_master.mp3")
    master_wav = os.path.join(AUDIO_DIR, "vo_ep14_en_master.wav")

    cmd_concat = [
        FFMPEG_EXE, "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list, "-c", "copy", master_mp3
    ]
    subprocess.run(cmd_concat, check=True)

    # Convert to uncompressed WAV for sample-accurate browser sync
    cmd_wav = [
        FFMPEG_EXE, "-y", "-i", master_mp3,
        "-ar", "44100", "-ac", "2", master_wav
    ]
    subprocess.run(cmd_wav, check=True)

    master_dur = get_audio_duration(master_wav)
    print(f"[Master] Master audio rendered: {master_dur:.2f} seconds ({master_wav})")
    return master_dur

def align_audio_whisper(master_wav, master_dur):
    print("\n--- Running Faster-Whisper Word-Level Alignment ---")
    model_path = os.path.expanduser("~/.cache/huggingface/hub/models--Systran--faster-whisper-base.en/snapshots/3d3d5dee26484f91867d81cb899cfcf72b96be6c")
    if os.path.exists(model_path):
        model = WhisperModel(model_path, device="cpu", compute_type="int8")
    else:
        model = WhisperModel("base.en", device="cpu", compute_type="int8", local_files_only=True)
    segments, info = model.transcribe(master_wav, word_timestamps=True, language="en")

    words_aligned = []
    for segment in segments:
        for word in segment.words:
            words_aligned.append({
                "word": word.word.strip(),
                "start": round(word.start, 2),
                "end": round(word.end, 2),
                "probability": round(word.probability, 2)
            })

    output_json = os.path.join(AUDIO_DIR, "ep14_en_words_aligned.json")
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump({
            "total_duration": master_dur,
            "beats": BEATS,
            "words": words_aligned
        }, f, indent=2)

    print(f"[Whisper] Aligned {len(words_aligned)} words -> {output_json}")

async def main():
    await synthesize_beats()
    master_dur = build_master_audio()
    master_wav = os.path.join(AUDIO_DIR, "vo_ep14_en_master.wav")
    align_audio_whisper(master_wav, master_dur)

if __name__ == "__main__":
    asyncio.run(main())
