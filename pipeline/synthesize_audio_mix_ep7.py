import os
import json
import numpy as np
import scipy.io.wavfile as wavfile
from scipy.signal import butter, lfilter
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(PROJECT_ROOT, "assets", "episode7_wow_signal", "audio")
SR = 24000  # 24kHz master rate matching Kokoro TTS

CUES_PATH = os.path.join(AUDIO_DIR, "vo_cues_wow_signal.json")
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

# 1. Deep Space Atmospheric Bed & Investigative Cosmic Drone
def generate_cosmic_drone():
    t = np.linspace(0, TOTAL_DUR, TOTAL_SAMPLES, endpoint=False)
    
    # Sub-bass foundation (42Hz - 46.5Hz slow beating cosmic resonance)
    sub = (np.sin(2 * np.pi * 43.0 * t) * 0.7 + np.sin(2 * np.pi * 46.5 * t) * 0.3) * 0.12
    
    # 120 BPM subtle observatory clock tick (sidereal timekeeper)
    clock_pulse = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    tick_interval = int(0.5 * SR)
    for i in range(0, TOTAL_SAMPLES - int(0.04 * SR), tick_interval):
        dt = np.linspace(0, 0.04, int(0.04 * SR), endpoint=False)
        tick = np.sin(2 * np.pi * 980.0 * dt) * np.exp(-dt * 90.0) * 0.028
        clock_pulse[i:i + len(tick)] += tick

    # Tension harmonic pad during the 6EQUJ5 revelation (50s - 85s)
    tension_pad = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    p_mask = (t >= 50.0) & (t < 85.0)
    p_dt = t[p_mask] - 50.0
    p_osc = (np.sin(2 * np.pi * 146.83 * p_dt) * 0.4 +
             np.sin(2 * np.pi * 174.61 * p_dt) * 0.3 +
             np.sin(2 * np.pi * 220.00 * p_dt) * 0.3)
    p_env = np.clip(p_dt / 3.0, 0, 1) * np.clip((85.0 - t[p_mask]) / 3.0, 0, 1)
    tension_pad[p_mask] = p_osc * p_env * 0.08

    # Wonder / mystery chord pad in Act 5 & Outro (100s - 128s)
    wonder_pad = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    w_mask = (t >= 100.0) & (t < 128.0)
    w_dt = t[w_mask] - 100.0
    w_osc = (np.sin(2 * np.pi * 130.81 * w_dt) * 0.4 +
             np.sin(2 * np.pi * 164.81 * w_dt) * 0.3 +
             np.sin(2 * np.pi * 196.00 * w_dt) * 0.3)
    w_env = np.clip(w_dt / 4.0, 0, 1) * np.clip((128.0 - t[w_mask]) / 3.0, 0, 1)
    wonder_pad[w_mask] = w_osc * w_env * 0.07

    return sub + clock_pulse + tension_pad + wonder_pad

# 2. Tactile Foley Generator
def generate_tactile_foley():
    foley = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    np.random.seed(1420405)

    # A. Folder Open / Dossier Paper Slap
    def add_dossier_open(start_t):
        s_idx = int(start_t * SR)
        dur = 0.45
        e_idx = min(s_idx + int(dur * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        thud = np.sin(2 * np.pi * 95.0 * dt) * np.exp(-dt * 30.0) * 0.42
        whoosh = butter_bandpass_filter(np.random.normal(0, 1, len(dt)), 800, 3200, SR) * np.exp(-dt * 12.0) * 0.22
        clink = np.sin(2 * np.pi * 3600.0 * dt) * np.exp(-dt * 110.0) * 0.18
        foley[s_idx:e_idx] += (thud + whoosh + clink)

    # B. Cosmic Static Radio Hiss
    def add_cosmic_hiss(start_t, length=5.0, gain=0.12):
        s_idx = int(start_t * SR)
        e_idx = min(s_idx + int(length * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        noise = np.random.normal(0, 1, len(dt))
        filtered = butter_bandpass_filter(noise, 600, 4200, SR)
        lfo = 0.7 + 0.3 * np.sin(2 * np.pi * 0.4 * dt)
        env = np.clip(dt / 0.8, 0, 1) * np.clip(((e_idx - s_idx)/SR - dt) / 0.8, 0, 1)
        foley[s_idx:e_idx] += filtered * lfo * env * gain

    # C. 1420.405 MHz Narrowband Sine Tone (The Wow! Signal Carrier Pitch)
    def add_wow_carrier_tone(start_t, length=3.5, freq=1420.0, gain=0.25):
        s_idx = int(start_t * SR)
        e_idx = min(s_idx + int(length * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        # Narrowband carrier with slight interstellar scintillation FM vibrato
        vibrato = 3.5 * np.sin(2 * np.pi * 4.2 * dt)
        tone = np.sin(2 * np.pi * (freq + vibrato) * dt)
        env = np.clip(dt / 0.4, 0, 1) * np.clip(((e_idx - s_idx)/SR - dt) / 0.5, 0, 1)
        foley[s_idx:e_idx] += tone * env * gain

    # D. IBM 1130 Dot-Matrix Impact Printer Chatter
    def add_dotmatrix_printer(start_t, length=3.2):
        s_idx = int(start_t * SR)
        e_idx = min(s_idx + int(length * SR), TOTAL_SAMPLES)
        # Rhythmic pin firing clusters
        for step in np.arange(0, length, 0.045):
            pos = s_idx + int(step * SR)
            if pos + 180 < e_idx:
                pin_dt = np.linspace(0, 0.0075, 180, endpoint=False)
                pin_click = np.sin(2 * np.pi * 2800.0 * pin_dt) * np.exp(-pin_dt * 380.0) * 0.16
                pin_noise = np.random.normal(0, 1, 180) * np.exp(-pin_dt * 450.0) * 0.12
                foley[pos:pos+180] += (pin_click + pin_noise)
        # Tractor feed carriage stepping motor hum
        dt_full = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        step_hum = np.sin(2 * np.pi * 180.0 * dt_full) * 0.04
        foley[s_idx:e_idx] += step_hum

    # E. 72-Second Bell Curve Antenna Beam Transit Sweep
    def add_bell_curve_swell(start_t, length=8.0):
        s_idx = int(start_t * SR)
        e_idx = min(s_idx + int(length * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        # Gaussian bell curve envelope
        center = length / 2.0
        sigma = length / 4.5
        bell_env = np.exp(-0.5 * ((dt - center) / sigma) ** 2)
        # Rising resonant harmonic tone
        tone = (np.sin(2 * np.pi * 320.0 * dt) * 0.6 + np.sin(2 * np.pi * 640.0 * dt) * 0.4)
        sub_rumble = np.sin(2 * np.pi * 55.0 * dt) * 0.5
        foley[s_idx:e_idx] += (tone * 0.12 + sub_rumble * 0.18) * bell_env

    # F. Red Pilot Pen Paper Scribble / Squeak (Circling "Wow!")
    def add_pen_scribble(start_t, length=2.4):
        s_idx = int(start_t * SR)
        e_idx = min(s_idx + int(length * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        # High friction paper scratch
        paper_scratch = butter_bandpass_filter(np.random.normal(0, 1, len(dt)), 1800, 6500, SR)
        # Squeak modulation
        squeak_mod = np.abs(np.sin(2 * np.pi * 7.5 * dt)) ** 2
        pen_body = np.sin(2 * np.pi * 2100.0 * dt) * np.exp(-dt * 4.0) * 0.10
        foley[s_idx:e_idx] += (paper_scratch * squeak_mod * 0.28 + pen_body)

    # G. Punch Card Sorter Mechanical Clatter
    def add_punchcard_clatter(start_t, length=2.5):
        s_idx = int(start_t * SR)
        e_idx = min(s_idx + int(length * SR), TOTAL_SAMPLES)
        for t_off in np.arange(0, length, 0.08):
            pos = s_idx + int(t_off * SR)
            if pos + 300 < e_idx:
                card_dt = np.linspace(0, 0.012, 300, endpoint=False)
                card_flap = (np.random.normal(0, 1, 300) * 0.4 + np.sin(2 * np.pi * 1200 * card_dt) * 0.6) * np.exp(-card_dt * 220) * 0.14
                foley[pos:pos+300] += card_flap

    # H. Giant Radio Telescope Dish Mechanical Motor Groan
    def add_telescope_gear_groan(start_t, length=3.5):
        s_idx = int(start_t * SR)
        e_idx = min(s_idx + int(length * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        gear_drone = np.sin(2 * np.pi * 68.0 * dt) * 0.18 + np.sin(2 * np.pi * 136.0 * dt) * 0.10
        foley[s_idx:e_idx] += gear_drone * np.clip(dt / 1.0, 0, 1) * np.clip(((e_idx - s_idx)/SR - dt) / 1.0, 0, 1)

    # I. Heavy Rubber Stamp Slam (Outro Declassification)
    def add_stamp_slam(start_t):
        s_idx = int(start_t * SR)
        dur = 0.8
        e_idx = min(s_idx + int(dur * SR), TOTAL_SAMPLES)
        dt = np.linspace(0, (e_idx - s_idx) / SR, e_idx - s_idx, endpoint=False)
        heavy_wood_thud = np.sin(2 * np.pi * 72.0 * dt) * np.exp(-dt * 22.0) * 0.78
        rubber_squelch = butter_bandpass_filter(np.random.normal(0, 1, len(dt)), 600, 2400, SR) * np.exp(-dt * 42.0) * 0.48
        desk_resonance = np.sin(2 * np.pi * 115.0 * dt) * np.exp(-dt * 9.0) * 0.32
        foley[s_idx:e_idx] += (heavy_wood_thud + rubber_squelch + desk_resonance)

    # Precise Cue Placements matching the narrative timeline:
    # ACT 1: The Listening Ear
    add_dossier_open(1.0)
    add_cosmic_hiss(1.5, 6.0, gain=0.14)
    add_cosmic_hiss(13.2, 5.0, gain=0.10)

    # ACT 2: The 72-Second Window
    add_dossier_open(23.0)
    add_bell_curve_swell(32.0, 8.5)   # Textbook Gaussian transit swell!

    # ACT 3: Decoding 6EQUJ5
    add_dotmatrix_printer(42.5, 4.0)   # IBM 1130 dot-matrix chatter
    add_punchcard_clatter(45.0, 2.8)   # Keypunch cards
    add_dotmatrix_printer(51.5, 4.5)   # 6EQUJ5 printout chatter
    add_wow_carrier_tone(54.0, 5.0, freq=1420.0, gain=0.30) # Spiking signal!
    add_wow_carrier_tone(65.0, 6.0, freq=1420.405, gain=0.28) # Hydrogen Line waterhole tone!

    # ACT 4: The Failed Explanations
    add_pen_scribble(80.5, 3.2)        # Red Pilot pen scribbles "Wow!" on paper!
    add_wow_carrier_tone(84.0, 3.5, freq=1420.0, gain=0.22)
    add_cosmic_hiss(89.0, 6.0, gain=0.11)

    # ACT 5: The Silent Void
    add_telescope_gear_groan(101.5, 4.0) # VLA Dish slewing to coordinates
    add_cosmic_hiss(106.0, 6.0, gain=0.08) # Complete, silent void...
    add_cosmic_hiss(113.0, 5.0, gain=0.07)

    # OUTRO: Investigation Unsolved
    add_stamp_slam(120.2)              # HEAVY RUBBER STAMP SLAM on 6EQUJ5 printout!

    return foley

def main():
    print(f"[Synthesize Ep7] Loading narration file...")
    vo_path = os.path.join(AUDIO_DIR, "vo_wow_signal_narration.wav")
    sr, vo = wavfile.read(vo_path)
    if vo.dtype != np.float32:
        vo = vo.astype(np.float32) / 32768.0

    dur_sec = len(vo) / SR
    print(f"  Narration length: {round(dur_sec, 2)}s (Target timeline: {TOTAL_DUR}s)")

    drone = generate_cosmic_drone()
    foley = generate_tactile_foley()

    # Dynamic Sidechain Ducking:
    # When voice is active, duck music/ambient drone by -45%
    print("[Synthesize Ep7] Applying -45% dynamic sidechain ducking...")
    max_len = min(len(vo), len(drone))
    vo_abs = np.abs(vo[:max_len])
    # Smooth envelope
    env = butter_lowpass_filter(vo_abs, 4.0, SR)
    max_env = np.max(env) if np.max(env) > 0 else 1.0
    norm_env = np.clip(env / max_env, 0, 1)

    duck_gain = 1.0 - (norm_env * 0.45)
    ducked_drone = drone[:max_len] * duck_gain

    # Master summing:
    master = (vo[:max_len] * 0.95) + (ducked_drone * 0.68) + (foley[:max_len] * 0.85)

    # Peak normalization to -1.0 dB (0.89 max amplitude)
    peak = np.max(np.abs(master))
    if peak > 0:
        master = (master / peak) * 0.89

    master_int16 = (master * 32767.0).astype(np.int16)
    out_wav = os.path.join(AUDIO_DIR, "vo_wow_signal_cinematic.wav")
    wavfile.write(out_wav, SR, master_int16)
    print(f"[Synthesize Ep7] Master WAV generated: {out_wav} ({round(os.path.getsize(out_wav)/(1024*1024), 2)} MB)")

    # Encode high quality MP3
    out_mp3 = os.path.join(AUDIO_DIR, "vo_wow_signal_cinematic.mp3")
    cmd = [
        "ffmpeg", "-y", "-i", out_wav,
        "-b:a", "192k",
        out_mp3
    ]
    subprocess.run(cmd, check=True, shell=True)
    print(f"[Synthesize Ep7] Master MP3 encoded: {out_mp3} ({round(os.path.getsize(out_mp3)/1024, 1)} KB)")

if __name__ == "__main__":
    main()
