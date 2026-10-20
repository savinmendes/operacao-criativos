# -*- coding: utf-8 -*-
"""LaMa (GPU) só onde a máscara da legenda PT marca. Leitura bt709/full (como o original está etiquetado) e gravação
com a matriz inversa bt709/tv + etiqueta bt709/tv: pixel não tocado volta igual (só muda a faixa de níveis)."""
import sys, time, warnings, subprocess; warnings.filterwarnings("ignore")
import cv2, numpy as np, torch
from PIL import Image
from simple_lama_inpainting import SimpleLama
V = r"C:\Users\PICHAU\Downloads\GRIMORIO V2.mp4"
MASK, SAIDA = sys.argv[1], sys.argv[2]
MK = np.concatenate([np.load(p) for p in MASK.split(",")]); N = len(MK); print("mascaras", N, flush=True)
lama = SimpleLama(); print("cuda", torch.cuda.is_available(), flush=True)
dec = subprocess.Popen(["ffmpeg","-v","error","-i",V,"-vf","scale=in_color_matrix=bt709:in_range=full:flags=accurate_rnd+full_chroma_int,format=bgr24",
    "-f","rawvideo","-"], stdout=subprocess.PIPE)
tmp = SAIDA.replace(".mp4", "_v.mp4")
enc = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",
    "-vf","scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
    "-c:v","libx264","-crf","12","-preset","medium","-color_range","tv","-colorspace","bt709","-color_primaries","bt709",
    "-color_trc","bt709", tmp], stdin=subprocess.PIPE)
T = 720*1280*3; ema = None; prev = None; t0 = time.time()
for i in range(N):
    b = dec.stdout.read(T)
    if len(b) < T: break
    f = np.frombuffer(b, np.uint8).reshape(1280, 720, 3).copy()
    m = np.unpackbits(MK[i])[:1280*720].reshape(1280, 720)
    g = cv2.resize(f, (90, 160)).astype(np.float32)
    if prev is not None and np.abs(g - prev).mean() > 12: ema = None
    prev = g
    if m.sum() == 0:
        ema = None; enc.stdin.write(f.tobytes()); continue
    ys = np.where(m.any(1))[0]; a0 = max(0, ys.min() - 120); a1 = min(1280, ys.max() + 120)
    crop = f[a0:a1]; mk = m[a0:a1]
    r = lama(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)), Image.fromarray(mk * 255))
    r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:crop.shape[0], :crop.shape[1]].astype(np.float32)
    l = f.astype(np.float32).copy(); l[a0:a1] = r
    ema = l if ema is None else 0.7 * l + 0.3 * ema
    al = np.maximum(cv2.GaussianBlur(m.astype(np.float32), (9, 9), 0), m)[..., None]
    f = np.clip(ema * al + f * (1 - al), 0, 255).astype(np.uint8)
    enc.stdin.write(f.tobytes())
    if (i + 1) % 200 == 0:
        el = time.time() - t0; print(f"[{i+1}/{N}] {100*(i+1)//N}% falta ~{el/(i+1)*(N-i-1):.0f} s", flush=True)
enc.stdin.close(); enc.wait(); dec.kill()
subprocess.run(["ffmpeg","-v","error","-y","-i",tmp,"-i",V,"-map","0:v","-map","1:a","-c","copy","-movflags","+faststart",SAIDA], check=True)
print("ok", SAIDA, round(time.time() - t0), "s")
