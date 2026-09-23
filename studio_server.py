#!/usr/bin/env python3
"""
Bang Studio Pro — Companion Backend Server
Serves the web app UI and provides REST API endpoints to:
1. Fetch style presets, topics, and design tokens
2. Generate production-ready standalone Bang Motion HTML files
3. Trigger headless Puppeteer + FFmpeg video rendering in the background
4. Inspect render progress and stream logs
"""

import http.server
import socketserver
import json
import os
import sys
import subprocess
import threading
import urllib.parse
import urllib.error
import urllib.request
import base64
import io
from pathlib import Path

PORT = 5200
PROJECT_ROOT = Path(__file__).resolve().parent

ACTIVE_JOB = {
    "status": "idle",
    "target": None,
    "progress": 0.0,
    "frame": 0,
    "total_frames": 1815,
    "log": [],
    "error": None
}
JOB_LOCK = threading.Lock()

CREATOR_STYLES = [
    {
        "id": "vox",
        "name": "Vox / Johnny Harris",
        "subtitle": "Tactile Investigative Journalism & Archival Dossier",
        "badge": "INVESTIGATIVE",
        "theme": {
            "bg": "#f5eee4",
            "bgSecondary": "#e8dcce",
            "ink": "#18181b",
            "mute": "#71717a",
            "accent": "#facc15",
            "accentRed": "#ef4444",
            "cardBg": "#ffffff",
            "texture": "paper",
            "fontDisplay": "'Archivo', sans-serif",
            "fontHand": "'Caveat', cursive",
            "fontMono": "'JetBrains Mono', monospace"
        },
        "description": "Textured archival paper base, real official Republic gazette decree clippings (Garuda seal), live SVG highlighter marks, transparent masking tape, hand-drawn annotations, and a 12-15fps handcrafted tactile feel.",
        "antiSlopGuide": "Authentic scanned archival decrees, real statistical BPS census tables, and highlighters. Zero floating 3D plastic toys."
    },
    {
        "id": "bloomberg",
        "name": "Bloomberg / Financial Times",
        "subtitle": "Macroeconomic Terminal & High-Density Data Journalism",
        "badge": "FINANCIAL TERMINAL",
        "theme": {
            "bg": "#070b14",
            "bgSecondary": "#0f172a",
            "ink": "#f8fafc",
            "mute": "#94a3b8",
            "accent": "#f59e0b",
            "accentRed": "#f43f5e",
            "cardBg": "rgba(13, 20, 36, 0.94)",
            "texture": "financial-grid",
            "fontDisplay": "'Inter', sans-serif",
            "fontHand": "'JetBrains Mono', monospace",
            "fontMono": "'JetBrains Mono', monospace"
        },
        "description": "Dark obsidian terminal aesthetic with Financial Times salmon and copper-gold accents. Dual-axis baseline charts, real recession bands, verified World Bank source citations, and live ticker tape.",
        "antiSlopGuide": "Precise numerical axes, verified economic indicators, calibrated data curves with benchmark target thresholds."
    },
    {
        "id": "polymatter",
        "name": "PolyMatter / Visual Capitalist",
        "subtitle": "Clean Structural Systems & Supply Chain Flowcharts",
        "badge": "SYSTEM DYNAMICS",
        "theme": {
            "bg": "#081026",
            "bgSecondary": "#111d3d",
            "ink": "#f8fafc",
            "mute": "#94a3b8",
            "accent": "#38bdf8",
            "accentRed": "#f43f5e",
            "cardBg": "#111d3d",
            "texture": "isometric-grid",
            "fontDisplay": "'Inter', sans-serif",
            "fontHand": "'JetBrains Mono', monospace",
            "fontMono": "'JetBrains Mono', monospace"
        },
        "description": "Precision vector infographics, interconnected supply chain nodes (Mines -> Smelters -> Gigafactories) with moving energy pulses, and demographic age pyramid breakdowns.",
        "antiSlopGuide": "Translate statistics into interactive structural nodes and percentage distributions. Zero decorative fluff."
    },
    {
        "id": "magnates",
        "name": "MagnatesMedia / ColdFusion",
        "subtitle": "Cinematic Noir & Luxury 2.5D Parallax Parallels",
        "badge": "CINEMATIC NOIR",
        "theme": {
            "bg": "#09090b",
            "bgSecondary": "#18181b",
            "ink": "#fafafa",
            "mute": "#a1a1aa",
            "accent": "#f59e0b",
            "accentRed": "#dc2626",
            "cardBg": "rgba(24, 24, 27, 0.88)",
            "texture": "noir-dust",
            "fontDisplay": "'Cinzel', 'Playfair Display', serif",
            "fontHand": "'Inter', sans-serif",
            "fontMono": "'JetBrains Mono', monospace"
        },
        "description": "High-contrast obsidian vignette with dramatic top-down golden spotlights, 2.5D layered photographic cutouts with depth blur, particle atmosphere, and gold-embossed seals.",
        "antiSlopGuide": "Cutout real historical figures, real bullion stacks, or authentic geological crystals with specular rim-lighting."
    },
    {
        "id": "cleo",
        "name": "Cleo Abram: Huge If True",
        "subtitle": "Futuristic Tech Explainer & Nanometer Schematics",
        "badge": "TECH FUTURISM",
        "theme": {
            "bg": "#050711",
            "bgSecondary": "#0c1229",
            "ink": "#ffffff",
            "mute": "#94a3b8",
            "accent": "#00f0ff",
            "accentRed": "#f43f5e",
            "cardBg": "rgba(12, 18, 41, 0.85)",
            "texture": "cyber-schematic",
            "fontDisplay": "'Inter', sans-serif",
            "fontHand": "'JetBrains Mono', monospace",
            "fontMono": "'JetBrains Mono', monospace"
        },
        "description": "Cyber-blueprint dark grid with neon cyan and electric ultraviolet accents, layered glassmorphism panels, and exploded technical dimension callouts with measurement caliper lines.",
        "antiSlopGuide": "Real technical specs (nanometer node, megawatt capacity, component counts) with precise blueprint callouts."
    }
]

TOPIC_PRESETS = [
    {
        "id": "indonesia_hari_ini",
        "title": "Indonesia Hari Ini: Di Persimpangan Emas atau Perangkap?",
        "category": "Geopolitics & Macroeconomics",
        "angle": "Critical Balance of Industrialization vs Household Purchasing Power",
        "beats": [
            {
                "beat": 1,
                "title": "Geopolitical Hook & Demographic Window",
                "time": "0:00 - 0:08",
                "claim": "Indonesia berada di persimpangan paling krusial dalam sejarahnya.",
                "subClaim": "Puncak bonus demografi 2030-2035 dengan sisa jendela waktu 12 tahun.",
                "visualElement": "Peta radar satelit Indonesia + highlight kepulauan strategis + data piramida BPS.",
                "stat": "282 Juta Jiwa",
                "statLabel": "Puncak Bonus Demografi"
            },
            {
                "beat": 2,
                "title": "The Nickel & EV Boom",
                "time": "0:08 - 0:18",
                "claim": "Hilirisasi mineral meledak luar biasa.",
                "subClaim": "Indonesia kini menguasai lebih dari 52% pasokan nikel dunia.",
                "visualElement": "Dokumen ekspor hilirisasi + diagram rantai pasok bijih nikel ke baterai global.",
                "stat": "52.3% Dunia",
                "statLabel": "Pangsa Pasar Nikel Global"
            },
            {
                "beat": 3,
                "title": "The Middle-Class Squeeze",
                "time": "0:18 - 0:28",
                "claim": "Di balik angka megah, 9,4 juta kelas menengah tergerus turun kelas.",
                "subClaim": "Alarm nyata penurunan daya beli masyarakat dan deindustrialisasi dini.",
                "visualElement": "Lembar survei BPS resmi dengan highlighter merah di angka penurunan 57,3jt -> 47,8jt.",
                "stat": "-9.48 Juta",
                "statLabel": "Kelas Menengah Terdegradasi"
            },
            {
                "beat": 4,
                "title": "Digital Acceleration & AI",
                "time": "0:28 - 0:38",
                "claim": "Penetrasi digital tembus delapan puluh persen.",
                "subClaim": "Talenta muda memutar ekonomi digital senilai ribuan triliun rupiah.",
                "visualElement": "Grafik pertumbuhan GMV digital US$ 100B+ dan adopsi AI talenta muda.",
                "stat": "Rp 1.400 T",
                "statLabel": "Valuasi Ekonomi Digital"
            },
            {
                "beat": 5,
                "title": "Middle Income Trap Benchmark",
                "time": "0:38 - 0:48",
                "claim": "Hanya lima belas persen negara yang lolos jadi negara maju.",
                "subClaim": "Target PDB per kapita harus melompat dari $4.920 ke $13.845 sebelum 2045.",
                "visualElement": "Kurva garis PDB Bank Dunia: ambang batas negara maju vs posisi Indonesia.",
                "stat": "15 dari 101",
                "statLabel": "Negara Lolos Sejak 1960"
            },
            {
                "beat": 6,
                "title": "Resolution: Indonesia Emas 2045",
                "time": "0:48 - 1:00",
                "claim": "Kuncinya: manufaktur bernilai tinggi, riset nyata, dan integritas hukum.",
                "subClaim": "Indonesia Emas bukan hadiah, melainkan masa depan yang harus direbut hari ini.",
                "visualElement": "Tiga pilar roadmap eksekusi + segel medali Garuda Emas beremboss.",
                "stat": "US$ 13,845",
                "statLabel": "Ambang PDB Target 2045"
            }
        ]
    },
    {
        "id": "semiconductor_war",
        "title": "Perang Semikonduktor: Blokade Silikon AS vs China",
        "category": "Tech Geopolitics",
        "angle": "Monopoly of Extreme Ultraviolet (EUV) Lithography & Global Supply Choke points",
        "beats": [
            {
                "beat": 1,
                "title": "The Nanometer Cold War",
                "time": "0:00 - 0:08",
                "claim": "Perang terbesar abad 21 tidak diperebutkan di laut atau udara, tapi di ukuran 2 nanometer.",
                "subClaim": "Blokade total mesin litografi tercanggih dunia.",
                "visualElement": "Wafer silikon makro + peta choke point Selat Taiwan dan Veldhoven Belanda.",
                "stat": "2 nm",
                "statLabel": "Ukuran Transistor Terkecil"
            },
            {
                "beat": 2,
                "title": "ASML Monopoly",
                "time": "0:08 - 0:18",
                "claim": "Hanya ada satu perusahaan di bumi yang mampu membuat mesin EUV.",
                "subClaim": "Monopoli mutlak ASML dengan 100.000 komponen presisi tinggi per mesin.",
                "visualElement": "Skema cetak biru mesin ASML High-NA EUV + label komponen optik Carl Zeiss.",
                "stat": "$380 Juta",
                "statLabel": "Harga 1 Unit Mesin EUV"
            },
            {
                "beat": 3,
                "title": "TSMC Island Fortress",
                "time": "0:18 - 0:28",
                "claim": "Sembilan puluh persen chip tercanggih dunia diproduksi di satu pulau kecil.",
                "subClaim": "Ketergantungan rapuh rantai pasok global pada pabrik fab Taiwan.",
                "visualElement": "Peta klaster foundry Hsinchu Science Park + diagram pasokan chip ke Apple & Nvidia.",
                "stat": "90%",
                "statLabel": "Pangsa Chip Advanced Dunia"
            },
            {
                "beat": 4,
                "title": "US Export Ban & Sanctions",
                "time": "0:28 - 0:38",
                "claim": "Amerika Serikat melarang ekspor chip GPU AI dan alat semikonduktor ke China.",
                "subClaim": "Upaya melumpuhkan lompatan kecerdasan buatan dan superkomputer militer.",
                "visualElement": "Dokumen Department of Commerce Entity List dengan highlighter merah di nama Huawei/SMIC.",
                "stat": "US$ 53B",
                "statLabel": "Subsidi US CHIPS Act"
            },
            {
                "beat": 5,
                "title": "China's Breakthrough & Retaliation",
                "time": "0:38 - 0:48",
                "claim": "China menginvestasikan ratusan miliar dolar untuk kemandirian silikon nasional.",
                "subClaim": "Terobosan tak terduga chip 7nm buatan SMIC mengejutkan analis Barat.",
                "visualElement": "Foto rontgen mikroskop chip Kirin + pembatasan ekspor mineral Galium dan Germanium.",
                "stat": "US$ 140B",
                "statLabel": "Dana Silikon Big Fund China"
            },
            {
                "beat": 6,
                "title": "The New World Order",
                "time": "0:48 - 1:00",
                "claim": "Siapa yang menguasai litografi, menguasai kecerdasan buatan dan kekuatan militer masa depan.",
                "subClaim": "Dunia terbelah menjadi dua ekosistem teknologi yang saling terisolasi.",
                "visualElement": "Diagram dunia bipolair: ekosistem Barat vs ekosistem China.",
                "stat": "100%",
                "statLabel": "Taruhan Kedaulatan Global"
            }
        ]
    }
]

class StudioRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PROJECT_ROOT), **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open(PROJECT_ROOT / "studio.html", "rb") as f:
                self.wfile.write(f.read())
            return

        if path == "/api/presets":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            data = {
                "styles": CREATOR_STYLES,
                "topics": TOPIC_PRESETS
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return

        if path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            with JOB_LOCK:
                data = dict(ACTIVE_JOB)
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return

        if path == "/api/sprites":
            sprites_dir = PROJECT_ROOT / "assets" / "studio" / "sprites"
            sprites_dir.mkdir(parents=True, exist_ok=True)
            files = [
                {
                    "name": f.name,
                    "url": f"/assets/studio/sprites/{f.name}",
                    "size": f.stat().st_size
                }
                for f in sorted(sprites_dir.glob("*.png"), key=lambda x: x.stat().st_mtime, reverse=True)
            ]
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"sprites": files}).encode("utf-8"))
            return

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/generate":
            content_len = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_len)
            try:
                payload = json.loads(post_body.decode('utf-8'))
                target_html = payload.get("filename", "index_studio_output.html")
                code_content = payload.get("code", "")

                target_path = PROJECT_ROOT / target_html
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write(code_content)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "path": str(target_path),
                    "filename": target_html,
                    "bytes": len(code_content)
                }).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))
            return

        if path == "/api/generate_asset":
            content_len = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_len)
            try:
                payload = json.loads(post_body.decode('utf-8'))
                prompt = payload.get("prompt", "")
                filename = payload.get("filename", "sprite_generated.png")
                provider = payload.get("provider", "9router")
                remove_bg = payload.get("transparent", True)

                output_dir = PROJECT_ROOT / "assets" / "studio" / "sprites"
                os.makedirs(output_dir, exist_ok=True)
                output_path = output_dir / filename

                if provider == "9router":
                    router_url = "http://127.0.0.1:20128/v1/images/generations"
                    api_key = "Bearer sk-c4f2444795b190b3-kzvd4h-ea839762"
                    model = "cx/gpt-5.5-image"

                    req_data = json.dumps({
                        "model": model,
                        "prompt": prompt,
                        "n": 1,
                        "size": "1024x1024"
                    }).encode("utf-8")

                    req = urllib.request.Request(
                        router_url,
                        data=req_data,
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": api_key
                        }
                    )
                    try:
                        with urllib.request.urlopen(req, timeout=120) as resp:
                            result = json.loads(resp.read().decode("utf-8"))
                            item = result.get("data", [{}])[0]
                            raw_bytes = None
                            if "b64_json" in item:
                                raw_bytes = base64.b64decode(item["b64_json"])
                            elif "url" in item:
                                with urllib.request.urlopen(item["url"], timeout=60) as img_resp:
                                    raw_bytes = img_resp.read()

                            if raw_bytes:
                                from PIL import Image
                                import numpy as np
                                im = Image.open(io.BytesIO(raw_bytes))
                                if remove_bg:
                                    im = im.convert("RGBA")
                                    arr = np.array(im)
                                    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
                                    is_white = (r > 245) & (g > 245) & (b > 245)
                                    diff = np.maximum.reduce([255 - r, 255 - g, 255 - b])
                                    alpha_soft = np.clip(diff * 6, 0, 255).astype(np.uint8)
                                    arr[:, :, 3] = np.where(is_white, alpha_soft, a)
                                    im = Image.fromarray(arr, "RGBA")
                                im.save(output_path, "PNG")

                                rel_url = f"/assets/studio/sprites/{filename}"
                                self.send_response(200)
                                self.send_header("Content-Type", "application/json")
                                self.send_header("Access-Control-Allow-Origin", "*")
                                self.end_headers()
                                self.wfile.write(json.dumps({
                                    "status": "success",
                                    "provider": "9router",
                                    "model": model,
                                    "url": rel_url,
                                    "path": str(output_path)
                                }).encode("utf-8"))
                                return
                            else:
                                raise Exception("No image data returned from 9Router")
                    except urllib.error.URLError as uerr:
                        self.send_response(503)
                        self.send_header("Content-Type", "application/json")
                        self.send_header("Access-Control-Allow-Origin", "*")
                        self.end_headers()
                        self.wfile.write(json.dumps({
                            "status": "offline",
                            "message": f"9Router offline at http://127.0.0.1:20128: {uerr}. Silakan buka/jalankan aplikasi 9Router di port 20128 terlebih dahulu."
                        }).encode("utf-8"))
                        return
                else:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "status": "info",
                        "provider": "gemini",
                        "message": "Prompt disiapkan untuk Google Gemini / Antigravity generate_image tool."
                    }).encode("utf-8"))
                    return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))
            return

        if path == "/api/render":
            content_len = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_len)
            try:
                payload = json.loads(post_body.decode('utf-8'))
                target_html = payload.get("targetHtml", "index_indonesia_hari_ini.html")
                audio_file = payload.get("audioFile", "assets/episode_indonesia_hari_ini/audio/vo.wav")

                with JOB_LOCK:
                    if ACTIVE_JOB["status"] == "rendering":
                        self.send_response(409)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({"status": "busy", "message": "Another render is in progress."}).encode("utf-8"))
                        return

                    ACTIVE_JOB["status"] = "rendering"
                    ACTIVE_JOB["target"] = target_html
                    ACTIVE_JOB["progress"] = 0.0
                    ACTIVE_JOB["frame"] = 0
                    ACTIVE_JOB["log"] = [f"Launching render for {target_html}..."]
                    ACTIVE_JOB["error"] = None

                t = threading.Thread(target=self._run_render_worker, args=(target_html, audio_file))
                t.daemon = True
                t.start()

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "started", "target": target_html}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

    def _run_render_worker(self, target_html: str, audio_file: str):
        try:
            render_script = PROJECT_ROOT / "pipeline" / "render_mp4.mjs"
            cmd = ["node", str(render_script), target_html, audio_file]

            proc = subprocess.Popen(
                cmd,
                cwd=str(PROJECT_ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                shell=True
            )

            for line in iter(proc.stdout.readline, ''):
                if not line:
                    break
                line_str = line.strip()
                with JOB_LOCK:
                    ACTIVE_JOB["log"].append(line_str)
                    if len(ACTIVE_JOB["log"]) > 100:
                        ACTIVE_JOB["log"] = ACTIVE_JOB["log"][-100:]
                    if "Frame " in line_str and "/" in line_str:
                        try:
                            parts = line_str.split("Frame ")[1].split(" ")[0].split("/")
                            cur_f = int(parts[0])
                            tot_f = int(parts[1])
                            ACTIVE_JOB["frame"] = cur_f
                            ACTIVE_JOB["total_frames"] = tot_f
                            ACTIVE_JOB["progress"] = round((cur_f / tot_f) * 100.0, 1)
                        except Exception:
                            pass

            proc.wait()
            with JOB_LOCK:
                if proc.returncode == 0:
                    ACTIVE_JOB["status"] = "success"
                    ACTIVE_JOB["progress"] = 100.0
                    ACTIVE_JOB["log"].append("Render finished successfully!")
                else:
                    ACTIVE_JOB["status"] = "error"
                    ACTIVE_JOB["error"] = f"Process exited with code {proc.returncode}"
        except Exception as err:
            with JOB_LOCK:
                ACTIVE_JOB["status"] = "error"
                ACTIVE_JOB["error"] = str(err)

def main():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), StudioRequestHandler) as httpd:
        print(f"============================================================")
        print(f"   BANG STUDIO PRO — Editorial & Motion Graphics Director   ")
        print(f"   Server active at: http://127.0.0.1:{PORT}                ")
        print(f"============================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down Studio Server...")
            httpd.shutdown()

if __name__ == "__main__":
    main()
