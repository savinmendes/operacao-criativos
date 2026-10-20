# -*- coding: utf-8 -*-
"""fechar_crop.py (ad17/ad18) em memoria: recebe a lista de quadros BGR e devolve a lista corrigida (sem gravar arquivo,
para nao somar passada de cor). Mesma logica: nas pausas da voz ES >= 6 q, cola a boca mais fechada do proprio trecho."""
import sys, cv2, numpy as np
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
MINQ, RAMPA = 6, 3
EST = [33, 133, 362, 263, 168, 6, 197, 195, 5, 4, 1, 234, 454, 127, 356]
_det = None
def fechar(fr, es, fps):
    global _det
    if _det is None:
        _det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
            base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=3))
    fr = [f.copy() for f in fr]; n = len(fr); H, W = fr[0].shape[:2]
    def marcos(f):
        r = _det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))))
        ps = [np.array([(p.x * W, p.y * H) for p in fl]) for fl in r.face_landmarks]
        return max(ps, key=lambda p: np.ptp(p[:, 0])) if ps else None
    x = cl.ler_audio(str(es)); env = cl.envelope(x, 16000, fps, n); fal = cl.mascara_fala(env)
    runs, k = [], 0
    while k < n:
        if not fal[k]:
            j = k
            while j < n and not fal[j]: j += 1
            if j - k >= MINQ: runs.append((k, j))
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
        viz = [k for k in range(max(0, a - 45), min(n, b + 45)) if np.isfinite(ab[k])]
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
        print(f"  fechar: pausa q{a}-{b} ref q{r} ab={ab[r]:.3f} (antes media {np.nanmean(ab[a:b]):.3f})", flush=True)
    return fr
