# -*- coding: utf-8 -*-
"""Correcao de cor do lote C (REVISAO-LOTE-C) do AD 10, SEM credito HeyGen: refaz base_sem_legenda e base_lipsync NUMA
GERACAO SO, a partir do ORIGINAL (UNICOS_HD/10.mp4, 24 fps) e das saidas do HeyGen ja baixadas (lipsync/out), com a
leitura/gravacao exata do ad13/lipsync3/comum3.py.
- Base (= _tmp/montar_base.py): faixa y 700-1130 do LaMa (_tmp/lama/NNNN.png) colada so na mascara (lama_mask.npy),
  EMA 0,65 zerada nos cortes; cada PNG corrigido pelo desvio (mediana) medido fora da mascara (PNG x quadro lido agora).
- Lipsync (= lipsync/recolocar.py segs.json plano.json): recorte boxes/<nome>.json, reamostragem p/ n+pad, elipse
  boca/queixo do rosto, fusao de 4 quadros na boca nas emendas da mesma tomada.
- Cor de cada trecho do HeyGen: afim no recorte fora da elipse + anel de pele + ajuste interno (_lote/cor_trecho.py).
- Lote B (= _tmp/loteB/reenquadrar.py): abertura q0-232 reenquadrada so na personagem (recorte 320x569 em (400,230),
  ampliado 2,25x, Lanczos), aplicada no quadro ja sincronizado, na mesma passada.
Saidas: ../base_sem_legenda.mp4, ../base_sem_legenda_crop.mp4 (base limpa com a abertura reenquadrada, p/ a checagem),
../base_lipsync.mp4 (24 fps, sem audio). Uso (em ad10/lipsync): python recolocar_cor.py"""
import sys, json, numpy as np, cv2
from pathlib import Path
AQ = Path(__file__).resolve().parent; AD = AQ.parent; T = AD.parent; P = T.parents[1]
sys.path.insert(0, str(T / "_lote"))
from cor_trecho import quadros, enc, medir, corrigir, txt
ORIG = P / "UNICOS_HD" / "10.mp4"
CFG = json.loads((AQ / "segs.json").read_text(encoding="utf-8")); PL = json.loads((AQ / "plano.json").read_text(encoding="utf-8")); FPS = CFG["fps"]
MK = np.load(AD / "_tmp" / "lama_mask.npy", mmap_mode="r"); N = len(MK); R0, R1 = 700, 1130
X, Y, W, H, ULT = 400, 230, 320, 569, 232
log = []; offs = []
def rec(f): return cv2.resize(f[Y:Y + H, X:X + W], (720, 1280), interpolation=cv2.INTER_LANCZOS4)
def base_gen():
    ema = None; prev = None
    for i, f in enumerate(quadros(ORIG, 0, N)):
        g = cv2.resize(f, (90, 160)).astype(np.float32)
        if prev is not None and np.abs(g - prev).mean() > 20: ema = None
        prev = g
        m = np.array(MK[i]).astype(np.float32)
        if m.sum() > 0:
            l = cv2.imread(str(AD / "_tmp" / "lama" / f"{i:04d}.png")).astype(np.float32); roi = f[R0:R1].astype(np.float32)
            fora = cv2.dilate((m > 0).astype(np.uint8), np.ones((15, 15), np.uint8)) == 0
            dv = np.median(roi[fora] - l[fora], axis=0) if fora.sum() > 1000 else np.zeros(3, np.float32)
            offs.append(dv); l = l + dv
            ema = l if ema is None else 0.65 * l + 0.35 * ema
            a = np.maximum(cv2.GaussianBlur(m, (11, 11), 0), m)[..., None]
            f[R0:R1] = np.clip(ema * a + roi * (1 - a) + 0.5, 0, 255).astype(np.uint8)
        else: ema = None
        eb.stdin.write(f.tobytes()); ec.stdin.write((rec(f) if i <= ULT else f).tobytes())
        yield f
def elipse(face, cy=0.70, rx=0.38, ry=0.32):
    x0, y0, x1, y1 = face; fw, fh = x1 - x0, y1 - y0
    m = np.zeros((1280, 720), np.float32)
    cv2.ellipse(m, (int((x0 + x1) / 2), int(y0 + cy * fh)), (int(rx * fw), int(ry * fh)), 0, 0, 360, 1.0, -1)
    return cv2.GaussianBlur(m, (0, 0), max(3.0, 0.07 * fw)), fw
def geo(base, g, bx, par):
    X0, Y0, Wi, Hi = bx["crop"]; c = cv2.resize(g, (Wi, Hi), interpolation=cv2.INTER_AREA); full = base.copy()
    xa, ya, xb, yb = max(0, X0), max(0, Y0), min(720, X0 + Wi), min(1280, Y0 + Hi)
    full[ya:yb, xa:xb] = c[ya - Y0:yb - Y0, xa - X0:xb - X0]
    m, fw = elipse(bx["face"], **par)
    return full, m, (xa, ya, xb, yb), fw
def reamostrar(fr, n):   # = recolocar.py
    m = len(fr)
    if m == n: return fr
    out = []
    for i in range(n):
        x = i * (m - 1) / (n - 1); j = int(np.floor(x)); a = x - j
        out.append(fr[min(j, m - 1)] if (a < 1e-3 or j >= m - 1) else cv2.addWeighted(fr[j], 1 - a, fr[j + 1], a, 0))
    return out
eb, ec, el = enc(AD / "base_sem_legenda.mp4", FPS), enc(AD / "base_sem_legenda_crop.mp4", FPS), enc(AD / "base_lipsync.mp4", FPS, crf=14)
pos = 0
def escrever(q, f): el.stdin.write((rec(f) if q <= ULT else f).tobytes())
B = base_gen(); pend = []   # [(q, img, mask, base)] ultimos 2 quadros do trecho anterior
def ler_base(k):
    global pos
    fr = []
    while pos < k: fr.append(next(B)); pos += 1
    return fr
for sg in CFG["segs"]:
    nome = sg["nome"]; a, b = sg["q"]
    if nome not in PL: log.append(f"{nome}: sem lipsync (base)"); continue
    antes = ler_base(a)
    if antes:
        for q, f, _, _ in pend: escrever(q, f)
        pend = []
        for k, f in enumerate(antes): escrever(a - len(antes) + k, f)
    bases = ler_base(b + 1)
    arq = PL[nome]; assert "@" not in arq
    bx = json.loads((AQ / "boxes" / f"{nome}.json").read_text()); n, pad = bx["n"], bx["pad"]; assert n == len(bases), (nome, n, len(bases))
    g = list(quadros(AQ / arq)); m0 = len(g); g = reamostrar(g, n + pad)[:n]
    par = sg.get("elipse", {})
    C = medir([(bases[k],) + geo(bases[k], g[k], bx["boxes"][k], par) for k in np.linspace(0, n - 1, 12).astype(int)])
    log.append(f"{nome} {a}-{b}: {m0} quadros -> {n + pad} (usa {n}); " + txt("cor", C)); print(log[-1], flush=True)
    cur = []
    def colado(k):
        full, m, cx, fw = geo(bases[k], g[k], bx["boxes"][k], par); full = corrigir(full, C, m, cx); M = m[..., None]
        return np.clip(full * M + bases[k] * (1 - M) + 0.5, 0, 255).astype(np.uint8), M
    for k in range(min(2, n)):
        f, M = colado(k); cur.append((a + k, f, M, bases[k]))
    if pend and pend[-1][0] == a - 1:
        bA, bB = pend[-1][3], cur[0][3]
        if np.abs(cv2.resize(bA, (90, 160)).astype(float) - cv2.resize(bB, (90, 160))).mean() <= 10:
            A_, B_ = pend[-1][1].astype(np.float32), cur[0][1].astype(np.float32); alvo = (A_ + B_) / 2
            M = np.maximum(pend[-1][2], cur[0][2])
            seq = pend[-2:] + cur[:2]; ws = [0.25, 0.5, 0.5, 0.25][-len(seq):] if len(pend) >= 2 else [0.5, 0.5, 0.25]
            for (q, f, mm, bb), w in zip(seq, ws):
                f[:] = np.clip(f.astype(np.float32) * (1 - w * M) + alvo * (w * M), 0, 255).astype(np.uint8)
            log.append(f"emenda q{a}: fusao na boca"); print(log[-1], flush=True)
    for q, f, _, _ in pend: escrever(q, f)
    pend = []
    for k in range(2, n):
        f, M = colado(k); cur.append((a + k, f, M, bases[k]))
        if len(cur) > 2: q, f0, _, _ = cur.pop(0); escrever(q, f0)
    pend = cur; del bases, g
for q, f, _, _ in pend: escrever(q, f)
q0 = pos
for k, f in enumerate(ler_base(N)): escrever(q0 + k, f)
for e in (eb, ec, el): e.stdin.close(); e.wait()
log.insert(0, f"base: desvio LaMa PNG -> leitura nova (BGR, mediana de {len(offs)} quadros): {np.median(np.array(offs), 0).round(2)}")
log.append(f"abertura q0-{ULT} reenquadrada (recorte {W}x{H} em ({X},{Y})) no quadro ja sincronizado")
print("\n".join(log)); print("ok", pos, "quadros")
(AQ / "recolocar_cor.log").write_text("\n".join(log) + f"\nok {pos} quadros\n", encoding="utf-8")
