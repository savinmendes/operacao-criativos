import sys, cv2, time, numpy as np
from rapidocr_onnxruntime import RapidOCR
o = RapidOCR()
for p in sys.argv[1:]:
    f = cv2.imread(p); t=time.time()
    for _ in range(3): r, _ = o(f[660:910], use_det=True, use_cls=False, use_rec=False)
    print(p, round((time.time()-t)/3,3))
    for b in (r or []):
        b=np.array(b); print("  ", b[:,0].min(), b[:,1].min()+660, b[:,0].max(), b[:,1].max()+660)
