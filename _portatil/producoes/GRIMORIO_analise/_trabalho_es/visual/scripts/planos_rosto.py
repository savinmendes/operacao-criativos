# -*- coding: utf-8 -*-
"""Planos com rosto (para o lip sync): cortes de cena (dif. média 90x160 > 12) + Face Landmarker (MediaPipe) a cada 3 quadros
no quadro inteiro e em janelas. Saída: _tmp/planos_raw.json com caixas por plano."""
import os, sys, json, subprocess, numpy as np, cv2
os.environ.setdefault("GLOG_minloglevel", "2")
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
from pathlib import Path
MOD = Path.home() / ".cache" / "kit-edicao" / "face_landmarker.task"
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=str(MOD)),
      running_mode=vision.RunningMode.IMAGE, num_faces=4))
V = r"C:\Users\PICHAU\Downloads\GRIMORIO V2.mp4"
JAN = [(0, 0, 720, 1280), (0, 0, 720, 720), (0, 560, 720, 720), (0, 280, 720, 720), (0, 0, 480, 480), (240, 0, 480, 480),
       (0, 400, 480, 480), (240, 400, 480, 480), (0, 800, 480, 480), (240, 800, 480, 480)]
def rostos(f):
    out = []
    for x0, y0, w, h in JAN:
        rec = np.ascontiguousarray(cv2.cvtColor(f[y0:y0 + h, x0:x0 + w], cv2.COLOR_BGR2RGB))
        r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rec))
        for lm in (r.face_landmarks or []):
            p = np.array([(x0 + q.x * w, y0 + q.y * h) for q in lm])
            b = [p[:, 0].min(), p[:, 1].min(), p[:, 0].max(), p[:, 1].max()]
            if b[2] - b[0] < 40: continue
            if any(abs((b[0] + b[2]) / 2 - (c[0] + c[2]) / 2) < 40 and abs((b[1] + b[3]) / 2 - (c[1] + c[3]) / 2) < 40 for c in out): continue
            out.append([round(v) for v in b])
    return out
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", V, "-vf", "scale=in_color_matrix=bt709:in_range=full,format=bgr24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
T = 720 * 1280 * 3; prev = None; cortes = [0]; F = {}; i = 0
while True:
    b = p.stdout.read(T)
    if len(b) < T: break
    f = np.frombuffer(b, np.uint8).reshape(1280, 720, 3)
    g = cv2.resize(f, (90, 160)).astype(np.float32)
    if prev is not None and np.abs(g - prev).mean() > 12: cortes.append(i)
    prev = g
    if i % 3 == 0: F[i] = rostos(f)
    if i % 600 == 0: print(i, flush=True)
    i += 1
json.dump({"cortes": cortes, "n": i, "rostos": F}, open(sys.argv[1], "w"))
print("ok")
