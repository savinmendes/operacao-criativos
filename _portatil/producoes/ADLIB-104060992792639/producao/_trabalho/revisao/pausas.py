# -*- coding: utf-8 -*-
"""Revisor: teste de pausas. Uma boca sincronizada com a voz X fica fechada nas pausas de X.
Para cada trecho de lipsync: abertura media da boca do FINAL nas pausas da voz ES, na fala ES, nas pausas da voz PT
(com ES falando) e o mesmo para a boca do ORIGINAL (referencia de sincronia com PT).
indice_ES = abertura(pausa ES) / abertura(fala ES): < ~0,7 = fecha nas pausas do ES (bom); ~1 ou mais = nao segue.
indice_PT = abertura(pausa PT com ES falando) / abertura(fala ES): baixo = boca fecha onde o PT parava (segue o PT).
Lista tambem cada pausa ES >= 0,3 s em que a boca do final ficou aberta.
Uso: python pausas.py ad01|ad13|ad11"""
import sys, json, csv
from pathlib import Path
import numpy as np
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl

AD = sys.argv[1]
T = Path(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho") / AD
rows = list(csv.DictReader(open(Path(__file__).parent / f"boca_{AD}.csv")))
N = len(rows)
col = lambda k: np.array([float(r[k]) if r[k] != "" else np.nan for r in rows])
abf, abo = col("ab_f"), col("ab_o")
env = lambda p: cl.envelope(cl.ler_audio(p), 16000, 30.0, N)
pt = env(T / "_audio/demucs/htdemucs/orig/vocals.wav")
segs = json.loads((T / "segmentos.json").read_text(encoding="utf-8"))["segmentos"]
nome = lambda s: s.get("nome") or Path(s["arquivo"]).stem[4:]
if AD == "ad13":
    esw, esj = env(T / "narr_mulher.wav"), env(T / "narr_jesus.wav")
else:
    esw = esj = env(T / "narracao_es.wav")

def falando(e):
    return e > np.nanmax(e) - 30

def pausas(f, minq=8, borda=2):
    p = np.zeros_like(f); run = 0
    for i, v in enumerate(list(f) + [True]):
        if not v: run += 1
        else:
            if run >= minq: p[i - run + borda:i - borda] = True
            run = 0
    return p

ptf = falando(pt)
tot = {"f_pes": [], "f_fes": [], "f_ppt": [], "o_pes": [], "o_fes": [], "o_ppt": []}
print(f"{'trecho':6} | FINAL idxES idxPT | ORIGINAL idxES idxPT | q pausaES q pausaPT")
abertas = []
for s in segs:
    a, b = s["quadro_ini"], min(s["quadro_fim"], N - 1); sl = slice(a, b + 1)
    es = esj if nome(s) == "j1" else esw
    fes = falando(es)[sl]; pes = pausas(fes); ppt = pausas(ptf[sl]) & fes
    r = []
    for tag, ab in (("f", abf[sl]), ("o", abo[sl])):
        m_f = np.nanmean(ab[fes]); m_pes = np.nanmean(ab[pes]) if pes.any() else np.nan
        m_ppt = np.nanmean(ab[ppt]) if ppt.any() else np.nan
        r += [m_pes / m_f, m_ppt / m_f]
        tot[tag + "_pes"] += list(ab[pes]); tot[tag + "_fes"] += list(ab[fes]); tot[tag + "_ppt"] += list(ab[ppt])
    print(f"{nome(s):6} | {r[0]:5.2f} {r[1]:5.2f}      | {r[2]:5.2f} {r[3]:5.2f}          | {pes.sum():4} {ppt.sum():4}")
    # pausas ES >= 0,3 s com boca aberta no final
    q = 0; f = list(pausas(fes, 9, 1))
    while q < len(f):
        if f[q]:
            j = q
            while j < len(f) and f[j]: j += 1
            m = np.nanmean(abf[sl][q:j])
            if m > 0.8 * np.nanmean(abf[sl][fes]): abertas.append((nome(s), (a + q) / 30, (a + j) / 30, m / np.nanmean(abf[sl][fes])))
            q = j
        else: q += 1
g = lambda k: np.nanmean(tot[k])
print(f"TOTAL  | {g('f_pes')/g('f_fes'):5.2f} {g('f_ppt')/g('f_fes'):5.2f}      | {g('o_pes')/g('o_fes'):5.2f} {g('o_ppt')/g('o_fes'):5.2f}")
print("\nPausas da voz ES (>= 0,3 s) com a boca do final aberta (>= 80% da abertura media de fala):")
for n, t0, t1, rr in abertas: print(f"  {n}: {t0:.2f}-{t1:.2f}s  abertura {rr:.0%} da fala")
