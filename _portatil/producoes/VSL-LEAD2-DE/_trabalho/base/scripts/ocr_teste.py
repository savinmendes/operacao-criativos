import sys, cv2, time
from rapidocr_onnxruntime import RapidOCR
o = RapidOCR()
for p in sys.argv[1:]:
    f = cv2.imread(p); t=time.time()
    r, _ = o(f[400:])
    print(p, round(time.time()-t,2))
    for b, txt, c in (r or []):
        xs=[q[0] for q in b]; ys=[q[1]+400 for q in b]
        print("  ", int(min(xs)),int(min(ys)),int(max(xs)),int(max(ys)), round(c,2), txt)
