# -*- coding: utf-8 -*-
"""Recorta os b-rolls EXISTENTES (TESTE1 limpo por LaMa na v1 + prints ES da v1) -> broll/*.mp4"""
import sys, json, subprocess
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent)); import norm
BR = Path(__file__).resolve().parents[1]; RAIZ = BR.parents[2]          # TESTE1-SB-ES
BASE = RAIZ / "_trabalho" / "lama" / "base_limpa.mp4"; G = RAIZ / "_trabalho" / "graficos"
CORTES = {  # nome: (a, b) em s no TESTE1 (base_limpa), com margem dos cortes detectados (scdet)
    "e01_teclado": (46.80, 47.83), "e02_sb_de_pie": (51.50, 52.75), "e03_sb_escribiendo": (53.30, 55.28),
    "e04_sb_acantilado": (55.40, 58.15), "e05_mujer_rezando": (58.28, 59.75), "e06_sb_grimorio": (77.95, 80.22),
    "e07_pergamino": (82.60, 85.55), "e08_cruz_agua": (88.85, 89.95), "e09_montanas_niebla": (90.45, 91.95),
    "e10_hombre_rezando": (92.50, 93.88), "e11_nino_playa": (95.88, 97.18), "e12_congreso": (99.05, 101.15),
    "e13_mujer_negra_rezando": (106.58, 108.80), "e14_deudas": (132.85, 136.15), "e15_alivio_paid": (136.42, 139.65)}
for n, (a, b) in CORTES.items():
    norm.video(BASE, BR / f"{n}.mp4", a, b); print(n, round(b - a, 2))
# prints ES (v1): zoom lento 1 -> 1.035 como na v1
for n, png, d in [("e16_print_geralda", "chat_1.png", 3.0), ("e17_print_rosa_maria", "chat_2.png", 3.0), ("e18_print_carmen", "chat_3.png", 3.0)]:
    norm.kb(G / png, BR / f"{n}.mp4", d, 1.0, 1.035); print(n, d)
# quadro das 12 palavras ES (v1) + titulo + circulos vermelhos sincronizados com L09b (t=0 = inicio do L09b)
L = json.loads((RAIZ / "_trabalho" / "voz" / "c" / "L09b.json").read_text(encoding="utf-8"))
W = [p["ini"] for p in L["palavras"] if p["w"].lower().strip(".") != "y"]
DUR = round(L["dur"] + 0.45, 2); N = int(round(DUR * 30))
base = Image.open(RAIZ / "_trabalho" / "q" / "board_clean.png").convert("RGBA"); base.alpha_composite(Image.open(G / "board_titulo.png"))
circ = {(k, j): Image.open(G / f"circ_{k:02d}_{j}.png") for k in range(12) for j in range(4)}
cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "720x1280", "-r", "30", "-i", "-",
       "-vf", "scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p", *norm.ENC, *norm.TAG, str(BR / "e19_cuadro_12_palabras.mp4")]
pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for q in range(N):
    t = q / 30; z = 1.0 + 0.03 * q / (N - 1)
    im = base.copy()
    for k, w in enumerate(W):
        ini = w - 0.05
        if t >= ini:
            j = min(3, int((t - ini) * 30)); im.alpha_composite(circ[(k, j)])
    im = im.convert("RGB"); w2, h2 = int(720 * z), int(1280 * z)
    im = im.resize((w2, h2), Image.LANCZOS).crop(((w2 - 720) // 2, (h2 - 1280) // 2, (w2 - 720) // 2 + 720, (h2 - 1280) // 2 + 1280))
    pr.stdin.write(np.asarray(im).tobytes())
pr.stdin.close(); pr.wait(); print("e19_cuadro_12_palabras", DUR, "circulos em", [round(w - 0.05, 2) for w in W])
