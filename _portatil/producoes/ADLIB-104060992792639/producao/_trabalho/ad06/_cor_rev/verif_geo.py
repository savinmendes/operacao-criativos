# confere que a montagem nova reproduz a antiga (mesma saida do HeyGen, mesmo quadro, mesma elipse): por trecho, compara
# base_lipsync nova x antiga (afim BGR global por quadro tirando a cor) na boca (escolha_06) e no anel fora dela.
import sys, json, cv2, numpy as np
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros
AD = Path(__file__).resolve().parent.parent
esc = json.loads((AD.parent / "revisao" / "loteC" / "escolha_06.json").read_text()); seg = {}
for nm, (a, b, t) in esc.items():
    for j, (q, cx, cy, L) in enumerate(t):
        if j % 8 == 0: seg[int(round(q * 24 / 30))] = (nm, cx, cy, L)
mx = max(seg) + 1; N = quadros(AD / "base_lipsync.mp4", 0, mx); V = quadros(AD / "_antes_cor" / "base_lipsync.mp4", 0, mx); res = {}
for i in range(mx):
    n, v = next(N), next(V)
    if i not in seg: continue
    nm, cx, cy, L = seg[i]; n = n.astype(np.float32); v = v.astype(np.float32)
    A = np.zeros((3, 2))
    for c in range(3): A[c] = np.polyfit(v[::4, ::4, c].ravel(), n[::4, ::4, c].ravel(), 1)
    d = np.abs(n - (v * A[:, 0] + A[:, 1])).mean(-1)
    bx = lambda x0, y0, w, h: d[int(y0):int(y0 + h), int(x0):int(x0 + w)].mean()
    res.setdefault(nm, []).append((bx(cx - 0.3 * L, cy - 0.15 * L, 0.6 * L, 0.5 * L), bx(cx - 0.6 * L, cy - 0.9 * L, 1.2 * L, 0.4 * L)))
print("trecho | dif. media nova x antiga (cor tirada): boca | testa/olhos (fora da elipse)")
for nm, r in res.items(): r = np.array(r); print(f"  {nm:5} {r[:, 0].mean():5.2f} {r[:, 1].mean():5.2f}  (max boca {r[:, 0].max():5.2f})")
