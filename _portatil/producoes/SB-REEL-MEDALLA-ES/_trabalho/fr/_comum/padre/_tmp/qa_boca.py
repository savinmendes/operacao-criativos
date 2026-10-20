import sys, json, subprocess, numpy as np
from PIL import Image, ImageDraw
vid, off, dur, saida = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
passo = float(sys.argv[5]) if len(sys.argv) > 5 else 0.2
ws = json.load(open("../palavras.json", encoding="utf-8"))
def falando(t):
    for w in ws:
        if w["ini"] - 0.03 <= t <= w["fim"] + 0.03: return w["w"]
    return None
X0, Y0, CW, CH = 420, 640, 300, 220
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", vid, "-vf", f"fps={1/passo},crop={CW}:{CH}:{X0}:{Y0}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
n = len(raw) // (CW * CH * 3); fr = np.frombuffer(raw, np.uint8)[: n * CW * CH * 3].reshape(n, CH, CW, 3)
cols = 10; s = 0.6; tw, th = int(CW * s), int(CH * s) + 18
img = Image.new("RGB", (cols * tw, ((n + cols - 1) // cols) * th), (20, 20, 20)); d = ImageDraw.Draw(img)
for i in range(n):
    t = i * passo; w = falando(t + off)
    x, y = (i % cols) * tw, (i // cols) * th
    img.paste(Image.fromarray(fr[i]).resize((tw, th - 18)), (x, y + 18))
    d.text((x + 2, y + 2), f"{t+off:.1f} {w or '--PAUSA--'}"[:28], fill=(255, 255, 0) if w is None else (220, 220, 220))
img.save(saida, quality=88); print(n)
