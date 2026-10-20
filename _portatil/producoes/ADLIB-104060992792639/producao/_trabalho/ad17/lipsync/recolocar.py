# -*- coding: utf-8 -*-
"""Cola as saidas do HeyGen (recorte que segue o rosto) de volta na base sem legenda, so numa elipse na parte de baixo
do rosto (boca/queixo), com borda suave. Usa os N primeiros quadros (trechos completados ate 3 s); se vier com menos,
REAMOSTRA no tempo (interpolacao). Uso: python lipsync/recolocar.py [seg=arquivo[@k] ...]  (sem arquivo -> out/ls_<seg>.mp4;
seg=- mantem a base). Saida: base_lipsync.mp4 (sem audio, bt709 tv)."""
import json, sys, subprocess, cv2, numpy as np
from pathlib import Path
AQ = Path(__file__).parent; AD = AQ.parent
CFG = json.loads((AQ / "segs.json").read_text()); FPS = CFG["fps"]
troca = dict(a.split("=", 1) for a in sys.argv[1:])
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
def ler(p, pula=0):
    cap = cv2.VideoCapture(str(p)); fr = []
    while True:
        ok, f = cap.read()
        if not ok: break
        fr.append(f)
    return fr[pula:]
def reamostrar(fr, n):
    m = len(fr)
    if m >= n: return fr[:n]
    out = []
    for i in range(n):
        x = i * (m - 1) / (n - 1); j = int(np.floor(x)); a = x - j
        out.append(fr[-1] if j >= m - 1 else (fr[j] if a < 1e-3 else cv2.addWeighted(fr[j], 1 - a, fr[j + 1], a, 0)))
    return out
def colar(base, g, c):
    x0, y0, w, h, mx, my, fw, fh = c
    M = np.float32([[w / 720, 0, x0], [0, h / 1280, y0]])
    full = cv2.warpAffine(g, M, (720, 1280), flags=cv2.INTER_AREA if w < 720 else cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    m = np.zeros((1280, 720), np.float32)
    cv2.ellipse(m, (int(mx), int(my + 0.02 * fh)), (int(0.40 * fw), int(0.30 * fh)), 0, 0, 360, 1.0, -1)
    m = cv2.GaussianBlur(m, (0, 0), max(3, 0.07 * fw))[..., None]
    return np.clip(full * m + base * (1 - m), 0, 255).astype(np.uint8)
segs = {s["a"]: s for s in CFG["segs"]}
cap = cv2.VideoCapture(str(AD / "base_sem_legenda.mp4")); NT = int(cap.get(7))
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",str(FPS),"-i","-",
    "-threads","4","-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",*COR,"-an",str(AD / "base_lipsync.mp4")], stdin=subprocess.PIPE)
i = 0
while i < NT:
    if i in segs:
        s = segs[i]; n = s["b"] - s["a"]; nm = s["nome"]
        arq = troca.get(nm, str(AQ / "out" / f"ls_{nm}.mp4"))
        if arq == "-" or not Path(arq.split("@")[0]).exists():
            print(nm, "base (sem lipsync)")
        else:
            p, _, k = arq.partition("@"); gs = ler(p, int(k or 0)); m0 = len(gs); gs = reamostrar(gs, n)
            C = np.load(AQ / s.get("cx", f"caixas_{nm}.npy")); print(nm, m0, "->", n, flush=True)
            for k2 in range(n):
                ok, f = cap.read(); ff.stdin.write(colar(f, gs[k2], C[k2]).tobytes())
            i += n; continue
    ok, f = cap.read()
    if not ok: break
    ff.stdin.write(f.tobytes()); i += 1
ff.stdin.close(); ff.wait(); print("ok quadros", i)
