# -*- coding: utf-8 -*-
"""Revisor: le boca_adNN.csv e mede, por trecho, se a boca do final (personagem que fala) mudou e se acompanha a
voz ES (e nao a voz PT). Envelope PT = vocals.wav do demucs do original; ES = wav do personagem.
Uso: python analisar.py ad01|ad13"""
import sys, json, csv, subprocess
from pathlib import Path
import numpy as np
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl

AD = sys.argv[1]
T = Path(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho") / AD
rows = list(csv.DictReader(open(Path(__file__).parent / f"boca_{AD}_v2.csv")))
N = len(rows)
def col(k):
    return np.array([float(r[k]) if r[k] != "" else np.nan for r in rows])
db, dc, abf, abo, dp = col("d_boca"), col("d_ctrl"), col("ab_f"), col("ab_o"), col("d_prev")
def env(p):
    a = cl.ler_audio(p); e = cl.envelope(a, 16000, 30.0, N); return e
pt = env(T / "_audio/demucs/htdemucs/orig/vocals.wav")
if AD in ("ad01", "ad11"):
    es_w = env(T / "narracao_es.wav"); es_j = es_w
    seg = [(s.get("nome") or Path(s["arquivo"]).stem[4:], s["quadro_ini"], s["quadro_fim"]) for s in json.loads((T / "segmentos.json").read_text())["segmentos"]]
else:
    es_w = env(T / "narr_mulher.wav"); es_j = env(T / "narr_jesus.wav")
    seg = [(Path(s["arquivo"]).stem[4:], s["quadro_ini"], s["quadro_fim"]) for s in json.loads((T / "segmentos.json").read_text(encoding="utf-8"))["segmentos"]]

def suav(x, k=3):
    y = x.copy(); m = np.isfinite(x)
    if m.sum() < 5: return y
    xi = np.interp(np.arange(len(x)), np.where(m)[0], x[m])
    return np.convolve(xi, np.ones(k) / k, mode="same")

mud = db > 2 * dc + 1
print(f"{'trecho':6} {'quadros':>11} {'rosto':>5} {'mudou':>5} {'dboca':>5} | corr ES  PT | orig x PT | boca pausa/fala ES")
for nome, a, b in seg:
    b = min(b, N - 1); sl = slice(a, b + 1)
    es = es_j if nome == "j1" else es_w
    rosto = np.isfinite(db[sl]).mean()
    m = np.isfinite(db[sl])
    mu = mud[sl][m].mean() if m.any() else np.nan
    f = suav(abf[sl]); o = suav(abo[sl])
    cE = cl.corr_lag(f, es[sl], 6); cP = cl.corr_lag(f, pt[sl], 6); cO = cl.corr_lag(o, pt[sl], 6)
    thr = np.nanmax(es[sl]) - 35
    fala = es[sl] > thr
    # pausas de >= 8 quadros no ES (miolo, sem as 2 bordas)
    pausa = np.zeros_like(fala)
    run = 0
    for i, v in enumerate(fala):
        if not v: run += 1
        else:
            if run >= 8: pausa[i - run + 2:i - 2] = True
            run = 0
    if run >= 8: pausa[len(fala) - run + 2:len(fala) - 2] = True
    ap = np.nanmean(abf[sl][pausa]) if pausa.any() else np.nan
    af = np.nanmean(abf[sl][fala]) if fala.any() else np.nan
    print(f"{nome:6} {a:5}-{b:5} {rosto:5.0%} {mu:5.0%} {np.nanmedian(db[sl]):5.1f} | {cE[0]:5.2f} {cP[0]:5.2f} | {cO[0]:5.2f}    | {ap:.3f}/{af:.3f} ({pausa.sum()} q pausa)")
    # fim do trecho: quadros congelados
    tail = dp[b - 5:b + 1]
    print(f"        fim: d_prev ultimos 6 quadros {np.round(tail, 2).tolist()}  -> proximo {np.round(dp[b+1:b+3], 2).tolist()}")

# fora dos trechos: rosto + fala ES + boca igual ao original
dentro = np.zeros(N, bool)
for _, a, b in seg: dentro[a:b + 1] = True
fala_all = np.maximum(es_w, es_j) > np.nanmax(es_w) - 35
cand = (~dentro) & np.isfinite(db)
print("\nFora dos trechos de lipsync: quadros com rosto detectado")
i = 0
while i < N:
    if cand[i]:
        j = i
        while j < N and cand[j]: j += 1
        print(f"  {i/30:7.2f}-{j/30:7.2f}s ({j-i} q) fala ES em {fala_all[i:j].mean():.0%} | mudou {mud[i:j][np.isfinite(db[i:j])].mean():.0%} | var abertura orig {np.nanstd(abo[i:j]):.4f}")
        i = j
    else: i += 1
# dentro dos trechos: corridas de >=6 quadros com boca IGUAL ao original durante fala
print("\nDentro dos trechos: corridas >= 6 quadros com boca igual ao original e fala ES")
igual = dentro & np.isfinite(db) & ~mud & fala_all
i = 0
while i < N:
    if igual[i]:
        j = i
        while j < N and igual[j]: j += 1
        if j - i >= 6: print(f"  {i/30:7.2f}-{j/30:7.2f}s ({j-i} q)")
        i = j
    else: i += 1
