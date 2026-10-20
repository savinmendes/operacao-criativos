import cv2, json, sys
V = "../../../VIDEOS/09 - Vitaly - 1855505272004884.mp4"
inits = json.loads(sys.argv[1])  # {"frame": [x,y,w,h]} re-init points
end = int(sys.argv[2])
cap = cv2.VideoCapture(V); boxes = {}; tr = None; n = 0
while n <= end:
    ok, im = cap.read()
    if not ok: break
    if str(n) in inits:
        b = inits[str(n)]
        if b is None: tr = None
        else:
            tr = cv2.TrackerCSRT_create(); tr.init(im, tuple(b)); boxes[n] = b
    elif tr is not None:
        ok2, b = tr.update(im)
        boxes[n] = [int(v) for v in b] if ok2 else None
    n += 1
json.dump(boxes, open('boxes.json', 'w'))
cap = cv2.VideoCapture(V); n = 0; sheet = []
while n <= end:
    ok, im = cap.read()
    if not ok: break
    if n % 10 == 0:
        b = boxes.get(n)
        if b: cv2.rectangle(im, (b[0], b[1]), (b[0]+b[2], b[1]+b[3]), (0,0,255), 4)
        cv2.putText(im, str(n), (10, 60), 0, 2, (0,255,255), 4)
        sheet.append(cv2.resize(im, (180, 320)))
    n += 1
import numpy as np
rows = [np.hstack(sheet[i:i+10] + [np.zeros((320,180,3),np.uint8)]*(10-len(sheet[i:i+10]))) for i in range(0, len(sheet), 10)]
cv2.imwrite('trk.jpg', np.vstack(rows))
