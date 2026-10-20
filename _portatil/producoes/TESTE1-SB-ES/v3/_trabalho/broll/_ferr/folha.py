# folha.py video t0 t1 passo saida [cols]  -> folha de contato com tempo
import sys, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
v, t0, t1, st, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
cols = int(sys.argv[6]) if len(sys.argv) > 6 else 12
W, H = 160, 284
f = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 18)
ts = list(np.arange(t0, t1, st)); ims = []
for t in ts:
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", v, "-frames:v", "1", "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    a = np.frombuffer(r.stdout, np.uint8)
    im = Image.fromarray(a.reshape(H, W, 3)) if a.size == W*H*3 else Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im); d.rectangle([0, 0, 70, 22], fill=(0, 0, 0)); d.text((3, 2), f"{t:.1f}", font=f, fill=(255, 255, 0)); ims.append(im)
rows = (len(ims) + cols - 1) // cols
S = Image.new("RGB", (cols*W, rows*H), (30, 30, 30))
for i, im in enumerate(ims): S.paste(im, ((i % cols)*W, (i//cols)*H))
S.save(out, quality=85); print(out, len(ims))
