# -*- coding: utf-8 -*-
"""Título do gancho (0-3 s) no topo da janela do post: "🔴 LO HUMILLARON EN PLENA CALLE… / AL DÍA SIGUIENTE PASÓ ESTO".
Emoji desenhado (círculo vermelho com brilho) porque a Poppins não tem 🔴. Saída: graficos/titulo_A.png (720x1280 RGBA)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = Path(__file__).resolve().parent; G = AQ.parents[2] / "_trabalho" / "graficos"
W, H, Y0 = 720, 1280, 300          # janela do post começa em y=297


def main():
    f1 = ImageFont.truetype(str(G / "Poppins-ExtraBold.ttf"), 33)
    L1, L2 = "LO HUMILLARON EN PLENA CALLE…", "AL DÍA SIGUIENTE PASÓ ESTO"
    d0 = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    w1 = d0.textlength(L1, font=f1); w2 = d0.textlength(L2, font=f1); R = 15; gap = 12
    lw1 = 2 * R + gap + w1; bw = max(lw1, w2) + 44; lh = 44; bh = 2 * lh + 22
    x0 = (W - bw) / 2; im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([x0 + 3, Y0 + 5, x0 + bw + 3, Y0 + bh + 5], 16, fill=(0, 0, 0, 120))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x0, Y0, x0 + bw, Y0 + bh], 16, fill=(10, 10, 10, 238), outline=(230, 30, 30, 255), width=3)
    y1 = Y0 + 11; y2 = y1 + lh
    xa = (W - lw1) / 2; cy = y1 + lh / 2 + 1
    d.ellipse([xa, cy - R, xa + 2 * R, cy + R], fill=(221, 46, 68, 255))                                # 🔴
    d.ellipse([xa + 7, cy - R + 5, xa + 15, cy - R + 11], fill=(255, 150, 160, 200))                   # brilho
    d.text((xa + 2 * R + gap, y1 + lh / 2), L1, font=f1, fill=(255, 255, 255, 255), anchor="lm")
    d.text((W / 2, y2 + lh / 2), L2, font=f1, fill=(255, 221, 0, 255), anchor="mm")
    im.save(AQ / "graficos" / "titulo_A.png"); print("titulo_A.png", int(bw), int(bh), "y", Y0, Y0 + bh)


if __name__ == "__main__":
    main()
