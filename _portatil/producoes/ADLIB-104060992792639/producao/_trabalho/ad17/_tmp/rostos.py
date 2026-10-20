import sys, json, numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=5,
    min_face_detection_confidence=0.3))
Y0 = int(sys.argv[5]) if len(sys.argv) > 5 else 0
src, cortes, passo = sys.argv[1], [int(x) for x in sys.argv[2].split(",")], int(sys.argv[3])
cap = cv2.VideoCapture(src); i = 0; res = {}
shot = 0
while True:
    ok, f = cap.read()
    if not ok or i >= cortes[-1]: break
    while shot + 1 < len(cortes) and i >= cortes[shot + 1]: shot += 1
    if (i - cortes[shot]) % passo == 0:
        rgb = np.ascontiguousarray(cv2.cvtColor(cv2.resize(f[Y0:Y0+720], (1440, 1440)), cv2.COLOR_BGR2RGB))
        r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))
        fs = []
        for fl in r.face_landmarks:
            p = np.array([(q.x * 720, Y0 + q.y * 720) for q in fl])
            fs.append([int(p[:, 0].min()), int(p[:, 1].min()), int(p[:, 0].max()), int(p[:, 1].max()), int(p[13][0]), int(p[13][1])])
        res.setdefault(shot, []).append((i, sorted(fs)))
    i += 1
for s, L in res.items():
    print(f"shot {s} [{cortes[s]},{cortes[s+1]})")
    for i, fs in L[:: max(1, len(L) // 4)]: print("  ", i, fs)
json.dump({str(k): v for k, v in res.items()}, open(sys.argv[4], "w"))
