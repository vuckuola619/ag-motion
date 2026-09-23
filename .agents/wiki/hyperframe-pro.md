# Hyperframe Pro × Bang Motion — Unified Production Engine Reference

## 1. Overview & Architecture
Hyperframe Pro is the production-grade quality assurance, audio alignment, and surgical revision layer integrated seamlessly with Bang Motion's continuous-world explainer and kinetic canvas engine.

```
+-----------------------------------------------------------------------------------+
|                            UNIFIED PRODUCTION PIPELINE                            |
+-----------------------------------------------------------------------------------+
| 1. Narration & Audio  : Kokoro ONNX (Offline) / ElevenLabs -> audio_meta.json     |
| 2. Pause Capping      : trim-vo.py (Lossless PCM splice & timestamp re-timing)    |
| 3. Line Surgery       : swap-line.py (Offline Kokoro or ElevenLabs splice)        |
| 4. Footage Prep       : prep-footage.mjs (1080x1920 crop, light sharpen, 30fps)   |
| 5. Layout & Animation : Bang Motion continuous camera rig + Hyperframe M helpers  |
| 6. Retention Lint     : lint.mjs (Hook coverage, 0 dead air, ceiling < 179s)      |
| 7. Headless Render    : render_mp4.mjs (Puppeteer + Backpressure FFmpeg Stream)   |
| 8. Contact Sheet QA   : shots.py sheet (Contact sheet visual inspection)          |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Pipelines & CLI Scripts

### 1. Offline Voice Alignment (`pipeline/generate_voice_aligned.py`)
Generates 16-bit 44.1kHz mono WAV and word-level `audio_meta.json` 100% locally using Kokoro ONNX.
```bash
python pipeline/generate_voice_aligned.py <cues_or_script.json> <output_dir> [voice=am_adam] [speed=1.05]
```

### 2. Lossless Pause Capping (`scripts/trim-vo.py`)
Caps pauses between sentences without re-recording or pitch modification. Preserves sample-exact sync with `TA()` cues.
```bash
python hyperframe-pro/plugins/hyperframe-pro/scripts/trim-vo.py <projectDir> [capDefault=0.24] [capBeforeStep=0.42]
```

### 3. Single-Line Revision Surgery (`scripts/swap-line.py`)
Replaces one spoken sentence without throwing away approved voice takes. Supports local Kokoro ONNX (`--kokoro`) or ElevenLabs.
```bash
python hyperframe-pro/plugins/hyperframe-pro/scripts/swap-line.py <projectDir> --find "<exact phrase>" --replace "<new text>" [--kokoro] [--dry-run]
```

### 4. Cross-Platform Footage Normalizer (`scripts/prep-footage.mjs`)
Scales, crops, sharpens, and locks framerate to 30fps for video plates. Native on Windows without bash/WSL.
```bash
node hyperframe-pro/plugins/hyperframe-pro/scripts/prep-footage.mjs <in.mp4> <out.mp4> <trimStart> <duration>
```

### 5. Multi-Contract Retention Linter (`scripts/lint.mjs`)
Audits both Hyperframe generator outputs and Bang Motion canvas templates:
```bash
node hyperframe-pro/plugins/hyperframe-pro/scripts/lint.mjs <targetDir_or_htmlFile> --force
```
Enforces:
- **Duration Ceiling**: $\le 179\text{s}$ (hard Instagram ceiling).
- **Zero Dead Air**: No hero-sized vacuum $> 1.2\text{s}$.
- **Hook Guarantee**: Hero element arrives within $0.04\text{s} - 6.0\text{s}$ with dark gaps $\le 0.25\text{s}$.
- **Dispatcher Coverage**: Recognizes `fly()`, `say()`, `label()`, `slam()`, `block()`, and camera glides.
- **Dangling Target Detection**: Fails if GSAP targets missing DOM elements.

### 6. Memory-Safe Headless Renderer (`pipeline/render_mp4.mjs`)
Drives dual-contract runtimes (`window.BANG_MOTION` and `window.__timelines["main"]`) with backpressure control:
```bash
# Render specific episode with automatic pre-flight lint
node pipeline/render_mp4.mjs index_ep1.html
node pipeline/render_mp4.mjs index_ep2.html
node pipeline/render_mp4.mjs index_ep3.html
```

### 7. Screenshot & Contact Sheet QA (`scripts/shots.py`)
Samples background polarity and stitches contact sheets for human visual review:
```bash
python hyperframe-pro/plugins/hyperframe-pro/scripts/shots.py sheet <out.jpg> <snap1.jpg> <snap2.jpg> ...
```

---

## 3. Windows 11 Runtime Invariants
1. **Child Process Shell Execution**: Always pass `{ shell: true }` in Node.js when calling command-line wrappers (`ffmpeg.cmd`, `ffprobe.cmd`).
2. **Stdout Encoding**: Always invoke `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` in Python scripts to prevent `cp1252` crashes on Unicode math and arrow symbols.
3. **FFmpeg Pipe Backpressure**: Never write frame buffers without checking `!ffmpegProc.stdin.write(buffer)` and awaiting `drain`.
4. **Offline Capability**: Zero reliance on external paid APIs for local iterations.
