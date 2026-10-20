"""Remove a legenda queimada (faixa y 836-980) do 11.mp4.
Mulher (câmera fixa): placa limpa temporal = mediana dos quadros em que o pixel está fora da caixa da legenda.
Menina: mesma ideia; o que nunca fica livre é preenchido por inpaint na PLACA (estático, sem tremer).
Transições/b-roll do mercado/cédulas: inpaint Telea por quadro (cédulas e mercado são trocados/recortados depois).
Saída sem áudio, 720x1280 30 fps."""
import subprocess, sys
import cv2
import numpy as np

SRC, OUT = sys.argv[1], sys.argv[2]
Y0, Y1 = 836, 980
BM = np.load('_tmp/boxmasks.npy')            # caixas por quadro (linhas da legenda), gerado por cobertura.py
SHOTS = [(0, 265, "menina"), (265, 271, "telea"), (271, 359, "mulherB"), (359, 462, "telea"),
         (462, 936, "mulherC"), (936, 939, "telea"), (939, 1138, "telea"), (1138, 1861, "mulherE")]


def mascara_justa(roi):
    b, g, r = cv2.split(roi.astype(np.int16))
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    txt = ((np.minimum(r, g) > 150) & (gray > 150)).astype(np.uint8)
    txt &= cv2.dilate((gray < 80).astype(np.uint8), np.ones((7, 7), np.uint8))
    return cv2.dilate(txt, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))


cap = cv2.VideoCapture(SRC)
rois = []
while True:
    ok, f = cap.read()
    if not ok:
        break
    rois.append(f[Y0:Y1].copy())
N = len(rois)
cap.release()


def placa(frames):
    st = np.stack([rois[i] for i in frames]).astype(np.float32)
    mk = np.stack([BM[i] for i in frames]).astype(bool)
    st[mk] = np.nan
    p = np.nanmedian(st, axis=0)
    buraco = np.isnan(p).any(axis=2)
    p = np.nan_to_num(p).astype(np.uint8)
    if buraco.any():
        p = cv2.inpaint(p, cv2.dilate(buraco.astype(np.uint8), np.ones((3, 3), np.uint8)), 6, cv2.INPAINT_TELEA)
    print("placa", frames[0], frames[-1], "buracos", int(buraco.sum()), flush=True)
    return p


import warnings
warnings.filterwarnings("ignore")
P = {
    "menina": placa(list(range(0, 265))),
    "mulherC": placa(list(range(462, 936))),
    "mulherE": placa(list(range(1138, N))),
}
P["mulherB"] = P["mulherC"]
cv2.imwrite('_tmp/placas.png', np.vstack([P["menina"], P["mulherC"], P["mulherE"]]))

cap = cv2.VideoCapture(SRC)
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "720x1280",
                       "-r", "30", "-i", "-", "-an", "-c:v", "libx264", "-crf", "12", "-preset", "medium",
                       "-pix_fmt", "yuv420p", OUT], stdin=subprocess.PIPE)
for i in range(N):
    ok, f = cap.read()
    roi = f[Y0:Y1]
    modo = next(m for a, b, m in SHOTS if a <= i < b)
    if modo == "telea":
        novo = cv2.inpaint(roi, mascara_justa(roi), 4, cv2.INPAINT_TELEA)
    else:
        m = BM[i].astype(np.uint8)
        p = P[modo].astype(np.float32)
        anel = (cv2.dilate(m, np.ones((21, 21), np.uint8)) > 0) & (m == 0)
        if anel.sum() > 50:
            p = p + (roi[anel].astype(np.float32).mean(0) - p[anel].mean(0))
        alpha = cv2.GaussianBlur(cv2.dilate(m, np.ones((9, 9), np.uint8)).astype(np.float32), (15, 15), 0)[..., None]
        alpha = np.maximum(alpha, m[..., None].astype(np.float32))
        novo = np.clip(p * alpha + roi * (1 - alpha), 0, 255).astype(np.uint8)
    f[Y0:Y1] = novo
    ff.stdin.write(f.tobytes())
    if i % 300 == 0:
        print(f"[{i}/{N}] {100*i//N}%", flush=True)
ff.stdin.close()
ff.wait()
print("ok", OUT)
