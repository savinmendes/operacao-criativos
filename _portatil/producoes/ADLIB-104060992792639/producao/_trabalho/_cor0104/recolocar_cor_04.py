# -*- coding: utf-8 -*-
"""Correcao de cor AD 04 (REVISAO-LOTE-C, sem credito HeyGen). Uma geracao so, com a leitura/gravacao exata do
ad13/lipsync3/comum3.py, a partir do ORIGINAL e das saidas do HeyGen ja baixadas. Gera ad04/base_sem_legenda.mp4 e
ad04/base_lipsync.mp4 (= _tmp/montar_base.py + lipsync/recolocar.py com o plano.json):
- base: UNICOS_HD/04.mp4 + faixas LaMa ja calculadas (_tmp/lama + _tmp/mask, y 840-1210, inclusive o clarao refeito
  pelo lama_flash.py), PNG convertidos da leitura cv2 para a leitura comum3 (afim fixa medida no proprio original);
  mesmas trocas das cenas do depoimento pelo overlay dos anjos (1586-1719 e 1906-2003);
- trechos do HeyGen (out/ls_<n>.mp4): mesma colagem do recolocar.py (MediaPipe na saida, elipse nariz-queixo com EMA,
  quadros iniciais sem rosto com a elipse final do trecho); antes de colar, afim BGR robusta saida -> base nova medida num
  ANEL DE PELE em volta da elipse (1,3x-2,4x), fora da boca; w2 continua coberto (zoom no overlay); w11/w12 com o mesmo
  crossfade linear na sobreposicao.
Uso: python recolocar_cor_04.py"""
import sys, os, json, numpy as np, cv2
from pathlib import Path
os.environ.setdefault("GLOG_minloglevel", "2")
from util import T, UNICOS, quadros, enc, ajustar, aplicar, fit_cv2_para_601
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl   # noqa: E402
import mediapipe as mp   # noqa: E402
from mediapipe.tasks import python as mpt   # noqa: E402
from mediapipe.tasks.python import vision   # noqa: E402
AD = T / "ad04"; AQ = AD / "lipsync"; ORI = UNICOS / "04.mp4"
cfg = json.loads((AQ / "segs.json").read_text()); NT = cfg["ntot"]; SEGS = sorted(cfg["segs"], key=lambda s: s["a"])
plano = json.loads((AQ / "plano.json").read_text())
R0, R1 = 840, 1210
CORTES = set(range(284, 308)) | {290, 293, 523, 602, 669, 810, 1043, 1292, 1586, 1720, 1906, 2004}
TROCA = [(1586, 1720, 1046), (1906, 2004, 1186)]
alpha = np.zeros((1280, 1, 1), np.float32); alpha[580:] = 1; alpha[520:580, 0, 0] = np.linspace(0, 1, 60); alpha = alpha[520:]
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=1,
    min_face_detection_confidence=0.3))
YY, XX = np.mgrid[0:1280, 0:720].astype(np.float32)
log = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); log.append(s)
def elipse(cx, cy, ax, ay, sig):
    m = (((XX - cx) / ax) ** 2 + ((YY - cy) / ay) ** 2 <= 1).astype(np.float32)
    return cv2.GaussianBlur(m, (0, 0), sig)[..., None]
def por(g, x, y, w, h):
    W, H = max(1, int(round(w))), max(1, int(round(h)))
    g2 = cv2.resize(g, (W, H), interpolation=cv2.INTER_AREA)
    return cv2.warpAffine(g2, np.float32([[w / W, 0, x], [0, h / H, y]]), (720, 1280), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
def cobre(s): return s["n"] in plano.get("cobrir", {})
def arq(s): return AQ / plano.get(s["n"], f"out/ls_{s['n']}.mp4")
AL, r, fr, d = fit_cv2_para_601(ORI); P("LaMa 04: afim leitura cv2 -> comum3, residuo", round(r, 2), "inliers", round(fr, 3), "desvio medio BGR", d.round(2))
# ---------- passada 1a: MediaPipe nas saidas (mesma conta do recolocar.py) ----------
GEO = {}
for s in SEGS:
    if cobre(s): continue
    a, b = s["a"], s["b"]; n = b - a; x, y, w, h = s["crop"]; sx, sy = w / 720, h / 1280
    par = None; pars = []; novos = []; nh = 0
    for k, g in enumerate(quadros(arq(s))):
        nh += 1
        if k >= n: continue
        rr = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(cv2.cvtColor(g, cv2.COLOR_BGR2RGB))))
        nv = None
        if rr.face_landmarks:
            p = np.array([(q.x * 720 * sx + x, q.y * 1280 * sy + y) for q in rr.face_landmarks[0]])
            fw = p[454, 0] - p[234, 0]; nose = p[1]; chin = p[152]; mo = (p[13] + p[14]) / 2
            nv = np.array([mo[0], (nose[1] + chin[1]) / 2 + 0.05 * (chin[1] - nose[1]), 0.40 * abs(fw), 0.70 * (chin[1] - nose[1])])
            par = nv if par is None else 0.6 * nv + 0.4 * par
        pars.append(None if par is None else par.copy()); novos.append(nv)
    assert nh >= n, (s["n"], nh, n)
    GEO[s["n"]] = dict(pars=pars, final=par, novos=novos)
    P(f"{s['n']}: {nh} quadros HeyGen -> {n}; rosto em {sum(v is not None for v in novos)}/{n}")
# ---------- base (gerador) ----------
def base_gen():
    cache = {}; precisa = set(); ema = None
    for a, b, s in TROCA: precisa |= set(range(s, s + (b - a)))
    for i, f in enumerate(quadros(ORI, 0, NT)):
        if i in CORTES: ema = None
        m = np.load(AD / "_tmp" / "mask" / f"{i:04d}.npy").astype(np.float32)
        if m.sum() > 0:
            l = aplicar(AL, cv2.imread(str(AD / "_tmp" / "lama" / f"{i:04d}.png"))).astype(np.float32)
            ema = l if ema is None else 0.65 * l + 0.35 * ema
            al = np.maximum(cv2.GaussianBlur(m, (11, 11), 0), m)[..., None]
            roi = f[R0:R1].astype(np.float32); f[R0:R1] = np.clip(ema * al + roi * (1 - al), 0, 255).astype(np.uint8)
        else: ema = None
        if i in precisa: cache[i] = f[520:].copy()
        for a, b, s in TROCA:
            if a <= i < b:
                g = cache.pop(s + i - a).astype(np.float32)
                f[520:] = np.clip(g * alpha + f[520:].astype(np.float32) * (1 - alpha), 0, 255).astype(np.uint8)
        yield i, f
# ---------- passada 1b: amostras da base no anel de pele ----------
def anel(s, k):
    x, y, w, h = s["crop"]; G = GEO[s["n"]]; p = G["novos"][k]
    if p is None: return None
    cx, cy, ax, ay = p[0], p[1], max(p[2], 20), max(p[3], 20)
    e = ((XX - cx) / ax) ** 2 + ((YY - cy) / ay) ** 2
    m = (e >= 1.3 ** 2) & (e <= 2.4 ** 2)
    box = np.zeros((1280, 720), bool); box[int(y) + 10:int(y + h) - 10, int(x) + 10:int(x + w) - 10] = True
    return m & box
amos = {}
for s in SEGS:
    if cobre(s): continue
    for k in range(1, s["b"] - s["a"] - 1, 4):
        if GEO[s["n"]]["novos"][k] is not None: amos.setdefault(s["a"] + k, []).append((s["n"], k))
Bs = {}
for i, f in base_gen():
    for nm, k in amos.get(i, []):
        s = next(z for z in SEGS if z["n"] == nm); m = anel(s, k); Bs[(nm, k)] = (m, f[m].copy())
AJ = {}
for s in SEGS:
    if cobre(s): continue
    want = {k for (nm, k) in Bs if nm == s["n"]}; Xs, Ys = [], []; x, y, w, h = s["crop"]
    for k, g in enumerate(quadros(arq(s))):
        if k in want:
            m, yv = Bs[(s["n"], k)]; Xs.append(por(g, x, y, w, h)[m]); Ys.append(yv)
    if not Xs: AJ[s["n"]] = np.r_[np.eye(3), np.zeros((1, 3))]; P(f"{s['n']}: sem amostra de rosto, sem ajuste"); continue
    Xa, Ya = np.vstack(Xs)[::2], np.vstack(Ys)[::2]; A, res, fi = ajustar(Xa, Ya); AJ[s["n"]] = A
    P(f"{s['n']}: saida-base antes {(Xa.astype(float) - Ya).mean(0).round(1)} depois {(aplicar(A, Xa.reshape(-1, 1, 3)).reshape(-1, 3).astype(float) - Ya).mean(0).round(1)} | residuo {res:.2f} inliers {fi:.2f} | {len(Xs)} quadros")
del Bs
# ---------- passada 2: geracao ----------
eb, el = enc(AD / "base_sem_legenda.mp4", crf=12), enc(AD / "base_lipsync.mp4", crf=14)
ativos = {}   # nome -> gerador de quadros da saida
def saida(s, k, b, g):
    """quadro k do trecho s colado na base b (= recolocar.colar_seg)"""
    x, y, w, h = s["crop"]; G = GEO[s["n"]]; par = G["pars"][k]
    if par is None:
        if G["final"] is None: return b
        par = G["final"]; sig = 6
    else: sig = max(4, 0.07 * abs(par[2]) * 2.5)
    full = aplicar(AJ[s["n"]], por(g, x, y, w, h))
    M = elipse(par[0], par[1], max(par[2], 20), max(par[3], 20), sig)
    return np.clip(full * M + b * (1 - M), 0, 255).astype(np.uint8)
for i, f in base_gen():
    eb.stdin.write(f.tobytes())
    cob = [s for s in SEGS if s["a"] <= i < s["b"]]
    outs = []
    for s in cob:
        k = i - s["a"]
        if cobre(s):
            x, y, w, h = plano["cobrir"][s["n"]]; outs.append(cv2.resize(f[y:y + h, x:x + w], (720, 1280), interpolation=cv2.INTER_LANCZOS4)); continue
        if k == 0: ativos[s["n"]] = quadros(arq(s))
        g = next(ativos[s["n"]]); outs.append(saida(s, k, f, g))
        if k == s["b"] - s["a"] - 1: ativos.pop(s["n"]).close()
    if not outs: o = f
    elif len(outs) == 1: o = outs[0]
    else:   # sobreposicao (w11/w12): crossfade linear, igual ao recolocar.py
        s0, s1 = cob[0], cob[1]; ov = list(range(max(s0["a"], s1["a"]), min(s0["b"], s1["b"]))); t = (ov.index(i) + 1) / (len(ov) + 1)
        o = np.clip(outs[0].astype(np.float32) * (1 - t) + outs[1].astype(np.float32) * t, 0, 255).astype(np.uint8)
    el.stdin.write(o.tobytes())
    if i % 500 == 0: P(f"[{i}/{NT}]")
assert i == NT - 1, i
eb.stdin.close(); el.stdin.close(); eb.wait(); el.wait()
P("ok quadros", NT)
np.save(Path(__file__).parent / "aj_04.npy", {"AL": AL, **AJ}, allow_pickle=True)
(Path(__file__).parent / "log_04.txt").write_text("\n".join(log), encoding="utf-8")
