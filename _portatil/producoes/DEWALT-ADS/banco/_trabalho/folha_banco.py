# -*- coding: utf-8 -*-
"""folha_banco.jpg: 1 quadro (meio) por take com o nome. Com --qa: 3 quadros (inicio/meio/fim) por take, folhas qa_N.jpg."""
import sys, glob, os, cv2, numpy as np
B = r"C:\Users\PICHAU\Downloads\DEWALT-ADS\banco"
fs = sorted(glob.glob(os.path.join(B, "*.mp4"))); qa = "--qa" in sys.argv
TW, TH = (240, 427) if qa else (180, 320)
def q(v, pos):
    cap = cv2.VideoCapture(v); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, min(n - 1, int(pos * (n - 1)))))
    ok, f = cap.read(); return cv2.resize(f, (TW, TH), interpolation=cv2.INTER_AREA)
tiles = []
for v in fs:
    nm = os.path.basename(v)[:-4]
    for p in ((0.03, 0.5, 0.97) if qa else (0.5,)):
        f = q(v, p); cv2.rectangle(f, (0, TH - 22), (TW, TH), (0, 0, 0), -1)
        cv2.putText(f, nm, (4, TH - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1); tiles.append(f)
cols = 9 if qa else 8; per = cols * (4 if qa else 100)
for k in range(0, len(tiles), per):
    g = tiles[k:k + per]; rows = (len(g) + cols - 1) // cols; W = np.zeros((rows * TH, cols * TW, 3), np.uint8)
    for i, f in enumerate(g): W[(i // cols) * TH:(i // cols + 1) * TH, (i % cols) * TW:(i % cols + 1) * TW] = f
    cv2.imwrite(os.path.join(B, "_trabalho", f"qa_{k // per}.jpg") if qa else os.path.join(B, "folha_banco.jpg"), W, [cv2.IMWRITE_JPEG_QUALITY, 88])
print(len(fs), "takes")
