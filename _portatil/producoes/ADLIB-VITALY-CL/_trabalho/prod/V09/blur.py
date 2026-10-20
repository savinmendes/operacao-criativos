import cv2, json, subprocess, numpy as np
V = "../../../VIDEOS/09 - Vitaly - 1855505272004884.mp4"
B = {int(k): v for k, v in json.load(open('boxes.json')).items() if v}
for n in range(336, 348):
    a = np.array([620, 250, 100, 300]); b = np.array([395, 385, 120, 190]); u = (n - 336) / 12
    B[n] = list((a * (1 - u) + b * u).astype(int))
END = 400  # 13.35 s
cap = cv2.VideoCapture(V); W, H = 720, 1280
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",
    "-i",V,"-map","0:v","-map","1:a","-t","13.35","-c:v","libx264","-crf","14","-pix_fmt","yuv420p",
    "-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709","-c:a","aac","-b:a","192k","-ar","48000","gancho.mp4"], stdin=subprocess.PIPE)
n = 0
while n <= END:
    ok, im = cap.read()
    if not ok: break
    if n in B:
        x, y, w, h = B[n]; mx, my = int(w * .22), int(h * .22)
        x0, y0, x1, y1 = max(0, x - mx), max(0, y - my), min(W, x + w + mx), min(H, y + h + my)
        bl = cv2.GaussianBlur(cv2.GaussianBlur(im, (0, 0), 18), (0, 0), 10)
        m = np.zeros((H, W), np.float32); cv2.rectangle(m, (x0, y0), (x1, y1), 1, -1)
        m = cv2.GaussianBlur(m, (0, 0), 8)[..., None]
        im = (im * (1 - m) + bl * m).astype(np.uint8)
    ff.stdin.write(im.tobytes()); n += 1
ff.stdin.close(); ff.wait(); print("ok", n)
