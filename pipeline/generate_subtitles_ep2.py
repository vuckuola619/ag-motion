import json
import os

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cues_path = os.path.join(root, 'assets', 'episode2_great_dying', 'audio', 'audio_cues_ep2.json')
    out_dir = os.path.join(root, 'output', 'episode2_great_dying')
    os.makedirs(out_dir, exist_ok=True)

    with open(cues_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    def fmt_srt(sec):
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        ms = int(round((sec - int(sec)) * 1000))
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    def fmt_vtt(sec):
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        ms = int(round((sec - int(sec)) * 1000))
        return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

    srt_out = []
    vtt_out = ["WEBVTT\n"]

    for i, cue in enumerate(data['cues'], 1):
        st = fmt_srt(cue['start'])
        et = fmt_srt(cue['end'])
        text = cue['text']
        srt_out.append(f"{i}\n{st} --> {et}\n{text}\n")
        
        vst = fmt_vtt(cue['start'])
        vet = fmt_vtt(cue['end'])
        vtt_out.append(f"{i}\n{vst} --> {vet}\n{text}\n")

    srt_file = os.path.join(out_dir, "the_great_dying_subtitles.srt")
    vtt_file = os.path.join(out_dir, "the_great_dying_subtitles.vtt")

    with open(srt_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(srt_out))

    with open(vtt_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(vtt_out))

    print(f"Generated SRT: {srt_file}")
    print(f"Generated VTT: {vtt_file}")

if __name__ == '__main__':
    main()
