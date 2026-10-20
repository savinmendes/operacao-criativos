"""Rostos por tomada (MediaPipe, 1 quadro a cada 6): caixa do rosto de quem fala e dos outros.
Uso: python rostos.py NN tomadas.json -> rostos.json. tomadas.json: [[nome, q_ini, q_fim, regra], ...]
regra: 'baixo' = rosto com a boca mais baixa (mulher na frente do Jesus); 'esq' = mais à esquerda; 'dir'; 'maior'."""
import sys, json, numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=4,
    min_face_detection_confidence=0.3, min_face_presence_confidence=0.3))
NN = sys.argv[1]; tom = json.load(open(sys.argv[2]))
cap = cv2.VideoCapture(f"../../../../UNICOS_HD/{NN}.mp4")
res = {}
for nome, a, b, regra in tom:
    S, O, B = [], [], []
    for k in range(a, b + 1, 6):
        cap.set(cv2.CAP_PROP_POS_FRAMES, k); ok, f = cap.read()
        r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))))
        ps = [np.array([(p.x * 720, p.y * 1280) for p in fl]) for fl in r.face_landmarks]
        if not ps: continue
        key = {"baixo": lambda p: p[13][1], "esq": lambda p: -p[:, 0].mean(), "dir": lambda p: p[:, 0].mean(),
               "maior": lambda p: np.ptp(p[:, 0])}[regra]
        ps.sort(key=key); s = ps[-1]
        bs = [s[:, 0].min(), s[:, 1].min(), s[:, 0].max(), s[:, 1].max()]
        S.append(bs); B.append([s[13][0], s[13][1]])
        for o in ps[:-1]:
            bo = [o[:, 0].min(), o[:, 1].min(), o[:, 0].max(), o[:, 1].max()]
            ix = max(0, min(bs[2], bo[2]) - max(bs[0], bo[0])) * max(0, min(bs[3], bo[3]) - max(bs[1], bo[1]))
            if ix / ((bo[2]-bo[0]) * (bo[3]-bo[1])) < 0.5: O.append(bo)
    S = np.array(S); O = np.array(O)
    res[nome] = dict(q=[a, b], n=len(S), fala=np.median(S,0).round().tolist() if len(S) else None, fala_uniao=[*np.percentile(S[:, :2],5,0).round().tolist(), *np.percentile(S[:, 2:],95,0).round().tolist()] if len(S) else None,
                     boca=np.array(B).mean(0).round().tolist() if B else None,
                     outros=[*O[:, :2].min(0).round().tolist(), *O[:, 2:].max(0).round().tolist()] if len(O) else None, outros_med=np.median(O,0).round().tolist() if len(O) else None, no=len(O))
    print(nome, res[nome], flush=True)
json.dump(res, open("rostos.json", "w"), indent=1)
