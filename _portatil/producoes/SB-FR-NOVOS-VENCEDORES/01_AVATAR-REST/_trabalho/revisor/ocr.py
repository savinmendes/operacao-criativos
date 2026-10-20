import sys, glob, os, json, cv2
from rapidocr_onnxruntime import RapidOCR
sys.stdout.reconfigure(encoding="utf-8")
eng = RapidOCR()
out = []
for p in sorted(glob.glob(os.path.join(sys.argv[1], "*.jpg")))[int(sys.argv[3]):int(sys.argv[4])]:
    i = int(os.path.basename(p)[:4]); t = (i - 1) / 2
    im = cv2.imread(p)
    r, _ = eng(im)
    items = []
    for box, txt, sc in (r or []):
        ys = [b[1] for b in box]; xs = [b[0] for b in box]
        items.append((round(min(xs)), round(min(ys)), round(max(xs)), round(max(ys)), txt, round(sc, 2)))
    out.append((t, items))
    print(f"{t:5.1f} | " + " || ".join(f"[{y0}-{y1} x{x0}-{x1}] {tx} ({sc})" for x0, y0, x1, y1, tx, sc in items))
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False)
