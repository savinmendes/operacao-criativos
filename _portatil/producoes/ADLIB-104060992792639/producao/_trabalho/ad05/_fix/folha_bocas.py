"""Folha de checagem v2 do AD 05:
(1) zoom 3x em TODAS as bocas detectadas (MediaPipe, até 4 rostos) em pontos de fala de cada personagem, no vídeo final;
(2) os dois trechos cobertos (6,1-8,2 s e 8,8-11,9 s): quadro inteiro a cada 0,25 s (nenhuma boca falando visível);
(3) zoom 2x na área da antiga legenda (y 900-1150) sem a legenda nova (corpo_ad05.mp4), em 16 pontos.
Saída: _fix/zoom_bocas_v2.jpg, _fix/cobertos_v2.jpg, _fix/zoom_faixa_v2.jpg"""
import json, cv2, numpy as np
from pathlib import Path
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
FIN = "../../AD 05 - ORACION-FAMILIA-ES-LATAM.mp4"
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(Path.home()/".cache/kit-edicao/face_landmarker.task")), num_faces=4,
    min_face_detection_confidence=0.3))
def frame(c, t):
    c.set(cv2.CAP_PROP_POS_MSEC, t*1000); ok, f = c.read(); return f
def rot(img, s, cor=(0,0,255)):
    cv2.putText(img, s, (4,18), 0, 0.5, (0,0,0), 3); cv2.putText(img, s, (4,18), 0, 0.5, cor, 1); return img
c = cv2.VideoCapture(FIN)
# pontos de fala: meio de cada palavra a cada ~1,5 s, pelo alinhamento
al = json.load(open("narracao_es.alinhamento.json", encoding="utf-8"))
ts = []; last = -9
for ch, s in zip(al["characters"], al["character_start_times_seconds"]):
    if ch.strip() and s - last >= 1.5: ts.append(s + 0.08); last = s
tiles = []
for t in ts:
    f = frame(c, t)
    if f is None: continue
    r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(f, cv2.COLOR_BGR2RGB)))
    if not r.face_landmarks:
        tiles.append(rot(cv2.resize(f, (135,240))[0:120].copy() if False else cv2.resize(f,(160,284))[:160], f"{t:.1f} sem rosto", (0,200,255)))
        continue
    for k, lm in enumerate(r.face_landmarks):
        p = np.array([(q.x*720, q.y*1280) for q in lm]); boca = p[[61,291,13,14,0,17]]
        cx, cy = boca[:,0].mean(), boca[:,1].mean(); w = max(40, (p[:,0].max()-p[:,0].min())*0.55)
        x0, y0 = int(max(0,cx-w)), int(max(0,cy-w*0.8)); x1, y1 = int(min(720,cx+w)), int(min(1280,cy+w*0.8))
        z = cv2.resize(f[y0:y1, x0:x1], (160,160), interpolation=cv2.INTER_CUBIC)
        tiles.append(rot(z, f"{t:.1f}s r{k+1}"))
def grade(ims, ncol):
    h = max(i.shape[0] for i in ims); w = max(i.shape[1] for i in ims)
    ims = [cv2.copyMakeBorder(i, 0, h-i.shape[0], 0, w-i.shape[1], cv2.BORDER_CONSTANT) for i in ims]
    while len(ims) % ncol: ims.append(np.zeros_like(ims[0]))
    return np.vstack([np.hstack(ims[k:k+ncol]) for k in range(0, len(ims), ncol)])
cv2.imwrite("_fix/zoom_bocas_v2.jpg", grade(tiles, 10)); print("bocas:", len(ts), "pontos,", len(tiles), "zooms")
cob = [rot(cv2.resize(frame(c, t), (180,320)), f"{t:.2f}") for t in np.arange(5.9, 12.05, 0.25)]
cv2.imwrite("_fix/cobertos_v2.jpg", grade(cob, 9))
cc = cv2.VideoCapture("corpo_ad05.mp4")
fx = [rot(cv2.resize(frame(cc, t)[900:1150], (720,250)), f"{t:.1f}s") for t in np.linspace(1, 94, 16)]
cv2.imwrite("_fix/zoom_faixa_v2.jpg", grade(fx, 2)); print("ok")
