# -*- coding: utf-8 -*-
"""Fecha a boca nas pausas da voz ES. O HeyGen (precision) devolve a boca do video de entrada quando o audio novo
esta em silencio, e nesse plano a boca original esta falando PT (aberta/sorrindo) justamente nas pausas do ES.
Para cada pausa ES >= MINQ quadros: pega o quadro do proprio lipsync (mesmo trecho, perto da pausa) com a boca mais
fechada, alinha esse quadro ao rosto atual por pontos estaveis (olhos/nariz, similaridade) e cola so a regiao
boca+queixo com borda suave, entrando/saindo em rampa de 3 quadros."""
import cv2, numpy as np
from pathlib import Path
import medir as Me
import mediapipe as mp
AD = Path(__file__).resolve().parent.parent
MINQ, RAMPA = 6, 3
ESTAVEIS = [33, 133, 362, 263, 168, 6, 197, 195, 5, 4, 1, 234, 454, 127, 356]
def marcos(f):
    x0, y0, L = 240, 200, 480
    rec = np.ascontiguousarray(cv2.cvtColor(f[y0:y0+L, x0:x0+L], cv2.COLOR_BGR2RGB))
    r = Me.det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rec))
    ps = [np.array([(x0 + p.x * L, y0 + p.y * L) for p in fl]) for fl in r.face_landmarks]
    return max(ps, key=lambda p: p[13][1]) if ps else None
def pausas_es(q0, n):
    es = Me.env("es", AD / "narracao_es.wav"); fal = Me.falando(es, es)[q0:q0 + n]
    runs, k = [], 0
    while k < n:
        if not fal[k]:
            j = k
            while j < n and not fal[j]: j += 1
            if j - k >= MINQ: runs.append((k, j))
            k = j
        else: k += 1
    return runs
def mascara(p):
    lab = (p[13] + p[14]) / 2; queixo = p[152]; nariz = p[2]
    c = (lab + queixo) / 2 + np.array([0, 0.08 * np.linalg.norm(queixo - nariz)])
    ax = int(0.62 * np.linalg.norm(p[61] - p[291]) + 18); ay = int(0.62 * np.linalg.norm(queixo - nariz) + 8)
    m = np.zeros((1280, 720), np.float32)
    cv2.ellipse(m, (int(c[0]), int(c[1])), (ax, ay), 0, 0, 360, 1.0, -1)
    return cv2.GaussianBlur(m, (0, 0), 7)
def fechar(frames, q0, log=None):
    """frames: lista de quadros 720x1280 do trecho (ja colados). Altera e devolve."""
    n = len(frames); runs = pausas_es(q0, n)
    if not runs: return frames
    P = [None] * n; ab = np.full(n, np.nan)
    need = set()
    for a, b in runs:
        need.update(range(max(0, a - 45), min(n, b + 45)))
    for k in sorted(need):
        P[k] = marcos(frames[k])
        if P[k] is not None: ab[k] = Me.cl._abertura(P[k])
    orig = [f.copy() for f in frames]
    for a, b in runs:
        viz = [k for k in range(max(0, a - 45), min(n, b + 45)) if np.isfinite(ab[k])]
        if not viz: continue
        r = min(viz, key=lambda k: ab[k]); pr = P[r]; ref = orig[r]
        for k in range(a, b):
            w = min(1.0, (k - a + 1) / RAMPA, (b - k) / RAMPA)
            pk = P[k] if P[k] is not None else marcos(frames[k])
            if pk is None: continue
            M, _ = cv2.estimateAffinePartial2D(pr[ESTAVEIS].astype(np.float32), pk[ESTAVEIS].astype(np.float32))
            if M is None: continue
            g = cv2.warpAffine(ref, M, (720, 1280), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
            ms = mascara(pk)[..., None] * w
            frames[k] = np.clip(g * ms + frames[k] * (1 - ms), 0, 255).astype(np.uint8)
        if log is not None: log.append(f"pausa {(q0+a)/30:.2f}-{(q0+b)/30:.2f}s ref q{q0+r} ab={ab[r]:.3f}")
    return frames
