# -*- coding: utf-8 -*-
"""Revisor: folha de zoom na boca, de 3 em 3 quadros, FINAL (linha de cima) x ORIGINAL (linha de baixo) no mesmo
tempo, com barra de energia da voz ES (verde) e da voz PT original (vermelho) sob cada quadro.
Uso: python folha_boca.py ad01|ad13 t_ini t_fim saida.jpg [passo=3] [por_linha=16]"""
import sys, csv
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl

AD, t0, t1, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
passo = int(sys.argv[5]) if len(sys.argv) > 5 else 3
porl = int(sys.argv[6]) if len(sys.argv) > 6 else 16
P = Path(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639")
T = P / "producao" / "_trabalho" / AD
FIN = P / "producao" / {"ad01": "AD 01 - ORACION-TRES-BENDICIONES-ES-LATAM.mp4", "ad13": "AD 13 - ORACION-PAZ-ES-LATAM.mp4", "ad11": "AD 11 - ORACION-DESATADORA-ES-LATAM.mp4", "ad05": "AD 05 - ORACION-FAMILIA-ES-LATAM.mp4"}[AD]
ORI = P / "UNICOS_HD" / {"ad01": "01.mp4", "ad13": "13.mp4", "ad11": "11.mp4", "ad05": "05.mp4"}[AD]
rows = list(csv.DictReader(open(Path(__file__).parent / f"boca_{AD}.csv")))
N = len(rows)
es = cl.envelope(cl.ler_audio(T / "narracao_es.wav"), 16000, 30.0, N)
_v = cl.ler_audio(T / "_audio/demucs/htdemucs/orig/vocals.wav")
if AD == "ad05":
    _c0, _cn = int(1286 / 24 * 16000), int(70 / 24 * 16000); _v = np.concatenate([_v[:_c0], _v[_c0 + _cn:]])
pt = cl.envelope(_v, 16000, 30.0, N)
def nrm(e):
    return np.clip((e - (np.nanmax(e) - 40)) / 40, 0, 1)
es, pt = nrm(es), nrm(pt)
a, b = int(t0 * 30), min(int(t1 * 30), N - 1)
idx = list(range(a, b + 1, passo))
cf, co = cv2.VideoCapture(str(FIN)), cv2.VideoCapture(str(ORI))
cf.set(cv2.CAP_PROP_POS_FRAMES, a); co.set(cv2.CAP_PROP_POS_FRAMES, a)
S = 120
tiles = []
last = None
oi = -1; o = None
if AD == "ad05": co.set(cv2.CAP_PROP_POS_FRAMES, 0)
for q in range(a, b + 1):
    ok, f = cf.read()
    if AD == "ad05":
        tq = q / 30; want = int(round((tq if tq * 24 < 1286 else tq + 70 / 24) * 24))
        if oi < 0: co.set(cv2.CAP_PROP_POS_FRAMES, want); oi = want - 1
        while oi < want: ok2, o = co.read(); oi += 1
    else:
        ok2, o = co.read()
    if not ok or not ok2: break
    r = rows[q]
    if r["cx"] != "":
        L = float(r["larg"]); last = (int(r["cx"]), int(r["cy"]), L)
    if q not in idx: continue
    if last is None:
        cx, cy, L = 360, 640, 400
    else:
        cx, cy, L = last
    h = int(max(40, 0.45 * L))
    x0, y0 = max(0, cx - h), max(0, cy - h)
    def crop(img):
        c = img[y0:y0 + 2 * h, x0:x0 + 2 * h]
        return cv2.resize(c, (S, S))
    t = np.full((2 * S + 34, S, 3), 255, np.uint8)
    t[:S] = crop(f); t[S:2 * S] = crop(o)
    t[2 * S + 2:2 * S + 10, :int(S * es[q])] = (0, 160, 0)
    t[2 * S + 12:2 * S + 20, :int(S * pt[q])] = (0, 0, 200)
    if r["cx"] == "": cv2.rectangle(t, (0, 0), (S - 1, 2 * S - 1), (0, 200, 255), 2)
    cv2.putText(t, f"{q/30:.2f}", (2, 2 * S + 32), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
    tiles.append(t)
linhas = []
for i in range(0, len(tiles), porl):
    l = tiles[i:i + porl]
    while len(l) < porl: l.append(np.full_like(tiles[0], 255))
    linhas.append(np.hstack(l))
img = np.vstack(linhas)
cv2.imwrite(out, img, [cv2.IMWRITE_JPEG_QUALITY, 85])
print("ok", out, len(tiles))
