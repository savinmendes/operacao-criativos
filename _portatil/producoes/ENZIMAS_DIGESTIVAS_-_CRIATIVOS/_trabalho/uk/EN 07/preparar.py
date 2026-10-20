# -*- coding: utf-8 -*-
"""Entrada do HeyGen por trecho: recorte 9:16 que segue o rosto da creator (caixas_<seg>.npy), 2x -> 720x1280,
com o AUDIO ORIGINAL do trecho. Leitura/gravacao de cor exatas (comum3). Uso: python preparar.py"""
import json, subprocess, cv2, numpy as np
from pathlib import Path
from comum3 import quadros, ENC_VF, ENC_TAG
AQ = Path(__file__).parent
SRC = AQ.parent.parent.parent / "INGLES" / "EN 07 - ENZIMAS-DUELO-DE-ENZIMAS-V2.mp4"
R = json.load(open(AQ / "rostos.json"))
SEGS = [("A", 603, 727)]
import sys
if len(sys.argv) > 1: SEGS = [s for s in SEGS if s[0] in sys.argv[1:]]
CW, CH = 360, 640
def suav(v, k=7):
    p = np.pad(v, (k // 2, k // 2), mode="edge"); return np.convolve(p, np.ones(k) / k, mode="valid")
for nm, a, b in SEGS:
    n = b - a; F = []; prev = None
    for q in range(a, b):
        fs = [f for f in R.get(str(q), []) if f[4] < 360]
        if prev is not None and fs: fs.sort(key=lambda f: abs(f[4] - prev[4]) + abs(f[5] - prev[5]))
        F.append(fs[0] if fs else None)
        if fs: prev = fs[0]
    idx = [i for i, f in enumerate(F) if f is not None]
    A = np.array([F[i] for i in idx])
    full = np.stack([np.interp(range(n), idx, A[:, j]) for j in range(7)], 1)
    x0, y0, x1, y1, mx, my = [full[:, j] for j in range(6)]
    cx = suav((x0 + x1) / 2); cy = suav((y0 + y1) / 2)
    bx = np.clip(cx - CW / 2, 0, 720 - CW); by = np.clip(cy - CH * 0.42, 0, 1280 - CH)
    fw = suav(x1 - x0, 5); fh = suav(y1 - y0, 5)
    C = np.stack([bx, by, np.full(n, CW), np.full(n, CH), suav(mx, 3), suav(my, 3), fw, fh], 1)
    np.save(AQ / f"caixas_{nm}.npy", C)
    tmp = AQ / "in" / f"_v_{nm}.mp4"
    ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",
        *ENC_VF,"-threads","4","-c:v","libx264","-crf","12","-preset","medium",*ENC_TAG,str(tmp)], stdin=subprocess.PIPE)
    for k, f in enumerate(quadros(SRC, a, n)):
        X, Y = C[k, 0], C[k, 1]
        M = np.float32([[720 / CW, 0, -X * 720 / CW], [0, 1280 / CH, -Y * 1280 / CH]])
        ff.stdin.write(cv2.warpAffine(f, M, (720, 1280), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT).tobytes())
    ff.stdin.close(); ff.wait()
    t0, d = a / 30, n / 30
    out = AQ / "in" / f"orig_{nm}.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(tmp),"-i",str(AQ / "orig.wav"),"-filter_complex",
        f"[1:a]atrim={t0:.4f}:{t0+d:.4f},asetpts=PTS-STARTPTS,apad=whole_dur={d:.4f}[a]","-map","0:v","-map","[a]",
        "-c:v","copy","-c:a","aac","-b:a","192k","-t",f"{d:.4f}",str(out)], check=True)
    tmp.unlink()
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(AQ / f"voz_{nm}.wav"),"-af",f"apad=whole_dur={d:.4f}","-t",f"{d:.4f}",
        "-ac","1","-ar","44100","-c:a","libmp3lame","-b:a","192k",str(AQ / "in" / f"novo_{nm}.mp3")], check=True)
    print(nm, n, out.stat().st_size, flush=True)
