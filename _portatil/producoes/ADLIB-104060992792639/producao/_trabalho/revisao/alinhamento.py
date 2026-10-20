# -*- coding: utf-8 -*-
"""Revisor: para cada trecho de lipsync, acha o deslocamento (em quadros) entre a saida do HeyGen e
(a) o original no tempo previsto e (b) o video final no tempo previsto. Usa a imagem toda reduzida (sem a
faixa de legenda), entao a boca pesa pouco. Imprime o deslocamento de melhor casamento no inicio e no fim.
Uso: python alinhamento.py ad01|ad13"""
import sys, json
from pathlib import Path
import numpy as np, cv2

AD = sys.argv[1]
T = Path(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho") / AD
FIN = {"ad01": "AD 01 - ORACION-TRES-BENDICIONES-ES-LATAM.mp4", "ad13": "AD 13 - ORACION-PAZ-ES-LATAM.mp4"}[AD]
ORI = {"ad01": "01.mp4", "ad13": "13.mp4"}[AD]
fin = T.parent.parent / FIN
ori = T.parent.parent.parent / "UNICOS_HD" / ORI
seg = json.loads((T / "segmentos.json").read_text(encoding="utf-8"))["segmentos"]


def ler(p):
    c = cv2.VideoCapture(str(p)); out = []
    while True:
        ok, f = c.read()
        if not ok: break
        out.append(cv2.resize(cv2.cvtColor(f[:760], cv2.COLOR_BGR2GRAY), (90, 95)).astype(np.float32))
    return out

F = ler(fin); O = ler(ori)
print("quadros final", len(F), "original", len(O))
for s in seg:
    nome = s.get("nome") or Path(s["arquivo"]).stem.replace("seg_", "")
    L = ler(T / "lipsync" / f"ls_{nome}.mp4")
    a, b = s["quadro_ini"], s["quadro_fim"]
    res = []
    for ref, R in (("orig", O), ("final", F)):
        for parte, idx in (("ini", range(0, 8)), ("fim", range(len(L) - 8, len(L)))):
            best = None
            for off in range(-6, 7):
                ds = []
                for i in idx:
                    j = a + i + off
                    if 0 <= j < len(R): ds.append(np.mean(np.abs(L[i] - R[j])))
                if ds:
                    m = float(np.mean(ds))
                    if best is None or m < best[1]: best = (off, m)
            res.append(f"{ref}-{parte}: off {best[0]:+d} (d {best[1]:.1f})")
    print(nome, f"quadros {a}-{b} ({b-a+1}) ls={len(L)}", " | ".join(res))
