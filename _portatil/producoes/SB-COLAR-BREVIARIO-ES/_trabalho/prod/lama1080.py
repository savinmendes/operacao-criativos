# -*- coding: utf-8 -*-
"""LaMa (GPU) na legenda PT queimada do original 1080x1920 -> base_sem_legenda.mp4 (cor fixa bt601, etiqueta bt709)."""
import sys, time, warnings, subprocess; warnings.filterwarnings("ignore")
import cv2, numpy as np, torch
from PIL import Image
from simple_lama_inpainting import SimpleLama
from comum3 import quadros, ENC_VF, ENC_TAG
from mascara import mascara
SRC = "../../original_wsen5drS7Nk.mp4"; N = 4175
lama = SimpleLama(); print("cuda", torch.cuda.is_available(), flush=True)
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","1080x1920","-r","30","-i","-",
    *ENC_VF,"-threads","3","-c:v","libx264","-crf","12","-preset","medium",*ENC_TAG,"-an","base_sem_legenda.mp4"],stdin=subprocess.PIPE)
ema = None; prev = None; t0 = time.time()
for i, f in enumerate(quadros(SRC, 0, None, 1080, 1920)):
    g = cv2.resize(f, (90, 160)).astype(np.float32)
    if prev is not None and np.abs(g - prev).mean() > 20: ema = None
    prev = g
    m = mascara(f)
    if m.sum() == 0:
        ema = None; ff.stdin.write(np.ascontiguousarray(f).tobytes()); continue
    ys = np.where(m.any(1))[0]; a0 = max(0, ys.min() - 90); a1 = min(1920, ys.max() + 90)
    crop = f[a0:a1].copy(); mk = m[a0:a1]
    r = lama(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)), Image.fromarray(mk * 255))
    r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:crop.shape[0], :crop.shape[1]].astype(np.float32)
    l = np.zeros_like(f, dtype=np.float32); l[a0:a1] = r
    ema = l if ema is None else 0.65 * l + 0.35 * ema
    al = np.maximum(cv2.GaussianBlur(m.astype(np.float32), (11, 11), 0), m)[..., None]
    f = np.clip(ema * al + f * (1 - al), 0, 255).astype(np.uint8)
    ff.stdin.write(np.ascontiguousarray(f).tobytes())
    if (i + 1) % 300 == 0:
        el = time.time() - t0; print(f"[{i+1}/{N}] {100*(i+1)//N}% falta ~{el/(i+1)*(N-i-1):.0f} s", flush=True)
ff.stdin.close(); ff.wait(); print("ok", i + 1, round(time.time() - t0))
