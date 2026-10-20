# -*- coding: utf-8 -*-
"""Rostos (mediapipe) e cortes de camera por quadro nas faixas dos trechos. Saida rostos.json, cortes.json"""
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
SRC = AQ.parent.parent.parent / "INGLES" / "EN 04 - ENZIMAS-BARRIGA-POS-RESTAURANTE.mp4"
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=2,
    min_face_detection_confidence=0.3, min_face_presence_confidence=0.3))
FAIXAS = [(940, 1081)]
R, C = {}, []
for a, b in FAIXAS:
    prev = None
    for k, f in enumerate(quadros(SRC, a - 1, b - a + 1)):
        q = a - 1 + k
        if prev is not None:
            d = float(np.abs(f.astype(np.float32) - prev).mean())
            if d > 10: C.append([q, round(d, 1)])
        prev = f.astype(np.float32)
        r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))))
        fs = []
        for fl in r.face_landmarks:
            p = np.array([(t.x * 720, t.y * 1280) for t in fl])
            m = (p[13] + p[14]) / 2
            ab = float(np.linalg.norm(p[13] - p[14]))
            fs.append([round(float(v), 1) for v in (p[:, 0].min(), p[:, 1].min(), p[:, 0].max(), p[:, 1].max(), m[0], m[1], ab)])
        R[q] = fs
    print(a, b, flush=True)
json.dump(R, open(AQ / "rostos.json", "w")); json.dump(C, open(AQ / "cortes.json", "w"))
print("cortes", C)
