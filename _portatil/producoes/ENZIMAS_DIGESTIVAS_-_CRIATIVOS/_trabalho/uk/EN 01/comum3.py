# -*- coding: utf-8 -*-
"""ler / reamostrar / colar (copiados do ad17/lipsync/recolocar.py)."""
import cv2, numpy as np
import subprocess
def quadros(p, pula=0, n=None, w=720, h=1280):
    """Gera os quadros BGR lendo com a matriz bt601/tv FIXA. O cv2 le arquivo com etiqueta bt709 usando bt709 e o sem
    etiqueta com bt601; os encoders destes scripts gravam em bt601 com etiqueta bt709, entao ler sempre em bt601 evita
    o desvio de cor acumulado a cada passada."""
    pr = subprocess.Popen(["ffmpeg","-v","error","-i",str(p),"-vf",f"select=gte(n\,{pula}),scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24",
        "-fps_mode","passthrough","-f","rawvideo","-"], stdout=subprocess.PIPE)
    k = 0; t = w * h * 3
    while n is None or k < n:
        b = pr.stdout.read(t)
        if len(b) < t: break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3).copy(); k += 1
    pr.stdout.close(); pr.kill(); pr.wait()
# encoder de quadros BGR (stdin) com a conversao inversa exata + etiqueta bt709/tv so no bitstream (sem mexer nos pixels)
ENC_VF = ["-vf", "scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p"]
ENC_TAG = ["-bsf:v", "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1"]
def ler(p, pula=0):
    return list(quadros(p, pula))
def reamostrar(fr, n):
    m = len(fr)
    if m >= n: return fr[:n]
    out = []
    for i in range(n):
        x = i * (m - 1) / (n - 1); j = int(np.floor(x)); a = x - j
        out.append(fr[-1] if j >= m - 1 else (fr[j] if a < 1e-3 else cv2.addWeighted(fr[j], 1 - a, fr[j + 1], a, 0)))
    return out
def colar(base, g, c):
    x0, y0, w, h, mx, my, fw, fh = c
    M = np.float32([[w / 720, 0, x0], [0, h / 1280, y0]])
    full = cv2.warpAffine(g, M, (720, 1280), flags=cv2.INTER_AREA if w < 720 else cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    m = np.zeros((1280, 720), np.float32)
    cv2.ellipse(m, (int(mx), int(my + 0.02 * fh)), (int(0.40 * fw), int(0.30 * fh)), 0, 0, 360, 1.0, -1)
    m = cv2.GaussianBlur(m, (0, 0), max(3, 0.07 * fw))[..., None]
    return np.clip(full * m + base * (1 - m), 0, 255).astype(np.uint8)
def desvio_cor(nm, a, AQ, AD, amostras=(0, 10, 20)):
    """Desvio de cor (BGR) que o recorte de entrada (cortar.py: leitura cv2 + encoder padrao) levou para o HeyGen:
    media de (base recortada - in/pt_<seg>.mp4) nos quadros amostrados. Soma-se a saida antes de colar."""
    C = np.load(AQ / f"caixas_{nm}.npy"); p = list(quadros(AQ / "in" / f"pt_{nm}.mp4", 0, max(amostras) + 1))
    b = list(quadros(AD / "base_sem_legenda.mp4", a, max(amostras) + 1)); d = []
    for k in amostras:
        x0, y0, w, h = C[k, :4]; M = np.float32([[720 / w, 0, -x0 * 720 / w], [0, 1280 / h, -y0 * 1280 / h]])
        cb = cv2.warpAffine(b[k], M, (720, 1280), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT).astype(np.float32)
        d.append((cb - p[k].astype(np.float32))[200:1100].mean(axis=(0, 1)))
    return np.mean(d, 0)
def corrigir(g, dv):
    return [np.clip(f.astype(np.float32) + dv, 0, 255).astype(np.uint8) for f in g]
