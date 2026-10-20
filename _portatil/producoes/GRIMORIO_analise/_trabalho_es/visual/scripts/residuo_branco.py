# Resto de letra na BASE: pixels branco-puros (min>=212, spread<=20) em componentes de glifo na linha da legenda.
import subprocess, numpy as np, cv2, json
LOG = {}
for k in (0, 930, 1860, 2790, 3720): LOG.update(json.load(open(f"../_tmp/mask_{k}.json")))
ALL = np.load("../_tmp/mask_all2.npy")
p = subprocess.Popen(["ffmpeg","-v","error","-i","../base_sem_legenda.mp4","-vf","scale=in_color_matrix=bt709:in_range=tv,format=bgr24","-f","rawvideo","-"],stdout=subprocess.PIPE)
T = 720*1280*3; idx = []; mks = []
for i in range(4645):
    f = np.frombuffer(p.stdout.read(T), np.uint8).reshape(1280,720,3)
    bx = LOG.get(str(i), []) or LOG.get(str(i-1), []) or LOG.get(str(i+1), [])
    if not bx or i < 657 or 1332 <= i <= 1810 or 1844 <= i <= 2032 or 2991 <= i <= 3147 or i >= 4554: continue
    add = np.zeros((1280,720), np.uint8)
    old = np.unpackbits(ALL[i])[:1280*720].reshape(1280,720)
    perto = cv2.dilate(old, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(17,17)))
    for L, Y0, R, Y1 in bx:
        xa, xb = max(0, L-170), min(720, R+170)
        r = f[Y0:Y1, xa:xb].astype(int); mn = r.min(2); sp = r.max(2) - mn
        m = ((mn >= 212) & (sp <= 20)).astype(np.uint8)
        n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(m, np.ones((3,3),np.uint8)))
        for j in range(1, n):
            if st[j,4] >= 70 and 14 <= st[j,3] <= 50 and abs(st[j,1] + st[j,3]/2 - (Y1-Y0)/2) < 9 and (perto[Y0:Y1, xa:xb][lab == j]).any(): add[Y0:Y1, xa:xb][lab == j] = 1
    if add.sum() > 30:
        d = cv2.dilate(add, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(13,13))); dn = np.zeros_like(d); dn[3:] = d[:-3]
        add = cv2.dilate(d|dn, np.ones((5,5),np.uint8))
        idx.append(i); mks.append(np.packbits(old | add))
print("quadros com resto branco:", len(idx), idx[:60])
np.save("../_tmp/rb_idx.npy", np.array(idx)); np.save("../_tmp/rb_mk.npy", np.array(mks))
