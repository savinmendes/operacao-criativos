import cv2, json, re
from rapidocr_onnxruntime import RapidOCR
o = RapidOCR(); cap = cv2.VideoCapture("../../SB-ES_BREVIARIO-COLAR_FICTICIO.mp4"); q = 0; R = []
while True:
    ok, f = cap.read()
    if not ok: break
    if q % 15 == 0:
        r, _ = o(cv2.resize(f, (540, 960)))
        txt = [x[1] for x in (r or []) if x[2] > 0.6]
        R.append([round(q/30, 1), txt])
    q += 1
json.dump(R, open("rev/ocr.json", "w", encoding="utf-8"), ensure_ascii=False)
alvo = re.compile(r"sagrad|verso|grim|R\$|\$|reais|bio|pix|link|clp|precio", re.I)
for t, tx in R:
    hit = [x for x in tx if alvo.search(x)]
    if hit: print(t, hit)
print("quadros", len(R))
