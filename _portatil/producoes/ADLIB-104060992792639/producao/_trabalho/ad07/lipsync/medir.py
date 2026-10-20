# -*- coding: utf-8 -*-
"""Índice de pausa (mesma conta do revisor): abertura média da boca da Desatadora nas pausas da voz ES / na fala ES.
Boca medida = rosto mais à direita (a Desatadora). ES = narracao_es.wav; PT = vocals do demucs.
Uso: python medir.py clipe_full.mp4 qini   (clipe 720x1280 já colado, começando no quadro qini da base)"""
import sys, os
from pathlib import Path
import numpy as np, cv2
os.environ.setdefault("GLOG_minloglevel", "2")
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
from segs import FPS
AD = Path(__file__).resolve().parent.parent
NTOT = 2170
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=3))
_env = {}
def env(nome, p):
    if nome not in _env: _env[nome] = cl.envelope(cl.ler_audio(p), 16000, float(FPS), NTOT)
    return _env[nome]
def falando(e, ref): return e > np.nanmax(ref) - 30
def pausas(f, minq=8, borda=2):
    p = np.zeros_like(f); run = 0
    for i, v in enumerate(list(f) + [True]):
        if not v: run += 1
        else:
            if run >= minq: p[i - run + borda:i - borda] = True
            run = 0
    return p
def abertura_quadro(f):
    x0, y0, L = 200, 250, 520
    rec = np.ascontiguousarray(cv2.cvtColor(f[y0:y0+L, x0:x0+L], cv2.COLOR_BGR2RGB))
    r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rec))
    ps = [np.array([(x0 + p.x * L, y0 + p.y * L) for p in fl]) for fl in r.face_landmarks]
    return cl._abertura(max(ps, key=lambda p: p[1][0])) if ps else np.nan
def aberturas_frames(frames): return np.array([abertura_quadro(f) for f in frames])
def aberturas(clip):
    cap = cv2.VideoCapture(str(clip)); out = []
    while True:
        ok, f = cap.read()
        if not ok: break
        out.append(abertura_quadro(f))
    return np.array(out)
def medir(abf, q0):
    es = env("es", AD / "narracao_es.wav"); pt = env("pt", AD / "_audio/demucs/htdemucs/orig/vocals.wav")
    sl = slice(q0, q0 + len(abf))
    fes = falando(es, es)[sl]; pes = pausas(fes); ppt = pausas(falando(pt, pt)[sl]) & fes
    mf = np.nanmean(abf[fes]) if fes.any() else np.nan
    iE = np.nanmean(abf[pes]) / mf if pes.any() else np.nan
    iP = np.nanmean(abf[ppt]) / mf if ppt.any() else np.nan
    m = np.isfinite(abf)
    x = np.interp(np.arange(len(abf)), np.where(m)[0], abf[m]) if m.any() else np.zeros(len(abf))
    x = np.convolve(x, np.ones(3) / 3, mode="same")
    cE = cl.corr_lag(x, es[sl], 5)[0]; cP = cl.corr_lag(x, pt[sl], 5)[0]
    return dict(idxES=iE, idxPT=iP, corrES=cE, corrPT=cP, qpausa=int(pes.sum()), q=len(abf), detect=float(m.mean()),
                sum_pes=float(np.nansum(abf[pes])), n_pes=int(np.isfinite(abf[pes]).sum()),
                sum_fes=float(np.nansum(abf[fes])), n_fes=int(np.isfinite(abf[fes]).sum()))
if __name__ == "__main__":
    r = medir(aberturas(sys.argv[1]), int(sys.argv[2]))
    print({k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()})
