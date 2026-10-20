# -*- coding: utf-8 -*-
"""Desenho de caixas de texto no estilo do V12 (título branco topo / legenda verde) com Poppins."""
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
FONTS = r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts"
def font(nome, px): return ImageFont.truetype(f"{FONTS}\{nome}", px)

def px_para_cap(nome, cap):
    """tamanho de fonte cuja altura de maiúscula 'H' = cap px"""
    for s in range(10, 120):
        b = font(nome, s).getbbox("H")
        if b[3] - b[1] >= cap: return s
    return 120

def largura(txt, f, track):
    return sum(f.getlength(c) for c in txt) + track * (len(txt) - 1)

def desenha_texto(dr, txt, f, cx, ytop_cap, cor, track=0.0):
    """centraliza em cx; ytop_cap = y do topo das maiúsculas"""
    w = largura(txt, f, track); x = cx - w / 2
    off = f.getbbox("H")[1]
    for c in txt:
        dr.text((x, ytop_cap - off), c, font=f, fill=cor)
        x += f.getlength(c) + track

def track_para(txt, f, alvo):
    return (alvo - largura(txt, f, 0)) / max(1, len(txt) - 1)

def mascara_arred(h, w, box, r):
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle(box, r, fill=255)
    return np.asarray(m) > 127

def cola_caixa_branca(frame_bgr, box, r, linhas):
    """linhas: [(texto, cap_px, ytop_cap, alvo_largura|None)]"""
    h, w = frame_bgr.shape[:2]
    im = Image.fromarray(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle(box, r, fill=(255, 255, 255))
    cx = (box[0] + box[2]) / 2
    for txt, cap, yt, alvo in linhas:
        f = font("Poppins-Bold.ttf", px_para_cap("Poppins-Bold.ttf", cap))
        tr = track_para(txt, f, alvo) if alvo else 1.0
        desenha_texto(dr, txt, f, cx, yt, (3, 3, 3), tr)
    return cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)

VERDE = (64, 129, 62)  # RGB

def cola_caixa_verde(frame_bgr, linhas, cy, fpx, min_box=None, pad_x=34, alt=125, r=18):
    """linhas: textos; fpx = tamanho Poppins SemiBold; caixa centralizada em x=360, centro y=cy"""
    h, w = frame_bgr.shape[:2]
    f = font("Poppins-SemiBold.ttf", fpx)
    larg = max(f.getlength(t) for t in linhas)
    x0, x1 = 360 - larg / 2 - pad_x, 360 + larg / 2 + pad_x
    y0, y1 = cy - alt / 2, cy + alt / 2
    if min_box:
        x0, y0 = min(x0, min_box[0]), min(y0, min_box[1]); x1, y1 = max(x1, min_box[2]), max(y1, min_box[3])
    x0, x1 = max(4, x0), min(w - 4, x1)
    im = Image.fromarray(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle((x0, y0, x1, y1), r, fill=VERDE)
    asc = f.getbbox("H")
    cap = asc[3] - asc[1]
    passo = 41  # distância entre linhas (topo das maiúsculas)
    ytop = cy - (passo * (len(linhas) - 1) + cap) / 2
    for k, t in enumerate(linhas):
        dr.text((360 - f.getlength(t) / 2, ytop + k * passo - asc[1]), t, font=f, fill=(255, 255, 255))
    return cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)

def bbox_verde(fo):
    b = fo[880:1120].astype(int); B, G, R = b[..., 0], b[..., 1], b[..., 2]
    m = (G - R > 35) & (G - B > 35) & (G < 175) & (R < 110)
    rows = np.where(m.sum(1) > 200)[0]
    if not len(rows): return None
    cols = np.where(m[rows[0]:rows[-1] + 1].sum(0) > 20)[0]
    return (int(cols[0]), int(rows[0] + 880), int(cols[-1]), int(rows[-1] + 880))

def copia_arred(dst, src, box, r):
    h, w = dst.shape[:2]
    m = mascara_arred(h, w, box, r)
    dst[m] = src[m]
    return dst
