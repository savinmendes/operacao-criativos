import json, numpy as np
R = json.load(open("rostos.json")); C = json.load(open("cortes.json")); P = json.load(open("plano_fala.json"))
J = [(0,21.37,'m'),(23.4,27.2,'m'),(31.6,36.55,'m'),(39.7,43.25,'m'),(43.97,45.33,'m'),(47.77,53.43,'m'),(58.17,64.1,'m'),(68.3,79.97,'m'),(83.17,84.43,'m'),(92.2,93.77,'m'),(98.85,109.13,'m'),(111.17,116.47,'m'),(116.63,119.2,'p'),(121.83,135.2,'p'),(137.23,139.17,'p')]
dif = {q: d for q, t, d in C}
def main(fs): return max(fs, key=lambda f: f[2]-f[0]) if fs else None
# fala ES (intervalos) e pausas entre segmentos
fala = [(p["ini"], p["fim"]) for p in P]
def em_fala(t): return any(a - 0.05 <= t <= b + 0.05 for a, b in fala)
out = []
for a, b, quem in J:
    qa, qb = int(round(a*30)), min(int(round(b*30)), len(R))
    runs = []; cur = []; prev = None
    for i in range(qa, qb):
        f = main(R[i])
        corte = dif.get(i, 0) > 25 or f is None or (prev is not None and np.hypot(f[4]-prev[4], f[5]-prev[5]) > 40)
        if corte:
            if cur: runs.append(cur); cur = []
            if f is not None and dif.get(i, 0) <= 25: cur = [i]
        else: cur.append(i)
        prev = f
    if cur: runs.append(cur)
    for r in runs:
        if len(r) < 6: continue
        s, e = r[0], r[-1] + 1
        # divide > 12 s em pausas da fala
        while (e - s) > 360:
            alvo = s + (e - s) // 2 if (e - s) < 720 else s + 330
            cands = [q for q in range(s + 90, min(e - 90, s + 360)) if not em_fala(q / 30)]
            k = min(cands, key=lambda q: abs(q - alvo)) if cands else s + 330
            out.append([quem, s, k]); s = k
        out.append([quem, s, e])
tot = 0
for k, (quem, s, e) in enumerate(out):
    fl = sum(1 for q in range(s, e) if em_fala(q/30))
    pad = max(e - s, 92); tot += pad
    print(f"{quem}{k+1:02d} {s:5d}-{e:5d} {s/30:6.2f}-{e/30:6.2f} dur {(e-s)/30:5.2f} fala_es {fl/30:4.1f}")
print("total s (com padding 3s):", round(tot/30, 1))
json.dump([dict(nome=f"{q}{k+1:02d}", quem=q, a=s, b=e) for k, (q, s, e) in enumerate(out)], open("chunks.json", "w"), indent=0)
