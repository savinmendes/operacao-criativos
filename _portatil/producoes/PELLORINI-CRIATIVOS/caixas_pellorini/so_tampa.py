# Monta a foto final = original + só a região da marca da tampa vinda da versão editada (mostrador fica 100% original)
import glob, os
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
for f in sorted(glob.glob("pellorini/*.jpg")):
    n = os.path.basename(f)
    ed = Image.open(f).convert("RGB")
    orig = Image.open("orig_full/" + n.replace(".jpg", ".png")).convert("RGB").resize(ed.size, Image.LANCZOS)
    a = np.asarray(orig).astype(int); b = np.asarray(ed).astype(int)
    dif = np.abs(a - b).sum(2)
    H, W = dif.shape
    m = dif > 60
    m[int(H * 0.55):] = False          # marca fica na metade de cima (tampa)
    m = ndimage.binary_opening(m, iterations=2)
    m = ndimage.binary_dilation(m, iterations=6)
    lab, k = ndimage.label(m)
    if k == 0: print("sem diferença", n); continue
    tam = ndimage.sum(m, lab, range(1, k + 1))
    # junta os blobs que ficam na mesma faixa horizontal do maior (as letras)
    big = np.argmax(tam) + 1
    ys, xs = np.where(lab == big)
    cy = ys.mean()
    sel = np.zeros_like(m)
    for i in range(1, k + 1):
        yy, xx = np.where(lab == i)
        if abs(yy.mean() - cy) < 80 and tam[i - 1] > 50: sel |= lab == i
    ys, xs = np.where(sel)
    y0, y1, x0, x1 = ys.min() - 25, ys.max() + 25, xs.min() - 40, xs.max() + 40
    mask = Image.new("L", ed.size, 0)
    mask.paste(255, (max(0, x0), max(0, y0), min(W, x1), min(H, y1)))
    mask = mask.filter(ImageFilter.GaussianBlur(10))
    final = Image.composite(ed, orig, mask)
    final.save("loja_final/" + n, quality=94)
    print(n, "caixa", (x0, y0, x1, y1))
