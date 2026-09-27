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
cues_path = os.path.join(project_dir, "assets", "episode6_project_azorian", "audio", "vo_cues_azorian_full.json")
out_dir = os.path.join(project_dir, "output", "episode6_project_azorian")
os.makedirs(out_dir, exist_ok=True)

with open(cues_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

cues = manifest["cues"]
srt_lines = []
vtt_lines = ["WEBVTT", ""]

for idx, cue in enumerate(cues, 1):
    start_s = cue["start"]
    end_s = cue["end"]
    text = cue["text"]
    
    srt_lines.append(str(idx))
    srt_lines.append(f"{format_srt_time(start_s)} --> {format_srt_time(end_s)}")
    srt_lines.append(text)
    srt_lines.append("")
    
    vtt_lines.append(str(idx))
    vtt_lines.append(f"{format_vtt_time(start_s)} --> {format_vtt_time(end_s)}")
    vtt_lines.append(text)
    vtt_lines.append("")

srt_path = os.path.join(out_dir, "azorian_subtitles.srt")
with open(srt_path, "w", encoding="utf-8") as f:
    f.write("\n".join(srt_lines))

vtt_path = os.path.join(out_dir, "azorian_subtitles.vtt")
with open(vtt_path, "w", encoding="utf-8") as f:
    f.write("\n".join(vtt_lines))

# Viral metadata (YouTube Shorts / TikTok / Reels)
meta = {
    "title": "How the CIA Secretly Stole a Soviet Nuclear Submarine from 3 Miles Deep (Project Azorian)",
    "description": (
        "In 1968, Soviet nuclear submarine K-129 vanished 16,000 feet into the Pacific Ocean. "
        "The USSR couldn't find it. But the US Navy did.\n\n"
        "What followed was Project Azorian: a $4 billion CIA operation disguised as a deep-sea mining venture "
        "by eccentric billionaire Howard Hughes using the Glomar Explorer. "
        "Discover the secret mechanics of Clementine Claw, the catastrophic hull snap at 9,000 feet, "
        "and the solemn burial at sea that birthed the legendary 'Glomar Response'.\n\n"
        "#ProjectAzorian #ColdWar #CIA #History #Submarine #GlomarExplorer #VisualJournalism #Investigation"
    ),
    "tags": [
        "Project Azorian", "CIA", "Soviet Submarine", "K-129", "Glomar Explorer",
        "Howard Hughes", "Cold War Heist", "Deep Sea Salvage", "Glomar Response",
        "Visual Journalism", "Vox Style", "History Documentary", "Shorts"
    ],
    "duration_seconds": manifest["total_duration"],
    "format": "9:16 Vertical (1080x1920)"
}

meta_path = os.path.join(out_dir, "azorian_metadata.json")
with open(meta_path, "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2)

print(f"[Subtitles Ep6] Generated:\n  -> {srt_path}\n  -> {vtt_path}\n  -> {meta_path}")
