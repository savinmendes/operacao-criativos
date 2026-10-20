# -*- coding: utf-8 -*-
"""Correcao de cor (REVISAO-LOTE-C) do AD 05, sem credito HeyGen: refaz base_sem_legenda_lama (= base_sem_legenda) e
base_lipsync NUMA GERACAO SO, a partir do ORIGINAL (UNICOS_HD/05.mp4), dos PNGs LaMa ja calculados (_fix/lama) e das
saidas do HeyGen ja baixadas, com a leitura/gravacao exata do ad13/lipsync3/comum3.py.
Camadas reproduzidas (mesma geometria, mesmos quadros) e onde estavam:
  1. base LaMa ............ _fix/montar_base_lama.py (mascara _fix/lama_mask.npy, borda 11, EMA 0,65 zerada nos cortes,
                            corte 1286-1355 do original). PNG corrigido por quadro: afim BGR PNG -> original fora da mascara.
  2. blocos v1 inteiros ... _v3/recolocar_v2_rgb.py: c1, m1(v1), c2, c3, d3, d4, d5 = quadro inteiro do HeyGen
                            (lipsync/ls_<id>.mp4) com a faixa da legenda de volta da base (mascara dilatada 9, borda 15).
                            Cor: afim BGR robusta saida -> base nova, por bloco, medida no quadro fora da faixa.
  3. coberturas ........... _v3/cobrir_v3.json: 87-118 (40,560,405,720), 119-160 (0,500,405,720), 196-285 (0,260,450,800).
  4. blocos v3 ............ _v3/recolocar_v3.py: base + so nariz-queixo do _v3/out/fx_<id>.mp4 (bocas ja fechadas nas pausas
                            pelo processar_v3.py) com os marcos fx_<id>.npy; crossfade em 739, 1025, 1474, 1573.
                            Cor: afim BGR robusta fx -> base no recorte FORA da elipse + ajuste interno (filtro e meio do
                            queixo) aplicado com o peso da elipse.
  5. fechar do c1 ......... _loteA/fechar_c1.py: pausa q45-75, ref q36, marcos de _cor/c1_marcos.npz (mesma entrada da rodada).
Uso (em ad05/_cor): python recolocar_cor.py"""
import sys, json, subprocess, time
from pathlib import Path
import numpy as np, cv2
C = Path(__file__).resolve().parent; AD = C.parent; T = AD.parent; P = T.parents[1]
sys.path.insert(0, str(T / "ad13" / "lipsync3"))
from comum3 import quadros, ENC_VF, ENC_TAG
ORIG = P / "UNICOS_HD" / "05.mp4"
N0, CA, CB, CN = 2368, 1286, 1356, 70; N = N0 - CN; R0, R1 = 940, 1110
MK = np.load(AD / "_fix" / "lama_mask.npy", mmap_mode="r")
L1 = AD / "lipsync"; V3 = AD / "_v3"
B1 = {k["id"]: k for k in json.load(open(L1 / "blocos.json", encoding="utf-8"))}
B3 = {k["id"]: k for k in json.load(open(V3 / "blocos_v3.json", encoding="utf-8"))}
COBRIR = json.load(open(V3 / "cobrir_v3.json", encoding="utf-8"))
V1_USAR = ["c1", "m1", "c2", "c3", "d3", "d4", "d5"]          # m3-m5, d1, d2 do v1 ficam inteiramente sob o v3
V3_USAR = ["m3a", "m3b", "m4a", "m4b", "m5", "d1", "d2a", "d2b"]  # m1 do v3 nao entrou (tomada coberta)
EMENDAS = {739, 1025, 1474, 1573}
log = []
def L(s): log.append(s); print(s, flush=True)
# ---------------------------------------------------------------- utilitarios de cor
def ajustar(X, Y, it=4):
    X = X.astype(np.float64); Y = Y.astype(np.float64); Xa = np.c_[X, np.ones(len(X))]; ok = np.ones(len(X), bool)
    for _ in range(it):
        A, *_ = np.linalg.lstsq(Xa[ok], Y[ok], rcond=None); r = np.linalg.norm(Xa @ A - Y, axis=1)
        ok = r < max(3.0, 2.5 * np.median(r[ok]))
    return A, float(np.median(r[ok])), float(ok.mean())
def aplicar(A, f):   # float32, sem arredondar (a colagem arredonda no fim)
    return (f.reshape(-1, 3).astype(np.float32) @ A[:3].astype(np.float32) + A[3].astype(np.float32)).reshape(f.shape)
# ---------------------------------------------------------------- 1) base LaMa
def base_gen():
    ema = None; prev = None; cortes = []; res = []
    for i, f in enumerate(quadros(ORIG, 0, N0)):
        g = cv2.resize(f, (90, 160)).astype(np.float32)
        if prev is not None and np.abs(g - prev).mean() > 20: ema = None; cortes.append(i)
        prev = g
        m = np.array(MK[i]).astype(np.float32)
        if m.sum() > 0:
            l = cv2.imread(str(AD / "_fix" / "lama" / f"{i:04d}.png")).astype(np.float32); roi = f[R0:R1].astype(np.float32)
            fora = cv2.dilate((m > 0).astype(np.uint8), np.ones((15, 15), np.uint8)) == 0; fora[::2] = False; fora[:, 1::2] = False
            A, r, _ = ajustar(l[fora], roi[fora], 2); res.append(r); l = aplicar(A, l)
            ema = l if ema is None else 0.65 * l + 0.35 * ema
            a = np.maximum(cv2.GaussianBlur(m, (11, 11), 0), m)[..., None]
            f[R0:R1] = np.clip(ema * a + roi * (1 - a), 0, 255).astype(np.uint8)
        else: ema = None
        if CA <= i < CB: continue
        yield f
    L(f"base: cortes (tempo do original) {cortes}; PNG LaMa -> original fora da mascara: residuo mediano {np.median(res):.2f} ({len(res)} quadros)")
def io_de(q): return q if q < CA else q + CN
# ---------------------------------------------------------------- 2) blocos v1 (quadro inteiro)
def faixa_da_base(g, f, q):
    m = cv2.dilate(np.array(MK[io_de(q)]), np.ones((9, 9), np.uint8)).astype(np.float32)
    a = np.maximum(cv2.GaussianBlur(m, (15, 15), 0), m)[..., None]
    g[R0:R1] = g[R0:R1] * (1 - a) + f[R0:R1].astype(np.float32) * a
    return g
def bloco_v1(bid, bases):
    k = B1[bid]; n = k["b"] - k["a"]; g = list(quadros(L1 / f"ls_{bid}.mp4", 0, n)); m0 = len(g)
    if len(g) < n: g += [g[-1]] * (n - len(g))
    X, Y = [], []
    for j in range(0, n, 4):
        sel = np.ones((1280, 720), bool); sel[900:1150] = False; sel[::3] = False; sel[1::3] = False; sel[:, ::2] = False
        X.append(g[j][sel]); Y.append(bases[j][sel])
    A, r, fr = ajustar(np.vstack(X), np.vstack(Y))
    d = (np.vstack(X).astype(np.float32) - np.vstack(Y)).mean(0)
    L(f"{bid} (v1 inteiro, q{k['a']}-{k['b']-1}): {m0} q HeyGen; saida-base antes {d.round(1)} BGR; afim residuo {r:.2f} inliers {fr:.2f}")
    return [np.clip(faixa_da_base(aplicar(A, g[j]), bases[j], k["a"] + j) + 0.5, 0, 255).astype(np.uint8) for j in range(n)]
# ---------------------------------------------------------------- 4) blocos v3 (nariz-queixo)
def mascara_v3(p, shape, s):   # = _v3/recolocar_v3.mascara
    queixo = p[152]; nariz = p[4]; c = (nariz + queixo) / 2
    ax = int(0.85 * np.linalg.norm(p[61] - p[291]) + 6 * s); ay = int(0.62 * np.linalg.norm(queixo - nariz) + 8 * s)
    m = np.zeros(shape[:2], np.float32)
    cv2.ellipse(m, (int(c[0]), int(c[1])), (ax, ay), 0, 0, 360, 1.0, -1)
    return cv2.GaussianBlur(m, (0, 0), max(3, ax / 5))
def bloco_v3(bid, bases):
    k = B3[bid]; n = k["b"] - k["a"]; fr = list(quadros(V3 / "out" / f"fx_{bid}.mp4")); Pm = np.load(V3 / "out" / f"fx_{bid}.npy")
    assert len(fr) == n, (bid, len(fr), n)
    x, y, w, h = k.get("crop", (0, 0, 720, 1280)); s = w / 720
    gs = [cv2.resize(f, (w, h), interpolation=cv2.INTER_AREA) for f in fr]
    ps = [(Pm[j] * s if np.isfinite(Pm[j]).all() else None) for j in range(n)]
    ms = [(mascara_v3(ps[j], (h, w), s) if ps[j] is not None else None) for j in range(n)]
    # afim fx -> base no recorte, fora da elipse (dilatada) e sem 6 px de borda
    X, Y = [], []
    for j in np.linspace(0, n - 1, 16).astype(int):
        if ms[j] is None: continue
        fora = cv2.dilate((ms[j] > 0.01).astype(np.uint8), np.ones((25, 25), np.uint8)) == 0
        fora[:6] = fora[-6:] = False; fora[:, :6] = fora[:, -6:] = False
        sub = np.zeros_like(fora); sub[::2, ::2] = True; fora &= sub
        X.append(gs[j][fora]); Y.append(bases[j][y:y + h, x:x + w][fora])
    X, Y = np.vstack(X), np.vstack(Y); A, r, fra = ajustar(X, Y); d = (X.astype(np.float32) - Y).mean(0)
    # ajuste interno (pele do filtro e do meio do queixo), depois da afim
    di = []
    for j in np.linspace(0, n - 1, 16).astype(int):
        p = ps[j]
        if p is None: continue
        fw = np.linalg.norm(p[234] - p[454]); rr = max(3, int(0.05 * fw)); full = aplicar(A, gs[j]); bb = bases[j][y:y + h, x:x + w].astype(np.float32)
        for c in ((p[2] + p[0]) / 2, (p[17] + p[152]) / 2):
            cx, cy = int(c[0]), int(c[1])
            if rr <= cx < w - rr and rr <= cy < h - rr: di.append((bb[cy-rr:cy+rr, cx-rr:cx+rr] - full[cy-rr:cy+rr, cx-rr:cx+rr]).reshape(-1, 3).mean(0))
    d1 = np.clip(np.median(np.array(di), 0), -8, 8) if di else np.zeros(3, np.float32)
    L(f"{bid} (v3 nariz-queixo, q{k['a']}-{k['b']-1}, recorte {x},{y},{w},{h}): fx-base antes {d.round(1)} BGR; afim residuo {r:.2f} inliers {fra:.2f}; interno {d1.round(2)}")
    out = []; semrosto = 0
    for j in range(n):
        f = bases[j].copy(); g = aplicar(A, gs[j])
        if ms[j] is None:
            semrosto += 1; f[y:y + h, x:x + w] = np.clip(g + 0.5, 0, 255).astype(np.uint8)
        else:
            m = ms[j][..., None]; g = g + d1.astype(np.float32) * m
            f[y:y + h, x:x + w] = np.clip(g * m + f[y:y + h, x:x + w] * (1 - m), 0, 255).astype(np.uint8)
        out.append(f)
    if semrosto: L(f"  {bid}: {semrosto} quadros sem marcos (recorte inteiro, como no v3)")
    return out
# ---------------------------------------------------------------- 5) fechar do c1
EST = [33, 133, 362, 263, 168, 6, 197, 195, 5, 4, 1, 234, 454, 127, 356]
def mascara_c1(p, shape):   # = _loteA/fechar_c1.mascara
    lab = (p[13] + p[14]) / 2; queixo = p[152]; nariz = p[2]
    c = (lab + queixo) / 2 + np.array([0, 0.05 * np.linalg.norm(queixo - nariz)])
    ax = int(0.62 * np.linalg.norm(p[61] - p[291]) + 10); ay = int(0.62 * np.linalg.norm(queixo - nariz) + 6)
    m = np.zeros(shape[:2], np.float32)
    cv2.ellipse(m, (int(c[0]), int(c[1])), (ax, ay), 0, 0, 360, 1.0, -1)
    return cv2.GaussianBlur(m, (0, 0), max(3, ax / 6))
def fechar_c1(fr):
    z = np.load(C / "c1_marcos.npz"); Pm = z["P"]; r = int(z["r"]); n = 75; RAMPA = 3
    P_ = [None if np.isnan(p).any() else p for p in Pm]; orig = [f.copy() for f in fr]; pr = P_[r]; feitos = 0
    for a, b in z["runs"]:
        for q in range(a, b):
            w = min(1.0, (q - a + 1) / RAMPA, (b - q) / RAMPA) if b < n else min(1.0, (q - a + 1) / RAMPA)
            pk = P_[q]
            if pk is None: continue
            M, _ = cv2.estimateAffinePartial2D(pr[EST].astype(np.float32), pk[EST].astype(np.float32))
            if M is None: continue
            g = cv2.warpAffine(orig[r], M, (720, 1280), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
            ms = mascara_c1(pk, fr[q].shape)[..., None] * w
            fr[q] = np.clip(g * ms + fr[q] * (1 - ms), 0, 255).astype(np.uint8); feitos += 1
    L(f"c1 fechar: pausas {z['runs'].tolist()} ref q{r}; {feitos} quadros colados")
    return fr
# ---------------------------------------------------------------- montagem
def enc(path):
    return subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","24","-i","-",
        *ENC_VF,"-threads","6","-c:v","libx264","-crf","12","-preset","medium","-pix_fmt","yuv420p",*ENC_TAG,"-an",str(path)], stdin=subprocess.PIPE)
plano = {}   # quadro inicial -> (tipo, id, n)
for b in V1_USAR: k = B1[b]; plano[k["a"]] = ("v1", b, k["b"] - k["a"])
for b in V3_USAR: k = B3[b]; plano[k["a"]] = ("v3", b, k["b"] - k["a"])
cob = {}
for a, b, cr in COBRIR:
    for i in range(a, b): cob[i] = cr
t0 = time.time()
eb, el = enc(AD / "base_sem_legenda_lama.mp4"), enc(AD / "base_lipsync.mp4")
gen = base_gen(); prev = None; q = 0
def ler(n):
    fs = []
    for _ in range(n):
        f = next(gen); eb.stdin.write(f.tobytes()); fs.append(f)
    return fs
def saida(fs, q0):
    for j, f in enumerate(fs):
        i = q0 + j
        if i in cob:
            x, y, w, h = cob[i]; f = cv2.resize(f[y:y+h, x:x+w], (720, 1280), interpolation=cv2.INTER_LANCZOS4)
        el.stdin.write(np.ascontiguousarray(f).tobytes())
while q < N:
    if q not in plano:
        saida(ler(1), q); q += 1; continue
    tipo, bid, n = plano[q]; bases = ler(n)
    if tipo == "v1":
        out = bloco_v1(bid, bases)
        if bid == "c1": out = fechar_c1(out)
        prev = None
    else:
        out = bloco_v3(bid, bases)
        if prev is not None and prev[0] != bid and prev[1] == q - 1 and q in EMENDAS:
            out[0] = cv2.addWeighted(out[0], 2 / 3, prev[2], 1 / 3, 0); L(f"  emenda q{q}: crossfade (como no v3)")
        prev = (bid, q + n - 1, out[-1].copy())
    saida(out, q); q += n
    print(f"[{q}/{N}] {100*q//N}% {time.time()-t0:.0f} s, falta ~{(time.time()-t0)/q*(N-q):.0f} s", flush=True)
for e in (eb, el): e.stdin.close(); e.wait()
try: next(gen)
except StopIteration: pass
(C / "recolocar_cor.log").write_text("\n".join(log), encoding="utf-8"); print("ok", N, "quadros", f"{time.time()-t0:.0f} s")
