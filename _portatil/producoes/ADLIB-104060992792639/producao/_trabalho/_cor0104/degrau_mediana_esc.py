# -*- coding: utf-8 -*-
"""Degrau robusto ao formato da boca (mesma ideia do _ad1718/degrau_mediana.py), usando as posicoes de boca do revisor
(escolha_NN.json: q, cx, cy, L): MEDIANA de (final - original) em luma dentro de uma elipse na boca/queixo (0,30L x 0,40L)
contra a mediana num anel de pele em volta (1,3x a 1,9x). A mediana ignora o +/- do labio que mudou de lugar; um degrau de
cor desloca a mediana inteira. Uso: python degrau_mediana_esc.py NN pasta_escolha [arquivo_final]"""
import sys, json, cv2, numpy as np
from pathlib import Path
from util import quadros, UNICOS
NN, pasta = sys.argv[1], Path(sys.argv[2])
P = UNICOS.parent
FIN = Path(sys.argv[3]) if len(sys.argv) > 3 else next((P / "producao").glob(f"AD {NN} - *-ES-LATAM.mp4"))
esc = json.loads((pasta / f"escolha_{NN}.json").read_text()); pos = {}
for k, (a, b, t) in esc.items():
    for q, cx, cy, L in t: pos[q] = (k, cx, cy, L)
qs = {q for q in pos if q % 4 == 0}; mx = max(qs) + 1; res = {}
for i, (f, o) in enumerate(zip(quadros(FIN, 0, mx), quadros(UNICOS / f"{NN}.mp4", 0, mx))):
    if i not in qs: continue
    k, cx, cy, L = pos[i]; c = (int(cx), int(cy + 0.08 * L)); ax = (0.30 * L, 0.40 * L)
    def el(s):
        m = np.zeros((1280, 720), np.uint8); cv2.ellipse(m, c, (int(ax[0] * s), int(ax[1] * s)), 0, 0, 360, 1, -1); return m > 0
    d = cv2.cvtColor(f, cv2.COLOR_BGR2YUV)[:, :, 0].astype(float) - cv2.cvtColor(o, cv2.COLOR_BGR2YUV)[:, :, 0].astype(float)
    res.setdefault(k, []).append((np.median(d[el(1.0)]), np.median(d[el(1.9) & ~el(1.3)])))
print(f"AD {NN} ({FIN.name}): mediana final-original | elipse boca/queixo | anel de pele | degrau")
tot = []
for k in esc:
    if k not in res: continue
    v = np.median(np.array(res[k]), 0); tot += res[k]; print(f"  {k:9} {v[0]:+5.1f} {v[1]:+5.1f} {v[0]-v[1]:+5.1f}")
v = np.median(np.array(tot), 0); print(f"  TODOS     {v[0]:+5.1f} {v[1]:+5.1f} {v[0]-v[1]:+5.1f}")
