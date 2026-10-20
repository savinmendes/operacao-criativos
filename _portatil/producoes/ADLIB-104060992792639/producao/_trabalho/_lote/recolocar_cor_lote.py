# -*- coding: utf-8 -*-
"""Correcao de cor do lote C (REVISAO-LOTE-C), ADs 15 e 16, SEM credito HeyGen: refaz base_sem_legenda e base_lipsync
NUMA GERACAO SO, a partir do ORIGINAL (UNICOS_HD) e das saidas do HeyGen ja baixadas, com a leitura/gravacao exata do
ad13/lipsync3/comum3.py. Pecas de cor em cor_trecho.py.
- Base: original + so as areas do LaMa (legenda/seta) da base antiga, cor levada ao original por quadro (= ad08).
- AD 16: abertura reenquadrada (q0-291: recorte 360x640 em (200,180) ampliado 2x, Lanczos) e fusao com clarao quente
  292-297 (A = 291 recortado, B = 298), iguais ao _tmp/crop_abertura.py -> base_sem_legenda_crop.mp4.
- Lote A (= _lote/recolocar.py): descarte do 1o quadro que nao bate com a entrada, reamostragem p/ o n exato, elipse
  'cola' (fixa ou com quadros-chave), recorte 'crop', crossfade 0,6 na boca nas emendas continuas.
- AD 16 lote B (= _lote/rastreado.py aplicar, lote_b.json): i1s, j1b, k1b com as trilhas (recorte por quadro, elipse do
  rosto), no lugar de i1r, j1, k1 (mesmos quadros); crossfade 2 q na boca so se a emenda nao for corte.
- Cada trecho do HeyGen: afim no recorte fora da elipse + anel de pele + ajuste interno (cor_trecho.medir/corrigir).
Uso (em _trabalho): python _lote/recolocar_cor_lote.py 15|16"""
import sys, json, numpy as np, cv2
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cor_trecho import quadros, reamostrar, enc, base_lama, medir, corrigir, txt
NN = sys.argv[1]; T = Path(__file__).resolve().parents[1]; AD = T / f"ad{NN}"; P = T.parents[1]
ORIG = P / "UNICOS_HD" / f"{NN}.mp4"; VELHA = AD / "_antes_cor" / "base_sem_legenda.mp4"
FPS = 30; log = []
SEGS = json.loads((AD / "lipsync" / ("segs_i1r.json" if NN == "16" else "segs.json")).read_text(encoding="utf-8"))["segs"]
N = int(cv2.VideoCapture(str(VELHA)).get(7))
plano = []
LB = {}
if NN == "16":
    LB = {t["nome"]: t for t in json.loads((AD / "lote_b.json").read_text(encoding="utf-8"))["trechos"]}
    trocar = {"i1r": "i1s", "j1": "j1b", "k1": "k1b"}
    for s in SEGS:
        if s["nome"] in trocar:
            t = LB[trocar[s["nome"]]]; assert (t["q0"], t["q1"]) == (s["q0"], s["q1"]); plano.append(dict(t, tipo="B"))
        else: plano.append(dict(s, tipo="A"))
else:
    plano = [dict(s, tipo="A") for s in SEGS]
plano.sort(key=lambda s: s["q0"])
# ---------------- base ----------------
REC = (200, 180, 360, 640, 291) if NN == "16" else None
def bases():
    gen = base_lama(ORIG, VELHA, AD / "base_sem_legenda_mask.npy", N, log); buf = {}
    for q, f in gen:
        eb.stdin.write(f.tobytes())
        if not REC: yield q, f; continue
        x, y, w, h, ult = REC
        if q <= ult: f = cv2.resize(f[y:y + h, x:x + w], (720, 1280), interpolation=cv2.INTER_LANCZOS4)
        if ult < q < ult + 7: buf[q] = f; continue          # fusao: espera o 298
        if q == ult: A_ = f.astype(np.float32)
        if q == ult + 7:
            B_ = f.astype(np.float32); flash = np.zeros_like(A_); flash[:] = (200, 225, 255)
            for k in range(ult + 1, ult + 7):
                t = (k - ult) / 7; w_ = 0.55 * np.sin(np.pi * t)
                fk = np.clip((A_ * (1 - t) + B_ * t) * (1 - w_) + flash * w_, 0, 255).astype(np.uint8)
                ec.stdin.write(fk.tobytes()); yield k, fk
            log.append(f"abertura reenquadrada q0-{ult} + fusao com clarao {ult+1}-{ult+6}")
        ec.stdin.write(f.tobytes()); yield q, f
eb = enc(AD / "base_sem_legenda.mp4", FPS)
ec = enc(AD / "base_sem_legenda_crop.mp4", FPS) if REC else None
el = enc(AD / "base_lipsync.mp4", FPS, crf=14)
# ---------------- colagem ----------------
def cola_em(c, k):
    if c is None or not isinstance(c[0], (list, tuple)): return c
    K = np.array(c, float); return [int(round(np.interp(k, K[:, 0], K[:, j]))) for j in range(1, 5)]
def mascara_A(c):
    if c is None: return np.ones((1280, 720), np.float32)
    cx, cy, ax, ay = c; m = np.zeros((1280, 720), np.float32)
    cv2.ellipse(m, (cx, cy), (ax, ay), 0, 0, 360, 1.0, -1)
    return cv2.GaussianBlur(m, (0, 0), max(4, ax * 0.12))
def geo_A(s, k, b, g):
    """(full sem mistura, mascara 2D, caixa, fw) do quadro k do trecho de lote A"""
    c = cola_em(s["cola"], k); m = mascara_A(c)
    if s.get("crop"):
        x, y, w, h = s["crop"]; full = b.copy(); full[y:y + h, x:x + w] = cv2.resize(g, (w, h), interpolation=cv2.INTER_AREA); cx = (x, y, x + w, y + h)
    else:
        full = g if g.shape[:2] == (1280, 720) else cv2.resize(g, (720, 1280), interpolation=cv2.INTER_LANCZOS4); cx = (0, 0, 720, 1280)
    return full, m, cx, (2 * c[2] if c else 200)
def geo_B(Tr, k, b, g):
    x0, y0, w, h = Tr["X0"][k], Tr["Y0"][k], Tr["W"][k], Tr["H"][k]; r = Tr["rosto"][k]
    full = b.copy(); full[y0:y0 + h, x0:x0 + w] = cv2.resize(g, (w, h), interpolation=cv2.INTER_AREA)
    fw, fh = r[2] - r[0], r[3] - r[1]; m = np.zeros((1280, 720), np.float32)
    cv2.ellipse(m, (int((r[0] + r[2]) / 2), int(r[1] + 0.68 * fh)), (int(0.42 * fw + 6), int(0.36 * fh + 8)), 0, 0, 360, 1.0, -1)
    m[:y0, :] = 0; m[y0 + h:, :] = 0; m[:, :x0] = 0; m[:, x0 + w:] = 0
    return full, cv2.GaussianBlur(m, (0, 0), max(4, fw / 25)), (x0, y0, x0 + w, y0 + h), fw
def saida_A(s, n):
    p = AD / "lipsync" / "out" / f"ls_{s['nome']}.mp4"; g = list(quadros(p)); m0 = len(g)
    e = list(quadros(AD / "lipsync" / "in" / f"pt_{s['nome']}.mp4", 0, 2))
    d0 = np.abs(cv2.resize(g[0], (180, 320)).astype(np.float32) - cv2.resize(e[0], (180, 320))).mean()
    d1 = np.abs(cv2.resize(g[1], (180, 320)).astype(np.float32) - cv2.resize(e[1], (180, 320))).mean()
    drop = d0 > 3 * max(d1, 1.5)
    if drop: g = g[1:]
    return reamostrar(g, n), f"{m0} q{' (1o descartado)' if drop else ''} d0={d0:.1f} d1={d1:.1f}"
def saida_B(s, n):
    g = list(quadros(AD / "lipsync_b" / "out" / f"ls_{s['nome']}.mp4")); m0 = len(g)
    return reamostrar(g[:n] if len(g) > n else g, n), f"{m0} q"
pend = None   # (q, quadro de saida, base, mascara do fim, tipo) do ultimo quadro do trecho anterior
def escrever(f): el.stdin.write(f.tobytes())
B = bases(); q = 0
for s in plano:
    a, b_ = s["q0"], s["q1"]; n = b_ - a + 1
    while q < a:
        _, f = next(B)
        if pend: escrever(pend[1]); pend = None
        escrever(f); q += 1
    bs = [next(B)[1] for _ in range(n)]; q += n
    if s["tipo"] == "A": g, info = saida_A(s, n); geo = lambda k: geo_A(s, k, bs[k], g[k])
    else:
        Tr = json.loads((AD / "lipsync_b" / "trilhas" / f"{s['nome']}.json").read_text()); g, info = saida_B(s, n); geo = lambda k: geo_B(Tr, k, bs[k], g[k])
    if s["tipo"] == "A" and s["cola"] is None:
        C = None; log.append(f"{s['nome']} (A) {a}-{b_}: saida {info}; quadro inteiro, sem correcao (substituido)")
    else:
        C = medir([(bs[k],) + geo(k) for k in np.linspace(0, n - 1, 12).astype(int)])
        log.append(f"{s['nome']} ({s['tipo']}) {a}-{b_}: saida {info}; " + txt("cor", C))
    print(log[-1], flush=True)
    ultimo = None
    for k in range(n):
        full, m, cx, fw = geo(k)
        full = corrigir(full, C, m, cx) if C else full.astype(np.float32)
        o = np.clip(full * m[..., None] + bs[k] * (1 - m[..., None]) + 0.5, 0, 255).astype(np.uint8)
        if k == 0:
            if pend and pend[0] == a - 1:
                corte = np.abs(pend[2].astype(np.float32) - bs[0]).mean() > 10
                if corte: log.append(f"  emenda q{a}: corte de camera")
                else:
                    L, R = pend[1].astype(np.float32), o.astype(np.float32)
                    if s["tipo"] == "A" and pend[4] == "A":
                        M = np.maximum(pend[3], m)[..., None]
                        pend = (pend[0], np.clip((L * 0.6 + R * 0.4) * M + L * (1 - M), 0, 255).astype(np.uint8)) + pend[2:]
                        o = np.clip((R * 0.6 + L * 0.4) * M + R * (1 - M), 0, 255).astype(np.uint8)
                    else:
                        M = (m if s["tipo"] == "B" else pend[3])[..., None]
                        pend = (pend[0], np.clip((L * 2 / 3 + R / 3) * M + L * (1 - M), 0, 255).astype(np.uint8)) + pend[2:]
                        o = np.clip((L / 3 + R * 2 / 3) * M + R * (1 - M), 0, 255).astype(np.uint8)
                    log.append(f"  emenda q{a}: continua, crossfade na boca")
                print(log[-1], flush=True)
            if pend: escrever(pend[1]); pend = None
        if ultimo is not None: escrever(ultimo)
        ultimo = o
    pend = (b_, ultimo, bs[-1], m, s["tipo"])
    del bs, g
if pend: escrever(pend[1])
for _, f in B: escrever(f); q += 1
for e in (eb, ec, el):
    if e: e.stdin.close(); e.wait()
print("\n".join(log)); print("ok", N, "quadros")
(AD / "lipsync" / "recolocar_cor.log").write_text("\n".join(log) + f"\nok {N} quadros\n", encoding="utf-8")
