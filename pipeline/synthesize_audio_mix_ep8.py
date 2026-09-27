import os
import json
import numpy as np
import scipy.io.wavfile as wavfile
from scipy.signal import butter, lfilter
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(PROJECT_ROOT, "assets", "episode8_voynich_manuscript", "audio")
SR = 24000  # 24kHz master rate matching Kokoro TTS

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

# 1. Medieval Cloister & Library Room-Tone Ambient Drone
def generate_ambient_drone(total_dur, total_samples):
    t = np.linspace(0, total_dur, total_samples, endpoint=False)
    
    # Sub-bass foundation (36Hz + 54Hz cathedral stone resonance)
    sub = (np.sin(2 * np.pi * 36.0 * t) * 0.7 + np.sin(2 * np.pi * 54.0 * t) * 0.3) * 0.11
    
    # Subtle ticking timekeeper (antique clockwork escapement)
    clock_pulse = np.zeros(total_samples, dtype=np.float64)
    tick_interval = int(0.6 * SR)
    for i in range(0, total_samples - int(0.04 * SR), tick_interval):
        dt = np.linspace(0, 0.04, int(0.04 * SR), endpoint=False)
        tick = np.sin(2 * np.pi * 1200.0 * dt) * np.exp(-dt * 110.0) * 0.025
        clock_pulse[i:i + len(tick)] += tick

    # Tension harmonic pad during the Zipf's Law & Cryptanalysis revelation (50s - 95s)
    tension_pad = np.zeros(total_samples, dtype=np.float64)
    p_mask = (t >= 50.0) & (t < min(95.0, total_dur))
    p_dt = t[p_mask] - 50.0
    p_osc = (np.sin(2 * np.pi * 130.81 * p_dt) * 0.4 + # C3
             np.sin(2 * np.pi * 155.56 * p_dt) * 0.3 + # Eb3
             np.sin(2 * np.pi * 196.00 * p_dt) * 0.3)  # G3 (C minor mystery chord)
    p_env = np.clip(p_dt / 3.0, 0, 1) * np.clip((min(95.0, total_dur) - t[p_mask]) / 3.0, 0, 1)
    tension_pad[p_mask] = p_osc * p_env * 0.08

    # Wonder & unsolved enigma pad in Outro (95s to end)
    wonder_pad = np.zeros(total_samples, dtype=np.float64)
    w_mask = (t >= 95.0)
    w_dt = t[w_mask] - 95.0
    w_osc = (np.sin(2 * np.pi * 110.00 * w_dt) * 0.4 + # A2
             np.sin(2 * np.pi * 164.81 * w_dt) * 0.3 + # E3
             np.sin(2 * np.pi * 220.00 * w_dt) * 0.3)  # A3
    w_env = np.clip(w_dt / 3.0, 0, 1) * np.clip((total_dur - t[w_mask]) / 3.0, 0, 1)
    wonder_pad[w_mask] = w_osc * w_env * 0.07

    return sub + clock_pulse + tension_pad + wonder_pad

# 2. Tactile Foley Generator (Quill scratches, parchment flutters, wax seal crack, rubber stamp)
def generate_tactile_foley(total_dur, total_samples, beats):
    foley = np.zeros(total_samples, dtype=np.float64)
    np.random.seed(408408) # MS 408 seed

    def add_foley_sample(sample_data, start_sec, volume=1.0):
        start_idx = int(start_sec * SR)
        end_idx = min(start_idx + len(sample_data), total_samples)
        valid_len = end_idx - start_idx
        if valid_len > 0:
            foley[start_idx:end_idx] += sample_data[:valid_len] * volume

    # A. Archival Folder Unsealing / Box Open (Intro 0.4s)
    dur = 0.65
    n = int(dur * SR)
    white = np.random.randn(n)
    env = np.exp(-np.linspace(0, 5, n))
    cardboard = butter_bandpass_filter(white * env, 300, 1800, SR) * 0.45
    add_foley_sample(cardboard, 0.4, 0.9)

    # B. Heavy Parchment Turn Foley (At transitions)
    for b in beats:
        t_start = max(0.1, b["start"] - 0.25)
        n_p = int(0.5 * SR)
        p_noise = np.random.randn(n_p)
        p_env = np.sin(np.linspace(0, np.pi, n_p)) ** 2
        p_filtered = butter_bandpass_filter(p_noise * p_env, 400, 3200, SR) * 0.22
        add_foley_sample(p_filtered, t_start, 0.6)

    # C. Medieval Quill Pen Scratching (During script/alphabet revelation)
    # Between 8s - 24s (Act 1 beats)
    quill_dur = 14.0
    n_q = int(quill_dur * SR)
    q_noise = np.random.randn(n_q)
    # rhythmic scratch strokes
    t_q = np.linspace(0, quill_dur, n_q, endpoint=False)
    stroke_mod = (np.sin(2 * np.pi * 3.5 * t_q) > 0.3).astype(np.float64)
    quill_scratch = butter_bandpass_filter(q_noise * stroke_mod, 1800, 6500, SR) * 0.08
    add_foley_sample(quill_scratch, 8.5, 0.7)

    # D. Cryptographic Data Chatter / Teletype Clicks (Act 5: NSA & AI attempts)
    # Around beat 10 & 11 (Friedman & modern AI)
    if len(beats) >= 11:
        ai_start = beats[9]["start"]
        ai_dur = min(22.0, total_dur - ai_start)
        n_ai = int(ai_dur * SR)
        ai_sig = np.zeros(n_ai, dtype=np.float64)
        click_idx = 0
        while click_idx < n_ai - int(0.01 * SR):
            click_len = int(0.008 * SR)
            dt = np.linspace(0, 0.008, click_len, endpoint=False)
            click_osc = np.sin(2 * np.pi * 3400.0 * dt) * np.exp(-dt * 500.0) * 0.04
            ai_sig[click_idx:click_idx + click_len] += click_osc
            click_idx += int(np.random.uniform(0.04, 0.12) * SR)
        add_foley_sample(ai_sig, ai_start, 0.8)

    # E. Heavy Rubber Stamp Slam directly on vellum at Outro
    stamp_time = max(0.0, total_dur - 4.2)
    n_slam = int(0.85 * SR)
    t_slam = np.linspace(0, 0.85, n_slam, endpoint=False)
    # Low frequency wood block thump + metal snap
    slam_thump = np.sin(2 * np.pi * 58.0 * t_slam) * np.exp(-t_slam * 14.0) * 0.75
    slam_snap = butter_bandpass_filter(np.random.randn(n_slam) * np.exp(-t_slam * 35.0), 450, 4200, SR) * 0.55
    add_foley_sample(slam_thump + slam_snap, stamp_time, 1.25)

    return foley

def main():
    cues_path = os.path.join(AUDIO_DIR, "vo_cues_voynich.json")
    if not os.path.exists(cues_path):
        print(f"[!] Cues file not found yet: {cues_path}")
        return

    with open(cues_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    total_dur = manifest["total_duration"]
    total_samples = int(total_dur * SR)
    beats = manifest["beats"]

    print(f"\n[Audio Synthesizer Ep8] Processing mix for '{manifest['title']}' ({total_dur:.2f}s)...")

    # Load master narration
    master_vo_path = os.path.join(AUDIO_DIR, "vo_voynich_narration.wav")
    sr_in, vo_raw = wavfile.read(master_vo_path)
    if sr_in != SR:
        raise ValueError(f"Sample rate mismatch: {sr_in} != {SR}")

    # Ensure float64 normalized
    if vo_raw.dtype == np.int16:
        vo_float = vo_raw.astype(np.float64) / 32768.0
    else:
        vo_float = vo_raw.astype(np.float64)

    if len(vo_float) < total_samples:
        vo_float = np.pad(vo_float, (0, total_samples - len(vo_float)))
    else:
        vo_float = vo_float[:total_samples]

    # Generate atmospheric background layers
    print("  -> Generating cathedral library ambient drone & antique clockwork...")
    drone = generate_ambient_drone(total_dur, total_samples)

    print("  -> Generating tactile foley (quill scratching, vellum rustle, stamp slam)...")
    foley = generate_tactile_foley(total_dur, total_samples, beats)

    # Sidechain ducking: Duck drone & foley by -42% when narration is active
    print("  -> Applying dynamic sidechain ducking (-42%)...")
    vo_abs = np.abs(vo_float)
    # Smooth envelope follower (attack ~20ms, release ~250ms)
    env = np.zeros(total_samples, dtype=np.float64)
    current_env = 0.0
    att = np.exp(-1.0 / (0.02 * SR))
    rel = np.exp(-1.0 / (0.25 * SR))
    for i in range(total_samples):
        val = vo_abs[i]
        if val > current_env:
            current_env = val + att * (current_env - val)
        else:
            current_env = val + rel * (current_env - val)
        env[i] = current_env

    ducking_gain = 1.0 - 0.42 * np.clip(env * 3.5, 0, 1.0)
    ducked_backing = (drone * 0.45 + foley * 0.65) * ducking_gain

    # Final Master Mix: Voice + Ducked Ambient Backing
    master_mix = vo_float * 0.95 + ducked_backing

    # Master soft peak limiter to prevent clipping
    peak = np.max(np.abs(master_mix))
    if peak > 0.95:
        print(f"  -> Normalizing mix peak from {peak:.3f} to 0.94...")
        master_mix = (master_mix / peak) * 0.94

    # Convert to 16-bit PCM
    master_int16 = (master_mix * 32767.0).astype(np.int16)

    out_wav = os.path.join(AUDIO_DIR, "vo_voynich_cinematic.wav")
    wavfile.write(out_wav, SR, master_int16)
    print(f"[+] Master cinematic WAV saved: {out_wav}")

    # Convert to 48kHz stereo MP3 for web & video render
    out_mp3 = os.path.join(AUDIO_DIR, "vo_voynich_cinematic.mp3")
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", out_wav,
        "-ar", "48000",
        "-ac", "2",
        "-b:a", "192k",
        out_mp3
    ]
    subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, shell=True)
    print(f"[+] Master cinematic MP3 saved: {out_mp3}")
    print("[Audio Synthesizer Ep8] Finished successfully.")

if __name__ == "__main__":
    main()
