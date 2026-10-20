import numpy as np, cv2, sys
from PIL import Image
sys.path.insert(0, ".")
from simple_lama_inpainting import SimpleLama
f = np.asarray(Image.open("dono2/ref_dono_orig.png").convert("RGB"))
r, g, b = [f[625:760, :, k].astype(int) for k in range(3)]
core = ((np.minimum(np.minimum(r, g), b) > 205) | ((g > 120) & (g > r + 50) & (g > b + 50))).astype(np.uint8)
m = np.zeros(f.shape[:2], np.uint8); m[625:760] = cv2.dilate(core, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (23, 23)))
ys, xs = np.where(m); m[:] = 0; m[ys.min():ys.max() + 1, 60:660] = 1   # caixa da legenda inteira
out = np.array(SimpleLama()(Image.fromarray(f), Image.fromarray(m * 255)))[:1280, :720]
Image.fromarray(out).save("dono2/ref_dono_limpa.png"); print(ys.min(), ys.max())
