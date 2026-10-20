import cv2, numpy as np, sys
SRC = '../../../UNICOS_HD/11.mp4'
X0, X1, Y0, Y1 = 0, 720, 848, 968


def preencher(f, desloc, x0=X0, x1=X1, y0=Y0, y1=Y1, fe=14):
    h = y1 - y0
    out = f.copy()
    patch = f[y0 - desloc:y1 - desloc, x0:x1].astype(np.float32)
    alvo = f[y0 - fe:y1 + fe, x0:x1].astype(np.float32)
    # alpha: 1 dentro da faixa, rampas nas bordas de cima/baixo
    a = np.ones((h + 2 * fe, 1, 1), np.float32)
    ramp = np.linspace(0, 1, fe + 2)[1:-1]
    a[:fe, 0, 0] = ramp
    a[-fe:, 0, 0] = ramp[::-1]
    big = f[y0 - fe - desloc:y1 + fe - desloc, x0:x1].astype(np.float32)
    # corrige o tom: média da faixa de baixo (abaixo da legenda) vs patch
    res = big * a + alvo * (1 - a)
    out[y0 - fe:y1 + fe, x0:x1] = np.clip(res, 0, 255).astype(np.uint8)
    return out


if __name__ == '__main__':
    d = int(sys.argv[1])
    rows = []
    for t in [2.0, 10.5, 20.0, 45.5]:
        c = cv2.VideoCapture(SRC); c.set(0, t * 1000); ok, f = c.read()
        g = preencher(f, d)
        rows.append(np.hstack([f[760:1060], g[760:1060]]))
    cv2.imwrite('_tmp/copia.jpg', np.vstack(rows))
