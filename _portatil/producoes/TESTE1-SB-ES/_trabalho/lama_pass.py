# -*- coding: utf-8 -*-
"""Base limpa do TESTE1: LaMa (GPU) na legenda PT, nos textos da moldura da live e no título/círculos do quadro das 12 palavras.
Leitura/gravação com matriz bt601 fixa (comum3). Saída: lama/base_limpa.mp4 + lama/base_mask.npy"""
import sys, time, warnings; warnings.filterwarnings("ignore")
import numpy as np, cv2, subprocess
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG
import mascaras as M
from PIL import Image
from simple_lama_inpainting import SimpleLama
SRC = r"C:\Users\PICHAU\Downloads\TESTE1.mp4"
M.REF_RED = M.red_mask(next(quadros(SRC, 2127, 1)))
lama = SimpleLama()
N = 4257
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "720x1280", "-r", "30", "-i", "-",
                       *ENC_VF, "-threads", "4", "-c:v", "libx264", "-crf", "12", "-preset", "medium", *ENC_TAG, "-an", "lama/base_limpa.mp4"],
                      stdin=subprocess.PIPE)
MK = []; prev = None; ema = None; ecob = None; t0 = time.time()
def inpaint(f, m, a0, a1):
    crop = f[a0:a1].copy(); mk = m[a0:a1]
    r = lama(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)), Image.fromarray(mk * 255))
    return cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:crop.shape[0], :crop.shape[1]].astype(np.float32)
for q, f in enumerate(quadros(SRC)):
    g = cv2.resize(f, (90, 160)).astype(np.float32)
    if prev is not None and np.abs(g - prev).mean() > 20: ema = None
    prev = g
    m = M.mascara(f, q); MK.append(np.packbits(m))
    if m.sum() == 0:
        ema = None; ff.stdin.write(f.tobytes()); continue
    l = f.astype(np.float32); cob = np.zeros(1280, bool)
    ys = np.where(m.any(1))[0]
    # regiões separadas (topo / meio / base) para recortes menores
    grupos = []; ini = ys[0]; ult = ys[0]
    for y in ys[1:]:
        if y - ult > 120: grupos.append((ini, ult)); ini = y
        ult = y
    grupos.append((ini, ult))
    for y0, y1 in grupos:
        a0 = max(0, y0 - 80); a1 = min(1280, y1 + 80)
        l[a0:a1] = inpaint(f, m, a0, a1); cob[a0:a1] = True
    if ema is None: ema, ecob = l, cob
    else:
        both = (cob & ecob)[:, None, None]
        ema = np.where(both, 0.65 * l + 0.35 * ema, l); ecob = cob
    al = np.maximum(cv2.GaussianBlur(m.astype(np.float32), (11, 11), 0), m)[..., None]
    o = np.clip(ema * al + f * (1 - al), 0, 255).astype(np.uint8)
    ff.stdin.write(np.ascontiguousarray(o).tobytes())
    if (q + 1) % 150 == 0:
        el = time.time() - t0; print(f"[{q+1}/{N}] {100*(q+1)//N}% falta ~{el/(q+1)*(N-q-1)/60:.1f} min", flush=True)
ff.stdin.close(); ff.wait()
np.save("lama/base_mask.npy", np.array(MK)); print("ok", q + 1, round(time.time() - t0), "s")
