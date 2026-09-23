import os
import json
import numpy as np
import scipy.io.wavfile as wavfile
from scipy.signal import butter, lfilter

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(PROJECT_ROOT, "assets", "episode2_great_dying", "audio")
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

# 1. Synthesize Cinematic Dark Ambient Drone Bed (70.0s)
def generate_ambient_drone():
    t = np.linspace(0, TOTAL_DUR, TOTAL_SAMPLES, endpoint=False)
    
    # Sub-bass fundamentals: 50 Hz & 55 Hz (binaural beat 5 Hz)
    f1 = 50.0 + 1.5 * np.sin(2 * np.pi * 0.05 * t)
    f2 = 55.0 + 1.2 * np.cos(2 * np.pi * 0.04 * t)
    sub1 = np.sin(2 * np.pi * f1 * t)
    sub2 = np.sin(2 * np.pi * f2 * t)
    
    # Ominous 5th harmonic (110 Hz, 165 Hz)
    h1 = 0.35 * np.sin(2 * np.pi * 110.0 * t + 0.3)
    h2 = 0.20 * np.sin(2 * np.pi * 165.0 * t + 0.8)
    
    # Low filtered tectonic rumble noise
    np.random.seed(42)
    noise = np.random.normal(0, 1, TOTAL_SAMPLES)
    rumble = butter_lowpass_filter(noise, 80, SR, order=4) * 0.45
    
    # Slow breathing LFO modulation (period ~ 12s)
    lfo = 0.75 + 0.25 * np.sin(2 * np.pi * (1.0 / 12.0) * t)
    
    drone = (sub1 * 0.45 + sub2 * 0.40 + h1 + h2 + rumble) * lfo
    
    # Fade in (3s) and fade out (4s)
    fade_in = np.clip(t / 3.0, 0, 1)
    fade_out = np.clip((TOTAL_DUR - t) / 4.0, 0, 1)
    drone = drone * fade_in * fade_out
    
    # Normalize drone to -18 dBFS (~0.12 amplitude)
    max_val = np.max(np.abs(drone))
    if max_val > 0:
        drone = (drone / max_val) * 0.125
        
    return drone

# 2. Synthesize Cinematic Glide Whoosh SFX (1.2s)
def generate_whoosh():
    dur = 1.2
    n = int(dur * SR)
    t = np.linspace(0, dur, n, endpoint=False)
    
    np.random.seed(101)
    noise = np.random.normal(0, 1, n)
    
    # Bell curve volume envelope peaking at 0.5s
    env = np.exp(-((t - 0.55) ** 2) / (2 * (0.18 ** 2)))
    
    # Pitch drop sub sweep (85 Hz -> 35 Hz)
    freq = 85.0 - 50.0 * (t / dur)
    sub = np.sin(2 * np.pi * freq * t) * env * 0.6
    
    # Filtered bandpass noise
    filtered = butter_bandpass_filter(noise, 120, 600, SR, order=2) * env * 0.5
    
    whoosh = (sub + filtered)
    max_val = np.max(np.abs(whoosh))
    if max_val > 0:
        whoosh = (whoosh / max_val) * 0.28
    return whoosh

# 3. Synthesize Heavy Rubber Stamp Slam Thud (0.35s)
def generate_stamp_slam():
    dur = 0.35
    n = int(dur * SR)
    t = np.linspace(0, dur, n, endpoint=False)
    
    # Fast decaying sub-bass thud (75 Hz -> 35 Hz)
    f_sub = 75.0 * np.exp(-t * 12) + 35.0
    sub = np.sin(2 * np.pi * f_sub * t) * np.exp(-t * 14) * 0.75
    
    # Sharp mechanical paper / wooden snap transient (first 30ms)
    snap_env = np.exp(-t * 90)
    snap_freq = 1800.0 * np.exp(-t * 50) + 400.0
    snap = np.sin(2 * np.pi * snap_freq * t) * snap_env * 0.45
    
    slam = sub + snap
    max_val = np.max(np.abs(slam))
    if max_val > 0:
        slam = (slam / max_val) * 0.38
    return slam

def main():
    print("[Audio Engine] Synthesizing Cinematic Multi-Track Sound Bed...")
    
    # 1. Base Ambient Drone
    drone = generate_ambient_drone()
    
    # 2. SFX Layer Buffer
    sfx_track = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    
    whoosh = generate_whoosh()
    slam = generate_stamp_slam()
    
    # Transition whooshes (at glide start points)
    whoosh_times = [9.1, 20.8, 32.2, 43.3, 54.3]
    for wt in whoosh_times:
        idx = int(wt * SR)
        end_idx = min(idx + len(whoosh), TOTAL_SAMPLES)
        length = end_idx - idx
        sfx_track[idx:end_idx] += whoosh[:length]
        print(f"  + Added Transition Whoosh at {wt}s")
        
    # Rubber stamp slam thuds (at exact stamp impact points)
    stamp_times = [3.2, 13.6, 25.5, 36.0, 47.0, 58.0, 66.5]
    for st in stamp_times:
        idx = int(st * SR)
        end_idx = min(idx + len(slam), TOTAL_SAMPLES)
        length = end_idx - idx
        sfx_track[idx:end_idx] += slam[:length]
        print(f"  + Added Stamp Slam Thud at {st}s")
        
    # 3. Load Kokoro Voiceover
    vo_path = os.path.join(AUDIO_DIR, "vo_great_dying.wav")
    sr_vo, vo_data = wavfile.read(vo_path)
    
    # Normalize VO data to float -1.0 to 1.0
    if vo_data.dtype == np.int16:
        vo_float = vo_data.astype(np.float64) / 32768.0
    else:
        vo_float = vo_data.astype(np.float64)
        
    if len(vo_float.shape) > 1:
        vo_float = vo_float[:, 0]  # Mono
        
    # Resample or pad VO to match exact TOTAL_SAMPLES
    vo_track = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    copy_len = min(len(vo_float), TOTAL_SAMPLES)
    vo_track[:copy_len] = vo_float[:copy_len]
    
    # Peak normalize VO to -1.0 dBFS (~0.89)
    vo_max = np.max(np.abs(vo_track))
    if vo_max > 0:
        vo_track = (vo_track / vo_max) * 0.89
        
    # 4. Master Multi-Track Summing & Soft Limiting
    # Master = VO (100%) + SFX (100%) + Drone (100%)
    master = vo_track + sfx_track + drone
    
    # Soft saturation / tanh limiting to prevent any digital clipping
    master = np.tanh(master * 0.95)
    master_max = np.max(np.abs(master))
    if master_max > 0:
        master = (master / master_max) * 0.92
        
    # Convert to 16-bit PCM WAV
    master_pcm = (master * 32767).astype(np.int16)
    
    out_master_wav = os.path.join(AUDIO_DIR, "vo_great_dying_cinematic.wav")
    out_master_mp3 = os.path.join(AUDIO_DIR, "vo_great_dying_cinematic.mp3")
    
    wavfile.write(out_master_wav, SR, master_pcm)
    print(f"\n[SUCCESS] Master Cinematic Audio exported: {out_master_wav} ({round(os.path.getsize(out_master_wav)/1024, 1)} KB)")
    
    # Also export MP3 using ffmpeg
    ffmpeg_exe = 'C:\\Program Files\\ShareX\\ffmpeg.exe'
    if not os.path.exists(ffmpeg_exe):
        ffmpeg_exe = 'ffmpeg'
    os.system(f'"{ffmpeg_exe}" -y -i "{out_master_wav}" -b:a 192k "{out_master_mp3}" >nul 2>&1')
    print(f"[SUCCESS] Master MP3 exported: {out_master_mp3}")

if __name__ == "__main__":
    main()
