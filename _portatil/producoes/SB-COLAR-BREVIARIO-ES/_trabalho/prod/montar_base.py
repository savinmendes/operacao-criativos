# base final (sem audio): base_sem_legenda + tarja TV ES + lipsync colado (boca/queixo) + pagina Pellorini no lugar do Instagram
import json, sys, subprocess, cv2, numpy as np
from comum3 import quadros, ENC_VF, ENC_TAG, reamostrar
R = json.load(open("rostos.json")); CH = json.load(open("chunks2.json"))
so = set(sys.argv[1:])
def main(fs): return max(fs, key=lambda f: f[2]-f[0]) if fs else None
def rostos_interp(a, b):
    F = [main(R[q]) for q in range(a, b)]; ok = [i for i, f in enumerate(F) if f]
    A = np.array([[f[4], f[5], f[2]-f[0], f[3]-f[1]] if f else [np.nan]*4 for f in F])
    for j in range(4): A[:, j] = np.interp(np.arange(len(F)), ok, A[ok, j])
    return A
def ler_crop(p, n): return [f for f in quadros(p, 0, n, 720, 1280)]
NOVO = {}
for c in CH:
    nm, a, b = c["nome"], c["a"], c["b"]; n = b - a
    if so and nm not in so: continue
    g = ler_crop(f"ls/out/ls_{nm}.mp4", None); m = len(g)
    g = g[:max(n, 1)] if m >= n else reamostrar(g, n)
    pin = ler_crop(f"ls/in/pt_{nm}.mp4", n)
    dv = np.mean([(pin[k].astype(np.float32) - g[k].astype(np.float32))[60:420].mean(axis=(0, 1)) for k in range(0, n, max(1, n // 6))], 0)
    C = np.load(f"ls/caixas_{nm}.npy"); A = rostos_interp(a, b)
    for k in range(n): NOVO[a + k] = (g[k], dv, C[k], A[k])
    print(nm, "quadros", m, "->", n, "desvio", dv.round(2), flush=True)
def colar(base, g, dv, c, r):
    x0, y0, w, h = c; mx, my, fw, fh = r
    M = np.float32([[w / 720, 0, x0], [0, h / 1280, y0]])
    full = cv2.warpAffine(np.clip(g.astype(np.float32) + dv, 0, 255), M, (1080, 1920), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REPLICATE)
    mk = np.zeros((1920, 1080), np.float32)
    cv2.ellipse(mk, (int(mx), int(my + 0.03 * fh)), (int(0.40 * fw), int(0.30 * fh)), 0, 0, 360, 1.0, -1)
    mk = cv2.GaussianBlur(mk, (0, 0), max(3, 0.07 * fw))[..., None]
    return np.clip(full * mk + base * (1 - mk), 0, 255).astype(np.uint8)
TV = {645 + k: f for k, f in enumerate(quadros("tv/tv_trecho.mp4", 0, None, 1080, 1920))}
def pagina(t0, n): return list(quadros("../pagina/pagina_completa.mp4", int(round(t0 * 30)), n, 1080, 1920))
PAG = {}
for (qa, qb, t0) in [(3576, 3655, 6.9), (4056, 4117, 10.17)]:
    for k, f in enumerate(pagina(t0, qb - qa)): PAG[qa + k] = f
print("tv", len(TV), "pagina", len(PAG))
saida = "base_final.mp4" if not so else "base_teste.mp4"
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","1080x1920","-r","30","-i","-",*ENC_VF,
    "-threads","3","-c:v","libx264","-crf","13","-preset","medium",*ENC_TAG,"-an",saida], stdin=subprocess.PIPE)
for i, f in enumerate(quadros("base_sem_legenda.mp4", 0, None, 1080, 1920)):
    if i in TV: f = TV[i]
    if i in PAG: f = PAG[i]
    elif i in NOVO: f = colar(f, *NOVO[i])
    ff.stdin.write(np.ascontiguousarray(f).tobytes())
ff.stdin.close(); ff.wait(); print("ok", i + 1)
