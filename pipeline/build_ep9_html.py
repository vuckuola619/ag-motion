#!/usr/bin/env python3
"""build_ep9_html.py — Build bright, warm, fun editorial documentary film for Episode 9:
The Father's Brain // Ar-Ra'i (Science & Prophetic Ethics of Active Fatherhood).
English Edition featuring transparent AI-generated sprites, light parchment canvas,
and crisp editorial infographics.
"""
import os
import json

def main():
    aligned_path = "assets/episode9_father_parenting/audio_en/ep9_en_words_aligned.json"
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
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>The Father's Brain // Ar-Ra'i — Editorial Documentary Film</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800;900&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@500;600;700;800&family=Amiri:ital,wght@0,700;1,700&display=swap" rel="stylesheet">
<style>
:root {{
  --bg-canvas: #FAF8F4;
  --bg-card: #FFFFFF;
  --bg-card-subtle: #F3EFE6;
  --ink-primary: #181A1E;
  --ink-secondary: #565C69;
  --ink-muted: #848B98;
  --coral-accent: #E76F51;
  --coral-soft: rgba(231, 111, 81, 0.12);
  --emerald-accent: #2A9D8F;
  --emerald-soft: rgba(42, 157, 143, 0.12);
  --gold-accent: #E9C46A;
  --gold-soft: rgba(233, 196, 106, 0.18);
  --navy-accent: #264653;
  --border-card: rgba(24, 26, 30, 0.08);
  --card-shadow: 0 16px 40px rgba(38, 70, 83, 0.08), 0 4px 12px rgba(38, 70, 83, 0.04);
  --sprite-shadow: drop-shadow(0 18px 32px rgba(38, 70, 83, 0.14));
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; -webkit-font-smoothing: antialiased; }}
html, body {{
  width: 100%; height: 100%;
  background: #EBE6DC;
  overflow: hidden;
  font-family: "Plus Jakarta Sans", sans-serif;
  color: var(--ink-primary);
}}

/* 1080x1920 Stage Canvas */
#stage {{
  position: absolute;
  left: 50%; top: 50%;
  width: 1080px; height: 1920px;
  background: var(--bg-canvas);
  overflow: hidden;
  transform: translate(-50%, -50%);
  transform-origin: center center;
  box-shadow: 0 0 120px rgba(0, 0, 0, 0.25);
}}

/* Editorial Geometric Grid Pattern */
.grid-overlay {{
  position: absolute; inset: 0;
  pointer-events: none;
  background-size: 36px 36px;
  background-image: 
    linear-gradient(to right, rgba(0, 0, 0, 0.035) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(0, 0, 0, 0.035) 1px, transparent 1px);
  z-index: 5;
}}

/* Tactile Soft Grain */
.grain-overlay {{
  position: absolute; inset: 0;
  pointer-events: none;
  opacity: 0.06;
  mix-blend-mode: multiply;
  z-index: 6;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='260' height='260'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.75' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='260' height='260' filter='url(%23n)'/%3E%3C/svg%3E");
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

/* Scene Container */
.scene-dossier {{
  position: relative;
  width: 1080px; height: 1920px;
  flex-shrink: 0;
  overflow: hidden;
}}

/* Editorial Top Archive Runner */
#archiveRunner {{
  position: absolute;
  top: 54px; left: 54px;
  width: 972px; height: 64px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  background: rgba(255, 255, 255, 0.94);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid var(--border-card);
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(38, 70, 83, 0.06);
  z-index: 90;
  font-family: "JetBrains Mono", monospace;
  font-size: 14px;
  letter-spacing: 0.12em;
  color: var(--ink-secondary);
}}
#archiveRunner .badge {{
  background: var(--navy-accent);
  color: #FFFFFF;
  font-weight: 700;
  padding: 5px 12px;
  border-radius: 6px;
  font-size: 13px;
  letter-spacing: 0.14em;
}}

/* Editorial Dossier Index Tag */
.dossier-tag {{
  position: absolute;
  font-family: "JetBrains Mono", monospace;
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: var(--navy-accent);
  background: #FFFFFF;
  padding: 8px 18px;
  border-left: 4px solid var(--coral-accent);
  border-radius: 6px;
  z-index: 25;
  box-shadow: 0 6px 18px rgba(38, 70, 83, 0.08);
  text-transform: uppercase;
  opacity: 0;
}}
.dossier-tag.emerald {{ border-left-color: var(--emerald-accent); }}
.dossier-tag.navy {{ border-left-color: var(--navy-accent); }}

/* Ghost Watermark Monogram */
.ghost-watermark {{
  position: absolute;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-weight: 900;
  font-size: 190px;
  line-height: 0.85;
  letter-spacing: -0.04em;
  color: rgba(38, 70, 83, 0.035);
  text-align: center;
  z-index: 4;
  pointer-events: none;
  white-space: nowrap;
  opacity: 0;
}}

/* Crisp Specimen Pill */
.specimen-pill {{
  position: absolute;
  padding: 8px 18px;
  background: #FFFFFF;
  border: 1px solid var(--border-card);
  color: var(--ink-secondary);
  font-family: "JetBrains Mono", monospace;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.10em;
  border-radius: 9999px;
  z-index: 26;
  box-shadow: 0 4px 16px rgba(38, 70, 83, 0.06);
  white-space: nowrap;
  opacity: 0;
}}
.specimen-pill.coral {{ color: var(--coral-accent); border-color: rgba(231,111,81,0.25); }}
.specimen-pill.emerald {{ color: var(--emerald-accent); border-color: rgba(42,157,143,0.25); }}

/* Handwritten Field Notes */
.hand-note {{
  position: absolute;
  font-family: "Instrument Serif", serif;
  font-style: italic;
  font-size: 38px;
  line-height: 1.22;
  color: var(--coral-accent);
  z-index: 32;
  letter-spacing: 0.01em;
  opacity: 0;
  max-width: 860px;
}}
.hand-note.emerald {{ color: var(--emerald-accent); }}
.hand-note.navy {{ color: var(--navy-accent); }}

/* Clean Editorial Telemetry Card */
.telemetry-panel {{
  position: absolute;
  background: var(--bg-card);
  border: 1.5px solid var(--border-card);
  border-radius: 16px;
  padding: 20px 26px;
  box-shadow: var(--card-shadow);
  z-index: 25;
  opacity: 0;
}}
.telemetry-panel .p-label {{
  font-family: "JetBrains Mono", monospace;
  font-size: 13px;
  font-weight: 700;
  color: var(--ink-muted);
  letter-spacing: 0.12em;
  margin-bottom: 6px;
  text-transform: uppercase;
}}
.telemetry-panel .p-value {{
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 58px;
  font-weight: 900;
  color: var(--coral-accent);
  line-height: 0.95;
}}
.telemetry-panel .p-value.emerald {{ color: var(--emerald-accent); }}
.telemetry-panel .p-value.navy {{ color: var(--navy-accent); }}
.telemetry-panel .p-unit {{
  font-family: "JetBrains Mono", monospace;
  font-size: 15px;
  font-weight: 700;
  color: var(--ink-muted);
  margin-left: 8px;
}}

/* Vector Chart Containers */
.vector-chart-panel {{
  position: absolute;
  background: var(--bg-card);
  border: 1.5px solid var(--border-card);
  border-radius: 18px;
  padding: 24px 28px;
  box-shadow: var(--card-shadow);
  z-index: 24;
  opacity: 0;
}}
.vector-chart-panel .chart-header {{
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 16px;
}}
.vector-chart-panel .chart-title {{
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 16px;
  font-weight: 800;
  color: var(--navy-accent);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}}
.vector-chart-panel .chart-sub {{
  font-family: "JetBrains Mono", monospace;
  font-size: 13px;
  color: var(--ink-muted);
}}

/* Prominent Editorial Transparent Sprites */
.sprite-cutout {{
  position: absolute;
  filter: var(--sprite-shadow);
  z-index: 20;
  opacity: 0;
  transform-origin: center center;
  pointer-events: none;
}}

/* Bold Editorial Headline Bar */
.editorial-headline-box {{
  position: absolute;
  bottom: 230px; left: 60px;
  width: 960px;
  background: #FFFFFF;
  border-radius: 18px;
  border: 1.5px solid var(--border-card);
  box-shadow: 0 20px 48px rgba(38, 70, 83, 0.08);
  padding: 28px 34px;
  z-index: 70;
  opacity: 0;
}}
.editorial-headline-box .h-kicker {{
  font-family: "JetBrains Mono", monospace;
  font-size: 14px;
  font-weight: 800;
  color: var(--coral-accent);
  letter-spacing: 0.16em;
  text-transform: uppercase;
  margin-bottom: 8px;
}}
.editorial-headline-box.emerald .h-kicker {{ color: var(--emerald-accent); }}
.editorial-headline-box.navy .h-kicker {{ color: var(--navy-accent); }}
.editorial-headline-box .h-text {{
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 40px;
  font-weight: 800;
  line-height: 1.25;
  color: var(--ink-primary);
  letter-spacing: -0.02em;
}}
.editorial-headline-box .hl {{
  position: relative;
  display: inline;
  color: var(--coral-accent);
  font-weight: 900;
}}
.editorial-headline-box .hl.g {{ color: var(--emerald-accent); }}
.editorial-headline-box .hl.n {{ color: var(--navy-accent); }}
.editorial-headline-box .hl i {{
  position: absolute;
  left: 0; bottom: 2px;
  width: 100%; height: 6px;
  background: rgba(231, 111, 81, 0.28);
  border-radius: 3px;
  transform-origin: left center;
  transform: scaleX(0);
  pointer-events: none;
}}
.editorial-headline-box .hl.g i {{ background: rgba(42, 157, 143, 0.28); }}
.editorial-headline-box .hl.n i {{ background: rgba(38, 70, 83, 0.25); }}

/* Whisper Word-Locked Subtitles Pill */
#subtitlesContainer {{
  position: absolute;
  bottom: 110px; left: 90px;
  width: 900px;
  text-align: center;
  pointer-events: none;
  z-index: 95;
}}
#subtitlePill {{
  display: inline-block;
  background: rgba(255, 255, 255, 0.96);
  border: 1.5px solid rgba(24, 26, 30, 0.10);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  padding: 14px 30px;
  border-radius: 9999px;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-weight: 700;
  font-size: 32px;
  line-height: 1.35;
  color: var(--ink-primary);
  box-shadow: 0 12px 32px rgba(38, 70, 83, 0.10);
  max-width: 860px;
}}
#subtitlePill .hl-word {{
  color: var(--coral-accent);
  font-weight: 900;
  text-shadow: 0 0 12px rgba(231, 111, 81, 0.35);
}}

/* Climax Outro Final Stamp */
#outroFinalStamp {{
  position: absolute;
  top: 960px; left: 90px; width: 900px; height: 240px;
  border: 4px solid var(--emerald-accent);
  background: #FFFFFF;
  border-radius: 18px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 45;
  opacity: 0;
  transform-origin: center center;
  box-shadow: 0 16px 40px rgba(42, 157, 143, 0.15);
}}
#outroFinalStamp .stamp-main {{
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 56px;
  font-weight: 900;
  letter-spacing: 0.14em;
  color: var(--emerald-accent);
  text-transform: uppercase;
}}
#outroFinalStamp .stamp-sub {{
  font-family: "JetBrains Mono", monospace;
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.18em;
  color: var(--navy-accent);
  margin-top: 8px;
}}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
</head>
<body>
<div id="stage">
  <div class="grid-overlay"></div>
  <div class="grain-overlay"></div>

  <!-- Editorial Top Archive Runner -->
  <div id="archiveRunner">
    <div style="display: flex; align-items: center; gap: 14px;">
      <span class="badge">DOSSIER #09</span>
      <span style="font-weight: 700; color: var(--navy-accent);">FATHERHOOD INQUIRY · NEUROSCIENCE & SUNNAH</span>
    </div>
    <div style="color: var(--ink-muted); font-size: 14px; font-weight: 600;">YALE & BUKHARI RESEARCH</div>
  </div>

  <!-- Master Camera Rig -->
  <div id="cameraRig">
    <div id="runway">

      <!-- ========================================================================= -->
      <!-- SCENE 1: THE ATM DAD FALLACY (X = 0)                                      -->
      <!-- ========================================================================= -->
      <div class="scene-dossier" id="scene1">
        <div class="dossier-tag" style="top: 150px; left: 60px;">PARADIGM INQUIRY // THE FINANCIAL ILLUSION</div>
        <div class="ghost-watermark" style="top: 140px; left: 60px; width: 960px;">ATM DAD</div>

        <!-- Transparent AI Sprite: Stressed ATM Dad -->
        <img class="sprite-cutout" id="spriteDadAtm" src="assets/episode9_father_parenting/sprites/sprite_dad_atm_myth.png" 
             style="top: 260px; right: 30px; width: 500px;" alt="The ATM Dad Fallacy">

        <div class="specimen-pill coral" id="pillMyth1" style="top: 270px; left: 70px;">COMMON TRAP: HUMAN ATM</div>
        <div class="specimen-pill" id="pillMyth2" style="top: 330px; left: 70px;">ABSENT FATHER RISK: +80% ANXIETY</div>

        <div class="hand-note" id="hn1_1" style="top: 420px; left: 70px; transform: rotate(-2deg); max-width: 480px;">
          Financial support cannot replace emotional presence
        </div>

        <!-- Telemetry Panel -->
        <div class="telemetry-panel" id="cardTelemetry1" style="top: 530px; left: 60px; width: 440px;">
          <div class="p-label">EMOTIONAL DYSREGULATION RISK</div>
          <div style="display: flex; align-items: baseline;">
            <span class="p-value">+80%</span>
            <span class="p-unit">HARVARD DATA</span>
          </div>
        </div>

        <!-- Beat 1 Headline -->
        <div class="editorial-headline-box" id="hlBox1">
          <div class="h-kicker">CRITICAL PARENTING FLAW</div>
          <div class="h-text">
            Fatherhood does not end when money is transferred: <span class="hl" id="hl1"><i></i>that is a dangerous illusion.</span>
          </div>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- SCENE 2: NEUROBIOLOGY & THE PATERNAL BRAIN (X = -1080)                    -->
      <!-- ========================================================================= -->
      <div class="scene-dossier" id="scene2">
        <div class="dossier-tag emerald" style="top: 150px; left: 60px;">NEUROSCIENCE // YALE CHILD STUDY CENTER</div>
        <div class="ghost-watermark" style="top: 140px; left: 60px; width: 960px;">YALE</div>

        <!-- Transparent AI Sprites: Loving Father Cradling Baby & Happy Brain -->
        <img class="sprite-cutout" id="spriteBabycare" src="assets/episode9_father_parenting/sprites/sprite_father_babycare.png" 
             style="top: 240px; left: 50px; width: 460px;" alt="Active Paternal Caregiving">
        <img class="sprite-cutout" id="spriteBrain" src="assets/episode9_father_parenting/sprites/sprite_brain_oxytocin.png" 
             style="top: 240px; right: 50px; width: 460px;" alt="Oxytocin Surge in Father's Brain">

        <!-- Hand-Crafted Modern SVG Hormonal Shift Calibration Chart -->
        <div class="vector-chart-panel" id="panelHormone" style="top: 750px; left: 60px; width: 960px; height: 320px;">
          <div class="chart-header">
            <span class="chart-title">Paternal Hormonal Shift During Active Caregiving</span>
            <span class="chart-sub">Feldman et al. (Yale University / PNAS)</span>
          </div>
          <svg width="900" height="220" viewBox="0 0 900 220" style="overflow: visible;">
            <!-- Grid Lines -->
            <line x1="60" y1="170" x2="860" y2="170" stroke="rgba(24,26,30,0.08)" stroke-width="1.5"/>
            <line x1="60" y1="20" x2="60" y2="170" stroke="rgba(24,26,30,0.08)" stroke-width="1.5"/>
            <!-- X Axis Marks -->
            <text x="80" y="195" fill="#848B98" font-family="JetBrains Mono" font-size="14" font-weight="600">Baseline (Passive Father)</text>
            <text x="480" y="195" fill="#2A9D8F" font-family="JetBrains Mono" font-size="14" font-weight="700">Active Care (Bathing & Carrying)</text>
            <!-- Oxytocin Curve (Coral/Gold Surge) -->
            <path id="curveOxytocin" d="M 80 150 Q 320 145, 500 45 T 820 30" fill="none" stroke="#E76F51" stroke-width="5" stroke-linecap="round" stroke-dasharray="1000" stroke-dashoffset="1000"/>
            <text x="700" y="22" fill="#E76F51" font-family="JetBrains Mono" font-weight="800" font-size="15">Oxytocin (+140%)</text>
            <!-- Testosterone Curve (Navy/Teal Dip) -->
            <path id="curveTesto" d="M 80 50 Q 320 55, 500 135 T 820 145" fill="none" stroke="#264653" stroke-width="3.5" stroke-dasharray="7 7"/>
            <text x="640" y="135" fill="#264653" font-family="JetBrains Mono" font-weight="700" font-size="14">Testosterone (-32%)</text>
            <!-- Data Dots -->
            <circle cx="820" cy="30" r="7" fill="#E76F51"/>
            <circle cx="820" cy="145" r="6" fill="#264653"/>
          </svg>
        </div>

        <div class="specimen-pill emerald" id="pillNeuro1" style="top: 1100px; left: 70px;">PREFRONTAL CORTEX: EMPATHY CIRCUITS</div>
        <div class="specimen-pill" id="pillNeuro2" style="top: 1100px; right: 70px;">OXYTOCIN PEAK: MATCHES NEW MOTHERS</div>

        <div class="hand-note emerald" id="hn2_1" style="top: 1160px; left: 80px; transform: rotate(-1.5deg);">
          A father's brain physically rewires when actively caring for his child
        </div>

        <!-- Beat 2 Headline -->
        <div class="editorial-headline-box emerald" id="hlBox2">
          <div class="h-kicker">PATERNAL NEUROBIOLOGY</div>
          <div class="h-text">
            When fathers bathe and carry their kids: <span class="hl g" id="hl2"><i></i>empathy circuits ignite instantly.</span>
          </div>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- SCENE 3: ROUGH PLAY & EMOTIONAL REGULATION (X = -2160)                    -->
      <!-- ========================================================================= -->
      <div class="scene-dossier" id="scene3">
        <div class="dossier-tag" style="top: 150px; left: 60px;">DEVELOPMENTAL PSYCHOLOGY // HARVARD CENTER</div>
        <div class="ghost-watermark" style="top: 140px; left: 60px; width: 960px;">RESILIENCE</div>

        <!-- Transparent AI Sprite: Dynamic Father Tossing Kid in Air -->
        <img class="sprite-cutout" id="spriteAirplane" src="assets/episode9_father_parenting/sprites/sprite_father_airplane.png" 
             style="top: 220px; left: 180px; width: 720px;" alt="Rough-and-Tumble Airplane Play">

        <!-- Modern SVG Dual-Bar Stress Resilience Benchmark -->
        <div class="vector-chart-panel" id="panelResilience" style="top: 860px; left: 60px; width: 960px; height: 260px;">
          <div class="chart-header">
            <span class="chart-title">Rough-and-Tumble Play: Impulse Control Index</span>
            <span class="chart-sub">Childhood Stress Resilience Benchmark</span>
          </div>
          <svg width="900" height="170" viewBox="0 0 900 170" style="overflow: visible;">
            <!-- Bar 1: Active Father Play -->
            <text x="60" y="40" fill="#181A1E" font-family="Plus Jakarta Sans" font-weight="700" font-size="16">Actively Engaged Father (Rough Play)</text>
            <rect x="60" y="55" width="700" height="34" rx="8" fill="rgba(231,111,81,0.12)" stroke="#E76F51" stroke-width="1.5"/>
            <rect id="barActive" x="60" y="55" width="0" height="34" rx="8" fill="#E76F51"/>
            <text x="780" y="78" fill="#E76F51" font-family="JetBrains Mono" font-weight="800" font-size="18">+40%</text>

            <!-- Bar 2: Passive / Absent Father -->
            <text x="60" y="118" fill="#848B98" font-family="Plus Jakarta Sans" font-weight="600" font-size="15">Passive / Financial-Only Presence</text>
            <rect x="60" y="130" width="700" height="34" rx="8" fill="rgba(24,26,30,0.05)" stroke="rgba(24,26,30,0.1)" stroke-width="1"/>
            <rect id="barPassive" x="60" y="130" width="0" height="34" rx="8" fill="#848B98"/>
            <text x="780" y="153" fill="#848B98" font-family="JetBrains Mono" font-weight="700" font-size="16">Baseline</text>
          </svg>
        </div>

        <div class="specimen-pill" id="pillPlay1" style="top: 1140px; left: 70px;">NEURAL TRAINING: IMPULSE CONTROL</div>
        <div class="specimen-pill coral" id="pillPlay2" style="top: 1140px; right: 70px;">STRESS RESILIENCE: +40% HIGHER</div>

        <!-- Beat 3 Headline -->
        <div class="editorial-headline-box" id="hlBox3">
          <div class="h-kicker">DEVELOPMENTAL PSYCHOLOGY</div>
          <div class="h-text">
            Physical play with dad: <span class="hl" id="hl3"><i></i>hardwires emotional control and stress resilience.</span>
          </div>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- SCENE 4: PROPHETIC ETHICS & AR-RA'I (X = -3240)                           -->
      <!-- ========================================================================= -->
      <div class="scene-dossier" id="scene4">
        <div class="dossier-tag emerald" style="top: 150px; left: 60px;">PROPHETIC ETHICS // AR-RA'I & MERCY</div>
        <div class="ghost-watermark" style="top: 140px; left: 60px; width: 960px;">AR-RA'I</div>

        <!-- Transparent AI Sprite: Golden Shepherd Emblem & Lantern -->
        <img class="sprite-cutout" id="spriteEmblem" src="assets/episode9_father_parenting/sprites/sprite_prophet_sunnah_emblem.png" 
             style="top: 220px; left: 260px; width: 560px;" alt="Ar-Rai Shepherd of Mercy Emblem">

        <!-- Calligraphic Archival Inscription Card -->
        <div class="vector-chart-panel" id="panelHadith" style="top: 800px; left: 60px; width: 960px; height: 310px; border-left: 6px solid var(--emerald-accent);">
          <div class="chart-header">
            <span class="chart-title" style="color: var(--emerald-accent);">Sahih Bukhari No. 5996 & 5997</span>
            <span class="chart-sub">Sunnah of the Prophet Muhammad ﷺ</span>
          </div>
          <div style="font-family: 'Amiri', serif; font-size: 38px; line-height: 1.5; color: #1B5E20; text-align: right; margin-bottom: 12px;">
            مَنْ لا يَرْحَمُ لا يُرْحَمُ
          </div>
          <div style="font-family: 'Instrument Serif', serif; font-style: italic; font-size: 32px; line-height: 1.35; color: var(--navy-accent);">
            "Whoever does not show mercy, will not be shown mercy."
          </div>
          <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 19px; line-height: 1.5; color: var(--ink-secondary); margin-top: 10px; border-top: 1px solid var(--border-card); padding-top: 10px;">
            The Prophet ﷺ carried his grandchildren during communal prayer—shattering toxic customs that viewed fatherly affection as weakness.
          </div>
        </div>

        <div class="specimen-pill emerald" id="pillIslam1" style="top: 1140px; left: 70px;">CONCEPT OF AR-RA'I: SHEPHERD OF SOULS</div>
        <div class="specimen-pill" id="pillIslam2" style="top: 1140px; right: 70px;">SURAH LUQMAN: HEART-TO-HEART DIALOGUE</div>

        <!-- Beat 4 Headline -->
        <div class="editorial-headline-box emerald" id="hlBox4">
          <div class="h-kicker">PROPHETIC WISDOM</div>
          <div class="h-text">
            In Islamic tradition, a father is Ar-Ra'i: <span class="hl g" id="hl4"><i></i>a shepherd of hearts and emotions.</span>
          </div>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- SCENE 5: THE LIFETIME RECORD & CLIMAX (X = -4320)                         -->
      <!-- ========================================================================= -->
      <div class="scene-dossier" id="scene5">
        <div class="dossier-tag" style="top: 150px; left: 60px;">FINAL VERDICT // THE LIFETIME RECORD</div>
        <div class="ghost-watermark" style="top: 140px; left: 60px; width: 960px;">PRESENCE</div>

        <!-- Transparent AI Sprite: Heartwarming Father & Child Hug -->
        <img class="sprite-cutout" id="spriteHug" src="assets/episode9_father_parenting/sprites/sprite_father_daughter_hug.png" 
             style="top: 220px; left: 200px; width: 680px;" alt="The Power of Fatherly Presence">

        <!-- Climax Outro Final Stamp -->
        <div id="outroFinalStamp">
          <div class="stamp-main">BE TRULY PRESENT</div>
          <div class="stamp-sub">GENUINE PRESENCE OUTWEIGHS OVERTIME BANK STATEMENTS</div>
        </div>

        <div class="hand-note" id="hn5_1" style="top: 1220px; left: 80px; transform: rotate(-1.5deg);">
          Your child won't recall your bank balance—their nervous system remembers your warm hand
        </div>

        <!-- Beat 5 Headline -->
        <div class="editorial-headline-box" id="hlBox5">
          <div class="h-kicker">THE FATHER'S LEGACY</div>
          <div class="h-text">
            What your child remembers forever: <span class="hl" id="hl5"><i></i>your presence when they were afraid.</span>
          </div>
        </div>
      </div>

    </div>
  </div>

  <!-- Whisper Word-Locked Subtitles -->
  <div id="subtitlesContainer">
    <div id="subtitlePill">Listening...</div>
  </div>

  <audio id="audioTrack" preload="auto">
    <source src="assets/episode9_father_parenting/audio_en/vo_ep9_en_master.wav" type="audio/wav">
    <source src="assets/episode9_father_parenting/audio_en/vo_ep9_en_master.mp3" type="audio/mpeg">
  </audio>
</div>

<script>
const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);

const DURATION = {aligned_data["total_duration"]};
const WORDS = {words_json};

/* Dynamic English Subtitles Logic */
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

function glideTo(time, targetX, dur = 0.90) {{
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

function popSprite(spriteId, time, scale = 1.0) {{
  tl.fromTo(spriteId, 
    {{ opacity: 0, scale: 0.6, y: 40 }}, 
    {{ opacity: 1, scale: scale, y: 0, duration: 0.75, ease: 'back.out(1.8)' }}, 
    time
  );
}}

// =========================================================================
// SCENE 1: HOOK & THE ATM FALLACY (0.0s - 14.5s)
// =========================================================================
cameraPush(0.0, 1.03, 14.0);
tl.to(['#scene1 .dossier-tag', '#scene1 .ghost-watermark'], {{ opacity: 1, duration: 0.6, ease: 'power2.out' }}, 0.3);

popSprite('#spriteDadAtm', 0.6, 1.0);
tl.fromTo(['#pillMyth1', '#pillMyth2'], {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.50, stagger: 0.15, ease: 'power3.out' }}, 1.2);
tl.fromTo('#hn1_1', {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.50, ease: 'back.out' }}, 2.0);
tl.fromTo('#cardTelemetry1', {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.55, ease: 'power3.out' }}, 3.0);

showHeadline('#hlBox1', 1.0, '#hl1');
hideHeadline('#hlBox1', 14.5);

// =========================================================================
// TRANSITION TO SCENE 2: NEUROBIOLOGY (14.5s - 15.45s)
// =========================================================================
glideTo(14.5, -1080, 0.90);

// =========================================================================
// SCENE 2: YALE NEUROBIOLOGY & OXYTOCIN (15.45s - 33.45s)
// =========================================================================
tl.to(['#scene2 .dossier-tag', '#scene2 .ghost-watermark'], {{ opacity: 1, duration: 0.6, ease: 'power2.out' }}, 15.6);
popSprite('#spriteBabycare', 15.8, 1.0);
popSprite('#spriteBrain', 16.4, 1.0);

tl.fromTo('#panelHormone', {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.65, ease: 'power3.out' }}, 17.0);
// Draw curves
tl.fromTo('#curveOxytocin', {{ strokeDashoffset: 1000 }}, {{ strokeDashoffset: 0, duration: 1.6, ease: 'power2.inOut' }}, 18.0);

tl.fromTo(['#pillNeuro1', '#pillNeuro2'], {{ opacity: 0, y: 15 }}, {{ opacity: 1, y: 0, duration: 0.50, stagger: 0.15, ease: 'power3.out' }}, 20.0);
tl.fromTo('#hn2_1', {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.50, ease: 'back.out' }}, 22.0);

showHeadline('#hlBox2', 16.0, '#hl2');
hideHeadline('#hlBox2', 33.5);

// =========================================================================
// TRANSITION TO SCENE 3: ROUGH PLAY & RESILIENCE (33.45s - 34.4s)
// =========================================================================
glideTo(33.5, -2160, 0.90);

// =========================================================================
// SCENE 3: ROUGH PLAY & HARVARD BENCHMARK (34.4s - 49.9s)
// =========================================================================
tl.to(['#scene3 .dossier-tag', '#scene3 .ghost-watermark'], {{ opacity: 1, duration: 0.6, ease: 'power2.out' }}, 34.6);
popSprite('#spriteAirplane', 34.8, 1.0);

tl.fromTo('#panelResilience', {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.65, ease: 'power3.out' }}, 36.0);
tl.to('#barActive', {{ width: 560, duration: 1.2, ease: 'power2.out' }}, 37.0);
tl.to('#barPassive', {{ width: 280, duration: 1.0, ease: 'power2.out' }}, 37.6);

tl.fromTo(['#pillPlay1', '#pillPlay2'], {{ opacity: 0, y: 15 }}, {{ opacity: 1, y: 0, duration: 0.50, stagger: 0.15, ease: 'power3.out' }}, 39.0);

showHeadline('#hlBox3', 35.0, '#hl3');
hideHeadline('#hlBox3', 49.9);

// =========================================================================
// TRANSITION TO SCENE 4: PROPHETIC MERCY & AR-RA'I (49.9s - 50.85s)
// =========================================================================
glideTo(49.9, -3240, 0.95);

// =========================================================================
// SCENE 4: ISLAMIC ETHICS & SUNNAH (50.85s - 69.91s)
// =========================================================================
tl.to(['#scene4 .dossier-tag', '#scene4 .ghost-watermark'], {{ opacity: 1, duration: 0.6, ease: 'power2.out' }}, 51.0);
popSprite('#spriteEmblem', 51.2, 1.0);

tl.fromTo('#panelHadith', {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.70, ease: 'power3.out' }}, 53.0);
tl.fromTo(['#pillIslam1', '#pillIslam2'], {{ opacity: 0, y: 15 }}, {{ opacity: 1, y: 0, duration: 0.50, stagger: 0.15, ease: 'power3.out' }}, 55.5);

showHeadline('#hlBox4', 51.5, '#hl4');
hideHeadline('#hlBox4', 69.9);

// =========================================================================
// TRANSITION TO SCENE 5: OUTRO & THE ENDURING PRESENCE (69.91s - 70.86s)
// =========================================================================
glideTo(69.9, -4320, 0.95);

// =========================================================================
// SCENE 5: OUTRO & FINAL VERDICT (70.86s - 85.16s)
// =========================================================================
tl.to(['#scene5 .dossier-tag', '#scene5 .ghost-watermark'], {{ opacity: 1, duration: 0.6, ease: 'power2.out' }}, 71.0);
popSprite('#spriteHug', 71.2, 1.0);

tl.fromTo('#outroFinalStamp', 
  {{ opacity: 0, scale: 2.2, rotate: -8 }}, 
  {{ opacity: 1, scale: 1, rotate: 0, duration: 0.40, ease: 'power4.in' }}, 
  73.0
);
tl.fromTo('#hn5_1', {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.50, ease: 'back.out' }}, 74.5);

showHeadline('#hlBox5', 72.0, '#hl5');

cameraPush(71.0, 0.98, 12.0);

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

    out_file = "index_ep9.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[OK] index_ep9.html successfully generated for English edition! ({len(html_content)} bytes)")

if __name__ == "__main__":
    main()
