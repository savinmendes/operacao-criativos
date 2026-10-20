# uso: _banda.py video saida ini fim passo  -> faixas y 0.45-0.80 empilhadas em colunas
import sys, cv2
from PIL import Image, ImageDraw, ImageFont
v = cv2.VideoCapture(sys.argv[1]); out = sys.argv[2]; ini, fim, p = map(float, sys.argv[3:6])
f = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 22); ims = []; t = ini
while t < fim:
    v.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, fr = v.read()
    im = Image.fromarray(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)).crop((0, 576, 720, 1024)).resize((360, 224))
    ImageDraw.Draw(im).text((4, 4), f"{t:.1f}", font=f, fill="yellow", stroke_width=2, stroke_fill="black"); ims.append(im); t += p
cols = 6; rows = (len(ims) + cols - 1) // cols
S = Image.new("RGB", (360 * cols, 224 * rows))
for i, im in enumerate(ims): S.paste(im, ((i % cols) * 360, (i // cols) * 224))
S.save(out, quality=85)
