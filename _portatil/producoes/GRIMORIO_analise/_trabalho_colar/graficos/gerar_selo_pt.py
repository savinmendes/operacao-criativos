# -*- coding: utf-8 -*-
"""Selo "VÍDEO FICTÍCIO" mini (mesmo estilo do SB-REEL-MEDALLA-ES/graficos/gerar_selo_mini.py:
Poppins Bold 18, caixa preta 70%, raio 5, x1=W-20, y0=4 no quadro 1080), desenhado em 1080x1920 e reduzido p/ 720x1280."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
AQUI = Path(__file__).resolve().parent
FON = Path(r"C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES\_trabalho\fonts")
W, H = 1080, 1920
im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
f = ImageFont.truetype(str(FON / "Poppins-Bold.ttf"), 18); t = "VÍDEO FICTÍCIO"
b = d.textbbox((0, 0), t, font=f); w, h = b[2] - b[0], b[3] - b[1]
px, py = 11, 6
x1 = W - 20; x0 = x1 - w - 2 * px
y0 = 4; y1 = y0 + h + 2 * py
d.rounded_rectangle([x0, y0, x1, y1], radius=5, fill=(0, 0, 0, 179))
d.text((x0 + px - b[0], y0 + py - b[1]), t, font=f, fill=(255, 255, 255, 255))
im.resize((720, 1280), Image.LANCZOS).save(AQUI / "selo_ficticio_mini_pt.png")
print("caixa 1080:", (x0, y0, x1, y1), "-> 720:", tuple(round(v * 2 / 3, 1) for v in (x0, y0, x1, y1)))
