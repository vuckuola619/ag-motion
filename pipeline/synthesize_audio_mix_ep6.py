import os
import json
import numpy as np
import scipy.io.wavfile as wavfile
from scipy.signal import butter, lfilter
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(PROJECT_ROOT, "assets", "episode6_project_azorian", "audio")
SR = 24000  # 24kHz master rate matching Kokoro TTS
TOTAL_DUR = 60.0
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

# 1. Vox Investigative Pulse & Low-Drone Bed
def generate_investigative_drone():
    t = np.linspace(0, TOTAL_DUR, TOTAL_SAMPLES, endpoint=False)
    
    # Sub-bass foundation (42Hz - 48Hz slow beating abyss resonance)
    sub = (np.sin(2 * np.pi * 44.0 * t) * 0.7 + np.sin(2 * np.pi * 47.5 * t) * 0.3) * 0.14
    
    # 120 BPM subtle clock/sonar pulse (2 pulses per second)
    clock_pulse = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    tick_interval = int(0.5 * SR)
    for i in range(0, TOTAL_SAMPLES - int(0.04 * SR), tick_interval):
        dt = np.linspace(0, 0.04, int(0.04 * SR), endpoint=False)
        tick = np.sin(2 * np.pi * 920.0 * dt) * np.exp(-dt * 95.0) * 0.038
        clock_pulse[i:i + len(tick)] += tick
        
    # Tension swell in Scene 4 & 5 (34s - 55s)
    tension_pad = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    p_mask = (t >= 34.0) & (t < 55.0)
    p_dt = t[p_mask] - 34.0
    # Cold War minor tension drone (E-minor: 164.8Hz E3, 196.0Hz G3, 246.9Hz B3)
    p_osc = (np.sin(2 * np.pi * 164.8 * p_dt) * 0.4 +
             np.sin(2 * np.pi * 196.0 * p_dt) * 0.3 +
             np.sin(2 * np.pi * 246.9 * p_dt) * 0.3)
    p_env = np.clip(p_dt / 4.0, 0, 1) * np.clip((55.0 - t[p_mask]) / 3.0, 0, 1)
    tension_pad[p_mask] = p_osc * p_env * 0.08

    return sub + clock_pulse + tension_pad

# 2. Tactile Foley (Folder open, Sonar ping, Camera shutter, Teletype, Hydraulic groan, Snap, Geiger click, Bell, Stamp slam)
def generate_tactile_foley():
    foley = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    np.random.seed(84000)

    # A. Folder Open / Paper Dossier Slap
    def add_dossier_open(start_t):
        s_idx = int(start_t * SR)
        dur = 0.45
        e_idx = min(s_idx + int(dur * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        # Heavy low thud + friction paper whoosh + metal fastener clink
        thud = np.sin(2 * np.pi * 95.0 * dt) * np.exp(-dt * 30.0) * 0.45
        whoosh = butter_bandpass_filter(np.random.normal(0, 1, len(dt)), 800, 3200, SR) * np.exp(-dt * 12.0) * 0.25
        clink = np.sin(2 * np.pi * 3800.0 * dt) * np.exp(-dt * 120.0) * 0.22
        foley[s_idx:e_idx] += (thud + whoosh + clink)

    # B. Sonar Ping (Acoustic deep-sea ping with long underwater reverb tail)
    def add_sonar_ping(start_t, freq=1480.0):
        s_idx = int(start_t * SR)
        dur = 1.6
        e_idx = min(s_idx + int(dur * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        # Attack chirp + long exponential decay sine
        tone = np.sin(2 * np.pi * freq * dt) * np.exp(-dt * 3.5) * 0.35
        # Secondary sub echo
        sub_echo = np.sin(2 * np.pi * (freq * 0.5) * dt) * np.exp(-dt * 4.2) * 0.15
        foley[s_idx:e_idx] += (tone + sub_echo)

    # C. Camera Shutter Snap / Press Flash
    def add_shutter_snap(start_t):
        s_idx = int(start_t * SR)
        e_idx = min(s_idx + int(0.12 * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        click1 = np.sin(2 * np.pi * 1800.0 * dt) * np.exp(-dt * 120.0) * 0.32
        click2 = np.zeros_like(dt)
        c2_idx = int(0.04 * SR)
        if len(dt) > c2_idx:
            dt2 = dt[c2_idx:] - 0.04
            click2[c2_idx:] = np.sin(2 * np.pi * 2700.0 * dt2) * np.exp(-dt2 * 140.0) * 0.26
        foley[s_idx:e_idx] += (click1 + click2)

    # D. Teletype / Wire service chatter burst
    def add_teletype_burst(start_t, count=8, speed=0.075):
        for k in range(count):
            t_curr = start_t + k * speed
            s_idx = int(t_curr * SR)
            e_idx = min(s_idx + int(0.03 * SR), TOTAL_SAMPLES)
            if s_idx >= TOTAL_SAMPLES:
                break
            dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
            strike = (np.sin(2 * np.pi * 1500.0 * dt) + np.sin(2 * np.pi * 3100.0 * dt) * 0.5) * np.exp(-dt * 190.0) * 0.18
            foley[s_idx:e_idx] += strike

    # E. Heavy Hydraulic Claw Groan & Motor Whine
    def add_hydraulic_groan(start_t, dur=1.8):
        s_idx = int(start_t * SR)
        e_idx = min(s_idx + int(dur * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        motor = (np.sin(2 * np.pi * (85.0 + 15.0 * np.sin(2 * np.pi * 3.0 * dt)) * dt) * 0.22 +
                 np.sin(2 * np.pi * 170.0 * dt) * 0.12)
        hiss = butter_bandpass_filter(np.random.normal(0, 1, len(dt)), 600, 2400, SR) * 0.10
        env = np.sin(np.pi * np.clip(dt / dur, 0, 1))
        foley[s_idx:e_idx] += (motor + hiss) * env

    # F. Catastrophic Metal Snap & Hull Fracture Impact
    def add_catastrophic_snap(start_t):
        s_idx = int(start_t * SR)
        dur = 2.2
        e_idx = min(s_idx + int(dur * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        # Violently sharp high-frequency shear (3200Hz) followed by massive low-frequency structural boom (55Hz)
        shear = np.sin(2 * np.pi * 3400.0 * dt) * np.exp(-dt * 80.0) * 0.55
        boom = np.sin(2 * np.pi * 52.0 * dt) * np.exp(-dt * 8.0) * 0.65
        rumble = butter_lowpass_filter(np.random.normal(0, 1, len(dt)), 250, SR) * np.exp(-dt * 4.0) * 0.35
        foley[s_idx:e_idx] += (shear + boom + rumble)

    # G. Geiger Counter Rapid Crackle Burst
    def add_geiger_clicks(start_t, dur=1.6, count=24):
        times = start_t + np.sort(np.random.uniform(0, dur, count))
        for t_click in times:
            s_idx = int(t_click * SR)
            e_idx = min(s_idx + int(0.004 * SR), TOTAL_SAMPLES)
            if s_idx >= TOTAL_SAMPLES:
                break
            dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
            click = np.sin(2 * np.pi * 4200.0 * dt) * np.exp(-dt * 1200.0) * 0.38
            foley[s_idx:e_idx] += click

    # H. Solemn Naval Bell Toll (440Hz / 554Hz brass harmonic ring)
    def add_naval_bell(start_t):
        s_idx = int(start_t * SR)
        dur = 3.5
        e_idx = min(s_idx + int(dur * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        bell = (np.sin(2 * np.pi * 440.0 * dt) * 0.4 +
                np.sin(2 * np.pi * 554.37 * dt) * 0.3 +
                np.sin(2 * np.pi * 880.0 * dt) * 0.2 +
                np.sin(2 * np.pi * 1320.0 * dt) * 0.1) * np.exp(-dt * 1.8) * 0.32
        foley[s_idx:e_idx] += bell

    # I. Soviet Anthem Solemn Brass Chord Bed
    def add_soviet_anthem_motif(start_t):
        s_idx = int(start_t * SR)
        dur = 7.0
        e_idx = min(s_idx + int(dur * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        # Majestic brass anthem chord progression (G-major into C-major)
        c_chord = (np.sin(2 * np.pi * 130.81 * dt) * 0.35 +  # C3
                   np.sin(2 * np.pi * 164.81 * dt) * 0.30 +  # E3
                   np.sin(2 * np.pi * 196.00 * dt) * 0.30 +  # G3
                   np.sin(2 * np.pi * 261.63 * dt) * 0.25)   # C4
        env = np.sin(np.pi * np.clip(dt / dur, 0, 1)) ** 0.8
        foley[s_idx:e_idx] += c_chord * env * 0.12

    # J. Stamp Slam (Heavy desk thud + wooden rubber stamp slap)
    def add_stamp_slam(start_t):
        s_idx = int(start_t * SR)
        dur = 0.8
        e_idx = min(s_idx + int(dur * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        thud = np.sin(2 * np.pi * 65.0 * dt) * np.exp(-dt * 18.0) * 0.70
        snap = np.sin(2 * np.pi * 2200.0 * dt) * np.exp(-dt * 90.0) * 0.45
        desk_ring = np.sin(2 * np.pi * 320.0 * dt) * np.exp(-dt * 24.0) * 0.25
        foley[s_idx:e_idx] += (thud + snap + desk_ring)

    # K. Highlighter Marker Squeak
    def add_marker_squeak(start_t, dur=0.32):
        s_idx = int(start_t * SR)
        e_idx = min(s_idx + int(dur * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        chirp = np.sin(2 * np.pi * (2300.0 + 350.0 * np.sin(2 * np.pi * 16.0 * dt)) * dt) * 0.11
        friction = butter_bandpass_filter(np.random.normal(0, 1, len(dt)), 1800, 4200, SR) * 0.07
        env = np.sin(np.pi * np.clip(dt / dur, 0, 1))
        foley[s_idx:e_idx] += (chirp + friction) * env

    # --- PLACEMENT OF TACTILE FOLEY CUES ---
    # 0.0s - 1.2s: Manila Dossier opens
    add_dossier_open(0.1)
    add_marker_squeak(0.7)

    # 1.2s - 12.0s: Scene 1 The Vanished Sub
    add_sonar_ping(2.0, 1420.0)
    add_teletype_burst(5.2, count=6)
    add_sonar_ping(7.8, 1420.0)
    add_marker_squeak(10.2)
    add_sonar_ping(11.2, 1260.0)

    # 12.0s - 23.0s: Scene 2 The Billionaire Cover Story
    add_shutter_snap(12.2)
    add_marker_squeak(13.8)
    add_teletype_burst(16.5, count=10)
    add_shutter_snap(19.2)
    add_hydraulic_groan(21.2, dur=1.8)

    # 23.0s - 34.0s: Scene 3 The Mechanical Monster
    add_hydraulic_groan(23.6, dur=2.4)
    add_marker_squeak(25.4)
    add_sonar_ping(28.0, 980.0)
    add_hydraulic_groan(31.0, dur=2.2)

    # 34.0s - 45.0s: Scene 4 The Snap & Radiation
    add_catastrophic_snap(35.2)  # THE SNAP!
    add_geiger_clicks(37.5, dur=3.5, count=32)
    add_marker_squeak(40.2)
    add_geiger_clicks(42.0, dur=2.8, count=28)

    # 45.0s - 55.0s: Scene 5 The Secret Burial at Sea
    add_naval_bell(45.6)
    add_soviet_anthem_motif(47.0)
    add_naval_bell(51.0)
    add_marker_squeak(53.2)

    # 55.0s - 60.0s: Scene 6 Outro Stamp Slam
    add_teletype_burst(55.2, count=5)
    add_stamp_slam(56.5)  # CASE SOLVED // PROJECT AZORIAN STAMP SLAM!

    return foley

def synthesize_final_master():
    print("[Audio Master Ep6] Synthesizing Project Azorian tactile sound design...")
    
    # 1. Load narration
    narration_file = os.path.join(AUDIO_DIR, "vo_azorian_narration_only.wav")
    sr, narration = wavfile.read(narration_file)
    if narration.dtype == np.int16:
        narration = narration.astype(np.float64) / 32768.0
    else:
        narration = narration.astype(np.float64)

    # Pad or trim narration to TOTAL_SAMPLES
    if len(narration) < TOTAL_SAMPLES:
        narration = np.pad(narration, (0, TOTAL_SAMPLES - len(narration)))
    else:
        narration = narration[:TOTAL_SAMPLES]

    # 2. Build drone bed and foley
    drone = generate_investigative_drone()
    foley = generate_tactile_foley()

    # 3. Dynamic Sidechain Ducking: duck drone by 42% when speech energy is present
    speech_envelope = np.abs(narration)
    # Smooth envelope with ~150ms moving window
    win_len = int(0.15 * SR)
    env_smooth = np.convolve(speech_envelope, np.ones(win_len)/win_len, mode='same')
    duck_gain = 1.0 - 0.42 * np.clip(env_smooth * 6.0, 0, 1)

    ducked_drone = drone * duck_gain

    # 4. Mix tracks with broadcast headroom
    master = (narration * 1.05) + ducked_drone + (foley * 0.95)

    # Peak normalization to -1.0 dB (approx 0.89)
    peak = np.max(np.abs(master))
    if peak > 0:
        master = (master / peak) * 0.89
        print(f"[Audio Master Ep6] Normalized peak from {peak:.3f} to 0.89 (-1.0 dBFS)")

    # Save 24-bit PCM WAV
    out_wav = os.path.join(AUDIO_DIR, "vo_azorian_cinematic.wav")
    master_int16 = (master * 32767.0).astype(np.int16)
    wavfile.write(out_wav, SR, master_int16)
    print(f"[Audio Master Ep6] Master WAV saved: {out_wav}")

    # Convert to high-bitrate MP3 via FFmpeg
    ffmpeg_exe = "C:\\Program Files\\ShareX\\ffmpeg.exe"
    out_mp3 = os.path.join(AUDIO_DIR, "vo_azorian_cinematic.mp3")
    cmd = [ffmpeg_exe, "-y", "-i", out_wav, "-b:a", "320k", out_mp3]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[Audio Master Ep6] Master MP3 saved: {out_mp3}")
    print("[Audio Master Ep6] Audio pipeline complete!")

if __name__ == "__main__":
    synthesize_final_master()
