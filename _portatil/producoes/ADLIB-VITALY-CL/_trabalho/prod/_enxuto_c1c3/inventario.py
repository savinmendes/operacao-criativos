# -*- coding: utf-8 -*-
"""Inventário visual dos takes Lymphoria: folha com o quadro do meio de cada take + duração."""
import subprocess, json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

A = Path(r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria\_trabalho")
U = Path(r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\producao\_trabalho\ugc\prod")
AQ = Path(__file__).parent
takes = sorted(U.glob("*.mp4")) + sorted(A.glob("ad*/flora*/t*_edit.mp4"))
out = []
def dur(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=width,height", "-of", "json", str(f)], capture_output=True, text=True)
    j = json.loads(r.stdout); s = [x for x in j["streams"] if "width" in x][0]
    return float(j["format"]["duration"]), s["width"], s["height"]
tmp = AQ / "_inv"; tmp.mkdir(exist_ok=True)
thumbs = []
for i, t in enumerate(takes):
    d, w, h = dur(t)
    p = tmp / f"{i:03d}.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{d/2:.2f}", "-i", str(t), "-frames:v", "1", "-vf", "scale=180:320:force_original_aspect_ratio=decrease,pad=180:320:(ow-iw)/2:(oh-ih)/2", str(p)])
    out.append({"i": i, "f": str(t), "dur": round(d, 2), "res": f"{w}x{h}"})
    thumbs.append(p)
json.dump(out, open(AQ / "inventario.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
cols = 10; rows = (len(thumbs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 180, rows * 340), "white"); dr = ImageDraw.Draw(sheet)
for k, p in enumerate(thumbs):
    x, y = (k % cols) * 180, (k // cols) * 340
    sheet.paste(Image.open(p), (x, y + 20))
    dr.text((x + 3, y + 3), f"{k} {out[k]['dur']}s", fill="red")
sheet.save(AQ / "inventario.jpg", quality=80)
for o in out: print(o["i"], o["dur"], o["res"], Path(o["f"]).parent.parent.name + "/" + Path(o["f"]).parent.name + "/" + Path(o["f"]).name)
