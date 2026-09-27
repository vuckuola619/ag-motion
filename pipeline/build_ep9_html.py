#!/usr/bin/env python3
"""build_ep9_html.py — Build premium, high-retention documentary editorial film for Episode 9:
The Father's Brain // Ar-Ra'i (Sains & Adab Ayah).
"""
import os
import json

def main():
    aligned_path = "assets/episode9_father_parenting/audio/ep9_words_aligned.json"
    with open(aligned_path, "r", encoding="utf-8") as f:
        aligned_data = json.load(f)

    words = aligned_data["words"]
    compact_words = []
    for w in words:
        compact_words.append({
            "w": w["word"],
            "s": w["start"],
            "e": w["end"],
            "b": w["beat"]
        })

    words_json = json.dumps(compact_words, separators=(',', ':'))

    html_content = f'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>The Father's Brain // Ar-Ra'i — Editorial Documentary Film</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Amiri:ital,wght@0,700;1,700&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #0C0E12;
  --canvas-dark: #101217;
  --ink-light: #F6F4EE;
  --ink-muted: #8E93A0;
  --ink-dim: #606573;
  --gold: #D4A373;
  --gold-glow: rgba(212, 163, 115, 0.35);
  --emerald: #2A5C45;
  --emerald-soft: rgba(42, 92, 69, 0.20);
  --vermilion: #B83526;
  --cyan-subtle: #4EA3A9;
  --border-subtle: rgba(255, 255, 255, 0.12);
  --card-shadow: 0 16px 40px rgba(0, 0, 0, 0.55), 0 2px 8px rgba(0, 0, 0, 0.35);
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
  opacity: 0.10;
  mix-blend-mode: overlay;
  z-index: 80;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='260' height='260'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.78' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='260' height='260' filter='url(%23n)'/%3E%3C/svg%3E");
}}

/* Soft Vignette */
.vignette {{
  position: absolute; inset: 0;
  pointer-events: none;
  background: radial-gradient(circle at 50% 50%, transparent 60%, rgba(6, 7, 9, 0.70) 100%);
  z-index: 81;
}}

/* Camera Rig & Horizontal Scene Runway */
#cameraRig {{
  position: absolute; inset: 0;
  will-change: transform;
}}
#runway {{
  position: absolute;
  top: 0; left: 0;
  width: 5400px; height: 1920px; /* 5 scenes @ 1080px */
  display: flex;
  will-change: transform;
}}

/* Scene Container Dossier */
.scene-dossier {{
  position: relative;
  width: 1080px; height: 1920px;
  flex-shrink: 0;
  overflow: hidden;
}}

/* Background Imagery */
.scene-bg {{
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  object-fit: cover;
  filter: brightness(0.68) contrast(1.10);
  transform: scale(1.02);
}}
.scene-scrim {{
  position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(12,14,18,0.72) 0%, rgba(12,14,18,0.40) 45%, rgba(12,14,18,0.88) 100%);
  pointer-events: none;
}}

/* Editorial Top Archive Runner */
#archiveRunner {{
  position: absolute;
  top: 60px; left: 54px;
  width: 972px; height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  background: rgba(14, 18, 25, 0.88);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.45);
  z-index: 90;
  font-family: "JetBrains Mono", monospace;
  font-size: 14px;
  letter-spacing: 0.12em;
  color: var(--ink-light);
}}
#archiveRunner .badge {{
  background: var(--gold);
  color: #12141A;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 13px;
  letter-spacing: 0.14em;
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
.dossier-tag.emerald {{
  color: #52B788;
  border-left-color: #52B788;
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
  font-size: 180px;
  line-height: 0.85;
  letter-spacing: -0.02em;
  color: transparent;
  -webkit-text-stroke: 2px rgba(246, 244, 238, 0.05);
  text-align: center;
  z-index: 6;
  pointer-events: none;
  white-space: nowrap;
  opacity: 0;
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

/* Handwritten Field Notes */
.hand-note {{
  position: absolute;
  font-family: "Instrument Serif", serif;
  font-style: italic;
  font-size: 34px;
  line-height: 1.25;
  color: var(--gold);
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.85);
  z-index: 32;
  letter-spacing: 0.01em;
  opacity: 0;
  max-width: 860px;
}}
.hand-note.emerald {{ color: #74C69D; }}
.hand-note.cyan {{ color: var(--cyan-subtle); }}
.hand-note.vermilion {{ color: var(--vermilion); }}

/* Clean Editorial Telemetry Card */
.telemetry-panel {{
  position: absolute;
  background: rgba(14, 18, 26, 0.94);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 18px 24px;
  box-shadow: var(--card-shadow);
  z-index: 25;
  opacity: 0;
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
  font-size: 56px;
  font-weight: 800;
  color: var(--gold);
  line-height: 0.95;
}}
.telemetry-panel .p-value.emerald {{ color: #52B788; }}
.telemetry-panel .p-value.vermilion {{ color: var(--vermilion); }}
.telemetry-panel .p-unit {{
  font-family: "JetBrains Mono", monospace;
  font-size: 16px;
  font-weight: 600;
  color: var(--ink-muted);
  margin-left: 8px;
}}

/* Vector Chart Containers */
.vector-chart-panel {{
  position: absolute;
  background: rgba(14, 18, 26, 0.95);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 22px 26px;
  box-shadow: var(--card-shadow);
  z-index: 24;
  opacity: 0;
}}
.vector-chart-panel .chart-header {{
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 14px;
}}
.vector-chart-panel .chart-title {{
  font-family: "JetBrains Mono", monospace;
  font-size: 15px;
  font-weight: 700;
  color: var(--gold);
  letter-spacing: 0.10em;
  text-transform: uppercase;
}}
.vector-chart-panel .chart-sub {{
  font-family: "JetBrains Mono", monospace;
  font-size: 13px;
  color: var(--ink-muted);
}}

/* Restrained Archival Rubber Stamps */
.archival-stamp {{
  position: absolute;
  padding: 8px 18px;
  border: 3.5px solid var(--vermilion);
  color: var(--vermilion);
  font-family: "Cinzel", serif;
  font-weight: 900;
  font-size: 24px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  border-radius: 4px;
  background: rgba(184, 53, 38, 0.12);
  mix-blend-mode: screen;
  z-index: 35;
  opacity: 0;
  pointer-events: none;
}}
.archival-stamp.gold {{
  border-color: var(--gold);
  color: var(--gold);
  background: rgba(212, 163, 115, 0.12);
}}
.archival-stamp.emerald {{
  border-color: #52B788;
  color: #52B788;
  background: rgba(82, 183, 136, 0.12);
}}

/* Primary Editorial Headline Box */
.editorial-headline-box {{
  position: absolute;
  left: 60px; right: 60px;
  top: 1340px;
  background: rgba(14, 18, 26, 0.94);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-left: 5px solid var(--gold);
  padding: 22px 26px;
  border-radius: 8px;
  box-shadow: var(--card-shadow);
  z-index: 40;
  opacity: 0;
}}
.editorial-headline-box.emerald {{ border-left-color: #52B788; }}
.editorial-headline-box.vermilion {{ border-left-color: var(--vermilion); }}
.editorial-headline-box .h-kicker {{
  font-family: "JetBrains Mono", monospace;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.14em;
  color: var(--gold);
  margin-bottom: 6px;
  text-transform: uppercase;
}}
.editorial-headline-box.emerald .h-kicker {{ color: #52B788; }}
.editorial-headline-box.vermilion .h-kicker {{ color: var(--vermilion); }}
.editorial-headline-box .h-text {{
  font-family: "Inter", sans-serif;
  font-size: 44px;
  font-weight: 800;
  line-height: 1.20;
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
.hl.g i {{ background: #52B788; }}
.hl.r i {{ background: var(--vermilion); }}

/* Immediate Opening Macro Curiosity Card */
#openingMacroCard {{
  position: absolute;
  top: 360px; left: 60px; right: 60px;
  background: rgba(14, 18, 26, 0.96);
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-left: 6px solid var(--gold);
  border-radius: 10px;
  padding: 40px 36px;
  box-shadow: 0 30px 70px rgba(0, 0, 0, 0.75);
  z-index: 50;
}}
#openingMacroCard .kicker {{
  font-family: "JetBrains Mono", monospace;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.16em;
  color: var(--gold);
  margin-bottom: 12px;
  text-transform: uppercase;
}}
#openingMacroCard .title {{
  font-family: "Cinzel", serif;
  font-size: 56px;
  font-weight: 900;
  line-height: 1.12;
  letter-spacing: -0.02em;
  color: #FFFFFF;
  margin-bottom: 18px;
}}
#openingMacroCard .meta {{
  font-family: "JetBrains Mono", monospace;
  font-size: 16px;
  color: var(--ink-muted);
  line-height: 1.6;
  border-top: 1px solid rgba(255, 255, 255, 0.10);
  padding-top: 16px;
}}

/* Whisper Word-Locked Subtitle Pill (Centered, Mobile-Safe Area) */
#subtitlesContainer {{
  position: absolute;
  left: 50%;
  bottom: 110px;
  transform: translateX(-50%);
  width: 900px;
  text-align: center;
  pointer-events: none;
  z-index: 95;
}}
#subtitlePill {{
  display: inline-block;
  background: rgba(12, 14, 18, 0.90);
  border: 1px solid rgba(255, 255, 255, 0.16);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 12px 28px;
  border-radius: 9999px;
  font-family: "Inter", sans-serif;
  font-weight: 700;
  font-size: 32px;
  line-height: 1.35;
  color: #ECE7DE;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.65);
  max-width: 860px;
}}
#subtitlePill .hl-word {{
  color: var(--gold);
  font-weight: 800;
  text-shadow: 0 0 16px rgba(212, 163, 115, 0.55);
}}

/* Climax Outro Final Stamp */
#outroFinalStamp {{
  position: absolute;
  top: 720px; left: 110px; width: 860px; height: 260px;
  border: 5px solid var(--emerald);
  background: rgba(42, 92, 69, 0.18);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 45;
  opacity: 0;
  transform-origin: center center;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
}}
#outroFinalStamp .stamp-main {{
  font-family: "Cinzel", serif;
  font-size: 52px;
  font-weight: 900;
  letter-spacing: 0.18em;
  color: #52B788;
  text-transform: uppercase;
}}
#outroFinalStamp .stamp-sub {{
  font-family: "JetBrains Mono", monospace;
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.22em;
  color: var(--gold);
  margin-top: 8px;
}}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
</head>
<body>
<div id="stage">
  <div class="grain-overlay"></div>
  <div class="vignette"></div>

  <!-- Editorial Top Archive Runner -->
  <div id="archiveRunner">
    <div style="display: flex; align-items: center; gap: 14px;">
      <span class="badge">DOSSIER #09</span>
      <span class="tag">FATHERHOOD INQUIRY · NEUROSCIENCE & ETHICS</span>
    </div>
    <div style="color: var(--ink-muted); font-size: 15px;">YALE & BUKHARI ARCHIVE</div>
  </div>

  <!-- Master Camera Rig -->
  <div id="cameraRig">
    <div id="runway">

      <!-- ========================================================================= -->
      <!-- SCENE 1: THE MYTH OF THE FINANCIAL ATM (X = 0)                            -->
      <!-- ========================================================================= -->
      <div class="scene-dossier" id="scene1">
        <img class="scene-bg" src="assets/episode9_father_parenting/images/bg_father_study.jpg" alt="Father Study Archive">
        <div class="scene-scrim"></div>

        <div class="dossier-tag vermilion" style="top: 175px; left: 70px;">PARADIGM INQUIRY // THE FINANCIAL ILLUSION</div>
        <div class="ghost-watermark" style="top: 170px; left: 70px; width: 940px;">ATM</div>

        <!-- Opening Macro Curiosity Card (0.0s - 2.8s) -->
        <div id="openingMacroCard">
          <div class="kicker">PARENTING COGNITION · CRITICAL FLAW</div>
          <div class="title">AYAH BUKAN MESIN NAFKAH. INI BUKTI SAINS & ADAB.</div>
          <div class="meta">
            Subjek: Neurosains Paternitas & Adab Pengasuhan<br>
            Fokus: Studi Yale University & Sunnah Nabawi
          </div>
        </div>

        <div class="specimen-pill" id="pillMyth1" style="top: 710px; left: 110px;">PARADIGMA UMUM: MESIN TRANSFER</div>
        <div class="specimen-pill" id="pillMyth2" style="top: 710px; right: 110px;">DAMPAK AYAH ABSEN: +80% ANXIETY</div>

        <div class="hand-note vermilion" id="hn1_1" style="top: 780px; left: 140px; transform: rotate(-2deg);">
          Nafkah finansial tak pernah menggantikan presensi
        </div>

        <!-- Telemetry Panel -->
        <div class="telemetry-panel" id="cardTelemetry1" style="top: 860px; left: 90px; width: 440px;">
          <div class="p-label">RISIKO GANGGUAN EMOSI (AYAH ABSEN)</div>
          <div style="display: flex; align-items: baseline;">
            <span class="p-value vermilion">+80%</span>
            <span class="p-unit">DATA HARVARD</span>
          </div>
        </div>

        <div class="archival-stamp" id="stampMyth" style="top: 860px; right: 90px; transform: rotate(-6deg);">
          KEKELIRUAN FATAL
        </div>

        <!-- Beat 1 Headline -->
        <div class="editorial-headline-box vermilion" id="hlBox1">
          <div class="h-kicker">KEKELIRUAN PARADIGMA AYAH</div>
          <div class="h-text">
            Tugas ayah tidak selesai saat nafkah ditransfer: <span class="hl r" id="hl1"><i></i>ini kekeliruan fatal.</span>
          </div>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- SCENE 2: NEUROBIOLOGY & THE PATERNAL BRAIN (X = -1080)                    -->
      <!-- ========================================================================= -->
      <div class="scene-dossier" id="scene2">
        <img class="scene-bg" src="assets/episode9_father_parenting/images/bg_neuroscience_scan.jpg" alt="Neuroscience Scan">
        <div class="scene-scrim"></div>

        <div class="dossier-tag" style="top: 175px; left: 70px;">NEUROBIOLOGY // YALE CHILD STUDY CENTER</div>
        <div class="ghost-watermark" style="top: 170px; left: 70px; width: 940px;">YALE</div>

        <!-- Hand-Crafted SVG Hormonal Shift Calibration Chart -->
        <div class="vector-chart-panel" id="panelHormone" style="top: 280px; left: 80px; width: 920px; height: 340px;">
          <div class="chart-header">
            <span class="chart-title">Paternal Hormonal Shift During Active Care</span>
            <span class="chart-sub">Feldman et al. (Yale University / PNAS)</span>
          </div>
          <svg width="870" height="230" viewBox="0 0 870 230" style="overflow: visible;">
            <!-- Grid Lines -->
            <line x1="60" y1="180" x2="830" y2="180" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
            <line x1="60" y1="20" x2="60" y2="180" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
            <!-- X Axis Marks -->
            <text x="80" y="205" fill="#8E93A0" font-family="JetBrains Mono" font-size="13">Baseline (Pria Pasif)</text>
            <text x="460" y="205" fill="#D4A373" font-family="JetBrains Mono" font-size="13">Aktif Mengasuh (Mandikan & Gendong)</text>
            <!-- Oxytocin Curve (Gold Surge) -->
            <path id="curveOxytocin" d="M 80 160 Q 300 155, 480 50 T 800 35" fill="none" stroke="#D4A373" stroke-width="4.5" stroke-linecap="round" stroke-dasharray="1000" stroke-dashoffset="1000"/>
            <text x="680" y="25" fill="#D4A373" font-family="JetBrains Mono" font-weight="700" font-size="14">Oksitosin (+140%)</text>
            <!-- Testosterone Curve (Cyan Suppression) -->
            <path id="curveTesto" d="M 80 60 Q 300 65, 480 140 T 800 155" fill="none" stroke="#4EA3A9" stroke-width="3" stroke-dasharray="6 6"/>
            <text x="600" y="145" fill="#4EA3A9" font-family="JetBrains Mono" font-size="13">Testosteron (-32%)</text>
            <!-- Data Dots -->
            <circle cx="800" cy="35" r="6" fill="#D4A373"/>
            <circle cx="800" cy="155" r="5" fill="#4EA3A9"/>
          </svg>
        </div>

        <div class="specimen-pill" id="pillNeuro1" style="top: 670px; left: 110px;">JARINGAN EMPATI: PREFRONTAL CORTEX</div>
        <div class="specimen-pill" id="pillNeuro2" style="top: 670px; right: 110px;">STATUS OKSITOSIN: SETARA IBU MELAHIRKAN</div>

        <div class="hand-note" id="hn2_1" style="top: 740px; left: 120px; transform: rotate(-2.5deg);">
          Otak ayah berubah secara biologis saat mengasuh
        </div>

        <!-- Telemetry Panel -->
        <div class="telemetry-panel" id="cardTelemetry2" style="top: 830px; left: 80px; width: 440px;">
          <div class="p-label">LONJAKAN HORMON OKSITOSIN</div>
          <div style="display: flex; align-items: baseline;">
            <span class="p-value">+140%</span>
            <span class="p-unit">SURGE EMPATI</span>
          </div>
        </div>

        <div class="archival-stamp gold" id="stampNeuro" style="top: 830px; right: 80px; transform: rotate(5deg);">
          TERBUKTI SAINS
        </div>

        <!-- Beat 2 Headline -->
        <div class="editorial-headline-box" id="hlBox2">
          <div class="h-kicker">NEUROBIOLOGI PATERNITAS</div>
          <div class="h-text">
            Saat ayah memandikan dan menidurkan anak: <span class="hl" id="hl2"><i></i>sirkuit empati otak aktif seketika.</span>
          </div>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- SCENE 3: ROUGH PLAY & EMOTIONAL REGULATION (X = -2160)                    -->
      <!-- ========================================================================= -->
      <div class="scene-dossier" id="scene3">
        <img class="scene-bg" src="assets/episode9_father_parenting/images/bg_father_study.jpg" alt="Living Study Room">
        <div class="scene-scrim"></div>

        <div class="dossier-tag cyan" style="top: 175px; left: 70px;">DEVELOPMENTAL PSYCHOLOGY // HARVARD CENTER</div>
        <div class="ghost-watermark" style="top: 170px; left: 70px; width: 940px;">RESILIENCE</div>

        <!-- SVG Dual-Bar Stress Resilience Comparison -->
        <div class="vector-chart-panel" id="panelResilience" style="top: 280px; left: 80px; width: 920px; height: 340px;">
          <div class="chart-header">
            <span class="chart-title">Rough-and-Tumble Play: Impulse Control Index</span>
            <span class="chart-sub">Childhood Stress Resilience Benchmark</span>
          </div>
          <svg width="870" height="230" viewBox="0 0 870 230" style="overflow: visible;">
            <!-- Bar 1: Ayah Terlibat Aktif -->
            <text x="60" y="55" fill="#FFFFFF" font-family="JetBrains Mono" font-weight="700" font-size="14">Ayah Terlibat Aktif (Rough Play)</text>
            <rect x="60" y="70" width="700" height="36" rx="6" fill="rgba(212,163,115,0.20)" stroke="#D4A373" stroke-width="2"/>
            <rect id="barActive" x="60" y="70" width="0" height="36" rx="6" fill="#D4A373"/>
            <text x="780" y="95" fill="#D4A373" font-family="JetBrains Mono" font-weight="700" font-size="16">+40%</text>

            <!-- Bar 2: Ayah Pasif / Absen -->
            <text x="60" y="145" fill="#8E93A0" font-family="JetBrains Mono" font-size="14">Ayah Pasif / Hanya Nafkah</text>
            <rect x="60" y="160" width="700" height="36" rx="6" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
            <rect id="barPassive" x="60" y="160" width="0" height="36" rx="6" fill="#606573"/>
            <text x="780" y="185" fill="#8E93A0" font-family="JetBrains Mono" font-size="15">Baseline</text>
          </svg>
        </div>

        <div class="specimen-pill" id="pillPlay1" style="top: 670px; left: 110px;">LATIHAN OTAK: KENDALI IMPULS & EMOSI</div>
        <div class="specimen-pill" id="pillPlay2" style="top: 670px; right: 110px;">RESILIENSI STRES: +40% LEBIH STABIL</div>

        <div class="hand-note cyan" id="hn3_1" style="top: 740px; left: 120px; transform: rotate(-2deg);">
          Bermain fisik bukan canda belaka—ini latihan ketahanan
        </div>

        <!-- Telemetry Panel -->
        <div class="telemetry-panel" id="cardTelemetry3" style="top: 830px; left: 80px; width: 440px;">
          <div class="p-label">STABILITAS REGULASI EMOSI</div>
          <div style="display: flex; align-items: baseline;">
            <span class="p-value">+40%</span>
            <span class="p-unit">LEBIH TANGGUH</span>
          </div>
        </div>

        <div class="archival-stamp gold" id="stampPlay" style="top: 830px; right: 80px; transform: rotate(-5deg);">
          REGULASI TERUJI
        </div>

        <!-- Beat 3 Headline -->
        <div class="editorial-headline-box" id="hlBox3">
          <div class="h-kicker">PSIKOLOGI PERKEMBANGAN</div>
          <div class="h-text">
            Bermain fisik teratur dengan ayah: <span class="hl" id="hl3"><i></i>melatih ketahanan stres dan kendali emosi.</span>
          </div>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- SCENE 4: ISLAMIC ETHICS & SUNNAH NABAWI (X = -3240)                       -->
      <!-- ========================================================================= -->
      <div class="scene-dossier" id="scene4">
        <img class="scene-bg" src="assets/episode9_father_parenting/images/bg_islamic_archival.jpg" alt="Islamic Archival Manuscript">
        <div class="scene-scrim"></div>

        <div class="dossier-tag emerald" style="top: 175px; left: 70px;">SUNNAH NABAWI // ADAB & PRESENSI KELUARGA</div>
        <div class="ghost-watermark" style="top: 170px; left: 70px; width: 940px;">AR-RA'I</div>

        <!-- Calligraphic Archival Inscription Card -->
        <div class="vector-chart-panel" id="panelHadith" style="top: 280px; left: 80px; width: 920px; height: 350px; background: rgba(14, 22, 18, 0.94); border-color: rgba(82, 183, 136, 0.35);">
          <div class="chart-header">
            <span class="chart-title" style="color: #74C69D;">Sahih Bukhari No. 5996 & 5997</span>
            <span class="chart-sub">Keteladanan Rasulullah ﷺ</span>
          </div>
          <div style="font-family: 'Amiri', serif; font-size: 34px; line-height: 1.6; color: #E8F5E9; text-align: right; margin-bottom: 14px;">
            مَنْ لا يَرْحَمُ لا يُرْحَمُ
          </div>
          <div style="font-family: 'Instrument Serif', serif; font-style: italic; font-size: 30px; line-height: 1.35; color: #D4A373;">
            "Siapa yang tidak menyayangi, niscaya tidak akan disayangi."
          </div>
          <div style="font-family: 'Inter', sans-serif; font-size: 18px; line-height: 1.5; color: #A3B19B; margin-top: 10px; border-top: 1px solid rgba(82, 183, 136, 0.2); padding-top: 10px;">
            Nabi ﷺ menggendong cucunya saat shalat berjamaah, membantah budaya jahiliyah yang gengsi mencium anak.
          </div>
        </div>

        <div class="specimen-pill" id="pillIslam1" style="top: 670px; left: 110px;">KONSEP AR-RA'I: PEMIMPIN JIWA & EMOSI</div>
        <div class="specimen-pill" id="pillIslam2" style="top: 670px; right: 110px;">SURAH LUQMAN: DIALOG AYAH KE ANAK</div>

        <div class="hand-note emerald" id="hn4_1" style="top: 740px; left: 120px; transform: rotate(-2deg);">
          Rasulullah ﷺ mendahulukan kasih sayang di atas formalitas
        </div>

        <!-- Telemetry Panel -->
        <div class="telemetry-panel" id="cardTelemetry4" style="top: 830px; left: 80px; width: 440px;">
          <div class="p-label">PERAN FUNDAMENTAL AYAH</div>
          <div style="display: flex; align-items: baseline;">
            <span class="p-value emerald">AR-RA'I</span>
            <span class="p-unit">PEMIMPIN JIWA</span>
          </div>
        </div>

        <div class="archival-stamp emerald" id="stampIslam" style="top: 830px; right: 80px; transform: rotate(5deg);">
          SUNNAH NABAWI
        </div>

        <!-- Beat 4 Headline -->
        <div class="editorial-headline-box emerald" id="hlBox4">
          <div class="h-kicker">ADAB & KETELADANAN ISLAM</div>
          <div class="h-text">
            Dalam Islam, ayah adalah Ar-Ra'i: <span class="hl g" id="hl4"><i></i>pemimpin jiwa dan pelindung emosional.</span>
          </div>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- SCENE 5: OUTRO & THE ENDURING PRESENCE (X = -4320)                        -->
      <!-- ========================================================================= -->
      <div class="scene-dossier" id="scene5">
        <img class="scene-bg" src="assets/episode9_father_parenting/images/bg_father_study.jpg" alt="Father Study Memory">
        <div class="scene-scrim"></div>

        <div class="dossier-tag" style="top: 175px; left: 70px;">FINAL VERDICT // THE LIFETIME RECORD</div>
        <div class="ghost-watermark" style="top: 170px; left: 70px; width: 940px;">PRESENSI</div>

        <!-- Outro Climax Stamp -->
        <div id="outroFinalStamp">
          <div class="stamp-main">HADIR SECARA UTUH</div>
          <div class="stamp-sub">PRESENSI NYATA MELAMPAUI SALDO REKENING</div>
        </div>

        <div class="hand-note" id="hn5_1" style="top: 1040px; left: 110px; transform: rotate(-1.5deg);">
          Anak tidak mengingat saldo tabunganmu—mereka merekam kehadiranmu
        </div>

        <!-- Telemetry Panel -->
        <div class="telemetry-panel" id="cardTelemetry5" style="top: 1120px; left: 80px; width: 920px;">
          <div class="p-label">WARISAN TERBESAR SEORANG AYAH</div>
          <div style="font-family: 'Cinzel', serif; font-size: 40px; font-weight: 800; color: var(--gold); line-height: 1.2; margin-top: 6px;">
            KEHANGATAN TANGAN SAAT MEREKA TAKUT
          </div>
        </div>

        <!-- Beat 5 Headline -->
        <div class="editorial-headline-box" id="hlBox5">
          <div class="h-kicker">PESAN ABADI SANG AYAH</div>
          <div class="h-text">
            Yang direkam anak seumur hidup: <span class="hl" id="hl5"><i></i>kehadiran dan kehangatan tanganmu.</span>
          </div>
        </div>
      </div>

    </div>
  </div>

  <!-- Whisper Word-Locked Subtitles -->
  <div id="subtitlesContainer">
    <div id="subtitlePill">Mendengarkan...</div>
  </div>

  <audio id="audioTrack" preload="auto">
    <source src="assets/episode9_father_parenting/audio/vo_ep9_master.wav" type="audio/wav">
    <source src="assets/episode9_father_parenting/audio/vo_ep9_master.mp3" type="audio/mpeg">
  </audio>
</div>

<script>
const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);

const DURATION = {aligned_data["total_duration"]};
const WORDS = {words_json};

/* Dynamic Subtitles Logic */
function updateDynamicSubtitles(t) {{
  let activeWord = null;
  let activeIdx = -1;

  for (let i = 0; i < WORDS.length; i++) {{
    if (t >= WORDS[i].s && t <= WORDS[i].e) {{
      activeWord = WORDS[i];
      activeIdx = i;
      break;
    }}
  }}

  const pill = $('#subtitlePill');

  if (activeWord) {{
    const beat = activeWord.b;
    let startIdx = Math.max(0, activeIdx - 3);
    let endIdx = Math.min(WORDS.length - 1, activeIdx + 4);

    while (startIdx > 0 && WORDS[startIdx].b === beat && (activeIdx - startIdx) < 4) {{
      startIdx--;
    }}
    if (WORDS[startIdx].b !== beat) startIdx++;

    while (endIdx < WORDS.length - 1 && WORDS[endIdx].b === beat && (endIdx - activeIdx) < 4) {{
      endIdx++;
    }}
    if (WORDS[endIdx].b !== beat) endIdx--;

    let html = '';
    for (let k = startIdx; k <= endIdx; k++) {{
      if (k === activeIdx) {{
        html += `<span class="hl-word">${{WORDS[k].w}}</span> `;
      }} else {{
        html += `${{WORDS[k].w}} `;
      }}
    }}
    pill.innerHTML = html.trim();
    pill.style.opacity = '1';
  }} else {{
    // Between words or silent gap
    let closestPrev = null;
    for (let i = WORDS.length - 1; i >= 0; i--) {{
      if (t >= WORDS[i].e) {{
        closestPrev = WORDS[i];
        break;
      }}
    }}
    if (closestPrev && (t - closestPrev.e) < 0.6) {{
      pill.style.opacity = '1';
    }} else {{
      pill.style.opacity = '0';
    }}
  }}
}}

/* Master GSAP Timeline */
const tl = gsap.timeline({{ paused: true }});
const cameraRig = $('#cameraRig');
const runway = $('#runway');

function glideTo(time, targetX, dur = 0.85) {{
  tl.to(runway, {{ x: targetX, duration: dur, ease: 'power3.inOut' }}, time);
}}

function cameraPush(time, targetScale, dur = 8.0) {{
  tl.to(cameraRig, {{ scale: targetScale, transformOrigin: '540px 960px', duration: dur, ease: 'power1.out' }}, time);
}}

function showHeadline(boxId, time, hlId) {{
  tl.fromTo(boxId, {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.55, ease: 'power3.out' }}, time);
  if (hlId) {{
    tl.to(`${{hlId}} i`, {{ scaleX: 1, duration: 0.70, ease: 'power2.out' }}, time + 0.35);
  }}
}}

function hideHeadline(boxId, time) {{
  tl.to(boxId, {{ opacity: 0, y: -20, duration: 0.45, ease: 'power2.in' }}, time);
}}

function slamStamp(stampId, time) {{
  tl.fromTo(stampId, 
    {{ opacity: 0, scale: 2.2, rotate: -18 }}, 
    {{ opacity: 1, scale: 1, rotate: 0, duration: 0.28, ease: 'power4.in' }}, 
    time
  );
}}

// =========================================================================
// SCENE 1: HOOK & THE MYTH OF NAFKAH (0.0s - 10.37s)
// =========================================================================
cameraPush(0.0, 1.04, 10.0);
tl.fromTo('#openingMacroCard', {{ opacity: 0, y: 35, scale: 0.96 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.75, ease: 'power3.out' }}, 0.2);
tl.to('#openingMacroCard', {{ opacity: 0, y: -20, duration: 0.55, ease: 'power2.in' }}, 2.8);

tl.to(['#scene1 .dossier-tag', '#scene1 .ghost-watermark'], {{ opacity: 1, duration: 0.6, ease: 'power2.out' }}, 3.2);
tl.fromTo(['#pillMyth1', '#pillMyth2'], {{ opacity: 0, y: 15 }}, {{ opacity: 1, y: 0, duration: 0.50, ease: 'power3.out' }}, 3.6);
tl.fromTo('#hn1_1', {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.50, ease: 'back.out' }}, 4.2);
tl.fromTo('#cardTelemetry1', {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.55, ease: 'power3.out' }}, 4.8);
slamStamp('#stampMyth', 5.6);

showHeadline('#hlBox1', 3.4, '#hl1');
hideHeadline('#hlBox1', 10.6);

// =========================================================================
// TRANSITION TO SCENE 2: NEUROBIOLOGY (10.6s - 11.57s)
// =========================================================================
glideTo(10.6, -1080, 0.85);

// =========================================================================
// SCENE 2: YALE NEUROBIOLOGY & HORMONAL SURGE (11.57s - 27.19s)
// =========================================================================
tl.to(['#scene2 .dossier-tag', '#scene2 .ghost-watermark'], {{ opacity: 1, duration: 0.6, ease: 'power2.out' }}, 11.6);
tl.fromTo('#panelHormone', {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.65, ease: 'power3.out' }}, 12.0);

// Draw Oxytocin curve
tl.fromTo('#curveOxytocin', {{ strokeDashoffset: 1000 }}, {{ strokeDashoffset: 0, duration: 1.4, ease: 'power2.inOut' }}, 12.6);

tl.fromTo(['#pillNeuro1', '#pillNeuro2'], {{ opacity: 0, y: 15 }}, {{ opacity: 1, y: 0, duration: 0.50, ease: 'power3.out' }}, 14.0);
tl.fromTo('#hn2_1', {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.50, ease: 'back.out' }}, 14.8);
tl.fromTo('#cardTelemetry2', {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.55, ease: 'power3.out' }}, 15.6);
slamStamp('#stampNeuro', 17.0);

showHeadline('#hlBox2', 12.2, '#hl2');
hideHeadline('#hlBox2', 27.2);

// =========================================================================
// TRANSITION TO SCENE 3: ROUGH PLAY & REGULATION (27.2s - 28.49s)
// =========================================================================
glideTo(27.2, -2160, 0.85);

// =========================================================================
// SCENE 3: PSYCHOLOGY & ROUGH-AND-TUMBLE PLAY (28.49s - 42.84s)
// =========================================================================
tl.to(['#scene3 .dossier-tag', '#scene3 .ghost-watermark'], {{ opacity: 1, duration: 0.6, ease: 'power2.out' }}, 28.6);
tl.fromTo('#panelResilience', {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.65, ease: 'power3.out' }}, 29.0);

// Animate dual bars
tl.to('#barActive', {{ width: 560, duration: 1.1, ease: 'power2.out' }}, 29.6);
tl.to('#barPassive', {{ width: 280, duration: 0.9, ease: 'power2.out' }}, 30.2);

tl.fromTo(['#pillPlay1', '#pillPlay2'], {{ opacity: 0, y: 15 }}, {{ opacity: 1, y: 0, duration: 0.50, ease: 'power3.out' }}, 31.0);
tl.fromTo('#hn3_1', {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.50, ease: 'back.out' }}, 31.8);
tl.fromTo('#cardTelemetry3', {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.55, ease: 'power3.out' }}, 32.6);
slamStamp('#stampPlay', 34.0);

showHeadline('#hlBox3', 29.0, '#hl3');
hideHeadline('#hlBox3', 42.8);

// =========================================================================
// TRANSITION TO SCENE 4: SUNNAH NABAWI & ADAB (42.8s - 44.14s)
// =========================================================================
glideTo(42.8, -3240, 0.85);

// =========================================================================
// SCENE 4: ISLAMIC ETHICS & KETELADANAN AR-RA'I (44.14s - 62.28s)
// =========================================================================
tl.to(['#scene4 .dossier-tag', '#scene4 .ghost-watermark'], {{ opacity: 1, duration: 0.6, ease: 'power2.out' }}, 44.2);
tl.fromTo('#panelHadith', {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.70, ease: 'power3.out' }}, 44.8);

tl.fromTo(['#pillIslam1', '#pillIslam2'], {{ opacity: 0, y: 15 }}, {{ opacity: 1, y: 0, duration: 0.50, ease: 'power3.out' }}, 46.5);
tl.fromTo('#hn4_1', {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.50, ease: 'back.out' }}, 47.5);
tl.fromTo('#cardTelemetry4', {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.55, ease: 'power3.out' }}, 48.5);
slamStamp('#stampIslam', 50.0);

showHeadline('#hlBox4', 45.0, '#hl4');
hideHeadline('#hlBox4', 62.2);

// =========================================================================
// TRANSITION TO SCENE 5: OUTRO & THE ENDURING PRESENCE (62.2s - 63.68s)
// =========================================================================
glideTo(62.2, -4320, 0.90);

// =========================================================================
// SCENE 5: OUTRO & FINAL VERDICT (63.68s - 74.56s)
// =========================================================================
tl.to(['#scene5 .dossier-tag', '#scene5 .ghost-watermark'], {{ opacity: 1, duration: 0.6, ease: 'power2.out' }}, 63.8);
tl.fromTo('#outroFinalStamp', 
  {{ opacity: 0, scale: 2.2, rotate: -8 }}, 
  {{ opacity: 1, scale: 1, rotate: 0, duration: 0.35, ease: 'power4.in' }}, 
  64.5
);
tl.fromTo('#hn5_1', {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.50, ease: 'back.out' }}, 65.5);
tl.fromTo('#cardTelemetry5', {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.55, ease: 'power3.out' }}, 66.2);

showHeadline('#hlBox5', 64.2, '#hl5');

// Final camera breath
cameraPush(64.0, 0.98, 9.0);

/* Headless Puppeteer Seek Hook */
window.BANG_MOTION = {{
  ready: true,
  seekFrame: function(t) {{
    tl.pause(t, false);
    updateDynamicSubtitles(t);
  }},
  duration: DURATION
}};

/* Interactive Playback */
const audio = $('#audioTrack');
let isPlaying = false;

function playVideo() {{
  tl.play(0);
  audio.currentTime = 0;
  audio.play().then(() => isPlaying = true).catch(() => {{}});
}}
window.addEventListener('click', () => {{
  if (!isPlaying) playVideo();
}});
</script>
</body>
</html>
'''

    with open("index_ep9.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("[OK] index_ep9.html successfully generated!")

if __name__ == "__main__":
    main()
