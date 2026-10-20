# -*- coding: utf-8 -*-
"""Correcao de cor (lote C): escolha_NN.json para o cor.py/brilho.py quando o AD nao passou pelo varrer/analisar
(1 rosto falando por trecho). Detecta o rosto no FINAL (janela em volta de 'perto', ampliada 2x se o rosto e pequeno)
e grava [q, cx, cy, L] com cx, cy = ponto 13 (labio) e L = largura do rosto (234-454), como o varrer.py.
Uso: python escolha_simples.py NN trechos.json   trechos: [[nome, q0, q1, [x, y, lado]], ...] (q do final, 30 fps)"""
import sys, json, os
from pathlib import Path
import numpy as np, cv2
os.environ.setdefault("GLOG_minloglevel", "2")
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
NN = sys.argv[1]; TR = json.load(open(sys.argv[2], encoding="utf-8"))
P = Path(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639")
FIN = next((P / "producao").glob(f"AD {NN} - *-ES-LATAM.mp4"))
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=1))
def detect(f, x0, y0, lado):
    s = max(1.0, 480 / lado); rec = cv2.resize(np.ascontiguousarray(f[y0:y0 + lado, x0:x0 + lado]), None, fx=s, fy=s, interpolation=cv2.INTER_CUBIC)
    r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(cv2.cvtColor(rec, cv2.COLOR_BGR2RGB))))
    return [np.array([(x0 + p.x * rec.shape[1] / s, y0 + p.y * rec.shape[0] / s) for p in fl]) for fl in r.face_landmarks]
cap = cv2.VideoCapture(str(FIN)); q = 0; esc = {n: [a, b, []] for n, a, b, _ in TR}
while True:
    ok, f = cap.read()
    if not ok: break
    for n, a, b, (x, y, lado) in TR:
        if a <= q <= b:
            ps = detect(f, x, y, lado)
            if ps:
                p = ps[0]; esc[n][2].append([q, int(p[13][0]), int(p[13][1]), round(float(np.linalg.norm(p[234] - p[454])), 1)])
    q += 1
json.dump(esc, open(Path(__file__).parent / f"escolha_{NN}.json", "w"))
for n, (a, b, t) in esc.items():
    print(n, a, b, "rosto em", len(t), "de", b - a + 1, "quadros; mediana", np.median(np.array(t)[:, 1:], 0).round(1) if t else None)
