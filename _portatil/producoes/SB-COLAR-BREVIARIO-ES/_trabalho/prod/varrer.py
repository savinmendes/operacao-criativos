import os, sys, json
os.environ.setdefault("GLOG_minloglevel", "2")
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=3,
    min_face_detection_confidence=0.3, min_face_presence_confidence=0.3))
cap = cv2.VideoCapture(r"../../original_wsen5drS7Nk.mp4"); R = []; q = 0
while True:
    ok, f = cap.read()
    if not ok: break
    s = cv2.resize(f, (540, 960))
    r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(cv2.cvtColor(s, cv2.COLOR_BGR2RGB))))
    fs = []
    for fl in r.face_landmarks:
        p = np.array([(t.x * 1080, t.y * 1920) for t in fl]); m = (p[13] + p[14]) / 2
        ab = float(np.linalg.norm(p[13]-p[14]))
        fs.append([round(float(v), 1) for v in (p[:, 0].min(), p[:, 1].min(), p[:, 0].max(), p[:, 1].max(), m[0], m[1], ab)])
    R.append(fs); q += 1
    if q % 500 == 0: print(q, flush=True)
json.dump(R, open("rostos.json", "w")); print("ok", q)
