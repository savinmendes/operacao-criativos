# -*- coding: utf-8 -*-
"""Camadas em tela cheia (PNG RGBA WxH) para o prep_A.py: selo COD e tela final de avaliações (cards + faixa vermelha).

  python camadas_A.py selo W H cy largura saida.png
  python camadas_A.py avaliacoes quadro.png cards.json saida.png [debug.png]
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONTS = Path(r"C:/Users/PICHAU/Downloads/Produtividade com ia/kit-edicao-criativos/fonts")
FB, FM, FS = str(FONTS / "Poppins-Bold.ttf"), str(FONTS / "Poppins-Medium.ttf"), str(FONTS / "Poppins-SemiBold.ttf")
EMOJI = "C:/Windows/Fonts/seguiemj.ttf"
OURO = (255, 196, 0, 255)


def selo(W, H, cy, largura, saida):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    txt = "PAGO CONTRA ENTREGA"
    px = 60
    while px > 10:
        f = ImageFont.truetype(FB, px)
        if d.textlength(txt, font=f) <= largura - 36:
            break
        px -= 1
    alt = int(px * 1.75)
    x0 = (W - largura) // 2
    y0 = cy - alt // 2
    d.rounded_rectangle([x0 + 3, y0 + 4, x0 + largura + 3, y0 + alt + 4], radius=alt // 4, fill=(0, 0, 0, 110))
    d.rounded_rectangle([x0, y0, x0 + largura, y0 + alt], radius=alt // 4, fill=(255, 214, 0, 255),
                        outline=(17, 17, 17, 255), width=max(2, px // 14))
    d.text((W / 2, y0 + alt / 2 + 1), txt, font=f, fill=(17, 17, 17, 255), anchor="mm")
    img.save(saida)
    return saida


def estrela(d, cx, cy, r, cor=OURO):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=cor)


def quebra(d, texto, f, maxw):
    linhas, cur = [], ""
    for w in texto.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw or not cur:
            cur = t
        else:
            linhas.append(cur)
            cur = w
    if cur:
        linhas.append(cur)
    return linhas


def card(w, h, titulo, corpo):
    """Card branco w x h: 5 estrelas, título em negrito, texto (ajusta o tamanho para caber)."""
    img = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    d = ImageDraw.Draw(img)
    m = max(6, int(h * 0.06))
    r = h * 0.075
    for k in range(5):
        estrela(d, m + r + k * (2.25 * r), m + r, r)
    y_txt = m + 2 * r + h * 0.04
    for pt in range(int(h * 0.14), 7, -1):
        ft = ImageFont.truetype(FB, pt)
        fc = ImageFont.truetype(FM, max(7, int(pt * 0.74)))
        lt = quebra(d, titulo, ft, w - 2 * m)
        lc = quebra(d, corpo, fc, w - 2 * m)
        alt = len(lt) * pt * 1.18 + len(lc) * fc.size * 1.28 + 2
        if alt <= h - y_txt - m * 0.6:
            break
    y = y_txt
    for l in lt:
        d.text((m, y), l, font=ft, fill=(17, 17, 17, 255))
        y += pt * 1.18
    for l in lc:
        d.text((m, y), l, font=fc, fill=(40, 40, 40, 255))
        y += fc.size * 1.28
    return img


def retangulos(fr):
    """Cards brancos (minAreaRect) e a faixa vermelha (boundingRect) no quadro BGR."""
    hsv = cv2.cvtColor(fr, cv2.COLOR_BGR2HSV)
    branco = ((hsv[..., 1] < 40) & (hsv[..., 2] > 215)).astype(np.uint8) * 255
    branco = cv2.morphologyEx(branco, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    cs, _ = cv2.findContours(branco, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cards = []
    for c in cs:
        a = cv2.contourArea(c)
        if a < fr.shape[0] * fr.shape[1] * 0.012:
            continue
        rect = cv2.minAreaRect(c)
        (cx, cy), (rw, rh), _ = rect
        if a / max(1, rw * rh) < 0.8:
            continue
        pts = cv2.boxPoints(rect)
        lados = [(pts[(k + 1) % 4] - pts[k]) for k in range(4)]
        lmax = max(lados, key=lambda v: np.hypot(*v))
        ang = math.degrees(math.atan2(lmax[1], lmax[0]))
        while ang > 45:
            ang -= 180 if ang > 90 else 90
        while ang < -45:
            ang += 180 if ang < -90 else 90
        cards.append(dict(cx=float(cx), cy=float(cy), w=float(max(rw, rh)), h=float(min(rw, rh)), ang=ang))
    verm = (((hsv[..., 0] < 8) | (hsv[..., 0] > 170)) & (hsv[..., 1] > 140) & (hsv[..., 2] > 90)).astype(np.uint8) * 255
    verm = cv2.morphologyEx(verm, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    cs, _ = cv2.findContours(verm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cs, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)
    cor = tuple(int(v) for v in np.median(fr[y + 5:y + h - 5, x + 5:x + w - 5][verm[y + 5:y + h - 5, x + 5:x + w - 5] > 0], axis=0)[::-1])
    return cards, (x, y, w, h), cor


def avaliacoes(quadro, cfg_json, saida, debug=None):
    cfg = json.load(open(cfg_json, encoding="utf-8"))
    fr = cv2.imread(quadro)
    H, W = fr.shape[:2]
    det, (bx, by, bw, bh), cor = retangulos(fr)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pad = cfg.get("pad", 5)
    usados = []
    for c in cfg["cards"]:
        alvo = min(det, key=lambda r: (r["cx"] - c["perto"][0]) ** 2 + (r["cy"] - c["perto"][1]) ** 2)
        usados.append(alvo)
        im = card(int(alvo["w"] + 2 * pad), int(alvo["h"] + 2 * pad), c["titulo"], c["texto"])
        im = im.rotate(-alvo["ang"], resample=Image.BICUBIC, expand=True)
        img.alpha_composite(im, (int(round(alvo["cx"] - im.width / 2)), int(round(alvo["cy"] - im.height / 2))))
        print(f"card '{c['titulo']}': c=({alvo['cx']:.0f},{alvo['cy']:.0f}) {alvo['w']:.0f}x{alvo['h']:.0f} ang {alvo['ang']:.1f}")
    # faixa vermelha
    p = cfg.get("pad_faixa", 6)
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = bx - p, by - p, bx + bw + p, by + bh + p
    d.rounded_rectangle([x0, y0, x1, y1], radius=int(bh * 0.12), fill=cor + (255,))
    linhas = cfg["faixa"]   # [[texto, px_rel], ...] px_rel = fração da altura da faixa
    ef = ImageFont.truetype(EMOJI, 20)
    alturas = [int(bh * r) for _, r in linhas]
    tot = sum(int(a * 1.18) for a in alturas)
    y = (y0 + y1) / 2 - tot / 2
    for (txt, _), a in zip(linhas, alturas):
        f = ImageFont.truetype(FB, a)
        while d.textlength(txt.replace("★", "  "), font=f) > (x1 - x0) - 30 and a > 8:
            a -= 1
            f = ImageFont.truetype(FB, a)
        larg = sum(a * 1.05 if ch == "★" else d.textlength(ch, font=f) for ch in txt)
        x = (x0 + x1) / 2 - larg / 2
        for ch in txt:
            if ch == "★":
                estrela(d, x + a * 0.5, y + a * 0.62, a * 0.5)
                x += a * 1.05
            else:
                d.text((x, y), ch, font=f, fill=(255, 255, 255, 255))
                x += d.textlength(ch, font=f)
        y += a * 1.18
    print(f"faixa vermelha: {bx},{by} {bw}x{bh} cor {cor}")
    img.save(saida)
    if debug:
        base = Image.fromarray(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)).convert("RGBA")
        base.alpha_composite(img)
        base.convert("RGB").save(debug)
    sobra = [r for r in det if r not in usados]
    if sobra:
        print("aviso: retângulos brancos não usados:", [(round(r["cx"]), round(r["cy"])) for r in sobra])


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "selo":
        selo(int(a[1]), int(a[2]), int(a[3]), int(a[4]), a[5])
    else:
        avaliacoes(a[1], a[2], a[3], a[4] if len(a) > 4 else None)
