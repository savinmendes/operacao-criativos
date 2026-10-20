import sys, csv
import numpy as np
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
N = 3594
def load(p):
    rows = list(csv.DictReader(open(p))); a = np.full(N, np.nan)
    for r in rows:
        q = int(r["q"])
        if q < N and r.get("ab_f"): a[q] = float(r["ab_f"])
    return a
env = lambda p: cl.envelope(cl.ler_audio(p), 16000, 30.0, N)
e2, e1 = env("../narr_mulher.wav"), env("../_v1/narr_mulher.wav")
v2, v1 = load("boca_v2.csv"), load("../../revisao/boca_ad13.csv")
def pausas(f, minq=8, borda=2):
    p = np.zeros_like(f); run = 0
    for i, v in enumerate(list(f) + [True]):
        if not v: run += 1
        else:
            if run >= minq: p[i - run + borda:i - borda] = True
            run = 0
    return p
def met(ab, e, a, b):
    ab, e = ab[a:b], e[a:b]; fes = e > np.nanmax(e) - 30; pes = pausas(fes)
    ok = ~np.isnan(ab); c = np.corrcoef(ab[ok], e[ok])[0, 1]
    idx = np.nanmean(ab[pes]) / np.nanmean(ab[fes]) if pes.any() else np.nan
    return round(c, 2), round(idx, 2), int(ok.sum())
for n, a, b in [("w01",211,455),("w03",692,873),("w04",1003,1307),("w09",2285,2517),("w10",2667,2949),("w10 frase nova 90.9-98.3",2727,2949)]:
    print(f"{n:26} v1 corr/idx {met(v1,e1,a,b)}  v2 corr/idx {met(v2,e2,a,b)}  | v2 boca x audio v1 {met(v2,e1,a,b)}")
# ultimos 30 quadros de w03 e w04 (onde antes congelava)
for n, a, b in [("w03 fim",843,873),("w04 fim",1277,1307)]:
    print(n, "v1", met(v1,e1,a,b), "v2", met(v2,e2,a,b))
print("--- correlacao por atraso (quadros; + = boca atrasada)")
def lagc(ab, e, a, b):
    out = []
    for L in range(-6, 7):
        x = ab[a+L:b+L]; y = e[a:b]; ok = ~np.isnan(x)
        out.append(round(np.corrcoef(x[ok], y[ok])[0,1], 2))
    return out
for n, a, b in [("w03",692,873),("w04",1003,1307),("w09",2285,2517),("w10",2667,2949),("w10 nova",2727,2949)]:
    print(n, "v1", lagc(v1,e1,a+6,b-6)); print(n, "v2", lagc(v2,e2,a+6,b-6))
