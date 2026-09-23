import os
import json
import numpy as np
import scipy.io.wavfile as wavfile
from scipy.signal import butter, lfilter
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(PROJECT_ROOT, "assets", "episode5_iridium_layer", "audio")
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
    
    # Sub-bass foundation (42Hz - 48Hz slow beating)
    sub = (np.sin(2 * np.pi * 44.0 * t) * 0.7 + np.sin(2 * np.pi * 48.0 * t) * 0.3) * 0.12
    
    # 120 BPM subtle clock/radar pulse (2 pulses per second)
    clock_pulse = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    tick_interval = int(0.5 * SR)
    for i in range(0, TOTAL_SAMPLES - int(0.04 * SR), tick_interval):
        dt = np.linspace(0, 0.04, int(0.04 * SR), endpoint=False)
        tick = np.sin(2 * np.pi * 950.0 * dt) * np.exp(-dt * 90.0) * 0.045
        clock_pulse[i:i + len(tick)] += tick
        
    # Tension swell in Beat 5 & 6 (40s - 60s)
    tension_pad = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    p_mask = (t >= 40.0) & (t < 59.5)
    p_dt = t[p_mask] - 40.0
    # D-minor harmonic tension (146.8Hz D3, 174.6Hz F3, 220Hz A3)
    p_osc = (np.sin(2 * np.pi * 146.8 * p_dt) * 0.4 +
             np.sin(2 * np.pi * 174.6 * p_dt) * 0.3 +
             np.sin(2 * np.pi * 220.0 * p_dt) * 0.3)
    p_env = np.clip(p_dt / 5.0, 0, 1) * np.clip((59.5 - t[p_mask]) / 3.0, 0, 1)
    tension_pad[p_mask] = p_osc * p_env * 0.09

    return sub + clock_pulse + tension_pad

# 2. Tactile Vox Foley (Marker squeaks, camera shutters, typewriter chatter, desk thuds)
def generate_vox_foley():
    foley = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    np.random.seed(77000)

    # A. Marker Squeak generator (yellow highlighter wiping text)
    def add_marker_squeak(start_t, dur=0.35):
        s_idx = int(start_t * SR)
        e_idx = min(s_idx + int(dur * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        # Chirp squeak 2200Hz - 2900Hz modulated with highpass friction noise
        chirp = np.sin(2 * np.pi * (2400.0 + 400.0 * np.sin(2 * np.pi * 18.0 * dt)) * dt) * 0.12
        friction = butter_bandpass_filter(np.random.normal(0, 1, len(dt)), 1800, 4500, SR) * 0.08
        env = np.sin(np.pi * np.clip(dt / dur, 0, 1))
        foley[s_idx:e_idx] += (chirp + friction) * env

    # B. Camera Shutter Snap / Slide Projector Click
    def add_shutter_snap(start_t):
        s_idx = int(start_t * SR)
        e_idx = min(s_idx + int(0.12 * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        # Mechanical double click (mirror lift + curtain snap)
        click1 = np.sin(2 * np.pi * 1800.0 * dt) * np.exp(-dt * 120.0) * 0.32
        click2 = np.zeros_like(dt)
        c2_idx = int(0.04 * SR)
        if len(dt) > c2_idx:
            dt2 = dt[c2_idx:] - 0.04
            click2[c2_idx:] = np.sin(2 * np.pi * 2800.0 * dt2) * np.exp(-dt2 * 140.0) * 0.28
        foley[s_idx:e_idx] += (click1 + click2)

    # C. Teletype / Typewriter chatter (data numbers rolling)
    def add_teletype_burst(start_t, count=8, speed=0.08):
        for k in range(count):
            t_curr = start_t + k * speed
            s_idx = int(t_curr * SR)
            e_idx = min(s_idx + int(0.03 * SR), TOTAL_SAMPLES)
            if s_idx >= TOTAL_SAMPLES:
                break
            dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
            strike = (np.sin(2 * np.pi * 1400.0 * dt) + np.sin(2 * np.pi * 3200.0 * dt) * 0.5) * np.exp(-dt * 180.0) * 0.16
            foley[s_idx:e_idx] += strike

    # D. Heavy Paper / Desk Thud / Rubber Stamp Impact
    def add_desk_stamp(start_t, is_stamp=False):
        s_idx = int(start_t * SR)
        e_idx = min(s_idx + int(0.4 * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        # Low wood resonance (70Hz - 90Hz)
        body = np.sin(2 * np.pi * 78.0 * dt) * np.exp(-dt * 14.0) * 0.35
        # High paper/rubber snap
        snap_freq = 2400.0 if is_stamp else 1600.0
        snap = np.sin(2 * np.pi * snap_freq * dt) * np.exp(-dt * 55.0) * (0.35 if is_stamp else 0.22)
        foley[s_idx:e_idx] += (body + snap)

    # E. Smooth Camera Glide Whoosh
    def add_glide_whoosh(start_t, dur=0.9):
        s_idx = int(start_t * SR)
        e_idx = min(s_idx + int(dur * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        noise = np.random.normal(0, 1, len(dt))
        filtered = butter_bandpass_filter(noise, 300, 1800, SR)
        env = np.sin(np.pi * np.clip(dt / dur, 0, 1)) ** 1.8
        foley[s_idx:e_idx] += filtered * env * 0.18

    # Apply Foley across 60.0s timeline
    # 1. Shutter clicks at scene reveals
    add_shutter_snap(0.4)
    add_shutter_snap(10.7)
    add_shutter_snap(19.9)
    add_shutter_snap(29.7)
    add_shutter_snap(40.4)
    add_shutter_snap(51.4)

    # 2. Marker squeaks synced to narration key terms
    add_marker_squeak(2.5, 0.40)   # "single centimeter"
    add_marker_squeak(12.0, 0.35)  # "thirty times higher"
    add_marker_squeak(22.2, 0.38)  # "six-mile-wide asteroid"
    add_marker_squeak(32.4, 0.42)  # "one hundred and ten miles wide"
    add_marker_squeak(43.0, 0.38)  # "one hundred million atomic bombs"
    add_marker_squeak(53.2, 0.40)  # "solved Earth's biggest murder mystery"

    # 3. Teletype data roll
    add_teletype_burst(11.2, count=10, speed=0.07)  # Iridium +3,000% spike
    add_teletype_burst(30.4, count=12, speed=0.06)  # Satellite coordinate ping

    # 4. Physical props slams
    add_desk_stamp(2.0, is_stamp=False)   # Scale ruler drop
    add_desk_stamp(14.0, is_stamp=False)  # Radiation tag placed
    add_desk_stamp(33.8, is_stamp=False)  # Target reticle lock
    add_desk_stamp(44.5, is_stamp=False)  # Tektite bead drop
    add_desk_stamp(55.2, is_stamp=True)   # SOLVED // K-PG CASE CLOSED red stamp slam!

    # 5. Transition glides
    add_glide_whoosh(9.6, 1.0)
    add_glide_whoosh(18.8, 1.0)
    add_glide_whoosh(28.6, 1.0)
    add_glide_whoosh(39.3, 1.0)
    add_glide_whoosh(50.2, 1.0)

    return foley

def main():
    vo_wav_path = os.path.join(AUDIO_DIR, "vo_iridium_layer.wav")
    if not os.path.exists(vo_wav_path):
        print(f"[Audio Ep5] ERROR: Missing {vo_wav_path}")
        return

    sr_in, vo_data = wavfile.read(vo_wav_path)
    if vo_data.dtype == np.int16:
        vo_float = vo_data.astype(np.float64) / 32768.0
    elif vo_data.dtype == np.float32 or vo_data.dtype == np.float64:
        vo_float = vo_data.astype(np.float64)
    else:
        vo_float = vo_data.astype(np.float64) / np.max(np.abs(vo_data))

    # Pad or trim to TOTAL_SAMPLES
    if len(vo_float) < TOTAL_SAMPLES:
        vo_pad = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
        vo_pad[:len(vo_float)] = vo_float
        vo_float = vo_pad
    else:
        vo_float = vo_float[:TOTAL_SAMPLES]

    print("[Audio Ep5] Generating Vox investigative drone bed...")
    music_bed = generate_investigative_drone()

    print("[Audio Ep5] Generating Vox tactile foley bed (marker, shutter, teletype, stamps)...")
    foley_bed = generate_vox_foley()

    # Dynamic sidechain ducking (-45% ducking during active speech)
    print("[Audio Ep5] Computing sidechain voice ducking...")
    window_len = int(0.12 * SR)
    vo_env = np.convolve(np.abs(vo_float), np.ones(window_len) / window_len, mode='same')
    duck_gain = np.ones(TOTAL_SAMPLES, dtype=np.float64)
    duck_mask = vo_env > 0.04
    duck_gain[duck_mask] = 0.55  # Duck background by 45% during speech

    # Smooth gain transitions
    duck_gain = butter_lowpass_filter(duck_gain, 12, SR, order=2)

    ducked_music = music_bed * duck_gain
    ducked_foley = foley_bed * (0.75 + 0.25 * duck_gain)

    # Master summing
    master = vo_float * 0.92 + ducked_music + ducked_foley

    # Master limiter / peak normalize to -0.3 dB
    max_peak = np.max(np.abs(master))
    if max_peak > 0.96:
        master = master * (0.96 / max_peak)

    out_wav = os.path.join(AUDIO_DIR, "vo_iridium_layer_cinematic.wav")
    master_int16 = (master * 32767.0).astype(np.int16)
    wavfile.write(out_wav, SR, master_int16)
    print(f"[Audio Ep5] Successfully exported master WAV: {out_wav} ({TOTAL_DUR}s @ {SR}Hz)")

    out_mp3 = os.path.join(AUDIO_DIR, "vo_iridium_layer_cinematic.mp3")
    ffmpeg_exe = r"C:\Program Files\ShareX\ffmpeg.exe"
    subprocess.run([ffmpeg_exe, "-y", "-i", out_wav, "-b:a", "192k", out_mp3], check=True, capture_output=True)
    print(f"[Audio Ep5] Exported MP3 preview: {out_mp3}")

if __name__ == "__main__":
    main()
