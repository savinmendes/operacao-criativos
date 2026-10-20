# -*- coding: utf-8 -*-
"""Versão A (v4): gancho com punch-in 130% no murro + PiP da mulher só depois do impacto.
Base: abertura_v2/briga_limpa.mp4 (sem PiP) + PiP refeito do HeyGen (hg_low.mp4, mesmo alfa/posição do compor_abertura.py)
e o áudio do react_briga.mp4 copiado sem mexer. Saída: final_A/abertura/react_briga_A.mp4 (720x840, cor bt601 fixa).
Uso: python abertura_A.py"""
import sys, json, subprocess
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG
AQ = Path(__file__).resolve().parent; AB = AQ.parent / "abertura_v2"; OUTD = AQ / "abertura"; OUTD.mkdir(exist_ok=True)
sys.path.insert(0, str(AB))
FPS, WW, WH = 30, 720, 840
ZOOM, CX, CY = 1.30, 330, 400          # centro do impacto (coord. da janela 720x840)
Q_ZOOM_FIM = 60                         # 0..59 em 130 % (0-2,0 s), depois volta ao 100 % (corte seco)
Q_PIP_INI = 40                          # PiP entra em 1,33 s (depois do murro, objetos voando)
C = json.loads((AB / "cfg.json").read_text(encoding="utf-8")); PIP = C["pip"]; NR = C["react"]["quadros"]
HG = AB.parents[2] / "v2" / "_trabalho" / "react" / "w" / "hg_low.mp4"


def run(c):
    r = subprocess.run([str(x) for x in c], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode: print(r.stderr[-3000:]); sys.exit(1)
    return r


def alfa(f):          # igual ao compor_abertura.alfa (chroma verde do HeyGen)
    x = f.astype(np.float32); b, g, r = x[..., 0], x[..., 1], x[..., 2]
    a = 1 - np.clip((g - np.maximum(r, b) - 18) / (70 - 18), 0, 1)
    a = cv2.GaussianBlur(cv2.erode(a, np.ones((3, 3), np.uint8)), (0, 0), 0.9)
    lim = np.maximum(r, b) + 4; x[..., 1] = np.where(g > lim, lim, g)
    return x, a


def zoom(f):
    sw, sh = round(WW * ZOOM), round(WH * ZOOM)
    z = cv2.resize(f, (sw, sh), interpolation=cv2.INTER_LANCZOS4)
    x0 = int(np.clip(CX * ZOOM - WW / 2, 0, sw - WW)); y0 = int(np.clip(CY * ZOOM - WH / 2, 0, sh - WH))
    return z[y0:y0 + WH, x0:x0 + WW]


def main():
    base = list(quadros(AB / "briga_limpa.mp4", 0, None, WW, WH)); N = len(base)
    t30 = OUTD / "hg30.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", HG, "-vf", f"fps={FPS}", "-c:v", "libx264", "-crf", "8", "-preset", "fast", "-an", t30])
    tk = [cv2.resize(f, (PIP["w"], PIP["h"]), interpolation=cv2.INTER_AREA) for f in quadros(t30)]
    tk += [tk[-1]] * max(0, NR - len(tk))
    x0, y0, w, h = PIP["x"], PIP["y"], PIP["w"], PIP["h"]; out = []
    for q, o in enumerate(base):
        if q < Q_ZOOM_FIM: o = zoom(o)
        if Q_PIP_INI <= q < NR:
            fg, a = alfa(tk[q]); A = np.zeros((WH, WW), np.float32); F = np.zeros((WH, WW, 3), np.float32)
            hh = min(h, WH - y0); A[y0:y0 + hh, x0:x0 + w] = a[:hh]; F[y0:y0 + hh, x0:x0 + w] = fg[:hh]; A[:, PIP["xc"]:] = 0
            if q < Q_PIP_INI + 4: A *= (q - Q_PIP_INI + 1) / 5          # entrada do PiP em 4 quadros
            o = np.clip(F * A[..., None] + o.astype(np.float32) * (1 - A[..., None]), 0, 255).astype(np.uint8)
        out.append(o)
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{WW}x{WH}", "-r", str(FPS), "-i", "-",
                           "-i", str(AB / "react_briga.mp4"), "-map", "0:v", "-map", "1:a", "-c:a", "copy",
                           *ENC_VF, "-c:v", "libx264", "-crf", "14", "-preset", "medium", *ENC_TAG, "-frames:v", str(N),
                           str(OUTD / "react_briga_A.mp4")], stdin=subprocess.PIPE)
    for f in out: ff.stdin.write(f.tobytes())
    ff.stdin.close(); ff.wait()
    # conferência de cor: luma média do quadro 100 (sem zoom/PiP) original x novo
    a = next(quadros(AB / "react_briga.mp4", 100, 1, WW, WH)); b = next(quadros(OUTD / "react_briga_A.mp4", 100, 1, WW, WH))
    print("react_briga_A", N, "quadros; luma q100 orig/novo", round(float(a.mean()), 2), round(float(b.mean()), 2))


if __name__ == "__main__":
    main()
