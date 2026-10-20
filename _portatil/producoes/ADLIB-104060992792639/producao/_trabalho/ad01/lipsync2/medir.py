# -*- coding: utf-8 -*-
"""Mede o indice de pausa (mesma conta do revisor, revisao/pausas.py) num clipe 720x1280 de um trecho.
Uso: python medir.py clipe.mp4 sNN [quadro_ini_no_clipe=0]
Boca medida = rosto mais baixo (a mulher). ES = narracao_es.wav, PT = demucs vocals do original.
falando = env > max(env do video todo) - 30 dB; pausas >= 8 quadros sem 2 de borda.
indice = abertura media nas pausas ES / abertura media na fala ES."""
import sys, os, json
from pathlib import Path
import numpy as np, cv2
os.environ.setdefault("GLOG_minloglevel", "2")
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
AD = Path(__file__).resolve().parent.parent
NTOT = 3937
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=3))
_env = {}
def env(nome, p):
    if nome not in _env: _env[nome] = cl.envelope(cl.ler_audio(p), 16000, 30.0, NTOT)
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
def aberturas(clip, ini=0, n=None):
    cap = cv2.VideoCapture(str(clip)); out = []; k = 0
    while True:
        ok, f = cap.read()
        if not ok: break
        if k >= ini:
            if f.shape[:2] != (1280, 720): f = cv2.resize(f, (720, 1280))
            x0, y0, L = 240, 200, 480
            rec = np.ascontiguousarray(cv2.cvtColor(f[y0:y0+L, x0:x0+L], cv2.COLOR_BGR2RGB))
            r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rec))
            ps = [np.array([(x0 + p.x * L, y0 + p.y * L) for p in fl]) for fl in r.face_landmarks]
            out.append(cl._abertura(max(ps, key=lambda p: p[13][1])) if ps else np.nan)
            if n and len(out) >= n: break
        k += 1
    return np.array(out)
def medir(abf, q0):
    es = env("es", AD / "narracao_es.wav"); pt = env("pt", AD / "_audio/demucs/htdemucs/orig/vocals.wav")
    sl = slice(q0, q0 + len(abf))
    fes = falando(es, es)[sl]; pes = pausas(fes); ppt = pausas(falando(pt, pt)[sl]) & fes
    mf = np.nanmean(abf[fes])
    iE = np.nanmean(abf[pes]) / mf if pes.any() else np.nan
    iP = np.nanmean(abf[ppt]) / mf if ppt.any() else np.nan
    m = np.isfinite(abf); x = np.interp(np.arange(len(abf)), np.where(m)[0], abf[m])
    x = np.convolve(x, np.ones(3) / 3, mode="same")
    cE = cl.corr_lag(x, es[sl], 6)[0]; cP = cl.corr_lag(x, pt[sl], 6)[0]
    return dict(idxES=iE, idxPT=iP, corrES=cE, corrPT=cP, qpausa=int(pes.sum()), q=len(abf), detect=float(m.mean()),
                sum_pes=float(np.nansum(abf[pes])), n_pes=int(np.isfinite(abf[pes]).sum()),
                sum_fes=float(np.nansum(abf[fes])), n_fes=int(np.isfinite(abf[fes]).sum()))
if __name__ == "__main__":
    seg = {s["nome"]: s for s in json.loads((AD / "segmentos.json").read_text())["segmentos"]}
    clip, nome = sys.argv[1], sys.argv[2]; ini = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    s = seg[nome]; n = s["quadro_fim"] - s["quadro_ini"] + 1
    r = medir(aberturas(clip, ini, n), s["quadro_ini"])
    print(f"{nome} {Path(clip).name}: idxES={r['idxES']:.2f} idxPT={r['idxPT']:.2f} corrES={r['corrES']:.2f} corrPT={r['corrPT']:.2f} pausaq={r['qpausa']} q={r['q']} det={r['detect']:.0%}")
