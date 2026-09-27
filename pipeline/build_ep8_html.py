#!/usr/bin/env python3
"""build_ep8_html.py — Generate high-end Vox Studio Visual Journalism HTML for Episode 8.
"""
import json
import os

def main():
    aligned_path = "assets/episode8_voynich_manuscript/audio/voynich_words_aligned.json"
    with open(aligned_path, "r", encoding="utf-8") as f:
        aligned_data = json.load(f)

    # Prepare compact words array: [{w: "word", s: start_t, e: end_t, b: beat_idx}]
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
<title>The Voynich Manuscript — Vox Visual Journalism Studio</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=IBM+Plex+Mono:ital,wght@0,500;0,600;0,700;1,500&family=Caveat:wght@700&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #07090E;
  --panel: #0E131E;
  --ink: #FFFFFF;
  --ink-dim: #94A3B8;
  --yel: #FFDE38;
  --red: #E11D48;
  --cyan: #38BDF8;
  --green: #22C55E;
  --border: rgba(255, 255, 255, 0.14);
  --shadow: 0 24px 60px rgba(0, 0, 0, 0.85);
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; -webkit-font-smoothing: antialiased; }}
html, body {{
  width: 100%; height: 100%;
  background: #040508;
  overflow: hidden;
  font-family: "Barlow Condensed", system-ui, sans-serif;
  color: var(--ink);
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
  box-shadow: 0 0 120px rgba(0, 0, 0, 0.98);
}}

/* 35mm Archival Film Grain */
.grain-overlay {{
  position: absolute; inset: 0;
  pointer-events: none;
  opacity: 0.14;
  mix-blend-mode: overlay;
  z-index: 50;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.82' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='240' height='240' filter='url(%23n)'/%3E%3C/svg%3E");
}}

/* Vignette */
.vignette {{
  position: absolute; inset: 0;
  pointer-events: none;
  background: radial-gradient(circle at 50% 50%, transparent 50%, rgba(4, 5, 8, 0.75) 100%);
  z-index: 51;
}}

/* Optical Transit Streak */
#motionStreak {{
  position: absolute; inset: 0;
  background: linear-gradient(90deg, transparent 0%, rgba(255, 222, 56, 0.28) 50%, transparent 100%);
  transform: translateX(-100%);
  pointer-events: none;
  z-index: 55;
  opacity: 0;
}}

/* Persistent Top Header Runner */
#voxRunner {{
  position: absolute;
  top: 70px; left: 60px; right: 60px;
  height: 68px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(12, 16, 24, 0.94);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  padding: 0 24px;
  border-radius: 8px;
  border: 1px solid var(--border);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.60);
  font-family: "IBM Plex Mono", monospace;
  font-size: 20px;
  font-weight: 500;
  letter-spacing: 0.08em;
  color: var(--ink-dim);
  z-index: 60;
}}
#voxRunner .badge {{
  background: var(--yel);
  color: #0A0D14;
  font-weight: 800;
  padding: 4px 14px;
  border-radius: 4px;
  font-size: 17px;
  letter-spacing: 0.05em;
}}
#voxRunner .tag {{
  color: #FFFFFF;
  font-weight: 600;
}}

/* 6-Scene Continuous Horizontal Runway */
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

/* Full Bleed Background Documents */
.scene-bg-doc {{
  position: absolute;
  inset: 0;
  width: 1080px; height: 1920px;
  object-fit: cover;
  filter: brightness(0.62) contrast(1.18);
  transform: scale(1.03);
  transform-origin: center center;
}}

/* Archival Source Tag */
.source-tag {{
  position: absolute;
  font-family: "IBM Plex Mono", monospace;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.12em;
  color: var(--yel);
  background: rgba(10, 14, 22, 0.92);
  padding: 6px 14px;
  border-left: 4px solid var(--yel);
  border-radius: 2px;
  z-index: 25;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.6);
  text-transform: uppercase;
}}
.source-tag.red-accent {{
  color: var(--red);
  border-left-color: var(--red);
}}
.source-tag.cyan-accent {{
  color: var(--cyan);
  border-left-color: var(--cyan);
}}

/* Ghost Watermark Numbers */
.ghost {{
  position: absolute;
  font-weight: 900;
  font-size: 210px;
  line-height: 0.85;
  letter-spacing: -0.04em;
  color: transparent;
  -webkit-text-stroke: 3px rgba(255, 255, 255, 0.08);
  text-align: center;
  z-index: 5;
  pointer-events: none;
  white-space: nowrap;
}}

/* Specimen Cutout Sprites */
.specimen-sprite {{
  position: absolute;
  filter: drop-shadow(0 20px 48px rgba(0, 0, 0, 0.88));
  will-change: transform;
  z-index: 20;
}}
.specimen-sprite img {{
  display: block;
  width: 100%; height: 100%;
  object-fit: contain;
}}

/* Specimen Details Label Tag */
.spec-tag {{
  position: absolute;
  padding: 6px 14px;
  background: rgba(10, 14, 22, 0.90);
  border: 1px solid rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  color: #F8FAFC;
  font-family: "IBM Plex Mono", monospace;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.12em;
  border-radius: 4px;
  z-index: 26;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}}

/* Handwritten Editorial Notes */
.hand-note {{
  position: absolute;
  font-family: "Caveat", cursive;
  font-size: 46px;
  font-weight: 700;
  line-height: 1.1;
  color: var(--yel);
  filter: drop-shadow(0 3px 8px rgba(0, 0, 0, 0.9));
  z-index: 32;
  white-space: nowrap;
}}
.hand-note.red {{ color: var(--red); }}
.hand-note.cyan {{ color: var(--cyan); }}

/* Telemetry Data Counter Card */
.telemetry-card {{
  position: absolute;
  background: rgba(14, 19, 28, 0.96);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 20px 26px;
  box-shadow: var(--shadow);
  z-index: 24;
}}
.telemetry-card .t-label {{
  font-family: "IBM Plex Mono", monospace;
  font-size: 15px;
  font-weight: 600;
  color: var(--ink-dim);
  letter-spacing: 0.1em;
  margin-bottom: 6px;
  text-transform: uppercase;
}}
.telemetry-card .t-value {{
  font-family: "Barlow Condensed", sans-serif;
  font-size: 72px;
  font-weight: 900;
  color: var(--yel);
  line-height: 0.95;
}}
.telemetry-card .t-value.red {{ color: var(--red); }}
.telemetry-card .t-value.cyan {{ color: var(--cyan); }}
.telemetry-card .t-value.green {{ color: var(--green); }}
.telemetry-card .t-unit {{
  font-family: "IBM Plex Mono", monospace;
  font-size: 20px;
  font-weight: 600;
  color: var(--ink-dim);
  margin-left: 8px;
}}

/* Rubber Stamps */
.rubber-stamp {{
  position: absolute;
  padding: 8px 24px;
  border: 5px solid var(--red);
  border-radius: 8px;
  color: var(--red);
  font-family: "Barlow Condensed", sans-serif;
  font-weight: 900;
  font-size: 38px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  background: rgba(10, 14, 22, 0.90);
  box-shadow: 0 10px 30px rgba(225, 29, 72, 0.35);
  z-index: 35;
  white-space: nowrap;
  opacity: 0;
}}
.rubber-stamp.green {{
  border-color: var(--green);
  color: var(--green);
  box-shadow: 0 10px 30px rgba(34, 197, 94, 0.35);
}}
.rubber-stamp.yellow {{
  border-color: var(--yel);
  color: var(--yel);
  box-shadow: 0 10px 30px rgba(255, 222, 56, 0.35);
}}

/* Vox Punchy Editorial Headline Box (No Wall of Text!) */
.vox-headline-box {{
  position: absolute;
  left: 60px; right: 60px;
  top: 1300px;
  background: rgba(10, 14, 22, 0.94);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border-left: 6px solid var(--yel);
  padding: 22px 28px;
  border-radius: 8px;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.85);
  z-index: 40;
  opacity: 0;
}}
.vox-headline-box.red-border {{ border-left-color: var(--red); }}
.vox-headline-box.cyan-border {{ border-left-color: var(--cyan); }}
.vox-headline-box .h-tag {{
  font-family: "IBM Plex Mono", monospace;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0.12em;
  color: var(--yel);
  margin-bottom: 6px;
  text-transform: uppercase;
}}
.vox-headline-box.red-border .h-tag {{ color: var(--red); }}
.vox-headline-box.cyan-border .h-tag {{ color: var(--cyan); }}
.vox-headline-box .h-text {{
  font-size: 52px;
  font-weight: 800;
  line-height: 1.15;
  letter-spacing: -0.01em;
  color: #FFFFFF;
}}

/* Sweeping Yellow / Red Highlighters */
.hl {{
  position: relative;
  display: inline-block;
  color: inherit;
  padding: 0 8px;
  margin: 0 2px;
  white-space: nowrap;
  vertical-align: baseline;
}}
.hl i {{
  position: absolute;
  left: 0; right: 0; top: 10%; bottom: 6%;
  background: var(--yel);
  transform: scaleX(0);
  transform-origin: 0 50%;
  z-index: -1;
  border-radius: 4px;
  box-shadow: 0 2px 10px rgba(255, 222, 56, 0.45);
}}
.hl.r i {{
  background: var(--red);
  box-shadow: 0 2px 10px rgba(225, 29, 72, 0.50);
}}
.hl.c i {{
  background: var(--cyan);
  box-shadow: 0 2px 10px rgba(56, 189, 248, 0.50);
}}

/* Dynamic Spoken TikTok Caption Pill (Compact & Precise) */
#captionPillContainer {{
  position: absolute;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%);
  width: 900px;
  display: flex;
  justify-content: center;
  z-index: 65;
  pointer-events: none;
}}
#captionPill {{
  background: rgba(10, 14, 22, 0.94);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.16);
  padding: 14px 32px;
  border-radius: 999px;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.85);
  font-family: "Barlow Condensed", system-ui, sans-serif;
  font-size: 42px;
  font-weight: 700;
  letter-spacing: 0.02em;
  color: #FFFFFF;
  text-align: center;
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 10px;
}}
.sub-word {{
  display: inline-block;
  color: #E2E8F0;
  transition: color 0.1s ease, transform 0.1s ease;
}}
.sub-word.active {{
  color: var(--yel);
  font-weight: 900;
  transform: scale(1.12);
  text-shadow: 0 0 20px rgba(255, 222, 56, 0.85);
}}
.sub-word.past {{
  color: #94A3B8;
}}

/* Outro Resolution Rubber Stamp */
#outroBigStamp {{
  position: absolute;
  top: 760px; left: 50%;
  width: 880px; height: 320px;
  transform: translate(-50%, 0) rotate(-6deg) scale(2.5);
  opacity: 0;
  z-index: 48;
  filter: drop-shadow(0 20px 50px rgba(225, 29, 72, 0.85));
}}

/* Intro Confidential Casefile Folder Card */
#introOverlay {{
  position: absolute; inset: 0;
  background: rgba(6, 8, 12, 0.92);
  z-index: 70;
  display: flex;
  justify-content: center;
  align-items: center;
}}
#introFolderCard {{
  width: 920px; height: 1360px;
  position: relative;
  background: #EAE3D2;
  border-radius: 12px;
  box-shadow: 0 24px 70px rgba(0, 0, 0, 0.85);
  overflow: hidden;
  border: 2px solid #C8BC9F;
}}
#introFolderCard .folder-tab {{
  position: absolute;
  top: 0; left: 0; right: 0; height: 90px;
  background: #DDD4C0;
  border-bottom: 2px solid #C8BC9F;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  font-family: "IBM Plex Mono", monospace;
  font-size: 18px;
  font-weight: 700;
  color: #554D3E;
  letter-spacing: 0.12em;
}}
#introFolderCard .folder-body {{
  padding: 130px 60px 60px 60px;
  display: flex;
  flex-direction: column;
  height: 100%;
  justify-content: space-between;
}}
#introFolderCard .folder-badge {{
  font-family: "IBM Plex Mono", monospace;
  font-size: 19px;
  color: var(--red);
  font-weight: 700;
  letter-spacing: 0.15em;
  margin-bottom: 20px;
  text-transform: uppercase;
}}
#introFolderCard .folder-title {{
  font-family: "Barlow Condensed", sans-serif;
  font-size: 84px;
  font-weight: 900;
  line-height: 0.95;
  color: #1A1814;
  letter-spacing: -0.02em;
}}
#introFolderCard .folder-meta {{
  margin-top: 36px;
  font-family: "IBM Plex Mono", monospace;
  font-size: 23px;
  color: #4A4437;
  line-height: 1.5;
}}
#introFolderCard .folder-meta strong {{
  color: #1A1814;
}}
#introTapeBar {{
  width: 100%; height: 130px;
  background: var(--red);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(225, 29, 72, 0.40);
  transform-origin: center;
}}
#introTapeBar span {{
  font-family: "Barlow Condensed", sans-serif;
  font-weight: 900;
  font-size: 46px;
  letter-spacing: 0.12em;
  color: #FFFFFF;
  text-transform: uppercase;
}}
</style>
</head>
<body>

<div id="stage">
  <div class="grain-overlay"></div>
  <div class="vignette"></div>
  <div id="motionStreak"></div>

  <!-- Intro Casefile Folder Overlay -->
  <div id="introOverlay">
    <div id="introFolderCard">
      <div class="folder-tab">
        <span>TOP SECRET // INVESTIGATION DOSSIER</span>
        <span>YALE BEINECKE ARCHIVE</span>
      </div>
      <div class="folder-body">
        <div>
          <div class="folder-badge">EVIDENCE DOSSIER #08 · UNRESOLVED HISTORICAL CIPHER</div>
          <div class="folder-title">
            THE 600-YEAR-OLD CODE THAT EVEN MODERN AI CANNOT CRACK
          </div>
          <div class="folder-meta">
            <strong>Artifact:</strong> Yale Beinecke Rare Book MS 408<br>
            <strong>Carbon Chronology:</strong> 1404–1438 AD (Univ. of Arizona)<br>
            <strong>Classification:</strong> 100% Undeciphered Historical Enigma
          </div>
        </div>
        <div id="introTapeBar">
          <span>UNSEALING RESTRICTED MANUSCRIPT ARCHIVE</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Persistent Header Runner -->
  <div id="voxRunner">
    <div style="display: flex; align-items: center; gap: 14px;">
      <span class="badge">VOX INVESTIGATION</span>
      <span class="tag" id="runnerDossier">DOSSIER #08: THE VOYNICH CIPHER</span>
    </div>
    <div id="runnerTimeline" style="color: var(--ink-dim); font-size: 18px;">1404 · BEINECKE MS 408</div>
  </div>

  <!-- 6-Scene Runway Container -->
  <div id="runway">

    <!-- ========================================================================= -->
    <!-- SCENE 1: THE MONASTERY DISCOVERY (X = 0)                                 -->
    <!-- ========================================================================= -->
    <div class="scene-dossier" id="scene1">
      <img class="scene-bg-doc" src="assets/episode8_voynich_manuscript/images/bg_monastery_library_vault.png" alt="Jesuit Vault">
      <div class="source-tag" style="top: 175px; left: 70px;">JESUIT ARCHIVE // VILLA MONDRAGONE · 1912</div>
      <div class="ghost" style="top: 180px; left: 70px; width: 940px;">1912</div>

      <!-- Closed Vellum Book Hero Cutout -->
      <div class="specimen-sprite" id="spBook" style="top: 270px; left: 140px; width: 800px; height: 480px;">
        <img src="assets/episode8_voynich_manuscript/images/sprite_voynich_closed_book.png" alt="Voynich Closed Book">
      </div>

      <!-- Red Wax Seal Broken -->
      <div class="specimen-sprite" id="spWax" style="top: 240px; right: 90px; width: 220px; height: 220px;">
        <img src="assets/episode8_voynich_manuscript/images/sprite_red_wax_seal_broken.png" alt="Broken Wax Seal">
      </div>

      <!-- Quill & Inkwell -->
      <div class="specimen-sprite" id="spQuill" style="top: 750px; left: 90px; width: 360px; height: 340px;">
        <img src="assets/episode8_voynich_manuscript/images/sprite_quill_ink_well.png" alt="Quill and Ink">
      </div>

      <!-- Open Spread Teaser -->
      <div class="specimen-sprite" id="spOpenSpread1" style="top: 760px; right: 90px; width: 480px; height: 320px;">
        <img src="assets/episode8_voynich_manuscript/images/sprite_voynich_open_spread.png" alt="Open Folio Spread">
      </div>

      <div class="spec-tag" style="top: 700px; left: 110px;">BINDING: AGED CALFSKIN VELLUM</div>
      <div class="spec-tag" style="top: 700px; right: 110px;">VOLUME: 240 FOLIO PAGES</div>

      <!-- Handwritten Notes -->
      <div class="hand-note" id="hn1_1" style="top: 650px; left: 140px; transform: rotate(-3deg);">
        Found inside a Jesuit wooden chest!
      </div>
      <div class="hand-note cyan" id="hn1_2" style="top: 1110px; right: 110px; transform: rotate(2deg);">
        Unbroken script never seen before!
      </div>

      <!-- Telemetry Card -->
      <div class="telemetry-card" id="cardTelemetry1" style="top: 1120px; left: 70px; width: 440px;">
        <div class="t-label">SURVIVING FOLIOS</div>
        <div style="display: flex; align-items: baseline;">
          <span class="t-value" id="valFolios">240</span>
          <span class="t-unit">PAGES</span>
        </div>
      </div>

      <!-- Rubber Stamp -->
      <div class="rubber-stamp" id="stampArtifact" style="top: 1130px; right: 90px; transform: rotate(-8deg);">
        AUTHENTIC ARTIFACT
      </div>

      <!-- Vox Headlines (Swapping cleanly without text clutter) -->
      <div class="vox-headline-box" id="hlBox1_1">
        <div class="h-tag">ROME, ITALY · 1912 DISCOVERY</div>
        <div class="h-text">
          Antique book dealer Wilfrid Voynich uncovered an <span class="hl" id="hl1_1"><i></i>unbreakable 600-year enigma.</span>
        </div>
      </div>

      <div class="vox-headline-box cyan-border" id="hlBox1_2">
        <div class="h-tag">THE UNKNOWN SCRIPT</div>
        <div class="h-text">
          240 illustrated folios written in a <span class="hl c" id="hl1_2"><i></i>completely unknown language.</span>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- SCENE 2: IMPOSSIBLE BOTANY & COSMOLOGY (X = -1080)                        -->
    <!-- ========================================================================= -->
    <div class="scene-dossier" id="scene2">
      <img class="scene-bg-doc" src="assets/episode8_voynich_manuscript/images/bg_botanical_herbal_folio.png" alt="Botanical Folio">
      <div class="source-tag" style="top: 175px; left: 70px;">BOTANICAL SECTION // UNCLASSIFIED FLORA</div>
      <div class="ghost" style="top: 180px; left: 70px; width: 940px;">FOLIO 42</div>

      <!-- Alien Flower Cutout -->
      <div class="specimen-sprite" id="spAlienFlower" style="top: 260px; left: 100px; width: 480px; height: 460px;">
        <img src="assets/episode8_voynich_manuscript/images/sprite_alien_flower_cutout.png" alt="Impossible Flower">
      </div>

      <!-- Vascular Leaf Cutout -->
      <div class="specimen-sprite" id="spVascularLeaf" style="top: 280px; right: 90px; width: 380px; height: 420px;">
        <img src="assets/episode8_voynich_manuscript/images/sprite_alien_vascular_leaf.png" alt="Alien Leaf Structure">
      </div>

      <!-- Magnifying Glass -->
      <div class="specimen-sprite" id="spMagnifier" style="top: 340px; right: 130px; width: 280px; height: 280px;">
        <img src="assets/episode8_voynich_manuscript/images/sprite_magnifying_glass.png" alt="Magnifying Glass">
      </div>

      <!-- Zodiac Star Wheel -->
      <div class="specimen-sprite" id="spZodiac" style="top: 750px; left: 90px; width: 440px; height: 360px;">
        <img src="assets/episode8_voynich_manuscript/images/sprite_zodiac_star_wheel.png" alt="Zodiac Wheel">
      </div>

      <!-- Balneological Tubes -->
      <div class="specimen-sprite" id="spTubes" style="top: 750px; right: 90px; width: 440px; height: 360px;">
        <img src="assets/episode8_voynich_manuscript/images/sprite_balneological_tubes.png" alt="Organic Plumbing">
      </div>

      <div class="spec-tag" style="top: 700px; left: 100px;">ROOT STRUCTURE: PREDATORY CLAWS</div>
      <div class="spec-tag" style="top: 700px; right: 100px;">ZODIAC: UNMAPPED CONSTELLATIONS</div>

      <!-- Handwritten Notes -->
      <div class="hand-note" id="hn2_1" style="top: 650px; left: 140px; transform: rotate(-4deg);">
        Roots shaped like animal claws!
      </div>
      <div class="hand-note cyan" id="hn2_2" style="top: 1110px; right: 110px; transform: rotate(2deg);">
        Organic plumbing labyrinth!
      </div>

      <!-- Telemetry Card -->
      <div class="telemetry-card" id="cardTelemetry2" style="top: 1120px; left: 70px; width: 460px;">
        <div class="t-label">KNOWN EARTH SPECIES MATCH</div>
        <div style="display: flex; align-items: baseline;">
          <span class="t-value red" id="valPlantMatch">0%</span>
          <span class="t-unit">OF 300+ TESTED</span>
        </div>
      </div>

      <!-- Vox Headlines -->
      <div class="vox-headline-box" id="hlBox2_1">
        <div class="h-tag">IMPOSSIBLE BOTANY</div>
        <div class="h-text">
          Folios depict <span class="hl" id="hl2_1"><i></i>bizarre botanical hybrids</span> that do not exist on Earth.
        </div>
      </div>

      <div class="vox-headline-box cyan-border" id="hlBox2_2">
        <div class="h-tag">COSMOLOGICAL WHEELS</div>
        <div class="h-text">
          Cosmological star wheels and <span class="hl c" id="hl2_2"><i></i>unmapped zodiac constellations.</span>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- SCENE 3: THE HOAX ACCUSATION & ARIZONA DATING (X = -2160)                 -->
    <!-- ========================================================================= -->
    <div class="scene-dossier" id="scene3">
      <img class="scene-bg-doc" src="assets/episode8_voynich_manuscript/images/bg_accelerator_mass_spectrometry.png" alt="AMS Laboratory">
      <div class="source-tag" style="top: 175px; left: 70px;">LABORATORY ANALYSIS // UNIV. OF ARIZONA AMS</div>
      <div class="ghost" style="top: 180px; left: 70px; width: 940px;">1404 AD</div>

      <!-- Arizona AMS Core Cutout -->
      <div class="specimen-sprite" id="spAmsCore" style="top: 260px; left: 90px; width: 500px; height: 460px;">
        <img src="assets/episode8_voynich_manuscript/images/sprite_arizona_ams_core.png" alt="Arizona AMS Core">
      </div>

      <!-- Vintage Ruler Scale -->
      <div class="specimen-sprite" id="spRuler" style="top: 310px; right: 90px; width: 380px; height: 380px;">
        <img src="assets/episode8_voynich_manuscript/images/sprite_vintage_ruler_scale.png" alt="Archival Ruler">
      </div>

      <!-- Carbon Dating Graph -->
      <div class="specimen-sprite" id="spCarbonGraph" style="top: 750px; left: 90px; width: 900px; height: 350px;">
        <img src="assets/episode8_voynich_manuscript/images/sprite_carbon_dating_graph.png" alt="Carbon Dating Graph">
      </div>

      <div class="spec-tag" style="top: 700px; left: 110px;">TEST: ACCELERATOR MASS SPECTROMETRY</div>
      <div class="spec-tag" style="top: 700px; right: 110px;">CONFIDENCE: 95% INTERVAL</div>

      <!-- Handwritten Notes -->
      <div class="hand-note red" id="hn3_1" style="top: 650px; left: 140px; transform: rotate(-3deg);">
        Skeptics claimed Renaissance forgery!
      </div>
      <div class="hand-note" id="hn3_2" style="top: 1110px; right: 110px; transform: rotate(2deg);">
        Genuinely 600 years old!
      </div>

      <!-- Telemetry Card -->
      <div class="telemetry-card" id="cardTelemetry3" style="top: 1120px; left: 70px; width: 480px;">
        <div class="t-label">CALIBRATED CARBON DATE</div>
        <div style="display: flex; align-items: baseline;">
          <span class="t-value" id="valCarbonDate">1404</span>
          <span class="t-unit">– 1438 AD</span>
        </div>
      </div>

      <!-- Rubber Stamp: Hoax Debunked -->
      <div class="rubber-stamp green" id="stampDebunked" style="top: 1130px; right: 80px; transform: rotate(6deg);">
        HOAX DEBUNKED
      </div>

      <!-- Vox Headlines -->
      <div class="vox-headline-box red-border" id="hlBox3_1">
        <div class="h-tag">THE HOAX THEORY</div>
        <div class="h-text">
          For nearly a century, skeptics called it an <span class="hl r" id="hl3_1"><i></i>elaborate Renaissance forgery.</span>
        </div>
      </div>

      <div class="vox-headline-box" id="hlBox3_2">
        <div class="h-tag">PHYSICS DISPROVES THE SKEPTICS</div>
        <div class="h-text">
          Physicists tested parchment samples using <span class="hl" id="hl3_2"><i></i>accelerator mass spectrometry.</span>
        </div>
      </div>

      <div class="vox-headline-box" id="hlBox3_3">
        <div class="h-tag">SCIENTIFIC VERDICT</div>
        <div class="h-text">
          The parchment was harvested <span class="hl" id="hl3_3"><i></i>between 1404 and 1438 AD.</span>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- SCENE 4: ZIPF'S LAW & LINGUISTIC ARCHITECTURE (X = -3240)                 -->
    <!-- ========================================================================= -->
    <div class="scene-dossier" id="scene4">
      <img class="scene-bg-doc" src="assets/episode8_voynich_manuscript/images/bg_ancient_vellum_parchment.png" alt="Ancient Parchment">
      <div class="source-tag" style="top: 175px; left: 70px;">CRYPTANALYSIS // MATHEMATICAL FREQUENCY MODEL</div>
      <div class="ghost" style="top: 180px; left: 70px; width: 940px;">ZIPF</div>

      <!-- Zipf's Law Curve Cutout -->
      <div class="specimen-sprite" id="spZipfCurve" style="top: 260px; left: 90px; width: 900px; height: 440px;">
        <img src="assets/episode8_voynich_manuscript/images/sprite_zipf_law_curve.png" alt="Zipf's Law Curve">
      </div>

      <!-- Alphabet Sample Cutout -->
      <div class="specimen-sprite" id="spAlphabet" style="top: 740px; left: 90px; width: 900px; height: 360px;">
        <img src="assets/episode8_voynich_manuscript/images/sprite_voynich_alphabet_sample.png" alt="Voynich Alphabet">
      </div>

      <div class="spec-tag" style="top: 690px; left: 110px;">FREQUENCY SLOPE: -1.02</div>
      <div class="spec-tag" style="top: 690px; right: 110px;">ENTROPY: NATURAL LANGUAGE PROFILE</div>

      <!-- Handwritten Notes -->
      <div class="hand-note" id="hn4_1" style="top: 640px; left: 140px; transform: rotate(-3deg);">
        Matches genuine human speech!
      </div>
      <div class="hand-note cyan" id="hn4_2" style="top: 1110px; right: 110px; transform: rotate(2deg);">
        Prefixes, roots, and suffixes!
      </div>

      <!-- Telemetry Card -->
      <div class="telemetry-card" id="cardTelemetry4" style="top: 1120px; left: 70px; width: 440px;">
        <div class="t-label">TOTAL CIPHER GLYPHS</div>
        <div style="display: flex; align-items: baseline;">
          <span class="t-value" id="valGlyphs">170,000</span>
          <span class="t-unit">SIGNS</span>
        </div>
      </div>

      <!-- Rubber Stamp: Zipf Confirmed -->
      <div class="rubber-stamp yellow" id="stampZipf" style="top: 1130px; right: 80px; transform: rotate(-5deg);">
        ZIPF'S LAW CONFIRMED
      </div>

      <!-- Vox Headlines -->
      <div class="vox-headline-box" id="hlBox4_1">
        <div class="h-tag">MATHEMATICAL PROOF</div>
        <div class="h-text">
          Statistical analysis proved the cipher strictly obeys <span class="hl" id="hl4_1"><i></i>Zipf's Law.</span>
        </div>
      </div>

      <div class="vox-headline-box cyan-border" id="hlBox4_2">
        <div class="h-tag">LINGUISTIC ARCHITECTURE</div>
        <div class="h-text">
          A rigorous grammar of prefixes and roots — <span class="hl c" id="hl4_2"><i></i>not random medieval noise.</span>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- SCENE 5: MILITARY CRYPTOGRAPHY & MODERN AI (X = -4320)                    -->
    <!-- ========================================================================= -->
    <div class="scene-dossier" id="scene5">
      <img class="scene-bg-doc" src="assets/episode8_voynich_manuscript/images/bg_ancient_vellum_parchment.png" alt="Ancient Parchment">
      <div class="source-tag red-accent" style="top: 175px; left: 70px;">MILITARY CRYPTANALYSIS // NSA & AI LABS</div>
      <div class="ghost" style="top: 180px; left: 70px; width: 940px;">NSA / AI</div>

      <!-- William Friedman Portrait -->
      <div class="specimen-sprite" id="spFriedman" style="top: 260px; left: 100px; width: 420px; height: 440px;">
        <img src="assets/episode8_voynich_manuscript/images/sprite_william_friedman_portrait.png" alt="William Friedman">
      </div>

      <!-- NSA Cryptanalysis Seal -->
      <div class="specimen-sprite" id="spNsaSeal" style="top: 280px; right: 100px; width: 400px; height: 400px;">
        <img src="assets/episode8_voynich_manuscript/images/sprite_nsa_cryptanalysis_seal.png" alt="NSA Cryptanalysis Seal">
      </div>

      <!-- Neural Network Nodes -->
      <div class="specimen-sprite" id="spNeuralNet" style="top: 740px; left: 90px; width: 900px; height: 360px;">
        <img src="assets/episode8_voynich_manuscript/images/sprite_neural_network_nodes.png" alt="Neural Network Nodes">
      </div>

      <div class="spec-tag" style="top: 690px; left: 110px;">WWII CODEBREAKERS: DEFEATED</div>
      <div class="spec-tag" style="top: 690px; right: 110px;">NEURAL NETWORKS: ZERO SUCCESS</div>

      <!-- Handwritten Notes -->
      <div class="hand-note red" id="hn5_1" style="top: 640px; left: 140px; transform: rotate(-3deg);">
        Friedman studied it for 30 years!
      </div>
      <div class="hand-note cyan" id="hn5_2" style="top: 1110px; right: 110px; transform: rotate(2deg);">
        Even modern AI hit a wall!
      </div>

      <!-- Telemetry Card -->
      <div class="telemetry-card" id="cardTelemetry5" style="top: 1120px; left: 70px; width: 480px;">
        <div class="t-label">SOLVED ENCRYPTION KEYS</div>
        <div style="display: flex; align-items: baseline;">
          <span class="t-value red" id="valSolvedKeys">0</span>
          <span class="t-unit">KEYS FOUND</span>
        </div>
      </div>

      <!-- Rubber Stamp: Classified Cold Case -->
      <div class="rubber-stamp" id="stampColdCase" style="top: 1130px; right: 80px; transform: rotate(-6deg);">
        CLASSIFIED COLD CASE
      </div>

      <!-- Vox Headlines -->
      <div class="vox-headline-box" id="hlBox5_1">
        <div class="h-tag">THE CODEBREAKER FAILURE</div>
        <div class="h-text">
          US military cryptanalysts and <span class="hl" id="hl5_1"><i></i>modern neural networks</span> both hit a wall.
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- SCENE 6: YALE BEINECKE VAULT & RESOLUTION (X = -5400)                    -->
    <!-- ========================================================================= -->
    <div class="scene-dossier" id="scene6">
      <img class="scene-bg-doc" src="assets/episode8_voynich_manuscript/images/bg_beinecke_rare_book_vault.png" alt="Beinecke Rare Book Vault">
      <div class="source-tag" style="top: 175px; left: 70px;">YALE ARCHIVE // BEINECKE RARE BOOK VAULT</div>
      <div class="ghost" style="top: 180px; left: 70px; width: 940px;">UNSOLVED</div>

      <!-- Beinecke Library Seal -->
      <div class="specimen-sprite" id="spBeineckeSeal" style="top: 240px; left: 100px; width: 240px; height: 240px;">
        <img src="assets/episode8_voynich_manuscript/images/sprite_beinecke_library_seal.png" alt="Beinecke Seal">
      </div>

      <!-- Cardboard Archival Box -->
      <div class="specimen-sprite" id="spArchiveBox" style="top: 230px; right: 100px; width: 340px; height: 280px;">
        <img src="assets/episode8_voynich_manuscript/images/sprite_cardboard_archival_box.png" alt="Archival Box">
      </div>

      <!-- Call Number Tag -->
      <div class="specimen-sprite" id="spCallTag" style="top: 480px; right: 120px; width: 300px; height: 90px;">
        <img src="assets/episode8_voynich_manuscript/images/sprite_ms408_callnumber_tag.png" alt="MS 408 Tag">
      </div>

      <!-- Open Voynich Spread Hero -->
      <div class="specimen-sprite" id="spFinalSpread" style="top: 550px; left: 80px; width: 920px; height: 580px;">
        <img src="assets/episode8_voynich_manuscript/images/sprite_voynich_open_spread.png" alt="Voynich Open Spread">
      </div>

      <!-- Outro Rubber Stamp Slammed on Folios -->
      <div id="outroBigStamp">
        <img src="assets/episode8_voynich_manuscript/images/sprite_stamp_case_unresolved.png" alt="Case Unresolved Stamp" style="width: 100%; height: 100%; object-fit: contain;">
      </div>

      <!-- Handwritten Note -->
      <div class="hand-note" id="hn6_1" style="top: 1060px; left: 90px; transform: rotate(-2deg);">
        Vault Shelf MS 408 — Unbroken.
      </div>

      <!-- Telemetry Card -->
      <div class="telemetry-card" id="cardTelemetry6" style="top: 1120px; right: 80px; width: 440px;">
        <div class="t-label">DECIPHERED WORDS</div>
        <div style="display: flex; align-items: baseline;">
          <span class="t-value red" id="valDeciphered">0</span>
          <span class="t-unit">TRANSLATED</span>
        </div>
      </div>

      <!-- Vox Headlines -->
      <div class="vox-headline-box" id="hlBox6_1">
        <div class="h-tag">THE YALE ARCHIVE</div>
        <div class="h-text">
          Locked in Yale's rare book vault — <span class="hl" id="hl6_1"><i></i>a code that has defeated every mind.</span>
        </div>
      </div>

      <div class="vox-headline-box red-border" id="hlBox6_2">
        <div class="h-tag">FINAL VERDICT</div>
        <div class="h-text">
          Six centuries later, the Voynich code remains <span class="hl r" id="hl6_2"><i></i>entirely unsolved.</span>
        </div>
      </div>
    </div>

  </div> <!-- /#runway -->

  <!-- Dynamic Spoken TikTok Caption Pill (Compact & Precise) -->
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

/* Group Aligned Words into 3-5 Word Phrase Chunks */
const CHUNKS = [];
let curChunk = [];
let curChars = 0;
for (const w of ALIGNED_WORDS) {{
  curChunk.push(w);
  curChars += w.w.length + 1;
  const isPunc = /[.!?]$/.test(w.w);
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
  // Find current chunk
  const chunk = CHUNKS.find(c => t >= c.start - 0.05 && t <= c.end + 0.35);
  if (!chunk) {{
    // If between beats, hide or dim
    captionPill.style.opacity = '0';
    return;
  }}
  captionPill.style.opacity = '1';

  // Build words HTML with active highlight
  let html = '';
  for (const w of chunk.words) {{
    const isActive = (t >= w.s && t <= w.e);
    const isPast = (t > w.e);
    const cls = isActive ? 'sub-word active' : (isPast ? 'sub-word past' : 'sub-word');
    html += `<span class="${{cls}}">${{w.w}}</span> `;
  }}
  captionWords.innerHTML = html;
}}

/* GSAP Choreography Timeline */
const tl = gsap.timeline({{ paused: true }});
const runway = $('#runway');

/* Camera Transition Helper */
function glideTo(startTime, targetX, dur = 1.1) {{
  tl.to(runway, {{
    x: targetX,
    duration: dur,
    ease: 'power3.inOut'
  }}, startTime);

  // Optical motion streak
  tl.fromTo('#motionStreak', {{ opacity: 0, x: '-100%' }}, {{ opacity: 0.65, x: '100%', duration: dur * 0.7, ease: 'power2.inOut' }}, startTime + dur * 0.15);
  tl.to('#motionStreak', {{ opacity: 0, duration: 0.2 }}, startTime + dur * 0.85);
}}

/* Headline Swap Helper */
function showHeadline(sel, startTime, hlSel) {{
  tl.fromTo(sel, {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.55, ease: 'power3.out' }}, startTime);
  if (hlSel) {{
    tl.fromTo(`${{hlSel}} i`, {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.45, ease: 'power3.out' }}, startTime + 0.45);
  }}
}}
function hideHeadline(sel, startTime) {{
  tl.to(sel, {{ opacity: 0, y: -20, duration: 0.35, ease: 'power2.in' }}, startTime);
}}

/* Stamp Slam Helper */
function slamStamp(sel, startTime) {{
  tl.fromTo(sel, {{ opacity: 0, scale: 2.2 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: 'power4.in' }}, startTime);
}}

/* --------------------------------------------------------------------------
   BUILD MASTER CHOREOGRAPHY (152.92s)
   -------------------------------------------------------------------------- */

// =========================================================================
// 0. INTRO CONFIDENTIAL DOSSIER UNSEALING (0.0s - 1.6s)
// =========================================================================
tl.set("#introOverlay", {{ opacity: 1, display: "flex" }}, 0);
tl.to("#introTapeBar", {{ scaleX: 0, opacity: 0, duration: 0.65, ease: "power3.inOut" }}, 0.6);
tl.to("#introFolderCard", {{ scale: 1.14, opacity: 0, duration: 0.75, ease: "power2.inOut" }}, 1.0);
tl.to("#introOverlay", {{ opacity: 0, duration: 0.4, onComplete: () => {{
  const o = document.getElementById("introOverlay");
  if (o) o.style.display = "none";
}} }}, 1.4);

// --- SCENE 1 (0.0s - 21.0s) [X = 0] ---
tl.set(runway, {{ x: 0 }}, 0);

// Sprites Entrance (Enters cleanly and stays anchored, ZERO wobbling/shake)
tl.fromTo('#spBook', {{ opacity: 0, y: 70, scale: 0.94 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.9, ease: 'power3.out' }}, 1.2);
tl.fromTo('#spWax', {{ opacity: 0, scale: 1.4, rotate: -15 }}, {{ opacity: 1, scale: 1, rotate: 0, duration: 0.7, ease: 'back.out(1.4)' }}, 1.5);
tl.fromTo('#spQuill', {{ opacity: 0, x: -50 }}, {{ opacity: 1, x: 0, duration: 0.8, ease: 'power3.out' }}, 1.8);
tl.fromTo('#spOpenSpread1', {{ opacity: 0, x: 50 }}, {{ opacity: 1, x: 0, duration: 0.8, ease: 'power3.out' }}, 2.0);
tl.fromTo('#hn1_1', {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: 'back.out' }}, 2.4);

// Telemetry & Stamp
tl.fromTo('#cardTelemetry1', {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' }}, 3.0);
slamStamp('#stampArtifact', 4.5);

// Beat 1 Headline (0.0s - 10.69s) - appears cleanly at 1.4s right after folder unseals
showHeadline('#hlBox1_1', 1.4, '#hl1_1');
hideHeadline('#hlBox1_1', 10.8);

// Beat 2 Headline (11.99s - 20.76s)
tl.fromTo('#hn1_2', {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: 'back.out' }}, 12.4);
showHeadline('#hlBox1_2', 12.0, '#hl1_2');
hideHeadline('#hlBox1_2', 20.8);

// --- TRANSITION TO SCENE 2 (20.8s - 22.0s) ---
glideTo(20.8, -1080, 1.2);

// --- SCENE 2 (22.0s - 46.5s) [X = -1080] ---
tl.fromTo('#spAlienFlower', {{ opacity: 0, y: 80, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 1.0, ease: 'power3.out' }}, 22.2);
tl.fromTo('#spVascularLeaf', {{ opacity: 0, x: 60 }}, {{ opacity: 1, x: 0, duration: 0.8, ease: 'power3.out' }}, 22.8);
tl.fromTo('#spMagnifier', {{ opacity: 0, scale: 0.7, rotate: -15 }}, {{ opacity: 1, scale: 1, rotate: 0, duration: 0.8, ease: 'back.out(1.4)' }}, 23.4);
tl.fromTo('#hn2_1', {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: 'back.out' }}, 24.0);

tl.fromTo('#spZodiac', {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }}, 25.0);
tl.fromTo('#spTubes', {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }}, 25.6);
tl.fromTo('#cardTelemetry2', {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' }}, 26.5);

// Beat 3 Headline (22.16s - 34.72s)
showHeadline('#hlBox2_1', 22.4, '#hl2_1');
hideHeadline('#hlBox2_1', 34.8);

// Beat 4 Headline (36.02s - 46.00s)
tl.fromTo('#hn2_2', {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: 'back.out' }}, 36.6);
showHeadline('#hlBox2_2', 36.2, '#hl2_2');
hideHeadline('#hlBox2_2', 46.2);

// --- TRANSITION TO SCENE 3 (46.2s - 47.4s) ---
glideTo(46.2, -2160, 1.2);

// --- SCENE 3 (47.4s - 81.9s) [X = -2160] ---
tl.fromTo('#spAmsCore', {{ opacity: 0, y: 80 }}, {{ opacity: 1, y: 0, duration: 1.0, ease: 'power3.out' }}, 47.6);
tl.fromTo('#spRuler', {{ opacity: 0, x: 60 }}, {{ opacity: 1, x: 0, duration: 0.8, ease: 'power3.out' }}, 48.2);
tl.fromTo('#hn3_1', {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: 'back.out' }}, 48.8);

// Beat 5 Headline (47.51s - 57.04s)
showHeadline('#hlBox3_1', 47.6, '#hl3_1');
hideHeadline('#hlBox3_1', 57.2);

// Beat 6: AMS Test (58.34s - 68.92s)
tl.fromTo('#spCarbonGraph', {{ opacity: 0, y: 60, scale: 0.95 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.9, ease: 'power3.out' }}, 58.4);
showHeadline('#hlBox3_2', 58.4, '#hl3_2');
hideHeadline('#hlBox3_2', 69.0);

// Beat 7: Indisputable 1404-1438 (70.22s - 81.40s)
tl.fromTo('#cardTelemetry3', {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' }}, 70.4);
slamStamp('#stampDebunked', 72.0);
tl.fromTo('#hn3_2', {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: 'back.out' }}, 72.8);
showHeadline('#hlBox3_3', 70.4, '#hl3_3');
hideHeadline('#hlBox3_3', 81.5);

// --- TRANSITION TO SCENE 4 (81.5s - 82.8s) ---
glideTo(81.5, -3240, 1.3);

// --- SCENE 4 (82.8s - 109.9s) [X = -3240] ---
tl.fromTo('#spZipfCurve', {{ opacity: 0, y: 70, scale: 0.95 }}, {{ opacity: 1, y: 0, scale: 1, duration: 1.0, ease: 'power3.out' }}, 83.0);
tl.fromTo('#spAlphabet', {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }}, 84.0);
tl.fromTo('#hn4_1', {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: 'back.out' }}, 84.8);
slamStamp('#stampZipf', 86.5);
tl.fromTo('#cardTelemetry4', {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' }}, 87.5);

// Beat 8 Headline (82.90s - 95.98s)
showHeadline('#hlBox4_1', 83.0, '#hl4_1');
hideHeadline('#hlBox4_1', 96.0);

// Beat 9 Headline (97.28s - 109.38s)
tl.fromTo('#hn4_2', {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: 'back.out' }}, 97.8);
showHeadline('#hlBox4_2', 97.4, '#hl4_2');
hideHeadline('#hlBox4_2', 109.5);

// --- TRANSITION TO SCENE 5 (109.5s - 110.6s) ---
glideTo(109.5, -4320, 1.1);

// --- SCENE 5 (110.6s - 124.9s) [X = -4320] ---
tl.fromTo('#spFriedman', {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.8, ease: 'power3.out' }}, 110.8);
tl.fromTo('#spNsaSeal', {{ opacity: 0, scale: 0.8, rotate: 10 }}, {{ opacity: 1, scale: 1, rotate: 0, duration: 0.8, ease: 'back.out(1.5)' }}, 111.4);
tl.fromTo('#spNeuralNet', {{ opacity: 0, y: 70 }}, {{ opacity: 1, y: 0, duration: 0.9, ease: 'power3.out' }}, 112.2);
tl.fromTo('#hn5_1', {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: 'back.out' }}, 113.0);
tl.fromTo('#cardTelemetry5', {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' }}, 114.2);
slamStamp('#stampColdCase', 115.5);
tl.fromTo('#hn5_2', {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: 'back.out' }}, 116.2);

// Beat 10 Headline (110.68s - 124.50s)
showHeadline('#hlBox5_1', 110.8, '#hl5_1');
hideHeadline('#hlBox5_1', 124.6);

// --- TRANSITION TO SCENE 6 (124.6s - 125.8s) ---
glideTo(124.6, -5400, 1.2);

// --- SCENE 6 (125.8s - 152.92s) [X = -5400] ---
tl.fromTo('#spBeineckeSeal', {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.7, ease: 'back.out' }}, 126.0);
tl.fromTo('#spArchiveBox', {{ opacity: 0, y: 50 }}, {{ opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }}, 126.6);
tl.fromTo('#spCallTag', {{ opacity: 0, x: 40 }}, {{ opacity: 1, x: 0, duration: 0.6, ease: 'power3.out' }}, 127.2);
tl.fromTo('#spFinalSpread', {{ opacity: 0, y: 80, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 1.0, ease: 'power3.out' }}, 127.8);
tl.fromTo('#cardTelemetry6', {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' }}, 129.0);
tl.fromTo('#hn6_1', {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: 'back.out' }}, 129.8);

// Beat 11 Headline (125.80s - 138.80s)
showHeadline('#hlBox6_1', 126.0, '#hl6_1');
hideHeadline('#hlBox6_1', 139.0);

// Beat 12 Headline & Final Stamp Slam (140.10s - 152.92s)
showHeadline('#hlBox6_2', 140.2, '#hl6_2');
// Climax Rubber Stamp Slam
tl.fromTo('#outroBigStamp', {{ opacity: 0, scale: 2.5, rotate: -15 }}, {{ opacity: 1, scale: 1, rotate: -6, duration: 0.28, ease: 'power4.in' }}, 143.5);

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

    print(f"[+] Successfully generated {out_file} ({len(html_content)} bytes)")

if __name__ == "__main__":
    main()
