# -*- coding: utf-8 -*-
"""Revisor AD 05: por bloco de lipsync (tempo novo, 30 fps no final): boca mudou?, corr. boca x voz ES do personagem,
corr. x voz PT (vocals do original, remapeada para o tempo novo), indice de pausa ES (meta <= 0,6), pausas ES com
boca aberta, quadros congelados no fim. Fora dos blocos: rostos com fala ES."""
import json, csv, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
T = Path(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad05")
rows = list(csv.DictReader(open(Path(__file__).parent / "boca_ad05.csv"))); N = len(rows)
col = lambda k: np.array([float(r[k]) if r[k] != "" else np.nan for r in rows])
db, dc, abf, abo, dp = col("d_boca"), col("d_ctrl"), col("ab_f"), col("ab_o"), col("d_prev")
env = lambda a: cl.envelope(a, 16000, 30.0, N)
voz = {q: env(cl.ler_audio(T / f"narr_{q}.wav")) for q in ("clara", "marido", "desatadora")}
es_all = env(cl.ler_audio(T / "narracao_es.wav"))
v = cl.ler_audio(T / "_audio/demucs/htdemucs/orig/vocals.wav")
cut0, cutn = int(1286 / 24 * 16000), int(70 / 24 * 16000)
v = np.concatenate([v[:cut0], v[cut0 + cutn:]])
pt = env(v)
BL = [b for b in json.loads((T / "lipsync/blocos.json").read_text(encoding="utf-8")) if b["id"] in
      ["c1", "m1", "c2", "c3", "m3", "m4", "m5", "d1", "d2", "d3", "d4", "d5"]]
def suav(x, k=3):
    m = np.isfinite(x)
    if m.sum() < 5: return x
    xi = np.interp(np.arange(len(x)), np.where(m)[0], x[m]); return np.convolve(xi, np.ones(k) / k, "same")
def pausas(f, minq=8, borda=2):
    p = np.zeros_like(f); run = 0
    for i, vv in enumerate(list(f) + [True]):
        if not vv: run += 1
        else:
            if run >= minq: p[i - run + borda:i - borda] = True
            run = 0
    return p
mud = db > 2 * dc + 1
print(f"{'bloco':5} {'tempo':>13} {'mudou':>5} {'dboca':>5} | corrES corrPT | idx pausa ES (q) | fim d_prev")
tot_p, tot_f = [], []
for b in BL:
    a, e = int(round(b["a"] / 24 * 30)), min(int(round(b["b"] / 24 * 30)) - 1, N - 1); sl = slice(a, e + 1)
    es = voz[b["quem"]]
    m = np.isfinite(db[sl]); mu = mud[sl][m].mean() if m.any() else np.nan
    cE = cl.corr_lag(suav(abf[sl]), es[sl], 6)[0]; cP = cl.corr_lag(suav(abf[sl]), pt[sl], 6)[0]
    fala = es[sl] > np.nanmax(es) - 30; pz = pausas(fala)
    mf = np.nanmean(abf[sl][fala]); mp_ = np.nanmean(abf[sl][pz]) if pz.any() else np.nan
    tot_p += list(abf[sl][pz]); tot_f += list(abf[sl][fala])
    print(f"{b['id']:5} {a/30:6.2f}-{(e+1)/30:6.2f} {mu:5.0%} {np.nanmedian(db[sl]):5.1f} | {cE:6.2f} {cP:6.2f} | {mp_/mf:5.2f} ({pz.sum():3}) | {np.round(dp[e-3:e+1],2).tolist()} -> {np.round(dp[e+1:e+2],2).tolist()}")
    q = 0; f = list(pausas(fala, 9, 1))
    while q < len(f):
        if f[q]:
            j = q
            while j < len(f) and f[j]: j += 1
            mm = np.nanmean(abf[sl][q:j])
            if mm > 0.8 * mf: print(f"        pausa ES {(a+q)/30:.2f}-{(a+j)/30:.2f}s com boca aberta ({mm/mf:.0%} da fala)")
            q = j
        else: q += 1
print(f"TOTAL indice de pausa ES: {np.nanmean(tot_p)/np.nanmean(tot_f):.2f}")
dentro = np.zeros(N, bool)
for b in BL: dentro[int(round(b["a"] / 24 * 30)):int(round(b["b"] / 24 * 30))] = True
blk = [r["bloco"] for r in rows]
fala_all = es_all > np.nanmax(es_all) - 30; fala_pt = pt > np.nanmax(pt) - 30
print("\nFora dos blocos (rosto detectado no original):")
i = 0
while i < N:
    if not dentro[i]:
        j = i
        while j < N and not dentro[j]: j += 1
        rr = np.isfinite(db[i:j]) | (np.array([int(rows[x]["nrostos"]) for x in range(i, j)]) > 0)
        print(f"  {i/30:6.2f}-{j/30:6.2f}s [{blk[i] or '-'}] rostos em {rr.mean():.0%} | fala ES {fala_all[i:j].mean():.0%} | fala PT {fala_pt[i:j].mean():.0%} | var abertura orig {np.nanstd(abo[i:j]) if np.isfinite(abo[i:j]).any() else float('nan'):.4f}")
        i = j
    else: i += 1
