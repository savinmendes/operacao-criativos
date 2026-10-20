# -*- coding: utf-8 -*-
"""Rastreia o rosto de quem fala (o mais baixo = a Desatadora; o Jesus fica atras/acima), define um recorte 9:16
que acompanha o rosto (suavizado na tomada) e cola a saida do lipsync de volta so na boca/queixo."""
import sys, os, json
os.environ.setdefault("GLOG_minloglevel", "2")
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=3))
def marcos(f):
    r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))))
    ps = [np.array([(p.x * f.shape[1], p.y * f.shape[0]) for p in fl]) for fl in r.face_landmarks]
    return max(ps, key=lambda p: p[13][1]) if ps else None
def caixas(frames, fator=1.75):
    """frames do trecho -> lista de caixas (x,y,w,h) inteiras, 9:16, suavizadas; e landmarks por quadro"""
    P = [marcos(f) for f in frames]
    c = np.array([[np.nan] * 3 if p is None else [p[:, 0].mean(), p[:, 1].mean(), np.linalg.norm(p[234] - p[454])] for p in P])
    for j in range(3):
        m = np.isfinite(c[:, j]); c[:, j] = np.interp(np.arange(len(c)), np.where(m)[0], c[m, j])
    k = min(len(c) // 2 * 2 - 1, 15)
    if k >= 3:
        pad = np.pad(c, ((k // 2, k // 2), (0, 0)), mode="edge")
        c = np.stack([np.convolve(pad[:, j], np.ones(k) / k, mode="valid") for j in range(3)], 1)
    B = []
    for cx, cy, fw in c:
        w = max(240, fator * fw); w = min(w, 720); h = w * 16 / 9
        if h > 1280: h = 1280; w = h * 9 / 16
        x = np.clip(cx - w / 2, 0, 720 - w); y = np.clip(cy - 0.40 * h, 0, 1280 - h)
        B.append((x, y, w, h))
    return B, P
def recortar(f, b, S=(720, 1280)):
    x, y, w, h = b
    M = np.array([[S[0] / w, 0, -x * S[0] / w], [0, S[1] / h, -y * S[1] / h]], np.float32)
    return cv2.warpAffine(f, M, S, flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
def mascara(p):
    lab = (p[13] + p[14]) / 2; queixo = p[152]; nariz = p[2]; fw = np.linalg.norm(p[234] - p[454])
    c = (lab + queixo) / 2 + np.array([0, 0.04 * fw])
    ax = int(0.42 * fw + 6); ay = int(0.62 * np.linalg.norm(queixo - nariz) + 6)
    m = np.zeros((1280, 720), np.float32)
    cv2.ellipse(m, (int(c[0]), int(c[1])), (ax, ay), 0, 0, 360, 1.0, -1)
    return cv2.GaussianBlur(m, (0, 0), max(4, fw * 0.05))[..., None]
def colar(base, g, b, p):
    x, y, w, h = b
    M = np.array([[w / g.shape[1], 0, x], [0, h / g.shape[0], y]], np.float32)
    full = cv2.warpAffine(g, M, (720, 1280), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REPLICATE)
    if p is None: return base
    m = mascara(p)
    return np.clip(full * m + base * (1 - m), 0, 255).astype(np.uint8)
def ler(path, a=0, n=None):
    cap = cv2.VideoCapture(str(path)); cap.set(cv2.CAP_PROP_POS_FRAMES, a); fr = []
    while n is None or len(fr) < n:
        ok, f = cap.read()
        if not ok: break
        fr.append(f)
    return fr
def reamostrar(fr, n):
    m = len(fr)
    if m == n: return fr
    out = []
    for i in range(n):
        x = i * (m - 1) / (n - 1); j = int(np.floor(x)); a = x - j
        out.append(fr[-1] if j >= m - 1 else (fr[j] if a < 1e-3 else cv2.addWeighted(fr[j], 1 - a, fr[j + 1], a, 0)))
    return out
