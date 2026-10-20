# -*- coding: utf-8 -*-
"""Lista rostos (caixas) a cada N quadros: python rostos.py video.mp4 q0 q1 passo"""
import sys, numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=6))
v, q0, q1, passo = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
cap = cv2.VideoCapture(v)
for q in range(q0, q1 + 1, passo):
    cap.set(1, q); ok, f = cap.read()
    if not ok: break
    out = []
    for y0 in (0, 560):   # duas janelas quadradas 720x720 (o detector gosta de quadrado)
        rec = np.ascontiguousarray(cv2.cvtColor(f[y0:y0+720], cv2.COLOR_BGR2RGB))
        r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rec))
        for fl in r.face_landmarks:
            p = np.array([(a.x * 720, a.y * 720 + y0) for a in fl])
            b = (int(p[:,0].min()), int(p[:,1].min()), int(p[:,0].max()), int(p[:,1].max()))
            if not any(abs(b[0]-o[0]) < 20 and abs(b[1]-o[1]) < 20 for o in out):
                out.append(b + (int((p[13,0]+p[14,0])/2), int((p[13,1]+p[14,1])/2)))
    print(q, f"{q/30:.2f}", " ".join(f"[{a},{b},{c},{d} boca {e},{g}]" for a,b,c,d,e,g in sorted(out)), flush=True)
