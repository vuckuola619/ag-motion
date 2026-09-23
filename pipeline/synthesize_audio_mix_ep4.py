import os
import json
import numpy as np
import scipy.io.wavfile as wavfile
from scipy.signal import butter, lfilter
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(PROJECT_ROOT, "assets", "episode4_chicxulub", "audio")
SR = 24000  # 24kHz master rate matching Kokoro TTS
TOTAL_DUR = 70.0
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

# 1. Cinematic Trailer Drone & Harmonic Music Bed
def generate_cinematic_music_bed():
    t = np.linspace(0, TOTAL_DUR, TOTAL_SAMPLES, endpoint=False)
    
    # Sub-bass foundation (42Hz - 48Hz slow beating)
    sub = (np.sin(2 * np.pi * 42.0 * t) * 0.6 + np.sin(2 * np.pi * 46.5 * t) * 0.4) * 0.12
    
    # Rising trailer riser leading up to impact (8.0s - 10.4s)
    riser = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    r_mask = (t >= 8.0) & (t < 10.4)
    r_dt = t[r_mask] - 8.0
    r_freq = 60.0 + 350.0 * (r_dt / 2.4) ** 2.2
    riser[r_mask] = np.sin(2 * np.pi * r_freq * r_dt) * ((r_dt / 2.4) ** 2) * 0.18
    
    # Post-extinction somber strings/pad (Scene 5: 42s - 52s)
    winter_pad = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    w_mask = (t >= 42.0) & (t < 52.5)
    w_dt = t[w_mask] - 42.0
    # D minor low fifth (73.4Hz + 110Hz)
    w_osc = (np.sin(2 * np.pi * 73.4 * w_dt) + 0.7 * np.sin(2 * np.pi * 110.0 * w_dt))
    w_env = np.sin(np.pi * np.clip(w_dt / 10.5, 0, 1))
    winter_pad[w_mask] = w_osc * w_env * 0.08
    
    # Mammalian Dawn & Resolution Swell (Scene 6 & 7: 52.5s - 70.0s)
    dawn_pad = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    d_mask = (t >= 52.5) & (t < 70.0)
    d_dt = t[d_mask] - 52.5
    # Warm C-major harmonic chords (130.8Hz C3, 164.8Hz E3, 196.0Hz G3, 261.6Hz C4)
    c_chord = (np.sin(2 * np.pi * 130.8 * d_dt) * 0.4 +
               np.sin(2 * np.pi * 164.8 * d_dt) * 0.3 +
               np.sin(2 * np.pi * 196.0 * d_dt) * 0.3 +
               np.sin(2 * np.pi * 261.6 * d_dt) * 0.2)
    d_env = np.clip(d_dt / 4.0, 0, 1) * np.clip((70.0 - t[d_mask]) / 2.5, 0, 1)
    dawn_pad[d_mask] = c_chord * d_env * 0.14
    
    return sub + riser + winter_pad + dawn_pad

# 2. Environmental Foley Bed (Impact Detonation, Firestorm, Boiling Tektites, Winter Gale)
def generate_foley_bed():
    t = np.linspace(0, TOTAL_DUR, TOTAL_SAMPLES, endpoint=False)
    np.random.seed(66038)
    raw_noise = np.random.normal(0, 1, TOTAL_SAMPLES)
    
    # Massive 100M Megaton Supersonic Blast Detonation at 10.4s
    blast_track = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    b_mask = (t >= 10.4) & (t < 18.0)
    b_dt = t[b_mask] - 10.4
    # Sub-kick transient (35Hz downward exponential sweep)
    sub_boom = np.sin(2 * np.pi * (35.0 * np.exp(-b_dt * 0.8)) * b_dt) * np.exp(-b_dt * 0.6) * 0.45
    # High-pressure shockwave explosive roar
    shock_noise = butter_lowpass_filter(np.random.normal(0, 1, len(b_dt)), 180, SR, order=3) * np.exp(-b_dt * 0.4) * 0.40
    # Initial explosive snap
    snap = np.sin(2 * np.pi * 1200.0 * b_dt) * np.exp(-b_dt * 45.0) * 0.30
    blast_track[b_mask] = (sub_boom + shock_noise + snap)
    
    # Scene 3: Thermal Infrared Firestorm Crackle (20.5s - 31.5s)
    fire_track = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    fire_mask = (t >= 20.5) & (t < 31.5)
    f_len = np.sum(fire_mask)
    f_noise = np.random.normal(0, 1, f_len)
    f_hiss = butter_bandpass_filter(f_noise, 600, 4200, SR, order=2)
    # Random popping embers
    pops = (np.random.uniform(0, 1, f_len) > 0.996).astype(np.float64) * np.random.uniform(0.3, 0.9, f_len)
    f_env = np.sin(np.pi * np.clip((t[fire_mask] - 20.5) / 11.0, 0, 1))
    fire_track[fire_mask] = (f_hiss * 0.18 + pops * 0.22) * f_env * 0.25
    
    # Scene 4: Boiling Glass Tektite Hail & 300m Wave Roar (31.0s - 41.5s)
    glass_track = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    g_mask = (t >= 31.0) & (t < 41.5)
    g_len = np.sum(g_mask)
    # Tektite crystalline pings (high micro-resonances)
    g_noise = np.random.normal(0, 1, g_len)
    g_hiss = butter_bandpass_filter(g_noise, 1500, 6000, SR, order=2) * 0.16
    # Low ocean tsunami surge
    tsunami_rumble = butter_lowpass_filter(g_noise, 90, SR, order=3) * 0.35
    g_env = np.sin(np.pi * np.clip((t[g_mask] - 31.0) / 10.5, 0, 1))
    glass_track[g_mask] = (g_hiss + tsunami_rumble) * g_env * 0.26
    
    # Scene 5: Nuclear Impact Winter Freezing Gale (41.5s - 52.5s)
    winter_track = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    w_mask = (t >= 41.5) & (t < 52.5)
    w_len = np.sum(w_mask)
    w_noise = np.random.normal(0, 1, w_len)
    w_howl = butter_bandpass_filter(w_noise, 180, 750, SR, order=2) * 0.32
    w_env = np.sin(np.pi * np.clip((t[w_mask] - 41.5) / 11.0, 0, 1))
    winter_track[w_mask] = w_howl * w_env * 0.24
    
    return blast_track + fire_track + glass_track + winter_track

# 3. Synchronized Camera Glide Whooshes (1.2s each, aligned with new camera transitions)
def generate_camera_whooshes():
    whoosh_track = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    # New camera glide triggers:
    # 1->2 (9.5s), 2->3 (20.2s), 3->4 (30.4s), 4->5 (40.8s), 5->6 (51.6s)
    triggers = [9.5, 20.2, 30.4, 40.8, 51.6]
    dur = 1.1
    n_samples = int(dur * SR)
    
    for trig in triggers:
        start_idx = int(trig * SR)
        end_idx = min(start_idx + n_samples, TOTAL_SAMPLES)
        local_len = end_idx - start_idx
        
        lt = np.linspace(0, dur, n_samples)[:local_len]
        noise = np.random.normal(0, 1, local_len)
        filt_noise = butter_bandpass_filter(noise, 200, 2200, SR, order=2)
        env = np.sin(np.pi * (lt / dur)) ** 1.6
        
        pitch_curve = 75.0 * (1.0 - 0.40 * (lt / dur))
        sub_sweep = np.sin(2 * np.pi * pitch_curve * lt) * env * 0.30
        
        whoosh_track[start_idx:end_idx] += (filt_noise * 0.65 + sub_sweep) * env * 0.14
        
    return whoosh_track

# 4. Tactile Archival Rubber Stamp Impacts
def generate_stamp_thuds():
    stamp_track = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    # New stamp trigger times matching the new pacing:
    stamp_times = [3.2, 13.0, 23.6, 33.8, 44.5, 54.8, 63.8]
    
    dur = 0.26
    n_samples = int(dur * SR)
    
    for st in stamp_times:
        start_idx = int(st * SR)
        end_idx = min(start_idx + n_samples, TOTAL_SAMPLES)
        local_len = end_idx - start_idx
        
        lt = np.linspace(0, dur, n_samples)[:local_len]
        # Low wood resonance (72Hz)
        body = np.sin(2 * np.pi * 72.0 * lt) * np.exp(-lt * 25.0)
        # Sharp transient snap (1800Hz)
        click = np.sin(2 * np.pi * 1800.0 * lt) * np.exp(-lt * 90.0)
        
        stamp_track[start_idx:end_idx] += (body * 0.72 + click * 0.28) * 0.18
        
    return stamp_track

def main():
    print("[Audio Mix Ep4] Synthesizing upgraded cinematic music bed...")
    music_bed = generate_cinematic_music_bed()
    
    print("[Audio Mix Ep4] Synthesizing atmospheric foley textures...")
    foley_bed = generate_foley_bed()
    
    print("[Audio Mix Ep4] Synthesizing camera glide whooshes...")
    whooshes = generate_camera_whooshes()
    
    print("[Audio Mix Ep4] Synthesizing tactile archival stamp thuds...")
    stamps = generate_stamp_thuds()
    
    # Load Master Kokoro Voice
    vo_path = os.path.join(AUDIO_DIR, "vo_chicxulub.wav")
    sr, vo = wavfile.read(vo_path)
    if vo.dtype == np.int16:
        vo = vo.astype(np.float64) / 32768.0
    elif vo.dtype == np.float32:
        vo = vo.astype(np.float64)
        
    if len(vo) < TOTAL_SAMPLES:
        vo = np.pad(vo, (0, TOTAL_SAMPLES - len(vo)))
    else:
        vo = vo[:TOTAL_SAMPLES]
        
    # Dynamic Sidechain Ducking: duck music and foley during voice
    vo_envelope = butter_lowpass_filter(np.abs(vo), 6, SR, order=2)
    # Duck factor: 0.55 during loud voice, 1.0 during silences/transitions
    duck = 1.0 - 0.40 * np.clip(vo_envelope / 0.12, 0, 1)
    
    print("[Audio Mix Ep4] Applying dynamic sidechain ducking and summing tracks...")
    bgm_composite = (music_bed * 0.70 + foley_bed * 0.65) * duck
    
    # Master balance: Voice upfront (0.92), ducked background (0.48), whooshes & stamps cut cleanly
    mix = vo * 0.92 + bgm_composite + whooshes * 0.38 + stamps * 0.42
    
    # Hyperbolic tangent soft saturation limiter
    mix = np.tanh(mix * 1.08)
    
    # Peak normalization to -0.3 dBFS (0.965)
    max_peak = np.max(np.abs(mix))
    if max_peak > 0:
        mix = mix * (0.965 / max_peak)
        
    out_wav = os.path.join(AUDIO_DIR, "vo_chicxulub_cinematic.wav")
    wavfile.write(out_wav, SR, (mix * 32767).astype(np.int16))
    print(f"[Audio Mix Ep4] SUCCESS: Saved master audio mix -> {out_wav}")
    
    out_mp3 = os.path.join(AUDIO_DIR, "vo_chicxulub_cinematic.mp3")
    ffmpeg_exe = r"C:\Program Files\ShareX\ffmpeg.exe"
    subprocess.run([ffmpeg_exe, "-y", "-i", out_wav, "-b:a", "192k", out_mp3], check=True, capture_output=True)
    print(f"[Audio Mix Ep4] SUCCESS: Converted MP3 preview -> {out_mp3}")

if __name__ == "__main__":
    main()
