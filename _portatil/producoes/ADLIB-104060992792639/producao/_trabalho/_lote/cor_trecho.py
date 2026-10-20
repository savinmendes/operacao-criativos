# -*- coding: utf-8 -*-
"""Correcao de cor do lote C (ADs 10, 15, 16), sem credito HeyGen. Pecas comuns:
- base_lama(): base limpa nova = quadro do ORIGINAL + so as areas do LaMa (mascara packbits) copiadas da base antiga,
  com a cor da antiga levada ao original por uma afim BGR 3x4 robusta por quadro, medida fora da mascara (= ad08).
- medir()/corrigir(): cor de cada trecho do HeyGen contra a base nova, em 3 camadas:
  1) afim BGR 3x4 robusta saida -> base no recorte enviado ao HeyGen, FORA da elipse colada (cobre a leitura cv2 bt709
     x gravacao bt601 da entrada e o desvio do proprio HeyGen, com a faixa de cores inteira do recorte);
  2) desvio residual no ANEL DE PELE em volta da elipse (fora dela), mediana de 12 quadros;
  3) ajuste interno (mediana dentro da elipse, m > 0,5) aplicado com o peso da propria elipse (0 na borda, 1 no centro),
     porque o HeyGen escurece a pele dentro da area da boca. Limitado a +-10.
Leitura/gravacao: ad13/lipsync3/comum3.py (bt601 + accurate_rnd, inversa exata, etiqueta bt709/tv so no bitstream)."""
import sys, subprocess, numpy as np, cv2
from pathlib import Path
T = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(T / "ad13" / "lipsync3"))
from comum3 import quadros, ENC_VF, ENC_TAG, reamostrar  # noqa: E402,F401


def enc(path, fps, crf=12):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "720x1280", "-r", str(fps), "-i", "-",
                             *ENC_VF, "-threads", "4", "-c:v", "libx264", "-crf", str(crf), "-preset", "medium", "-pix_fmt", "yuv420p", *ENC_TAG,
                             "-an", str(path)], stdin=subprocess.PIPE)


def ajustar(X, Y, it=4):
    """afim robusta 4x3 (linhas B G R 1) X -> Y"""
    X = X.astype(np.float64); Y = Y.astype(np.float64); Xa = np.c_[X, np.ones(len(X))]; ok = np.ones(len(X), bool)
    for _ in range(it):
        A, *_ = np.linalg.lstsq(Xa[ok], Y[ok], rcond=None); r = np.linalg.norm(Xa @ A - Y, axis=1)
        ok = r < max(3.0, 2.5 * np.median(r[ok]))
    return A.astype(np.float32), float(np.median(r[ok])), float(ok.mean())


def aplicar(A, f):
    return f.reshape(-1, 3).astype(np.float32) @ A[:3] + A[3]


def base_lama(orig, velha, mk_npy, n, log):
    """gera (q, quadro) da base nova; mascara = packbits 1280x720 por quadro (lama_base.py)"""
    MK = np.load(mk_npy, mmap_mode="r"); fits = []
    for q, (o, v) in enumerate(zip(quadros(orig, 0, n), quadros(velha, 0, n))):
        m = np.unpackbits(MK[q])[:1280 * 720].reshape(1280, 720) if q < len(MK) else np.zeros((1280, 720), np.uint8)
        if m.any():
            M = cv2.dilate(m, np.ones((19, 19), np.uint8))
            fora = cv2.dilate(M, np.ones((41, 41), np.uint8)) == 0; fora[::2] = False; fora[:, ::3] = False
            A, r, fr = ajustar(v[fora][::4], o[fora][::4], 3); fits.append((r, fr))
            vc = aplicar(A, v).reshape(v.shape)
            w = np.maximum(cv2.GaussianBlur(M.astype(np.float32), (0, 0), 3), M)[..., None]
            o = np.clip(vc * w + o.astype(np.float32) * (1 - w) + 0.5, 0, 255).astype(np.uint8)
        yield q, o
    if fits:
        F = np.array(fits); log.append(f"base: areas LaMa da base antiga levadas ao original em {len(F)} quadros (afim 3x4/quadro, residuo mediano {np.median(F[:, 0]):.2f}, inliers {np.median(F[:, 1]):.2f})")


def caixa_mask(x0, y0, x1, y1, ins=2):
    c = np.zeros((1280, 720), bool); c[max(0, y0) + ins:min(1280, y1) - ins, max(0, x0) + ins:min(720, x1) - ins] = True; return c


def medir(amostras):
    """amostras: [(base uint8, full uint8 = saida do HeyGen colada no recorte sem mistura, m 2D float, caixa (x0,y0,x1,y1), fw)]"""
    X, Y = [], []
    for b, full, m, cx, fw in amostras:
        sel = caixa_mask(*cx, ins=4) & (cv2.dilate((m > 0.005).astype(np.uint8), np.ones((9, 9), np.uint8)) == 0)
        X.append(full[sel][::7]); Y.append(b[sel][::7])
    A, res, fr = ajustar(np.vstack(X), np.vstack(Y))
    d0s, d1s = [], []
    for b, full, m, cx, fw in amostras:
        fc = aplicar(A, full).reshape(full.shape); cm = caixa_mask(*cx); dentro = m > 0.01
        k = int(max(9, 0.5 * fw)) | 1
        anel = cv2.dilate(dentro.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))).astype(bool) & ~dentro & cm
        if anel.sum() >= 50: d0s.append((b.astype(np.float32) - fc)[anel].mean(0))
    d0 = np.median(np.array(d0s), 0).astype(np.float32) if d0s else np.zeros(3, np.float32)
    for b, full, m, cx, fw in amostras:
        fc = aplicar(A, full).reshape(full.shape) + d0; sel = (m > 0.5) & caixa_mask(*cx)
        if sel.sum() >= 50: d1s.append(np.median((b.astype(np.float32) - fc)[sel], 0))
    d1 = np.clip(np.median(np.array(d1s), 0), -10, 10).astype(np.float32) if d1s else np.zeros(3, np.float32)
    antes = np.median(np.array([(b.astype(np.float32) - full.astype(np.float32))[caixa_mask(*cx) & (m <= 0.005)].mean(0) for b, full, m, cx, fw in amostras]), 0)
    return dict(A=A, d0=d0, d1=d1, res=res, inl=fr, antes=antes)


def corrigir(full, C, m, cx):
    """aplica as 3 camadas so dentro do recorte (fora dele o 'full' e a propria base)"""
    x0, y0, x1, y1 = max(0, cx[0]), max(0, cx[1]), min(720, cx[2]), min(1280, cx[3])
    out = full.astype(np.float32); r = full[y0:y1, x0:x1]
    out[y0:y1, x0:x1] = aplicar(C["A"], r).reshape(r.shape) + C["d0"] + C["d1"] * m[y0:y1, x0:x1, None]
    return out


def txt(nome, C):
    return (f"{nome}: saida HeyGen x base nova (BGR, fora da elipse) antes {C['antes'].round(1)} | afim residuo {C['res']:.2f} inliers {C['inl']:.2f}"
            f" | anel {C['d0'].round(2)} | interno {C['d1'].round(2)}")
