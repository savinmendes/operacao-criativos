import cv2, numpy as np, sys, json, subprocess; sys.path.insert(0, "scripts")
from limpar import preparar
from PIL import Image
from simple_lama_inpainting import SimpleLama
lama = SimpleLama(); D = json.load(open("ocr_boxes.json"))
def L(img, m, a0, a1):
    r = lama(Image.fromarray(cv2.cvtColor(img[a0:a1], cv2.COLOR_BGR2RGB)), Image.fromarray(m[a0:a1] * 255))
    r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:a1 - a0, :720]; o = img.copy(); o[a0:a1] = np.where(m[a0:a1, :, None] > 0, r, img[a0:a1]); return o
cols = []
for t in [310, 420, 470, 600]:
    q = int(round(t * 30)); k = sorted(int(x) for x in D); a = max(x for x in k if x <= q)
    raw = subprocess.run(["ffmpeg","-v","error","-ss",f"{q/30:.4f}","-i",r"C:\Users\PICHAU\Downloads\Lead 2.mp4","-frames:v","1","-vf","scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24","-f","rawvideo","-"],capture_output=True).stdout
    f = np.frombuffer(raw, np.uint8).reshape(960, 720, 3).copy(); u, mk, _ = preparar(f, D[str(a)])
    ys = np.where(mk.any(1))[0]; y0, y1 = ys.min(), ys.max()
    v = []
    v.append(L(u, mk, max(0, y0 - 90), min(960, y1 + 60)))                     # atual
    v.append(L(u, mk, max(0, y0 - 30), min(960, y1 + 30)))                     # contexto curto
    m2 = cv2.dilate(mk, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))); v.append(L(u, m2, max(0, y0 - 90), min(960, y1 + 60)))
    # escala 0.5
    us = cv2.resize(u, (360, 480), interpolation=cv2.INTER_AREA); ms = (cv2.resize(mk, (360, 480), interpolation=cv2.INTER_AREA) > 0).astype(np.uint8)
    r = lama(Image.fromarray(cv2.cvtColor(us, cv2.COLOR_BGR2RGB)), Image.fromarray(ms * 255)); r = cv2.resize(cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:480, :360], (720, 960), interpolation=cv2.INTER_CUBIC)
    v.append(np.where(mk[..., None] > 0, r, u))
    cols.append(np.vstack([x[760:900] for x in v]))
cv2.imwrite("rev/var.jpg", np.hstack(cols))
