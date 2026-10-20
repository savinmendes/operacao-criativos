# -*- coding: utf-8 -*-
"""Máscara por quadro da legenda PT queimada (GRIMORIO V2), v2.
OCR det (RapidOCR, quadro inteiro) -> caixas na faixa da legenda do trecho -> agrupa por linha e só aceita linha
CENTRADA (a legenda é centralizada; bordado da casula vira caixa estreita fora do centro) -> glifo branco (top-hat)
/ destaque roxo / amarelo dentro da caixa -> extensão lateral só até o espelho da linha (palavra que o OCR cortou)
-> quadro sem detecção herda as caixas do anterior se o glifo ainda estiver lá (>=60% dos pixels)."""
import sys, json, subprocess, numpy as np, cv2
from rapidocr_onnxruntime import RapidOCR
V = r"C:\Users\PICHAU\Downloads\GRIMORIO V2.mp4"
OUT = sys.argv[1]; QA, QB = int(sys.argv[2]), int(sys.argv[3])
BANDAS = [(0, 239, 625, 725, True), (232, 668, 1010, 1110, True), (657, 2290, 725, 880, False),
          (2279, 2628, 870, 975, False), (2616, 4645, 725, 880, False)]
e = RapidOCR(intra_op_num_threads=4)
K21 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
def glifos(f, x0, y0, x1, y1, extra):
    r = f[y0:y1, x0:x1]
    g = cv2.cvtColor(r, cv2.COLOR_BGR2GRAY)
    mn = r.min(2).astype(int); mx = r.max(2).astype(int)
    white = (mn >= 195) & ((mx - mn) <= 50)
    th = cv2.morphologyEx(g, cv2.MORPH_TOPHAT, K21)
    m = white & (th > 30)
    if extra:
        hsv = cv2.cvtColor(r, cv2.COLOR_BGR2HSV); h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
        roxo = (h >= 125) & (h <= 160) & (s >= 120) & (v >= 90)
        ama = (h >= 18) & (h <= 40) & (s >= 110) & (v >= 160)
        roxo = cv2.morphologyEx(roxo.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)).astype(bool)
        m = m | roxo | ama
    return m.astype(np.uint8), white.mean() > 0.45
def linhas(cx):
    """agrupa caixas por linha (sobreposição vertical) e devolve só as linhas centradas."""
    cx = sorted(cx, key=lambda b: b[1]); grupos = []
    for b in cx:
        for gr in grupos:
            g0 = min(q[1] for q in gr); g1 = max(q[3] for q in gr)
            if abs(gr[0][1] - b[1]) <= 12 and abs(gr[0][3] - b[3]) <= 12: gr.append(b); break
        else: grupos.append([b])
    ok = []
    for gr in grupos:
        gr = sorted(gr, key=lambda b: b[0])
        while gr:
            x0 = min(b[0] for b in gr); x1 = max(b[2] for b in gr); c = (x0 + x1) / 2
            if abs(c - 360) <= 45: break
            gr.remove(max(gr, key=lambda b: abs((b[0] + b[2]) / 2 - 360)))
        if gr: ok.append(gr)
    return ok
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", V, "-vf",
    "scale=in_color_matrix=bt709:in_range=full:flags=accurate_rnd+full_chroma_int,format=bgr24", "-f", "rawvideo", "-"],
    stdout=subprocess.PIPE)
T = 720 * 1280 * 3; MK = []; LOG = {}; i = 0; ANT = []
while True:
    b = p.stdout.read(T)
    if len(b) < T: break
    if i < QA: i += 1; continue
    if i >= QB: break
    f = np.frombuffer(b, np.uint8).reshape(1280, 720, 3)
    full = np.zeros((1280, 720), np.uint8); cand = []
    r_all, _ = e(f, use_cls=False, use_rec=False)
    for q0, q1, y0, y1, extra in BANDAS:
        if not (q0 <= i < q1): continue
        for q in (r_all or []):
            q = np.array(q); bx0, by0, bx1, by1 = q[:, 0].min(), q[:, 1].min(), q[:, 0].max(), q[:, 1].max()
            if not (y0 - 10 <= (by0 + by1) / 2 <= y1 + 10): continue
            if not (26 <= by1 - by0 <= 90): continue
            cand.append((int(max(0, bx0 - 8)), int(max(0, by0 - 6)), int(min(720, bx1 + 8)), int(min(1280, by1 + 8)), extra))
    usadas = []
    for gr in linhas(cand):
        X0 = min(b[0] for b in gr); X1 = max(b[2] for b in gr); Y0 = min(b[1] for b in gr); Y1 = max(b[3] for b in gr); extra = gr[0][4]
        # extensão até o espelho da linha (máx. 140 px)
        L, R = min(X0, 720 - X1), max(X1, 720 - X0)
        L, R = max(L, X0 - 140), min(R, X1 + 140)
        for X0b, X1b in [(b[0], b[2]) for b in gr] + [(L, X0), (X1, R)]:
            if X1b - X0b < 6: continue
            m, claro = glifos(f, X0b, Y0, X1b, Y1, extra)
            if claro and m.sum() < 0.04 * m.size: m[:] = 1
            if (X0b, X1b) in ((L, X0), (X1, R)):
                n, lab, st, _ = cv2.connectedComponentsWithStats(m); k = np.zeros_like(m)
                for j in range(1, n):
                    cy = st[j, 1] + st[j, 3] / 2
                    if 8 <= st[j, 3] <= 55 and st[j, 4] >= 12 and abs(cy - (Y1 - Y0) / 2) < 14: k[lab == j] = 1
                m = k
            full[Y0:Y1, X0b:X1b] |= m
        usadas.append((L, Y0, R, Y1, extra, int(full[Y0:Y1, L:R].sum())))
    if not usadas and ANT:      # OCR falhou neste quadro: herda se o texto ainda está lá
        for L, Y0, R, Y1, extra, cnt in ANT:
            m, _ = glifos(f, L, Y0, R, Y1, extra)
            if cnt > 0 and m.sum() >= 0.6 * cnt and m.sum() <= 1.4 * cnt:
                full[Y0:Y1, L:R] |= m; usadas.append((L, Y0, R, Y1, extra, cnt))
    ANT = usadas
    if full.any():
        d = cv2.dilate(full, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
        dn = np.zeros_like(d); dn[3:] = d[:-3]; d = d | dn
        full = cv2.dilate(d, np.ones((5, 5), np.uint8))
    MK.append(np.packbits(full)); LOG[i] = [list(u[:4]) for u in usadas]
    if i % 300 == 0: print(f"[{i}/4645] {100*i//4645}%", flush=True)
    i += 1
np.save(OUT, np.array(MK)); json.dump(LOG, open(OUT.replace(".npy", ".json"), "w"))
print("ok", i)
