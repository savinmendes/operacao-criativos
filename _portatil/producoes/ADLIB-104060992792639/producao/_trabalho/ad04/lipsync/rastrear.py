# -*- coding: utf-8 -*-
"""Recorte 9:16 que segue o rosto de quem fala (o rosto mais baixo do quadro) num trecho com zoom/movimento.
Caixa = centro do rosto suavizado, largura = K x largura do rosto (suavizada), escalada p/ 720x1280.
Uso: python rastrear.py nome saida.mp4  -> grava boxes_<nome>.json ([x,y,w,h] float por quadro) e o vídeo recortado (sem áudio)."""
import sys, os, json, subprocess
os.environ.setdefault("GLOG_minloglevel", "2")
import numpy as np, cv2
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
AQ = Path(__file__).parent; AD = AQ.parent
cfg = json.loads((AQ/"segs.json").read_text()); FPS = cfg["fps"]
nome, saida = sys.argv[1], sys.argv[2]
s = next(x for x in cfg["segs"] if x["n"] == nome); K = s.get("track", 1.6)
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())),
    running_mode=vision.RunningMode.IMAGE, num_faces=3, min_face_detection_confidence=0.3))
cap = cv2.VideoCapture(str(AD/"base_sem_legenda.mp4")); cap.set(1, s["a"])
fr, C = [], []
for k in range(s["a"], s["b"]):
    ok, f = cap.read(); fr.append(f)
    r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))))
    ps = [np.array([(q.x*720, q.y*1280) for q in fl]) for fl in r.face_landmarks]
    if ps:
        p = max(ps, key=lambda p: p[13][1]); C.append([(p[:,0].min()+p[:,0].max())/2, (p[:,1].min()+p[:,1].max())/2, p[:,0].max()-p[:,0].min()])
    else: C.append([np.nan]*3)
C = np.array(C)
for j in range(3):
    m = np.isfinite(C[:,j]); C[:,j] = np.interp(np.arange(len(C)), np.where(m)[0], C[m,j])
# suaviza (média móvel de 9 quadros, com borda)
ker = np.ones(9)/9
Cs = np.stack([np.convolve(np.pad(C[:,j], 4, mode="edge"), ker, mode="valid") for j in range(3)], 1)
B = []
for cx, cy, fw in Cs:
    w = K*fw*1.6; h = w*16/9
    x = min(max(cx - w/2, 0), 720-w); y = min(max(cy - h*0.45, 0), 1280-h)
    B.append([float(x), float(y), float(w), float(h)])
json.dump(B, open(AQ/f"boxes_{nome}.json", "w"))
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",str(FPS),"-i","-",
    "-c:v","libx264","-crf","12","-preset","slow","-pix_fmt","yuv420p",*COR,saida], stdin=subprocess.PIPE)
for f, (x, y, w, h) in zip(fr, B):
    s_ = 720/w; M = np.float32([[s_, 0, -x*s_], [0, s_, -y*s_]])
    ff.stdin.write(cv2.warpAffine(f, M, (720, 1280), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE).tobytes())
ff.stdin.close(); ff.wait(); print(nome, "caixas", len(B), "largura", round(min(b[2] for b in B)), "-", round(max(b[2] for b in B)))
