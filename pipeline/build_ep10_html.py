#!/usr/bin/env python3
"""build_ep10_html.py — Build elegant, alus (smooth), non-dizzying documentary film for Episode 10:
The Mother's Microchimerism // Cellular Epigenetics & Prophetic Covenant.

Revisions applied per director feedback:
- REMOVED all camera shakes, aggressive stamp slams, and sudden runway whips.
- Replaced lateral runway whip with cinematic smooth cross-dissolves (opacity cross-fade + gentle vertical drift).
- Ultra-alus easing curves (power2.out, sine.inOut) for all sprite entries and headline reveals.
- REMOVED technical geometric grid lines.
- ADDED luxurious Islamic geometric rosette & arabesque watermark pattern (Girih / Khatam motif).
- Clean, subtitle-free layout with generous breathing room.
- Strict faceless Islamic characters (mouth + sweet smile expression only).
- Deterministic window.BANG_MOTION.seekFrame(t) hook.
"""
import os
import json

def main():
    aligned_path = "assets/episode10_mother_microchimerism/audio_en/ep10_en_words_aligned.json"
    with open(aligned_path, "r", encoding="utf-8") as f:
        aligned_data = json.load(f)

    total_duration = aligned_data["total_duration"]

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>The Mother's Microchimerism — Editorial Documentary Film</title>
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
  --emerald-accent: #1A5336;
  --emerald-soft: rgba(26, 83, 54, 0.10);
  --gold-accent: #D4AF37;
  --gold-soft: rgba(212, 175, 55, 0.18);
  --navy-accent: #1D3557;
  --border-card: rgba(26, 83, 54, 0.10);
  --card-shadow: 0 16px 40px rgba(26, 83, 54, 0.07), 0 4px 12px rgba(26, 83, 54, 0.03);
  --sprite-shadow: drop-shadow(0 20px 36px rgba(26, 83, 54, 0.14));
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

/* Islamic Arabesque Geometric Watermark Pattern (Replaced Cold Grid Lines) */
.ornament-overlay {{
  position: absolute; inset: 0;
  pointer-events: none;
  background-size: 140px 140px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140' viewBox='0 0 140 140'%3E%3Cg fill='none' stroke='%231A5336' stroke-width='1.1' opacity='0.045'%3E%3Crect x='41' y='41' width='58' height='58' rx='2'/%3E%3Crect x='41' y='41' width='58' height='58' rx='2' transform='rotate(45 70 70)'/%3E%3Ccircle cx='70' cy='70' r='21'/%3E%3Ccircle cx='70' cy='70' r='38' stroke-dasharray='4 4'/%3E%3Ccircle cx='0' cy='0' r='28'/%3E%3Ccircle cx='140' cy='0' r='28'/%3E%3Ccircle cx='0' cy='140' r='28'/%3E%3Ccircle cx='140' cy='140' r='28'/%3E%3Cpath d='M70 0 L70 140 M0 70 L140 70' stroke-dasharray='3 5'/%3E%3C/g%3E%3C/svg%3E");
  z-index: 5;
}}

/* Arch Corner Decorative Border Vignette */
.arch-border-overlay {{
  position: absolute; inset: 24px;
  border: 1px solid rgba(26, 83, 54, 0.08);
  border-radius: 36px;
  pointer-events: none;
  z-index: 7;
}}

/* Tactile Soft Grain */
.grain-overlay {{
  position: absolute; inset: 0;
  pointer-events: none;
  opacity: 0.055;
  mix-blend-mode: multiply;
  z-index: 6;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='260' height='260'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.75' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='260' height='260' filter='url(%23n)'/%3E%3C/svg%3E");
}}

/* Camera Rig & Scene Container */
#cameraRig {{
  position: absolute; inset: 0;
  will-change: transform;
}}

/* Stacked Cross-Dissolve Scenes (Zero Whip, Zero Dizziness) */
.scene {{
  position: absolute;
  inset: 0;
  width: 1080px; height: 1920px;
  overflow: hidden;
  opacity: 0;
  pointer-events: none;
  will-change: opacity, transform;
}}
.scene.active {{
  pointer-events: auto;
}}

/* Dossier Identity Tag */
.dossier-tag {{
  position: absolute;
  top: 90px; left: 80px;
  font-family: "JetBrains Mono", monospace;
  font-size: 15px;
  font-weight: 800;
  letter-spacing: 0.12em;
  color: var(--emerald-accent);
  background: #FFFFFF;
  padding: 8px 22px;
  border-left: 4.5px solid var(--emerald-accent);
  border-radius: 6px;
  z-index: 25;
  box-shadow: 0 6px 18px rgba(26, 83, 54, 0.08);
  text-transform: uppercase;
  opacity: 0;
}}
.dossier-tag.coral {{ border-left-color: var(--coral-accent); color: var(--coral-accent); }}
.dossier-tag.gold {{ border-left-color: var(--gold-accent); color: #8A6D1C; }}

/* Ghost Watermark Monogram */
.ghost-watermark {{
  position: absolute;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-weight: 900;
  font-size: 190px;
  line-height: 0.85;
  letter-spacing: -0.04em;
  color: rgba(26, 83, 54, 0.032);
  text-align: center;
  z-index: 4;
  pointer-events: none;
  white-space: nowrap;
  opacity: 0;
}}

/* Crisp Specimen Pill */
.specimen-pill {{
  position: absolute;
  padding: 10px 22px;
  background: #FFFFFF;
  border: 1.5px solid var(--border-card);
  color: var(--ink-secondary);
  font-family: "JetBrains Mono", monospace;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.10em;
  border-radius: 9999px;
  z-index: 26;
  box-shadow: 0 4px 16px rgba(26, 83, 54, 0.06);
  white-space: nowrap;
  opacity: 0;
}}
.specimen-pill.emerald {{ color: var(--emerald-accent); border-color: rgba(26, 83, 54, 0.25); }}
.specimen-pill.coral {{ color: var(--coral-accent); border-color: rgba(231,111,81,0.25); }}

/* Handwritten Field Notes */
.hand-note {{
  position: absolute;
  font-family: "Instrument Serif", serif;
  font-style: italic;
  font-size: 38px;
  line-height: 1.22;
  color: var(--emerald-accent);
  z-index: 32;
  letter-spacing: 0.01em;
  opacity: 0;
  max-width: 860px;
}}
.hand-note.coral {{ color: var(--coral-accent); }}

/* Clean Editorial Telemetry Card */
.telemetry-panel {{
  position: absolute;
  background: var(--bg-card);
  border: 1.5px solid var(--border-card);
  border-radius: 20px;
  padding: 24px 30px;
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
  color: var(--emerald-accent);
  line-height: 0.95;
}}
.telemetry-panel .p-value.coral {{ color: var(--coral-accent); }}
.telemetry-panel .p-unit {{
  font-family: "JetBrains Mono", monospace;
  font-size: 15px;
  font-weight: 700;
  color: var(--ink-muted);
  margin-left: 8px;
}}
.telemetry-panel .p-desc {{
  font-size: 17px;
  color: var(--ink-secondary);
  font-weight: 600;
  margin-top: 10px;
  line-height: 1.35;
}}

/* Cutout Transparent Sprites with Ultra-Subtle Breathing Float */
.sprite-cutout {{
  position: absolute;
  z-index: 20;
  pointer-events: none;
  filter: var(--sprite-shadow);
  transform-origin: center center;
}}

@keyframes gentleBreath {{
  0%, 100% {{ transform: translateY(0px); }}
  50% {{ transform: translateY(-7px); }}
}}
@keyframes softPulse {{
  0%, 100% {{ transform: scale(1.0); }}
  50% {{ transform: scale(1.025); }}
}}

.floating-anim {{
  animation: gentleBreath 6.8s ease-in-out infinite;
}}
.pulsing-anim {{
  animation: softPulse 5.0s ease-in-out infinite;
}}

/* Big Editorial Headline Card (Clean, No Subtitles) */
.editorial-headline-box {{
  position: absolute;
  left: 80px; right: 80px; bottom: 120px;
  background: #FFFFFF;
  border: 1.5px solid var(--border-card);
  border-radius: 28px;
  padding: 36px 42px;
  box-shadow: 0 24px 60px rgba(26, 83, 54, 0.09);
  z-index: 30;
  opacity: 0;
}}
.editorial-headline-box .h-kicker {{
  font-family: "JetBrains Mono", monospace;
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 0.16em;
  color: var(--emerald-accent);
  text-transform: uppercase;
  margin-bottom: 12px;
}}
.editorial-headline-box .h-text {{
  font-size: 34px;
  font-weight: 800;
  line-height: 1.30;
  color: var(--ink-primary);
  letter-spacing: -0.02em;
}}
.editorial-headline-box .h-text .hl {{
  color: var(--emerald-accent);
  position: relative;
  display: inline-block;
}}
.editorial-headline-box .h-text .hl i {{
  position: absolute;
  left: 0; bottom: -2px; width: 100%; height: 5px;
  background: var(--gold-accent);
  border-radius: 3px;
  transform-origin: left center;
  transform: scaleX(0);
}}

/* Outro Slate (Smooth Soft Settle) */
.outro-slate {{
  position: absolute;
  left: 50%; top: 48%;
  transform: translate(-50%, -50%);
  width: 900px;
  background: #FFFFFF;
  border: 2px solid var(--border-card);
  border-radius: 36px;
  padding: 60px 50px;
  text-align: center;
  box-shadow: 0 32px 80px rgba(26, 83, 54, 0.12);
  z-index: 35;
  opacity: 0;
}}
.outro-slate .o-title {{
  font-size: 48px;
  font-weight: 900;
  line-height: 1.15;
  letter-spacing: -0.03em;
  color: var(--emerald-accent);
  margin-bottom: 18px;
}}
.outro-slate .o-desc {{
  font-size: 24px;
  font-weight: 600;
  color: var(--ink-secondary);
  line-height: 1.45;
  max-width: 780px;
  margin: 0 auto 30px auto;
}}
.outro-slate .o-badge {{
  display: inline-block;
  padding: 12px 28px;
  background: var(--emerald-soft);
  color: var(--emerald-accent);
  font-family: "JetBrains Mono", monospace;
  font-size: 15px;
  font-weight: 800;
  letter-spacing: 0.12em;
  border-radius: 9999px;
  text-transform: uppercase;
}}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
</head>
<body>
<div id="stage">
  <div class="ornament-overlay"></div>
  <div class="arch-border-overlay"></div>
  <div class="grain-overlay"></div>

  <div id="cameraRig">

    <!-- ===================================================================
         SCENE 1: THE INVISIBLE PASSENGER (0.0s - 9.9s)
         =================================================================== -->
    <div class="scene" id="scene1">
      <div class="dossier-tag">CELLULAR EPIGENETICS • DOSSIER #10</div>
      <div class="ghost-watermark" style="top: 180px; left: 60px;">01 / PASSENGER</div>

      <!-- Sprites -->
      <img class="sprite-cutout floating-anim" id="spriteMotherBaby" 
           src="assets/episode10_mother_microchimerism/sprites/sprite_mother_baby_faceless.png" 
           style="width: 720px; top: 280px; left: 180px;" alt="Mother and Baby">
      
      <img class="sprite-cutout pulsing-anim" id="spriteFetalCells1" 
           src="assets/episode10_mother_microchimerism/sprites/sprite_glowing_fetal_cells.png" 
           style="width: 380px; top: 760px; right: 80px;" alt="Glowing Cells">

      <!-- Pills & Annotations -->
      <div class="specimen-pill emerald" id="pillFetal1" style="top: 240px; right: 100px;">FETAL MICROCHIMERISM</div>
      <div class="specimen-pill coral" id="pillFetal2" style="top: 1020px; left: 90px;">CELLULAR TRANSLOCATION</div>

      <div class="hand-note" id="hn1_1" style="top: 1100px; left: 100px;">
        "You never truly left her body..."
      </div>

      <!-- Telemetry Card -->
      <div class="telemetry-panel" id="cardTelemetry1" style="top: 1190px; left: 90px; right: 90px;">
        <div class="p-label">CELLULAR RESIDENCE DURATION</div>
        <div class="p-value">30+<span class="p-unit">YEARS POST-PARTUM</span></div>
        <div class="p-desc">Fetal stem cells cross the placenta, establishing eternal colonies inside maternal organs.</div>
      </div>

      <!-- Headline Box -->
      <div class="editorial-headline-box" id="hlBox1">
        <div class="h-kicker">CELLULAR EPIGENETICS</div>
        <div class="h-text">
          When you left your mother's womb: <span class="hl" id="hl1"><i></i>your living cells remained inside her heart and brain.</span>
        </div>
      </div>
    </div>

    <!-- ===================================================================
         SCENE 2: MATERNAL HEART REGENERATION (10.43s - 25.6s)
         =================================================================== -->
    <div class="scene" id="scene2">
      <div class="dossier-tag coral">CIRCULATION RESEARCH (2011) • MT. SINAI</div>
      <div class="ghost-watermark" style="top: 180px; left: 60px;">02 / CARDIAC</div>

      <!-- Sprites -->
      <img class="sprite-cutout pulsing-anim" id="spriteHeartRepair" 
           src="assets/episode10_mother_microchimerism/sprites/sprite_anatomical_heart_repair.png" 
           style="width: 680px; top: 290px; left: 200px;" alt="Heart Repair">
      
      <img class="sprite-cutout floating-anim" id="spriteFetalCells2" 
           src="assets/episode10_mother_microchimerism/sprites/sprite_glowing_fetal_cells.png" 
           style="width: 340px; top: 820px; left: 80px;" alt="Stem Cells">

      <div class="specimen-pill coral" id="pillCardio1" style="top: 250px; right: 80px;">CARDIOMYOCYTE CONVERSION</div>
      <div class="specimen-pill emerald" id="pillCardio2" style="top: 960px; right: 100px;">STEM CELL HOMING</div>

      <div class="hand-note coral" id="hn2_1" style="top: 1040px; left: 100px;">
        "When her heart aches, her child's cells rush to repair it."
      </div>

      <!-- SVG ECG Panel -->
      <div class="telemetry-panel" id="panelHeartECG" style="top: 1140px; left: 90px; right: 90px;">
        <div class="p-label">CARDIOMYOCYTE REGENERATION RATE</div>
        <div class="p-value coral">ACTIVE<span class="p-unit">DIFFERENTIATION</span></div>
        <svg width="100%" height="70" viewBox="0 0 800 70" style="margin-top: 12px;">
          <path id="curveECG" d="M 0 35 L 200 35 L 220 15 L 240 55 L 260 20 L 280 45 L 300 35 L 500 35 L 520 15 L 540 55 L 560 20 L 580 45 L 600 35 L 800 35" 
                fill="none" stroke="#E76F51" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"
                stroke-dasharray="1000" stroke-dashoffset="0"/>
        </svg>
        <div class="p-desc">Fetal stem cells transform directly into functional, beating heart muscle cells upon injury.</div>
      </div>

      <!-- Headline Box -->
      <div class="editorial-headline-box" id="hlBox2">
        <div class="h-kicker">MATERNAL RESCUE MECHANISM</div>
        <div class="h-text">
          When a pregnant mother suffers heart injury: <span class="hl" id="hl2"><i></i>fetal stem cells rush across the placenta to heal her.</span>
        </div>
      </div>
    </div>

    <!-- ===================================================================
         SCENE 3: THE 94-YEAR BRAIN LEGACY (26.12s - 43.2s)
         =================================================================== -->
    <div class="scene" id="scene3">
      <div class="dossier-tag">FRED HUTCHINSON CENTER • PLOS ONE</div>
      <div class="ghost-watermark" style="top: 180px; left: 60px;">03 / NEURAL</div>

      <!-- Sprites -->
      <img class="sprite-cutout floating-anim" id="spriteGrandmother" 
           src="assets/episode10_mother_microchimerism/sprites/sprite_grandmother_faceless.png" 
           style="width: 700px; top: 290px; left: 190px;" alt="Grandmother">

      <div class="specimen-pill emerald" id="pillBrain1" style="top: 250px; right: 100px;">Y-CHROMOSOME SEQUENCE</div>
      <div class="specimen-pill emerald" id="pillBrain2" style="top: 980px; left: 90px;">CEREBRAL MICROCHIMERISM</div>

      <div class="hand-note" id="hn3_1" style="top: 1060px; left: 100px;">
        "Even in her nineties, a mother carries her child's code."
      </div>

      <div class="telemetry-panel" id="panelBrainData" style="top: 1160px; left: 90px; right: 90px;">
        <div class="p-label">MAXIMUM RECORDED SUBJECT AGE</div>
        <div class="p-value">94<span class="p-unit">YEARS OLD</span></div>
        <div class="p-desc">Child DNA was detected in 63% of female brains autopsied. Stored in memory and sensory centers for a lifetime.</div>
      </div>

      <!-- Headline Box -->
      <div class="editorial-headline-box" id="hlBox3">
        <div class="h-kicker">LIFETIME NEURAL MARK</div>
        <div class="h-text">
          For nearly a century: <span class="hl" id="hl3"><i></i>children leave an indelible biological mark in her memory centers.</span>
        </div>
      </div>
    </div>

    <!-- ===================================================================
         SCENE 4: PROPHETIC HADITH: 3 TO 1 (43.75s - 64.4s)
         =================================================================== -->
    <div class="scene" id="scene4">
      <div class="dossier-tag gold">SAHIH BUKHARI 5971 • SAHIH MUSLIM 2548</div>
      <div class="ghost-watermark" style="top: 180px; left: 60px;">04 / SUNNAH</div>

      <!-- Sprites -->
      <img class="sprite-cutout floating-anim" id="spriteMotherSon" 
           src="assets/episode10_mother_microchimerism/sprites/sprite_mother_son_prayer_faceless.png" 
           style="width: 680px; top: 280px; left: 200px;" alt="Son and Mother">
      
      <img class="sprite-cutout pulsing-anim" id="spriteHadithBadge" 
           src="assets/episode10_mother_microchimerism/sprites/sprite_hadith_3x_badge.png" 
           style="width: 320px; top: 820px; right: 70px;" alt="3X Priority Badge">

      <div class="specimen-pill coral" id="pillIslam1" style="top: 250px; left: 90px;">3:1 COMPANIONSHIP</div>
      <div class="specimen-pill emerald" id="pillIslam2" style="top: 980px; left: 90px;">ETERNAL HONOUR</div>

      <!-- Hadith Hierarchy Card -->
      <div class="telemetry-panel" id="panelHadithList" style="top: 1060px; left: 90px; right: 90px; padding: 26px 32px;">
        <div class="p-label">PROPHETIC COMPANIONSHIP ORDER</div>
        <div style="font-size: 24px; font-weight: 800; line-height: 1.6; margin-top: 8px;">
          <div style="color: var(--emerald-accent);">1. UMMUKA <span style="font-size: 18px; color: var(--ink-secondary); font-weight: 600;">(YOUR MOTHER)</span></div>
          <div style="color: var(--emerald-accent);">2. UMMUKA <span style="font-size: 18px; color: var(--ink-secondary); font-weight: 600;">(YOUR MOTHER)</span></div>
          <div style="color: var(--emerald-accent);">3. UMMUKA <span style="font-size: 18px; color: var(--ink-secondary); font-weight: 600;">(YOUR MOTHER)</span></div>
          <div style="color: var(--coral-accent); margin-top: 4px;">4. ABUKA <span style="font-size: 18px; color: var(--ink-secondary); font-weight: 600;">(YOUR FATHER)</span></div>
        </div>
      </div>

      <!-- Headline Box -->
      <div class="editorial-headline-box" id="hlBox4">
        <div class="h-kicker">PROPHETIC COVENANT</div>
        <div class="h-text">
          The Prophet ﷺ declared the mother's priority 3 times: <span class="hl" id="hl4"><i></i>mirroring the biological reality that she carried you forever.</span>
        </div>
      </div>
    </div>

    <!-- ===================================================================
         SCENE 5: OUTRO & STITCHED TOGETHER (64.91s - 76.61s)
         =================================================================== -->
    <div class="scene" id="scene5">
      <div class="dossier-tag">THE FINAL VERDICT • DOSSIER #10</div>
      <div class="ghost-watermark" style="top: 180px; left: 60px;">05 / FOREVER</div>

      <!-- Sprites -->
      <img class="sprite-cutout pulsing-anim" id="spriteHoldingHands" 
           src="assets/episode10_mother_microchimerism/sprites/sprite_holding_mother_hand.png" 
           style="width: 720px; top: 290px; left: 180px;" alt="Holding Hands">

      <div class="hand-note" id="hn5_1" style="top: 980px; left: 100px;">
        "You are not just a chapter in her life. You are stitched into her forever."
      </div>

      <!-- Outro Final Stamp Slate -->
      <div class="outro-slate" id="outroFinalStamp">
        <div class="o-title">CALL YOUR MOTHER TODAY.</div>
        <div class="o-desc">Your living cells are still beating inside her heart. Cherish the woman whose very biology carried you into existence.</div>
        <div class="o-badge">AG-BANG DOCUMENTARY • EPISODE 10</div>
      </div>

      <!-- Headline Box -->
      <div class="editorial-headline-box" id="hlBox5">
        <div class="h-kicker">THE ETERNAL CONNECTION</div>
        <div class="h-text">
          Biologically and spiritually: <span class="hl" id="hl5"><i></i>you are stitched into her living organs forever.</span>
        </div>
      </div>
    </div>

  </div>

  <audio id="audioTrack" preload="auto">
    <source src="assets/episode10_mother_microchimerism/audio_en/vo_ep10_en_master.wav" type="audio/wav">
    <source src="assets/episode10_mother_microchimerism/audio_en/vo_ep10_en_master.mp3" type="audio/mpeg">
  </audio>
</div>

<script>
const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);

const DURATION = {total_duration};

/* Master GSAP Timeline */
const tl = gsap.timeline({{ paused: true }});
const cameraRig = $('#cameraRig');

// =========================================================================
// ALUS (SMOOTH) MOTION HELPER FUNCTIONS — ZERO SHAKE, ZERO WHIP
// =========================================================================

function crossDissolve(fadeOutScene, fadeInScene, time, dur = 0.85) {{
  if (fadeOutScene) {{
    tl.to(fadeOutScene, {{ opacity: 0, duration: dur, ease: 'sine.inOut' }}, time);
    tl.set(fadeOutScene, {{ className: '-=active' }}, time + dur);
  }}
  if (fadeInScene) {{
    tl.fromTo(fadeInScene, 
      {{ opacity: 0, y: 15 }}, 
      {{ opacity: 1, y: 0, duration: dur, ease: 'sine.inOut' }}, 
      time + 0.10
    );
    tl.set(fadeInScene, {{ className: '+=active' }}, time);
  }}
}}

function gentleCameraBreath(time, targetScale, dur = 9.0) {{
  tl.to(cameraRig, {{ scale: targetScale, transformOrigin: '540px 960px', duration: dur, ease: 'power1.out' }}, time);
}}

function revealHeadline(boxId, time, hlId) {{
  tl.fromTo(boxId, 
    {{ opacity: 0, y: 22 }}, 
    {{ opacity: 1, y: 0, duration: 0.65, ease: 'power2.out' }}, 
    time
  );
  if (hlId) {{
    tl.to(`${{hlId}} i`, {{ scaleX: 1, duration: 0.80, ease: 'power2.out' }}, time + 0.35);
  }}
}}

function hideHeadline(boxId, time) {{
  tl.to(boxId, {{ opacity: 0, y: -12, duration: 0.50, ease: 'sine.in' }}, time);
}}

function revealSprite(spriteId, time, scale = 1.0) {{
  tl.fromTo(spriteId, 
    {{ opacity: 0, scale: scale * 0.94, y: 24 }}, 
    {{ opacity: 1, scale: scale, y: 0, duration: 0.90, ease: 'power2.out' }}, 
    time
  );
}}

// =========================================================================
// SCENE 1: HOOK & THE INVISIBLE PASSENGER (0.0s - 9.9s)
// =========================================================================
tl.set('#scene1', {{ opacity: 1, className: '+=active' }}, 0);
gentleCameraBreath(0.0, 1.025, 9.5);

tl.fromTo(['#scene1 .dossier-tag', '#scene1 .ghost-watermark'], 
  {{ opacity: 0, y: -10 }}, 
  {{ opacity: 1, y: 0, duration: 0.70, ease: 'power2.out' }}, 
  0.2
);

revealSprite('#spriteMotherBaby', 0.4, 1.0);
revealSprite('#spriteFetalCells1', 0.8, 1.0);

tl.fromTo(['#pillFetal1', '#pillFetal2'], 
  {{ opacity: 0, y: 15 }}, 
  {{ opacity: 1, y: 0, duration: 0.60, stagger: 0.15, ease: 'power2.out' }}, 
  1.2
);
tl.fromTo('#hn1_1', 
  {{ opacity: 0, y: 12 }}, 
  {{ opacity: 1, y: 0, duration: 0.60, ease: 'power2.out' }}, 
  1.9
);
tl.fromTo('#cardTelemetry1', 
  {{ opacity: 0, y: 18 }}, 
  {{ opacity: 1, y: 0, duration: 0.65, ease: 'power2.out' }}, 
  2.6
);

revealHeadline('#hlBox1', 0.7, '#hl1');
hideHeadline('#hlBox1', 9.5);

// =========================================================================
// CROSS-DISSOLVE TO SCENE 2: CARDIAC REPAIR (9.6s - 10.45s)
// =========================================================================
crossDissolve('#scene1', '#scene2', 9.6, 0.85);

// =========================================================================
// SCENE 2: MT. SINAI CARDIAC REGENERATION (10.43s - 25.6s)
// =========================================================================
gentleCameraBreath(10.4, 1.028, 14.5);

tl.fromTo(['#scene2 .dossier-tag', '#scene2 .ghost-watermark'], 
  {{ opacity: 0, y: -10 }}, 
  {{ opacity: 1, y: 0, duration: 0.70, ease: 'power2.out' }}, 
  10.7
);

revealSprite('#spriteHeartRepair', 10.8, 1.0);
revealSprite('#spriteFetalCells2', 11.4, 1.0);

tl.fromTo('#panelHeartECG', 
  {{ opacity: 0, y: 20 }}, 
  {{ opacity: 1, y: 0, duration: 0.70, ease: 'power2.out' }}, 
  12.0
);
tl.fromTo('#curveECG', 
  {{ strokeDashoffset: 1000 }}, 
  {{ strokeDashoffset: 0, duration: 2.4, ease: 'power2.inOut' }}, 
  12.8
);

tl.fromTo(['#pillCardio1', '#pillCardio2'], 
  {{ opacity: 0, y: 15 }}, 
  {{ opacity: 1, y: 0, duration: 0.60, stagger: 0.15, ease: 'power2.out' }}, 
  14.5
);
tl.fromTo('#hn2_1', 
  {{ opacity: 0, y: 12 }}, 
  {{ opacity: 1, y: 0, duration: 0.60, ease: 'power2.out' }}, 
  16.0
);

revealHeadline('#hlBox2', 11.2, '#hl2');
hideHeadline('#hlBox2', 25.4);

// =========================================================================
// CROSS-DISSOLVE TO SCENE 3: 94-YEAR BRAIN LEGACY (25.5s - 26.35s)
// =========================================================================
crossDissolve('#scene2', '#scene3', 25.5, 0.85);

// =========================================================================
// SCENE 3: FRED HUTCHINSON BRAIN AUTOPSY (26.12s - 43.2s)
// =========================================================================
gentleCameraBreath(26.1, 1.025, 16.5);

tl.fromTo(['#scene3 .dossier-tag', '#scene3 .ghost-watermark'], 
  {{ opacity: 0, y: -10 }}, 
  {{ opacity: 1, y: 0, duration: 0.70, ease: 'power2.out' }}, 
  26.4
);

revealSprite('#spriteGrandmother', 26.6, 1.0);

tl.fromTo('#panelBrainData', 
  {{ opacity: 0, y: 20 }}, 
  {{ opacity: 1, y: 0, duration: 0.70, ease: 'power2.out' }}, 
  27.6
);
tl.fromTo(['#pillBrain1', '#pillBrain2'], 
  {{ opacity: 0, y: 15 }}, 
  {{ opacity: 1, y: 0, duration: 0.60, stagger: 0.15, ease: 'power2.out' }}, 
  29.5
);
tl.fromTo('#hn3_1', 
  {{ opacity: 0, y: 12 }}, 
  {{ opacity: 1, y: 0, duration: 0.60, ease: 'power2.out' }}, 
  31.5
);

revealHeadline('#hlBox3', 27.0, '#hl3');
hideHeadline('#hlBox3', 43.0);

// =========================================================================
// CROSS-DISSOLVE TO SCENE 4: PROPHETIC HADITH (43.1s - 43.95s)
// =========================================================================
crossDissolve('#scene3', '#scene4', 43.1, 0.85);

// =========================================================================
// SCENE 4: 3:1 PRIORITY SUNNAH (43.75s - 64.4s)
// =========================================================================
gentleCameraBreath(43.7, 1.025, 20.0);

tl.fromTo(['#scene4 .dossier-tag', '#scene4 .ghost-watermark'], 
  {{ opacity: 0, y: -10 }}, 
  {{ opacity: 1, y: 0, duration: 0.70, ease: 'power2.out' }}, 
  44.0
);

revealSprite('#spriteMotherSon', 44.2, 1.0);
revealSprite('#spriteHadithBadge', 44.9, 1.0);

tl.fromTo('#panelHadithList', 
  {{ opacity: 0, y: 20 }}, 
  {{ opacity: 1, y: 0, duration: 0.70, ease: 'power2.out' }}, 
  46.0
);
tl.fromTo(['#pillIslam1', '#pillIslam2'], 
  {{ opacity: 0, y: 15 }}, 
  {{ opacity: 1, y: 0, duration: 0.60, stagger: 0.15, ease: 'power2.out' }}, 
  48.0
);

revealHeadline('#hlBox4', 44.5, '#hl4');
hideHeadline('#hlBox4', 64.2);

// =========================================================================
// CROSS-DISSOLVE TO SCENE 5: OUTRO (64.3s - 65.15s)
// =========================================================================
crossDissolve('#scene4', '#scene5', 64.3, 0.85);

// =========================================================================
// SCENE 5: OUTRO & FINAL VERDICT (64.91s - 76.61s)
// =========================================================================
gentleCameraBreath(64.9, 1.020, 11.5);

tl.fromTo(['#scene5 .dossier-tag', '#scene5 .ghost-watermark'], 
  {{ opacity: 0, y: -10 }}, 
  {{ opacity: 1, y: 0, duration: 0.70, ease: 'power2.out' }}, 
  65.1
);

revealSprite('#spriteHoldingHands', 65.3, 1.0);

// Smooth, dignified settle for final slate (No slam, no rotation tilt)
tl.fromTo('#outroFinalStamp', 
  {{ opacity: 0, scale: 0.94, y: 25 }}, 
  {{ opacity: 1, scale: 1, y: 0, duration: 0.85, ease: 'power2.out' }}, 
  66.8
);

tl.fromTo('#hn5_1', 
  {{ opacity: 0, y: 12 }}, 
  {{ opacity: 1, y: 0, duration: 0.60, ease: 'power2.out' }}, 
  68.5
);

revealHeadline('#hlBox5', 65.8, '#hl5');

/* Headless Puppeteer Seek Hook */
window.BANG_MOTION = {{
  ready: true,
  seekFrame: function(t) {{
    tl.pause(t, false);
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

    out_file = "index_ep10.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[OK] index_ep10.html rebuilt with Alus (smooth) transitions, Islamic arabesque pattern, and zero shake! ({len(html_content)} bytes)")

if __name__ == "__main__":
    main()
