# Revisor (lote C): deslocamento de cor (V = vermelho, U = azul; YUV) final - original na area colada (labio sup + queixo)
# e na face fora dela (bochechas altas), por trecho. Uso: python cor.py NN pasta [passo]
import sys, json, cv2, numpy as np
from pathlib import Path
NN, d = sys.argv[1], Path(sys.argv[2]); passo = int(sys.argv[3]) if len(sys.argv) > 3 else 6
P = Path(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639")
FIN = next((P / "producao").glob(f"AD {NN} - *-ES-LATAM.mp4")); ORI = P / "UNICOS_HD" / f"{NN}.mp4"
esc = json.loads((d / f"escolha_{NN}.json").read_text()); pos = {}
for k, (a, b, t) in esc.items():
    for q, cx, cy, L in t: pos[q] = (k, cx, cy, L)
cf, co = cv2.VideoCapture(str(FIN)), cv2.VideoCapture(str(ORI)); fpo = co.get(cv2.CAP_PROP_FPS)
res = {}; oi = -1; o = None; q = 0
def bx(im, cx, cy, w, h): x0, y0 = int(max(0, cx - w / 2)), int(max(0, cy - h / 2)); return im[y0:int(y0 + h), x0:int(x0 + w)].reshape(-1, 3).mean(0)
while True:
    ok, f = cf.read()
    if not ok: break
    want = int(round(q / 30 * fpo))
    while oi < want:
        ok2, o2 = co.read(); oi += 1
        if ok2: o = o2
    if q in pos and q % passo == 0:
        k, cx, cy, L = pos[q]; F = cv2.cvtColor(f, cv2.COLOR_BGR2YUV).astype(float); O = cv2.cvtColor(o, cv2.COLOR_BGR2YUV).astype(float)
        dd = lambda *a: bx(F, *a) - bx(O, *a)
        boca = (dd(cx, cy - 0.17 * L, 0.30 * L, 0.08 * L) + dd(cx, cy + 0.30 * L, 0.30 * L, 0.12 * L)) / 2
        face = (dd(cx - 0.33 * L, cy - 0.55 * L, 0.14 * L, 0.14 * L) + dd(cx + 0.33 * L, cy - 0.55 * L, 0.14 * L, 0.14 * L)) / 2
        res.setdefault(k, []).append(np.r_[boca, face])
    q += 1
print(f"AD {NN}: final - original | boca Y U V | face Y U V | degrau boca-face Y V")
allr = []
for k in esc:
    if k not in res: continue
    r = np.median(np.array(res[k]), 0); allr += res[k]
    print(f"{k:9} boca {r[0]:+5.1f} {r[1]:+5.1f} {r[2]:+5.1f} | face {r[3]:+5.1f} {r[4]:+5.1f} {r[5]:+5.1f} | degrau Y {r[0]-r[3]:+5.1f} V {r[2]-r[5]:+5.1f}")
r = np.median(np.array(allr), 0); print(f"TODOS     boca {r[0]:+5.1f} {r[1]:+5.1f} {r[2]:+5.1f} | face {r[3]:+5.1f} {r[4]:+5.1f} {r[5]:+5.1f} | degrau Y {r[0]-r[3]:+5.1f} V {r[2]-r[5]:+5.1f}")
