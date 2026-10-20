"""2a passada: tira a seta vermelha + faiscas do original (deteccao no ORIGINAL, y 680-1010), LaMa sobre a base ja sem legenda.
Uso: _vg python seta_patch.py base_in.mp4 original.mp4 fps t_seta base_out.mp4"""
import sys, time, subprocess, warnings; warnings.filterwarnings("ignore")
import cv2, numpy as np
from PIL import Image
from simple_lama_inpainting import SimpleLama
BIN, SRC, FPS, T0, OUT = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
S0 = int(T0 * FPS); lama = SimpleLama()
x0, x1, y0, y1 = 190, 530, 680, 1010; C0, C1 = 560, 1100
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",str(FPS),"-i","-","-an",
    "-threads","4","-c:v","libx264","-crf","12","-preset","medium","-pix_fmt","yuv420p",*COR,OUT], stdin=subprocess.PIPE)
b = cv2.VideoCapture(BIN); o = cv2.VideoCapture(SRC); i = 0; ema = None; prev = None; n = 0; t = time.time()
while True:
    ok, f = b.read()
    if not ok: break
    ok2, g = o.read()
    gg = cv2.resize(g, (90, 160)).astype(np.float32)
    if prev is not None and np.abs(gg - prev).mean() > 12: ema = None
    prev = gg
    if i >= S0:
        hs = cv2.cvtColor(g[y0:y1, x0:x1], cv2.COLOR_BGR2HSV); H, S, V = hs[..., 0], hs[..., 1], hs[..., 2]
        red = (((H <= 8) | (H >= 170)) & (S >= 150) & (V >= 120)).astype(np.uint8)
        if red.sum() > 200:
            ys, xs = np.nonzero(red); bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max()
            wht = ((S < 60) & (V > 200)).astype(np.uint8); zona = np.zeros_like(wht)
            zona[max(0, by0 - 15):by1 + 40, max(0, bx0 - 100):bx1 + 100] = 1
            m = cv2.dilate(red, np.ones((17, 17), np.uint8)) | cv2.dilate(wht & zona, np.ones((11, 11), np.uint8))
            # o contorno branco da seta
            m = cv2.dilate(m, np.ones((5, 5), np.uint8))
            crop = f[C0:C1].copy(); mk = np.zeros(crop.shape[:2], np.uint8); mk[y0 - C0:y1 - C0, x0:x1] = m
            r = lama(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)), Image.fromarray(mk * 255))
            r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:crop.shape[0], :crop.shape[1]].astype(np.float32)
            ema = r if ema is None else 0.65 * r + 0.35 * ema
            mf = mk.astype(np.float32); a = np.maximum(cv2.GaussianBlur(mf, (11, 11), 0), mf)[..., None]
            f[C0:C1] = np.clip(ema * a + crop * (1 - a), 0, 255).astype(np.uint8); n += 1
        else: ema = None
    ff.stdin.write(np.ascontiguousarray(f).tobytes()); i += 1
ff.stdin.close(); ff.wait(); print("ok", i, "quadros, seta em", n, time.time() - t)
