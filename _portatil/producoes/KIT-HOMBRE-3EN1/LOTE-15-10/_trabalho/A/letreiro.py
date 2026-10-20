# Troca ESSENZALUX -> ARABESPERFUME no letreiro (camera parada). Uso: _vg python letreiro.py in.mp4 out.mp4 [prev.png]
import sys, cv2, numpy as np, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from simple_lama_inpainting import SimpleLama
src, out = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src); fps = cap.get(5); fr = []
while True:
    ok, f = cap.read()
    if not ok: break
    fr.append(f)
H, W = fr[0].shape[:2]
med = np.median(np.stack(fr[::4]), axis=0).astype(np.uint8)
X0, Y0, X1, Y1 = 150, 198, 520, 282          # caixa do texto antigo (com brilho)
mask = np.zeros((H, W), np.uint8); mask[Y0:Y1, X0:X1] = 255
lama = SimpleLama()
r = lama(Image.fromarray(cv2.cvtColor(med, cv2.COLOR_BGR2RGB)), Image.fromarray(mask))
clean = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:H, :W]
# texto novo
txt = "ARABESPERFUME"; cx, cy = 334, 238; alvo_w = 352
fnt = None
for s in range(30, 80):
    f_ = ImageFont.truetype("C:/Windows/Fonts/pala.ttf", s)
    b = f_.getbbox(txt)
    if b[2] - b[0] > alvo_w: break
    fnt = f_
b = fnt.getbbox(txt); tw, th = b[2] - b[0], b[3] - b[1]
lay = Image.new("L", (W, H), 0); d = ImageDraw.Draw(lay)
d.text((cx - tw / 2 - b[0], cy - th / 2 - b[1]), txt, font=fnt, fill=255)
m = np.array(lay).astype(np.float32) / 255
glow = cv2.GaussianBlur(m, (0, 0), 9) * 1.3 + cv2.GaussianBlur(m, (0, 0), 3) * 0.6
base = clean.astype(np.float32)
glow_col = np.array([60, 150, 230], np.float32)      # BGR laranja-dourado
fill_col = np.array([175, 222, 250], np.float32)     # creme
img = base + glow[..., None] * glow_col * 0.55
img = img * (1 - m[..., None]) + fill_col * m[..., None]
img = np.clip(img, 0, 255)
delta = img - med.astype(np.float32)
fe = np.zeros((H, W), np.float32); fe[Y0:Y1, X0:X1] = 1; fe = cv2.GaussianBlur(fe, (0, 0), 4)[..., None]
delta *= fe
if len(sys.argv) > 3:
    cv2.imwrite(sys.argv[3], np.clip(fr[24].astype(np.float32) + delta, 0, 255).astype(np.uint8))
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
p = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r",f"{fps}","-i","-",
    "-i", src, "-map","0:v","-map","1:a?","-c:a","copy","-c:v","libx264","-crf","14","-pix_fmt","yuv420p",*COR,"-shortest",out], stdin=subprocess.PIPE)
for f in fr:
    p.stdin.write(np.clip(f.astype(np.float32) + delta, 0, 255).astype(np.uint8).tobytes())
p.stdin.close(); p.wait(); print("ok", len(fr), fnt.size)
