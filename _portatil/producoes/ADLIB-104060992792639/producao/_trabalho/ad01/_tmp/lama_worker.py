"""LaMa local na faixa da legenda (y 820-990) do 01.mp4, quadros [a,b). Salva a faixa preenchida em _tmp/lama/NNNN.png."""
import sys, os, time, warnings
warnings.filterwarnings("ignore")
import torch; torch.set_num_threads(int(sys.argv[3]) if len(sys.argv) > 3 else 7)
import cv2, numpy as np
from PIL import Image
from simple_lama_inpainting import SimpleLama
a, b = int(sys.argv[1]), int(sys.argv[2])
Y0, Y1, C0, C1 = 820, 990, 760, 1056
BM = np.load('_tmp/boxmasks.npy', mmap_mode='r')
lama = SimpleLama()
cap = cv2.VideoCapture('../../../UNICOS_HD/01.mp4'); cap.set(cv2.CAP_PROP_POS_FRAMES, a)
t0 = time.time()
for i in range(a, b):
    ok, f = cap.read()
    out = f'_tmp/lama/{i:04d}.png'
    if os.path.exists(out): continue
    m = np.array(BM[i])
    if m.sum() == 0:
        cv2.imwrite(out, f[Y0:Y1]); continue
    crop = f[C0:C1].copy(); mk = np.zeros(crop.shape[:2], np.uint8)
    mk[Y0 - C0:Y1 - C0] = cv2.dilate(m, np.ones((5, 5), np.uint8))
    r = lama(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)), Image.fromarray(mk * 255))
    r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:crop.shape[0], :crop.shape[1]]
    cv2.imwrite(out, r[Y0 - C0:Y1 - C0])
    k = i - a + 1
    if k % 25 == 0:
        el = time.time() - t0; print(f"[{k}/{b-a}] {100*k//(b-a)}% falta ~{el/k*(b-a-k)/60:.0f} min", flush=True)
print("ok", a, b)
