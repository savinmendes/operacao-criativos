# -*- coding: utf-8 -*-
"""Compõe o take HeyGen (mulher em fundo verde) no PiP do react, sobre a rua sem a mulher antiga (w/rua.mp4).
Caixa: take 720x1280 -> R=(0,500,405,720) do quadro 720x1280; recorte vertical em x<378 e y<1220 (borda do PiP original).
Saídas: take_react.mp4 (720x1280, 30 fps, N quadros, com voz L01) + w/pip_<tag>.mp4 (só a mulher com alfa pré-mult. p/ debug).
Uso: python compor.py heygen.mp4 [saida.mp4]"""
import sys, json, subprocess
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG
AQ = Path(__file__).resolve().parent; W = AQ / "w"
SRC = Path(sys.argv[1]); OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else AQ / "take_react.mp4"
VOZ = AQ.parents[2] / "_trabalho" / "voz" / "c" / "L01.wav"
R = (0, 500, 405, 720); XC, YC = 378, 1220; FPS = 30
DUR = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(VOZ)],
                           capture_output=True, text=True).stdout)
N = round(DUR * FPS)
# take -> 30 fps na escala da caixa
t30 = W / "take30.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(SRC), "-vf", f"fps={FPS}",
                "-c:v", "libx264", "-crf", "10", "-preset", "fast", "-an", str(t30)], check=True)


def alfa(f):
    """chroma verde: alfa por (G - max(R,B)), despill no verde, borda suave."""
    x = f.astype(np.float32); b, g, r = x[..., 0], x[..., 1], x[..., 2]
    d = g - np.maximum(r, b)
    a = 1 - np.clip((d - 18) / (70 - 18), 0, 1)
    a = cv2.erode(a, np.ones((3, 3), np.uint8))
    a = cv2.GaussianBlur(a, (0, 0), 0.9)
    lim = np.maximum(r, b) * 1.0 + 4
    x[..., 1] = np.where(g > lim, lim, g)                      # despill
    return x, a


ruas = list(quadros(str(W / "rua.mp4"), 0, N))
tk = [cv2.resize(f, (R[2], R[3]), interpolation=cv2.INTER_AREA) for f in quadros(str(t30))]
if len(tk) < N: tk += [tk[-1]] * (N - len(tk))
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "720x1280", "-r", str(FPS), "-i", "-",
                       "-i", str(VOZ), "-map", "0:v", "-map", "1:a", *ENC_VF, "-c:v", "libx264", "-crf", "14", "-preset", "medium", *ENC_TAG,
                       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-t", f"{N / FPS:.4f}", str(OUT)], stdin=subprocess.PIPE)
x0, y0, w, h = R
for q in range(N):
    o = ruas[min(q, len(ruas) - 1)].astype(np.float32)
    fg, a = alfa(tk[q])
    A = np.zeros((1280, 720), np.float32); F = np.zeros((1280, 720, 3), np.float32)
    A[y0:y0 + h, x0:x0 + w] = a; F[y0:y0 + h, x0:x0 + w] = fg
    A[:, XC:] = 0; A[YC:] = 0
    o = F * A[..., None] + o * (1 - A[..., None])
    ff.stdin.write(np.clip(o, 0, 255).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait()
json.dump(dict(N=N, dur=DUR), open(W / "compor_info.json", "w"))
print("ok", OUT, N, f"{N / FPS:.3f}s")
