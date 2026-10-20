"""base_sem_legenda.mp4 (24 fps, N quadros, sem audio): faixa LaMa colada so na mascara (borda suave), EMA leve zerada nos cortes.
Uso: montar_base.py video.mp4 lamadir N saida [hook_video hook_lamadir hook_n]"""
import sys, subprocess, cv2, numpy as np
sys.path.insert(0, '_tmp'); from mascara import R0, R1
vid, ld, N, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","24","-i","-","-an",
    "-c:v","libx264","-crf","12","-preset","medium","-threads","4","-pix_fmt","yuv420p",*COR,out], stdin=subprocess.PIPE)
cap = cv2.VideoCapture(vid); ema = None; prev = None
for i in range(N):
    ok, f = cap.read(); g = cv2.resize(f, (90, 160)).astype(np.float32)
    if prev is not None and np.abs(g - prev).mean() > 8: ema = None
    prev = g
    m = cv2.imread(f"{ld}/mask_{i:04d}.png", 0).astype(np.float32) / 255
    if m.sum() > 0:
        l = cv2.imread(f"{ld}/{i:04d}.png").astype(np.float32)
        ema = l if ema is None else 0.7 * l + 0.3 * ema
        a = np.maximum(cv2.GaussianBlur(m, (11, 11), 0), m)[..., None]
        roi = f[R0:R1].astype(np.float32); f[R0:R1] = np.clip(ema * a + roi * (1 - a), 0, 255).astype(np.uint8)
    else: ema = None
    ff.stdin.write(np.ascontiguousarray(f).tobytes())
ff.stdin.close(); ff.wait(); print("ok", N)
