# -*- coding: utf-8 -*-
"""Remove legenda queimada. Dois modos por linha de texto:
 - 'caixa' (caixa preta semitransparente ~0,67): desfaz o escurecimento (pixel/a) e o LaMa so preenche glifos + borda da caixa.
 - 'ret' (sem caixa ou caixa opaca): LaMa no retangulo da linha.
Leitura/gravacao com matriz bt601/tv fixa (comum3)."""
import numpy as np, cv2
from PIL import Image
A_PADRAO = 0.67
GL = 17
def juntar_linhas(bx):
    bx = sorted([list(b) for b in bx], key=lambda b: (b[1] + b[3]) / 2); L = []
    for b in bx:
        for l in L:
            cy, ly = (b[1] + b[3]) / 2, (l[1] + l[3]) / 2
            if abs(cy - ly) < 14:
                l[0] = min(l[0], b[0]); l[1] = min(l[1], b[1]); l[2] = max(l[2], b[2]); l[3] = max(l[3], b[3]); break
        else: L.append(b)
    return L
def _ref(g, ini, rng, f):
    best = (f(ini), ini)
    for c in rng:
        s = f(c)
        if s > best[0] + 3: best = (s, c)
    return best[1] if best[0] > 12 else ini
def caixa_linha(g, b):
    H, W = g.shape; x0, y0, x1, y1 = b
    xs = slice(max(0, x0 + 8), min(W, x1 - 8)); ys = slice(max(0, y0 + 4), min(H, y1 - 4))
    t0, b0, l0, r0 = y0 - 6, y1 + 4, x0 - 4, x1 + 8
    t0 = int(np.clip(t0, 3, H - 4)); b0 = int(np.clip(b0, 3, H - 4)); l0 = int(np.clip(l0, 3, W - 4)); r0 = int(np.clip(r0, 3, W - 4))
    t = _ref(g, t0, range(max(3, t0 - 6), t0 + 5), lambda y: np.median(g[y - 2, xs] - g[y + 1, xs]))
    bb = _ref(g, b0, range(b0 - 4, min(H - 3, b0 + 7)), lambda y: np.median(g[y + 2, xs] - g[y - 1, xs]))
    l = _ref(g, l0, range(max(3, l0 - 6), l0 + 5), lambda x: np.median(g[ys, x - 2] - g[ys, x + 1]))
    r = _ref(g, r0, range(r0 - 8, min(W - 3, r0 + 7)), lambda x: np.median(g[ys, x + 2] - g[ys, x - 1]))
    return [max(0, l), max(0, t), min(W, r), min(H, bb)]
def razao_borda(g, c):
    l, t, r, bb = c; H, W = g.shape; out = []
    xs = slice(l + 10, r - 10); ys = slice(t + 4, bb - 4)
    pares = []
    if t >= 4: pares.append((g[t + 2, xs], g[t - 3, xs]))
    if bb + 4 < H: pares.append((g[bb - 2, xs], g[bb + 3, xs]))
    if l >= 4: pares.append((g[ys, l + 2], g[ys, l - 3]))
    if r + 4 < W: pares.append((g[ys, r - 2], g[ys, r + 3]))
    for a, o in pares:
        ok = (a < 185) & (a > 12) & (o > 25)
        if ok.sum() > 8: out.append(float(np.median(a[ok] / o[ok])))
    return out
def preparar(f, boxes):
    """Devolve (f_desfeito, mascara_inpaint, modo_linhas)."""
    g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32); H, W = g.shape
    L = juntar_linhas(boxes); cx = np.zeros((H, W), np.uint8); mk = np.zeros((H, W), np.uint8); rz = []; modos = []
    cxs = []; info = []
    for b in L:
        c = caixa_linha(g, b); r = razao_borda(g, c); info.append((b, c, r)); rz += r
    boa = [x for x in rz if 0.55 <= x <= 0.80]
    eh_caixa = len(boa) >= 2 and len(boa) >= 0.4 * len(rz)
    for b, c, r in info:
        if eh_caixa: cxs.append(c); modos.append("caixa")
        else:
            p = 10; mk[max(0, b[1] - p):b[3] + p, max(0, b[0] - p):b[2] + p] = 1
            modos.append("ret%.2f" % (float(np.median(r)) if r else 1.0))
    out = f
    if cxs:
        for l, t, r, bb in cxs: cx[t:bb, l:r] = 1
        a = float(np.clip(np.median(boa), 0.6, 0.74))
        out = f.astype(np.float32); sel = cx > 0
        out[sel] = np.clip(out[sel] / a, 0, 255); out = out.astype(np.uint8)
        # glifo branco (+ contorno preto) so dentro da caixa
        gl = ((g > 185) & sel).astype(np.uint8)
        el = lambda n: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n, n))
        perto = cv2.dilate(gl, el(13)); escuro = ((g < 75) & (perto > 0)).astype(np.uint8)
        gl = cv2.dilate(cv2.dilate(gl, el(5)) | escuro, el(5))
        gl = cv2.dilate(gl, el(15))   # halo do glifo fora da mascara fazia o LaMa redesenhar a letra (fantasma cinza)
        borda = cv2.dilate(cx, np.ones((11, 11), np.uint8)) - cv2.erode(cx, np.ones((11, 11), np.uint8))
        mk |= gl | borda
    return out, mk, modos
def inpaint(lama, f, mk):
    if mk.sum() == 0: return f
    ys = np.where(mk.any(1))[0]; a0 = max(0, ys.min() - 90); a1 = min(f.shape[0], ys.max() + 60)
    crop = f[a0:a1]; m = mk[a0:a1]
    r = lama(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)), Image.fromarray(m * 255))
    r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:crop.shape[0], :crop.shape[1]]
    r = corrigir_fill(crop, m, r)
    o = f.copy(); al = np.maximum(cv2.GaussianBlur(m.astype(np.float32), (7, 7), 0), m)[..., None]
    o[a0:a1] = np.clip(r * al + crop * (1 - al), 0, 255).astype(np.uint8)
    return o

def corrigir_fill(crop, m, r, lim=12.0):
    """Se o LaMa desbotar o preenchimento (falha cinza-azulada em pele lisa: croma dentro << croma do anel em volta),
    usa o Telea no quadro inteiro. Checagem barata; o Telea so roda quando precisa."""
    mm = m > 0
    if not mm.any(): return r
    anel = (cv2.dilate(m.astype(np.uint8), np.ones((11, 11), np.uint8)) > 0) & ~mm
    labr = cv2.cvtColor(np.ascontiguousarray(r), cv2.COLOR_BGR2LAB).astype(np.float32)
    labc = cv2.cvtColor(np.ascontiguousarray(crop), cv2.COLOR_BGR2LAB).astype(np.float32)
    cr = np.hypot(labr[..., 1] - 128, labr[..., 2] - 128)[mm].mean(); ca = np.hypot(labc[..., 1] - 128, labc[..., 2] - 128)[anel].mean()
    if cr < ca - lim:
        corrigir_fill.quadros += 1
        return cv2.inpaint(crop, m.astype(np.uint8), 5, cv2.INPAINT_TELEA)
    return r
corrigir_fill.trocas = 0
corrigir_fill.quadros = 0
