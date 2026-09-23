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
cues_path = os.path.join(project_dir, "assets", "episode5_iridium_layer", "audio", "audio_cues_ep5.json")
out_dir = os.path.join(project_dir, "output", "episode5_iridium_layer")
os.makedirs(out_dir, exist_ok=True)

with open(cues_path, "r", encoding="utf-8") as f:
    cues = json.load(f)

srt_lines = []
vtt_lines = ["WEBVTT", ""]

for idx, cue in enumerate(cues, 1):
    start_s = cue["start"]
    end_s = min(cue["end"], 60.0)
    text = cue["text"]
    
    srt_lines.append(str(idx))
    srt_lines.append(f"{format_srt_time(start_s)} --> {format_srt_time(end_s)}")
    srt_lines.append(text)
    srt_lines.append("")
    
    vtt_lines.append(str(idx))
    vtt_lines.append(f"{format_vtt_time(start_s)} --> {format_vtt_time(end_s)}")
    vtt_lines.append(text)
    vtt_lines.append("")

srt_path = os.path.join(out_dir, "iridium_layer_subtitles.srt")
with open(srt_path, "w", encoding="utf-8") as f:
    f.write("\n".join(srt_lines))

vtt_path = os.path.join(out_dir, "iridium_layer_subtitles.vtt")
with open(vtt_path, "w", encoding="utf-8") as f:
    f.write("\n".join(vtt_lines))

print(f"Generated {srt_path} and {vtt_path}")
