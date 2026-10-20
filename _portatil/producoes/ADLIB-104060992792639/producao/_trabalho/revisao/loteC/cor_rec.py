# -*- coding: utf-8 -*-
"""Correcao de cor (lote C): cor.py + brilho.py numa passada, com o ORIGINAL reenquadrado igual ao final na abertura
(AD 10: recorte 320x569 em (400,230) nos quadros q24 0-232; AD 16: recorte 360x640 em (200,180) nos quadros 0-291).
Fora da abertura as contas sao identicas as do cor.py (passo 6, Y U V) e do brilho.py (passo 3, Y + fundo).
Uso: python cor_rec.py NN [video_final]"""
import sys, json, cv2, numpy as np
from pathlib import Path
NN = sys.argv[1]; D = Path(__file__).parent
P = Path(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639")
FIN = Path(sys.argv[2]) if len(sys.argv) > 2 else next((P / "producao").glob(f"AD {NN} - *-ES-LATAM.mp4"))
ORI = P / "UNICOS_HD" / f"{NN}.mp4"
REC = {"10": (400, 230, 320, 569, 232), "16": (200, 180, 360, 640, 291)}.get(NN)
esc = json.loads((D / f"escolha_{NN}.json").read_text()); pos = {}
for k, (a, b, t) in esc.items():
    for q, cx, cy, L in t: pos[q] = (k, cx, cy, L)
cf, co = cv2.VideoCapture(str(FIN)), cv2.VideoCapture(str(ORI)); fpo = co.get(cv2.CAP_PROP_FPS)
def bx(im, cx, cy, w, h): x0, y0 = int(max(0, cx - w / 2)), int(max(0, cy - h / 2)); return im[y0:int(y0 + h), x0:int(x0 + w)].reshape(-1, im.shape[2]).mean(0)
RC, RB = {}, {}; oi = -1; o = None; q = 0
while True:
    ok, f = cf.read()
    if not ok: break
    want = int(round(q / 30 * fpo))
    while oi < want:
        ok2, o2 = co.read(); oi += 1
        if ok2: o = o2
    if q in pos and (q % 6 == 0 or q % 3 == 0) and o is not None:
        oo = o
        if REC and oi <= REC[4]:
            x, y, w, h, _ = REC; oo = cv2.resize(o[y:y + h, x:x + w], (720, 1280), interpolation=cv2.INTER_LANCZOS4)
        k, cx, cy, L = pos[q]; F = cv2.cvtColor(f, cv2.COLOR_BGR2YUV).astype(float); O = cv2.cvtColor(oo, cv2.COLOR_BGR2YUV).astype(float)
        dd = lambda *a: bx(F, *a) - bx(O, *a)
        boca = (dd(cx, cy - 0.17 * L, 0.30 * L, 0.08 * L) + dd(cx, cy + 0.30 * L, 0.30 * L, 0.12 * L)) / 2
        face = (dd(cx - 0.33 * L, cy - 0.55 * L, 0.14 * L, 0.14 * L) + dd(cx + 0.33 * L, cy - 0.55 * L, 0.14 * L, 0.14 * L)) / 2
        if q % 6 == 0: RC.setdefault(k, []).append(np.r_[boca, face])
        if q % 3 == 0:
            m = np.ones(F.shape[:2], bool); m[int(max(0, cy - 1.6 * L)):int(cy + 1.0 * L), int(max(0, cx - 0.9 * L)):int(cx + 0.9 * L)] = False
            RB.setdefault(k, []).append((boca[0], face[0], F[..., 0][m].mean() - O[..., 0][m].mean()))
    q += 1
print(f"AD {NN} ({FIN.name}): final - original{' (abertura: original reenquadrado igual)' if REC else ''}")
print("trecho    | cor.py: boca Y U V | face Y U V | degrau Y V || brilho.py: boca face fundo | boca-face")
ac, ab = [], []
for k in esc:
    if k not in RC: continue
    r = np.median(np.array(RC[k]), 0); b = np.array(RB[k]); ac += RC[k]; ab += RB[k]
    print(f"{k:9} | {r[0]:+5.1f} {r[1]:+5.1f} {r[2]:+5.1f} | {r[3]:+5.1f} {r[4]:+5.1f} {r[5]:+5.1f} | {r[0]-r[3]:+5.1f} {r[2]-r[5]:+5.1f} || "
          f"{np.median(b[:,0]):+5.1f} {np.median(b[:,1]):+5.1f} {np.median(b[:,2]):+5.1f} | {np.median(b[:,0]-b[:,1]):+5.1f}")
r = np.median(np.array(ac), 0); b = np.array(ab)
print(f"TODOS     | {r[0]:+5.1f} {r[1]:+5.1f} {r[2]:+5.1f} | {r[3]:+5.1f} {r[4]:+5.1f} {r[5]:+5.1f} | {r[0]-r[3]:+5.1f} {r[2]-r[5]:+5.1f} || "
      f"{np.median(b[:,0]):+5.1f} {np.median(b[:,1]):+5.1f} {np.median(b[:,2]):+5.1f} | {np.median(b[:,0]-b[:,1]):+5.1f}")
