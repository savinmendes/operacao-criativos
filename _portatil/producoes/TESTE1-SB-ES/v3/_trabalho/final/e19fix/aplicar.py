# -*- coding: utf-8 -*-
"""Aplica board_edit (Crux/Silentium) em cada quadro do e19 (que tem zoom lento): acha a afim board->quadro por ECC e soma a diferença edit-clean nas 2 placas, preservando os círculos vermelhos."""
import sys, subprocess, cv2, numpy as np
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG
SRC = r"C:\Users\PICHAU\Downloads\TESTE1-SB-ES\v3\_trabalho\broll\e19_cuadro_12_palabras.mp4"
CL = cv2.imread(r"C:\Users\PICHAU\Downloads\TESTE1-SB-ES\_trabalho\q\board_clean.png"); ED = cv2.imread("board_edit.png")
D = ED.astype(np.float32) - CL.astype(np.float32)
M = np.zeros(CL.shape[:2], np.uint8); M[394:426, 324:396] = 255; M[660:695, 70:168] = 255
M = cv2.GaussianBlur(M, (0, 0), 1.5).astype(np.float32) / 255
s = 0.5; g0 = cv2.cvtColor(cv2.resize(CL, None, fx=s, fy=s), cv2.COLOR_BGR2GRAY).astype(np.float32)
mask_ecc = np.ones_like(g0, np.uint8); mask_ecc[int(150 * s):int(340 * s), :] = 0     # título não está no board_clean
W = np.eye(2, 3, dtype=np.float32); out = []; crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 80, 1e-5)
for k, f in enumerate(quadros(SRC)):
    g = cv2.cvtColor(cv2.resize(f, None, fx=s, fy=s), cv2.COLOR_BGR2GRAY).astype(np.float32)
    try: cc, W = cv2.findTransformECC(g0, g, W, cv2.MOTION_AFFINE, crit, mask_ecc, 5)
    except cv2.error: cc = -1
    A = W.copy(); A[:, 2] /= s
    h, w = f.shape[:2]
    dw = cv2.warpAffine(D, A, (w, h), flags=cv2.INTER_LINEAR); mw = cv2.warpAffine(M, A, (w, h), flags=cv2.INTER_LINEAR)
    b, gg, r = [f[..., i].astype(np.int32) for i in range(3)]
    red = ((r > 140) & (gg < 90) & (b < 100)).astype(np.uint8)
    red = cv2.dilate(red, np.ones((5, 5), np.uint8)).astype(np.float32)
    m = (mw * (1 - red))[..., None]
    out.append(np.clip(f.astype(np.float32) + dw * m, 0, 255).astype(np.uint8))
    if k % 50 == 0: print(k, round(cc, 4), W.round(4).tolist(), flush=True)
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", "30", "-i", "-", *ENC_VF,
                      "-c:v", "libx264", "-crf", "12", "-preset", "medium", *ENC_TAG, "e19_cuadro_12_palabras_fix.mp4"], stdin=subprocess.PIPE)
for f in out: p.stdin.write(f.tobytes())
p.stdin.close(); p.wait()
for k in (0, 120, 254): cv2.imwrite(f"chk_{k}.png", out[k])
print("ok", len(out))
