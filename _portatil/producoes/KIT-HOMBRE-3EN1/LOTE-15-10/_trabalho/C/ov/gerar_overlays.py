# -*- coding: utf-8 -*-
"""Overlays do agente C (720x1280, PIL, sem custo).
banner_topo.png (selo COD, cobre o selo queimado do B-roll), sticker_kit.png (cartao opaco com os 3 frascos,
cobre o adesivo queimado do B-roll), cta_final.png (tela cheia: texto CTA + cartao + setas),
titulos de gancho (tela cheia) e rotulos de segmento (tela cheia, faixa no topo)."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cv2

OUT = Path(__file__).resolve().parent
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts")
N2 = Path(r"C:\Users\PICHAU\Downloads\KIT-HOMBRE-3EN1\flora\image_n2.png")
PB, AN = str(KIT / "Poppins-Bold.ttf"), str(KIT / "Anton-Regular.ttf")
PS = str(KIT / "Poppins-SemiBold.ttf") if (KIT / "Poppins-SemiBold.ttf").exists() else PB
W, H = 720, 1280
NAVY = (14, 38, 77, 255)
BRANCO = (255, 255, 255, 255)
AMA = (255, 214, 0, 255)
VERM = (226, 30, 38, 255)
PRETO = (12, 12, 12, 255)
OURO = (201, 162, 74, 255)
F = lambda p, s: ImageFont.truetype(p, s)


def caminhao(d, x, y, s, cor):
    """icone simples de caminhao (s = altura)"""
    d.rectangle((x, y, x + s * 1.25, y + s * 0.75), fill=cor)
    d.polygon([(x + s * 1.3, y + s * 0.2), (x + s * 1.75, y + s * 0.2), (x + s * 1.95, y + s * 0.5),
               (x + s * 1.95, y + s * 0.75), (x + s * 1.3, y + s * 0.75)], fill=cor)
    for cx in (x + s * 0.35, x + s * 1.6):
        d.ellipse((cx - s * 0.2, y + s * 0.6, cx + s * 0.2, y + s), fill=cor, outline=NAVY, width=3)
    for k in range(3):
        d.line((x - s * (0.9 - 0.15 * k), y + s * (0.15 + 0.22 * k), x - s * 0.15, y + s * (0.15 + 0.22 * k)), fill=cor, width=4)


def banner():
    im = Image.new("RGBA", (520, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((-30, 20, 506, 124), radius=22, fill=NAVY)
    d.text((22, 34), "PAGO CONTRA ENTREGA", font=F(PB, 29), fill=BRANCO)
    d.text((22, 76), "ENVÍO EN 24 HORAS", font=F(PB, 27), fill=AMA)
    caminhao(d, 418, 50, 40, BRANCO)
    im.save(OUT / "banner_topo.png")


def frascos(alt):
    """recorte dos 3 frascos do n2 (fundo branco ligado a borda -> transparente)"""
    a = cv2.imread(str(N2))
    h, w = a.shape[:2]
    clara = (a.min(2) > 235).astype(np.uint8)
    m = np.zeros((h + 2, w + 2), np.uint8)
    fundo = clara.copy()
    for sx, sy in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 5), (w // 2, h - 5)]:
        cv2.floodFill(fundo, m, (sx, sy), 2)
    alfa = np.where(fundo == 2, 0, 255).astype(np.uint8)
    alfa = cv2.GaussianBlur(cv2.erode(alfa, np.ones((3, 3), np.uint8)), (3, 3), 0)
    rgba = np.dstack([a[..., ::-1], alfa])
    ys, xs = np.where(alfa > 10)
    rgba = rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    im = Image.fromarray(rgba, "RGBA")
    r = alt / im.height
    return im.resize((int(im.width * r), alt), Image.LANCZOS)


def sticker():
    cw, ch = 460, 340
    im = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, cw - 1, ch - 1), radius=26, fill=(18, 18, 20, 255), outline=OURO, width=4)
    fr = frascos(240)
    if fr.width > cw - 40:
        fr = fr.resize((cw - 40, int(fr.height * (cw - 40) / fr.width)), Image.LANCZOS)
    im.alpha_composite(fr, ((cw - fr.width) // 2, 18))
    t = "PACK 3 EN 1"
    f = F(AN, 46)
    tw = d.textlength(t, font=f)
    d.text(((cw - tw) / 2, ch - 70), t, font=f, fill=AMA)
    im.save(OUT / "sticker_kit.png")
    return im


def texto_contorno(d, xy, t, f, cor, borda=6, anchor="mm"):
    d.text(xy, t, font=f, fill=cor, stroke_width=borda, stroke_fill=PRETO, anchor=anchor)


def caixa_titulo(linhas, y, fontes, cores, fundo=None, nome=None):
    """linhas centralizadas com contorno; fundo opcional (caixa)"""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cy = y
    for t, f, cor in zip(linhas, fontes, cores):
        bb = d.textbbox((W / 2, cy), t, font=f, anchor="mt", stroke_width=6)
        if fundo:
            d.rounded_rectangle((bb[0] - 18, bb[1] - 10, bb[2] + 18, bb[3] + 12), radius=14, fill=fundo)
        d.text((W / 2, cy), t, font=f, fill=cor, anchor="mt", stroke_width=0 if fundo else 6, stroke_fill=PRETO)
        cy = bb[3] + 18
    im.save(OUT / nome)


def seta(d, cx, y0, y1, larg, cor):
    d.rectangle((cx - larg * 0.18, y0, cx + larg * 0.18, y1 - larg * 0.55), fill=cor)
    d.polygon([(cx - larg / 2, y1 - larg * 0.6), (cx + larg / 2, y1 - larg * 0.6), (cx, y1)], fill=cor)


def cta(stk):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, 600, 660, 820), radius=24, fill=(12, 12, 12, 225))
    d.text((W / 2, 625), "PIDE EL TUYO AHORA", font=F(AN, 66), fill=BRANCO, anchor="mt")
    d.rounded_rectangle((110, 720, 610, 800), radius=18, fill=AMA)
    d.text((W / 2, 760), "PAGAS AL RECIBIR", font=F(PB, 40), fill=PRETO, anchor="mm")
    im.alpha_composite(stk, ((W - stk.width) // 2, H - stk.height - 40))
    for cx in (70, 650):
        seta(d, cx, 960, 1150, 90, VERM)
    im.save(OUT / "cta_final.png")


if __name__ == "__main__":
    banner()
    stk = sticker()
    cta(stk)
    A80, A64, A56 = F(AN, 92), F(AN, 76), F(AN, 60)
    # ganchos (tela cheia)
    caixa_titulo(["3 ERRORES", "AL COMPRAR PERFUME"], 560, [F(AN, 110), F(AN, 64)], [AMA, BRANCO], nome="tit_07.png")
    caixa_titulo(["UN PERFUME", "PARA CADA MOMENTO"], 560, [F(AN, 104), F(AN, 64)], [AMA, BRANCO], nome="tit_08.png")
    caixa_titulo(["¿UNO SOLO", "PARA TODO?"], 150, [F(AN, 110), F(AN, 96)], [BRANCO, AMA], nome="tit_09.png")
    # rotulos de segmento (topo, abaixo do selo)
    caixa_titulo(["ERROR #1", "PAGAR POR LA MARCA DEL MALL"], 150, [F(AN, 84), F(PB, 34)], [VERM[:3] + (255,), BRANCO],
                 fundo=(12, 12, 12, 215), nome="err1.png")
    caixa_titulo(["ERROR #2", "UN SOLO PERFUME PARA TODO"], 150, [F(AN, 84), F(PB, 34)], [VERM[:3] + (255,), BRANCO],
                 fundo=(12, 12, 12, 215), nome="err2.png")
    caixa_titulo(["ERROR #3", "PAGAR ANTES DE TENERLO"], 150, [F(AN, 84), F(PB, 34)], [VERM[:3] + (255,), BRANCO],
                 fundo=(12, 12, 12, 215), nome="err3.png")
    caixa_titulo(["LA PEGA", "ARMAF CLUB DE NUIT"], 900, [F(AN, 84), F(PB, 36)], [AMA, BRANCO], fundo=(12, 12, 12, 215), nome="lab_pega.png")
    caixa_titulo(["LA CITA", "LATTAFA ASAD"], 900, [F(AN, 84), F(PB, 36)], [AMA, BRANCO], fundo=(12, 12, 12, 215), nome="lab_cita.png")
    caixa_titulo(["EL FINDE", "AFNAN 9PM"], 900, [F(AN, 84), F(PB, 36)], [AMA, BRANCO], fundo=(12, 12, 12, 215), nome="lab_finde.png")
    caixa_titulo(["3 PERFUMES", "AL PRECIO DE 1"], 150, [F(AN, 92), F(AN, 64)], [AMA, BRANCO], fundo=(12, 12, 12, 215), nome="lab_3x1.png")
    # previa
    base = Image.open(Path(r"C:\Users\PICHAU\Downloads\KIT-HOMBRE-3EN1\LOTE-15-10\_trabalho\C\img\C07-A1.png")).convert("RGBA").resize((W, H))
    prev = []
    for n in ["tit_07.png", "err1.png", "lab_pega.png", "cta_final.png"]:
        b = base.copy()
        b.alpha_composite(Image.open(OUT / "banner_topo.png"), (0, 0))
        b.alpha_composite(Image.open(OUT / n))
        if n == "err1.png":
            b.alpha_composite(Image.open(OUT / "sticker_kit.png"), ((W - 460) // 2, H - 340 - 40))
        prev.append(b.resize((360, 640)))
    p = Image.new("RGBA", (360 * len(prev), 640))
    for i, b in enumerate(prev):
        p.paste(b, (360 * i, 0))
    p.convert("RGB").save(OUT / "preview.jpg", quality=88)
    print("ok")
