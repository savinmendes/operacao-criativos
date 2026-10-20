# -*- coding: utf-8 -*-
"""Correcao de cor AD 03 (REVISAO-LOTE-C, sem credito HeyGen). Uma geracao so, com a leitura/gravacao exata do
ad13/lipsync3/comum3.py, a partir do ORIGINAL e das saidas do HeyGen ja baixadas. Gera ad03/base_sem_legenda.mp4 e
ad03/base_lipsync.mp4 (= _tmp/montar_base.py + lipsync/recolocar.py + _tmp/loteA.py quadro):
- base: UNICOS_HD/03.mp4 + faixas LaMa ja calculadas (_tmp/lama, y 440-1180, mesmas mascaras/EMA/zeragem nos cortes),
  PNG convertidos da leitura cv2 para a leitura comum3 (afim fixa medida no proprio original); split 1198-1436 com a
  _tmp/broll_cruz.mp4 (feita por ffmpeg, ja no espaco da leitura comum3);
- cada trecho do HeyGen (ls_pNN.mp4, recorte 360x640 em (170,0), colado no recorte inteiro com borda de 24 px): antes de
  colar, afim BGR robusta saida -> base nova, medida no recorte fora da boca (rosto e fundo do proprio recorte);
- mesmas emendas (crossfade de 2 q sem corte de camera) e o quadro 282 com a boca do 283 (correcao do lote A).
Uso: python recolocar_cor_03.py"""
import json, os, numpy as np, cv2
from pathlib import Path
from util import T, UNICOS, quadros, enc, ajustar, aplicar, fit_cv2_para_601
AD = T / "ad03"; L = AD / "lipsync"; ORI = UNICOS / "03.mp4"
J = json.loads((L / "trechos.json").read_text(encoding="utf-8-sig")); X, Y, W, H = J["recorte"]; TR = J["trechos"]
R0, R1 = 440, 1180; SPLIT = (1198, 1436); NT = 2893
M = np.zeros((H, W), np.float32); M[24:-24, 24:-24] = 1; M[:24, 24:-24] = 1
M = cv2.GaussianBlur(M, (0, 0), 9)[..., None]; M[:4] = M[4]
# pixels do ajuste: recorte sem 28 px de borda (exceto o topo) e sem a boca/queixo (elipse do lote A: (358,372), 78x62)
AJM = np.zeros((H, W), bool); AJM[8:-28, 28:-28] = True
AJM[372 - 100 - Y:372 + 110 - Y, 358 - 115 - X:358 + 115 - X] = False
log = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); log.append(s)
AL, r, fr, d = fit_cv2_para_601(ORI); P("LaMa 03: afim leitura cv2 -> comum3, residuo", round(r, 2), "inliers", round(fr, 3), "desvio medio BGR", d.round(2))
def n_usados(nome, a, b):
    n = b - a + 1; return n
def base_gen():
    cz = quadros(AD / "_tmp" / "broll_cruz.mp4", h=640); ema = None; prev = None
    for i, f in enumerate(quadros(ORI)):
        g = cv2.resize(f, (90, 160)).astype(np.float32)
        if prev is not None and np.abs(g - prev).mean() > 8: ema = None
        prev = g
        mp = AD / "_tmp" / "mask" / f"{i:04d}.png"; lp = AD / "_tmp" / "lama" / f"{i:04d}.png"
        if mp.exists() and lp.exists():
            m = (cv2.imread(str(mp), 0)[R0:R1] > 0).astype(np.float32)
            l = aplicar(AL, cv2.imread(str(lp))).astype(np.float32)
            ema = l if ema is None else 0.65 * l + 0.35 * ema
            a = np.maximum(cv2.GaussianBlur(m, (11, 11), 0), m)[..., None]
            roi = f[R0:R1].astype(np.float32); f[R0:R1] = np.clip(ema * a + roi * (1 - a), 0, 255).astype(np.uint8)
        else: ema = None
        if SPLIT[0] <= i <= SPLIT[1]: f[640:1280] = next(cz)
        yield i, f
    for _ in cz: pass
# ---------- passada 1: amostras (so leitura) ----------
amos = {}
for nome, a, b in TR:
    for j in range(1, b - a, 4): amos[a + j] = (nome, j)
B = {}
for i, f in base_gen():
    if i in amos: B[amos[i]] = f[Y:Y + H, X:X + W].copy()
AJ = {}
for nome, a, b in TR:
    n = b - a + 1; Xs, Ys = [], []; nh = 0
    for j, g in enumerate(quadros(L / f"ls_{nome}.mp4")):
        nh += 1
        if (nome, j) in B and j < n:
            c = cv2.resize(g, (W, H), interpolation=cv2.INTER_AREA); Xs.append(c[AJM][::2]); Ys.append(B[(nome, j)][AJM][::2])
    assert nh >= n, (nome, nh, n)
    Xa, Ya = np.vstack(Xs), np.vstack(Ys); A, res, fi = ajustar(Xa, Ya); AJ[nome] = A
    P(f"{nome}: saida-base antes {(Xa.astype(float) - Ya).mean(0).round(1)} depois {(aplicar(A, Xa.reshape(-1, 1, 3)).reshape(-1, 3).astype(float) - Ya).mean(0).round(1)} | residuo {res:.2f} inliers {fi:.2f} | quadros {nh}->{n}")
del B
# ---------- passada 2: geracao ----------
eb, el = enc(AD / "base_sem_legenda.mp4", crf=12), enc(AD / "base_lipsync.mp4", crf=13)
porq = {}
for nome, a, b in TR:
    for q in range(a, b + 1): porq[q] = (nome, a, b)
MQ = np.zeros((1280, 720), np.float32); cv2.ellipse(MQ, (358, 372), (78, 62), 0, 0, 360, 1.0, -1); MQ = cv2.GaussianBlur(MQ, (0, 0), 9)[..., None]
segura = {}            # quadro 282 fica retido ate o 283 (lote A)
pend = None; ultima_base = None; ultimo_fim = None; gl = None
def emit(i, f):
    if i == 282: segura[282] = f; return
    if i == 283 and 282 in segura:
        f282 = np.clip(f * MQ + segura.pop(282) * (1 - MQ), 0, 255).astype(np.uint8); el.stdin.write(f282.tobytes()); P("  q282: boca do q283 colada (lote A)")
    el.stdin.write(f.tobytes())
for i, f in base_gen():
    eb.stdin.write(f.tobytes())
    if i not in porq:
        if pend is not None: emit(*pend); pend = None
        emit(i, f); continue
    nome, a, b = porq[i]; j = i - a
    if j == 0:
        gl = quadros(L / f"ls_{nome}.mp4"); A = AJ[nome]
    g = next(gl); c = aplicar(A, cv2.resize(g, (W, H), interpolation=cv2.INTER_AREA)).astype(np.float32)
    o = f.copy(); roi = f[Y:Y + H, X:X + W].astype(np.float32); o[Y:Y + H, X:X + W] = np.clip(c * M + roi * (1 - M), 0, 255).astype(np.uint8)
    if j == 0:
        if pend is not None:
            corte = np.abs(ultima_base.astype(np.float32) - f).mean() > 10
            if not corte and ultimo_fim == a - 1:
                Lf, Rf = pend[1].astype(np.float32), o.astype(np.float32)
                pend = (pend[0], np.clip(Lf * 2 / 3 + Rf / 3, 0, 255).astype(np.uint8)); o = np.clip(Lf / 3 + Rf * 2 / 3, 0, 255).astype(np.uint8)
            P(f"  emenda {nome} q{a}: {'corte' if corte else 'crossfade 2q'}" + ("" if ultimo_fim == a - 1 else " (nao contigua)"))
            emit(*pend); pend = None
    if i < b: emit(i, o)
    else:
        pend = (i, o); ultima_base = f; ultimo_fim = b; gl.close(); P(nome, "ok")
if pend is not None: emit(*pend)
assert i == NT - 1, i
eb.stdin.close(); el.stdin.close(); eb.wait(); el.wait()
P("ok quadros", NT)
np.save(Path(__file__).parent / "aj_03.npy", {"AL": AL, **AJ}, allow_pickle=True)
(Path(__file__).parent / "log_03.txt").write_text("\n".join(log), encoding="utf-8")
