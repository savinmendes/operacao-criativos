# -*- coding: utf-8 -*-
"""V26: imagem do corpo (0 -> 30,967 s) com trocas Vitaly -> Lymphoria e textos suavizados.
  python render_v26.py  -> corpo_video.mp4 (sem áudio)"""
import sys, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, str(Path(__file__).parent.parent / "comum"))
import texto as T

D = Path(__file__).parent
PROD = Path(r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\producao\_trabalho\ugc\prod")
W, H, FPS = 720, 1280, 30
NQ = 929                       # 0..928 -> corte em 30,967 s (antes de "Link en bio")

orig = T.ler_quadros(str(D / "orig.mp4"))
v3 = T.ler_quadros(str(PROD / "V3_frasco_mesa.mp4"))                      # 80 q
v1 = T.ler_quadros(str(PROD / "V1_gotero_hierbas.mp4"))                   # 90 q
p1 = T.ler_quadros(str(PROD / "P1_kit3.mp4"))                             # 90 q
p2 = T.ler_quadros(str(PROD / "P2_frasco_miel.mp4"), vf="setpts=PTS*104/90,fps=30")  # ~104 q
print(len(orig), len(v3), len(v1), len(p1), len(p2))


def take(arr, i):
    return arr[min(i, len(arr) - 1)].copy()


def ret_branco(im, box):
    ImageDraw.Draw(im).rectangle(box, fill=(255, 255, 255))


def grande(im, txt, cy, px, alpha=1.0, escala=1.0, cx=W / 2):
    """Texto grande branco com sombra suave, centrado em x, cy = centro vertical da tinta."""
    px = int(px * escala)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    y0, y1, _, _ = T.tinta_bbox([(txt, 1)], px)
    ytop = cy - (y0 + y1) / 2
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    T.desenhar_linha(sh, [(txt, 1)], cx, ytop + 3, px, cor=(0, 0, 0, int(130 * alpha)))
    sh = sh.filter(ImageFilter.GaussianBlur(5))
    lay = Image.alpha_composite(lay, sh)
    T.desenhar_linha(lay, [(txt, 1)], cx, ytop, px, cor=(255, 255, 255, int(255 * alpha)))
    return Image.alpha_composite(im, lay)


def gota(im, cx, cy, h, alpha=1.0):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    r = h * 0.36
    d.ellipse((cx - r, cy + h / 2 - 2 * r, cx + r, cy + h / 2), fill=(255, 255, 255, int(255 * alpha)))
    d.polygon([(cx, cy - h / 2), (cx - r * 0.93, cy + h / 2 - r * 1.25), (cx + r * 0.93, cy + h / 2 - r * 1.25)],
              fill=(255, 255, 255, int(255 * alpha)))
    return Image.alpha_composite(im, lay)


def pop(k, k0, n=4):
    """escala de 'pop' na entrada"""
    u = (k - k0) / n
    return 1.0 if u >= 1 else 0.75 + 0.25 * u + 0.12 * np.sin(np.pi * u)


# máscara arredondada da caixa "No era GRASA" (copiada do original para o take novo)
BOX = (108, 64, 601, 257)
mbox = Image.new("L", (W, H), 0)
ImageDraw.Draw(mbox).rounded_rectangle(BOX, radius=10, fill=255)
mbox = np.asarray(mbox)[..., None] / 255.0

ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                       "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "14", "-preset", "medium",
                       "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
                       "-colorspace", "bt709", str(D / "corpo_video.mp4")], stdin=subprocess.PIPE)
PREV = [int(x) for x in sys.argv[sys.argv.index("--prev")+1].split(",")] if "--prev" in sys.argv else None
for k in (PREV or range(NQ)):
    if k <= 83:                                   # gancho (quadro 84 do original já é o frasco Vitaly): "-7 KILOS 😱" -> "ADIÓS HINCHAZÓN 😱"
        im = Image.fromarray(orig[k]).convert("RGBA")
        ret_branco(im, (106, 183, 611, 238))
        T.desenhar_linha(im, [("ADIÓS HINCHAZÓN 😱", 1)], 358.5, 186 - 11 + 2, 41)
    elif k <= 164:                                # (84 = 1º quadro do take) frasco Vitaly na mão -> frasco Lymphoria + NO DIETAS/NO GIMNASIO
        a = take(v3, max(0, k - 85)).astype(np.float32)
        f = 1.0 - 0.47 * min(1.0, (k - 85) / 28)
        im = Image.fromarray((a * f).clip(0, 255).astype(np.uint8)).convert("RGBA")
        if k >= 97:
            e = pop(k, 97)
            im = grande(im, "NO", 420, 118, escala=e)
            im = grande(im, "DIETAS", 535, 118, escala=e)
        if k >= 127:
            e = pop(k, 127)
            im = grande(im, "NO", 695, 118, escala=e)
            im = grande(im, "GIMNASIO", 805, 112, escala=e)
    elif k <= 310:                                # conta-gotas Vitaly -> gotero Lymphoria / kit Lymphoria
        im = Image.fromarray(take(v1, k - 165) if k <= 254 else take(p1, k - 255)).convert("RGBA")
        if k >= 176:
            u = min(1.0, (k - 176) / 8)
            dy = (1 - u) * -40
            im = grande(im, "ESTAS GOTAS", 108 + dy, 76, alpha=u)
            im = grande(im, "LYMPHORIA", 205 + dy, 84, alpha=u, cx=318)
            im = gota(im, 625, 203 + dy, 70, alpha=u)
    elif k <= 603:                                # "Mes 1: -7 kg de HINCHAZÓN" -> "Mes 1: Adiós a la HINCHAZÓN"
        im = Image.fromarray(orig[k]).convert("RGBA")
        ret_branco(im, (40, 248, 680, 294))
        T.desenhar_linha(im, [("Mes 1:", 1), (" Adiós a la ", 0), ("HINCHAZÓN", 1)], 359, 252 - 4, 36)
    elif k <= 707:                                # frasco Vitaly legível -> frasco Lymphoria (caixa original por cima)
        a = take(p2, k - 604).astype(np.float32)
        o = orig[k].astype(np.float32)
        im = Image.fromarray((o * mbox + a * (1 - mbox)).astype(np.uint8)).convert("RGBA")
    elif k <= 843:
        im = Image.fromarray(orig[k]).convert("RGBA")
    else:                                         # "LINK EN BIO 👇" -> "TOCA EL BOTÓN DE ABAJO 👇"
        im = Image.fromarray(orig[k]).convert("RGBA")
        ret_branco(im, (40, 80, 681, 122))
        T.desenhar_linha(im, [("TOCA EL BOTÓN DE ABAJO 👇", 1)], 360, 83 - 2, 34)
    if PREV:
        im.convert("RGB").save(D / "fr" / f"prev_{k}.png"); continue
    ff.stdin.write(np.asarray(im.convert("RGB")).tobytes())
ff.stdin.close()
ff.wait()
print("ok corpo_video.mp4")
