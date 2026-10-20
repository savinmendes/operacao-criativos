# -*- coding: utf-8 -*-
"""Lote B (revisor): fim do E1, 46,93-47,07 s (q24 1126-1130), a boca abre como no original (PT) numa pausa do ES.
Cola nesses quadros a boca mais fechada de 46,77-46,90 s (q24 1122-1125), alinhada por olhos/nariz, so boca+queixo.
Sem credito. Le _antes_loteB/base_lipsync.mp4 e grava ../base_lipsync.mp4.
Uso: python fechar_e1.py [medir]"""
import sys, subprocess, cv2, numpy as np
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
AQ = Path(__file__).parent; AD = AQ.parent
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=3))
EST = [33, 133, 362, 263, 168, 6, 197, 195, 5, 4, 1, 234, 454, 127, 356]
REF, ALVO = range(1122, 1126), range(1126, 1131)
FACE = (321, 342, 474, 533)   # boxes/E1.json, ultimo quadro
def marcos(f):
    cx, cy = (FACE[0] + FACE[2]) // 2, (FACE[1] + FACE[3]) // 2; L = 420
    x0, y0 = max(0, cx - L // 2), max(0, cy - L // 2)
    rec = np.ascontiguousarray(cv2.cvtColor(f[y0:y0 + L, x0:x0 + L], cv2.COLOR_BGR2RGB))
    r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rec))
    ps = [np.array([(x0 + p.x * rec.shape[1], y0 + p.y * rec.shape[0]) for p in fl]) for fl in r.face_landmarks]
    if not ps: return None
    return min(ps, key=lambda p: np.hypot(*(p[1] - (cx, cy))))
def mascara(p):
    lab = (p[13] + p[14]) / 2; qx = p[152]; nz = p[2]
    c = (lab + qx) / 2 + np.array([0, 0.08 * np.linalg.norm(qx - nz)])
    ax = int(0.62 * np.linalg.norm(p[61] - p[291]) + 18); ay = int(0.62 * np.linalg.norm(qx - nz) + 8)
    m = np.zeros((1280, 720), np.float32); cv2.ellipse(m, (int(c[0]), int(c[1])), (ax, ay), 0, 0, 360, 1.0, -1)
    return cv2.GaussianBlur(m, (0, 0), 7)
src = AD / "_antes_loteB" / "base_lipsync.mp4"
cap = cv2.VideoCapture(str(src)); fr = {}
k = 0
while True:
    ok, f = cap.read()
    if not ok: break
    if 1112 <= k <= 1140: fr[k] = f
    k += 1
NT = k; print("quadros", NT)
P = {k: marcos(fr[k]) for k in range(1112, 1141)}
ab = {k: (cl._abertura(p) if p is not None else np.nan) for k, p in P.items()}
print(" ".join(f"{k}:{ab[k]:.3f}" for k in sorted(ab)))
if len(sys.argv) > 1 and sys.argv[1] == "medir": sys.exit()
r = min(REF, key=lambda k: ab[k] if np.isfinite(ab[k]) else 9); pr = P[r]; ref = fr[r].copy()
print("ref", r, f"{ab[r]:.3f}")
for k in ALVO:
    pk = P[k]
    if pk is None: print("sem rosto", k); continue
    M, _ = cv2.estimateAffinePartial2D(pr[EST].astype(np.float32), pk[EST].astype(np.float32))
    g = cv2.warpAffine(ref, M, (720, 1280), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    ms = mascara(pk)[..., None] * (0.6 if k == 1130 else 1.0)   # 1130 = ataque da fala ES
    fr[k] = np.clip(g * ms + fr[k] * (1 - ms), 0, 255).astype(np.uint8)
# conferência
print("depois", " ".join(f"{k}:{cl._abertura(marcos(fr[k])):.3f}" for k in range(1120, 1134)))
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","24","-i","-",
    "-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",*COR,"-an",str(AD / "base_lipsync.mp4")], stdin=subprocess.PIPE)
cap = cv2.VideoCapture(str(src)); k = 0
while True:
    ok, f = cap.read()
    if not ok: break
    ff.stdin.write((fr[k] if k in fr else f).tobytes()); k += 1
ff.stdin.close(); ff.wait(); print("ok")
