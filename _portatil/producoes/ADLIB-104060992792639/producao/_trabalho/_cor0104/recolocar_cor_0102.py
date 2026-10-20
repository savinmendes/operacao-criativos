# -*- coding: utf-8 -*-
"""Correcao de cor ADs 01 e 02 (REVISAO-LOTE-C, sem credito HeyGen). Uma geracao so, a partir do ORIGINAL e das saidas do
HeyGen ja baixadas, com a leitura/gravacao exata do ad13/lipsync3/comum3.py. Gera, de uma vez:
  ad01/base_sem_legenda.mp4, ad01/base_lipsync.mp4, ad02/base_sem_legenda.mp4, ad02/base_lipsync.mp4
AD 01 (= ad01/_tmp/montar_base.py + ad01/lipsync2/recolocar2.py):
- base: UNICOS_HD/01.mp4 + faixas LaMa ja calculadas (_tmp/lama, y 820-990, mesma mascara/EMA), PNG convertidos da leitura
  cv2 para a leitura comum3 (afim fixa medida no proprio original);
- trechos refeitos (plano.json, v1_*.mp4, recorte 288x512 em (318,196)): mesma elipse do colar.py; antes de colar, afim BGR
  robusta saida -> base nova medida num ANEL DE PELE em volta da elipse (1,3x-2,4x), fora da boca;
- trechos antigos (lipsync/ls_s03/s04/s10/s13, quadro inteiro, parte de cima): afim robusta saida -> base nova medida em y<760
  fora da boca; s03/s10/s13 com o fechar.py (mesma logica, em memoria);
- emendas sem corte de camera: crossfade de 2 quadros (mesma regra).
AD 02 (= ad02/_tmp/montar_base.py + lipsync/colar_h1.py + montar_corpo.py): gancho 0-285 = UNICOS_HD/02.mp4 + LaMa do gancho
(_tmp/lama, y 820-970) + ls_h1_speed.mp4 colado no recorte inteiro (360x640 em (290,200), borda 24 px) com afim robusta
saida -> base no recorte fora da boca; do quadro 286 em diante = os quadros do AD 01 a partir do 242 (mesmos bytes).
Uso: python recolocar_cor_0102.py"""
import sys, json, numpy as np, cv2
from pathlib import Path
from util import T, UNICOS, quadros, enc, ajustar, aplicar, fit_cv2_para_601, elipse_mask
A1, A2 = T / "ad01", T / "ad02"; L2 = A1 / "lipsync2"
sys.path.insert(0, str(L2))
import fechar as Fe, medir as Me   # noqa: E402  (mesmas funcoes do fechar.py aprovado)
ORI1, ORI2 = UNICOS / "01.mp4", UNICOS / "02.mp4"
N1 = 3937; NL = 3473; OFF = 242; NG = 286
SEG = json.loads((A1 / "segmentos.json").read_text())["segmentos"]
PL = json.loads((L2 / "plano.json").read_text()); FECHAR = set(PL.get("_fechar", []))
CORTES = {477, 584, 629, 979, 1470}
X0, Y0, W, H = 318, 196, 288, 512                       # colar.py
MC = (425, 468); MAX = (90, 88)
Mel = np.zeros((1280, 720), np.float32); cv2.ellipse(Mel, MC, MAX, 0, 0, 360, 1.0, -1); Mel = cv2.GaussianBlur(Mel, (0, 0), 10)[..., None]
WV = np.zeros((1280, 1, 1), np.float32); WV[800:] = 1; WV[760:800, 0, 0] = np.linspace(0, 1, 40)
HX, HY, HW, HH = 290, 200, 360, 640                     # colar_h1.py
MH = np.zeros((HH, HW), np.float32); MH[24:-24, 24:-24] = 1; MH = cv2.GaussianBlur(MH, (0, 0), 10)[..., None]
log = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); log.append(s)

# ---------------- mascaras de ajuste ----------------
# anel de pele (coordenadas do recorte 288x512): entre 1,3x e 2,4x a elipse colada, sem 12 px de borda e sem o canto inpaintado
anel = elipse_mask((1280, 720), MC, (MAX[0] * 2.4, MAX[1] * 2.4)) & ~elipse_mask((1280, 720), MC, (MAX[0] * 1.3, MAX[1] * 1.3))
anel = anel[Y0:Y0 + H, X0:X0 + W].copy(); anel[:12] = anel[-12:] = False; anel[:, :12] = anel[:, -12:] = False
anel[:345 - Y0 + 6, :352 - X0 + 6] = False
# trechos antigos (quadro inteiro): y < 760, fora da boca (2x a elipse)
topo = np.zeros((1280, 720), bool); topo[8:752, 8:712] = True; topo &= ~elipse_mask((1280, 720), MC, (MAX[0] * 2, MAX[1] * 2))
topo_s = topo[::3, ::3]
# gancho do 02: recorte inteiro sem 28 px de borda e sem a boca/queixo (rosto 258,357,234,278)
gm = np.zeros((HH, HW), bool); gm[28:-28, 28:-28] = True; gm[520 - HY:680 - HY, 300 - HX:460 - HX] = False

def tipo(s): return "novo" if s["nome"] in PL and not s["nome"].startswith("_") else "antigo"
def arq(s): return L2 / PL[s["nome"]][0][0] if tipo(s) == "novo" else A1 / "lipsync" / f"ls_{s['nome']}.mp4"

# ---------------- 0) conversao dos PNG do LaMa (cv2 -> comum3) ----------------
AL1, r, fr, d = fit_cv2_para_601(ORI1); P("LaMa 01: afim leitura cv2 -> comum3, residuo", round(r, 2), "inliers", round(fr, 3), "desvio medio BGR", d.round(2))
AL2, r, fr, d = fit_cv2_para_601(ORI2); P("LaMa 02: afim leitura cv2 -> comum3, residuo", round(r, 2), "inliers", round(fr, 3), "desvio medio BGR", d.round(2))

# ---------------- 1) passada de leitura: amostras para o ajuste de cor de cada trecho ----------------
amos = {}
for s in SEG:
    n = s["quadro_fim"] - s["quadro_ini"] + 1
    for j in range(1, n - 1, 5): amos[s["quadro_ini"] + j] = (s["nome"], j)
B = {}
for i, f in enumerate(quadros(ORI1, 0, NL)):
    if i in amos:
        nm, j = amos[i]; s = next(x for x in SEG if x["nome"] == nm)
        B[(nm, j)] = f[Y0:Y0 + H, X0:X0 + W].copy() if tipo(s) == "novo" else f[::3, ::3].copy()
AJ = {}
for s in SEG:
    nm = s["nome"]; n = s["quadro_fim"] - s["quadro_ini"] + 1; want = {j for (k, j) in B if k == nm}; Xs, Ys = [], []
    nh = 0
    for j, g in enumerate(quadros(arq(s))):
        nh += 1
        if j not in want: continue
        if tipo(s) == "novo":
            c = cv2.resize(g, (W, H), interpolation=cv2.INTER_AREA); Xs.append(c[anel]); Ys.append(B[(nm, j)][anel])
        else:
            Xs.append(g[::3, ::3][topo_s]); Ys.append(B[(nm, j)][topo_s])
    assert nh == n, (nm, nh, n)
    X, Y = np.vstack(Xs), np.vstack(Ys); A, res, fi = ajustar(X, Y); AJ[nm] = A
    P(f"{nm} ({tipo(s)}): saida-base antes {(X.astype(float) - Y).mean(0).round(1)} depois {(aplicar(A, X.reshape(-1, 1, 3)).reshape(-1, 3).astype(float) - Y).mean(0).round(1)} | residuo {res:.2f} inliers {fi:.2f}")
del B
# gancho do 02
Bg = {}
for i, f in enumerate(quadros(ORI2, 0, NG)):
    if i % 5 == 2: Bg[i] = f[HY:HY + HH, HX:HX + HW].copy()
Xs, Ys = [], []
for j, g in enumerate(quadros(A2 / "lipsync" / "ls_h1_speed.mp4")):
    if j in Bg:
        c = cv2.resize(g, (HW, HH), interpolation=cv2.INTER_AREA); Xs.append(c[gm][::2]); Ys.append(Bg[j][gm][::2])
X, Y = np.vstack(Xs), np.vstack(Ys); AH, res, fi = ajustar(X, Y)
P(f"h1 (02): saida-base antes {(X.astype(float) - Y).mean(0).round(1)} depois {(aplicar(AH, X.reshape(-1, 1, 3)).reshape(-1, 3).astype(float) - Y).mean(0).round(1)} | residuo {res:.2f} inliers {fi:.2f}")
del Bg, X, Y, Xs, Ys

# ---------------- 2) geracao ----------------
eb1, el1 = enc(A1 / "base_sem_legenda.mp4", crf=12), enc(A1 / "base_lipsync.mp4", crf=12)
eb2, el2 = enc(A2 / "base_sem_legenda.mp4", crf=12), enc(A2 / "base_lipsync.mp4", crf=12)
# 2a) gancho do 02 (quadros 0-285)
MK = np.load(A2 / "_tmp" / "lama_mask.npy"); ema = None
for i, (f, g) in enumerate(zip(quadros(ORI2, 0, NG), quadros(A2 / "lipsync" / "ls_h1_speed.mp4"))):
    m = MK[i].astype(np.float32)
    if m.sum() > 0:
        l = aplicar(AL2, cv2.imread(str(A2 / "_tmp" / "lama" / f"{i:04d}.png"))).astype(np.float32)
        ema = l if ema is None else 0.65 * l + 0.35 * ema
        a = np.maximum(cv2.GaussianBlur(m, (11, 11), 0), m)[..., None]
        roi = f[820:970].astype(np.float32); f[820:970] = np.clip(ema * a + roi * (1 - a), 0, 255).astype(np.uint8)
    else: ema = None
    eb2.stdin.write(f.tobytes())
    c = aplicar(AH, cv2.resize(g, (HW, HH), interpolation=cv2.INTER_AREA)).astype(np.float32); roi = f[HY:HY + HH, HX:HX + HW].astype(np.float32)
    f[HY:HY + HH, HX:HX + HW] = np.clip(c * MH + roi * (1 - MH), 0, 255).astype(np.uint8)
    el2.stdin.write(f.tobytes())
assert i == NG - 1
P("gancho 02 ok", NG, "quadros")
# 2b) AD 01 (e o 02 a partir do quadro 242 do 01)
BM = np.load(A1 / "_tmp" / "boxmasks.npy", mmap_mode="r")
def base01():
    ema = None
    for i, f in enumerate(quadros(ORI1)):
        if i < NL:
            if i in CORTES: ema = None
            l = aplicar(AL1, cv2.imread(str(A1 / "_tmp" / "lama" / f"{i:04d}.png"))).astype(np.float32)
            ema = l if ema is None else 0.6 * l + 0.4 * ema
            m = cv2.dilate(np.array(BM[i]), np.ones((5, 5), np.uint8)).astype(np.float32)
            a = np.maximum(cv2.GaussianBlur(m, (11, 11), 0), m)[..., None]
            roi = f[820:990].astype(np.float32); f[820:990] = np.clip(ema * a + roi * (1 - a), 0, 255).astype(np.uint8)
        eb1.stdin.write(f.tobytes())
        if i >= OFF: eb2.stdin.write(f.tobytes())
        yield i, f
def emit(i, f):
    el1.stdin.write(f.tobytes())
    if i >= OFF: el2.stdin.write(f.tobytes())
def colar_novo(b, g, A):
    c = aplicar(A, cv2.resize(g, (W, H), interpolation=cv2.INTER_AREA)); full = b.copy(); full[Y0:Y0 + H, X0:X0 + W] = c
    return np.clip(full * Mel + b * (1 - Mel), 0, 255).astype(np.uint8)
def colar_antigo(b, g, A):
    return np.clip(aplicar(A, g) * (1 - WV) + b * WV, 0, 255).astype(np.uint8)
def fechar_mem(frames, q0):
    """= lipsync2/fechar.fechar, sem copiar o trecho inteiro (guarda so os quadros de referencia, tirados antes de mexer)."""
    n = len(frames); runs = Fe.pausas_es(q0, n); lg = []
    if not runs: return frames, lg
    Pm = [None] * n; ab = np.full(n, np.nan); need = set()
    for a, b in runs: need.update(range(max(0, a - 45), min(n, b + 45)))
    for k in sorted(need):
        Pm[k] = Fe.marcos(frames[k])
        if Pm[k] is not None: ab[k] = Me.cl._abertura(Pm[k])
    refs = {}
    for a, b in runs:
        viz = [k for k in range(max(0, a - 45), min(n, b + 45)) if np.isfinite(ab[k])]
        if viz: r = min(viz, key=lambda k: ab[k]); refs[(a, b)] = (r, frames[r].copy())
    for a, b in runs:
        if (a, b) not in refs: continue
        r, ref = refs[(a, b)]; pr = Pm[r]
        for k in range(a, b):
            w = min(1.0, (k - a + 1) / Fe.RAMPA, (b - k) / Fe.RAMPA); pk = Pm[k] if Pm[k] is not None else Fe.marcos(frames[k])
            if pk is None: continue
            M, _ = cv2.estimateAffinePartial2D(pr[Fe.ESTAVEIS].astype(np.float32), pk[Fe.ESTAVEIS].astype(np.float32))
            if M is None: continue
            gg = cv2.warpAffine(ref, M, (720, 1280), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
            ms = Fe.mascara(pk)[..., None] * w
            frames[k] = np.clip(gg * ms + frames[k] * (1 - ms), 0, 255).astype(np.uint8)
        lg.append(f"pausa {(q0+a)/30:.2f}-{(q0+b)/30:.2f}s ref q{q0+r} ab={ab[r]:.3f}")
    return frames, lg
porq = {}
for s in SEG:
    for q in range(s["quadro_ini"], s["quadro_fim"] + 1): porq[q] = s
gen = base01(); pend = None; ultima_base = None; ultimo_fim = None
i = 0
while True:
    try: i, f = next(gen)
    except StopIteration: break
    if i not in porq:
        if pend is not None: emit(*pend); pend = None
        emit(i, f); continue
    s = porq[i]; nm, a, b = s["nome"], s["quadro_ini"], s["quadro_fim"]; n = b - a + 1; A = AJ[nm]
    gl = quadros(arq(s)); colar = colar_novo if tipo(s) == "novo" else colar_antigo
    corte = None
    if nm in FECHAR:
        fr = [colar(f, next(gl), A)]; b0 = f
        for _ in range(n - 1):
            i, f = next(gen); fr.append(colar(f, next(gl), A))
        fr, lg = fechar_mem(fr, a); P(f"  {nm} +fechar: " + "; ".join(lg))
        primeiro_b = b0; lista = fr
    else:
        lista = None; primeiro_b = f
    # emenda com o trecho anterior (base: ultimo de A x primeiro de B)
    if pend is not None:
        corte = np.abs(ultima_base.astype(np.float32) - primeiro_b).mean() > 10
        primeiro = lista[0] if lista is not None else colar(f, next(gl), A)
        if not corte and ultimo_fim == a - 1:
            Lf, Rf = pend[1].astype(np.float32), primeiro.astype(np.float32)
            pend = (pend[0], np.clip(Lf * 2 / 3 + Rf / 3, 0, 255).astype(np.uint8)); primeiro = np.clip(Lf / 3 + Rf * 2 / 3, 0, 255).astype(np.uint8)
        P(f"  emenda {nm} q{a}: {'corte' if corte else 'crossfade 2q'}")
        emit(*pend); pend = None
    else:
        primeiro = lista[0] if lista is not None else colar(f, next(gl), A)
    if lista is not None:
        lista[0] = primeiro
        for k, fk in enumerate(lista[:-1]): emit(a + k, fk)
        pend = (b, lista[-1]); ultima_base = f; del lista, fr
    else:
        if n == 1: pend = (a, primeiro)
        else:
            emit(a, primeiro)
            for k in range(1, n):
                i, f = next(gen); o = colar(f, next(gl), A)
                if k < n - 1: emit(a + k, o)
                else: pend = (b, o)
        ultima_base = f
    ultimo_fim = b
    for _ in gl: pass
    P(nm, tipo(s), n, "quadros")
if pend is not None: emit(*pend)
assert i == N1 - 1, i
for e in (eb1, el1, eb2, el2): e.stdin.close(); e.wait()
P("ok AD 01:", N1, "quadros; AD 02:", NG + N1 - OFF, "quadros")
np.save(Path(__file__).parent / "aj_0102.npy", {"AL1": AL1, "AL2": AL2, "AH": AH, **AJ}, allow_pickle=True)
(Path(__file__).parent / "log_0102.txt").write_text("\n".join(log), encoding="utf-8")
