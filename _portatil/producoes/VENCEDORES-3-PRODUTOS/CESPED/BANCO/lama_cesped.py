# Remove a legenda queimada (branca/amarela com contorno preto) da faixa y 795-895 com LaMa. Uso: _vg python lama_leg.py in out
import sys, cv2, numpy as np, subprocess, time, torch
from PIL import Image
from simple_lama_inpainting import SimpleLama
src, out = sys.argv[1], sys.argv[2]
Y0, Y1 = 630, 780
cap = cv2.VideoCapture(src); fps = cap.get(5); N = int(cap.get(7)); lama = SimpleLama(); print("cuda", torch.cuda.is_available(), flush=True)
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
p = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",f"{fps}","-i","-","-an","-c:v","libx264","-crf","13","-preset","fast","-pix_fmt","yuv420p",*COR,out], stdin=subprocess.PIPE)
t0 = time.time(); prev = None; ema = None; i = 0
FR = []
while True:
    ok, x = cap.read()
    if not ok: break
    FR.append(x)
N = len(FR)
for j in range(N):
    f = FR[j]
    roi = f[Y0:Y1].astype(np.int16); b, g, r = roi[...,0], roi[...,1], roi[...,2]
    st_ = np.zeros(roi.shape[:2], bool)
    for jj in (j - 1, j + 1):
        if 0 <= jj < N: st_ |= np.abs(FR[jj][Y0:Y1].astype(np.int16) - roi).max(-1) < 14
    white = (roi.min(-1) > 200) & ((roi.max(-1) - roi.min(-1)) < 40)
    yel = (r > 190) & (g > 190) & (b < 110)
    dark = (roi.max(-1) < 60).astype(np.uint8)
    core = ((white | yel) & st_).astype(np.uint8) & cv2.dilate(dark, np.ones((7, 7), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(core)
    for k in range(1, n):
        if st[k, cv2.CC_STAT_AREA] < 12: core[lab == k] = 0
    m = np.zeros(f.shape[:2], np.uint8)
    if core.sum() > 150:
        # junta as letras de cada palavra num bloco: fecha na horizontal e dilata
        d = cv2.dilate(core, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
        d = cv2.morphologyEx(d, cv2.MORPH_CLOSE, np.ones((5, 25), np.uint8))
        dn = np.zeros_like(d); dn[4:] = d[:-4]
        m[Y0:Y1] = cv2.dilate(d | dn, np.ones((5, 5), np.uint8))
    g_ = cv2.resize(f, (90, 160)).astype(np.float32)
    if prev is not None and np.abs(g_ - prev).mean() > 20: ema = None
    prev = g_
    if m.sum() == 0:
        ema = None; p.stdin.write(f.tobytes()); i += 1; continue
    a0, a1 = Y0 - 60, Y1 + 60
    crop = f[a0:a1].copy()
    res = lama(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)), Image.fromarray(m[a0:a1] * 255))
    res = cv2.cvtColor(np.array(res), cv2.COLOR_RGB2BGR)[:crop.shape[0], :crop.shape[1]].astype(np.float32)
    l = f.astype(np.float32).copy(); l[a0:a1] = res
    ema = l if ema is None else 0.7 * l + 0.3 * ema
    al = np.maximum(cv2.GaussianBlur(m.astype(np.float32), (11, 11), 0), m)[..., None]
    f = np.clip(ema * al + f * (1 - al), 0, 255).astype(np.uint8)
    p.stdin.write(f.tobytes()); i += 1
    if i % 100 == 0: el = time.time() - t0; print(f"[{i}/{N}] {100*i//N}% falta ~{el/i*(N-i):.0f} s", flush=True)
p.stdin.close(); p.wait(); print("ok", i, round(time.time() - t0), "s")
