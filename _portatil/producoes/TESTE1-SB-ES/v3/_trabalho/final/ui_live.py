# -*- coding: utf-8 -*-
"""Moldura EN VIVO completa (os takes novos do padre vêm sem UI): avatar com o rosto do padre novo, nome, EN VIVO,
contador 286, X, caixa "Comentarios desactivados" e ícones -> graficos/live_v2.png (720x1280 RGBA). Mesmas posições da v1.
Uso: python ui_live.py [take_do_padre.mp4]"""
import subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = Path(__file__).resolve().parent; GV = AQ / "graficos"; GV.mkdir(exist_ok=True)
WF = Path(r"C:\Windows\Fonts"); W, H = 720, 1280
def SG(n, t): return ImageFont.truetype(str(WF / n), t)


def avatar(take, t=1.0, cx=353, cy=470, lado=300, d=66):
    b = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(take), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True).stdout
    f = Image.frombytes("RGB", (W, H), b).crop((cx - lado // 2, cy - lado // 2, cx + lado // 2, cy + lado // 2)).resize((d * 4, d * 4), Image.LANCZOS)
    m = Image.new("L", (d * 4, d * 4), 0); ImageDraw.Draw(m).ellipse([0, 0, d * 4 - 1, d * 4 - 1], fill=255)
    a = Image.new("RGBA", (d * 4, d * 4), (0, 0, 0, 0)); a.paste(f, (0, 0), m)
    a = a.resize((d, d), Image.LANCZOS); o = Image.new("RGBA", (d + 6, d + 6), (0, 0, 0, 0))
    ImageDraw.Draw(o).ellipse([0, 0, d + 5, d + 5], fill=(245, 245, 245, 255)); o.alpha_composite(a, (3, 3)); return o


def gerar(take):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # sombreado suave em cima e embaixo (legibilidade, como na live real)
    g = np.zeros((H, W), np.float32); g[:170] = np.linspace(0.42, 0, 170)[:, None]; g[1090:] = np.linspace(0, 0.45, 190)[:, None]
    sh = Image.fromarray((g * 255).astype(np.uint8), "L"); som = Image.new("RGBA", (W, H), (0, 0, 0, 255)); som.putalpha(sh); im.alpha_composite(som)
    av = avatar(take); im.alpha_composite(av, (70 - av.size[0] // 2, 86 - av.size[1] // 2))
    d = ImageDraw.Draw(im)
    nome = "P. Andrés Molina"; fn = SG("seguisb.ttf", 29)
    s = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(s).text((126, 97), nome, font=fn, fill=(0, 0, 0, 120), anchor="ls")
    im.alpha_composite(s.filter(ImageFilter.GaussianBlur(1.5))); d = ImageDraw.Draw(im)
    d.text((126, 97), nome, font=fn, fill=(250, 250, 250, 250), anchor="ls")
    xe = 126 + d.textlength(nome, font=fn) + 9
    d.line([(xe, 81), (xe + 7, 88), (xe + 14, 81)], fill=(245, 245, 245, 235), width=2)
    d.rounded_rectangle([400, 60, 517, 111], radius=7, fill=(236, 45, 118, 255))
    d.text((458.5, 86), "EN VIVO", font=SG("seguisb.ttf", 23), fill=(255, 255, 255, 255), anchor="mm")
    d.rounded_rectangle([531, 61, 629, 111], radius=7, fill=(48, 48, 48, 165))
    # olho
    d.ellipse([546, 78, 572, 94], outline=(240, 240, 240, 255), width=2); d.ellipse([554, 81, 564, 91], fill=(240, 240, 240, 255))
    d.text((578, 86), "286", font=SG("seguisb.ttf", 23), fill=(240, 240, 240, 255), anchor="lm")
    d.line([(655, 72), (683, 100)], fill=(250, 250, 250, 250), width=3); d.line([(683, 72), (655, 100)], fill=(250, 250, 250, 250), width=3)
    # rodapé
    d.rounded_rectangle([38, 1153, 450, 1230], radius=39, outline=(235, 235, 235, 200), width=2)
    d.text((63, 1200), "Comentarios desactivados", font=SG("segoeui.ttf", 19), fill=(235, 235, 235, 215), anchor="ls")
    c = (245, 245, 245, 245)
    d.rounded_rectangle([483, 1178, 515, 1214], radius=7, outline=c, width=3); d.rounded_rectangle([515, 1186, 523, 1206], radius=3, outline=c, width=2)
    d.text((499, 1197), "?", font=SG("seguisb.ttf", 24), fill=c, anchor="mm")
    d.line([(564, 1182), (602, 1180), (580, 1214), (577, 1196), (564, 1182)], fill=c, width=3, joint="curve"); d.line([(577, 1196), (602, 1180)], fill=c, width=2)
    hx, hy = 656, 1196
    pts = [(hx + 16 * np.sin(t) ** 3 * 1.1, hy - (13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)) * 1.1 - 2) for t in np.linspace(0, 2 * np.pi, 80)]
    d.line(pts + [pts[0]], fill=c, width=3, joint="curve")
    out = GV / "live_v2.png"; im.save(out); return out


if __name__ == "__main__":
    tk = Path(sys.argv[1]) if len(sys.argv) > 1 else AQ.parent / "padre" / "take_P1.mp4"
    o = gerar(tk); print(o)
    b = subprocess.run(["ffmpeg", "-v", "error", "-ss", "2", "-i", str(tk), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    f = Image.frombytes("RGB", (W, H), b).convert("RGBA"); f.alpha_composite(Image.open(o)); f.convert("RGB").save(GV / "live_v2_prev.jpg", quality=92)
