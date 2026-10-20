# -*- coding: utf-8 -*-
"""Folha de emendas: para cada tempo, 10 quadros seguidos (de -5 a +4) do FINAL: quadro inteiro reduzido (cima) e
zoom na boca de quem fala (baixo). Uso: python emendas.py NN saida.jpg t1 t2 ..."""
import sys, json
from pathlib import Path
import numpy as np, cv2
NN, out = sys.argv[1], sys.argv[2]
ts = [float(x) for x in sys.argv[3:]]
D = Path(__file__).parent
P = Path(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639")
FIN = next((P / "producao").glob(f"AD {NN} - *-ES-LATAM.mp4"))
pos = {}
esc = D / f"escolha_{NN}.json"
if esc.exists():
    for k, (a, b, t) in json.loads(esc.read_text()).items():
        for q, cx, cy, L in t: pos[q] = (cx, cy, L)
rows = [json.loads(l) for l in open(D / f"faces_{NN}.jsonl")]
cap = cv2.VideoCapture(str(FIN))
FR = {}
alvo = set(q for t in ts for q in range(int(round(t * 30)) - 5, int(round(t * 30)) + 5))
k = 0
while k <= max(alvo):
    ok, f = cap.read()
    if not ok: break
    if k in alvo: FR[k] = f
    k += 1
linhas = []
for t in ts:
    c = int(round(t * 30)); tiles = []
    for q in range(c - 5, c + 5):
        if q not in FR: break
        f = FR[q]
        if q in pos: cx, cy, L = pos[q]
        elif rows[q]["faces"]:
            g = max(rows[q]["faces"], key=lambda z: z["L"]); cx, cy, L = g["cx"], g["cy"], g["L"]
        else: cx, cy, L = 360, 500, 300
        h = int(max(40, 0.5 * L)); x0, y0 = max(0, cx - h), max(0, cy - h)
        z = cv2.resize(f[y0:y0 + 2 * h, x0:x0 + 2 * h], (140, 140))
        s = cv2.resize(f, (140, 249))
        tile = np.vstack([s, z, np.full((22, 140, 3), 255, np.uint8)])
        cv2.putText(tile, f"{q/30:.2f}", (3, 249 + 140 + 16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)
        if q == c: cv2.rectangle(tile, (0, 0), (139, 249 + 139), (0, 0, 255), 2)
        tiles.append(tile)
    linhas.append(np.hstack(tiles))
cv2.imwrite(out, np.vstack(linhas), [cv2.IMWRITE_JPEG_QUALITY, 82])
print("ok", out)
