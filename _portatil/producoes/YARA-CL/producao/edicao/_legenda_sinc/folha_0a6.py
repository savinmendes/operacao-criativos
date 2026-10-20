# -*- coding: utf-8 -*-
"""Folha 0-6 s de cada gancho: 1 quadro a cada 0,4 s + o quadro em que cada bloco de legenda aparece,
com a palavra falada naquele instante (alinhamento forcado no audio limpo)."""
import json, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import medir_sinc as ms
import alinhar_roteiro as ar

Y = Path(r"C:\Users\PICHAU\Downloads\YARA-CL")
ED = Y / "producao" / "edicao"
F = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 17)
TW, TH = 216, 384


def quadro(video, k):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-vf", f"select=eq(n\\,{k}),scale={TW}:{TH}",
                        "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    return Image.frombytes("RGB", (TW, TH), r.stdout)


def folha(h, cfg, ass, video, saida):
    c, raiz, faixas, t_tit, t_cta, tot = ms.preparar(cfg)
    ref = ar.palavras_timeline(c["segmentos"], raiz, faixas, json.load(open(ED / "textos_legenda.json", encoding="utf-8")), "ctc")
    ev = ms.eventos(ass)
    ks = {int(round(t * 30)) for t in np.arange(0.2, 6.0, 0.4)}
    ks |= {int(np.ceil(e["ini"] * 30 - 1e-6)) for e in ev if e["ini"] < 6.0}
    ks = sorted(ks)
    cols = 6
    rows = (len(ks) + cols - 1) // cols
    img = Image.new("RGB", (cols * TW, rows * (TH + 48) + 40), (20, 20, 20))
    d = ImageDraw.Draw(img)
    d.text((8, 8), f"{h}  0-6 s  (titulo ate {t_tit:.2f} s)  amarelo = quadro em que um bloco de legenda entra", font=F, fill=(255, 255, 255))
    for i, k in enumerate(ks):
        t = k / 30
        x, y = (i % cols) * TW, 40 + (i // cols) * (TH + 48)
        img.paste(quadro(video, k), (x, y))
        fala = [r for r in ref if r[1] <= t + 0.017 and t < r[2] + 0.05]
        ult = [r for r in ref if r[1] <= t + 0.017]
        txt = fala[-1][0] if fala else ("(pausa)" if ult else "(silencio)")
        novo = any(int(np.ceil(e["ini"] * 30 - 1e-6)) == k for e in ev)
        cor = (255, 220, 0) if novo else (230, 230, 230)
        d.text((x + 4, y + TH + 2), f"t={t:.2f}s", font=F, fill=cor)
        ini = f" @{fala[-1][1]:.2f}" if fala else ""
        d.text((x + 4, y + TH + 22), f"fala: {txt}{ini}", font=F, fill=cor)
    img.save(saida, quality=88)
    return saida


if __name__ == "__main__":
    out = []
    for h in ["H1", "H2", "H3", "H4", "H5"]:
        out.append(folha(h, ED / "volume" / f"cfg_{h}.json", AQUI / "saidas" / f"YARA-BF_{h}_sem-musica.ass",
                         Y / "entregas" / "volume" / f"YARA-BF_{h}_sem-musica.mp4", AQUI / f"folha_0a6_{h}.jpg"))
    out.append(folha("AD-C", ED / "ad_C_final.json", AQUI / "saidas" / "AD-C_yara-kit3_bf_es-cl.ass",
                     Y / "entregas" / "AD-C_yara-kit3_bf_es-cl.mp4", AQUI / "folha_0a6_AD-C.jpg"))
    print("\n".join(map(str, out)))
