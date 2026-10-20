import numpy as np, cv2
def bordas(g, b):
    """g: cinza float; b: det box. Acha as bordas da caixa escura (degrau de luminancia)."""
    x0, y0, x1, y1 = b; H, W = g.shape
    xs = slice(max(0, x0 + 8), min(W, x1 - 8)); ys = slice(max(0, y0 + 3), min(H, y1 - 3))
    def melhor(cands, f):
        sc = [(f(c), c) for c in cands]; return max(sc)
    top = melhor(range(max(2, y0 - 12), y0 + 2), lambda y: np.median(g[y - 2, xs] - g[y + 1, xs]))
    bot = melhor(range(y1 - 2, min(H - 2, y1 + 12)), lambda y: np.median(g[y + 2, xs] - g[y - 1, xs]))
    lef = melhor(range(max(2, x0 - 14), x0 + 2), lambda x: np.median(g[ys, x - 2] - g[ys, x + 1]))
    rig = melhor(range(x1 - 2, min(W - 2, x1 + 14)), lambda x: np.median(g[ys, x + 2] - g[ys, x - 1]))
    return (lef[1], top[1], rig[1], bot[1]), (lef[0], top[0], rig[0], bot[0])
def razao(g, c):
    l, t, r, bb = c; out = []
    xs = slice(l + 10, r - 10); ys = slice(t + 3, bb - 3)
    for a, o in [(g[t + 2, xs], g[t - 3, xs]), (g[bb - 2, xs], g[bb + 3, xs]), (g[ys, l + 2], g[ys, l - 3]), (g[ys, r - 2], g[ys, r + 3])]:
        ok = (a < 190) & (a > 15) & (o > 20)
        if ok.sum() > 5: out.append(np.median(a[ok] / o[ok]))
    return out
