# -*- coding: utf-8 -*-
"""Monta o EN 04 UK: original quadro a quadro (cor exata, comum3) + boca/queixo do HeyGen no trecho C (q990-1061,
quadro inteiro com a legenda apagada por LaMa, elipse na boca seguindo os landmarks, correcao de desvio de cor fora da boca) + legenda queimada
restaurada do original por cima + trilha audio_uk.wav. Crossfade de 2 quadros nas emendas sem corte de camera.
Uso: python montar.py [q_pular...]  (quadros em que a boca esta coberta: fica o original)"""
import subprocess, json, sys, cv2, numpy as np
from pathlib import Path
from comum3 import quadros, ler, reamostrar, ENC_VF, ENC_TAG
def colar(base, g, c):
    """igual ao comum3.colar, com elipse menor (rosto muito grande neste video: so boca e queixo)"""
    x0, y0, w, h, mx, my, fw, fh = c
    M = np.float32([[w / 720, 0, x0], [0, h / 1280, y0]])
    full = cv2.warpAffine(g, M, (720, 1280), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    m = np.zeros((1280, 720), np.float32)
    cv2.ellipse(m, (int(mx), int(my + 0.05 * fh)), (int(0.24 * fw), int(0.17 * fh)), 0, 0, 360, 1.0, -1)
    m = cv2.GaussianBlur(m, (0, 0), max(3, 0.05 * fw))[..., None]
    return np.clip(full * m + base * (1 - m), 0, 255).astype(np.uint8)
AQ = Path(__file__).parent
SRC = AQ.parent.parent.parent / "INGLES" / "EN 04 - ENZIMAS-BARRIGA-POS-RESTAURANTE.mp4"
DST = AQ.parent.parent.parent / "UK" / "EN 04 - ENZIMAS-BARRIGA-POS-RESTAURANTE - UK.mp4"
a, b = 990, 1062; n = b - a; S, OX, OY = 1.0, 0, 0  # quadro inteiro sem legenda (sem_legenda.py)
PULAR = set()
for s in sys.argv[1:]:
    x, y = (s.split("-") + [s])[:2]; PULAR |= set(range(int(x), int(y) + 1))
R = json.load(open(AQ / "rostos.json"))
def suav(v, k=3):
    p = np.pad(v, (k // 2, k // 2), mode="edge"); return np.convolve(p, np.ones(k) / k, mode="valid")
F = np.array([R[str(q)][0] if R.get(str(q)) else [np.nan] * 7 for q in range(a, b)], float)
idx = np.where(~np.isnan(F[:, 0]))[0]
F = np.stack([np.interp(range(n), idx, F[idx, j]) for j in range(7)], 1)
C = np.stack([np.full(n, -OX / S), np.full(n, -OY / S), np.full(n, 720 / S), np.full(n, 1280 / S), suav(F[:, 4]), suav(F[:, 5]),
              suav(F[:, 2] - F[:, 0]), suav(F[:, 3] - F[:, 1])], 1)
g = ler(AQ / "out" / "ls_C.mp4"); m = len(g); g = reamostrar(g, n)
e = list(quadros(AQ / "in" / "orig_C.mp4"))
d = []
for k in range(0, n, 6):
    x = (e[k].astype(np.float32) - g[k].astype(np.float32))
    d.append(np.concatenate([x[20:200].reshape(-1, 3), x[1100:1260].reshape(-1, 3)]).mean(0))
dv = np.median(d, 0); g = [np.clip(f.astype(np.float32) + dv, 0, 255).astype(np.uint8) for f in g]
print("HeyGen", m, "->", n, "quadros; desvio BGR", dv.round(2), flush=True)
# legenda queimada (branca, fixa): pixels claros em >=90% dos quadros do trecho
eo = list(quadros(SRC, a, n)); st = np.stack([f.min(2) for f in eo[::3]]); leg = ((st > 215).mean(0) > 0.9).astype(np.uint8)
leg[:500] = 0; leg[760:] = 0
leg = cv2.dilate(leg, np.ones((5, 5), np.uint8)).astype(np.float32)
leg = cv2.GaussianBlur(leg, (0, 0), 1.0)[..., None]
print("pixels de legenda", int((leg > 0.5).sum()))
DST.parent.mkdir(exist_ok=True)
tmp = AQ / "video_uk_sem_audio.mp4"
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",
    *ENC_VF,"-threads","4","-c:v","libx264","-crf","18","-preset","slow","-pix_fmt","yuv420p",*ENC_TAG,"-an",str(tmp)], stdin=subprocess.PIPE)
prev_out = prev_base = prev_dono = None; log = []
for i, fb in enumerate(quadros(SRC)):
    if a <= i < b and i not in PULAR:
        out = colar(fb, g[i - a], C[i - a]); out = np.clip(fb * leg + out * (1 - leg), 0, 255).astype(np.uint8); dono = "A"
    else:
        out = fb; dono = None
    if prev_out is not None and dono != prev_dono:
        corte = np.abs(fb.astype(np.float32) - prev_base).mean() > 10
        if not corte:
            L, Rr = prev_out.astype(np.float32), out.astype(np.float32)
            prev_out = np.clip(L * 2 / 3 + Rr / 3, 0, 255).astype(np.uint8); out = np.clip(L / 3 + Rr * 2 / 3, 0, 255).astype(np.uint8)
        log.append(f"emenda q{i} ({i/30:.2f}s): {'corte' if corte else 'crossfade 2q'}")
    if prev_out is not None: ff.stdin.write(prev_out.tobytes())
    prev_out, prev_base, prev_dono = out, fb.astype(np.float32), dono
ff.stdin.write(prev_out.tobytes()); ff.stdin.close(); ff.wait()
print("\n".join(log), "| quadros", i + 1)
subprocess.run(["ffmpeg","-v","error","-y","-i",str(tmp),"-i",str(AQ / "audio_uk.wav"),"-map","0:v","-map","1:a","-c:v","copy",
    "-c:a","aac","-b:a","128k","-ar","44100","-movflags","+faststart",str(DST)], check=True)
print("ok", DST, DST.stat().st_size)
