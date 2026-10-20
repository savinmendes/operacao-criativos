# -*- coding: utf-8 -*-
"""Plano B sem credito (adaptado do ad01/lipsync2/fechar.py para a saida RECORTADA do HeyGen, 1 rosto):
nas pausas da voz ES >= MINQ quadros, cola a boca mais fechada do proprio trecho (alinhada por olhos/nariz),
so boca+queixo, com rampa de 3 quadros. Uso: python fechar3.py entrada.mp4 es.mp3 saida.mp4 fps [cortes_locais q1,q2,...] [so_de_q:ate_q]
v3 AD 13: a boca de referencia so vem da MESMA tomada (cortes_locais) e a pausa e cortada nos cortes."""
import sys, subprocess, cv2, numpy as np
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=3))
MINQ, RAMPA = 6, 3
EST = [33, 133, 362, 263, 168, 6, 197, 195, 5, 4, 1, 234, 454, 127, 356]
ent, es, sai = sys.argv[1], sys.argv[2], sys.argv[3]; fps = float(sys.argv[4]) if len(sys.argv) > 4 else 24
CUT = sorted(int(c) for c in sys.argv[5].split(',') if c) if len(sys.argv) > 5 and sys.argv[5] not in ('-', '') else []
JAN = tuple(map(int, sys.argv[6].split(':'))) if len(sys.argv) > 6 and sys.argv[6] != '-' else None
ESQ = len(sys.argv) > 7 and sys.argv[7] == 'esq'   # rosto mais a esquerda (a mulher) em vez do maior
def tomada(k): return sum(1 for c in CUT if c <= k)
from comum3 import ler as _ler, ENC_VF, ENC_TAG
fr = _ler(ent)
n = len(fr); H, W = fr[0].shape[:2]
def marcos(f):
    r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))))
    ps = [np.array([(p.x * W, p.y * H) for p in fl]) for fl in r.face_landmarks]
    if ESQ: return min(ps, key=lambda p: p[:, 0].mean()) if ps else None
    return max(ps, key=lambda p: np.ptp(p[:, 0])) if ps else None
x = cl.ler_audio(es); env = cl.envelope(x, 16000, fps, n); fal = cl.mascara_fala(env)
runs, k = [], 0
while k < n:
    if not fal[k]:
        j = k
        while j < n and not fal[j]: j += 1
        pts = [k] + [c for c in CUT if k < c < j] + [j]
        for u, v in zip(pts[:-1], pts[1:]):
            if v - u >= MINQ and (JAN is None or (v > JAN[0] and u < JAN[1])): runs.append((u, v))
        k = j
    else: k += 1
P = [marcos(f) for f in fr]; ab = np.array([cl._abertura(p) if p is not None else np.nan for p in P])
orig = [f.copy() for f in fr]
def mascara(p):
    lab = (p[13] + p[14]) / 2; qx = p[152]; nz = p[2]
    c = (lab + qx) / 2 + np.array([0, 0.08 * np.linalg.norm(qx - nz)])
    ax = int(0.62 * np.linalg.norm(p[61] - p[291]) + 18); ay = int(0.62 * np.linalg.norm(qx - nz) + 8)
    m = np.zeros((H, W), np.float32); cv2.ellipse(m, (int(c[0]), int(c[1])), (ax, ay), 0, 0, 360, 1.0, -1)
    return cv2.GaussianBlur(m, (0, 0), 9)
for a, b in runs:
    viz = [k for k in range(max(0, a - 60), min(n, b + 60)) if np.isfinite(ab[k]) and tomada(k) == tomada(a)]
    if not viz: continue
    r = min(viz, key=lambda k: ab[k]); pr = P[r]
    for k in range(a, b):
        w = min(1.0, (k - a + 1) / RAMPA, (b - k) / RAMPA); pk = P[k]
        if pk is None: continue
        M, _ = cv2.estimateAffinePartial2D(pr[EST].astype(np.float32), pk[EST].astype(np.float32))
        if M is None: continue
        g = cv2.warpAffine(orig[r], M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        ms = mascara(pk)[..., None] * w
        fr[k] = np.clip(g * ms + fr[k] * (1 - ms), 0, 255).astype(np.uint8)
    print(f"pausa q{a}-{b} ref q{r} ab={ab[r]:.3f} (antes media {np.nanmean(ab[a:b]):.3f})")
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r",str(fps),"-i","-","-i",es,
    "-map","0:v","-map","1:a","-frames:v",str(len(fr)),*ENC_VF,"-c:v","libx264","-crf","13","-pix_fmt","yuv420p",*ENC_TAG,"-c:a","aac",sai], stdin=subprocess.PIPE)
for f in fr: ff.stdin.write(f.tobytes())
ff.stdin.close(); ff.wait(); print("ok", sai, len(runs), "pausas")
