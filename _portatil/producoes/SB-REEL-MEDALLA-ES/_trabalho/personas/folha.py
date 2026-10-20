# folha de contato a cada 0,2 s com rotulo; opcional recorte. uso: python folha.py video saida.jpg [x y w h] [passo] [larg]
import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw
v, out = sys.argv[1], sys.argv[2]
crop = [int(x) for x in sys.argv[3:7]]; passo = float(sys.argv[7]) if len(sys.argv) > 7 else 0.2
w = int(sys.argv[8]) if len(sys.argv) > 8 else (270 if not crop else 300)
p = subprocess.run(["ffprobe","-v","error","-select_streams","v","-show_entries","stream=width,height","-of","csv=p=0",v],capture_output=True,text=True).stdout.split(",")
W, H = int(p[0]), int(p[1])
cr = f"crop={crop[2]}:{crop[3]}:{crop[0]}:{crop[1]}," if crop else ""
cw, ch = (crop[2], crop[3]) if crop else (W, H)
h = int(w * ch / cw) // 2 * 2
raw = subprocess.run(["ffmpeg","-v","error","-i",v,"-vf",f"fps=1/{passo},{cr}scale={w}:{h}","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
cols = 10; rows = (len(fr) + cols - 1) // cols
S = Image.new("RGB", (cols * w, rows * h))
for i, f in enumerate(fr):
    im = Image.fromarray(f); d = ImageDraw.Draw(im); d.rectangle([0,0,52,16], fill="black"); d.text((3,2), f"{i*passo:.1f}s", fill="yellow")
    S.paste(im, ((i % cols) * w, (i // cols) * h))
S.save(out, quality=85); print(out, len(fr))
