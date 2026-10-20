# Revisor (lote C): mapa medio de (final - original) em luma no rosto de quem fala, alinhado pelo centro da boca,
# media de N quadros de um trecho. Uma elipse colada mais escura aparece como mancha azul com borda nitida.
# Uso: python mapa_dif.py saida.jpg NN:pasta:t0:t1 ...
import sys, json, cv2, numpy as np
from pathlib import Path
P = Path(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639")
tiles = []
for arg in sys.argv[2:]:
    nn, d, t0, t1 = arg.split(":"); t0, t1 = float(t0), float(t1)
    esc = json.load(open(f"{d}/escolha_{nn}.json")); pos = {}
    for k, (a, b, tr) in esc.items():
        for q, cx, cy, L in tr: pos[q] = (cx, cy, L)
    fin = next((P / "producao").glob(f"AD {nn} - *-ES-LATAM.mp4")); ori = P / "UNICOS_HD" / f"{nn}.mp4"
    cf, co = cv2.VideoCapture(str(fin)), cv2.VideoCapture(str(ori)); fpo = co.get(cv2.CAP_PROP_FPS)
    mapa = (lambda t: t if t * 24 < 1286 else t + 70 / 24) if nn == "05" else (lambda t: t)
    acc = []; ref = None
    for q in range(int(t0 * 30), int(t1 * 30), 2):
        if q not in pos: continue
        cx, cy, L = pos[q]
        cf.set(cv2.CAP_PROP_POS_FRAMES, q); co.set(cv2.CAP_PROP_POS_FRAMES, int(round(mapa(q / 30) * fpo)))
        a, b = cf.read()[1], co.read()[1]
        if a is None or b is None: continue
        h = int(0.8 * L); x0, y0 = int(cx - h), int(cy - 1.1 * h)
        if x0 < 0 or y0 < 0 or x0 + 2 * h > 720 or y0 + 2 * h > 1280: continue
        Y = lambda im: cv2.cvtColor(cv2.resize(im[y0:y0 + 2 * h, x0:x0 + 2 * h], (240, 240)), cv2.COLOR_BGR2YUV)[:, :, 0].astype(float)
        acc.append(Y(a) - Y(b)); ref = cv2.resize(a[y0:y0 + 2 * h, x0:x0 + 2 * h], (240, 240))
    m = cv2.GaussianBlur(np.mean(acc, 0), (0, 0), 3)
    off = np.median(m[60:150, 70:170])  # mediana da regiao central do rosto
    v = np.clip((m - off) / 4.0, -1, 1)  # +-4 niveis em torno da mediana
    col = np.zeros((240, 240, 3), np.uint8); col[..., 0] = np.clip(-v * 255, 0, 255); col[..., 2] = np.clip(v * 255, 0, 255)
    col = cv2.addWeighted(col, 0.75, cv2.cvtColor(cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR), 0.25, 0)
    t = np.vstack([ref, col]); cv2.putText(t, f"AD{nn} {t0:.0f}-{t1:.0f}s med{off:+.1f}", (3, 16), 0, 0.5, (0, 255, 255), 1); tiles.append(t)
rows = [np.hstack(tiles[i:i + 6] + [np.zeros_like(tiles[0])] * (6 - len(tiles[i:i + 6]))) for i in range(0, len(tiles), 6)]
cv2.imwrite(sys.argv[1], np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 88]); print("ok")
