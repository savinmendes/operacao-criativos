# -*- coding: utf-8 -*-
"""Cola cada out/ls_sNN.mp4 na base (reamostrando p/ N quadros) e mede o índice de pausa por trecho e o total.
Uso: python medir_out.py [sNN ...]"""
import sys, json, cv2, numpy as np
from pathlib import Path
import colar as C, medir as Me
AQ = Path(__file__).parent; AD = AQ.parent
segs = json.loads((AD / "segmentos.json").read_text())["segmentos"]
so = sys.argv[1:]; tot = {"p": 0.0, "np": 0, "f": 0.0, "nf": 0}; res = {}
for s in segs:
    nome = s["nome"]
    if so and nome not in so: continue
    p = AQ / "out" / f"ls_{nome}.mp4"
    if not p.exists(): print(nome, "sem saída"); continue
    a, n = s["quadro_ini"], s["n"]
    g = C.ler(p); m = len(g); g = C.reamostrar(g[:n] if s["pad"] else g, n)
    base = cv2.VideoCapture(str(AD / "base_sem_legenda.mp4")); base.set(1, a)
    bs = [base.read()[1] for _ in range(n)]
    col = C.colador(nome); fr = [col(b, g, i) for i, b in enumerate(bs)]
    r = Me.medir(Me.aberturas_frames(fr), a); ro = Me.medir(Me.aberturas_frames(bs), a)
    for k, kk in (("p", "sum_pes"), ("np", "n_pes"), ("f", "sum_fes"), ("nf", "n_fes")): tot[k] += r[kk]
    res[nome] = {"quadros_saida": m, "idxES": r["idxES"], "corrES": r["corrES"], "corrPT": r["corrPT"], "orig_idxES": ro["idxES"], "qpausa": r["qpausa"]}
    print(f"{nome}: saida {m}q -> {n} | idxES={r['idxES']:.2f} corrES={r['corrES']:.2f} corrPT={r['corrPT']:.2f} pausaq={r['qpausa']} det={r['detect']:.0%} | original idxES={ro['idxES']:.2f}", flush=True)
if tot["np"] and tot["nf"]: print(f"TOTAL idxES={(tot['p']/tot['np'])/(tot['f']/tot['nf']):.2f}")
json.dump(res, open(AQ / ("medidas.json" if not so else "medidas_parcial.json"), "w"), indent=1, default=float)
