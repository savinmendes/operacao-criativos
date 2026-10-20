# -*- coding: utf-8 -*-
"""Retoques locais pos-revisao (venv _vg, LaMa GPU):
1) elipse vermelha + seta (resto de animacao do original) nos 1os quadros da peca P10 -> LaMa (cenas 27 e 34);
2) adesivos com QR "...ATRAVES DO PIX" (PT) nas cadeiras do congresso -> desfoque forte (cena 28).
Leitura/gravacao bt601 fixa (comum3)."""
import sys, subprocess, shutil, warnings; warnings.filterwarnings("ignore")
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG
from PIL import Image
AQ = Path(__file__).resolve().parent; M = AQ / "mont"


def enc(path):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "720x1280", "-r", "30", "-i", "-",
                            *ENC_VF, "-c:v", "libx264", "-crf", "12", "-preset", "medium", *ENC_TAG, "-an", str(path)], stdin=subprocess.PIPE)


def elipse(arq, q0, q1):
    from simple_lama_inpainting import SimpleLama
    lama = SimpleLama(); tmp = arq.with_name(arq.stem + "_tmp.mp4"); out = enc(tmp); feitos = []
    for q, f in enumerate(quadros(arq)):
        if q0 <= q <= q1:
            hsv = cv2.cvtColor(f[120:600, 0:470], cv2.COLOR_BGR2HSV)
            red = (((hsv[..., 0] < 9) | (hsv[..., 0] > 168)) & (hsv[..., 1] > 120) & (hsv[..., 2] > 110)).astype(np.uint8)
            if red.sum() > 60:
                m = np.zeros(f.shape[:2], np.uint8); m[120:600, 0:470] = cv2.dilate(red, np.ones((11, 11), np.uint8))
                crop = f[60:660]; mk = m[60:660]
                r = lama(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)), Image.fromarray(mk * 255))
                r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:crop.shape[0], :crop.shape[1]]
                al = cv2.GaussianBlur(mk.astype(np.float32), (9, 9), 0)[..., None]; al = np.maximum(al, mk[..., None])
                f = f.copy(); f[60:660] = np.clip(r * al + crop * (1 - al), 0, 255).astype(np.uint8); feitos.append(q)
        out.stdin.write(f.tobytes())
    out.stdin.close(); out.wait(); shutil.move(str(tmp), str(arq)); print(arq.name, "elipse removida nos quadros", feitos)


def adesivos(arq):
    """caixas por quadro-chave (interpoladas) nos adesivos com QR + texto PT; desfoque forte"""
    K = {0: [(515, 740, 720, 860), (0, 990, 125, 1140)], 20: [(515, 705, 720, 820), (0, 985, 75, 1130)],
         42: [(515, 685, 720, 800), (0, 985, 45, 1130)]}
    ks = sorted(K); tmp = arq.with_name(arq.stem + "_tmp.mp4"); out = enc(tmp); n = 0
    for q, f in enumerate(quadros(arq)):
        m = np.zeros(f.shape[:2], np.float32)
        for j in range(2):
            cx = [np.interp(q, ks, [K[k][j][i] for k in ks]) for i in range(4)]
            x0, y0, x1, y1 = map(int, cx); cv2.rectangle(m, (x0, y0), (x1, y1), 1.0, -1)
        m = cv2.GaussianBlur(m, (0, 0), 4)[..., None]
        b = cv2.GaussianBlur(f, (0, 0), 12)
        f = np.clip(b * m + f * (1 - m), 0, 255).astype(np.uint8); n += 1
        out.stdin.write(f.tobytes())
    out.stdin.close(); out.wait(); shutil.move(str(tmp), str(arq)); print(arq.name, "adesivos desfocados em", n, "quadros")


def enquadra(arq, qs, qref):
    """quadros de outro take (zoom) colados no inicio da peca P10: leva o conteudo ao enquadramento do 1o quadro normal
    (afim por ECC fora das barras da moldura); bordas e barras da moldura vem do quadro de referencia"""
    F = list(quadros(arq)); ref = F[qref]; g_ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY).astype(np.float32)
    mask = np.zeros(ref.shape[:2], np.uint8); mask[140:1130, 20:700] = 255
    for q in qs:
        orb = cv2.ORB_create(4000); g1 = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY); g2 = cv2.cvtColor(F[q], cv2.COLOR_BGR2GRAY)
        k1, d1 = orb.detectAndCompute(g1, mask); k2, d2 = orb.detectAndCompute(g2, mask)
        mt = sorted(cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(d1, d2), key=lambda m: m.distance)[:600]
        p1 = np.float32([k1[m.queryIdx].pt for m in mt]); p2 = np.float32([k2[m.trainIdx].pt for m in mt])
        W, inl = cv2.estimateAffinePartial2D(p1, p2, method=cv2.RANSAC, ransacReprojThreshold=2.0)   # ref -> zoom
        w = cv2.warpAffine(F[q], W, (720, 1280), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        val = cv2.warpAffine(np.ones((1280, 720), np.float32), W, (720, 1280), flags=cv2.INTER_NEAREST + cv2.WARP_INVERSE_MAP)
        val[:135] = 0; val[1135:] = 0
        val = cv2.erode(val, np.ones((7, 7), np.uint8)); val = cv2.GaussianBlur(val, (0, 0), 3)[..., None]
        F[q] = np.clip(w * val + ref * (1 - val), 0, 255).astype(np.uint8)
        print(arq.name, "q", q, "escala ~", round(float(W[0, 0]), 3), "desl", W[:, 2].round(1).tolist())
    tmp = arq.with_name(arq.stem + "_tmp.mp4"); out = enc(tmp)
    for f in F: out.stdin.write(f.tobytes())
    out.stdin.close(); out.wait(); shutil.move(str(tmp), str(arq))


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "enquadra":
    enquadra(M / "cena_27_ls.mp4", [0, 1, 2, 3], 4)
    enquadra(M / "cena_34_ls.mp4", [107, 108, 109, 110], 111)
    sys.exit(0)

if __name__ == "__main__":
    elipse(M / "cena_27_ls.mp4", 0, 12)
    elipse(M / "cena_34_ls.mp4", 105, 120)
    adesivos(M / "cena_28.mp4")
