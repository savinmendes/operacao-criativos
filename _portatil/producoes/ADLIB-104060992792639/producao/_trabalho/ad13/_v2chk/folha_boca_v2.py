# zoom na boca: linha 1 = v2 final, linha 2 = v1 final; barra verde = voz ES v2, azul = voz ES v1. Uso: t0 t1 passo saida
import sys, csv, numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
t0, t1, passo, out = float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
N = 3594
rows = {int(r["q"]): r for r in csv.DictReader(open("boca_v2.csv")) if r.get("cx")}
nrm = lambda e: np.clip((e - (np.nanmax(e) - 40)) / 40, 0, 1)
e2 = nrm(cl.envelope(cl.ler_audio("../narr_mulher.wav"), 16000, 30.0, N)); e1 = nrm(cl.envelope(cl.ler_audio("../_v1/narr_mulher.wav"), 16000, 30.0, N))
def frames(p, a, b):
    c = cv2.VideoCapture(p); c.set(cv2.CAP_PROP_POS_FRAMES, a); o = []
    for _ in range(a, b): o.append(c.read()[1])
    return o
a, b = int(t0*30), int(t1*30)
F2 = frames(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\AD 13 - ORACION-PAZ-ES-LATAM.mp4", a, b)
F1 = frames("../_v1/AD13_v1.mp4", a, b)
S = 110; tiles = []
for i in range(a, b, passo):
    r = rows.get(i)
    if r is None: continue
    cx, cy, L = int(r["cx"]), int(r["cy"]), float(r["larg"]); h = int(L*0.45)
    def crop(f):
        y0, x0 = max(0, cy-h), max(0, cx-h); return cv2.resize(f[y0:cy+h, x0:cx+h], (S, S))
    lab = np.full((26, S, 3), 255, np.uint8)
    cv2.rectangle(lab, (0, 0), (int(S*e2[i]), 6), (0, 170, 0), -1); cv2.rectangle(lab, (0, 8), (int(S*e1[i]), 13), (200, 80, 0), -1)
    cv2.putText(lab, f"{i/30:.2f}", (2, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
    tiles.append(np.vstack([crop(F2[i-a]), crop(F1[i-a]), lab]))
per = 16; rows_img = []
for k in range(0, len(tiles), per):
    t = tiles[k:k+per]; t += [np.full_like(tiles[0], 255)] * (per - len(t)); rows_img.append(np.hstack(t))
cv2.imwrite(out, np.vstack(rows_img)); print(out, len(tiles))
