# AG-Motion: Cinematic Web Motion Graphics Engine

> **Style 3: White Catalog Explainer — "The Extinction of Dinosaurs" (60.00s English Master Edition)**  
> Built strictly adhering to the [Bang Motion](https://github.com/bangtutorial/bang-motion) methodology and anti-slop visual discipline.

---

## 🎬 Project Overview

AG-Motion is an open-source, code-driven motion graphics explainer engine that renders professional, broadcast-quality vertical video (1080×1920 @ 30fps) directly from web standards (HTML5, CSS3, GSAP) into lossless MP4 via headless Chrome and FFmpeg pipes.

This repository features the complete 60-second pilot explainer: **"Extinction Archive: How the Age of Dinosaurs Ended"**.

---

## ✨ Key Architectural Features

1. **Horizontal Continuous Runway**:
   - Spans 12,000+ pixels horizontally across 6 distinct geological and astrophysical dossiers.
   - Smooth, organic camera glides (`glideTransition`) with directional motion blur sweeps (`blurTween`), eliminating jarring slide cuts.

2. **Strict Anti-Slop Visual Hierarchy**:
   - Zero abstract vector wireframes or floating circular lines; all scientific artifacts use authentic photorealistic photography and transparent background specimen cutouts.
   - Distinct 8-layer vertical typographic hierarchy:
     - Header Series Tag (`#stag1`–`#stag6`)
     - Ghost Chrono Watermark (`#ghost1`–`#ghost6`)
     - Taxonomy Classification (`#name1`–`#name6`)
     - Hero Visual Specimen (`#cutTrex`, `#cardAsteroidEntry`, etc.)
     - Specimen Telemetry Tag (`#tag1`–`#tag6`)
     - High-Contrast Stamp Badge (`#sb1`–`#sb6`) & Editorial Annotation (`#hand1`–`#hand6`)
     - Kinetic Narrative Headline (`#line1`–`#line6`)
     - Forensic Evidence Dossier Card (`#doc1`–`#doc6`)
     - Telemetry Metric Bar & Barcode Verification Footer (`#gauge1`, `#footer1`)

3. **Frame-Accurate Audio/Visual Synchronization**:
   - 60.00-second English voiceover powered by Kokoro 82M TTS (`vo_dinosaurus.wav`).
   - Every word entrance, card fly-in, and rubber stamp strike is locked to millisecond audio cues.

4. **Deterministic Headless Puppeteer Render Pipeline**:
   - Instead of real-time screen capture, frames are driven deterministically through `window.BANG_MOTION.seekFrame(time)`.
   - 1,800 uncompressed frames piped directly into `ffmpeg` via stdin (`libx264`, `yuv420p`, `crf 18`, `faststart`).

5. **Adobe After Effects Bridge**:
   - `build_after_effects.jsx`: Automatically reconstructs the exact 6-beat camera rig, solids, audio layer, images, and text cards directly inside Adobe After Effects.

---

## 🗂 Timeline & Story Beats

| Beat | Timestamp | Xc | Dossier Theme | Hero Visual Artifact |
|:---:|:---:|:---:|:---|:---|
| **01** | `00.0s – 10.0s` | `540px` | Late Cretaceous Apex Biomass | Authentic T-Rex Skull & Sauropod Fossil |
| **02** | `10.0s – 20.0s` | `2540px` | Chicxulub Impactor Trajectory | Hypersonic Atmospheric Entry & Carbonaceous Chondrite |
| **03** | `20.0s – 30.0s` | `4540px` | Ground Zero & Megatsunami | 1,000-Foot Tsunami Wall & Chicxulub Satellite Bathymetry |
| **04** | `30.0s – 40.0s` | `6540px` | Deccan Traps Supervolcanoes | Continental Flood Basalts & Global Firestorm Sky |
| **05** | `40.0s – 50.0s` | `8540px` | Nuclear Winter & Biosphere Collapse | Sun Blackout Soot Cloud & Disaster Fern Spore Fossil |
| **06** | `50.0s – 60.0s` | `10540px` | K-Pg Iridium Boundary & Rise of Mammals | Alvarez Iridium Clay Core Specimen & Burrowing Mammal |

---

## 🚀 Quick Start

### 1. Prerequisites
- **Node.js** v18+
- **Google Chrome** installed
- **FFmpeg** on system PATH (or configured in `pipeline/render_mp4.mjs`)

### 2. Inspect & Test Snapshots
Run the automated snapshot suite to capture high-resolution diagnostic frames at each beat:
```bash
node pipeline/test_snapshots.mjs
```
Snapshots are exported to `output/snap_beat*.jpg`.

### 3. Render 60-Second Master Video
Export the complete 1080×1920 @ 30fps MP4 video:
```bash
node pipeline/render_mp4.mjs
```
The output file will be generated at `output/pilot_dinosaurus_catalog.mp4`.

### 4. Interactive In-Browser Scrubber
To scrub through the timeline visually with live audio and timecode:
```
http://127.0.0.1:5199/index.html?debug=1
```

---

## 📁 Repository Structure

```
AG-Bang/
├── index.html                   # Master White Catalog Explainer engine (GSAP 3.12)
├── build_after_effects.jsx      # Adobe After Effects auto-build script
├── package.json                 # Node project configuration
├── .gitignore                   # Clean ignore rules (excludes renders and node_modules)
├── assets/
│   ├── audio/                   # 60s Kokoro English voiceover & audio cues
│   │   ├── vo_dinosaurus.wav
│   │   └── audio_cues.json
│   ├── images/                  # Photorealistic cutouts and archival photographs
│   │   ├── trex_fossil.png
│   │   ├── asteroid_entry_realistic.png
│   │   ├── meteorite_chondrite.png
│   │   ├── megatsunami_wave_realistic.png
│   │   ├── chicxulub_crater_aerial.png
│   │   ├── deccan_volcano.png
│   │   ├── sun_blackout.png
│   │   ├── fern_fossil.png
│   │   ├── iridium_layer.png
│   │   └── mammal_survivor.png
│   └── video/                   # Simulation reference media
├── pipeline/
│   ├── render_mp4.mjs           # Deterministic Puppeteer -> FFmpeg pipe renderer
│   ├── test_snapshots.mjs       # Multi-beat diagnostic frame exporter
│   ├── generate_assets_9router.py
│   └── generate_voice_kokoro.py
└── output/
    └── tiktok_viral_metadata.md # Viral retention hooks, SEO tags, and descriptions
```

---

## 📜 License & Attribution
MIT License. Inspired by the **Bang Motion** design framework by [Bang Tutorial](https://github.com/bangtutorial/bang-motion).
