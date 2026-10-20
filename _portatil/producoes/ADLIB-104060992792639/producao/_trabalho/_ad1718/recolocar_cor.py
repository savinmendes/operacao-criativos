# -*- coding: utf-8 -*-
"""Lote C, correcao de cor AD 17/18 (sem credito HeyGen): refaz a base_lipsync.mp4 numa geracao so, a partir de
base_sem_legenda.mp4 + saidas do HeyGen ja baixadas, com a leitura/gravacao exata do ad13/lipsync3/comum3.py.
1) cor global: a base_sem_legenda ficou mais escura que o original pelas passadas antigas (cv2 bt709 x encoder bt601).
   Ajusta uma afim BGR (3x4, robusta) base -> original (ambos lidos com bt601 exato) e aplica em todos os quadros.
2) cor de cada trecho do HeyGen: afim BGR robusta saida -> base corrigida, medida no recorte FORA da elipse da boca.
3) estender/fechar_crop refeitos em memoria (sem arquivo intermediario); emenda s06b e flash do AD 18 refeitos aqui.
Uso: python recolocar_cor.py 17|18"""
import sys, json, subprocess, cv2, numpy as np
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG, colar, reamostrar
from fechar_mem import fechar
NN = sys.argv[1]; T = Path(__file__).resolve().parent.parent; AD = T / f"ad{NN}"; AQ = AD / "lipsync"
ORI = T.parent.parent / "UNICOS_HD" / f"{NN}.mp4"
CFG = json.loads((AQ / "segs.json").read_text()); FPS = CFG["fps"]; SEGS = CFG["segs"]
BASE = AD / "base_sem_legenda.mp4"; NT = int(cv2.VideoCapture(str(BASE)).get(7))
# fonte de cada trecho: (arquivo em out/, quadros extras da base no fim, audio do fechar ou None)
FONTE = {"17": {"s00": ("ls_s00_loteB.mp4", 0, None), "s11": ("ls_s11.mp4", 0, AQ / "in" / "es_s11.mp3")},
         "18": {"s00": ("ls_s00.mp4", 14, AQ / "out" / "_es_s00.wav")}}[NN]
FLASH = (283, 293) if NN == "18" else None
def fonte(nm): return FONTE.get(nm, (f"ls_{nm}.mp4", 0, None))
def caixas(s): return np.load(AQ / s.get("cx", f"caixas_{s['nome']}.npy"))
def warp_crop(f, x0, y0, w, h):
    M = np.float32([[720 / w, 0, -x0 * 720 / w], [0, 1280 / h, -y0 * 1280 / h]])
    return cv2.warpAffine(f, M, (720, 1280), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
def mask_crop(c):
    """pixels validos do recorte: anel entre 1,3x e 2,8x a elipse colada (pele do rosto, fora da boca), sem 24 px de borda"""
    x0, y0, w, h, mx, my, fw, fh = c; s = 720 / w
    M = np.float32([[s, 0, -x0 * s], [0, 1280 / h, -y0 * 1280 / h]])
    v = cv2.warpAffine(np.ones((1280, 720), np.float32), M, (720, 1280), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT) > 0.5
    c = (int((mx - x0) * s), int((my + 0.02 * fh - y0) * s)); ax = (0.40 * fw * s, 0.30 * fh * s)
    e = np.zeros((1280, 720), np.uint8); cv2.ellipse(e, c, (int(ax[0] * 1.3), int(ax[1] * 1.3)), 0, 0, 360, 1, -1)
    fora = np.zeros((1280, 720), np.uint8); cv2.ellipse(fora, c, (int(ax[0] * 2.8), int(ax[1] * 2.8)), 0, 0, 360, 1, -1)
    m = v & (e == 0) & (fora > 0); m[:24] = m[-24:] = False; m[:, :24] = m[:, -24:] = False   # anel de pele em volta da elipse
    return m
def ajustar(X, Y, it=4):
    X = X.astype(np.float64); Y = Y.astype(np.float64); Xa = np.c_[X, np.ones(len(X))]; ok = np.ones(len(X), bool)
    for _ in range(it):
        A, *_ = np.linalg.lstsq(Xa[ok], Y[ok], rcond=None); r = np.linalg.norm(Xa @ A - Y, axis=1)
        ok = r < max(3.0, 2.5 * np.median(r[ok]))
    return A, float(np.median(r[ok])), ok.mean()
def aplicar(A, f):
    return np.clip(f.reshape(-1, 3).astype(np.float32) @ A[:3].astype(np.float32) + A[3].astype(np.float32) + 0.5, 0, 255).reshape(f.shape).astype(np.uint8)
def baixa(f): return cv2.resize(f, (360, 640), interpolation=cv2.INTER_AREA)

# ---------- passada 1 (so leitura): amostras da cor global e dos recortes
amg = [int(x) for x in np.linspace(6, NT - 7, 48)]
if FLASH: amg = [x for x in amg if not (FLASH[0] - 2 <= x <= FLASH[1] + 2)]
SI = {}
for s in SEGS:
    nm = s["nome"]; arq, ext, _ = fonte(nm); n = s["b"] - s["a"]; nh = int(cv2.VideoCapture(str(AQ / "out" / arq)).get(7))
    nreal = min(n, nh) if ext == 0 else min(n - ext, nh)
    SI[nm] = dict(s=s, a=s["a"], arq=arq, ext=ext, n=n, nh=nh, nreal=nreal, am=list(range(0, nreal, 6)))
    print(nm, arq, "quadros HeyGen", nh, "| trecho", n, "| extra", ext)
pedidos = {}
for nm, d in SI.items():
    for j in d["am"]: pedidos.setdefault(d["a"] + j, []).append((nm, j))
G, CR = {}, {}
for i, f in enumerate(quadros(BASE)):
    if i in amg: G[i] = f
    for nm, j in pedidos.get(i, []):
        c = caixas(SI[nm]["s"])[j]; CR[(nm, j)] = (baixa(warp_crop(f, *c[:4])), baixa(mask_crop(c).astype(np.uint8)) > 0)
O = {}
need = set(i + o for i in amg[:6] for o in range(-2, 3)) | set(amg)
for i, f in enumerate(quadros(ORI, 0, NT + 3)):
    if i in need: O[i] = f
def dif(a, b):
    a = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY).astype(float); b = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY).astype(float)
    return np.abs((a - a.mean()) - (b - b.mean())).mean()
for o in range(-2, 3):
    print("alinhamento base x original: deslocamento", o, "dif", round(np.mean([dif(G[i], O[i + o]) for i in amg[:6] if i + o in O]), 2))
X = np.vstack([G[i][::3, ::3].reshape(-1, 3) for i in amg]); Y = np.vstack([O[i][::3, ::3].reshape(-1, 3) for i in amg])
AG, res, frac = ajustar(X, Y)
print("cor global base->original (BGR, linhas B G R 1):\n", AG.round(4), "\n residuo mediano", round(res, 2), "inliers", round(frac, 3))
Xc = aplicar(AG, X.reshape(-1, 1, 3)).reshape(-1, 3).astype(float); yb = Y @ np.array([0.114, 0.587, 0.299])
for lo, hi in [(0, 60), (60, 120), (120, 180), (180, 256)]:
    k = (yb >= lo) & (yb < hi)
    if k.sum(): print(f"  luma {lo}-{hi}: base-orig antes {(X[k]-Y[k]).mean(0).round(1)} depois {(Xc[k]-Y[k]).mean(0).round(1)}")
np.save(Path(__file__).parent / f"cor_global_{NN}.npy", AG)
del G, O, X, Y, Xc
HG = {}
for nm, d in SI.items():
    want = set(d["am"])
    for j, f in enumerate(quadros(AQ / "out" / d["arq"], 0, d["nreal"])):
        if j in want: HG[(nm, j)] = baixa(f)
AS = {}
for nm, d in SI.items():
    Xs, Ys = [], []
    for j in d["am"]:
        crop, m = CR[(nm, j)]; tgt = aplicar(AG, crop); Xs.append(HG[(nm, j)][m]); Ys.append(tgt[m])
    Xs, Ys = np.vstack(Xs)[::2], np.vstack(Ys)[::2]
    A, r, fr = ajustar(Xs, Ys); AS[nm] = A
    print(f"{nm}: HeyGen - alvo (BGR) antes {(Xs.astype(float)-Ys).mean(0).round(1)} | residuo {r:.2f} inliers {fr:.2f}", flush=True)
del HG, CR

# ---------- passada 2: gera a base_lipsync.mp4 (uma gravacao so)
porA = {d["a"]: nm for nm, d in SI.items()}
out_p = AD / "base_lipsync.mp4"
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",str(FPS),"-i","-",
    *ENC_VF,"-threads","4","-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",*ENC_TAG,"-an",str(out_p)], stdin=subprocess.PIPE)
buf = []   # atraso de 12 quadros (flash e crossfade mexem em quadros ja feitos)
def emitir(final=False):
    while len(buf) > (0 if final else 12): ff.stdin.write(buf.pop(0)[1].tobytes())
def flash_se_preciso(i):
    if FLASH and i == FLASH[1]:
        idx = {q: k for k, (q, _) in enumerate(buf)}
        A_, B_ = buf[idx[FLASH[0]]][1].astype(np.float32), buf[idx[FLASH[1]]][1].astype(np.float32)
        for q in range(FLASH[0] + 1, FLASH[1]):
            t = (q - FLASH[0]) / (FLASH[1] - FLASH[0]); src = A_ if t < 0.5 else B_; w = 0.92 * np.sin(np.pi * t)
            buf[idx[q]] = (q, np.clip(src * (1 - w) + np.array([235, 245, 250], np.float32) * w, 0, 255).astype(np.uint8))
        print("  flash", FLASH, flush=True)
cur = None; gs = C = None; acum = []
for i, fb in enumerate(quadros(BASE)):
    fb = aplicar(AG, fb)
    if i in porA:
        cur = porA[i]; d = SI[cur]; C = caixas(d["s"]); aud = fonte(cur)[2]
        g = [aplicar(AS[cur], f) for f in quadros(AQ / "out" / d["arq"])]
        if d["ext"]:
            gs = g[:d["nreal"]]; acum = []      # completa com a base quando os quadros chegarem
        else:
            m0 = len(g)
            gs = fechar(g, aud, FPS)[:d["n"]] if aud is not None else reamostrar(g, d["n"])
            print(cur, m0, "->", len(gs), "quadros", "(fechar em memoria)" if aud is not None else "", flush=True)
    if cur is not None and i >= SI[cur]["a"] + SI[cur]["n"]: cur = None
    if cur is None:
        buf.append((i, fb)); flash_se_preciso(i); emitir(); continue
    d = SI[cur]; j = i - d["a"]
    if d["ext"]:
        acum.append(fb)
        if j >= d["nreal"]: gs.append(warp_crop(fb, *C[d["nreal"] - 1][:4]))
        if j == d["n"] - 1:
            seq = fechar(gs, fonte(cur)[2], FPS)
            print(cur, d["nreal"], "+", d["ext"], "->", len(seq), "quadros (estender + fechar em memoria)", flush=True)
            for k, (b0, gk) in enumerate(zip(acum, seq)):
                buf.append((d["a"] + k, colar(b0, gk, C[k]))); flash_se_preciso(d["a"] + k); emitir()
            acum = []
        continue
    out = colar(fb, gs[j], C[j])
    if j == 0 and d["s"].get("emenda") and buf:
        L, R = buf[-1][1].astype(np.float32), out.astype(np.float32)
        buf[-1] = (buf[-1][0], np.clip(L * 2 / 3 + R / 3, 0, 255).astype(np.uint8)); out = np.clip(L / 3 + R * 2 / 3, 0, 255).astype(np.uint8)
        print("  crossfade 2q em", i, flush=True)
    buf.append((i, out)); flash_se_preciso(i); emitir()
emitir(True); ff.stdin.close(); ff.wait(); print("ok quadros", NT, "->", out_p)
