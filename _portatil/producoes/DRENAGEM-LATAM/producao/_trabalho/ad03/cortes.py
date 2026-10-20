# -*- coding: utf-8 -*-
"""Refina pontos de corte (silêncio entre palavras) e grava cortes_longo.json / cortes_curto.json"""
import json, wave, numpy as np
P = json.load(open('pal03.json', encoding='utf-8'))
w = wave.open('a16.wav'); sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)
def rms_min(t0, t1):
    if t1 - t0 < 0.03: return (t0 + t1) / 2
    best, bt = 1e18, (t0 + t1) / 2
    t = t0
    while t <= t1 - 0.02:
        i = int(t * sr); r = float(np.mean(a[i:i + int(0.02 * sr)] ** 2))
        if r < best: best, bt = r, t + 0.01
        t += 0.005
    return bt
def ini(s):
    prev = max([e for _, _, e in P if e <= s + 0.01] or [s - 0.3])
    return round(rms_min(max(prev, s - 0.4), s + 0.02), 3)
def fim(e):
    nxt = min([s for _, s, _ in P if s >= e - 0.01] or [e + 0.3])
    return round(rms_min(e - 0.02, min(nxt, e + 0.4)), 3)
LONGO = [(0, 68.22), (84.74, 93.36), (98.88, 105.46), (113.24, 138.48), (139.88, 150.36), (159.26, 185.24), (199.24, 229.20),
         (252.32, 258.54), (269.38, 288.82), (322.30, 336.36), (370.04, 373.82), (392.52, 509.12),
         (531.42, 537.44), (542.40, 584.38), (611.58, 632.48), (640.50, 659.60)]
CURTO = [(0, 21.38), (439.52, 457.36), (463.56, 483.16), (578.58, 584.38)]
# ajustes de vídeo (início/fim no corte de cena, evita quadro solto) — índice: [vs, ve]
AJUSTE_V = {'longo': {0: [None, 68.30], 1: [85.2, None], 3: [None, 138.40], 4: [140.1, None], 5: [159.667, None], 11: [393.467, None],
                      12: [None, 537.40], 13: [542.5334, 584.2667], 14: [611.933, None]},
            'curto': {0: [None, 21.2667], 3: [None, 584.2667]}}
for nome, L in (('longo', LONGO), ('curto', CURTO)):
    seg = [[0.0 if s == 0 else ini(s), fim(e)] for s, e in L]
    for k, v in AJUSTE_V.get(nome, {}).items():
        seg[k] = seg[k] + v
    json.dump(seg, open(f'cortes_{nome}.json', 'w'), indent=0)
    print(nome, seg, 'total %.1f s' % sum(g[1] - g[0] for g in seg))
