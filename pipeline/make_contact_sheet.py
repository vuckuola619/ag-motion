from PIL import Image
import glob
import os

files = sorted(glob.glob('output/indonesia_hari_ini/snap_idn_*.jpg'))
images = [Image.open(f) for f in files]
target_h = 900
resized = [im.resize((int(im.width * target_h / im.height), target_h), Image.Resampling.LANCZOS) for im in images]
total_w = sum(im.width for im in resized)
sheet = Image.new('RGB', (total_w, target_h))
x = 0
for im in resized:
    sheet.paste(im, (x, 0))
    x += im.width

os.makedirs('output/indonesia_hari_ini', exist_ok=True)
sheet.save('output/indonesia_hari_ini/contact_sheet.jpg', quality=90)
brain_path = r'C:\Users\bati-\.gemini\antigravity\brain\6c49e710-6b1f-406b-9eb2-9a374f179691\contact_sheet_indonesia_hari_ini.jpg'
sheet.save(brain_path, quality=90)
print('SUCCESS! Stitched', len(images), 'images into', total_w, 'x', target_h)
