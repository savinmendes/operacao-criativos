# uso: _folha.py video saida.jpg passo [ini] [fim]
import sys, cv2
from PIL import Image, ImageDraw, ImageFont
v, out, passo = sys.argv[1], sys.argv[2], float(sys.argv[3])
ini = float(sys.argv[4]) if len(sys.argv) > 4 else 0
cap = cv2.VideoCapture(v); fps = cap.get(5); n = cap.get(7); dur = n / fps
fim = float(sys.argv[5]) if len(sys.argv) > 5 else dur
ims, t = [], ini
f = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 20)
while t < fim - 0.01:
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, fr = cap.read()
    if not ok: break
    im = Image.fromarray(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)); im.thumbnail((180, 320))
    ImageDraw.Draw(im).text((4, 4), f"{t:.1f}", font=f, fill="yellow", stroke_width=2, stroke_fill="black")
    ims.append(im); t += passo
w, h = ims[0].size; cols = min(10, len(ims)); rows = (len(ims) + cols - 1) // cols
S = Image.new("RGB", (w * cols, h * rows))
for k, im in enumerate(ims): S.paste(im, ((k % cols) * w, (k // cols) * h))
S.save(out, quality=85); print(out, len(ims), round(dur, 2))
