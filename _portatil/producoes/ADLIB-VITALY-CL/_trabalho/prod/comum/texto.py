# -*- coding: utf-8 -*-
"""Render de texto estilo TikTok/caixa: linha com segmentos (texto, negrito?) + emoji monocromático."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, subprocess
F = r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts"
EMO = r"C:\Windows\Fonts\seguiemj.ttf"
def fonte(bold, px):
    return ImageFont.truetype(F + ("/Poppins-Bold.ttf" if bold else "/Poppins-Medium.ttf"), px)
def eh_emoji(ch):
    return ord(ch) > 0x2500
def pedacos(segs):
    out = []
    for txt, b in segs:
        cur = ""
        for ch in txt:
            if eh_emoji(ch) or ch == "\ufe0f":
                if cur: out.append((cur, b, False)); cur = ""
                if ch != "\ufe0f": out.append((ch, b, True))
            else:
                cur += ch
        if cur: out.append((cur, b, False))
    return out
def largura(segs, px):
    w = 0
    for t, b, e in pedacos(segs):
        f = ImageFont.truetype(EMO, int(px * 0.95)) if e else fonte(b, px)
        w += f.getlength(t)
    return w
def desenhar_linha(img, segs, cx, ytop, px, cor=(0, 0, 0, 255), emoji_cor=False):
    """Desenha centrado em cx; ytop = topo da caixa de texto (ascendente)."""
    d = ImageDraw.Draw(img)
    x = cx - largura(segs, px) / 2
    for t, b, e in pedacos(segs):
        if e:
            f = ImageFont.truetype(EMO, int(px * 0.95))
            if emoji_cor:
                d.text((x, ytop + px * 0.12), t, font=f, embedded_color=True)
            else:
                d.text((x, ytop + px * 0.12), t, font=f, fill=cor)
        else:
            f = fonte(b, px)
            d.text((x, ytop), t, font=f, fill=cor)
        x += f.getlength(t)
def px_para_largura(segs, alvo):
    lo, hi = 8, 300
    while hi - lo > 0.5:
        m = (lo + hi) / 2
        if largura(segs, int(m)) > alvo: hi = m
        else: lo = m
    return int(lo)
def tinta_bbox(segs, px):
    im = Image.new("L", (int(largura(segs, px)) + 40, int(px * 2)), 0)
    desenhar_linha(im, segs, im.size[0] / 2, 0, px, cor=255)
    a = np.asarray(im); ys = np.where(a.max(1) > 128)[0]; xs = np.where(a.max(0) > 128)[0]
    return ys.min(), ys.max(), xs.min(), xs.max()
def ler_quadros(src, w=720, h=1280, vf=None, ss=None, t=None):
    c = ["ffmpeg", "-v", "error"]
    if ss is not None: c += ["-ss", str(ss)]
    if t is not None: c += ["-t", str(t)]
    c += ["-i", src]
    if vf: c += ["-vf", vf]
    c += ["-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.run(c, capture_output=True, check=True).stdout
    return np.frombuffer(p, np.uint8).reshape(-1, h, w, 3)
