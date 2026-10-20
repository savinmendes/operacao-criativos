# -*- coding: utf-8 -*-
"""Abertura P9: take Seedance (briga no salão) com câmera lenta 0,43x nos 2,3 s da ação (para a reportera caber antes da 1ª fala),
punch-in 130 % no impacto (1,9-3,6 s), REPORTERA em PiP (chroma) no canto inf. dir. 0-5,2 s.
Saída: mont/abertura.mp4 (720x840, 30 fps, sem áudio) + mont/abertura_nat.wav (som nativo com voz STS da Lucía, câmera lenta no trecho lento)."""
import sys, json, subprocess
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG
AQ = Path(__file__).resolve().parent; M = AQ / "mont"
FPS, WW, WH = 30, 720, 840
SL, TS = 0.43, 2.3                       # câmera lenta: 0..TS s do take a SL x
Y0 = 30                                  # recorte vertical do take 720x960 -> 720x840
FIM_FALA = 9.24                          # fim de "cálmese" no take original (whisper)
T_OUT = lambda t: t / SL if t <= TS else TS / SL + (t - TS)
N = int(round((T_OUT(FIM_FALA) + 0.40) * FPS))
PIP = dict(x=470, y=396, w=250, h=444)
Z, ZDE, ZATE, ZC = 1.30, 57, 108, (300, 400)          # punch-in 130 % no impacto (secador e crucifixo batem no chão)
NFADE = 4


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
    cw, ch = WW / Z, WH / Z; x0 = min(max(ZC[0] - cw / 2, 0), WW - cw); y0 = min(max(ZC[1] - ch / 2, 0), WH - ch)
    Mz = np.float32([[Z, 0, -x0 * Z], [0, Z, -y0 * Z]])
    return cv2.warpAffine(f, Mz, (WW, WH), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)


def main():
    base = [f[Y0:Y0 + WH] for f in quadros(M / "briga_slow.mp4", 0, N, 720, 960)]
    assert len(base) == N, (len(base), N)
    t30 = M / "_hg30.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", AQ / "takes" / "hg_R00.mp4", "-vf", f"fps={FPS}", "-c:v", "libx264", "-crf", "8", "-preset", "fast", "-an", t30])
    tk = [cv2.resize(f, (PIP["w"], PIP["h"]), interpolation=cv2.INTER_AREA) for f in quadros(t30)]
    NP = len(tk); Q_SAI = NP - NFADE; out = []
    for q, o in enumerate(base):
        if ZDE <= q < ZATE: o = zoom(o)
        if q < NP:
            fg, a = alfa(tk[q]); x0, y0, w, h = PIP["x"], PIP["y"], PIP["w"], PIP["h"]
            A = np.zeros((WH, WW), np.float32); F = np.zeros((WH, WW, 3), np.float32)
            A[y0:y0 + h, x0:x0 + w] = a; F[y0:y0 + h, x0:x0 + w] = fg
            # borda branca fina da caixa (como a janela da v4): só onde há pessoa não; caixa simples sem borda
            if q >= Q_SAI: A *= 1 - (q - Q_SAI + 1) / (NFADE + 1)
            o = np.clip(F * A[..., None] + o.astype(np.float32) * (1 - A[..., None]), 0, 255).astype(np.uint8)
        out.append(o)
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{WW}x{WH}", "-r", str(FPS), "-i", "-",
                           *ENC_VF, "-c:v", "libx264", "-crf", "12", "-preset", "medium", *ENC_TAG, "-frames:v", str(N), str(M / "abertura.mp4")], stdin=subprocess.PIPE)
    for f in out: ff.stdin.write(f.tobytes())
    ff.stdin.close(); ff.wait()
    # som nativo: 0..TS lento (atempo), resto normal
    src = AQ / "voz" / "briga_sts.wav"; D = N / FPS
    run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex",
         f"[0:a]atrim=0:{TS},asetpts=PTS-STARTPTS,atempo=0.5,atempo={SL / 0.5:.4f}[s];[0:a]atrim={TS},asetpts=PTS-STARTPTS[n];[s][n]concat=n=2:v=0:a=1,aresample=48000[a]",
         "-map", "[a]", "-t", f"{D:.3f}", "-ac", "2", "-c:a", "pcm_s16le", M / "abertura_nat.wav"])
    json.dump(dict(N=N, dur=D, pip_quadros=NP, fala_off=T_OUT(0) , mapa="t_out = t/0.43 (t<=2.3) | 5.349+(t-2.3)"), open(M / "abertura.json", "w"), indent=1)
    print("abertura", N, "quadros", round(D, 2), "s; PiP", NP)


if __name__ == "__main__":
    main()
