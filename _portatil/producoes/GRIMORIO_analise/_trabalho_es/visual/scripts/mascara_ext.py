# Extensão encadeada da linha da legenda: a partir das caixas aceitas (LOG), cresce para os lados (até 160 px) só com
# componentes de glifo branco na altura da linha e a <= 28 px do texto já aceito (palavra que o OCR cortou nas pontas).
import subprocess, numpy as np, cv2, json, sys
sys.argv = ["x", "_", "0", "0"]
src = open("mascara.py", encoding="utf-8").read(); exec(src[:src.index("e = RapidOCR")])
K21 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
def glif(f, x0, y0, x1, y1):
    r = f[y0:y1, x0:x1]; g = cv2.cvtColor(r, cv2.COLOR_BGR2GRAY)
    mn = r.min(2).astype(int); mx = r.max(2).astype(int)
    return ((mn >= 205) & ((mx - mn) <= 45) & (cv2.morphologyEx(g, cv2.MORPH_TOPHAT, K21) > 25)).astype(np.uint8)
LOG = {}
for k in (0, 930, 1860, 2790, 3720): LOG.update(json.load(open(f"../_tmp/mask_{k}.json")))
MK = np.load("../_tmp/mask_all.npy")
V = r"C:\Users\PICHAU\Downloads\GRIMORIO V2.mp4"
p = subprocess.Popen(["ffmpeg","-v","error","-i",V,"-vf","scale=in_color_matrix=bt709:in_range=full,format=bgr24","-f","rawvideo","-"],stdout=subprocess.PIPE)
T = 720*1280*3; mud = []
for i in range(4645):
    f = np.frombuffer(p.stdout.read(T), np.uint8).reshape(1280,720,3)
    bx = LOG.get(str(i), [])
    if not bx: continue
    add = np.zeros((1280,720), np.uint8)
    for L, Y0, R, Y1 in bx:
        cyl = (Y1 - Y0) / 2
        for lado in (-1, 1):
            xa, xb = (max(0, L - 160), L) if lado < 0 else (R, min(720, R + 160))
            if xb - xa < 8: continue
            m = glif(f, xa, Y0, xb, Y1); n, lab, st, _ = cv2.connectedComponentsWithStats(m)
            comps = [j for j in range(1, n) if 8 <= st[j,3] <= 55 and st[j,4] >= 10 and abs(st[j,1] + st[j,3]/2 - cyl) < 12]
            borda = L if lado < 0 else R; ok = True
            comps.sort(key=lambda j: -(st[j,0] + st[j,2]) if lado < 0 else st[j,0])
            for j in comps:
                x0c = xa + st[j,0]; x1c = x0c + st[j,2]
                gap = (borda - x1c) if lado < 0 else (x0c - borda)
                if gap > 28: break
                add[Y0:Y1, xa:xb][lab == j] = 1
                borda = min(borda, x0c) if lado < 0 else max(borda, x1c)
    if add.sum() > 25:
        d = cv2.dilate(add, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11))); dn = np.zeros_like(d); dn[3:] = d[:-3]
        add = cv2.dilate(d | dn, np.ones((5,5),np.uint8))
        old = np.unpackbits(MK[i])[:1280*720].reshape(1280,720)
        if (add & ~old.astype(bool)).sum() > 40:
            MK[i] = np.packbits(old | add); mud.append(i)
print("quadros com extensão:", len(mud))
np.save("../_tmp/mask_all2.npy", MK); np.save("../_tmp/ext_idx.npy", np.array(mud))
