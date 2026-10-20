# compara original x lipsync: diff media por bloco 48x48 na metade de cima; o bloco de maior diff ~ boca.
# imprime: diff do pior bloco (media no tempo), posicao, e diff mediana do quadro (ruido de recodificacao)
import sys, cv2, numpy as np
sys.path.insert(0, '..')
from segs import SEGS
def frames(p):
    c = cv2.VideoCapture(p); out = []
    while True:
        ok, f = c.read()
        if not ok: break
        out.append(f)
    return out
for n, q, a, b in SEGS:
    if len(sys.argv) > 1 and n not in sys.argv[1:]: continue
    A = frames(f'../seg_{n}.mp4'); B = frames(f'ls_{n}.mp4')
    if not B: print(n, 'sem saida'); continue
    m = min(len(A), len(B)); acc = np.zeros((800 // 48, 720 // 48)); med = []; pq = []
    for i in range(0, m, 2):
        d = np.abs(A[i][:768].astype(float) - B[i][:768].astype(float)).mean(2)
        bl = d[:16 * 48, :15 * 48].reshape(16, 48, 15, 48).mean((1, 3))
        acc += bl; med.append(np.median(d)); pq.append(bl.max())
    acc /= len(range(0, m, 2)); y, x = np.unravel_index(acc.argmax(), acc.shape)
    print(n, 'quadros', len(A), len(B), 'pior bloco', round(acc.max(), 2), 'em (x,y)', (x * 48 + 24, y * 48 + 24), 'ruido', round(float(np.median(med)), 2), 'max/quadro', round(float(np.mean(pq)), 2))
    # folha de zoom: 4 quadros, original em cima, lipsync embaixo, recorte 192x192 centrado no pior bloco
    cx, cy = min(max(x * 48 + 24, 96), 720 - 96), min(max(y * 48 + 24, 96), 1280 - 96)
    idx = np.linspace(0, m - 1, 6).astype(int)
    top = np.hstack([A[i][cy - 96:cy + 96, cx - 96:cx + 96] for i in idx]); bot = np.hstack([B[i][cy - 96:cy + 96, cx - 96:cx + 96] for i in idx])
    cv2.imwrite(f'zoom_{n}.jpg', np.vstack([top, bot]))
