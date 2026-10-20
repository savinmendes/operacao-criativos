import sys, cv2, numpy as np, subprocess
from PIL import Image, ImageDraw, ImageFont
src, out = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src); fps = cap.get(5); fr = []
while True:
    ok, f = cap.read()
    if not ok: break
    fr.append(f)
H, W = fr[0].shape[:2]
TX0, TY0, TX1, TY1 = 222, 555, 312, 685   # template do corpo do frasco (quadro 0)
EX0, EY0, EX1, EY1 = 236, 638, 299, 677   # area do texto (quadro 0)
tpl = cv2.cvtColor(fr[0][TY0:TY1, TX0:TX1], cv2.COLOR_BGR2GRAY)
pos = []; prev = (TX0, TY0)
for f in fr:
    g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    sx0, sy0 = max(0, prev[0]-50), max(0, prev[1]-50)
    win = g[sy0:sy0+(TY1-TY0)+100, sx0:sx0+(TX1-TX0)+100]
    r = cv2.matchTemplate(win, tpl, cv2.TM_CCOEFF_NORMED); _, mv, _, ml = cv2.minMaxLoc(r)
    prev = (sx0+ml[0], sy0+ml[1]); pos.append((prev[0]-TX0, prev[1]-TY0, mv))
P = np.array(pos, np.float32)
k = 5; Ps = P.copy()
for i in range(len(P)):
    a, b = max(0, i-k), min(len(P), i+k+1); Ps[i, :2] = np.median(P[a:b, :2], 0)
print("score min", P[:,2].min(), "desloc max", np.abs(Ps[:,:2]).max(0))
def texto(img, txt, cx, cy, px, col):
    fnt = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", px)
    im = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)); d = ImageDraw.Draw(im)
    b = d.textbbox((0,0), txt, font=fnt); w = b[2]-b[0]; h = b[3]-b[1]
    d.text((cx - w/2 - b[0], cy - h/2 - b[1]), txt, font=fnt, fill=col)
    return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
p = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r",f"{fps}","-i","-",
    "-i", src, "-map","0:v","-map","1:a?","-c:a","copy","-c:v","libx264","-crf","14","-pix_fmt","yuv420p",*COR,out], stdin=subprocess.PIPE)
prevs = []
for i, f in enumerate(fr):
    dx, dy = int(round(Ps[i,0])), int(round(Ps[i,1]))
    x0, y0, x1, y1 = EX0+dx, EY0+dy, EX1+dx, EY1+dy
    reg = f[y0-6:y1+6, x0-6:x1+6].copy()
    m = np.zeros(reg.shape[:2], np.uint8); m[6:-6, 6:-6] = 255
    fill = cv2.inpaint(reg, m, 5, cv2.INPAINT_TELEA)
    # escurece o miolo para o tom do frasco (borda media)
    sub = fill.copy()
    sub = texto(sub, "club de nuit", sub.shape[1]/2, 6+12, 10, (185,185,190))
    sub = texto(sub, "intense man", sub.shape[1]/2, 6+22, 7, (155,155,160))
    g = f.copy(); al = cv2.GaussianBlur(m.astype(np.float32)/255, (0,0), 1.2)[...,None]
    g[y0-6:y1+6, x0-6:x1+6] = (sub*al + reg*(1-al)).astype(np.uint8)
    if i in (0, 60, 120): prevs.append(cv2.resize(g[y0-90:y1+20, x0-50:x1+50], None, fx=3, fy=3))
    p.stdin.write(g.tobytes())
p.stdin.close(); p.wait()
cv2.imwrite("q/frasco_prev.png", np.hstack([cv2.resize(x,(prevs[0].shape[1],prevs[0].shape[0])) for x in prevs]))
