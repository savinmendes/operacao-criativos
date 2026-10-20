import cv2, numpy as np, time, warnings
warnings.filterwarnings("ignore")
from simple_lama_inpainting import SimpleLama
from PIL import Image
lama = SimpleLama(); BM = np.load('_tmp/boxmasks.npy')
c = cv2.VideoCapture('../../../UNICOS_HD/13.mp4'); rows = []
for t in [2.0, 20.0, 31.0, 45.0, 86.0, 100.0, 107.5]:
    fi = int(round(t * 30)); c.set(1, fi); ok, f = c.read()
    crop = f[840:1160].copy()
    m = np.zeros(crop.shape[:2], np.uint8); m[960-840:1030-840] = BM[fi]
    t0 = time.time()
    r = lama(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)), Image.fromarray(m * 255))
    r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:crop.shape[0], :crop.shape[1]]
    print(t, round(time.time() - t0, 2))
    rows.append(np.hstack([crop[90:230], r[90:230]]))
cv2.imwrite('_tmp/lama.jpg', np.vstack(rows))
