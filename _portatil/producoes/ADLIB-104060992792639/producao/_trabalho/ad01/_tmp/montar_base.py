"""Monta base_sem_legenda.mp4 (720x1280, 30 fps, sem áudio, todos os 3937 quadros).
Faixa y 820-990: LaMa (GPU) por quadro, colado só na máscara da legenda com borda suave e
EMA leve dentro da máscara (zera nos cortes de cena) para não tremer. Quadros >= 3473 (cartão final) ficam iguais."""
import subprocess, cv2, numpy as np
Y0, Y1, NF = 820, 990, 3473
CORTES = {477, 584, 629, 979, 1470}
BM = np.load('_tmp/boxmasks.npy', mmap_mode='r')
cap = cv2.VideoCapture('../../../UNICOS_HD/01.mp4')
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",
    "-an","-c:v","libx264","-crf","13","-preset","medium","-pix_fmt","yuv420p","base_sem_legenda.mp4"], stdin=subprocess.PIPE)
ema = None; i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    if i < NF:
        if i in CORTES: ema = None
        l = cv2.imread(f'_tmp/lama/{i:04d}.png').astype(np.float32)
        ema = l if ema is None else 0.6 * l + 0.4 * ema
        m = cv2.dilate(np.array(BM[i]), np.ones((5, 5), np.uint8)).astype(np.float32)
        a = np.maximum(cv2.GaussianBlur(m, (11, 11), 0), m)[..., None]
        roi = f[Y0:Y1].astype(np.float32)
        f[Y0:Y1] = np.clip(ema * a + roi * (1 - a), 0, 255).astype(np.uint8)
    ff.stdin.write(f.tobytes()); i += 1
    if i % 500 == 0: print(f"[{i}/3937]", flush=True)
ff.stdin.close(); ff.wait(); print("ok", i)
