# folha de contato com tempo: python sheet.py video.mp4 out.jpg [fps] [de] [ate] [larg] [cols]
import sys, subprocess, tempfile, glob, os
from PIL import Image, ImageDraw, ImageFont
v, out = sys.argv[1], sys.argv[2]
fps = float(sys.argv[3]) if len(sys.argv) > 3 else 4
de = float(sys.argv[4]) if len(sys.argv) > 4 else 0
ate = float(sys.argv[5]) if len(sys.argv) > 5 else 9999
w = int(sys.argv[6]) if len(sys.argv) > 6 else 180
cols = int(sys.argv[7]) if len(sys.argv) > 7 else 8
d = tempfile.mkdtemp()
subprocess.run(["ffmpeg", "-v", "error", "-ss", str(de), "-i", v, "-t", str(ate - de), "-vf", f"fps={fps}", d + "/f_%04d.png"], check=True)
fs = sorted(glob.glob(d + "/f_*.png"))
ims = [Image.open(f) for f in fs]
h = int(ims[0].height * w / ims[0].width)
rows = (len(ims) + cols - 1) // cols
S = Image.new("RGB", (cols * w, rows * h), "black"); dr = ImageDraw.Draw(S)
F = ImageFont.truetype("arial.ttf", 16)
for i, im in enumerate(ims):
    x, y = (i % cols) * w, (i // cols) * h
    S.paste(im.convert("RGB").resize((w, h)), (x, y))
    t = de + (i + 0.5) / fps if fps != 0 else 0
    dr.rectangle([x, y, x + 52, y + 19], fill="black"); dr.text((x + 3, y + 1), f"{de + i / fps:.2f}", fill="yellow", font=F)
S.save(out, quality=85)
print(out, len(ims))
