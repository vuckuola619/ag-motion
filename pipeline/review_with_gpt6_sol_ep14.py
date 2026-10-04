import os
import sys
import json
import base64
import urllib.request
from io import BytesIO
from PIL import Image

ROUTER_URL = "http://127.0.0.1:20128/v1/chat/completions"
API_KEY = "Bearer sk-c4f2444795b190b3-kzvd4h-ea839762"
MODEL = "cx/gpt-6-sol"

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAROUSEL_DIR = os.path.join(PROJECT_ROOT, "assets", "episode14_glymphatic_brain_wash", "carousel_native_text")
OUTPUT_MD = os.path.join(PROJECT_ROOT, "output", "episode14_glymphatic_brain_wash", "designer_review_gpt6_sol.md")

SLIDE_FILES = [
    "slide_1_cover_native_text.png",
    "slide_2_astrocytes_native_text.png",
    "slide_3_alzheimer_purge_native_text.png",
    "slide_4_sleep_debt_native_text.png",
    "slide_5_closing_protocol_native_text.png"
]

def encode_image(img_path, max_dim=1024):
    img = Image.open(img_path).convert("RGB")
    ratio = min(max_dim / img.width, max_dim / img.height)
    if ratio < 1.0:
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)
    
    buffered = BytesIO()
    img.save(buffered, format="JPEG", quality=85)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def main():
    print(f"--- Preparing image review with {MODEL} via 9Router ---")
    
    content_parts = [
        {
            "type": "text",
            "text": (
                "You are an elite Creative Director and Senior Motion & Visual Designer. "
                "Audit these 5 native text carousel slides for Episode 14: 'The Glymphatic Brain Wash' "
                "(The Neuroscience of Deep Sleep & Cerebral Flushing).\n\n"
                "KEY EVALUATION CRITERIA:\n"
                "1. Typography & Spelling: Evaluate the native typography generated directly in GPT Image (clarity, hierarchy, font pairings, spelling accuracy, kerning).\n"
                "2. Composition & Visual Drama: Evaluate the scientific illustrations (bioluminescent brain, astrocyte network, amyloid-beta clearance, sleep architecture).\n"
                "3. Safe Zones & Contrast: Check readability against deep navy backgrounds for mobile (TikTok/Instagram 4:5).\n"
                "4. Narrative Arc & Retention: How compelling is the 5-slide journey from hook to biological protocol?\n\n"
                "Provide a rigorous, high-signal, expert critique and score (out of 10) for each slide and the whole carousel."
            )
        }
    ]

    for i, fname in enumerate(SLIDE_FILES, 1):
        fpath = os.path.join(CAROUSEL_DIR, fname)
        if os.path.exists(fpath):
            print(f"[Encode] Encoding Slide {i}: {fname}...")
            b64 = encode_image(fpath)
            content_parts.append({
                "type": "text",
                "text": f"--- SLIDE {i}: {fname} ---"
            })
            content_parts.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{b64}"
                }
            })

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": content_parts
            }
        ],
        "temperature": 0.4
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": API_KEY,
        "User-Agent": "BangMotion/1.0"
    }

    print(f"[Request] Sending audit payload to {ROUTER_URL} with model {MODEL}...")
    req = urllib.request.Request(ROUTER_URL, data=json.dumps(payload).encode("utf-8"), headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=180) as res:
            res_json = json.loads(res.read().decode("utf-8"))
            review_text = res_json["choices"][0]["message"]["content"]
            with open(OUTPUT_MD, "w", encoding="utf-8") as f:
                f.write(f"# Senior Creative Director Audit (cx/gpt-6-sol)\n")
                f.write(f"**Episode 14**: The Glymphatic Brain Wash\n")
                f.write(f"**Model Reviewer**: `{MODEL}` via 9Router\n\n")
                f.write(review_text)
            print(f"[Saved] Report saved to: {OUTPUT_MD}")
            print("\n" + "="*50)
            print("DESIGNER REVIEW SUMMARY FROM CX/GPT-6-SOL:")
            print("="*50)
            safe_text = review_text[:1200].encode('ascii', errors='replace').decode('ascii')
            print(safe_text + "...\n[Full review written to file]")

    except Exception as e:
        print(f"[Error] Review request failed: {e}")

if __name__ == "__main__":
    main()
