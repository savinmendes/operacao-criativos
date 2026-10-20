# -*- coding: utf-8 -*-
"""Correcao de cor (REVISAO-LOTE-C): refaz base_sem_legenda + base_lipsync dos ADs 12/14 NUMA GERACAO SO, a partir do
ORIGINAL e das saidas do HeyGen ja baixadas, com a leitura/gravacao exata do ad13/lipsync3/comum3.py
(ffmpeg bt601 + accurate_rnd na leitura, conversao inversa exata na gravacao, etiqueta bt709/tv so no bitstream).
- Base: original (UNICOS_HD) + faixas LaMa ja calculadas (_tmp/lama/NNNN.png), mesma colagem/EMA do _tmp/montar_base.py.
  Os PNG do LaMa vieram da leitura cv2 (~1 nivel mais escura); cada PNG e corrigido pelo desvio medido nos pixels
  fora da mascara da propria faixa (PNG x quadro lido agora).
- Lipsync: lipsync/out/ls_<nome>.mp4 reamostrado p/ o n exato (sem congelar) e colado so na boca/queixo (mesma elipse
  do rosto.py). Antes de colar soma-se o desvio de cor (BGR) da saida contra a base nova, medido num anel de pele em
  volta da elipse (fora dela), mediana de 12 quadros do trecho; mais um ajuste interno (pele do filtro e do meio do queixo,
  saida x base) aplicado com o peso da propria elipse (0 na borda, 1 no centro), porque a saida do HeyGen escurece a pele
  dentro da area da boca (~5 niveis no gancho do 12).
- AD 14: quadros < 231 vem do 14.mp4 + ad14/_tmp/lama (gancho); do 231 em diante o corpo e o do 12 (original 12 + LaMa 12),
  com os mesmos trechos de lipsync do 12 (copias em ad14/lipsync).
Uso: python recolocar_cor.py 12|14   -> adNN/base_sem_legenda.mp4 e adNN/base_lipsync.mp4 (24 fps, sem audio)"""
import sys, json, subprocess, numpy as np, cv2
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "ad13" / "lipsync3"))
from comum3 import quadros, ENC_VF, ENC_TAG, reamostrar
NN = sys.argv[1]
T = Path(__file__).resolve().parents[2]; P = T.parents[1]
AD = T / f"ad{NN}"
cfg = json.loads((AD / "segmentos.json").read_text()); N = cfg["n"]; SEG = cfg["segmentos"]
R0, R1 = 720, 1130
CORTE14 = 231
def fontes():
    """(gerador de quadros do original, pasta lama, quadro inicial) por faixa de quadros"""
    if NN == "14":
        return [(0, CORTE14, P / "UNICOS_HD" / "14.mp4", AD / "_tmp" / "lama"),
                (CORTE14, N, P / "UNICOS_HD" / "12.mp4", T / "ad12" / "_tmp" / "lama")]
    return [(0, N, P / "UNICOS_HD" / "12.mp4", T / "ad12" / "_tmp" / "lama")]
def base_gen(log):
    ema = None; prev = None; offs = []
    for a, b, vid, ld in fontes():
        for i, f in enumerate(quadros(vid, a, b - a), start=a):
            g = cv2.resize(f, (90, 160)).astype(np.float32)
            if prev is not None and np.abs(g - prev).mean() > 8: ema = None
            prev = g
            m = cv2.imread(str(ld / f"mask_{i:04d}.png"), 0).astype(np.float32) / 255
            if m.sum() > 0:
                l = cv2.imread(str(ld / f"{i:04d}.png")).astype(np.float32); roi = f[R0:R1].astype(np.float32)
                fora = cv2.dilate((m > 0).astype(np.uint8), np.ones((15, 15), np.uint8)) == 0
                dv = np.median(roi[fora] - l[fora], axis=0) if fora.sum() > 1000 else np.zeros(3, np.float32)
                offs.append(dv); l = l + dv
                ema = l if ema is None else 0.7 * l + 0.3 * ema
                al = np.maximum(cv2.GaussianBlur(m, (11, 11), 0), m)[..., None]
                f[R0:R1] = np.clip(ema * al + roi * (1 - al), 0, 255).astype(np.uint8)
            else: ema = None
            yield i, f
    if offs: log.append(f"desvio LaMa PNG -> leitura nova (BGR, mediana): {np.median(np.array(offs), 0).round(2)}")
def mascara(p):   # = rosto.mascara
    lab = (p[13] + p[14]) / 2; queixo = p[152]; nariz = p[2]; fw = np.linalg.norm(p[234] - p[454])
    c = (lab + queixo) / 2 + np.array([0, 0.04 * fw])
    ax = int(0.42 * fw + 6); ay = int(0.62 * np.linalg.norm(queixo - nariz) + 6)
    m = np.zeros((1280, 720), np.float32)
    cv2.ellipse(m, (int(c[0]), int(c[1])), (ax, ay), 0, 0, 360, 1.0, -1)
    return cv2.GaussianBlur(m, (0, 0), max(4, fw * 0.05))[..., None], fw
def esticar(g, b):
    x, y, w, h = b
    M = np.array([[w / g.shape[1], 0, x], [0, h / g.shape[0], y]], np.float32)
    return cv2.warpAffine(g, M, (720, 1280), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REPLICATE)
def colar(base, g, b, p, dv):   # = rosto.colar + desvio de cor (dv = (anel, interno))
    if p is None: return base
    m, _ = mascara(p); full = esticar(g, b).astype(np.float32) + dv[0] + dv[1] * m
    return np.clip(full * m + base * (1 - m), 0, 255).astype(np.uint8)
def desvio(bases, g, B, P):
    ds = []
    for k in np.linspace(0, len(bases) - 1, 12).astype(int):
        if np.isnan(P[k]).any(): continue
        m, fw = mascara(P[k]); dentro = m[..., 0] > 0.01
        anel = cv2.dilate(dentro.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(0.5 * fw) | 1,) * 2)).astype(bool) & ~dentro
        x, y, w, h = B[k]; cx = np.zeros_like(anel); cx[int(y) + 2:int(y + h) - 2, int(x) + 2:int(x + w) - 2] = True; anel &= cx
        full = esticar(g[k], B[k]).astype(np.float32)
        ds.append((bases[k].astype(np.float32) - full)[anel].mean(0))
    d0 = np.median(np.array(ds), 0) if ds else np.zeros(3, np.float32); di = []
    for k in np.linspace(0, len(bases) - 1, 12).astype(int):   # pele DENTRO da elipse (filtro e meio do queixo)
        p = P[k]
        if np.isnan(p).any(): continue
        full = esticar(g[k], B[k]).astype(np.float32) + d0; bb = bases[k].astype(np.float32); r = max(3, int(0.05 * np.linalg.norm(p[234] - p[454])))
        for c in ((p[2] + p[0]) / 2, (p[17] + p[152]) / 2):
            x, y = int(c[0]), int(c[1]); di.append((bb[y-r:y+r, x-r:x+r] - full[y-r:y+r, x-r:x+r]).reshape(-1, 3).mean(0))
    d1 = np.clip(np.median(np.array(di), 0), -8, 8) if di else np.zeros(3, np.float32)
    return d0, d1
def enc(path):
    return subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","24","-i","-",
        *ENC_VF,"-threads","4","-c:v","libx264","-crf","12","-preset","medium","-pix_fmt","yuv420p",*ENC_TAG,"-an",str(path)], stdin=subprocess.PIPE)
log = []
eb, el = enc(AD / "base_sem_legenda.mp4"), enc(AD / "base_lipsync.mp4")
porq = {}
for s in SEG:
    for q in range(s["quadro_ini"], s["quadro_fim"] + 1): porq[q] = s
gen = base_gen(log); pend = None   # pend = (lista de quadros de saida do trecho anterior, ultima base dele, fim)
def flush():
    global pend
    if pend is not None:
        for f in pend[0]: el.stdin.write(f.tobytes())
        pend = None
i = 0
while i < N:
    if i not in porq:
        _, f = next(gen); eb.stdin.write(f.tobytes()); flush(); el.stdin.write(f.tobytes()); i += 1; continue
    s = porq[i]; nome, a, b = s["nome"], s["quadro_ini"], s["quadro_fim"]; n = b - a + 1
    bases = []
    for _ in range(n):
        _, f = next(gen); eb.stdin.write(f.tobytes()); bases.append(f)
    g = list(quadros(AD / "lipsync" / "out" / f"ls_{nome}.mp4")); m0 = len(g); g = reamostrar(g, n)
    geo = np.load(AD / "lipsync" / "in" / f"geo_{nome}.npz"); B, Pm = geo["B"], geo["P"]
    dv = desvio(bases, g, B, Pm)
    out = [colar(bases[j], g[j], B[j], None if np.isnan(Pm[j]).any() else Pm[j], dv) for j in range(n)]
    log.append(f"{nome}: {m0}->{n} quadros; desvio de cor da saida HeyGen (BGR) anel {dv[0].round(2)} + interno {dv[1].round(2)}")
    if pend is not None and pend[2] == a - 1:
        corte = np.abs(pend[1].astype(np.float32) - bases[0]).mean() > 10
        if not corte:
            Lf, Rf = pend[0][-1].astype(np.float32), out[0].astype(np.float32)
            pend[0][-1] = np.clip(Lf * 2 / 3 + Rf / 3, 0, 255).astype(np.uint8); out[0] = np.clip(Lf / 3 + Rf * 2 / 3, 0, 255).astype(np.uint8)
        log.append(f"  emenda q{a}: {'corte' if corte else 'crossfade 2q'}")
    flush(); pend = (out, bases[-1], b); i = b + 1
    print(log[-1], flush=True)
flush()
for e in (eb, el): e.stdin.close(); e.wait()
print("\n".join(log)); print("ok quadros", N)
