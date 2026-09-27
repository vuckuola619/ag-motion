#!/usr/bin/env python3
"""build_ep8_editorial_film.py — Build premium, high-retention documentary editorial film for Episode 8.
Upgrades:
- Restrained color palette (parchment, ivory, charcoal, warm gold accent)
- Bespoke identity (MS 408 BEINECKE ARCHIVE, no borrowed Vox branding)
- Immediate curiosity macro-hook opening (no static blocking card)
- Purposeful shot choreography: camera pushes, focal shifts, macro crops
- Hand-crafted animated SVG Zipf's Law chart & C-14 radiocarbon Gaussian curve
- Sequential botanical & astronomical reveals (no multi-specimen clutter)
- Stable grounded physics (zero oscillation/shake)
- Whisper word-locked subtitle pill clear of mobile safe areas
- Final motif loop back to shelf MS 408
"""
import json
import os

def main():
    aligned_path = "assets/episode8_voynich_manuscript/audio/voynich_words_aligned.json"
    with open(aligned_path, "r", encoding="utf-8") as f:
        aligned_data = json.load(f)

    compact_words = []
    for w in aligned_data["global_words"]:
        compact_words.append({
            "w": w["word"],
            "s": w["global_start"],
            "e": w["global_end"],
            "b": w["beat_index"]
        })

    words_json = json.dumps(compact_words, separators=(',', ':'))

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>The Voynich Manuscript — Editorial Documentary Film</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #0C0E12;
  --canvas-dark: #101217;
  --canvas-vellum: #F3EFE6;
  --paper-card: #FAF8F2;
  --ink-dark: #12141A;
  --ink-light: #F2EFE8;
  --ink-muted: #8E93A0;
  --ink-dim: #606573;
  --gold: #C8973E;
  --gold-glow: rgba(200, 151, 62, 0.35);
  --vermilion: #B83526;
  --vermilion-soft: rgba(184, 53, 38, 0.16);
  --cyan-subtle: #4EA3A9;
  --border-subtle: rgba(255, 255, 255, 0.12);
  --border-paper: rgba(18, 20, 26, 0.14);
  --card-shadow: 0 16px 40px rgba(0, 0, 0, 0.45), 0 2px 8px rgba(0, 0, 0, 0.25);
  --contact-shadow: 0 20px 48px rgba(0, 0, 0, 0.55);
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; -webkit-font-smoothing: antialiased; }}
html, body {{
  width: 100%; height: 100%;
  background: #060709;
  overflow: hidden;
  font-family: "Inter", -apple-system, system-ui, sans-serif;
  color: var(--ink-light);
}}

/* 1080x1920 Stage Canvas */
#stage {{
  position: absolute;
  left: 50%; top: 50%;
  width: 1080px; height: 1920px;
  background: var(--bg);
  overflow: hidden;
  transform: translate(-50%, -50%);
  transform-origin: center center;
  box-shadow: 0 0 140px rgba(0, 0, 0, 0.98);
}}

/* Tactile 35mm Archival Film Grain */
.grain-overlay {{
  position: absolute; inset: 0;
  pointer-events: none;
  opacity: 0.11;
  mix-blend-mode: overlay;
  z-index: 80;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='260' height='260'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.78' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='260' height='260' filter='url(%23n)'/%3E%3C/svg%3E");
}}

/* Soft Vignette */
.vignette {{
  position: absolute; inset: 0;
  pointer-events: none;
  background: radial-gradient(circle at 50% 50%, transparent 60%, rgba(6, 7, 9, 0.65) 100%);
  z-index: 81;
}}

/* Optical Transit Shutter */
#transitShutter {{
  position: absolute; inset: 0;
  background: linear-gradient(90deg, transparent 0%, rgba(200, 151, 62, 0.18) 50%, transparent 100%);
  transform: translateX(-100%);
  pointer-events: none;
  z-index: 85;
  opacity: 0;
}}

/* Bespoke Editorial Archive Runner (No Borrowed Branding) */
#archiveRunner {{
  position: absolute;
  top: 72px; left: 60px; right: 60px;
  height: 64px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(14, 17, 23, 0.92);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  padding: 0 22px;
  border-radius: 6px;
  border: 1px solid var(--border-subtle);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.50);
  font-family: "JetBrains Mono", monospace;
  font-size: 17px;
  font-weight: 500;
  letter-spacing: 0.10em;
  color: var(--ink-muted);
  z-index: 90;
}}
#archiveRunner .badge {{
  background: var(--gold);
  color: #0E1015;
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 3px;
  font-size: 15px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}}
#archiveRunner .tag {{
  color: var(--ink-light);
  font-weight: 600;
}}

/* Master Camera & Panoramic Runway */
#cameraRig {{
  position: absolute;
  inset: 0;
  width: 1080px; height: 1920px;
  transform-origin: 540px 960px;
  will-change: transform;
}}

#runway {{
  position: absolute;
  top: 0; left: 0;
  width: 6480px; height: 1920px; /* 6 scenes x 1080px */
  display: flex;
  will-change: transform;
}}

.scene-dossier {{
  position: relative;
  width: 1080px; height: 1920px;
  flex-shrink: 0;
  overflow: hidden;
}}

/* Soft Background Canvas Layers (Never Muddy or Over-Contrasty) */
.scene-bg {{
  position: absolute;
  inset: 0;
  width: 1080px; height: 1920px;
  object-fit: cover;
  filter: brightness(0.72) contrast(1.08) saturate(0.85);
  transform: scale(1.02);
}}
.scene-scrim {{
  position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(12,14,18,0.70) 0%, rgba(12,14,18,0.40) 45%, rgba(12,14,18,0.85) 100%);
  pointer-events: none;
}}

/* Editorial Dossier Index Tag */
.dossier-tag {{
  position: absolute;
  font-family: "JetBrains Mono", monospace;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.14em;
  color: var(--gold);
  background: rgba(14, 17, 23, 0.92);
  padding: 6px 14px;
  border-left: 3px solid var(--gold);
  border-radius: 2px;
  z-index: 25;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
  text-transform: uppercase;
  opacity: 0;
}}
.dossier-tag.vermilion {{
  color: var(--vermilion);
  border-left-color: var(--vermilion);
}}
.dossier-tag.cyan {{
  color: var(--cyan-subtle);
  border-left-color: var(--cyan-subtle);
}}

/* Ghost Watermark Monogram */
.ghost-watermark {{
  position: absolute;
  font-family: "Cinzel", serif;
  font-weight: 900;
  font-size: 200px;
  line-height: 0.85;
  letter-spacing: -0.02em;
  color: transparent;
  -webkit-text-stroke: 2px rgba(242, 239, 232, 0.07);
  text-align: center;
  z-index: 6;
  pointer-events: none;
  white-space: nowrap;
  opacity: 0;
}}

/* Hero Artifact Cutout Sprites */
.artifact-sprite {{
  position: absolute;
  will-change: transform, opacity;
  filter: drop-shadow(0 20px 42px rgba(0, 0, 0, 0.65));
  z-index: 20;
}}
.artifact-sprite img {{
  display: block;
  width: 100%; height: 100%;
  object-fit: contain;
}}

/* Archival Specimen Callout Pill */
.specimen-pill {{
  position: absolute;
  padding: 6px 14px;
  background: rgba(14, 18, 25, 0.92);
  border: 1px solid rgba(255, 255, 255, 0.14);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  color: #ECE7DE;
  font-family: "JetBrains Mono", monospace;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.12em;
  border-radius: 4px;
  z-index: 26;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
  white-space: nowrap;
  opacity: 0;
}}

/* Precision Traced Annotation Boxes */
.traced-box {{
  position: absolute;
  border: 1.5px dashed var(--gold);
  border-radius: 6px;
  background: rgba(200, 151, 62, 0.05);
  z-index: 22;
  opacity: 0;
}}

/* Handwritten Field Notes */
.hand-note {{
  position: absolute;
  font-family: "Instrument Serif", serif;
  font-style: italic;
  font-size: 42px;
  line-height: 1.1;
  color: var(--gold);
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.8);
  z-index: 32;
  white-space: nowrap;
  letter-spacing: 0.01em;
}}
.hand-note.vermilion {{ color: var(--vermilion); }}
.hand-note.cyan {{ color: var(--cyan-subtle); }}

/* Clean Editorial Telemetry Card */
.telemetry-panel {{
  position: absolute;
  background: rgba(14, 18, 26, 0.94);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 18px 24px;
  box-shadow: var(--card-shadow);
  z-index: 25;
}}
.telemetry-panel .p-label {{
  font-family: "JetBrains Mono", monospace;
  font-size: 14px;
  font-weight: 600;
  color: var(--ink-muted);
  letter-spacing: 0.12em;
  margin-bottom: 4px;
  text-transform: uppercase;
}}
.telemetry-panel .p-value {{
  font-family: "Cinzel", serif;
  font-size: 64px;
  font-weight: 800;
  color: var(--gold);
  line-height: 0.95;
}}
.telemetry-panel .p-value.vermilion {{ color: var(--vermilion); }}
.telemetry-panel .p-value.cyan {{ color: var(--cyan-subtle); }}
.telemetry-panel .p-unit {{
  font-family: "JetBrains Mono", monospace;
  font-size: 18px;
  font-weight: 600;
  color: var(--ink-muted);
  margin-left: 8px;
}}

/* Restrained Archival Stamps */
.archival-stamp {{
  position: absolute;
  padding: 7px 20px;
  border: 3.5px solid var(--vermilion);
  border-radius: 6px;
  color: var(--vermilion);
  font-family: "JetBrains Mono", monospace;
  font-weight: 700;
  font-size: 26px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  background: rgba(14, 18, 25, 0.92);
  box-shadow: 0 8px 24px rgba(184, 53, 38, 0.30);
  z-index: 35;
  white-space: nowrap;
  opacity: 0;
}}
.archival-stamp.gold {{
  border-color: var(--gold);
  color: var(--gold);
  box-shadow: 0 8px 24px rgba(200, 151, 62, 0.30);
}}

/* Decisive Editorial Headline Box */
.editorial-headline-box {{
  position: absolute;
  left: 60px; right: 60px;
  top: 1340px;
  background: rgba(14, 18, 26, 0.94);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-left: 5px solid var(--gold);
  padding: 20px 26px;
  border-radius: 8px;
  box-shadow: var(--card-shadow);
  z-index: 40;
  opacity: 0;
}}
.editorial-headline-box.vermilion {{ border-left-color: var(--vermilion); }}
.editorial-headline-box.cyan {{ border-left-color: var(--cyan-subtle); }}
.editorial-headline-box .h-kicker {{
  font-family: "JetBrains Mono", monospace;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.14em;
  color: var(--gold);
  margin-bottom: 6px;
  text-transform: uppercase;
}}
.editorial-headline-box.vermilion .h-kicker {{ color: var(--vermilion); }}
.editorial-headline-box.cyan .h-kicker {{ color: var(--cyan-subtle); }}
.editorial-headline-box .h-text {{
  font-family: "Inter", sans-serif;
  font-size: 46px;
  font-weight: 800;
  line-height: 1.18;
  letter-spacing: -0.015em;
  color: #FFFFFF;
}}

/* Editorial Highlight Underlines */
.hl {{
  position: relative;
  display: inline-block;
  color: inherit;
  padding: 0 4px;
}}
.hl i {{
  position: absolute;
  left: 0; right: 0; bottom: 2px;
  height: 5px;
  background: var(--gold);
  border-radius: 3px;
  transform: scaleX(0);
  transform-origin: left;
  z-index: -1;
}}
.hl.r i {{ background: var(--vermilion); }}
.hl.c i {{ background: var(--cyan-subtle); }}

/* Dynamic Spoken TikTok Caption Pill (Clear of Bottom Safe Area) */
#captionPillContainer {{
  position: absolute;
  bottom: 110px;
  left: 50%;
  transform: translateX(-50%);
  width: 900px;
  display: flex;
  justify-content: center;
  z-index: 95;
  pointer-events: none;
}}
#captionPill {{
  background: rgba(14, 18, 25, 0.94);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.16);
  padding: 14px 30px;
  border-radius: 999px;
  box-shadow: 0 10px 32px rgba(0, 0, 0, 0.70);
  font-family: "Inter", sans-serif;
  font-size: 38px;
  font-weight: 700;
  letter-spacing: 0.01em;
  color: #FFFFFF;
  text-align: center;
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 10px;
}}
.sub-word {{
  display: inline-block;
  color: #DDD8CE;
  transition: color 0.1s ease, transform 0.1s ease;
}}
.sub-word.active {{
  color: var(--gold);
  font-weight: 800;
  transform: scale(1.08);
  text-shadow: 0 0 16px var(--gold-glow);
}}
.sub-word.past {{
  color: #8C877D;
}}

/* Vector Chart Containers (Zipf & Radiocarbon) */
.vector-chart-panel {{
  position: absolute;
  top: 730px; left: 80px; width: 920px; height: 380px;
  background: rgba(14, 18, 26, 0.95);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 20px 24px;
  box-shadow: var(--card-shadow);
  z-index: 24;
  opacity: 0;
}}
.vector-chart-panel .chart-header {{
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 12px;
}}
.vector-chart-panel .chart-title {{
  font-family: "JetBrains Mono", monospace;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.10em;
  color: var(--gold);
  text-transform: uppercase;
}}
.vector-chart-panel .chart-sub {{
  font-family: "JetBrains Mono", monospace;
  font-size: 13px;
  color: var(--ink-muted);
}}

/* Opening Macro Curiosity Card (Integrated into Flow) */
#openingMacroCard {{
  position: absolute;
  top: 420px; left: 80px; right: 80px;
  background: rgba(14, 18, 26, 0.94);
  border-left: 5px solid var(--gold);
  border-radius: 8px;
  padding: 32px 36px;
  box-shadow: var(--card-shadow);
  z-index: 50;
  opacity: 0;
}}
#openingMacroCard .kicker {{
  font-family: "JetBrains Mono", monospace;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: var(--gold);
  margin-bottom: 10px;
  text-transform: uppercase;
}}
#openingMacroCard .title {{
  font-family: "Cinzel", serif;
  font-size: 58px;
  font-weight: 900;
  line-height: 1.05;
  color: #FFFFFF;
  letter-spacing: -0.01em;
  margin-bottom: 16px;
}}
#openingMacroCard .meta {{
  font-family: "JetBrains Mono", monospace;
  font-size: 20px;
  line-height: 1.5;
  color: var(--ink-muted);
}}

/* Outro Heavy Rubber Stamp */
#outroFinalStamp {{
  position: absolute;
  top: 760px; left: 50%;
  width: 860px; height: 320px;
  transform: translate(-50%, 0) rotate(-6deg) scale(2.4);
  opacity: 0;
  z-index: 48;
  filter: drop-shadow(0 20px 48px rgba(184, 53, 38, 0.80));
}}
</style>
</head>
<body>

<div id="stage">
  <div class="grain-overlay"></div>
  <div class="vignette"></div>
  <div id="transitShutter"></div>

  <!-- Editorial Top Archive Runner -->
  <div id="archiveRunner">
    <div style="display: flex; align-items: center; gap: 14px;">
      <span class="badge">MS 408 ARCHIVE</span>
      <span class="tag" id="runnerDossier">HISTORICAL INVESTIGATION · DOSSIER #08</span>
    </div>
    <div id="runnerTimeline" style="color: var(--ink-muted); font-size: 16px;">YALE BEINECKE LIBRARY</div>
  </div>

  <!-- Master Camera Rig (Provides Slow Cinematic Breathing / Pushes) -->
  <div id="cameraRig">
    <div id="runway">

      <!-- ========================================================================= -->
      <!-- SCENE 1: THE MONASTERY DISCOVERY & UNKNOWN SCRIPT (X = 0)                 -->
      <!-- ========================================================================= -->
      <div class="scene-dossier" id="scene1">
        <img class="scene-bg" src="assets/episode8_voynich_manuscript/images/bg_monastery_library_vault.png" alt="Jesuit Vault">
        <div class="scene-scrim"></div>

        <div class="dossier-tag" style="top: 175px; left: 70px;">ARCHIVAL RECOVERY // VILLA MONDRAGONE · 1912</div>
        <div class="ghost-watermark" style="top: 170px; left: 70px; width: 940px;">1912</div>

        <!-- Opening Macro Curiosity Card (0.2s - 2.8s) -->
        <div id="openingMacroCard">
          <div class="kicker">DOCUMENTARY INQUIRY · UNBROKEN CIPHER</div>
          <div class="title">THE 600-YEAR-OLD CODE MODERN AI CANNOT CRACK</div>
          <div class="meta">
            Artifact: Yale Beinecke MS 408<br>
            240 Extant Pages · 0 Translated Words
          </div>
        </div>

        <!-- Closed Codex Hero Cutout -->
        <div class="artifact-sprite" id="spBook" style="top: 270px; left: 140px; width: 800px; height: 480px;">
          <img src="assets/episode8_voynich_manuscript/images/sprite_voynich_closed_book.png" alt="Voynich Closed Book">
        </div>

        <!-- Broken Jesuit Wax Seal -->
        <div class="artifact-sprite" id="spWax" style="top: 240px; right: 90px; width: 220px; height: 220px;">
          <img src="assets/episode8_voynich_manuscript/images/sprite_red_wax_seal_broken.png" alt="Broken Wax Seal">
        </div>

        <!-- Quill & Inkwell -->
        <div class="artifact-sprite" id="spQuill" style="top: 740px; left: 80px; width: 340px; height: 320px;">
          <img src="assets/episode8_voynich_manuscript/images/sprite_quill_ink_well.png" alt="Quill and Ink">
        </div>

        <!-- Open Spread Reveal (Match Cut for Beat 2) -->
        <div class="artifact-sprite" id="spOpenSpread1" style="top: 300px; left: 90px; width: 900px; height: 500px;">
          <img src="assets/episode8_voynich_manuscript/images/sprite_voynich_open_spread.png" alt="Open Folio Spread">
        </div>

        <div class="specimen-pill" id="pillSubstrate" style="top: 710px; left: 110px;">SUBSTRATE: GOAT VELLUM</div>
        <div class="specimen-pill" id="pillVolume" style="top: 710px; right: 110px;">VOLUME: 240 FOLIO LEAVES</div>

        <!-- Field Notes -->
        <div class="hand-note" id="hn1_1" style="top: 780px; left: 450px; transform: rotate(-2.5deg);">
          Found in a secluded Jesuit library chest
        </div>
        <div class="hand-note cyan" id="hn1_2" style="top: 840px; left: 130px; transform: rotate(1.8deg);">
          Unbroken glyphs unknown to human history
        </div>

        <!-- Telemetry Panel -->
        <div class="telemetry-panel" id="cardTelemetry1" style="top: 870px; left: 450px; width: 360px;">
          <div class="p-label">SURVIVING FOLIOS</div>
          <div style="display: flex; align-items: baseline;">
            <span class="p-value" id="valFolios">240</span>
            <span class="p-unit">PAGES</span>
          </div>
        </div>

        <!-- Archival Verification Stamp -->
        <div class="archival-stamp" id="stampArtifact" style="top: 1010px; left: 470px; transform: rotate(-7deg);">
          ARCHIVE VERIFIED
        </div>

        <!-- Beat 1 & 2 Headlines -->
        <div class="editorial-headline-box" id="hlBox1_1">
          <div class="h-kicker">1912 DISCOVERY · JESUIT ARCHIVE</div>
          <div class="h-text">
            Antique dealer Wilfrid Voynich uncovered an <span class="hl" id="hl1_1"><i></i>unbreakable 600-year enigma.</span>
          </div>
        </div>

        <div class="editorial-headline-box cyan" id="hlBox1_2">
          <div class="h-kicker">THE UNKNOWN SCRIPT</div>
          <div class="h-text">
            240 illustrated leaves written in a <span class="hl c" id="hl1_2"><i></i>completely unmapped language.</span>
          </div>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- SCENE 2: BOTANICAL & CELESTIAL ANOMALIES (X = -1080)                     -->
      <!-- ========================================================================= -->
      <div class="scene-dossier" id="scene2">
        <img class="scene-bg" src="assets/episode8_voynich_manuscript/images/bg_botanical_herbal_folio.png" alt="Botanical Folio">
        <div class="scene-scrim"></div>

        <div class="dossier-tag" style="top: 175px; left: 70px;">ILLUSTRATED FOLIOS // BOTANICAL & CELESTIAL SECTIONS</div>
        <div class="ghost-watermark" style="top: 170px; left: 70px; width: 940px;">FOLIO 42</div>

        <!-- Sequential Focus 1: Alien Flower -->
        <div class="artifact-sprite" id="spAlienFlower" style="top: 260px; left: 100px; width: 480px; height: 460px;">
          <img src="assets/episode8_voynich_manuscript/images/sprite_alien_flower_cutout.png" alt="Impossible Flower">
        </div>

        <!-- Traced Root Annotation Box -->
        <div class="traced-box" id="boxRoot" style="top: 560px; left: 180px; width: 320px; height: 160px;"></div>

        <!-- Sequential Focus 2: Vascular Leaf -->
        <div class="artifact-sprite" id="spVascularLeaf" style="top: 280px; right: 90px; width: 380px; height: 420px;">
          <img src="assets/episode8_voynich_manuscript/images/sprite_alien_vascular_leaf.png" alt="Alien Leaf Structure">
        </div>

        <!-- Magnifying Lens Inspection -->
        <div class="artifact-sprite" id="spMagnifier" style="top: 340px; right: 130px; width: 280px; height: 280px;">
          <img src="assets/episode8_voynich_manuscript/images/sprite_magnifying_glass.png" alt="Magnifying Glass">
        </div>

        <!-- Sequential Focus 3: Zodiac Star Wheel & Fluid Tubes -->
        <div class="artifact-sprite" id="spZodiac" style="top: 280px; left: 90px; width: 440px; height: 440px;">
          <img src="assets/episode8_voynich_manuscript/images/sprite_zodiac_star_wheel.png" alt="Zodiac Wheel">
        </div>

        <div class="artifact-sprite" id="spTubes" style="top: 280px; right: 90px; width: 440px; height: 440px;">
          <img src="assets/episode8_voynich_manuscript/images/sprite_balneological_tubes.png" alt="Organic Plumbing">
        </div>

        <div class="specimen-pill" id="pillBot1" style="top: 740px; left: 100px;">ROOT MORPHOLOGY: PREDATORY CLAWS</div>
        <div class="specimen-pill" id="pillBot2" style="top: 740px; right: 100px;">CELESTIAL DIALS: 30 CONCENTRIC SECTORS</div>

        <div class="hand-note" id="hn2_1" style="top: 800px; left: 140px; transform: rotate(-3deg);">
          Roots resembling animal claws
        </div>
        <div class="hand-note cyan" id="hn2_2" style="top: 800px; left: 140px; transform: rotate(1.8deg);">
          Intricate fluid conduits & uncharted stars
        </div>

        <!-- Telemetry Panel -->
        <div class="telemetry-panel" id="cardTelemetry2" style="top: 870px; left: 70px; width: 460px;">
          <div class="p-label">KNOWN BOTANICAL MATCH</div>
          <div style="display: flex; align-items: baseline;">
            <span class="p-value vermilion" id="valPlantMatch">0%</span>
            <span class="p-unit">OF 300+ SPECIES</span>
          </div>
        </div>

        <!-- Beat 3 & 4 Headlines -->
        <div class="editorial-headline-box" id="hlBox2_1">
          <div class="h-kicker">IMPOSSIBLE BOTANY</div>
          <div class="h-text">
            Drawings depict <span class="hl" id="hl2_1"><i></i>bizarre botanical hybrids</span> with no match on Earth.
          </div>
        </div>

        <div class="editorial-headline-box cyan" id="hlBox2_2">
          <div class="h-kicker">CELESTIAL WHEELS</div>
          <div class="h-text">
            Cosmological star wheels and <span class="hl c" id="hl2_2"><i></i>unmapped zodiac constellations.</span>
          </div>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- SCENE 3: RADIOCARBON FORENSICS (X = -2160)                               -->
      <!-- ========================================================================= -->
      <div class="scene-dossier" id="scene3">
        <img class="scene-bg" src="assets/episode8_voynich_manuscript/images/bg_accelerator_mass_spectrometry.png" alt="AMS Laboratory">
        <div class="scene-scrim"></div>

        <div class="dossier-tag" style="top: 175px; left: 70px;">FORENSIC MEASUREMENT // UNIV. OF ARIZONA AMS</div>
        <div class="ghost-watermark" style="top: 170px; left: 70px; width: 940px;">1404 AD</div>

        <!-- Micro-sample Target Core -->
        <div class="artifact-sprite" id="spAmsCore" style="top: 260px; left: 90px; width: 500px; height: 460px;">
          <img src="assets/episode8_voynich_manuscript/images/sprite_arizona_ams_core.png" alt="Arizona AMS Core">
        </div>

        <!-- Calibrated Archival Scale -->
        <div class="artifact-sprite" id="spRuler" style="top: 310px; right: 90px; width: 380px; height: 380px;">
          <img src="assets/episode8_voynich_manuscript/images/sprite_vintage_ruler_scale.png" alt="Archival Ruler">
        </div>

        <!-- Hand-Crafted SVG Radiocarbon Gaussian Calibration Chart -->
        <div class="vector-chart-panel" id="panelC14" style="top: 740px;">
          <div class="chart-header">
            <span class="chart-title">14C Accelerator Mass Spectrometry Calibration</span>
            <span class="chart-sub">95.4% Confidence Interval (IntCal20)</span>
          </div>
          <svg width="870" height="260" viewBox="0 0 870 260" style="overflow: visible;">
            <!-- Grid Lines -->
            <line x1="60" y1="210" x2="840" y2="210" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
            <line x1="60" y1="30" x2="60" y2="210" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
            <!-- X Axis Marks -->
            <text x="120" y="235" fill="#8E93A0" font-family="JetBrains Mono" font-size="14">1350 AD</text>
            <text x="320" y="235" fill="#C8973E" font-family="JetBrains Mono" font-weight="700" font-size="15">1404 AD</text>
            <text x="560" y="235" fill="#C8973E" font-family="JetBrains Mono" font-weight="700" font-size="15">1438 AD</text>
            <text x="760" y="235" fill="#8E93A0" font-family="JetBrains Mono" font-size="14">1500 AD</text>
            <!-- 1404-1438 Shaded Confidence Band -->
            <rect id="c14Band" x="320" y="30" width="240" height="180" fill="rgba(200,151,62,0.15)" stroke="rgba(200,151,62,0.4)" stroke-dasharray="4 4" opacity="0"/>
            <!-- Animated Gaussian Distribution Curve -->
            <path id="c14Curve" d="M 120 205 Q 260 200, 380 100 T 440 45 T 500 100 Q 620 200, 760 205" fill="none" stroke="#C8973E" stroke-width="3.5" stroke-linecap="round" stroke-dasharray="1000" stroke-dashoffset="1000"/>
          </svg>
        </div>

        <div class="specimen-pill" id="pillAms1" style="top: 680px; left: 110px;">TEST: ACCELERATOR MASS SPECTROMETRY</div>
        <div class="specimen-pill" id="pillAms2" style="top: 680px; right: 110px;">CONFIDENCE: 95.4% 2-SIGMA</div>

        <div class="hand-note vermilion" id="hn3_1" style="top: 540px; left: 140px; transform: rotate(-2.5deg);">
          Skeptics claimed a Renaissance forgery
        </div>
        <div class="hand-note" id="hn3_2" style="top: 1060px; left: 100px; transform: rotate(1.8deg);">
          Parchment prepared 1404–1438 AD
        </div>

        <!-- Telemetry Panel -->
        <div class="telemetry-panel" id="cardTelemetry3" style="top: 1130px; left: 80px; width: 460px;">
          <div class="p-label">CALIBRATED VELLUM DATE</div>
          <div style="display: flex; align-items: baseline;">
            <span class="p-value" id="valCarbonDate">1404</span>
            <span class="p-unit">– 1438 AD</span>
          </div>
        </div>

        <!-- Restrained Stamp -->
        <div class="archival-stamp gold" id="stampDebunked" style="top: 1070px; right: 80px; transform: rotate(5deg);">
          DATING CONFIRMED
        </div>

        <!-- Headlines -->
        <div class="editorial-headline-box vermilion" id="hlBox3_1">
          <div class="h-kicker">THE HOAX THEORY</div>
          <div class="h-text">
            For nearly a century, skeptics dismissed it as an <span class="hl r" id="hl3_1"><i></i>elaborate Renaissance forgery.</span>
          </div>
        </div>

        <div class="editorial-headline-box" id="hlBox3_2">
          <div class="h-kicker">PHYSICS INTERVENES</div>
          <div class="h-text">
            Physicists dated parchment samples using <span class="hl" id="hl3_2"><i></i>accelerator mass spectrometry.</span>
          </div>
        </div>

        <div class="editorial-headline-box" id="hlBox3_3">
          <div class="h-kicker">SCIENTIFIC VERDICT</div>
          <div class="h-text">
            The calfskin vellum was prepared <span class="hl" id="hl3_3"><i></i>between 1404 and 1438 AD.</span>
          </div>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- SCENE 4: MATHEMATICAL ARCHITECTURE & ZIPF'S LAW (X = -3240)               -->
      <!-- ========================================================================= -->
      <div class="scene-dossier" id="scene4">
        <img class="scene-bg" src="assets/episode8_voynich_manuscript/images/bg_ancient_vellum_parchment.png" alt="Ancient Parchment">
        <div class="scene-scrim"></div>

        <div class="dossier-tag" style="top: 175px; left: 70px;">STATISTICAL CRYPTANALYSIS // MATHEMATICAL FREQUENCY MODEL</div>
        <div class="ghost-watermark" style="top: 170px; left: 70px; width: 940px;">ZIPF</div>

        <!-- Hand-Crafted SVG Zipf's Law Log-Log Chart -->
        <div class="vector-chart-panel" id="panelZipf" style="top: 260px; height: 420px;">
          <div class="chart-header">
            <span class="chart-title">Zipf's Law Log-Log Frequency Distribution</span>
            <span class="chart-sub">Log(Rank) vs Log(Frequency) — Slope = -1.02</span>
          </div>
          <svg width="870" height="310" viewBox="0 0 870 310" style="overflow: visible;">
            <!-- Grid Lines -->
            <line x1="70" y1="260" x2="830" y2="260" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
            <line x1="70" y1="30" x2="70" y2="260" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
            <!-- Labels -->
            <text x="80" y="285" fill="#8E93A0" font-family="JetBrains Mono" font-size="13">Rank 1 (Most Frequent)</text>
            <text x="680" y="285" fill="#8E93A0" font-family="JetBrains Mono" font-size="13">Rank 10,000</text>
            <!-- Theoretical Human Speech Baseline (Dashed) -->
            <line id="zipfTheoLine" x1="100" y1="50" x2="800" y2="245" stroke="#8E93A0" stroke-width="2" stroke-dasharray="6 6"/>
            <text x="620" y="225" fill="#8E93A0" font-family="JetBrains Mono" font-size="12">Natural Language (k = -1.0)</text>
            <!-- Voynich Empirical Curve (Traced Gold) -->
            <path id="zipfVoynichCurve" d="M 100 52 L 200 85 L 320 120 L 460 155 L 620 198 L 800 248" fill="none" stroke="#C8973E" stroke-width="4" stroke-linecap="round" stroke-dasharray="1000" stroke-dashoffset="1000"/>
            <!-- Data Scatter Dots -->
            <circle cx="100" cy="52" r="5" fill="#C8973E"/>
            <circle cx="200" cy="85" r="5" fill="#C8973E"/>
            <circle cx="320" cy="120" r="5" fill="#C8973E"/>
            <circle cx="460" cy="155" r="5" fill="#C8973E"/>
            <circle cx="620" cy="198" r="5" fill="#C8973E"/>
            <circle cx="800" cy="248" r="5" fill="#C8973E"/>
          </svg>
        </div>

        <!-- Alphabet Sample with Morphology Anatomy -->
        <div class="artifact-sprite" id="spAlphabet" style="top: 300px; left: 90px; width: 900px; height: 360px;">
          <img src="assets/episode8_voynich_manuscript/images/sprite_voynich_alphabet_sample.png" alt="Voynich Alphabet">
        </div>

        <div class="specimen-pill" id="pillZipf1" style="top: 710px; left: 110px;">ZIPF POWER EXPONENT: -1.02</div>
        <div class="specimen-pill" id="pillZipf2" style="top: 710px; right: 110px;">MORPHOLOGY: PREFIX + ROOT + SUFFIX</div>

        <div class="hand-note" id="hn4_1" style="top: 770px; left: 120px; transform: rotate(-2.5deg);">
          Matches the exact frequency slope of natural speech
        </div>
        <div class="hand-note cyan" id="hn4_2" style="top: 770px; left: 120px; transform: rotate(1.8deg);">
          Rigorous grammar — not medieval gibberish
        </div>

        <!-- Telemetry Panel -->
        <div class="telemetry-panel" id="cardTelemetry4" style="top: 850px; left: 80px; width: 440px;">
          <div class="p-label">TOTAL GLYPH SAMPLE</div>
          <div style="display: flex; align-items: baseline;">
            <span class="p-value" id="valGlyphs">170,000</span>
            <span class="p-unit">SIGNS</span>
          </div>
        </div>

        <div class="archival-stamp gold" id="stampZipf" style="top: 850px; right: 80px; transform: rotate(-5deg);">
          ZIPF LAW CONFIRMED
        </div>

        <!-- Headlines -->
        <div class="editorial-headline-box" id="hlBox4_1">
          <div class="h-kicker">MATHEMATICAL PROOF</div>
          <div class="h-text">
            Statistical analysis proved the cipher strictly obeys <span class="hl" id="hl4_1"><i></i>Zipf's Law.</span>
          </div>
        </div>

        <div class="editorial-headline-box cyan" id="hlBox4_2">
          <div class="h-kicker">LINGUISTIC ARCHITECTURE</div>
          <div class="h-text">
            A complex syntax of prefixes and roots — <span class="hl c" id="hl4_2"><i></i>genuine human language.</span>
          </div>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- SCENE 5: CRYPTANALYSIS & MODERN AI ATTEMPTS (X = -4320)                    -->
      <!-- ========================================================================= -->
      <div class="scene-dossier" id="scene5">
        <img class="scene-bg" src="assets/episode8_voynich_manuscript/images/bg_ancient_vellum_parchment.png" alt="Ancient Parchment">
        <div class="scene-scrim"></div>

        <div class="dossier-tag vermilion" style="top: 175px; left: 70px;">DECIPHERMENT ATTEMPTS // MILITARY INTELLIGENCE & AI</div>
        <div class="ghost-watermark" style="top: 170px; left: 70px; width: 940px;">UNBROKEN</div>

        <!-- William Friedman Portrait -->
        <div class="artifact-sprite" id="spFriedman" style="top: 260px; left: 100px; width: 420px; height: 440px;">
          <img src="assets/episode8_voynich_manuscript/images/sprite_william_friedman_portrait.png" alt="William Friedman">
        </div>

        <!-- NSA Cryptanalysis Seal -->
        <div class="artifact-sprite" id="spNsaSeal" style="top: 280px; right: 100px; width: 400px; height: 400px;">
          <img src="assets/episode8_voynich_manuscript/images/sprite_nsa_cryptanalysis_seal.png" alt="NSA Cryptanalysis Seal">
        </div>

        <!-- Neural Network Architecture -->
        <div class="artifact-sprite" id="spNeuralNet" style="top: 290px; left: 90px; width: 900px; height: 420px;">
          <img src="assets/episode8_voynich_manuscript/images/sprite_neural_network_nodes.png" alt="Neural Network Nodes">
        </div>

        <div class="specimen-pill" id="pillCode1" style="top: 760px; left: 110px;">WWII CODEBREAKERS: DEFEATED</div>
        <div class="specimen-pill" id="pillCode2" style="top: 760px; right: 110px;">NEURAL NETWORKS: 0 TRANSLATIONS</div>

        <div class="hand-note vermilion" id="hn5_1" style="top: 820px; left: 120px; transform: rotate(-2.5deg);">
          Friedman dedicated 30 years without solving one word
        </div>
        <div class="hand-note cyan" id="hn5_2" style="top: 790px; left: 120px; transform: rotate(1.8deg);">
          Modern AI models hit a mathematical wall
        </div>

        <!-- Telemetry Panel -->
        <div class="telemetry-panel" id="cardTelemetry5" style="top: 870px; left: 70px; width: 460px;">
          <div class="p-label">SOLVED CIPHER PHRASES</div>
          <div style="display: flex; align-items: baseline;">
            <span class="p-value vermilion" id="valSolvedKeys">0</span>
            <span class="p-unit">WORDS DECRYPTED</span>
          </div>
        </div>

        <div class="archival-stamp" id="stampColdCase" style="top: 870px; right: 80px; transform: rotate(-5deg);">
          COLD CASE
        </div>

        <!-- Headlines -->
        <div class="editorial-headline-box vermilion" id="hlBox5_1">
          <div class="h-kicker">CODEBREAKER FAILURE</div>
          <div class="h-text">
            US military cryptanalysts and <span class="hl r" id="hl5_1"><i></i>modern neural networks</span> both hit a wall.
          </div>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- SCENE 6: YALE BEINECKE VAULT & THE ENDURING ENIGMA (X = -5400)            -->
      <!-- ========================================================================= -->
      <div class="scene-dossier" id="scene6">
        <img class="scene-bg" src="assets/episode8_voynich_manuscript/images/bg_beinecke_rare_book_vault.png" alt="Beinecke Rare Book Vault">
        <div class="scene-scrim"></div>

        <div class="dossier-tag" style="top: 175px; left: 70px;">YALE ARCHIVE // BEINECKE RARE BOOK VAULT</div>
        <div class="ghost-watermark" style="top: 170px; left: 70px; width: 940px;">UNSOLVED</div>

        <!-- Beinecke Library Seal -->
        <div class="artifact-sprite" id="spBeineckeSeal" style="top: 240px; left: 100px; width: 240px; height: 240px;">
          <img src="assets/episode8_voynich_manuscript/images/sprite_beinecke_library_seal.png" alt="Beinecke Seal">
        </div>

        <!-- Cardboard Archival Box -->
        <div class="artifact-sprite" id="spArchiveBox" style="top: 230px; right: 100px; width: 340px; height: 280px;">
          <img src="assets/episode8_voynich_manuscript/images/sprite_cardboard_archival_box.png" alt="Archival Box">
        </div>

        <!-- Call Number Tag -->
        <div class="artifact-sprite" id="spCallTag" style="top: 480px; right: 120px; width: 300px; height: 90px;">
          <img src="assets/episode8_voynich_manuscript/images/sprite_ms408_callnumber_tag.png" alt="MS 408 Tag">
        </div>

        <!-- Open Voynich Spread Centerpiece -->
        <div class="artifact-sprite" id="spFinalSpread" style="top: 560px; left: 80px; width: 920px; height: 540px;">
          <img src="assets/episode8_voynich_manuscript/images/sprite_voynich_open_spread.png" alt="Voynich Open Spread">
        </div>

        <!-- Outro Climax Stamp Slammed Directly on Folio -->
        <div id="outroFinalStamp">
          <img src="assets/episode8_voynich_manuscript/images/sprite_stamp_case_unresolved.png" alt="Case Unresolved Stamp" style="width: 100%; height: 100%; object-fit: contain;">
        </div>

        <div class="hand-note" id="hn6_1" style="top: 1140px; left: 90px; transform: rotate(-2deg);">
          Vault Shelf MS 408 — Unbroken across six centuries
        </div>

        <!-- Telemetry Panel -->
        <div class="telemetry-panel" id="cardTelemetry6" style="top: 1120px; right: 80px; width: 440px;">
          <div class="p-label">DECIPHERED WORDS</div>
          <div style="display: flex; align-items: baseline;">
            <span class="p-value vermilion" id="valDeciphered">0</span>
            <span class="p-unit">TRANSLATED</span>
          </div>
        </div>

        <!-- Headlines -->
        <div class="editorial-headline-box" id="hlBox6_1">
          <div class="h-kicker">THE YALE VAULT</div>
          <div class="h-text">
            Locked in Yale's rare book vault — <span class="hl" id="hl6_1"><i></i>a code that has defeated every mind.</span>
          </div>
        </div>

        <div class="editorial-headline-box vermilion" id="hlBox6_2">
          <div class="h-kicker">FINAL VERDICT</div>
          <div class="h-text">
            Six centuries later, the Voynich code remains <span class="hl r" id="hl6_2"><i></i>entirely unsolved.</span>
          </div>
        </div>
      </div>

    </div> <!-- /#runway -->
  </div> <!-- /#cameraRig -->

  <!-- Whisper-Locked Dynamic Spoken Subtitle Pill -->
  <div id="captionPillContainer">
    <div id="captionPill">
      <span id="captionWords">The Voynich Manuscript</span>
    </div>
  </div>

</div> <!-- /#stage -->

<audio id="audioTrack" src="assets/episode8_voynich_manuscript/audio/vo_voynich_cinematic.mp3" preload="auto"></audio>

<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script>
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

const W = 1080, H = 1920, DURATION = 152.923;

/* Stage Auto-Scaler */
function fitStage() {{
  const sx = window.innerWidth / W;
  const sy = window.innerHeight / H;
  const s = Math.min(sx, sy);
  $('#stage').style.transform = `translate(-50%, -50%) scale(${{s}})`;
}}
window.addEventListener('resize', fitStage);
fitStage();

/* Embedded Whisper Aligned Words */
const ALIGNED_WORDS = {words_json};

/* Group Aligned Words into 3-5 Word Natural Phrase Chunks */
const CHUNKS = [];
let curChunk = [];
let curChars = 0;
for (const w of ALIGNED_WORDS) {{
  curChunk.push(w);
  curChars += w.w.length + 1;
  const isPunc = /[.!?;:]$/.test(w.w);
  if (curChunk.length >= 4 || curChars >= 28 || isPunc) {{
    CHUNKS.push({{
      start: curChunk[0].s,
      end: curChunk[curChunk.length - 1].e,
      words: curChunk
    }});
    curChunk = [];
    curChars = 0;
  }}
}}
if (curChunk.length) {{
  CHUNKS.push({{
    start: curChunk[0].s,
    end: curChunk[curChunk.length - 1].e,
    words: curChunk
  }});
}}

/* Dynamic Caption Pill Update Engine */
const captionPill = $('#captionPill');
const captionWords = $('#captionWords');

function updateDynamicSubtitles(t) {{
  const chunk = CHUNKS.find(c => t >= c.start - 0.05 && t <= c.end + 0.35);
  if (!chunk) {{
    captionPill.style.opacity = '0';
    return;
  }}
  captionPill.style.opacity = '1';

  let html = '';
  for (const w of chunk.words) {{
    const isActive = (t >= w.s && t <= w.e);
    const isPast = (t > w.e);
    const cls = isActive ? 'sub-word active' : (isPast ? 'sub-word past' : 'sub-word');
    html += `<span class="${{cls}}">${{w.w}}</span> `;
  }}
  captionWords.innerHTML = html;
}}

/* GSAP Master Choreography */
const tl = gsap.timeline({{ paused: true }});
const cameraRig = $('#cameraRig');
const runway = $('#runway');

/* Camera Transition Helper with Transit Shutter */
function glideTo(startTime, targetX, dur = 0.85) {{
  tl.to(runway, {{
    x: targetX,
    duration: dur,
    ease: 'power2.inOut'
  }}, startTime);

  // Subtle optical transit shutter
  tl.fromTo('#transitShutter', {{ opacity: 0, x: '-100%' }}, {{ opacity: 0.45, x: '100%', duration: dur * 0.7, ease: 'power2.inOut' }}, startTime + dur * 0.15);
  tl.to('#transitShutter', {{ opacity: 0, duration: 0.15 }}, startTime + dur * 0.85);
}}

/* Slow Cinematic Reading Push (Keeps Camera Gently Breathing, No Wobble) */
function cameraPush(startTime, targetScale, dur = 8.0) {{
  tl.to(cameraRig, {{
    scale: targetScale,
    duration: dur,
    ease: 'sine.inOut'
  }}, startTime);
}}

/* Headline Swap Helper */
function showHeadline(sel, startTime, hlSel) {{
  tl.fromTo(sel, {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.50, ease: 'power3.out' }}, startTime);
  if (hlSel) {{
    tl.fromTo(`${{hlSel}} i`, {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.40, ease: 'power3.out' }}, startTime + 0.40);
  }}
}}
function hideHeadline(sel, startTime) {{
  tl.to(sel, {{ opacity: 0, y: -16, duration: 0.30, ease: 'power2.in' }}, startTime);
}}

/* Stamp Slam Helper */
function slamStamp(sel, startTime) {{
  tl.fromTo(sel, {{ opacity: 0, scale: 2.1 }}, {{ opacity: 1, scale: 1, duration: 0.24, ease: 'power4.in' }}, startTime);
}}

/* --------------------------------------------------------------------------
   BUILD MASTER EDITORIAL CHOREOGRAPHY (152.92s)
   -------------------------------------------------------------------------- */

// =========================================================================
// SHOT 1A: CURIOSITY MACRO HOOK (0.0s - 3.2s)
// Starts immediately on macro book crop with bold hook
// =========================================================================
tl.set(runway, {{ x: 0 }}, 0);
tl.set(cameraRig, {{ scale: 1.15, transformOrigin: '540px 600px' }}, 0);

// Opening Macro Hook Card fades in immediately
tl.fromTo('#openingMacroCard', {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.65, ease: 'power2.out' }}, 0.1);
tl.fromTo('#spBook', {{ opacity: 0, scale: 0.95 }}, {{ opacity: 1, scale: 1, duration: 0.85, ease: 'power3.out' }}, 0.3);

// Smooth pull-back from macro to wide establishing shot as voiceover enters (1.8s - 3.4s)
tl.to(cameraRig, {{ scale: 1.0, transformOrigin: '540px 960px', duration: 1.6, ease: 'power2.inOut' }}, 1.8);
tl.to('#openingMacroCard', {{ opacity: 0, y: -20, duration: 0.6, ease: 'power2.in' }}, 2.6);

// =========================================================================
// SHOT 1B: VILLA MONDRAGONE & THE CLOSED CODEX (3.2s - 11.5s)
// =========================================================================
tl.to(['#scene1 .dossier-tag', '#scene1 .ghost-watermark'], {{ opacity: 1, duration: 0.6, ease: 'power2.out' }}, 3.2);
tl.fromTo('#spWax', {{ opacity: 0, scale: 1.4, rotate: -15 }}, {{ opacity: 1, scale: 1, rotate: 0, duration: 0.65, ease: 'back.out(1.4)' }}, 3.2);
tl.fromTo('#spQuill', {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.70, ease: 'power3.out' }}, 3.6);
tl.fromTo(['#pillSubstrate', '#pillVolume'], {{ opacity: 0, y: 15 }}, {{ opacity: 1, y: 0, duration: 0.50, ease: 'power3.out' }}, 4.0);
tl.fromTo('#hn1_1', {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.50, ease: 'back.out' }}, 4.4);
tl.fromTo('#cardTelemetry1', {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.55, ease: 'power3.out' }}, 4.8);
slamStamp('#stampArtifact', 6.0);

// Beat 1 Headline (3.4s - 10.69s)
showHeadline('#hlBox1_1', 3.4, '#hl1_1');
hideHeadline('#hlBox1_1', 10.8);

// =========================================================================
// SHOT 1C: THE OPEN SPREAD & UNKNOWN SCRIPT (11.5s - 21.0s)
// Match-reveal into open spread
// =========================================================================
tl.to(['#spBook', '#spWax', '#spQuill', '#hn1_1', '#stampArtifact', '#pillSubstrate', '#pillVolume', '#cardTelemetry1'], {{ opacity: 0, duration: 0.5, ease: 'power2.inOut' }}, 11.4);
tl.fromTo('#spOpenSpread1', {{ opacity: 0, scale: 0.92, y: 20 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.85, ease: 'power3.out' }}, 11.8);
tl.fromTo('#hn1_2', {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.55, ease: 'back.out' }}, 12.8);
cameraPush(12.0, 1.04, 8.5);

showHeadline('#hlBox1_2', 12.0, '#hl1_2');
hideHeadline('#hlBox1_2', 20.8);

// =========================================================================
// TRANSITION TO SCENE 2: BOTANICAL & CELESTIAL ANOMALIES (20.8s - 22.0s)
// =========================================================================
glideTo(20.8, -1080, 0.85);

// =========================================================================
// SHOT 2A: IMPOSSIBLE BOTANY & CLAW ROOTS (22.0s - 34.72s)
// =========================================================================
tl.to(['#scene2 .dossier-tag', '#scene2 .ghost-watermark'], {{ opacity: 1, duration: 0.6, ease: 'power2.out' }}, 21.5);
tl.fromTo('#spAlienFlower', {{ opacity: 0, y: 50, scale: 0.94 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.85, ease: 'power3.out' }}, 22.2);
tl.fromTo('#boxRoot', {{ opacity: 0, scale: 0.9 }}, {{ opacity: 1, scale: 1, duration: 0.60, ease: 'power2.out' }}, 23.2);
tl.fromTo('#pillBot1', {{ opacity: 0, y: 15 }}, {{ opacity: 1, y: 0, duration: 0.50, ease: 'power3.out' }}, 23.5);
tl.fromTo('#hn2_1', {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.50, ease: 'back.out' }}, 23.8);

// Focal Shift to Vascular Leaf & Magnifier at 27.0s
tl.fromTo('#spVascularLeaf', {{ opacity: 0, x: 40 }}, {{ opacity: 1, x: 0, duration: 0.70, ease: 'power3.out' }}, 27.2);
tl.fromTo('#spMagnifier', {{ opacity: 0, scale: 0.7, rotate: -15 }}, {{ opacity: 1, scale: 1, rotate: 0, duration: 0.65, ease: 'back.out(1.4)' }}, 27.8);
tl.fromTo('#cardTelemetry2', {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.55, ease: 'power3.out' }}, 28.5);

showHeadline('#hlBox2_1', 22.4, '#hl2_1');
hideHeadline('#hlBox2_1', 34.8);

// =========================================================================
// SHOT 2B: CELESTIAL STAR WHEELS & FLUID PIPES (35.5s - 46.2s)
// Sequential reveal: clean out botany specimens, bring in celestial dials
// =========================================================================
tl.to(['#spAlienFlower', '#boxRoot', '#spVascularLeaf', '#spMagnifier', '#pillBot1', '#hn2_1', '#cardTelemetry2'], {{ opacity: 0, duration: 0.5, ease: 'power2.inOut' }}, 34.8);

tl.fromTo('#spZodiac', {{ opacity: 0, y: 50 }}, {{ opacity: 1, y: 0, duration: 0.75, ease: 'power3.out' }}, 35.8);
tl.fromTo('#spTubes', {{ opacity: 0, y: 50 }}, {{ opacity: 1, y: 0, duration: 0.75, ease: 'power3.out' }}, 36.4);
tl.fromTo('#pillBot2', {{ opacity: 0, y: 15 }}, {{ opacity: 1, y: 0, duration: 0.50, ease: 'power3.out' }}, 36.8);
tl.fromTo('#hn2_2', {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.50, ease: 'back.out' }}, 37.2);

showHeadline('#hlBox2_2', 36.2, '#hl2_2');
hideHeadline('#hlBox2_2', 46.2);

// =========================================================================
// TRANSITION TO SCENE 3: RADIOCARBON FORENSICS (46.2s - 47.4s)
// =========================================================================
glideTo(46.2, -2160, 0.85);

// =========================================================================
// SHOT 3A: THE HOAX ACCUSATION (47.4s - 57.2s)
// =========================================================================
tl.to(['#scene3 .dossier-tag', '#scene3 .ghost-watermark'], {{ opacity: 1, duration: 0.6, ease: 'power2.out' }}, 46.8);
tl.fromTo('#hn3_1', {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.50, ease: 'back.out' }}, 47.8);
showHeadline('#hlBox3_1', 47.6, '#hl3_1');
hideHeadline('#hlBox3_1', 57.2);

// =========================================================================
// SHOT 3B: MICRO-SAMPLE EXTRACTION & AMS ACCELERATOR (57.8s - 69.5s)
// =========================================================================
tl.to('#hn3_1', {{ opacity: 0, duration: 0.4 }}, 57.5);
tl.fromTo('#spAmsCore', {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.85, ease: 'power3.out' }}, 58.0);
tl.fromTo('#spRuler', {{ opacity: 0, x: 40 }}, {{ opacity: 1, x: 0, duration: 0.70, ease: 'power3.out' }}, 58.6);
tl.fromTo('#pillAms1', {{ opacity: 0, y: 15 }}, {{ opacity: 1, y: 0, duration: 0.50, ease: 'power3.out' }}, 59.0);
showHeadline('#hlBox3_2', 58.4, '#hl3_2');
hideHeadline('#hlBox3_2', 69.0);

// =========================================================================
// SHOT 3C: SVG C-14 CALIBRATION & INDISPUTABLE DATING (69.8s - 81.8s)
// =========================================================================
tl.fromTo('#panelC14', {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.65, ease: 'power3.out' }}, 70.0);
// Draw Gaussian curve and reveal confidence band
tl.fromTo('#c14Curve', {{ strokeDashoffset: 1000 }}, {{ strokeDashoffset: 0, duration: 1.2, ease: 'power2.inOut' }}, 70.4);
tl.to('#c14Band', {{ opacity: 1, duration: 0.6, ease: 'power2.out' }}, 71.4);
tl.fromTo('#pillAms2', {{ opacity: 0, y: 15 }}, {{ opacity: 1, y: 0, duration: 0.50, ease: 'power3.out' }}, 71.6);
tl.fromTo('#cardTelemetry3', {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.55, ease: 'power3.out' }}, 72.0);
slamStamp('#stampDebunked', 73.0);
tl.fromTo('#hn3_2', {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.50, ease: 'back.out' }}, 73.6);

showHeadline('#hlBox3_3', 70.4, '#hl3_3');
hideHeadline('#hlBox3_3', 81.5);

// =========================================================================
// TRANSITION TO SCENE 4: MATHEMATICAL ARCHITECTURE & ZIPF'S LAW (81.5s - 82.8s)
// =========================================================================
glideTo(81.5, -3240, 0.90);

// =========================================================================
// SHOT 4A: SVG ZIPF'S LAW FREQUENCY MODEL (82.8s - 96.2s)
// =========================================================================
tl.to(['#scene4 .dossier-tag', '#scene4 .ghost-watermark'], {{ opacity: 1, duration: 0.6, ease: 'power2.out' }}, 82.2);
tl.fromTo('#panelZipf', {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.65, ease: 'power3.out' }}, 82.8);
tl.fromTo('#zipfVoynichCurve', {{ strokeDashoffset: 1000 }}, {{ strokeDashoffset: 0, duration: 1.4, ease: 'power2.inOut' }}, 83.2);
tl.fromTo('#pillZipf1', {{ opacity: 0, y: 15 }}, {{ opacity: 1, y: 0, duration: 0.50, ease: 'power3.out' }}, 83.8);
tl.fromTo('#hn4_1', {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.50, ease: 'back.out' }}, 84.5);
slamStamp('#stampZipf', 86.5);
tl.fromTo('#cardTelemetry4', {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.55, ease: 'power3.out' }}, 87.5);

showHeadline('#hlBox4_1', 83.0, '#hl4_1');
hideHeadline('#hlBox4_1', 96.0);

// =========================================================================
// SHOT 4B: MORPHOLOGY ANATOMY (96.8s - 109.8s)
// Sequential reveal: clean out graph, display alphabet specimen
// =========================================================================
tl.to(['#panelZipf', '#pillZipf1', '#hn4_1', '#stampZipf', '#cardTelemetry4'], {{ opacity: 0, duration: 0.5, ease: 'power2.inOut' }}, 96.2);

tl.fromTo('#spAlphabet', {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.75, ease: 'power3.out' }}, 96.8);
tl.fromTo('#pillZipf2', {{ opacity: 0, y: 15 }}, {{ opacity: 1, y: 0, duration: 0.50, ease: 'power3.out' }}, 97.2);
tl.fromTo('#hn4_2', {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.50, ease: 'back.out' }}, 97.8);

showHeadline('#hlBox4_2', 97.4, '#hl4_2');
hideHeadline('#hlBox4_2', 109.5);

// =========================================================================
// TRANSITION TO SCENE 5: MILITARY & AI CODEBREAKING (109.5s - 110.6s)
// =========================================================================
glideTo(109.5, -4320, 0.85);

// =========================================================================
// SHOT 5A: FRIEDMAN & WWII CODEBREAKERS (110.6s - 119.8s)
// =========================================================================
tl.to(['#scene5 .dossier-tag', '#scene5 .ghost-watermark'], {{ opacity: 1, duration: 0.6, ease: 'power2.out' }}, 110.2);
tl.fromTo('#spFriedman', {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.75, ease: 'power3.out' }}, 110.8);
tl.fromTo('#spNsaSeal', {{ opacity: 0, scale: 0.8, rotate: 10 }}, {{ opacity: 1, scale: 1, rotate: 0, duration: 0.70, ease: 'back.out(1.4)' }}, 111.4);
tl.fromTo('#pillCode1', {{ opacity: 0, y: 15 }}, {{ opacity: 1, y: 0, duration: 0.50, ease: 'power3.out' }}, 112.0);
tl.fromTo('#hn5_1', {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.50, ease: 'back.out' }}, 112.8);

// =========================================================================
// SHOT 5B: MODERN NEURAL NETWORKS & COLD CASE (119.8s - 124.8s)
// Sequential reveal: clean out Friedman, spotlight neural network
// =========================================================================
tl.to(['#spFriedman', '#spNsaSeal', '#pillCode1', '#hn5_1'], {{ opacity: 0, duration: 0.45, ease: 'power2.inOut' }}, 119.8);

tl.fromTo('#spNeuralNet', {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.75, ease: 'power3.out' }}, 120.2);
tl.fromTo('#pillCode2', {{ opacity: 0, y: 15 }}, {{ opacity: 1, y: 0, duration: 0.50, ease: 'power3.out' }}, 120.6);
tl.fromTo('#hn5_2', {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.50, ease: 'back.out' }}, 121.2);
slamStamp('#stampColdCase', 121.8);
tl.fromTo('#cardTelemetry5', {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.55, ease: 'power3.out' }}, 122.2);

showHeadline('#hlBox5_1', 110.8, '#hl5_1');
hideHeadline('#hlBox5_1', 124.6);

// =========================================================================
// TRANSITION TO SCENE 6: YALE BEINECKE VAULT & RESOLUTION (124.6s - 125.8s)
// =========================================================================
glideTo(124.6, -5400, 0.90);

// =========================================================================
// SHOT 6A: YALE RARE BOOK VAULT (125.8s - 139.2s)
// =========================================================================
tl.to(['#scene6 .dossier-tag', '#scene6 .ghost-watermark'], {{ opacity: 1, duration: 0.6, ease: 'power2.out' }}, 125.8);
tl.fromTo('#spBeineckeSeal', {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.65, ease: 'back.out' }}, 126.0);
tl.fromTo('#spArchiveBox', {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.70, ease: 'power3.out' }}, 126.6);
tl.fromTo('#spCallTag', {{ opacity: 0, x: 30 }}, {{ opacity: 1, x: 0, duration: 0.55, ease: 'power3.out' }}, 127.2);
tl.fromTo('#spFinalSpread', {{ opacity: 0, y: 60, scale: 0.94 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.90, ease: 'power3.out' }}, 127.8);
tl.fromTo('#cardTelemetry6', {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.55, ease: 'power3.out' }}, 129.0);
tl.fromTo('#hn6_1', {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.50, ease: 'back.out' }}, 129.8);

showHeadline('#hlBox6_1', 126.0, '#hl6_1');
hideHeadline('#hlBox6_1', 139.0);

// =========================================================================
// SHOT 6B: THE DEFINITIVE CASE UNRESOLVED & MOTIF LOOP (139.8s - 152.92s)
// Climax Rubber Stamp Slam & Quiet Holding Gravitas
// =========================================================================
showHeadline('#hlBox6_2', 140.2, '#hl6_2');
// Definitive Rubber Stamp Slam directly on vellum
tl.fromTo('#outroFinalStamp', {{ opacity: 0, scale: 2.4, rotate: -15 }}, {{ opacity: 1, scale: 1, rotate: -6, duration: 0.28, ease: 'power4.in' }}, 143.0);

// Gentle pull-back to wide vault at the conclusion (144.0s - 150.0s)
cameraPush(144.0, 0.97, 6.5);

/* Headless Puppeteer Seek Hook */
window.BANG_MOTION = {{
  ready: true,
  seekFrame: function(t) {{
    tl.pause(t, false);
    updateDynamicSubtitles(t);
  }},
  duration: DURATION
}};

/* Interactive Autoplay & Audio Sync */
const audio = $('#audioTrack');
let isPlaying = false;

function playVideo() {{
  tl.play(0);
  audio.currentTime = 0;
  audio.play().then(() => isPlaying = true).catch(() => {{}});
}}

window.addEventListener('click', () => {{
  if (!isPlaying) {{
    playVideo();
  }} else {{
    tl.paused(!tl.paused());
    if (tl.paused()) audio.pause(); else audio.play();
  }}
}});

gsap.ticker.add(() => {{
  const t = tl.time();
  updateDynamicSubtitles(t);
  if (isPlaying && !tl.paused()) {{
    if (Math.abs(audio.currentTime - t) > 0.15) {{
      audio.currentTime = t;
    }}
  }}
}});
</script>
</body>
</html>
'''

    out_file = "index_ep8.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[+] Successfully generated upgraded {out_file} ({len(html_content)} bytes)")

if __name__ == "__main__":
    main()
