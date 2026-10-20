# -*- coding: utf-8 -*-
"""Abertura P1 Ramón: briga Seedance (janela 720x840, take único) + REPORTERA em PiP (chroma verde, caixa do v4: 304x540 em (0,300), recorte x<284)
falando desde 0:00; punch-in 130 % no impacto (q de ZI a ZF). Só vídeo (o áudio é mixado no montar.py).
Uso: python compor_abertura.py SS DUR ZI ZF  (segundos no take Seedance / quadros do zoom no resultado) -> takes/abertura.mp4"""
import sys, subprocess
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG
AQ = Path(__file__).resolve().parent; T = AQ / "takes"; W = AQ / "w"
FPS, WW, WH = 30, 720, 840
PIP = dict(x=0, y=408, w=243, h=432, xc=227); Z = 1.30; NFADE = 4
SS, DUR, ZI, ZF = float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
CX = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5; CY = float(sys.argv[6]) if len(sys.argv) > 6 else 0.4


def run(c):
    r = subprocess.run([str(x) for x in c], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode: print(r.stderr[-3000:]); sys.exit(1)
    return r


def alfa(f):
    x = f.astype(np.float32); b, g, r = x[..., 0], x[..., 1], x[..., 2]
    a = 1 - np.clip((g - np.maximum(r, b) - 18) / (70 - 18), 0, 1)
    a = cv2.GaussianBlur(cv2.erode(a, np.ones((3, 3), np.uint8)), (0, 0), 0.9)
    lim = np.maximum(r, b) + 4; x[..., 1] = np.where(g > lim, lim, g)
    return x, a


def zoom(f):
    cw, ch = WW / Z, WH / Z; x0 = min(max(WW * CX - cw / 2, 0), WW - cw); y0 = min(max(WH * CY - ch / 2, 0), WH - ch)
    M = np.float32([[Z, 0, -x0 * Z], [0, Z, -y0 * Z]])
    return cv2.warpAffine(f, M, (WW, WH), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)


def main():
    N = round(DUR * FPS); b30 = W / "briga_30.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{SS:.3f}", "-i", T / "briga_mont.mp4", "-vf",
         f"fps={FPS},scale={WW}:{WH}:force_original_aspect_ratio=increase:flags=lanczos,crop={WW}:{WH}", "-frames:v", N, "-an",
         "-c:v", "libx264", "-crf", "8", "-preset", "fast", b30])
    base = list(quadros(b30, 0, N, WW, WH)); base += [base[-1]] * (N - len(base))
    t30 = W / "pip30.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", T / "hg_R00_pip.mp4", "-vf", f"fps={FPS}", "-c:v", "libx264", "-crf", "8", "-preset", "fast", "-an", t30])
    tk = [cv2.resize(f, (PIP["w"], PIP["h"]), interpolation=cv2.INTER_AREA) for f in quadros(t30)]
    NP = min(len(tk), int(PIP_ATE * FPS)) if PIP_ATE else len(tk); Q_SAI = NP - NFADE
    x0, y0, w, h = PIP["x"], PIP["y"], PIP["w"], PIP["h"]; out = []
    for q, o in enumerate(base):
        if ZI <= q < ZF: o = zoom(o)
        if q < NP:
            fg, a = alfa(tk[q]); A = np.zeros((WH, WW), np.float32); F = np.zeros((WH, WW, 3), np.float32)
            hh = min(h, WH - y0); A[y0:y0 + hh, x0:x0 + w] = a[:hh]; F[y0:y0 + hh, x0:x0 + w] = fg[:hh]; A[:, PIP["xc"]:] = 0
            if q >= Q_SAI: A *= 1 - (q - Q_SAI + 1) / (NFADE + 1)
            o = np.clip(F * A[..., None] + o.astype(np.float32) * (1 - A[..., None]), 0, 255).astype(np.uint8)
        out.append(o)
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{WW}x{WH}", "-r", str(FPS), "-i", "-",
                           *ENC_VF, "-c:v", "libx264", "-crf", "14", "-preset", "medium", *ENC_TAG, "-frames:v", str(N), "-an",
                           str(T / "abertura.mp4")], stdin=subprocess.PIPE)
    for f in out: ff.stdin.write(f.tobytes())
    ff.stdin.close(); ff.wait(); print("abertura", N, "quadros; PiP", NP)


PIP_ATE = 4.5     # a reportera termina a fala em 4,43 s (R00f); PiP sai em fade até 4,5 s
if __name__ == "__main__":
    main()
