import os
import json

def format_srt_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

def format_vtt_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hrs:02d}:{mins:02d}:{secs:02d}.{millis:03d}"

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cues_path = os.path.join(project_dir, "assets", "episode8_voynich_manuscript", "audio", "vo_cues_voynich.json")
out_dir = os.path.join(project_dir, "output", "episode8_voynich_manuscript")
os.makedirs(out_dir, exist_ok=True)

with open(cues_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

beats = manifest["beats"]
srt_lines = []
vtt_lines = ["WEBVTT", ""]

for idx, beat in enumerate(beats, 1):
    start_s = beat["start"]
    end_s = beat["end"]
    text = beat["text"]
    
    srt_lines.append(str(idx))
    srt_lines.append(f"{format_srt_time(start_s)} --> {format_srt_time(end_s)}")
    srt_lines.append(text)
    srt_lines.append("")
    
    vtt_lines.append(str(idx))
    vtt_lines.append(f"{format_vtt_time(start_s)} --> {format_vtt_time(end_s)}")
    vtt_lines.append(text)
    vtt_lines.append("")

srt_path = os.path.join(out_dir, "voynich_subtitles.srt")
with open(srt_path, "w", encoding="utf-8") as f:
    f.write("\n".join(srt_lines))

vtt_path = os.path.join(out_dir, "voynich_subtitles.vtt")
with open(vtt_path, "w", encoding="utf-8") as f:
    f.write("\n".join(vtt_lines))

# TikTok & YouTube Shorts Markdown Metadata
tiktok_md = f"""# TikTok & YouTube Shorts Metadata: The Voynich Manuscript

**Title:** The 600-Year-Old Code That Even Modern AI Can't Crack (The Voynich Manuscript)  
**Format:** 9:16 Vertical (1080x1920)  
**Duration:** ~{int(manifest['total_duration'])}s ({round(manifest['total_duration']/60, 1)} min)  
**Pacing:** Vox Visual Journalism (unhurried forensic investigation)  

## Copy & Description:
In 1912, inside a secluded Jesuit college in Italy, an antique book dealer uncovered a 240-page parchment codex written in an alphabet found nowhere else in human history.

Its pages are filled with bizarre botanical drawings of plants that don't exist on Earth, rotating astrological wheels, and naked figures in labyrinthine plumbing systems.

For a century, skeptics called it an elaborate hoax. But in 2009, University of Arizona physicists radiocarbon-dated the vellum to between 1404 and 1438 AD. It is genuinely 600 years old.

Even stranger: mathematical linguists discovered the text strictly obeys Zipf's Law and exhibits the exact information entropy of real human speech. It has grammar, prefixes, and suffixes. It is not random gibberish.

Yet, after 30 years of attempts by WW2 cryptanalyst William Friedman, the National Security Agency, supercomputers, and modern neural network AIs... not a single sentence has ever been deciphered.

Is it a lost language? An unbreakable cipher? Or the ultimate intellectual puzzle left behind by history?

## Tags & Hashtags:
#VoynichManuscript #UnsolvedMystery #Cryptography #HistoryMysteries #AncientCode #MedievalHistory #ArtificialIntelligence #BeineckeLibrary #Science #VisualJournalism #Shorts #TikTokEdu
"""

tiktok_path = os.path.join(out_dir, "tiktok_metadata_ep8.md")
with open(tiktok_path, "w", encoding="utf-8") as f:
    f.write(tiktok_md)

print(f"[Subtitles Ep8] Generated:\n  -> {srt_path}\n  -> {vtt_path}\n  -> {tiktok_path}")
