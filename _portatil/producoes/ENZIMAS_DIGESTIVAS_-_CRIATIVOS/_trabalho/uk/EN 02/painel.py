# -*- coding: utf-8 -*-
"""Apaga o pais ("United States") do print de avaliacoes (q 3343-3404, painel x 81-289, y 167-513).
Acha cada linha de autor pelo avatar redondo na margem esquerda, mede onde termina o nome (texto escuro) e,
na faixa da linha, deixa branco tudo que for cinza-claro sem cor depois do nome (ate antes do menu "...")."""
import numpy as np, cv2
Q0, Q1 = 3343, 3405
X0, X1, Y0, Y1 = 81, 289, 167, 513
def avatares(g):
    nb = (g < 225).astype(np.float32); H, W = g.shape; ys = []
    for y in range(6, H - 6):
        a = nb[y - 5:y + 6, 8:20].mean()
        gap = nb[y - 6:y + 7, 21:24].mean()
        lim = 0.55 if y < H - 22 else 0.25
        if a > lim and gap < 0.15 and (g[max(0, y - 8):y + 3, 25:80] < 165).sum() > 15:
            if not ys or y - ys[-1][-1] > 1: ys.append([y])
            else: ys[-1].append(y)
    return [int(np.mean(v)) for v in ys if len(v) >= 2]
def limpar(f):
    p = f[Y0:Y1, X0:X1]
    g = cv2.cvtColor(p, cv2.COLOR_BGR2GRAY).astype(np.int16)
    sat = p.max(2).astype(np.int16) - p.min(2).astype(np.int16)
    out = p.copy(); W = g.shape[1]; info = []
    PAD = 8
    gp = np.pad(g, ((PAD, PAD), (0, 0)), mode="edge")
    for yc in [y - PAD for y in avatares(gp)]:
        # linha do nome: um pouco acima do centro do avatar
        best = None
        for ya in range(max(2, yc - 9), max(3, min(g.shape[0] - 8, yc + 1))):
            band = g[ya:ya + 7, 25:W - 22]
            d = (band < 165).sum()
            if best is None or d > best[1]: best = (ya, d)
        ya = best[0]; band = g[ya - 1:ya + 8, 25:W - 22]; bs = sat[ya - 1:ya + 8, 25:W - 22]
        cols = np.where(((band < 178) | (bs >= 40)).any(0))[0]
        if not len(cols): continue
        fim = cols[0]
        for c in cols:
            if c - fim > 4: break
            fim = c
        x0 = 25 + fim + 2; x1 = W - 22
        sub = g[ya - 2:ya + 8, x0:x1]; ss = sat[ya - 2:ya + 8, x0:x1]
        m = (sub >= 110) & (ss < 40)
        reg = out[ya - 2:ya + 8, x0:x1]; reg[m] = 255
        info.append((yc, ya, x0))
    # borda de baixo (linha de autor cortada pela borda do painel): cinza-claro vira branco
    B = 12; sb = g[-B:, 60:W - 22]; ssb = sat[-B:, 60:W - 22]
    mb = (sb >= 150) & (ssb < 40); rb = out[-B:, 60:W - 22]; rb[mb] = 255
    f = f.copy(); f[Y0:Y1, X0:X1] = out
    return f, info
if __name__ == "__main__":
    from comum3 import quadros
    ims = []
    for k, f in enumerate(quadros("../../../INGLES/EN 02 - ENZIMAS-TRUQUE-6-MESES-GRAVIDA.mp4", Q0, Q1 - Q0)):
        g, info = limpar(f)
        if k % 6 == 0:
            print(Q0 + k, info); ims.append(cv2.resize(g[160:520, 75:295], None, fx=1.5, fy=1.5))
    cv2.imwrite('chk_painel.jpg', np.hstack(ims[:6])); cv2.imwrite('chk_painel2.jpg', np.hstack(ims[6:]))
