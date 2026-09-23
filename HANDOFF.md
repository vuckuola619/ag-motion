# HANDOFF: AG-Bang — Cinematic Short-Form Video Engine
**For: Codex / GPT Astra**  
**Date: 2026-09-22**  
**Previous Agent: Antigravity (Gemini)**  
**Repo: `c:\Users\bati-\Documents\AG-Bang`**  
**Git Corpus: `vuckuola619/ag-motion`**

---

## 1. WHAT THIS PROJECT IS

AG-Bang is a **code-driven cinematic short-form video factory** that produces broadcast-quality 9:16 vertical video (1080×1920 @ 30 FPS) using:

```
HTML5 + GSAP 3.12  →  Headless Puppeteer  →  FFmpeg pipe  →  MP4
```

Each episode is an educational/viral explainer in the style of **BBC Earth / Discovery Science**. The pipeline is 100% deterministic — no screen recording, frame-by-frame `seekFrame(t)` via `window.BANG_MOTION`.

---

## 2. REPOSITORY STRUCTURE (CRITICAL — READ BEFORE TOUCHING)

```
AG-Bang/
├── index.html                    # EP1: pilot "Extinction Archive" (60s, White Catalog style)
├── index_ep2.html                # EP2: Great Dying Permian-Triassic (60s)
├── index_ep3.html                # EP3: Carnian Pluvial Event (60s)
├── index_ep4.html                # EP4: Chicxulub Impact — LATEST, DONE & RENDERED ✅
├── index_indonesia_hari_ini.html # Bonus: Indonesian news segment
├── studio.html                   # Visual studio UI (style preview tool)
├── package.json                  # Node: puppeteer dependency
│
├── assets/
│   ├── episode1_dinosaurus/      # Footage: images/ audio/
│   ├── episode2_great_dying/
│   ├── episode3_carnian_pluvial/
│   ├── episode4_chicxulub/       # CURRENT — fully rendered
│   │   ├── images/               # 14 AI-generated PNGs (9router cx/gpt-5.5-image, rembg alpha)
│   │   └── audio/
│   │       ├── vo_chicxulub_cinematic.wav   # Master 70s cinematic audio mix
│   │       └── vo_chicxulub_cinematic.mp3
│   └── episode_indonesia_hari_ini/
│
├── pipeline/
│   ├── render_mp4_ep4.mjs        # Puppeteer→FFmpeg render (EP4, port 5196)
│   ├── test_snapshots_ep4.mjs    # 8-beat QC snapshot suite (port 5196)
│   ├── generate_assets_9router_ep4.py    # AI asset gen via 9router (cx/gpt-5.5-image)
│   ├── generate_voice_ep4.py     # Kokoro TTS narration (am_adam, speed 1.08)
│   ├── synthesize_audio_mix_ep4.py       # Multi-track SFX + BGM + sidechain mix
│   └── generate_subtitles_ep4.py
│
├── output/
│   ├── episode4_chicxulub/
│   │   ├── episode4_chicxulub.mp4         # MASTER OUTPUT (70.0s, 23.9 MB) ✅
│   │   ├── chicxulub_subtitles.srt
│   │   ├── chicxulub_subtitles.vtt
│   │   └── tiktok_metadata_ep4.md
│   └── [ep1–3 rendered outputs]
│
├── bang-motion-repo/             # Bang Motion skill/framework reference
└── hyperframe-pro/               # Hyperframe plugin scripts
```

### STRICT RULE — 1 Project 1 Folder
- Assets: `assets/episode{N}_{slug}/`
- Output: `output/episode{N}_{slug}/`
- NO loose files in root. NO temp PNGs in root.

---

## 3. EPISODE STATUS

| Ep | Title | Style | Duration | Status |
|---|---|---|---|---|
| **EP1** | Extinction Archive: How the Age of Dinosaurs Ended | White Catalog | 60s | ✅ Done |
| **EP2** | The Great Dying: Earth's Worst Mass Extinction | White Catalog | 60s | ✅ Done |
| **EP3** | The Carnian Pluvial Event: 2M Years of Non-Stop Rain | White Catalog | 60s | ✅ Done |
| **EP4** | The Day the Dinosaurs Died: Minute-by-Minute Chicxulub | White Catalog + Dust FX | 70s | ✅ Done |
| **EP5** | The 1-Centimeter Layer of Mud That Solved Earth's Murder Mystery | **Vox Style Visual Journalism** | 60s | ✅ **DONE & RENDERED (26.6 MB)** |

---

## 4. TECH STACK

### Render Pipeline
- **Node.js** v18+  
- **Google Chrome**: `C:\Program Files\Google\Chrome\Application\chrome.exe`  
- **FFmpeg**: `C:\Program Files\ShareX\ffmpeg.exe`
- **Puppeteer**: `^22.0.0`
- **Port convention**: EP1=5199, EP2=5194, EP3=5195, EP4=5196, **EP5=5197**

### Voice / TTS
- **Kokoro 82M ONNX** (local, offline)  
- Models: `~/.kokoro/kokoro-v0_19.onnx`, `~/.kokoro/voices.bin`  
- Voice: `am_adam`, speed `1.08`

### AI Image Generation (Asset Footage)
- **9Router**: `http://127.0.0.1:20128/v1/images/generations`  
- **Model**: `cx/gpt-5.5-image`  
- **API Key**: `Bearer sk-c4f2444795b190b3-kzvd4h-ea839762` (local router key)
- Post-process: `rembg` / alpha channel thresholding for transparent cutouts

### Python Dependencies
```bash
pip install kokoro-onnx soundfile numpy pillow scipy
```

---

## 5. HOW THE HTML ANIMATION ENGINE WORKS

Every `index_ep{N}.html` runs identically:

```javascript
// Render mode: BANG_MOTION.seekFrame(t) drives all animations deterministically
window.BANG_MOTION = { ready: true, seekFrame(t) { tl.seek(t); } }

// URL modes:
// ?clean=1   → pauses at frame 0 for headless render (no autoplay)
// ?debug=1   → shows scrub panel for manual QA
// Default    → autoplay + loop
```

**Key components inside each HTML:**
- `#runway` — horizontal 12,000px world container, camera moves via `translateX()`
- `#dustField` / `#ashField` — particle systems
- `#atmosphere` — colored overlay tint per scene phase
- `#countdownRunner` — fixed header telemetry bar
- `#motionStreak` — optical speed streak on transitions
- `gsap.timeline({paused: true})` — master GSAP timeline, seeked frame-by-frame

**Audio sync pattern:**
- Beat VO starts at `target_start` seconds
- Camera glide triggers `0.5s BEFORE` VO ends
- SFX swells in `1.5–2.5s` breathing window BETWEEN beats
- Sidechain: BGM ducks -40% during active speech

---

## 6. EPISODE 4 QA NOTES (What was fixed last session)

All 6 of user's feedback items resolved:

| Issue | Fix |
|---|---|
| Voice overlapping transitions | Rewrote script: 52.8s total / 7 beats with 1.5–2.5s buffers |
| Sprites passive/static | Ken Burns `scale 1.0→1.08` + ambient float `yoyo:true` |
| Generic SFX/BGM | Full cinematic sound bed: 35Hz blast sub-kick, fire foley, tektite glass pings, polar gale, C-major mammal dawn pad |
| Screen dots (dirty) | Replaced static `#ashField` circles with dynamic `#dustField` 24 blurred motes |
| Background grid lines | Removed `.topo-svg` + runway graph paper; clean radial vignette |
| Missing effects | Added `#shockwaveRing` (detonation ring at 10.4s) + `#motionStreak` |

---

## 7. NEXT MISSION — EPISODE 5: VOX STYLE

### Decision made by user (2026-09-21):
User wants to **switch visual style to Vox-style visual journalism** for higher CTR and impressions.

### Why Vox Style?
- **Hold Rate**: Hook drops viewer into "evidence" immediately (no logo intro)
- **Pattern Interrupt**: Visual change every 1.5–2.5s (vs 3–5s in current catalog style)
- **Shareability**: Ends on open question → triggers comments → algorithm boost
- **Loopability**: Seamless loop from outro → hook text

### Visual Anatomy of Vox Style (build this):

```
LAYER STACK (bottom to top):
1. Black background (#0B0B0C) + fine grain overlay (0.14 opacity, mix-blend: overlay)
2. Archival photo / map (Ken Burns SLOW, with dark vignette gradient)
3. Ghost watermark year (huge stroke-only typography, transparent fill)
4. Neon highlighter wipe (scaleX: 0 → 1 on yellow/red spans, synced to VO word)
5. Main headline: Barlow Condensed 800 (huge, left-aligned)
6. Hand-drawn SVG annotation (clip-path draw on dasharray path — red/yellow)
7. Source label: IBM Plex Mono (small, left border accent strip)
8. Handwritten margin note: Caveat / Permanent Marker font
9. Kinetic data counter (number rolls up fast on stats)
10. Vignetted radial overlay (edges dark)
```

### Typography System
```css
/* Fonts to load */
Barlow Condensed: wght@800   /* hero headline */
IBM Plex Mono: wght@400;500  /* data/source labels */
Caveat: wght@700             /* hand-written margin notes */

/* Color tokens */
--bg: #0B0B0C
--ink: #F5F2EA
--yel: #FFD400    /* highlighter, primary callout */
--red: #E8402F    /* warning, danger callout */
--mute: #B9B3A6   /* secondary text */
```

### Candidate Hook Topics (user was presented these options — awaiting choice):
| Option | Hook |
|---|---|
| **A (Chicxulub reframe)** | "The 1-Centimeter Layer of Mud That Solved Earth's Biggest Murder Mystery" |
| **B (Carnian reframe)** | "The 2 Million Years It Never Stopped Raining on Earth" |
| **C (Tech/Geo)** | "Why 99% of Internet Cables Run Next to Active Underwater Volcanoes" |

**User said "continue" but didn't explicitly pick A/B/C yet** — ask user to confirm topic choice before starting EP5.

### Starter to Base EP5 On:
Use `bang-motion-repo` / Bang Motion skill's `starter-explainer-jurnalisme.html` as foundation:
- Already has: Barlow Condensed, IBM Plex Mono, `.hl` highlighter wipe, `.anno` SVG drawpath, `.ghost` watermark
- Adapt to 9:16 (1080×1920 vertical) — the starter is 16:9, wrap in `.safe { transform: scale(0.78) }` or rebuild native 9:16
- Pipeline pattern: same as EP4 (generate_assets → generate_voice → synthesize_audio_mix → HTML build → test_snapshots → render_mp4)

### SFX Additions for Vox Style
Replace the orchestral cinematic bed with taktil journalism foley:
- Marker squeak / sharpie drag (when highlighter sweeps)
- Camera shutter snap (when photo changes)
- Typewriter teletype chatter (when data/code appears)  
- Paper slap / dossier thud (when document slams)
- Low sub-drone + clock tick (tension layer)

---

## 8. HOW TO RENDER A NEW EPISODE (Exact Workflow)

```bash
# Step 1: Generate footage assets
# Preferred: 9Router cx/gpt-5.5-image when 127.0.0.1:20128 is running.
# EP5 fallback used: built-in GPT Image transparent PNG generation.
python pipeline/generate_assets_9router_ep5.py

# Step 2: Generate Kokoro TTS narration
python pipeline/generate_voice_ep5.py

# Step 3: Build/update index_ep5.html (main task)

# Step 4: Run snapshot QA suite
node pipeline/test_snapshots_ep5.mjs

# Step 5: Render master MP4
node pipeline/render_mp4_ep5.mjs

# Output:
# output/episode5_{slug}/episode5_{slug}.mp4
```

---

## 9. ENVIRONMENT / GOTCHAS

| Item | Detail |
|---|---|
| Chrome path | `C:\Program Files\Google\Chrome\Application\chrome.exe` |
| FFmpeg path | `C:\Program Files\ShareX\ffmpeg.exe` |
| 9Router URL | `http://127.0.0.1:20128/v1/images/generations` (must be running locally) |
| Kokoro model | `~/.kokoro/kokoro-v0_19.onnx` + `~/.kokoro/voices.bin` |
| Port conflicts | Kill any leftover node processes before re-running render |
| `rtk` prefix | All CLI commands should be prefixed `rtk` (e.g. `rtk node ...`, `rtk python ...`) |
| Image gen | Verify generated PNGs are RGBA; GPT Image can return transparent cutouts directly. |
| Port EP5 | Use `5197` (EP1=5199, EP2=5194, EP3=5195, EP4=5196) |

### Known Pitfalls (Lessons from EP1–EP4)
1. **`.card { position: relative }` breaks runway rig** — always use `position: absolute`
2. **Static particle circles look like screen dirt** — always use GSAP-animated motes with blur
3. **VO total > 90% of duration = collision** — budget max 75% of total duration for speech
4. **Background ornaments (grid, waves) must be removed** — clean vignette only
5. **Don't add audio elements to HTML if not playing in headless render** — audio is baked into final MP4 via FFmpeg `-i audioFile` arg

---

## 10. CONTEXT HISTORY REFERENCES

Previous completed sessions covered:
- **EP1**: Pilot white-catalog style, 14 GSAP scenes, Kokoro TTS, Puppeteer render
- **EP2**: Great Dying, improved blur transitions and specimen system
- **EP3**: Carnian Pluvial, rain particle system, Wrangellia texture
- **EP4**: Chicxulub, full audio overhaul, dust particles, shockwave ring, all 6 user QA fixes resolved, **RENDERED ✅**
- **Style discussion**: User approved pivot to Vox visual journalism style for EP5+

---

## 11. EP5 FINAL HANDOVER

- Topic: **The world is not collapsing. It is being squeezed.**
- Final master: `output/episode5_polycrisis/episode5_polycrisis.mp4`
- Voice: English, local Kokoro ONNX `am_adam`; available runtime is **Kokoro 82M**, not 82B.
- On-screen copy: English; decorative SVG line overlays are disabled and typography carries the visual emphasis.
- Six EP5 sprites are transparent `RGBA` PNGs under `assets/episode5_polycrisis/images/`.
- 9Router generator remains the canonical reproducible path when port `20128` is available; the delivered EP5 sprites were generated through the permitted GPT Image fallback because 9Router was offline.

Good luck. The engine is solid — focus on nailing the Vox visual design language.
