"""base_sem_legenda.mp4 do 17 (24 fps, quadros [0, N), sem audio, bt709 tv).
Legenda PT amarela (faixa y 940-1110): mascara JUSTA (glifo amarelo h 22-40 dilatado 9) -> LaMa GPU.
Seta vermelha + faiscas brancas do original (>= 69,4 s, x 200-520, y 780-1000): mascara da seta dilatada -> LaMa.
EMA leve dentro da mascara, zerada nos cortes. Salva a mascara em _tmp/mask.npy (linhas R0-R1) para conferencia.
Uso: _vg python _tmp/base_lama.py N"""
import sys, time, subprocess, warnings; warnings.filterwarnings("ignore")
import cv2, numpy as np, torch
from PIL import Image
from simple_lama_inpainting import SimpleLama
SRC = sys.argv[2] if len(sys.argv) > 2 else '../../../UNICOS_HD/17.mp4'
N = int(sys.argv[1]); FPS = int(sys.argv[3]) if len(sys.argv) > 3 else 24
SETA0 = int(float(sys.argv[4]) * FPS) if len(sys.argv) > 4 else int(69.3 * 24)
OUT = sys.argv[5] if len(sys.argv) > 5 else 'base_sem_legenda.mp4'
R0, R1 = 770, 1115; C0, C1 = 700, 1180
lama = SimpleLama(); print("cuda", torch.cuda.is_available(), flush=True)
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",str(FPS),"-i","-","-an",
    "-threads","4","-c:v","libx264","-crf","12","-preset","medium","-pix_fmt","yuv420p",*COR,OUT], stdin=subprocess.PIPE)
cap = cv2.VideoCapture(SRC); MK = np.zeros((N, R1 - R0, 720), np.uint8)
el = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)); ema = None; prev = None; t0 = time.time(); cortes = []
def mascara(f, i):
    m = np.zeros((R1 - R0, 720), np.uint8)
    roi = f[940:1110]; hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV); h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    core = ((h >= 22) & (h <= 40) & (s >= 90) & (v >= 150)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(core)
    for k in range(1, n):
        if st[k, 4] < 6: core[lab == k] = 0
    if core.sum() > 30:
        m[940 - R0:1110 - R0] = cv2.dilate(cv2.dilate(core, el), np.ones((9, 9), np.uint8))
    if i >= SETA0:
        x0, x1, y0, y1 = 200, 520, 780, 1000
        hs = cv2.cvtColor(f[y0:y1, x0:x1], cv2.COLOR_BGR2HSV); H, S, V = hs[..., 0], hs[..., 1], hs[..., 2]
        red = (((H <= 8) | (H >= 170)) & (S >= 150) & (V >= 120)).astype(np.uint8)
        if red.sum() > 200:
            ys, xs = np.nonzero(red); bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max()
            wht = ((S < 45) & (V > 215)).astype(np.uint8); zona = np.zeros_like(wht)
            zona[max(0, by0 - 15):min(y1 - y0, by1 + 35), max(0, bx0 - 95):min(x1 - x0, bx1 + 95)] = 1
            sm = cv2.dilate(red, np.ones((15, 15), np.uint8)) | cv2.dilate(wht & zona, np.ones((9, 9), np.uint8))
            m[y0 - R0:y1 - R0, x0:x1] |= sm
    return m
for i in range(N):
    ok, f = cap.read()
    if not ok: print("fim antecipado", i); break
    g = cv2.resize(f, (90, 160)).astype(np.float32)
    if prev is not None and np.abs(g - prev).mean() > 12: ema = None; cortes.append(i)
    prev = g
    m = mascara(f, i); MK[i] = m
    if m.any():
        crop = f[C0:C1].copy(); mk = np.zeros(crop.shape[:2], np.uint8); mk[R0 - C0:R1 - C0] = m
        r = lama(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)), Image.fromarray(mk * 255))
        r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:crop.shape[0], :crop.shape[1]][R0 - C0:R1 - C0].astype(np.float32)
        ema = r if ema is None else 0.65 * r + 0.35 * ema
        mf = m.astype(np.float32); a = np.maximum(cv2.GaussianBlur(mf, (11, 11), 0), mf)[..., None]
        roi = f[R0:R1].astype(np.float32); f[R0:R1] = np.clip(ema * a + roi * (1 - a), 0, 255).astype(np.uint8)
    else: ema = None
    ff.stdin.write(np.ascontiguousarray(f).tobytes())
    if (i + 1) % 200 == 0:
        e = time.time() - t0; print(f"[{i+1}/{N}] {100*(i+1)//N}% falta ~{e/(i+1)*(N-i-1):.0f} s", flush=True)
ff.stdin.close(); ff.wait(); np.save('_tmp/mask.npy', MK); print("ok cortes", cortes, time.time() - t0)
