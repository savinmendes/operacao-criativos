# acha quadros com resto de legenda na base (OCR det) nas janelas suspeitas e monta máscara nova (glifo do ORIGINAL na caixa)
import subprocess, numpy as np, cv2, json, sys
from rapidocr_onnxruntime import RapidOCR
sys.argv = ["x", "_", "0", "0"]
src = open("mascara.py", encoding="utf-8").read(); exec(src[:src.index("p = subprocess.Popen")])
JAN = [(2205, 2265), (2925, 2955), (3910, 3940), (4485, 4520)]
def ler(p, rng, a, b):
    r = subprocess.Popen(["ffmpeg","-v","error","-i",p,"-vf",f"select=between(n\,{a}\,{b}),scale=in_color_matrix=bt709:in_range={rng},format=bgr24","-fps_mode","passthrough","-f","rawvideo","-"],stdout=subprocess.PIPE)
    T = 720*1280*3; out = []
    while True:
        x = r.stdout.read(T)
        if len(x) < T: break
        out.append(np.frombuffer(x, np.uint8).reshape(1280,720,3))
    return out
MK = np.load("../_tmp/mask_all.npy"); novos = {}
for a, b in JAN:
    B = ler("../base_sem_legenda.mp4", "tv", a, b); O = ler(r"C:\Users\PICHAU\Downloads\GRIMORIO V2.mp4", "full", a, b)
    for k, (fb, fo) in enumerate(zip(B, O)):
        i = a + k
        r, _ = e(fb, use_cls=False, use_rec=False); add = np.zeros((1280,720), np.uint8)
        for q in (r or []):
            q = np.array(q); x0, y0, x1, y1 = q[:,0].min(), q[:,1].min(), q[:,0].max(), q[:,1].max()
            if not (720 <= (y0+y1)/2 <= 885 and 26 <= y1-y0 <= 90 and 60 <= (x0+x1)/2 <= 660): continue
            X0, Y0, X1, Y1 = int(max(0,x0-10)), int(max(0,y0-8)), int(min(720,x1+10)), int(min(1280,y1+8))
            m, _ = glifos(fo, X0, Y0, X1, Y1, False)
            if m.sum() > 40: add[Y0:Y1, X0:X1] |= m
        if add.any():
            d = cv2.dilate(add, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11))); dn = np.zeros_like(d); dn[3:] = d[:-3]
            add = cv2.dilate(d|dn, np.ones((5,5),np.uint8))
            old = np.unpackbits(MK[i])[:1280*720].reshape(1280,720)
            novos[i] = np.packbits(old | add)
print("quadros com resto:", sorted(novos))
np.save("../_tmp/residuos_idx.npy", np.array(sorted(novos))); np.save("../_tmp/residuos_mk.npy", np.array([novos[k] for k in sorted(novos)]))
