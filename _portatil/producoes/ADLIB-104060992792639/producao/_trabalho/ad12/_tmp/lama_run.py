"""LaMa GPU nas faixas (legenda + seta) de um video, quadros [a,b). Uso: lama_run.py video.mp4 outdir a b
Salva outdir/NNNN.png (faixa R0:R1 preenchida) e outdir/mask_NNNN.png."""
import os, sys, time, warnings; warnings.filterwarnings("ignore")
import cv2, numpy as np, torch; torch.set_num_threads(4)
from PIL import Image
from simple_lama_inpainting import SimpleLama
sys.path.insert(0, os.path.dirname(__file__)); from mascara import mascara, R0, R1
vid, od, a, b = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]); os.makedirs(od, exist_ok=True)
C0, C1 = 640, 1210
lama = SimpleLama(); cap = cv2.VideoCapture(vid); cap.set(cv2.CAP_PROP_POS_FRAMES, a); t0 = time.time()
for i in range(a, b):
    ok, f = cap.read()
    if not ok: break
    m = mascara(f); cv2.imwrite(f"{od}/mask_{i:04d}.png", m * 255)
    out = f"{od}/{i:04d}.png"
    if m.sum() == 0: cv2.imwrite(out, f[R0:R1]); continue
    crop = f[C0:C1].copy(); mk = np.zeros(crop.shape[:2], np.uint8); mk[R0 - C0:R1 - C0] = m
    r = lama(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)), Image.fromarray(mk * 255))
    r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:crop.shape[0], :crop.shape[1]]
    cv2.imwrite(out, r[R0 - C0:R1 - C0])
    k = i - a + 1
    if k % 200 == 0: el = time.time() - t0; print(f"[{k}/{b-a}] {100*k//(b-a)}% falta ~{el/k*(b-a-k):.0f} s", flush=True)
print("ok", a, b, round(time.time() - t0))
