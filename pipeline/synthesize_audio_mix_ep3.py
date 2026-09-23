import os
import json
import numpy as np
import scipy.io.wavfile as wavfile
from scipy.signal import butter, lfilter

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(PROJECT_ROOT, "assets", "episode3_carnian_pluvial", "audio")
SR = 24000  # Matching Kokoro TTS 24kHz master sample rate
TOTAL_DUR = 70.0
TOTAL_SAMPLES = int(TOTAL_DUR * SR)

def butter_lowpass_filter(data, cutoff, fs, order=3):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return lfilter(b, a, data)

def butter_bandpass_filter(data, lowcut, highcut, fs, order=2):
    nyq = 0.5 * fs
    low = max(lowcut / nyq, 0.001)
    high = min(highcut / nyq, 0.999)
    b, a = butter(order, [low, high], btype='band', analog=False)
    return lfilter(b, a, data)

# 1. Synthesize Atmospheric Environment (Dry Wind -> Torrential Rainstorm -> Thunder)
def generate_environmental_bed():
    t = np.linspace(0, TOTAL_DUR, TOTAL_SAMPLES, endpoint=False)
    np.random.seed(1337)
    raw_noise = np.random.normal(0, 1, TOTAL_SAMPLES)
    
    # Base Tectonic Drone (50Hz + 55Hz)
    sub1 = np.sin(2 * np.pi * 50.0 * t)
    sub2 = np.sin(2 * np.pi * 55.0 * t)
    rumble = butter_lowpass_filter(raw_noise, 75, SR, order=4) * 0.4
    base_drone = (sub1 * 0.4 + sub2 * 0.35 + rumble) * 0.08
    
    # Dry Arid Wind for Scenes 1 & 2 (0s - 21.4s)
    wind_band = butter_bandpass_filter(raw_noise, 200, 800, SR, order=2)
    wind_env = np.clip(1.0 - (t - 18.0) / 3.4, 0, 1)
    wind_track = wind_band * wind_env * 0.04
    
    # Torrential Rainstorm Bed (Starts at 21.4s with sudden cloudburst, intensifies through 55s)
    rain_noise = np.random.normal(0, 1, TOTAL_SAMPLES)
    rain_hiss = butter_bandpass_filter(rain_noise, 800, 6000, SR, order=2)
    
    # Rain envelope
    rain_env = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    # Cloudburst rise: 21.4s to 24.0s
    rise_mask = (t >= 21.4) & (t < 24.0)
    rain_env[rise_mask] = (t[rise_mask] - 21.4) / 2.6
    # Full storm: 24.0s to 55.0s
    storm_mask = (t >= 24.0) & (t < 55.0)
    rain_env[storm_mask] = 1.0
    # Gentle taper into Triassic dawn: 55.0s to 68.0s
    taper_mask = (t >= 55.0) & (t < 68.0)
    rain_env[taper_mask] = 1.0 - (t[taper_mask] - 55.0) / 15.0
    
    rain_track = rain_hiss * rain_env * 0.075
    
    # Distant Thunder Strikes at 22.5s and 34.0s
    thunder_track = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    for th_time in [22.8, 34.2, 45.5]:
        th_idx = int(th_time * SR)
        th_len = int(3.5 * SR)
        if th_idx + th_len < TOTAL_SAMPLES:
            tt = np.linspace(0, 3.5, th_len, endpoint=False)
            t_noise = np.random.normal(0, 1, th_len)
            t_low = butter_lowpass_filter(t_noise, 65, SR, order=4)
            th_env = np.exp(-tt * 1.2) * (1.0 + 0.3 * np.sin(2 * np.pi * 35 * tt))
            thunder_track[th_idx:th_idx + th_len] += t_low * th_env * 0.35
            
    bed = base_drone + wind_track + rain_track + thunder_track
    return bed

# 2. Camera Glide Whoosh FX
def generate_whoosh_sound(dur=1.1):
    n_samples = int(dur * SR)
    t = np.linspace(0, dur, n_samples, endpoint=False)
    np.random.seed(99)
    noise = np.random.normal(0, 1, n_samples)
    
    # Frequency sweep bandpass 180Hz -> 1800Hz -> 120Hz
    mid = dur * 0.45
    env = np.exp(-((t - mid) ** 2) / (2 * (0.16 ** 2)))
    swept = butter_bandpass_filter(noise, 250, 2400, SR, order=2)
    
    # Sub drop whoosh transient
    sub_drop = np.sin(2 * np.pi * (140.0 - 90.0 * (t / dur)) * t) * env
    whoosh = (swept * 0.7 + sub_drop * 0.5) * env
    return whoosh

# 3. Tactile Rubber Stamp Slam Impact Thud
def generate_stamp_slam():
    dur = 0.45
    n_samples = int(dur * SR)
    t = np.linspace(0, dur, n_samples, endpoint=False)
    
    # Wooden stamp body punch (75 Hz + 140 Hz)
    thud = np.sin(2 * np.pi * 75.0 * t) * np.exp(-t * 22.0)
    sub = np.sin(2 * np.pi * 45.0 * t) * np.exp(-t * 14.0) * 0.8
    
    # Crisp ink paper snap (highpass band around 1800 Hz)
    np.random.seed(77)
    noise = np.random.normal(0, 1, n_samples)
    snap = butter_bandpass_filter(noise, 1200, 3200, SR, order=2) * np.exp(-t * 55.0) * 0.45
    
    impact = (thud * 0.7 + sub * 0.4 + snap * 0.35)
    return impact

def main():
    print("[Audio Synthesizer Ep3] Generating multi-track environmental and SFX sound bed...")
    env_bed = generate_environmental_bed()
    sfx_track = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    
    # Whoosh cues (matching 5 camera glides)
    whoosh_cues = [9.1, 20.8, 32.2, 43.3, 54.3]
    whoosh_snd = generate_whoosh_sound(1.1)
    for cue in whoosh_cues:
        idx = int(cue * SR)
        l = min(len(whoosh_snd), TOTAL_SAMPLES - idx)
        sfx_track[idx:idx + l] += whoosh_snd[:l] * 0.45
        
    # Stamp slam cues (matching archival stamp impacts)
    stamp_cues = [3.2, 13.6, 25.5, 36.0, 47.0, 58.0, 66.5]
    stamp_snd = generate_stamp_slam()
    for cue in stamp_cues:
        idx = int(cue * SR)
        l = min(len(stamp_snd), TOTAL_SAMPLES - idx)
        sfx_track[idx:idx + l] += stamp_snd[:l] * 0.75

    # Load Voiceover
    vo_path = os.path.join(AUDIO_DIR, "vo_carnian_pluvial.wav")
    if not os.path.exists(vo_path):
        print(f"[Wait] vo_carnian_pluvial.wav not ready yet at {vo_path}")
        return
        
    sr_vo, vo_data = wavfile.read(vo_path)
    if vo_data.dtype == np.int16:
        vo_float = vo_data.astype(np.float64) / 32768.0
    else:
        vo_float = vo_data.astype(np.float64)
        
    if len(vo_float.shape) > 1:
        vo_float = vo_float[:, 0]
        
    vo_track = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    copy_len = min(len(vo_float), TOTAL_SAMPLES)
    vo_track[:copy_len] = vo_float[:copy_len]
    
    # Peak normalize VO to -1.0 dBFS (~0.89)
    vo_max = np.max(np.abs(vo_track))
    if vo_max > 0:
        vo_track = (vo_track / vo_max) * 0.89
        
    # Master Summing & Soft Saturation
    master = vo_track + sfx_track + env_bed
    master = np.tanh(master * 0.95)
    master_max = np.max(np.abs(master))
    if master_max > 0:
        master = (master / master_max) * 0.92
        
    master_pcm = (master * 32767).astype(np.int16)
    out_master_wav = os.path.join(AUDIO_DIR, "vo_carnian_pluvial_cinematic.wav")
    out_master_mp3 = os.path.join(AUDIO_DIR, "vo_carnian_pluvial_cinematic.mp3")
    
    wavfile.write(out_master_wav, SR, master_pcm)
    print(f"[SUCCESS] Master Cinematic Audio exported: {out_master_wav} ({round(os.path.getsize(out_master_wav)/1024, 1)} KB)")
    
    ffmpeg_exe = r"C:\Program Files\ShareX\ffmpeg.exe"
    if not os.path.exists(ffmpeg_exe):
        ffmpeg_exe = "ffmpeg"
    os.system(f'"{ffmpeg_exe}" -y -i "{out_master_wav}" -b:a 192k "{out_master_mp3}" >nul 2>&1')
    print(f"[SUCCESS] Master MP3 exported: {out_master_mp3}")

if __name__ == "__main__":
    main()
