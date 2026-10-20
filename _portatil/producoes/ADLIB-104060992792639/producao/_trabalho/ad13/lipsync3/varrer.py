# -*- coding: utf-8 -*-
"""Varre os trechos da v3: rostos (mediapipe, ate 3) e cortes de camera (diferenca media > 10) por quadro.
Saida: rostos.json {q: [[x0,y0,x1,y1,mx,my],...]}, cortes.json"""
import os, sys, json
os.environ.setdefault("GLOG_minloglevel", "2")
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
from pathlib import Path
AQ = Path(__file__).parent; AD = AQ.parent
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=3,
    min_face_detection_confidence=0.3, min_face_presence_confidence=0.3))
FAIXAS = [(692, 873), (1003, 1307), (1414, 1794), (1909, 2013), (2285, 2517), (2949, 3480)]
cap = cv2.VideoCapture(str(AD / "base_sem_legenda.mp4"))
R, C = {}, []
for a, b in FAIXAS:
    cap.set(cv2.CAP_PROP_POS_FRAMES, a - 1); ok, prev = cap.read()
    for q in range(a, b):
        ok, f = cap.read()
        d = float(np.abs(f.astype(np.float32) - prev).mean()); prev = f
        if d > 10: C.append([q, round(d, 1)])
        r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))))
        fs = []
        for fl in r.face_landmarks:
            p = np.array([(t.x * 720, t.y * 1280) for t in fl])
            m = (p[13] + p[14]) / 2
            fs.append([round(float(v), 1) for v in (p[:, 0].min(), p[:, 1].min(), p[:, 0].max(), p[:, 1].max(), m[0], m[1])])
        R[q] = fs
    print(a, b, flush=True)
json.dump(R, open(AQ / "rostos.json", "w")); json.dump(C, open(AQ / "cortes.json", "w"))
print("cortes", C)
