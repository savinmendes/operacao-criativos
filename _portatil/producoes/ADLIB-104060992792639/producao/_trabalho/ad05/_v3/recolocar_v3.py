# -*- coding: utf-8 -*-
"""v3: parte da base_lipsync da v2 (_v2/base_lipsync_v2.mp4: blocos aprovados + trechos cobertos) e troca os quadros
dos blocos refeitos: quadro da base limpa (LaMa) + SÓ a parte de baixo do rosto (nariz-queixo) do out/fx_<id>.mp4,
desfazendo o recorte (escala de volta) e com borda suave. Emendas da mesma tomada: crossfade de 2 quadros na boca.
Saída: ../base_lipsync.mp4 (24 fps, bt709 tv)."""
import json, subprocess, sys
from pathlib import Path
import cv2, numpy as np
V = Path(__file__).parent; AD = V.parent
USAR = sys.argv[1].split(",") if len(sys.argv) > 1 else ["m1","m3a","m3b","m4a","m4b","m5","d1","d2a","d2b"]
B = {k["id"]: k for k in json.load(open(V/"blocos_v3.json", encoding="utf-8"))}
def ler(p):
    c = cv2.VideoCapture(str(p)); fr = []
    while True:
        ok, f = c.read()
        if not ok: break
        fr.append(f)
    return fr
def mascara(p, shape, s):
    lab = (p[13] + p[14]) / 2; queixo = p[152]; nariz = p[4]
    c = (nariz + queixo) / 2
    ax = int(0.85 * np.linalg.norm(p[61] - p[291]) + 6 * s); ay = int(0.62 * np.linalg.norm(queixo - nariz) + 8 * s)
    m = np.zeros(shape[:2], np.float32)
    cv2.ellipse(m, (int(c[0]), int(c[1])), (ax, ay), 0, 0, 360, 1.0, -1)
    return cv2.GaussianBlur(m, (0, 0), max(3, ax / 5))
novo = {}
EMENDAS = {739, 1025, 1474, 1573}   # emendas sem corte de câmera
for i in USAR:
    k = B[i]; n = k["b"] - k["a"]; fr = ler(V/"out"/f"fx_{i}.mp4"); P = np.load(V/"out"/f"fx_{i}.npy")
    assert len(fr) == n, (i, len(fr), n)
    x, y, w, h = k.get("crop", (0, 0, 720, 1280)); s = w / 720
    for j in range(n):
        p = P[j]
        if not np.isfinite(p).all(): p = None
        novo[k["a"] + j] = (i, fr[j], p, (x, y, w, h), s)
lama = cv2.VideoCapture(str(AD/"base_sem_legenda_lama.mp4")); v2 = cv2.VideoCapture(str(V/"base_v2_rgb.mkv"))
N = int(lama.get(7))
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","24","-i","-",
    "-c:v","libx264","-crf","13","-preset","medium","-pix_fmt","yuv420p","-threads","4",*COR,"-an",str(AD/"base_lipsync.mp4")], stdin=subprocess.PIPE)
prev = None; semrosto = []
for q in range(N):
    ok1, fl = lama.read(); ok2, f2 = v2.read()
    if q in novo:
        i, g, p, (x, y, w, h), s = novo[q]
        out = fl.copy()
        gs = cv2.resize(g, (w, h), interpolation=cv2.INTER_AREA)
        if p is None:
            semrosto.append(q); out[y:y+h, x:x+w] = gs  # sem marcos: recorte inteiro (raro)
        else:
            m = mascara(p * s, (h, w), s)[..., None]
            out[y:y+h, x:x+w] = np.clip(gs * m + fl[y:y+h, x:x+w] * (1 - m), 0, 255).astype(np.uint8)
        # emenda dentro da mesma tomada entre blocos refeitos: 2 quadros de crossfade
        if prev is not None and prev[0] != i and prev[1] == q - 1 and q in EMENDAS:
            out = cv2.addWeighted(out, 2/3, prev[2], 1/3, 0)
        prev = (i, q, out.copy()); f = out
    else:
        f = f2
    ff.stdin.write(np.ascontiguousarray(f).tobytes())
ff.stdin.close(); ff.wait(); print("ok", N, "sem rosto:", semrosto[:20], len(semrosto))
