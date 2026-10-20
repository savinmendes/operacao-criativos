# Revisor (lote C): procura padrao de xadrez (pixels alternados) perto da boca de quem fala, final x original.
# Uso: python xadrez.py NN pasta_escolha
import sys, json, cv2, numpy as np
from pathlib import Path
NN, d = sys.argv[1], Path(sys.argv[2])
P = Path(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639")
FIN = next((P / "producao").glob(f"AD {NN} - *-ES-LATAM.mp4")); ORI = P / "UNICOS_HD" / f"{NN}.mp4"
rows = [json.loads(l) for l in open(d / f"faces_{NN}.jsonl")]
K = np.array([[1, -1], [-1, 1]], float)
cf, co = cv2.VideoCapture(str(FIN)), cv2.VideoCapture(str(ORI)); fpo = co.get(cv2.CAP_PROP_FPS); oi = -1; o = None
out = []
for q in range(len(rows)):
    ok, f = cf.read()
    if not ok: break
    want = int(round(q / 30 * fpo))
    while oi < want:
        ok2, o2 = co.read(); oi += 1
        if ok2: o = o2
    best = 0
    for fc in rows[q]["faces"]:
        cx, cy, L = fc["cx"], fc["cy"], fc["L"]; h = int(0.45 * L)
        x0, y0 = max(0, cx - h), max(0, cy - h // 2)
        a = cv2.cvtColor(f[y0:y0 + h + h // 2, x0:x0 + 2 * h], cv2.COLOR_BGR2GRAY).astype(float)
        b = cv2.cvtColor(o[y0:y0 + h + h // 2, x0:x0 + 2 * h], cv2.COLOR_BGR2GRAY).astype(float)
        if a.size < 100 or a.shape != b.shape: continue
        ea = np.abs(cv2.filter2D(a, -1, K)); eb = np.abs(cv2.filter2D(b, -1, K))
        # pior bloco 12x12
        ba = cv2.blur(ea, (12, 12)); bb = cv2.blur(eb, (12, 12))
        r = float(ba.max() - bb[np.unravel_index(ba.argmax(), ba.shape)])
        best = max(best, r)
    out.append(best)
x = np.array(out); thr = 6.0
print(f"AD {NN}: excesso de xadrez (final - original, pior bloco 12x12 perto da boca); limiar {thr}")
q = 0
while q < len(x):
    if x[q] > thr:
        j = q
        while j < len(x) and x[j] > thr * 0.7: j += 1
        if j - q >= 2: print(f"  {q/30:7.2f}-{j/30:7.2f}s ({j-q} q) pico {x[q:j].max():.1f}")
        q = j
    else: q += 1
print("mediana", np.median(x), "p99", np.percentile(x, 99))
