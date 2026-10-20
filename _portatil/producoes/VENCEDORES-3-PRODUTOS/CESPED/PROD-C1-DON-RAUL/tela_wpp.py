# -*- coding: utf-8 -*-
"""Tela de grupo estilo WhatsApp (por código, sem logo). Saída: PNG 720x1280 com o celular sobre o fundo dado."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F = r"C:\Windows\Fonts"
f_reg = lambda s: ImageFont.truetype(F + r"\segoeui.ttf", s)
f_bold = lambda s: ImageFont.truetype(F + r"\segoeuib.ttf", s)
EMJ = ImageFont.truetype(F + r"\seguiemj.ttf", 109)  # bitmap emoji: só tamanho 109

def is_emoji(ch): return ord(ch) > 0x2600

def run_width(txt, font, size):
    w = 0
    for ch in txt:
        w += size * 1.15 if is_emoji(ch) else font.getlength(ch)
    return w

def draw_text(img, d, xy, txt, font, size, fill):
    x, y = xy
    for ch in txt:
        if is_emoji(ch):
            e = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
            ImageDraw.Draw(e).text((0, 0), ch, font=EMJ, embedded_color=True)
            e = e.crop(e.getbbox()).resize((int(size * 1.05), int(size * 1.05)), Image.LANCZOS)
            img.alpha_composite(e, (int(x), int(y + size * 0.18)))
            x += size * 1.15
        else:
            d.text((x, y), ch, font=font, fill=fill); x += font.getlength(ch)

def wrap(txt, font, size, maxw):
    lines, cur = [], ""
    for w in txt.split(" "):
        t = (cur + " " + w).strip()
        if run_width(t, font, size) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

def tela(fundo, msgs, out, hora_topo="18:42"):
    W, H = 720, 1280
    bg = Image.open(fundo).convert("RGB").resize((W, H)).filter(ImageFilter.GaussianBlur(14))
    bg = Image.blend(bg, Image.new("RGB", (W, H), (0, 0, 0)), 0.45).convert("RGBA")
    # celular
    px, py, pw, ph = 70, 170, 580, 1030
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((px - 10, py - 10, px + pw + 10, py + ph + 10), 56, fill=(15, 15, 15, 255))
    bg.alpha_composite(sh)
    scr = Image.new("RGBA", (pw, ph), (236, 229, 221, 255)); d = ImageDraw.Draw(scr)
    # header
    d.rectangle((0, 0, pw, 118), fill=(0, 128, 105))
    d.text((22, 50), "←", font=f_bold(30), fill="white")
    d.ellipse((62, 46, 118, 102), fill=(190, 205, 200))
    d.text((80, 52), "V", font=f_bold(32), fill=(0, 128, 105))
    d.text((132, 44), "Vecinos Pasaje Los Aromos", font=f_bold(25), fill="white")
    d.text((132, 78), "Sra. Marta, Don Pepe, Rosa, tú…", font=f_reg(19), fill=(220, 240, 235))
    d.text((pw - 120, 14), hora_topo, font=f_bold(18), fill="white")
    # mensagens
    cores = {"Sra. Marta": (214, 62, 120), "Don Pepe": (40, 120, 200)}
    fs = 31; fn = f_reg(fs)
    alturas = [40 if a == "__sep__" else 44 + len(wrap(t, fn, fs, pw - 110)) * 42 + 28 for a, t, _ in msgs]
    y = ph - 100 - sum(h + 18 for h in alturas)
    for k, (autor, txt, hora) in enumerate(msgs):
        bh = alturas[k]
        if autor == "__sep__":
            dd = ImageDraw.Draw(scr); tw = f_bold(20).getlength(txt)
            dd.rounded_rectangle((pw / 2 - tw / 2 - 16, y, pw / 2 + tw / 2 + 16, y + 38), 12, fill=(225, 243, 251))
            dd.text((pw / 2 - tw / 2, y + 6), txt, font=f_bold(20), fill=(80, 90, 95)); y += bh + 18; continue
        ls = wrap(txt, fn, fs, pw - 110)
        bw = max(run_width(l, fn, fs) for l in ls) + 40
        bw = max(bw, f_bold(22).getlength(autor) + 40, 200)
        dd = ImageDraw.Draw(scr)
        dd.rounded_rectangle((16, y, 16 + bw, y + bh), 18, fill="white")
        dd.text((32, y + 10), autor, font=f_bold(22), fill=cores.get(autor, (0, 128, 105)))
        for i, l in enumerate(ls):
            draw_text(scr, dd, (32, y + 42 + i * 42), l, fn, fs, (20, 20, 20))
        dd.text((16 + bw - 62, y + bh - 28), hora, font=f_reg(17), fill=(130, 130, 130))
        y += bh + 18
    # barra de digitação
    d = ImageDraw.Draw(scr)
    d.rounded_rectangle((12, ph - 78, pw - 84, ph - 18), 30, fill="white")
    d.text((40, ph - 64), "Mensaje", font=f_reg(24), fill=(150, 150, 150))
    d.ellipse((pw - 72, ph - 80, pw - 12, ph - 20), fill=(0, 128, 105))
    m = Image.new("L", (pw, ph), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, pw, ph), 46, fill=255)
    bg.paste(scr, (px, py), m)
    bg.convert("RGB").save(out)

if __name__ == "__main__":
    pass
