# -*- coding: utf-8 -*-
"""Revisor (lote B): le faces_NN.jsonl, escolhe em cada trecho o rosto de QUEM FALA (a trilha de rosto cuja boca
mais mudou contra o original = o rosto refeito pelo lipsync; com 1 rosto so, ele) e calcula:
- indice de pausa por trecho (conta do kit: fala = pico do trecho - 30 dB na voz ES isolada por demucs do FINAL;
  pausas >= 8 q sem 2 q de borda) e do conjunto;
- "mudou" (boca diferente do original), corr. boca x ES e x PT;
- pausas ES >= 0,3 s com boca aberta;
- fora dos trechos: rostos com fala ES e boca igual a original (candidato a boca em PT).
Uso: python analisar.py NN"""
import sys, json, subprocess
from pathlib import Path
import numpy as np
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl

NN = sys.argv[1]
D = Path(__file__).parent
T = Path(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho")
rows = [json.loads(l) for l in open(D / f"faces_{NN}.jsonl")]
N = len(rows)


def env(p):
    return cl.envelope(cl.ler_audio(p), 16000, 30.0, N)


es = env(D / f"audio/sep/htdemucs/fin_{NN}/vocals.wav")
pt = env(D / f"audio/sep/htdemucs/ori_{NN}/vocals.wav")


def segs():
    """lote B: trechos de lipsync dos relatorios (segundos -> quadros a 30 fps)"""
    j = json.loads((D / "segs_B.json").read_text(encoding="utf-8"))[NN]
    return [(n, int(round(a * 30)), int(round(b * 30)) - 1) for n, a, b in j]


SEG = [(n, a, min(b, N - 1)) for n, a, b in segs() if a < N]


def tracks(a, b):
    """trilhas de rosto no trecho por continuidade da boca"""
    tr = []
    for q in range(a, b + 1):
        for f in rows[q]["faces"]:
            best = None
            for t in tr:
                lq, lf = t[-1]
                if q - lq <= 6 and np.hypot(f["cx"] - lf["cx"], f["cy"] - lf["cy"]) < 0.35 * lf["L"]:
                    if best is None or t[-1][0] > best[-1][0]: best = t
            if best is not None and best[-1][0] != q: best.append((q, f))
            elif best is None: tr.append([(q, f)])
    return [t for t in tr if len(t) >= 0.25 * (b - a + 1) and len(t) >= 10]


def mud(f):
    return ("d_boca" in f) and f["d_boca"] > 2 * f["d_ctrl"] + 1


def serie(t, a, b, key):
    x = np.full(b - a + 1, np.nan)
    for q, f in t:
        if key in f: x[q - a] = f[key]
    return x


def suav(x, k=3):
    m = np.isfinite(x)
    if m.sum() < 5: return x
    xi = np.interp(np.arange(len(x)), np.where(m)[0], x[m])
    return np.convolve(xi, np.ones(k) / k, mode="same")


itens, linhas, abertas, escolha = [], [], [], {}
for nome, a, b in SEG:
    tr = tracks(a, b)
    if not tr:
        linhas.append(f"{nome:9} {a/30:6.2f}-{(b+1)/30:6.2f}s  sem rosto"); continue
    info = []
    for t in tr:
        fr = np.mean([mud(f) for _, f in t])
        info.append((fr, len(t), t))
    # lote B: a mulher que fala fica a direita do Jesus; com 'mudou' empatado (metrica de pixels nao serve), prefere o rosto mais a direita
    info.sort(key=lambda z: (-z[0], -np.median([f['cx'] for _, f in z[2]]), -z[1]))
    fr, n, t = info[0]
    escolha[nome] = (a, b, t)
    ab = serie(t, a, b, "ab_f"); abo = serie(t, a, b, "ab_o")
    e = es[a:b + 1]
    s = cl.somas_pausa(ab, e); idx = cl.indice_agregado([s])
    itens.append(s)
    cE = cl.corr_lag(suav(ab), e, 6)[0]; cP = cl.corr_lag(suav(ab), pt[a:b + 1], 6)[0]
    cx = int(np.median([f["cx"] for _, f in t])); cy = int(np.median([f["cy"] for _, f in t]))
    outros = "; ".join(f"rosto2 ({int(np.median([f['cx'] for _, f in z[2]]))},{int(np.median([f['cy'] for _, f in z[2]]))}) mudou {z[0]:.0%}" for z in info[1:])
    idx_s = f"{idx:.2f}" if idx is not None else "  - "
    ver = cl.classificar_pausa(idx) or "sem pausa"
    if idx is None:
        fl = cl.mascara_fala(e); pc = cl.mascara_pausas(fl, 4, 1); okk = np.isfinite(ab)
        if (pc & okk).sum() >= 3 and (fl & okk).sum() > 10:
            ver += f" (idx pausas>=4q: {np.nanmean(ab[pc & okk]) / np.nanmean(ab[fl & okk]):.2f}, {int((pc & okk).sum())} q)"
    linhas.append(f"{nome:9} {a/30:6.2f}-{(b+1)/30:6.2f}s rosto({cx},{cy}) L{np.median([f['L'] for _, f in t]):.0f} "
                  f"presenca {n/(b-a+1):4.0%} mudou {fr:4.0%} | idx {idx_s} ({s['n_pausa']} q pausa) {ver:9} | corrES {cE:5.2f} PT {cP:5.2f} | {outros}")
    # pausas ES >= 9 q (0,3 s) com boca aberta (>= 80 % da abertura media de fala)
    fala = cl.mascara_fala(e); pa = cl.mascara_pausas(fala, 9, 1)
    mf = np.nanmean(ab[fala]) if np.isfinite(ab[fala]).any() else np.nan
    q = 0
    while q < len(pa):
        if pa[q]:
            j = q
            while j < len(pa) and pa[j]: j += 1
            m = np.nanmean(ab[q:j]) if np.isfinite(ab[q:j]).any() else np.nan
            if m > 0.8 * mf: abertas.append(f"  {nome}: {(a+q)/30:.2f}-{(a+j)/30:.2f}s abertura {m/mf:.0%} da fala")
            q = j
        else: q += 1

print(f"AD {NN}: {N} quadros")
print("\n".join(linhas))
tot = cl.indice_agregado(itens)
print(f"CONJUNTO: indice de pausa {tot:.2f}" if tot is not None else "CONJUNTO: -")
print("\nPausas ES >= 0,3 s com boca aberta (>= 80% da fala):")
print("\n".join(abertas) or "  nenhuma")

# fora dos trechos / boca igual ao original com fala
dentro = np.zeros(N, bool)
for _, a, b in SEG: dentro[a:b + 1] = True
falaG = es > np.nanmax(es) - 30
ptG = pt > np.nanmax(pt) - 30
print("\nQuadros com rosto (L>=60) e boca IGUAL ao original enquanto o PT original falava (candidatos a boca em PT), corridas >= 3 q:")
cand = np.zeros(N, bool); info_q = {}
for q in range(N):
    for f in rows[q]["faces"]:
        if f["L"] >= 60 and "d_boca" in f and not mud(f) and ptG[q]:
            cand[q] = True; info_q[q] = f
q = 0; achou = False
while q < N:
    if cand[q]:
        j = q
        while j < N and cand[j]: j += 1
        abv0 = [info_q[k].get("ab_o", np.nan) for k in range(q, j)]
        if j - q >= 3 and np.nanstd(abv0) > 0.008:
            achou = True
            abv = [info_q[k].get("ab_o", np.nan) for k in range(q, j)]
            print(f"  {q/30:7.2f}-{j/30:7.2f}s ({j-q} q) dentro_trecho {dentro[q:j].mean():.0%} fala_ES {falaG[q:j].mean():.0%} "
                  f"rosto ({info_q[q]['cx']},{info_q[q]['cy']}) L{info_q[q]['L']:.0f} var.abertura_orig {np.nanstd(abv):.3f}")
        q = j
    else: q += 1
if not achou: print("  nenhuma")
print("\nFora dos trechos de lipsync: corridas com rosto e fala ES:")
q = 0
while q < N:
    c = (not dentro[q]) and len(rows[q]["faces"]) > 0
    if c:
        j = q
        while j < N and (not dentro[j]) and rows[j]["faces"]: j += 1
        print(f"  {q/30:7.2f}-{j/30:7.2f}s ({j-q} q) fala ES {falaG[q:j].mean():.0%} rostos {max(len(rows[k]['faces']) for k in range(q,j))}")
        q = j
    else: q += 1
print("\nDentro dos trechos: corridas >= 6 q com a boca de QUEM FALA igual ao original durante fala ES:")
for nome, (a, b, t) in escolha.items():
    m = np.zeros(b - a + 1, bool)
    for q, f in t:
        if "d_boca" in f and not mud(f) and falaG[q]: m[q - a] = True
    i = 0
    while i < len(m):
        if m[i]:
            j = i
            while j < len(m) and m[j]: j += 1
            if j - i >= 6: print(f"  {nome}: {(a+i)/30:.2f}-{(a+j)/30:.2f}s ({j-i} q)")
            i = j
        else: i += 1
json.dump({k: [a, b, [[q, f["cx"], f["cy"], f["L"]] for q, f in t]] for k, (a, b, t) in escolha.items()},
          open(D / f"escolha_{NN}.json", "w"))
