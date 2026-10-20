# -*- coding: utf-8 -*-
"""Revisor (lote A): folha de zoom na boca, de N em N quadros: FINAL (cima) x ORIGINAL (baixo), barra verde = voz ES
(demucs do final), vermelha = voz PT (demucs do original). Posicao da boca: rosto escolhido em escolha_NN.json
(ou o maior rosto do quadro). Uso: python folha.py NN t0 t1 saida.jpg [passo=3] [por_linha=16]"""
import sys, json
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
sys.argv += []
NN, t0, t1, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
passo = int(sys.argv[5]) if len(sys.argv) > 5 else 3
porl = int(sys.argv[6]) if len(sys.argv) > 6 else 16
D = Path(__file__).parent
import importlib.util
P = Path(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639")
FIN, ORI = next((P / "producao").glob(f"AD {NN} - *-ES-LATAM.mp4")), P / "UNICOS_HD" / f"{NN}.mp4"
rows = [json.loads(l) for l in open(D / f"faces_{NN}.jsonl")]
N = len(rows)
pos = {}
FORCA = tuple(float(v) for v in sys.argv[7].split(',')) if len(sys.argv) > 7 else None
esc = D / f"escolha_{NN}.json"
if esc.exists():
    for k, (a, b, t) in json.loads(esc.read_text()).items():
        for q, cx, cy, L in t: pos[q] = (cx, cy, L)
mapa = (lambda t: t if t * 24 < 1286 else t + 70 / 24) if NN == "05" else (lambda t: t)
es = cl.envelope(cl.ler_audio(D / f"audio/sep/htdemucs/fin_{NN}/vocals.wav"), 16000, 30.0, N)
pt = cl.envelope(cl.ler_audio(D / f"audio/sep/htdemucs/ori_{NN}/vocals.wav"), 16000, 30.0, N)
nrm = lambda e: np.clip((e - (np.nanmax(e) - 40)) / 40, 0, 1)
es, pt = nrm(es), nrm(pt)
a, b = int(round(t0 * 30)), min(int(round(t1 * 30)), N - 1)
cf, co = cv2.VideoCapture(str(FIN)), cv2.VideoCapture(str(ORI))
fpo = co.get(cv2.CAP_PROP_FPS)
cf.set(cv2.CAP_PROP_POS_FRAMES, a)
S = 120; tiles = []; last = None; oi = -1; o = None
for q in range(a, b + 1):
    ok, f = cf.read()
    if not ok: break
    want = int(round(mapa(q / 30) * fpo))
    if oi < 0 or want < oi:
        co.set(cv2.CAP_PROP_POS_FRAMES, want); oi = want - 1
    while oi < want:
        ok2, o2 = co.read(); oi += 1
        if ok2: o = o2
    if FORCA and len(FORCA) > 3:  # trilha linear: t0,x0,y0,t1,x1,y1,...,L
        ks = FORCA[:-1]; ts = ks[0::3]; last = (int(np.interp(q/30, ts, ks[1::3])), int(np.interp(q/30, ts, ks[2::3])), FORCA[-1])
    elif FORCA: last = FORCA
    elif q in pos: last = pos[q]
    elif rows[q]["faces"] and (last is None):
        g = max(rows[q]["faces"], key=lambda z: z["L"]); last = (g["cx"], g["cy"], g["L"])
    if (q - a) % passo: continue
    cx, cy, L = (int(v) for v in last) if last else (360, 640, 400)
    h = int(max(40, 0.45 * L)); x0, y0 = max(0, cx - h), max(0, cy - h)
    crop = lambda img: cv2.resize(img[y0:y0 + 2 * h, x0:x0 + 2 * h], (S, S))
    t = np.full((2 * S + 34, S, 3), 255, np.uint8)
    t[:S] = crop(f); t[S:2 * S] = crop(o)
    t[2 * S + 2:2 * S + 10, :int(S * es[q])] = (0, 160, 0)
    t[2 * S + 12:2 * S + 20, :int(S * pt[q])] = (0, 0, 200)
    if q not in pos: cv2.rectangle(t, (0, 0), (S - 1, 2 * S - 1), (0, 200, 255), 2)
    cv2.putText(t, f"{q/30:.2f}", (2, 2 * S + 32), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
    tiles.append(t)
lin = []
for i in range(0, len(tiles), porl):
    l = tiles[i:i + porl]
    while len(l) < porl: l.append(np.full_like(tiles[0], 255))
    lin.append(np.hstack(l))
cv2.imwrite(out, np.vstack(lin), [cv2.IMWRITE_JPEG_QUALITY, 85])
print("ok", out, len(tiles))
