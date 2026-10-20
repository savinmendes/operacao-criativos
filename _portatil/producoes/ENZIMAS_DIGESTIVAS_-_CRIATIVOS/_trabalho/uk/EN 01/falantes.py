# -*- coding: utf-8 -*-
"""Quem fala cada frase: mediapipe em todos os quadros (2 rostos), abertura da boca por lado (esq/dir),
desvio padrao da abertura em cada segmento da transcricao. Grava rostos.json (todas as deteccoes por quadro),
cortes.json (cortes de camera) e falantes.txt.  Uso: python falantes.py <video>"""
import os, sys, json
os.environ.setdefault("GLOG_minloglevel", "2")
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
from pathlib import Path
from comum3 import quadros
AQ = Path(__file__).parent
SRC = sys.argv[1]
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=2,
    min_face_detection_confidence=0.3, min_face_presence_confidence=0.3))
R, C = {}, []; prev = None
for q, f in enumerate(quadros(SRC)):
    if prev is not None:
        d = float(np.abs(f.astype(np.float32) - prev).mean())
        if d > 10: C.append([q, round(d, 1)])
    prev = f.astype(np.float32)
    r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))))
    fs = []
    for fl in r.face_landmarks:
        p = np.array([(t.x * 720, t.y * 1280) for t in fl])
        m = (p[13] + p[14]) / 2; ab = float(np.linalg.norm(p[13] - p[14]))
        fs.append([round(float(v), 1) for v in (p[:, 0].min(), p[:, 1].min(), p[:, 0].max(), p[:, 1].max(), m[0], m[1], ab)])
    R[q] = fs
    if q % 300 == 0: print(q, flush=True)
json.dump(R, open(AQ / "rostos.json", "w")); json.dump(C, open(AQ / "cortes.json", "w"))
N = len(R)
ab = {"esq": np.full(N, np.nan), "dir": np.full(N, np.nan)}
for q, fs in R.items():
    for f in fs:
        lado = "esq" if f[4] < 360 else "dir"; h = f[3] - f[1]
        ab[lado][int(q)] = f[6] / max(h, 1)
T = json.load(open(AQ / "transcricao.json", encoding="utf-8"))
L = []
for s in T:
    a, b = int(s["s"] * 30), int(s["e"] * 30) + 1
    v = {k: np.nanstd(np.diff(x[a:b])) if np.isfinite(x[a:b]).sum() > 3 else float("nan") for k, x in ab.items()}
    quem = "esq" if v["esq"] > v["dir"] else "dir"
    L.append(f"[{s['s']:6.2f}-{s['e']:6.2f}] esq {v['esq']:.4f} dir {v['dir']:.4f} -> {quem} | {s['t'].strip()}")
open(AQ / "falantes.txt", "w", encoding="utf-8").write("\n".join(L)); print("\n".join(L)); print("cortes", C)
