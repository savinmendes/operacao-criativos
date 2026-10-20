import cv2, numpy as np, sys, subprocess, wave
seg, cx, cy = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
cap = cv2.VideoCapture(seg + ".mp4"); fr = []
while True:
    ok, im = cap.read()
    if not ok: break
    fr.append(im)
w = wave.open(seg + "_voz.wav"); sr = w.getframerate(); ch = w.getnchannels()
a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, ch).mean(1) / 32768
tiles = []
for i in range(0, len(fr), 2):
    s = a[int(i/30*sr):int((i+1)/30*sr)]; db = 20*np.log10(np.sqrt((s**2).mean())+1e-9) if len(s) else -90
    c = fr[i][cy-150:cy+150, cx-200:cx+200].copy()
    c = cv2.resize(c, (240, 180))
    col = (0,255,0) if db > -35 else (0,0,255)
    cv2.rectangle(c, (0,170), (int(max(0,(db+60))*4), 180), col, -1)
    cv2.putText(c, f"{i/30:.2f}", (3,16), 0, 0.5, (0,255,255), 1)
    tiles.append(c)
cols = 10
while len(tiles) % cols: tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite(f"bocas_{seg}.jpg", np.vstack([np.hstack(tiles[i:i+cols]) for i in range(0,len(tiles),cols)]), [cv2.IMWRITE_JPEG_QUALITY, 88])
