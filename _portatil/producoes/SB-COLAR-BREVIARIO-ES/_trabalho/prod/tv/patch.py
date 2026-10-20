import cv2, numpy as np, warnings; warnings.filterwarnings("ignore")
from PIL import Image, ImageDraw, ImageFont
from simple_lama_inpainting import SimpleLama
import sys; sys.path.insert(0, ".")
from comum3 import quadros
f = next(quadros("base_sem_legenda.mp4", 670, 1, 1080, 1920))
m = np.zeros(f.shape[:2], np.uint8)
m[22:102, 20:1060] = 1; m[778:842, 95:915] = 1; m[845:1052, 75:995] = 1
lama = SimpleLama()
r = lama(Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)), Image.fromarray(m * 255))
im = Image.fromarray(np.array(r)[:1920, :1080]); d = ImageDraw.Draw(im)
W = r"C:\Windows\Fonts"
def centro(txt, fonte, px, cy, cor, contorno=0, maxw=1000):
    while True:
        F = ImageFont.truetype(fonte, px); b = d.textbbox((0, 0), txt, font=F, stroke_width=contorno)
        if b[2] - b[0] <= maxw: break
        px -= 1
    x = (1080 - (b[2] - b[0])) / 2 - b[0]; y = cy - (b[3] + b[1]) / 2
    d.text((x, y), txt, font=F, fill=cor, stroke_width=contorno, stroke_fill=(0, 0, 0))
centro("97 mil personas salen de sus deudas en 24 h", W + r"\arialbd.ttf", 56, 62, (255, 255, 255), maxw=1010)
centro("Oración que está haciendo milagros en el mundo", r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts\Poppins-SemiBold.ttf", 40, 810, (40, 40, 40), maxw=800)
for txt, cy in [("Personas están recibiendo", 905), ("milagros de la oración de", 960), ("San Benito.", 1015)]:
    centro(txt, W + r"\ariblk.ttf", 58, cy, (255, 230, 0), contorno=4, maxw=880)
out = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
cv2.imwrite("tv/es670.png", out); np.save("tv/mask670.npy", m)
cv2.imwrite("tv/es670_s.jpg", cv2.resize(out[0:1100], (540, 550)))
