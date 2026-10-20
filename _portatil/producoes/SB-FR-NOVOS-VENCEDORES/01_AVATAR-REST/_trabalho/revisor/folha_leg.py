import json, cv2, numpy as np, os, sys
R = sys.argv[1]
ocr = json.load(open(os.path.join(R, "ocr.json"), encoding="utf-8")) + json.load(open(os.path.join(R, "ocr2.json"), encoding="utf-8"))
crops = []; last = None
for t, items in ocr:
    leg = [it for it in items if 1150 < it[1] < 1450 and it[3] - it[1] < 120 and not (t < 5 and it[1] < 1300)]
    if not leg: continue
    txt = leg[0][4]
    if txt == last: continue
    last = txt
    im = cv2.imread(os.path.join(R, "q", f"{int(t*2)+1:04d}.jpg"))
    y0 = max(0, leg[0][1] - 45); y1 = leg[0][3] + 20
    c = im[y0:y1, 120:960].copy()
    c = cv2.copyMakeBorder(c, 0, 0, 90, 0, cv2.BORDER_CONSTANT, value=(40, 40, 40))
    cv2.putText(c, f"{t:.1f}", (5, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
    c = cv2.resize(c, (930, int(c.shape[0] * 930 / c.shape[1])))
    crops.append(c)
H = 1800; sheets = []; cur = []; h = 0
for c in crops:
    if h + c.shape[0] > H and cur:
        sheets.append(cur); cur = []; h = 0
    cur.append(c); h += c.shape[0]
sheets.append(cur)
for i, s in enumerate(sheets):
    w = max(c.shape[1] for c in s)
    img = np.vstack([cv2.copyMakeBorder(c, 0, 2, 0, w - c.shape[1], cv2.BORDER_CONSTANT, value=(0, 0, 255)) for c in s])
    cv2.imwrite(os.path.join(R, f"leg_{i}.jpg"), img, [cv2.IMWRITE_JPEG_QUALITY, 90])
print(len(crops), len(sheets))
