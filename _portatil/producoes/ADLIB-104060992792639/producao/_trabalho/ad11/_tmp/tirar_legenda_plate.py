"""Remove a legenda queimada do 11.mp4 com 'placa limpa' temporal por tomada (câmera fixa)
e inpaint Telea com máscara justa nas tomadas com câmera em movimento/transição."""
import subprocess, sys
import cv2
import numpy as np

SRC = sys.argv[1]
OUT = sys.argv[2]
X0, X1, Y0, Y1 = 40, 680, 836, 980          # retângulo da legenda (720x1280)
# tomadas (frames, fim exclusivo) e modo
SHOTS = [(0, 265, "plate"), (265, 271, "telea"), (271, 359, "plate"), (359, 462, "telea"),
         (462, 936, "plate"), (936, 939, "telea"), (939, 1138, "telea"), (1138, 99999, "plate")]


def mascara(roi):
    b, g, r = cv2.split(roi.astype(np.int16))
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    txt = ((np.minimum(r, g) > 165) & (gray > 165)).astype(np.uint8)
    escuro = (gray < 70).astype(np.uint8)
    perto_escuro = cv2.dilate(escuro, np.ones((7, 7), np.uint8))
    txt = txt & perto_escuro
    # componentes da letra: junta e expande para pegar o contorno preto
    txt = cv2.dilate(txt, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(txt)
    keep = np.zeros_like(txt)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] >= 25:
            keep[lab == i] = 1
    return cv2.dilate(keep, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))


cap = cv2.VideoCapture(SRC)
N = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
rois, masks = [], []
while True:
    ok, f = cap.read()
    if not ok:
        break
    roi = f[Y0:Y1, X0:X1].copy()
    rois.append(roi)
    masks.append(mascara(roi))
N = len(rois)
print("frames", N, flush=True)

plates = {}
for a, b, modo in SHOTS:
    b = min(b, N)
    if modo != "plate":
        continue
    idx = list(range(a, b, 2))
    st = np.stack([rois[i] for i in idx]).astype(np.float32)
    mk = np.stack([masks[i] for i in idx]).astype(bool)
    st[mk] = np.nan
    plate = np.nanmedian(st, axis=0)
    buraco = np.isnan(plate).any(axis=2)
    plate = np.nan_to_num(plate).astype(np.uint8)
    if buraco.any():
        plate = cv2.inpaint(plate, buraco.astype(np.uint8), 5, cv2.INPAINT_TELEA)
    plates[(a, b)] = plate
    print("placa", a, b, "buracos", int(buraco.sum()), flush=True)

cap.release()
cap = cv2.VideoCapture(SRC)
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "720x1280",
                       "-r", "30", "-i", "-", "-an", "-c:v", "libx264", "-crf", "12", "-preset", "medium",
                       "-pix_fmt", "yuv420p", OUT], stdin=subprocess.PIPE)
for i in range(N):
    ok, f = cap.read()
    roi = f[Y0:Y1, X0:X1]
    m = masks[i]
    for a, b, modo in SHOTS:
        if a <= i < min(b, N):
            break
    if modo == "plate":
        plate = plates[(a, min(b, N))]
        # corrige pequena diferença de brilho entre placa e quadro (anel ao redor da máscara)
        anel = (cv2.dilate(m, np.ones((15, 15), np.uint8)) > 0) & (m == 0)
        if anel.sum() > 50:
            delta = roi[anel].astype(np.float32).mean(0) - plate[anel].astype(np.float32).mean(0)
            plate = np.clip(plate.astype(np.float32) + delta, 0, 255).astype(np.uint8)
        alpha = cv2.GaussianBlur(m.astype(np.float32), (7, 7), 0)[..., None]
        alpha = np.maximum(alpha, m[..., None].astype(np.float32))
        novo = (plate * alpha + roi * (1 - alpha)).astype(np.uint8)
    else:
        novo = cv2.inpaint(roi, m, 4, cv2.INPAINT_TELEA)
    f[Y0:Y1, X0:X1] = novo
    ff.stdin.write(f.tobytes())
    if i % 300 == 0:
        print(f"[{i}/{N}]", flush=True)
ff.stdin.close()
ff.wait()
print("ok", OUT)
