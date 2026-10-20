import cv2, numpy as np, sys, json, subprocess; sys.path.insert(0, "scripts")
import limpar
from limpar import preparar, inpaint
from simple_lama_inpainting import SimpleLama
lama = SimpleLama(); D = json.load(open("ocr_boxes.json"))
res = []
for t in [float(x) for x in sys.argv[1:]]:
    q = int(round(t * 30)); k = sorted(int(x) for x in D); a = max(x for x in k if x <= q); b = min(x for x in k if x > q)
    bx = D[str(a)] + D[str(b)]
    raw = subprocess.run(["ffmpeg","-v","error","-ss",f"{q/30:.4f}","-i",r"C:\Users\PICHAU\Downloads\Lead 2.mp4","-frames:v","1","-vf","scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24","-f","rawvideo","-"],capture_output=True).stdout
    f = np.frombuffer(raw, np.uint8).reshape(960, 720, 3).copy()
    u, mk, modos = preparar(f, bx); n0 = limpar.corrigir_fill.quadros; o = inpaint(lama, u, mk)
    print(t, bx, modos, "telea" if limpar.corrigir_fill.quadros > n0 else "lama")
    v = u.copy(); v[mk > 0] = (v[mk > 0] * 0.4 + np.array([255, 0, 255]) * 0.6).astype(np.uint8)
    res.append(np.vstack([f[740:900], v[740:900], o[740:900]]))
cv2.imwrite("rev/rep.jpg", np.hstack(res))
