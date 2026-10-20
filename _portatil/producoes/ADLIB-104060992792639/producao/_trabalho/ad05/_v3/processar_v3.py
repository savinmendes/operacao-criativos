# -*- coding: utf-8 -*-
"""v3: trata a saída do HeyGen de cada bloco (no espaço da entrada, 720x1280):
1. reamostra no tempo para o número exato de quadros (sem congelar; m1 usa só os quadros reais);
2. FECHA A BOCA NAS PAUSAS DA VOZ ES (licão do AD 01, lipsync2/fechar.py): o HeyGen devolve a boca da entrada
   (falando PT) onde o ES está em silêncio. Em cada pausa ES >= MINQ quadros (inclui o fim depois da última palavra),
   cola a boca+queixo do quadro mais fechado do próprio trecho, alinhado por pontos estáveis, com rampa de 3 quadros.
Saída: out/fx_<id>.mp4 (mesmo espaço da entrada) + out/fx_<id>.npy (marcos por quadro) + log.
Uso: python processar_v3.py id[,id...]"""
import sys, os, json, subprocess
from pathlib import Path
import numpy as np, cv2
os.environ.setdefault("GLOG_minloglevel", "2")
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
V = Path(__file__).parent; FPS = 24
B = {k["id"]: k for k in json.load(open(V/"blocos_v3.json", encoding="utf-8"))}
MINQ, RAMPA, JAN = 5, 3, 60
ESTAVEIS = [33, 133, 362, 263, 168, 6, 197, 195, 5, 4, 1, 234, 454, 127, 356]
R = cl.Rastreador()
def ler(p):
    c = cv2.VideoCapture(str(p)); fr = []
    while True:
        ok, f = c.read()
        if not ok: break
        fr.append(f)
    return fr
def reamostrar(fr, n):
    m = len(fr)
    if m == n: return fr
    out = []
    for i in range(n):
        x = i * (m - 1) / max(1, n - 1); j = int(np.floor(x)); a = x - j
        out.append(fr[-1] if j >= m - 1 else (fr[j] if a < 1e-3 else cv2.addWeighted(fr[j], 1 - a, fr[j + 1], a, 0)))
    return out
def pausas(es_mp3, n):
    e = cl.envelope(cl.ler_audio(es_mp3), 16000, float(FPS), n)
    fal = e > np.nanmax(e) - 30
    runs, k = [], 0
    while k < n:
        if not fal[k]:
            j = k
            while j < n and not fal[j]: j += 1
            if j - k >= MINQ: runs.append((k, j))
            k = j
        else: k += 1
    return runs, fal
def mascara(p, shape):
    lab = (p[13] + p[14]) / 2; queixo = p[152]; nariz = p[2]
    c = (lab + queixo) / 2 + np.array([0, 0.05 * np.linalg.norm(queixo - nariz)])
    ax = int(0.62 * np.linalg.norm(p[61] - p[291]) + 0.03 * shape[1]); ay = int(0.62 * np.linalg.norm(queixo - nariz) + 0.01 * shape[0])
    m = np.zeros(shape[:2], np.float32)
    cv2.ellipse(m, (int(c[0]), int(c[1])), (ax, ay), 0, 0, 360, 1.0, -1)
    return cv2.GaussianBlur(m, (0, 0), max(3, ax / 6))
for i in sys.argv[1].split(","):
    k = B[i]; n = k["b"] - k["a"]
    fr = ler(V/"out"/f"ls_{i}.mp4")
    if "pad" in k: fr = fr[:n] if len(fr) >= n else reamostrar(fr, n)
    else: fr = reamostrar(fr, n)
    P = [R.pontos(f) for f in fr]
    ab = np.array([cl._abertura(p) if p is not None else np.nan for p in P])
    runs, fal = pausas(V/"in"/f"es_{i}.mp3", n)
    orig = [f.copy() for f in fr]; log = []
    for a, b in runs:
        viz = [q for q in range(max(0, a - JAN), min(n, b + JAN)) if np.isfinite(ab[q])]
        if not viz: continue
        r = min(viz, key=lambda q: ab[q]); pr = P[r]
        for q in range(a, b):
            w = min(1.0, (q - a + 1) / RAMPA, (b - q) / RAMPA) if (a > 0 and b < n) else (min(1.0, (q - a + 1) / RAMPA) if a > 0 else min(1.0, (b - q) / RAMPA) if b < n else 1.0)
            pk = P[q]
            if pk is None: continue
            M, _ = cv2.estimateAffinePartial2D(pr[ESTAVEIS].astype(np.float32), pk[ESTAVEIS].astype(np.float32))
            if M is None: continue
            g = cv2.warpAffine(orig[r], M, (fr[q].shape[1], fr[q].shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
            ms = mascara(pk, fr[q].shape)[..., None] * w
            fr[q] = np.clip(g * ms + fr[q] * (1 - ms), 0, 255).astype(np.uint8)
        log.append(f"pausa q{a}-{b} ({a/FPS:.2f}-{b/FPS:.2f}s do bloco) ref q{r} ab={ab[r]:.3f}")
    np.save(V/"out"/f"fx_{i}.npy", np.array([p if p is not None else np.full((478, 2), np.nan) for p in P]))
    h, w = fr[0].shape[:2]
    tmp = V/"out"/f"_fx_{i}.mp4"
    ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{w}x{h}","-r",str(FPS),"-i","-",
        "-c:v","libx264","-crf","13","-preset","medium","-pix_fmt","yuv420p","-threads","4",str(tmp)], stdin=subprocess.PIPE)
    for f in fr: ff.stdin.write(np.ascontiguousarray(f).tobytes())
    ff.stdin.close(); ff.wait()
    # áudio: o ES do bloco (para o checar usar a voz nova como trilha)
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(tmp),"-i",str(V/"in"/f"es_{i}.mp3"),"-map","0:v","-map","1:a","-c:v","copy","-c:a","aac",str(V/"out"/f"fx_{i}.mp4")], check=True)
    tmp.unlink()
    print(i, len(fr), "quadros |", "; ".join(log) or "sem pausa", flush=True)
