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
cues_path = os.path.join(project_dir, "assets", "episode7_wow_signal", "audio", "vo_cues_wow_signal.json")
out_dir = os.path.join(project_dir, "output", "episode7_wow_signal")
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

srt_path = os.path.join(out_dir, "wow_signal_subtitles.srt")
with open(srt_path, "w", encoding="utf-8") as f:
    f.write("\n".join(srt_lines))

vtt_path = os.path.join(out_dir, "wow_signal_subtitles.vtt")
with open(vtt_path, "w", encoding="utf-8") as f:
    f.write("\n".join(vtt_lines))

# TikTok Markdown Metadata
tiktok_md = f"""# TikTok & YouTube Shorts Metadata: The Wow! Signal

**Title:** The 72-Second Deep Space Transmission That Science Still Can't Explain (The Wow! Signal)  
**Format:** 9:16 Vertical (1080x1920)  
**Duration:** ~{int(manifest['total_duration'])}s ({round(manifest['total_duration']/60, 1)} min)  
**Pacing:** Vox Visual Journalism (unhurried forensic inquiry)  

## Copy & Description:
On August 15, 1977, Ohio State University's "Big Ear" radio telescope was scanning the cosmos for signs of extraterrestrial technology. 

Because Big Ear had no steering motors and relied on Earth's rotation, any true interstellar signal could only pass through its beam for exactly 72 seconds in a textbook bell curve.

Days later, astronomer Jerry Ehman examined the IBM 1130 dot-matrix printout. Amidst the random ones and twos of cosmic background noise, channel 2 exploded into '6EQUJ5' — an intensity 30 times background at 1420.405 MHz (the neutral hydrogen line, the quietest frequency in the universe).

Jerry circled it with a red pen and wrote "Wow!". For nearly 50 years, every terrestrial explanation — satellites, radar, comets — has been tested and ruled out. When humanity pointed our greatest radio telescopes back to Chi Sagittarii, the sky was completely silent.

Was it a passing interstellar beacon? An alien radar beam? Or something science has yet to comprehend?

## Tags & Hashtags:
#TheWowSignal #WowSignal #Astronomy #SpaceMystery #SETI #Aliens #BigEar #Science #SpaceExploration #VisualJournalism #Cosmology #DeepSpace #Shorts
"""

tiktok_path = os.path.join(out_dir, "tiktok_metadata_ep7.md")
with open(tiktok_path, "w", encoding="utf-8") as f:
    f.write(tiktok_md)

print(f"[Subtitles Ep7] Generated:\n  -> {srt_path}\n  -> {vtt_path}\n  -> {tiktok_path}")
