# -*- coding: utf-8 -*-
# Folha visual da correcao de cor do AD 09: original x antes x depois (finais), recorte do rosto, e zoom da boca do E1
# em 46,85-47,15 s. Sem abrir video. Uso: python folha_cor.py  -> _cor_rev/folha_cor.jpg e _cor_rev/folha_E1.jpg
import sys, json, cv2, numpy as np
from pathlib import Path
R = Path(__file__).resolve().parent; AD = R.parent; T = AD.parent; P = T.parents[1]
sys.path.insert(0, str(T / "ad13" / "lipsync3"))
from comum3 import quadros
FIN = next((P / "producao").glob("AD 09 - *-ES-LATAM.mp4")); ANT = next((AD / "_antes_cor").glob("AD 09 - *-ES-LATAM.mp4"))
ORI = P / "UNICOS_HD" / "09.mp4"
segs = json.loads((AD / "lipsync" / "segs.json").read_text())["segs"]
def face(q24):
    for s in segs:
        a, b = s["q"]
        if a <= q24 <= b: return json.loads((AD / "lipsync" / "boxes" / f"{s['nome']}.json").read_text())["boxes"][q24 - a]["face"], s["nome"]
    return None, "-"
Q24 = [100, 300, 600, 850, 1000, 1200, 1400, 1650, 1800, 1950, 2250, 2400, 2460]
E1 = list(range(1124, 1133))
def pega(path, fps, qs):
    want = {int(round(q * fps / 24)): q for q in qs}; out = {}
    for i, f in enumerate(quadros(path, 0, max(want) + 1)):
        if i in want: out[want[i]] = f
    return out
todos = sorted(set(Q24 + E1))
o, a, d = pega(ORI, 24, todos), pega(ANT, 30, todos), pega(FIN, 30, todos)
def rec(f, fc, esc, L):
    x0, y0, x1, y1 = fc; cx, cy = (x0 + x1) / 2, y0 + 0.55 * (y1 - y0); w = (x1 - x0) * esc
    X0, Y0 = int(max(0, cx - w / 2)), int(max(0, cy - w * 0.6)); c = f[Y0:Y0 + int(w * 1.2), X0:X0 + int(w)]
    return cv2.resize(c, (L, int(L * 1.2)))
def put(im, t):
    cv2.putText(im, t, (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 3); cv2.putText(im, t, (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    return im
linhas = []
for q in Q24:
    fc, nm = face(q)
    if fc is None: continue
    cs = [put(rec(x[q], fc, 1.8, 300), f"{lab} {q/24:.2f}s {nm}") for x, lab in ((o, "orig"), (a, "antes"), (d, "depois"))]
    linhas.append(np.hstack(cs))
cv2.imwrite(str(R / "folha_cor.jpg"), np.vstack(linhas), [cv2.IMWRITE_JPEG_QUALITY, 88])
ls = []
for x, lab in ((o, "orig"), (a, "antes"), (d, "depois")):
    ls.append(np.hstack([put(rec(x[q], face(q)[0], 1.0, 200), f"{lab} {q/24:.3f}") for q in E1]))
cv2.imwrite(str(R / "folha_E1.jpg"), np.vstack(ls), [cv2.IMWRITE_JPEG_QUALITY, 90]); print("ok")
