import os
import json
import numpy as np
import scipy.io.wavfile as wavfile
from scipy.signal import butter, lfilter
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(PROJECT_ROOT, "assets", "episode6_project_azorian", "audio")
SR = 24000  # 24kHz master rate matching Kokoro TTS

CUES_PATH = os.path.join(AUDIO_DIR, "vo_cues_azorian_full.json")
with open(CUES_PATH, "r", encoding="utf-8") as f:
    manifest = json.load(f)

TOTAL_DUR = manifest["total_duration"]
TOTAL_SAMPLES = int(TOTAL_DUR * SR)

def butter_lowpass_filter(data, cutoff, fs, order=3):
    nyq = 0.5 * fs
    normal_cutoff = min(cutoff / nyq, 0.999)
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return lfilter(b, a, data)

def butter_bandpass_filter(data, lowcut, highcut, fs, order=2):
    nyq = 0.5 * fs
    low = max(lowcut / nyq, 0.001)
    high = min(highcut / nyq, 0.999)
    b, a = butter(order, [low, high], btype='band', analog=False)
    return lfilter(b, a, data)

def butter_highpass_filter(data, cutoff, fs, order=2):
    nyq = 0.5 * fs
    normal_cutoff = max(cutoff / nyq, 0.001)
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return lfilter(b, a, data)

# 1. Vox Investigative Pulse & Atmospheric Ocean Bed
def generate_investigative_drone():
    t = np.linspace(0, TOTAL_DUR, TOTAL_SAMPLES, endpoint=False)
    
    # Sub-bass foundation (42Hz - 48Hz slow beating abyss resonance)
    sub = (np.sin(2 * np.pi * 44.0 * t) * 0.7 + np.sin(2 * np.pi * 47.5 * t) * 0.3) * 0.13
    
    # 120 BPM subtle clock/sonar pulse (2 pulses per second)
    clock_pulse = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    tick_interval = int(0.5 * SR)
    for i in range(0, TOTAL_SAMPLES - int(0.04 * SR), tick_interval):
        dt = np.linspace(0, 0.04, int(0.04 * SR), endpoint=False)
        tick = np.sin(2 * np.pi * 920.0 * dt) * np.exp(-dt * 95.0) * 0.032
        clock_pulse[i:i + len(tick)] += tick
        
    # Tension swell in Act 4 (The Snap & Radiation: 78s - 101s)
    tension_pad = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    p_mask = (t >= 78.0) & (t < 101.0)
    p_dt = t[p_mask] - 78.0
    p_osc = (np.sin(2 * np.pi * 164.8 * p_dt) * 0.4 +
             np.sin(2 * np.pi * 196.0 * p_dt) * 0.3 +
             np.sin(2 * np.pi * 246.9 * p_dt) * 0.3)
    p_env = np.clip(p_dt / 3.0, 0, 1) * np.clip((101.0 - t[p_mask]) / 3.0, 0, 1)
    tension_pad[p_mask] = p_osc * p_env * 0.09

    return sub + clock_pulse + tension_pad

# 2. Tactile Foley Generator
def generate_tactile_foley():
    foley = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    np.random.seed(84000)

    # A. Folder Open / Paper Dossier Slap
    def add_dossier_open(start_t):
        s_idx = int(start_t * SR)
        dur = 0.45
        e_idx = min(s_idx + int(dur * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        thud = np.sin(2 * np.pi * 95.0 * dt) * np.exp(-dt * 30.0) * 0.45
        whoosh = butter_bandpass_filter(np.random.normal(0, 1, len(dt)), 800, 3200, SR) * np.exp(-dt * 12.0) * 0.25
        clink = np.sin(2 * np.pi * 3800.0 * dt) * np.exp(-dt * 120.0) * 0.22
        foley[s_idx:e_idx] += (thud + whoosh + clink)

    # B. Sonar Ping (Acoustic deep-sea ping with long underwater reverb tail)
    def add_sonar_ping(start_t, freq=1480.0):
        s_idx = int(start_t * SR)
        dur = 1.8
        e_idx = min(s_idx + int(dur * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        ping = np.sin(2 * np.pi * freq * dt) * np.exp(-dt * 3.8) * 0.28
        tail = np.sin(2 * np.pi * (freq * 0.5) * dt) * np.exp(-dt * 1.8) * 0.10
        foley[s_idx:e_idx] += (ping + tail)

    # C. Underwater Acoustic Implosion Blast (SOSUS Detection)
    def add_implosion_blast(start_t):
        s_idx = int(start_t * SR)
        dur = 2.4
        e_idx = min(s_idx + int(dur * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        sub_rumble = np.sin(2 * np.pi * 38.0 * dt) * np.exp(-dt * 1.4) * 0.65
        concussive = np.random.normal(0, 1, len(dt))
        concussive = butter_lowpass_filter(concussive, 220, SR) * np.exp(-dt * 2.8) * 0.55
        foley[s_idx:e_idx] += (sub_rumble + concussive)

    # D. Teletype Cable Chatter
    def add_teletype(start_t, length=2.2):
        s_idx = int(start_t * SR)
        e_idx = min(s_idx + int(length * SR), TOTAL_SAMPLES)
        for t_off in np.arange(0, length, 0.09):
            pos = s_idx + int(t_off * SR)
            if pos + 600 < e_idx:
                click_dt = np.linspace(0, 0.025, 600, endpoint=False)
                click = np.sin(2 * np.pi * 1800 * click_dt) * np.exp(-click_dt * 180) * 0.15
                foley[pos:pos+600] += click

    # E. Hydraulic Claws Groan & Mechanical Clamp
    def add_hydraulic_clamp(start_t):
        s_idx = int(start_t * SR)
        dur = 2.2
        e_idx = min(s_idx + int(dur * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        groan_freq = 110.0 + 35.0 * np.sin(2 * np.pi * 1.8 * dt)
        groan = np.sin(2 * np.pi * groan_freq * dt) * np.exp(-dt * 1.2) * 0.32
        metallic_scrape = butter_bandpass_filter(np.random.normal(0, 1, len(dt)), 1200, 4800, SR) * np.exp(-dt * 1.5) * 0.18
        # Final locking latch impact
        latch_pos = int(1.2 * SR)
        if latch_pos < len(dt):
            dt_latch = dt[latch_pos:] - dt[latch_pos]
            latch = np.sin(2 * np.pi * 180.0 * dt_latch) * np.exp(-dt_latch * 35.0) * 0.55
            foley[s_idx + latch_pos:e_idx] += latch
        foley[s_idx:e_idx] += (groan + metallic_scrape)

    # F. Catastrophic Metal Fracture & Snap
    def add_claw_snap(start_t):
        s_idx = int(start_t * SR)
        dur = 2.8
        e_idx = min(s_idx + int(dur * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        snap_crack = butter_highpass_filter(np.random.normal(0, 1, len(dt)), 2400, SR) * np.exp(-dt * 45.0) * 0.85
        iron_twang = np.sin(2 * np.pi * 320.0 * dt) * np.exp(-dt * 8.0) * 0.55
        plunge_boom = np.sin(2 * np.pi * 48.0 * dt) * np.exp(-dt * 1.2) * 0.60
        foley[s_idx:e_idx] += (snap_crack + iron_twang + plunge_boom)

    # G. Radiation Geiger Clicks & Alarm Pulse
    def add_radiation_geiger(start_t, length=5.0):
        s_idx = int(start_t * SR)
        e_idx = min(s_idx + int(length * SR), TOTAL_SAMPLES)
        # Random chaotic Geiger discharge clicks
        click_times = np.sort(np.random.uniform(0, length, int(length * 28)))
        for ct in click_times:
            pos = s_idx + int(ct * SR)
            if pos + 240 < e_idx:
                click_dt = np.linspace(0, 0.01, 240, endpoint=False)
                click = (np.random.normal(0, 1, 240) * 0.5 + np.sin(2 * np.pi * 3200 * click_dt) * 0.5) * np.exp(-click_dt * 450) * 0.32
                foley[pos:pos+240] += click
        # Two warning beeps
        for beep_t in [1.5, 3.2]:
            b_pos = s_idx + int(beep_t * SR)
            if b_pos + int(0.25 * SR) < e_idx:
                b_dt = np.linspace(0, 0.25, int(0.25 * SR), endpoint=False)
                beep = np.sin(2 * np.pi * 1050.0 * b_dt) * np.exp(-b_dt * 5.0) * 0.28
                foley[b_pos:b_pos + len(beep)] += beep

    # H. Solemn Ship's Bell & Soviet Naval Hymn motif
    def add_ceremonial_funeral(start_t):
        s_idx = int(start_t * SR)
        # Deep brass bell tolls at start
        for b_off in [0.0, 3.5, 7.0]:
            b_pos = s_idx + int(b_off * SR)
            dur = 3.2
            if b_pos + int(dur * SR) < TOTAL_SAMPLES:
                b_dt = np.linspace(0, dur, int(dur * SR), endpoint=False)
                bell = (np.sin(2 * np.pi * 420.0 * b_dt) * 0.5 + np.sin(2 * np.pi * 840.0 * b_dt) * 0.3 + np.sin(2 * np.pi * 1260.0 * b_dt) * 0.2) * np.exp(-b_dt * 1.1) * 0.38
                foley[b_pos:b_pos + len(bell)] += bell
        # Low orchestral brass chord progression (USSR Anthem opening C-F-G-C solemn cadence)
        hymn_dur = 8.0
        h_pos = s_idx + int(1.2 * SR)
        if h_pos + int(hymn_dur * SR) < TOTAL_SAMPLES:
            h_dt = np.linspace(0, hymn_dur, int(hymn_dur * SR), endpoint=False)
            chord = (np.sin(2 * np.pi * 130.81 * h_dt) * 0.4 +
                     np.sin(2 * np.pi * 174.61 * h_dt) * 0.3 +
                     np.sin(2 * np.pi * 196.00 * h_dt) * 0.3)
            chord_env = np.clip(h_dt / 2.0, 0, 1) * np.clip((hymn_dur - h_dt) / 2.5, 0, 1)
            foley[h_pos:h_pos + len(chord)] += chord * chord_env * 0.14

    # I. Heavy Rubber Stamp Slam (Outro Declassification)
    def add_stamp_slam(start_t):
        s_idx = int(start_t * SR)
        dur = 0.75
        e_idx = min(s_idx + int(dur * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        heavy_wood_thud = np.sin(2 * np.pi * 75.0 * dt) * np.exp(-dt * 24.0) * 0.75
        rubber_squelch = butter_bandpass_filter(np.random.normal(0, 1, len(dt)), 600, 2400, SR) * np.exp(-dt * 45.0) * 0.45
        desk_resonance = np.sin(2 * np.pi * 125.0 * dt) * np.exp(-dt * 10.0) * 0.30
        foley[s_idx:e_idx] += (heavy_wood_thud + rubber_squelch + desk_resonance)

    # Cue Placement strictly matching the narrative milestones:
    # ACT 1
    add_sonar_ping(1.2, 1420.0)
    add_sonar_ping(8.5, 1380.0)
    add_implosion_blast(19.2)   # SOSUS underwater implosion detection
    add_sonar_ping(23.5, 1480.0)

    # ACT 2
    add_dossier_open(27.6)
    add_teletype(31.5, 2.5)
    add_dossier_open(40.5)

    # ACT 3
    add_dossier_open(54.5)
    add_hydraulic_clamp(68.5)   # Clementine claw locking onto K-129
    add_sonar_ping(73.0, 1550.0)

    # ACT 4
    add_claw_snap(86.8)         # The Snap at 9,000 feet!
    add_radiation_geiger(90.5, 8.5) # Radiation alarm & Geiger counter chatter

    # ACT 5
    add_ceremonial_funeral(102.0) # Solemn burial at sea & Soviet anthem
    add_teletype(119.0, 3.2)     # Jack Anderson leak

    # OUTRO
    add_stamp_slam(133.2)       # Heavy INVESTIGATION SOLVED declassification stamp!

    return foley

def main():
    print(f"[Synthesize Ep6 Full] Loading narration file...")
    vo_path = os.path.join(AUDIO_DIR, "vo_azorian_full_narration.wav")
    sr, vo = wavfile.read(vo_path)
    if vo.dtype != np.float32:
        vo = vo.astype(np.float32) / 32768.0

    dur_sec = len(vo) / SR
    print(f"  Narration length: {round(dur_sec, 2)}s")

    drone = generate_investigative_drone()
    foley = generate_tactile_foley()

    # Dynamic Sidechain Ducking:
    # When voice is active, duck music/ambient drone by -45%
    print("[Synthesize Ep6 Full] Applying -45% dynamic sidechain ducking...")
    vo_abs = np.abs(vo[:len(drone)])
    # Smooth envelope
    env = butter_lowpass_filter(vo_abs, 4.0, SR)
    max_env = np.max(env) if np.max(env) > 0 else 1.0
    norm_env = np.clip(env / max_env, 0, 1)

    duck_gain = 1.0 - (norm_env * 0.45)
    ducked_drone = drone * duck_gain

    # Master summing
    master = (vo[:len(drone)] * 0.95) + (ducked_drone * 0.70) + (foley * 0.85)

    # Peak normalization to -1.0 dB
    peak = np.max(np.abs(master))
    if peak > 0:
        master = (master / peak) * 0.89

    master_int16 = (master * 32767.0).astype(np.int16)
    out_wav = os.path.join(AUDIO_DIR, "vo_azorian_cinematic_full.wav")
    wavfile.write(out_wav, SR, master_int16)
    print(f"[Synthesize Ep6 Full] Master WAV generated: {out_wav}")

    # Encode high quality MP3
    out_mp3 = os.path.join(AUDIO_DIR, "vo_azorian_cinematic_full.mp3")
    cmd = [
        "ffmpeg", "-y", "-i", out_wav,
        "-b:a", "192k",
        out_mp3
    ]
    subprocess.run(cmd, check=True, shell=True)
    print(f"[Synthesize Ep6 Full] Master MP3 encoded: {out_mp3} ({round(os.path.getsize(out_mp3)/1024, 1)} KB)")

if __name__ == "__main__":
    main()
