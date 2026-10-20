import subprocess, numpy as np, cv2, sys
W, Y0, Y1 = 720, 600, 910; Hh = Y1 - Y0
def conta(p, out):
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-i", p, "-vf", f"crop=720:{Hh}:0:{Y0},format=gray", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    res = []; k = np.ones((5, 5), np.uint8)
    while True:
        b = pr.stdout.read(W * Hh)
        if len(b) < W * Hh: break
        g = np.frombuffer(b, np.uint8).reshape(Hh, W)
        wh = (g > 210).astype(np.uint8); dk = cv2.dilate((g < 70).astype(np.uint8), k)
        res.append(int((wh & dk).sum()))
    np.save(out, np.array(res, np.int32)); print(out, len(res), flush=True)
conta(sys.argv[1], sys.argv[2])
