# -*- coding: utf-8 -*-
"""Folha visual da correcao de cor: por instante, ORIGINAL | ANTES | DEPOIS (quadro inteiro reduzido + zoom no rosto de quem fala).
Saida: folha_cor_05.jpg"""
import sys, json
from pathlib import Path
import numpy as np, cv2
C = Path(__file__).resolve().parent; AD = C.parent; T = AD.parent; P = T.parents[1]
sys.path.insert(0, str(T / "ad13" / "lipsync3"))
from comum3 import quadros
NOME = "AD 05 - ORACION-FAMILIA-ES-LATAM.mp4"
FIN, ANT, ORI = P / "producao" / NOME, AD / "_antes_cor" / NOME, P / "UNICOS_HD" / "05.mp4"
esc = json.loads((T / "revisao" / "loteC" / "escolha_05.json").read_text()); pos = {}
for k, (a, b, t) in esc.items():
    for q, cx, cy, L in t: pos[q] = (k, cx, cy, L)
TS = [1.0, 2.6, 4.2, 9.0, 13.0, 21.0, 30.0, 41.0, 49.0, 57.0, 65.0, 76.0, 86.0, 93.0]
def pega(path, qs):
    out = {}; want = set(qs)
    for i, f in enumerate(quadros(path, 0, max(qs) + 1)):
        if i in want: out[i] = f
    return out
qf = [int(round(t * 30)) for t in TS]
qo = [int(round((t if t * 24 < 1286 else t + 70 / 24) * 24)) for t in TS]
F, A, O = pega(FIN, qf), pega(ANT, qf), pega(ORI, qo)
lin = []
for t, a, b in zip(TS, qf, qo):
    k = min(pos, key=lambda q: abs(q - a)) if pos else None
    nm, cx, cy, L = pos[k] if k is not None and abs(k - a) < 8 else ("-", 360, 500, 300)
    def z(im):
        x0, y0 = int(max(0, cx - 0.8 * L)), int(max(0, cy - 0.9 * L)); c = im[y0:int(cy + 0.9 * L), x0:int(cx + 0.8 * L)]
        return cv2.resize(c, (300, int(300 * c.shape[0] / max(1, c.shape[1])))) if c.size else np.zeros((300, 300, 3), np.uint8)
    cols = []
    for im, rot in ((O[b], "original"), (A[a], "antes"), (F[a], "depois")):
        s = cv2.resize(im, (225, 400)); zz = z(im); h = max(400, zz.shape[0])
        cel = np.zeros((h, 525, 3), np.uint8); cel[:400, :225] = s; cel[:zz.shape[0], 225:525] = zz[:h]
        cv2.putText(cel, f"{rot} {t:.1f}s {nm}", (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cols.append(cel)
    h = max(c.shape[0] for c in cols); lin.append(np.hstack([np.pad(c, ((0, h - c.shape[0]), (0, 0), (0, 0))) for c in cols]))
cv2.imwrite(str(C / "folha_cor_05.jpg"), np.vstack(lin), [cv2.IMWRITE_JPEG_QUALITY, 85]); print("ok", C / "folha_cor_05.jpg")
