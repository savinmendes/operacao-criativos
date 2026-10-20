import sys, os, json
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=3))
seg = json.loads(Path("segmentos.json").read_text())["segmentos"]
cap = cv2.VideoCapture("base_sem_legenda.mp4"); fr = []
while True:
    ok, f = cap.read()
    if not ok: break
    fr.append(f if len(fr) % 10 == 0 else None)
res = {}
for s in seg:
    W, J = [], []
    for k in range(s["quadro_ini"] + (-s["quadro_ini"]) % 10, s["quadro_fim"] + 1, 10):
        f = fr[k]
        if f is None: continue
        rec = np.ascontiguousarray(cv2.cvtColor(f[0:720], cv2.COLOR_BGR2RGB))
        r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rec))
        ps = [np.array([(p.x * 720, p.y * 720) for p in fl]) for fl in r.face_landmarks]
        if not ps: continue
        ps.sort(key=lambda p: p[13][1])
        w = ps[-1]; W.append([w[:,0].min(), w[:,1].min(), w[:,0].max(), w[:,1].max()])
        if len(ps) > 1: j = ps[0]; J.append([j[:,0].min(), j[:,1].min(), j[:,0].max(), j[:,1].max()])
    W, J = np.array(W), np.array(J)
    res[s["nome"]] = dict(w_min=W.min(0).round().tolist(), w_max=W.max(0).round().tolist(),
                          j_xmax=float(J[:,2].max().round()) if len(J) else None, j_ymax=float(J[:,3].max().round()) if len(J) else None, nj=len(J), nw=len(W))
    print(s["nome"], res[s["nome"]])
json.dump(res, open("lipsync2/rostos.json", "w"), indent=1)
