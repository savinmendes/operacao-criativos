# -*- coding: utf-8 -*-
"""Correcao de cor (REVISAO-LOTE-C) do AD 09: refaz base_sem_legenda + base_lipsync NUMA GERACAO SO, a partir do ORIGINAL
(UNICOS_HD/09.mp4), das faixas LaMa ja calculadas (_tmp/lama/NNNN.png + _tmp/lama_mask.npy) e das saidas do HeyGen ja
baixadas (lipsync/out/ls_*.mp4), com a leitura/gravacao exata do ad13/lipsync3/comum3.py (ffmpeg bt601 + accurate_rnd;
conversao inversa exata; etiqueta bt709/tv so no bitstream).
- Base = _tmp/montar_base.py (faixa y 700-1130 do LaMa so na mascara, borda suave, EMA 0,65 zerada nos cortes), com cada PNG
  corrigido pelo desvio (mediana BGR) medido fora da mascara (PNG x quadro lido agora). Nenhum LaMa novo.
- Lipsync = lipsync/recolocar.py segs.json plano.json (mesmas caixas boxes/*.json, mesma elipse, mesma reamostragem, mesma
  fusao de 4 quadros na boca nas emendas da mesma tomada) + lipsync/fechar_e1.py EM MEMORIA (q 1126-1130 recebem a boca
  fechada do q 1124 alinhada por olhos/nariz; 1130 com peso 0,6), sem passada intermediaria gravada.
- Cada trecho do HeyGen leva antes de colar o desvio de cor (BGR) medido num anel de pele em volta da elipse (fora dela),
  mediana de 12 quadros, + um ajuste interno (pele do filtro e do meio do queixo) aplicado com o peso da elipse.
Uso (em ad09/lipsync): python recolocar_cor.py  -> ../base_sem_legenda.mp4 e ../base_lipsync.mp4 (2490 q, 24 fps)"""
import sys, json, subprocess, numpy as np, cv2
from pathlib import Path
AQ = Path(__file__).resolve().parent; AD = AQ.parent; T = AD.parent; P = T.parents[1]
sys.path.insert(0, str(T / "ad13" / "lipsync3"))
from comum3 import quadros, ENC_VF, ENC_TAG
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
ORIG = P / "UNICOS_HD" / "09.mp4"; N = 2490; FPS = 24; R0, R1 = 700, 1130
CFG = json.loads((AQ / "segs.json").read_text(encoding="utf-8")); PL = json.loads((AQ / "plano.json").read_text(encoding="utf-8"))
MK = np.load(AD / "_tmp" / "lama_mask.npy", mmap_mode="r"); LAMA = AD / "_tmp" / "lama"
log = []
# ---------------- base (= _tmp/montar_base.py) ----------------
def base_gen():
    ema = None; prev = None; offs = []; cortes = []
    for i, f in enumerate(quadros(ORIG, 0, N)):
        g = cv2.resize(f, (90, 160)).astype(np.float32)
        if prev is not None and np.abs(g - prev).mean() > 20: ema = None; cortes.append(i)
        prev = g
        m = np.array(MK[i]).astype(np.float32)
        if m.sum() > 0:
            l = cv2.imread(str(LAMA / f"{i:04d}.png")).astype(np.float32); roi = f[R0:R1].astype(np.float32)
            fora = cv2.dilate((m > 0).astype(np.uint8), np.ones((15, 15), np.uint8)) == 0
            dv = np.median(roi[fora] - l[fora], axis=0) if fora.sum() > 1000 else np.zeros(3, np.float32)
            offs.append(dv); l = l + dv
            ema = l if ema is None else 0.65 * l + 0.35 * ema
            a = np.maximum(cv2.GaussianBlur(m, (11, 11), 0), m)[..., None]
            f[R0:R1] = np.clip(ema * a + roi * (1 - a), 0, 255).astype(np.uint8)
        else: ema = None
        yield i, f
    log.append(f"base: cortes {cortes}")
    if offs: log.append(f"desvio LaMa PNG -> leitura nova (BGR): mediana {np.median(np.array(offs), 0).round(2)}, "
                        f"p5 {np.percentile(np.array(offs), 5, 0).round(2)}, p95 {np.percentile(np.array(offs), 95, 0).round(2)} ({len(offs)} quadros)")
# ---------------- colagem (= recolocar.py) ----------------
def reamostrar(fr, n):   # = recolocar.reamostrar (interpola nos dois sentidos)
    m = len(fr)
    if m == n: return fr
    out = []
    for i in range(n):
        x = i * (m - 1) / (n - 1); j = int(np.floor(x)); a = x - j
        out.append(fr[min(j, m - 1)] if (a < 1e-3 or j >= m - 1) else cv2.addWeighted(fr[j], 1 - a, fr[j + 1], a, 0))
    return out
def elipse(face, cy=0.70, rx=0.38, ry=0.32):
    x0, y0, x1, y1 = face; fw, fh = x1 - x0, y1 - y0
    m = np.zeros((1280, 720), np.float32)
    cv2.ellipse(m, (int((x0 + x1) / 2), int(y0 + cy * fh)), (int(rx * fw), int(ry * fh)), 0, 0, 360, 1.0, -1)
    s = max(3.0, 0.07 * fw); m = cv2.GaussianBlur(m, (0, 0), s)
    return m[..., None]
def esticar(base, g, bx, d0=None, d1=None, M=None):
    X0, Y0, Wi, Hi = bx["crop"]
    c = cv2.resize(g, (Wi, Hi), interpolation=cv2.INTER_AREA).astype(np.float32)
    full = base.astype(np.float32).copy()
    xa, ya, xb, yb = max(0, X0), max(0, Y0), min(720, X0 + Wi), min(1280, Y0 + Hi)
    full[ya:yb, xa:xb] = c[ya - Y0:yb - Y0, xa - X0:xb - X0]
    dentro = np.zeros((1280, 720), bool); dentro[ya:yb, xa:xb] = True
    if d0 is not None:
        full[ya:yb, xa:xb] += d0 + d1 * M[ya:yb, xa:xb]
    return full, dentro
def colar(base, g, bx, par, d0, d1):
    M = elipse(bx["face"], **par)
    full, _ = esticar(base, g, bx, d0, d1, M)
    return np.clip(full * M + base * (1 - M), 0, 255).astype(np.uint8), M
def desvio(bases, g, BX, par):
    ks = np.linspace(0, len(bases) - 1, 12).astype(int); d0s = []
    for k in ks:
        bx = BX[k]; x0, y0, x1, y1 = bx["face"]; fw = x1 - x0
        m = elipse(bx["face"], **par)[..., 0]; dentro = m > 0.01
        full, cx = esticar(bases[k], g[k], bx)
        e = cv2.erode(cx.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
        anel = cv2.dilate(dentro.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(0.5 * fw) | 1,) * 2)).astype(bool) & ~dentro & e
        if anel.sum() < 50: continue
        d0s.append((bases[k].astype(np.float32) - full)[anel].mean(0))
    d0 = np.median(np.array(d0s), 0) if d0s else np.zeros(3, np.float32); dis = []
    for k in ks:
        bx = BX[k]; x0, y0, x1, y1 = bx["face"]; fw, fh = x1 - x0, y1 - y0; rr = max(3, int(0.05 * fw))
        full, _ = esticar(bases[k], g[k], bx); full = full + d0; bb = bases[k].astype(np.float32)
        for fy in (0.655, 0.915):
            x, y = int((x0 + x1) / 2), int(y0 + fy * fh)
            dis.append((bb[y-rr:y+rr, x-rr:x+rr] - full[y-rr:y+rr, x-rr:x+rr]).reshape(-1, 3).mean(0))
    d1 = np.clip(np.median(np.array(dis), 0), -8, 8) if dis else np.zeros(3, np.float32)
    return d0, d1
# ---------------- fechar_e1 (= lipsync/fechar_e1.py, em memoria) ----------------
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=3))
EST = [33, 133, 362, 263, 168, 6, 197, 195, 5, 4, 1, 234, 454, 127, 356]
REF, ALVO, REF_APROVADO = range(1122, 1126), range(1126, 1131), 1124
FACE = (321, 342, 474, 533)
def marcos(f):
    cx, cy = (FACE[0] + FACE[2]) // 2, (FACE[1] + FACE[3]) // 2; L = 420
    x0, y0 = max(0, cx - L // 2), max(0, cy - L // 2)
    rec = np.ascontiguousarray(cv2.cvtColor(f[y0:y0 + L, x0:x0 + L], cv2.COLOR_BGR2RGB))
    r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rec))
    ps = [np.array([(x0 + p.x * rec.shape[1], y0 + p.y * rec.shape[0]) for p in fl]) for fl in r.face_landmarks]
    if not ps: return None
    return min(ps, key=lambda p: np.hypot(*(p[1] - (cx, cy))))
def mascara_f(p):
    lab = (p[13] + p[14]) / 2; qx = p[152]; nz = p[2]
    c = (lab + qx) / 2 + np.array([0, 0.08 * np.linalg.norm(qx - nz)])
    ax = int(0.62 * np.linalg.norm(p[61] - p[291]) + 18); ay = int(0.62 * np.linalg.norm(qx - nz) + 8)
    m = np.zeros((1280, 720), np.float32); cv2.ellipse(m, (int(c[0]), int(c[1])), (ax, ay), 0, 0, 360, 1.0, -1)
    return cv2.GaussianBlur(m, (0, 0), 7)
def fechar_e1(fr):
    """fr: {q: quadro} com 1122..1130 (ja com a fusao da emenda E1|E2). Altera 1126..1130 no lugar."""
    Pm = {k: marcos(fr[k]) for k in range(1122, 1131)}
    ab = {k: (cl._abertura(p) if p is not None else np.nan) for k, p in Pm.items()}
    rmin = min(REF, key=lambda k: ab[k] if np.isfinite(ab[k]) else 9)
    log.append("fechar_e1 abertura antes: " + " ".join(f"{k}:{ab[k]:.3f}" for k in sorted(ab)) + f" | menor ref {rmin}, usada {REF_APROVADO}")
    r = REF_APROVADO; pr = Pm[r]; ref = fr[r].copy()
    for k in ALVO:
        pk = Pm[k]
        if pk is None: log.append(f"fechar_e1: sem rosto {k}"); continue
        M, _ = cv2.estimateAffinePartial2D(pr[EST].astype(np.float32), pk[EST].astype(np.float32))
        g = cv2.warpAffine(ref, M, (720, 1280), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        ms = mascara_f(pk)[..., None] * (0.6 if k == 1130 else 1.0)
        fr[k][:] = np.clip(g * ms + fr[k] * (1 - ms), 0, 255).astype(np.uint8)
    log.append("fechar_e1 abertura depois: " + " ".join(f"{k}:{cl._abertura(marcos(fr[k])):.3f}" for k in range(1122, 1131)))
# ---------------- gravacao ----------------
def enc(path, crf):
    return subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",str(FPS),"-i","-",
        *ENC_VF,"-threads","4","-c:v","libx264","-crf",str(crf),"-preset","medium","-pix_fmt","yuv420p",*ENC_TAG,"-an",str(path)], stdin=subprocess.PIPE)
eb, el = enc(AD / "base_sem_legenda.mp4", 12), enc(AD / "base_lipsync.mp4", 14)
gen = base_gen(); pos = 0; nl = 0
def ler_base(k):
    global pos
    fr = []
    while pos < k:
        try: i, f = next(gen)
        except StopIteration: break
        eb.stdin.write(f.tobytes()); fr.append(f); pos += 1
    return fr
def wl(f):
    global nl
    el.stdin.write(f.tobytes()); nl += 1
pend = []   # [(q, img, mask, base)] ainda nao escritos
def flush():
    global pend
    for _, f, _, _ in pend: wl(f)
    pend = []
for sg in CFG["segs"]:
    nome = sg["nome"]; a, b = sg["q"]
    if nome not in PL: log.append(f"{nome}: sem lipsync (base)"); continue
    antes = ler_base(a)
    if antes:
        flush()
        for f in antes: wl(f)
    bases = ler_base(b + 1)
    arq, _, pula = PL[nome].partition("@")
    bx = json.loads((AQ / "boxes" / f"{nome}.json").read_text()); n, pad = bx["n"], bx["pad"]; assert n == len(bases), (nome, n, len(bases))
    g = list(quadros(AQ / arq, int(pula or 0))); m = len(g)
    g = reamostrar(g, n + pad)[:n]
    par = sg.get("elipse", {}); BX = bx["boxes"]
    d0, d1 = desvio(bases, g, BX, par)
    cur = []
    for i in range(n):
        f, M = colar(bases[i], g[i], BX[i], par, d0, d1); cur.append((a + i, f, M, bases[i]))
    del g
    log.append(f"{nome}: {m} quadros -> {n + pad} (usa {n}); desvio anel BGR {d0.round(2)} + interno {d1.round(2)}")
    if pend and pend[-1][0] == a - 1:
        bA, bB = pend[-1][3], cur[0][3]
        dif = np.abs(cv2.resize(bA, (90, 160)).astype(float) - cv2.resize(bB, (90, 160))).mean()
        if dif <= 10:
            A_, B_ = pend[-1][1].astype(np.float32), cur[0][1].astype(np.float32); alvo = (A_ + B_) / 2
            M = np.maximum(pend[-1][2], cur[0][2])
            seq = pend[-2:] + cur[:2]; ws = [0.25, 0.5, 0.5, 0.25][-len(seq):] if len(pend) >= 2 else [0.5, 0.5, 0.25]
            for (q, f, mm, bb), w in zip(seq, ws):
                f[:] = np.clip(f.astype(np.float32) * (1 - w * M) + alvo * (w * M), 0, 255).astype(np.uint8)
            log.append(f"  emenda q{a}: fusao na boca (dif {dif:.1f})")
        else: log.append(f"  emenda q{a}: corte (dif {dif:.1f})")
    if pend and pend[-1][0] == 1130:   # E1 guardado ate a fusao E1|E2 -> fechar_e1 em memoria
        fechar_e1({q: f for q, f, _, _ in pend})
    flush()
    guarda = 9 if nome == "E1" else 2   # E1: guarda 1122..1130 p/ o fechar_e1
    for q, f, M, bb in cur[:-guarda]: wl(f)
    pend = cur[-guarda:]
    print(log[-1], flush=True)
flush()
for f in ler_base(10**9): wl(f)
eb.stdin.close(); eb.wait(); el.stdin.close(); el.wait()
print("\n".join(log)); print("ok", pos, "quadros base,", nl, "quadros lipsync")
