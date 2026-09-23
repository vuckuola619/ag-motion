import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "assets/episode_indonesia_hari_ini/images"
os.makedirs(OUT_DIR, exist_ok=True)

INK = (15, 23, 42, 255)
INK_MUTED = (100, 116, 139, 255)
RED = (225, 29, 72, 255)
AMBER = (245, 158, 11, 255)
BLUE = (37, 99, 235, 255)
EMERALD = (16, 185, 129, 255)
WHITE = (255, 255, 255, 255)
PAPER = (248, 250, 252, 255)
BORDER = (15, 23, 42, 40)

def get_font(size, bold=False):
    # Try system fonts on Windows
    cand_fonts = [
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\calibrib.ttf" if bold else "C:\\Windows\\Fonts\\calibri.ttf"
    ]
    for p in cand_fonts:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()

def draw_dossier_card(w, h, title, doc_ref, stamp_text, stamp_color):
    im = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    dr = ImageDraw.Draw(im)
    
    # White card base with subtle border
    dr.rounded_rectangle([(10, 10), (w - 10, h - 10)], radius=24, fill=(255, 255, 255, 245), outline=(15, 23, 42, 35), width=2)
    
    # Top header bar
    f_micro = get_font(20, bold=True)
    f_title = get_font(32, bold=True)
    dr.text((36, 32), doc_ref.upper(), fill=INK_MUTED, font=f_micro)
    dr.text((36, 62), title, fill=INK, font=f_title)
    
    # Subtle grid
    for gx in range(40, w - 40, 60):
        dr.line([(gx, 120), (gx, h - 40)], fill=(15, 23, 42, 10), width=1)
    for gy in range(120, h - 40, 60):
        dr.line([(40, gy), (w - 40, gy)], fill=(15, 23, 42, 10), width=1)
        
    return im, dr

# 1. Indonesia Archipelago Geopolitical Map
def create_map_asset():
    W, H = 840, 640
    im, dr = draw_dossier_card(W, H, "GEO-STRATEGIC MAP // ARCHIPELAGO 2026", "DOSSIER // GEOPOLITICS #01", "FASE KRUSIAL", RED)
    
    # Draw stylized islands
    f_tag = get_font(22, bold=True)
    f_lbl = get_font(18, bold=False)
    
    # Sumatra
    dr.polygon([(100, 220), (180, 180), (280, 280), (220, 380), (140, 320)], fill=(37, 99, 235, 30), outline=BLUE, width=3)
    dr.text((120, 260), "SUMATRA", fill=INK, font=f_tag)
    
    # Java
    dr.polygon([(240, 420), (440, 430), (430, 470), (230, 460)], fill=(225, 29, 72, 35), outline=RED, width=3)
    dr.text((280, 435), "JAWA (56% PDB)", fill=INK, font=f_tag)
    
    # Kalimantan & IKN
    dr.polygon([(320, 220), (450, 210), (470, 330), (330, 340)], fill=(16, 185, 129, 30), outline=EMERALD, width=3)
    dr.text((340, 260), "KALIMANTAN", fill=INK, font=f_tag)
    # IKN marker
    dr.ellipse([(420, 280), (440, 300)], fill=AMBER, outline=RED, width=3)
    dr.text((450, 280), "[IKN NUSANTARA]", fill=RED, font=f_tag)
    
    # Sulawesi (Nickel Hub)
    dr.polygon([(520, 230), (560, 210), (590, 310), (540, 360), (510, 300)], fill=(245, 158, 11, 40), outline=AMBER, width=4)
    dr.text((570, 240), "SULAWESI", fill=INK, font=f_tag)
    dr.text((570, 270), "HUB NIKEL DUNIA", fill=AMBER, font=f_lbl)
    
    # Papua
    dr.polygon([(660, 250), (790, 240), (800, 360), (690, 380)], fill=(37, 99, 235, 25), outline=BLUE, width=3)
    dr.text((700, 290), "PAPUA", fill=INK, font=f_tag)
    
    # Metric badge
    dr.rounded_rectangle([(40, 520), (440, 600)], radius=12, fill=(15, 23, 42, 6), outline=(15, 23, 42, 25), width=1)
    dr.text((56, 532), "T-MINUS BONUS DEMOGRAFI:", fill=INK_MUTED, font=f_lbl)
    dr.text((56, 558), "12 TAHUN (PUNCAK 2030-2035)", fill=RED, font=f_tag)
    
    im.save(os.path.join(OUT_DIR, "indonesia_map_dossier.png"))
    print("Generated indonesia_map_dossier.png")

# 2. Nickel & Battery Cell Specimen Card
def create_nickel_asset():
    W, H = 840, 640
    im, dr = draw_dossier_card(W, H, "STRATEGIC MINERAL // CLASS 1 NICKEL & LFP", "COMMODITY ARCHIVE #02", "52% SUPPLY", AMBER)
    
    f_stat = get_font(64, bold=True)
    f_tag = get_font(24, bold=True)
    f_lbl = get_font(18, bold=False)
    
    # Circular progress chart
    cx, cy, r = 240, 340, 140
    dr.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(245, 158, 11, 20), outline=(245, 158, 11, 60), width=16)
    # Highlight 52% arc
    dr.arc([(cx - r, cy - r), (cx + r, cy + r)], start=-90, end=97, fill=AMBER, width=18)
    dr.text((cx - 70, cy - 45), "52%", fill=INK, font=f_stat)
    dr.text((cx - 85, cy + 25), "PASOKAN DUNIA", fill=INK_MUTED, font=f_lbl)
    
    # Specimen Specs Box
    dr.rounded_rectangle([(440, 180), (800, 580)], radius=16, fill=(15, 23, 42, 6), outline=(15, 23, 42, 20), width=1)
    dr.text((465, 210), "INDEX HILIRISASI NASIONAL", fill=INK, font=f_tag)
    
    rows = [
        ("CADANGAN TERVERIFIKASI:", "5.3 Miliar Ton"),
        ("PROVINSI UTAMA:", "Sulteng, Sultra, Malut"),
        ("TARGET EKOSISTEM:", "Baterai EV & ESS"),
        ("REALISASI INVESTASI:", "Rp 540+ Triliun"),
        ("STATUS GEOPOLITIK:", "Critical Minerals Lead")
    ]
    y = 260
    for label, val in rows:
        dr.text((465, y), label, fill=INK_MUTED, font=f_lbl)
        dr.text((465, y + 24), val, fill=BLUE if "Miliar" in val else (RED if "Critical" in val else INK), font=f_tag)
        y += 60
        
    im.save(os.path.join(OUT_DIR, "nickel_cathode_battery.png"))
    print("Generated nickel_cathode_battery.png")

# 3. Middle Class Economic Trend Card
def create_middle_class_asset():
    W, H = 840, 640
    im, dr = draw_dossier_card(W, H, "ECONOMIC DISPLACEMENT // BPS STATISTIK", "SOCIO-ECONOMIC #03", "ALARM DATA", RED)
    
    f_stat = get_font(60, bold=True)
    f_tag = get_font(22, bold=True)
    f_lbl = get_font(18, bold=False)
    
    # Downward curve chart
    pts = [(100, 240), (220, 260), (360, 290), (520, 360), (680, 460)]
    for i in range(len(pts) - 1):
        dr.line([pts[i], pts[i+1]], fill=RED, width=6)
        dr.ellipse([(pts[i][0] - 8, pts[i][1] - 8), (pts[i][0] + 8, pts[i][1] + 8)], fill=RED, outline=WHITE, width=2)
    dr.ellipse([(pts[-1][0] - 12, pts[-1][1] - 12), (pts[-1][0] + 12, pts[-1][1] + 12)], fill=RED, outline=WHITE, width=3)
    
    # Callout drop indicator
    dr.text((100, 200), "57.3 Juta (2019)", fill=INK_MUTED, font=f_lbl)
    dr.text((540, 480), "47.9 Juta (2024)", fill=RED, font=f_tag)
    
    # Big stat callout card
    dr.rounded_rectangle([(60, 520), (780, 600)], radius=14, fill=(225, 29, 72, 15), outline=RED, width=2)
    dr.text((85, 532), "PENURUNAN KELAS MENENGAH (5 TAHUN):", fill=INK_MUTED, font=f_lbl)
    dr.text((85, 558), "-9.48 JUTA ORANG BERGESER KE MENUJU KELAS MENENGAH", fill=RED, font=f_tag)
    
    im.save(os.path.join(OUT_DIR, "middle_class_chart.png"))
    print("Generated middle_class_chart.png")

# 4. Digital Economy & Tech Grid Card
def create_digital_asset():
    W, H = 840, 640
    im, dr = draw_dossier_card(W, H, "DIGITAL ADOPTION & AI INFRASTRUCTURE", "TECH ECOSYSTEM #04", "RP 1400 T", BLUE)
    
    f_stat = get_font(60, bold=True)
    f_tag = get_font(22, bold=True)
    f_lbl = get_font(18, bold=False)
    
    # Grid of tech metrics
    boxes = [
        ("PENETRASI INTERNET", "79.5%", "221 Juta Pengguna Aktif", BLUE),
        ("GMV DIGITAL 2026", "Rp 1.400 T", "Terbesar di Asia Tenggara", EMERALD),
        ("ADIPSI GENERATIF AI", "TOP 3 ASEAN", "Efisiensi UMKM & Korporasi", AMBER),
        ("FINTECH TRANSAKSI", "3.2 Miliar/Bln", "QRIS & Digital Banking", INK)
    ]
    
    coords = [(60, 160), (440, 160), (60, 360), (440, 360)]
    for (title, val, desc, col), (bx, by) in zip(boxes, coords):
        dr.rounded_rectangle([(bx, by), (bx + 340, by + 170)], radius=16, fill=(15, 23, 42, 6), outline=(15, 23, 42, 20), width=1)
        dr.text((bx + 24, by + 20), title, fill=INK_MUTED, font=f_lbl)
        dr.text((bx + 24, by + 48), val, fill=col, font=f_stat)
        dr.text((bx + 24, by + 125), desc, fill=INK, font=f_lbl)
        
    im.save(os.path.join(OUT_DIR, "digital_economy_chip.png"))
    print("Generated digital_economy_chip.png")

# 5. Middle Income Trap Curve
def create_trap_asset():
    W, H = 840, 640
    im, dr = draw_dossier_card(W, H, "MIDDLE INCOME TRAP BENCHMARK", "GLOBAL COMPARISON #05", "15% LOLOS", RED)
    
    f_tag = get_font(22, bold=True)
    f_lbl = get_font(18, bold=False)
    
    # Threshold threshold line
    dr.line([(80, 240), (760, 240)], fill=(225, 29, 72, 120), width=3)
    dr.text((80, 210), "STANDAR NEGARA MAJU: USD $13,845 / KAPITA", fill=RED, font=f_lbl)
    
    # Korea curve (success)
    korea_pts = [(100, 480), (250, 400), (420, 260), (600, 160), (740, 140)]
    dr.line(korea_pts, fill=EMERALD, width=4)
    dr.text((750, 130), "Korea (Lolos)", fill=EMERALD, font=f_lbl)
    
    # Latin America (trapped)
    latam_pts = [(100, 420), (300, 360), (500, 340), (740, 350)]
    dr.line(latam_pts, fill=INK_MUTED, width=3)
    dr.text((750, 340), "Trap", fill=INK_MUTED, font=f_lbl)
    
    # Indonesia trajectory
    indo_pts = [(100, 520), (320, 490), (500, 440), (640, 400)]
    dr.line(indo_pts, fill=BLUE, width=5)
    for px, py in indo_pts:
        dr.ellipse([(px - 6, py - 6), (px + 6, py + 6)], fill=BLUE, outline=WHITE, width=2)
    dr.text((655, 390), "Indonesia ($4,920)", fill=BLUE, font=f_tag)
    
    # Ratio callout box
    dr.rounded_rectangle([(60, 520), (780, 600)], radius=14, fill=(15, 23, 42, 6), outline=(15, 23, 42, 20), width=1)
    dr.text((85, 535), "RASIO KELOLOSAN GLOBAL: HANYA 15% DARI 101 NEGARA BERKEMBANG", fill=INK_MUTED, font=f_lbl)
    dr.text((85, 560), "SYARAT UTAMA: PRODUKTIVITAS RISET + MANUFAKTUR PRESISI TINGGI", fill=RED, font=f_tag)
    
    im.save(os.path.join(OUT_DIR, "middle_income_trap.png"))
    print("Generated middle_income_trap.png")

# 6. Blueprint Indonesia 2045
def create_blueprint_asset():
    W, H = 840, 640
    im, dr = draw_dossier_card(W, H, "INDONESIA EMAS 2045 ARCHITECTURAL BLUEPRINT", "ACTION ROADMAP #06", "STRATEGI 2045", EMERALD)
    
    f_tag = get_font(24, bold=True)
    f_lbl = get_font(18, bold=False)
    
    pillars = [
        ("01", "MANUFAKTUR BERBASIS RISET", "Bukan sekadar ekspor tanah dan mineral mentah."),
        ("02", "REFORMASI PENDIDIKAN & SKILL", "Fokus STEM, AI terapan, dan vokasi berstandar global."),
        ("03", "INTEGRITAS DAN EFISIENSI HUKUM", "Hapus kebocoran birokrasi & jamin iklim investasi sehat.")
    ]
    
    y = 170
    for num, head, desc in pillars:
        dr.rounded_rectangle([(60, y), (780, y + 120)], radius=16, fill=(16, 185, 129, 12), outline=EMERALD, width=2)
        dr.text((90, y + 25), num, fill=EMERALD, font=get_font(40, bold=True))
        dr.text((180, y + 24), head, fill=INK, font=f_tag)
        dr.text((180, y + 64), desc, fill=INK_MUTED, font=f_lbl)
        y += 140
        
    im.save(os.path.join(OUT_DIR, "indonesia_2045_blueprint.png"))
    print("Generated indonesia_2045_blueprint.png")

# 7. Official Seal Badge
def create_seal_asset():
    S = 400
    im = Image.new("RGBA", (S, S), (255, 255, 255, 0))
    dr = ImageDraw.Draw(im)
    
    dr.ellipse([(20, 20), (S - 20, S - 20)], fill=(255, 255, 255, 240), outline=RED, width=8)
    dr.ellipse([(40, 40), (S - 40, S - 40)], outline=RED, width=2)
    
    f_seal = get_font(28, bold=True)
    f_seal_sm = get_font(20, bold=True)
    dr.text((105, 120), "OFFICIAL DOSSIER", fill=RED, font=f_seal_sm)
    dr.text((95, 160), "INDONESIA", fill=RED, font=f_seal)
    dr.text((130, 210), "2026-2045", fill=RED, font=f_seal_sm)
    dr.text((115, 260), "CRITICAL DECISION", fill=INK_MUTED, font=f_seal_sm)
    
    im.save(os.path.join(OUT_DIR, "archive_seal_ri.png"))
    print("Generated archive_seal_ri.png")

if __name__ == "__main__":
    create_map_asset()
    create_nickel_asset()
    create_middle_class_asset()
    create_digital_asset()
    create_trap_asset()
    create_blueprint_asset()
    create_seal_asset()
