# -*- coding: utf-8 -*-
"""Sincronia fala x boca no video final: abertura da boca (MediaPipe) x envelope do audio, lag de -8..+8 quadros.
Uso: python qa_sync.py final.mp4 t1 t2 ... (s do video final; janela de 8 s)"""
import sys, subprocess, json, numpy as np
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\montagem\scripts")
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from vslcomum import ler
import checar_lipsync as CL
v = sys.argv[1]; res = []
import os; DURW = float(os.environ.get("JANELA", "8"))
for t in map(float, sys.argv[2:]):
    fr = ler(v, t, int(DURW * 30))
    tr = CL.Rastreador(); ab = []
    for f in fr:
        p = tr.pontos(f); ab.append(CL._abertura(p) if p is not None else np.nan)
    tr.close(); ab = np.array(ab)
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t}", "-t", str(DURW), "-i", v, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                                     capture_output=True).stdout, np.float32)
    env = np.array([np.sqrt(np.mean(x[i * 16000 // 30:(i + 1) * 16000 // 30] ** 2) + 1e-9) for i in range(len(fr))])
    env = 20 * np.log10(env)
    ok = ~np.isnan(ab)
    best = None
    for lag in range(-8, 9):
        a = ab[max(0, lag):len(ab) + min(0, lag)]; e = env[max(0, -lag):len(env) - max(0, lag)]; m = ~np.isnan(a)
        if m.sum() < 60: continue
        c = np.corrcoef(a[m], e[m])[0, 1]
        if best is None or c > best[1]: best = (lag, c)
    res.append({"t": t, "rosto_%": round(100 * ok.mean()), "lag_quadros": None if best is None else best[0],
                "corr": None if best is None else round(float(best[1]), 2)})
    print(res[-1], flush=True)
json.dump(res, open(sys.argv[1] + ".sync.json", "w"))
