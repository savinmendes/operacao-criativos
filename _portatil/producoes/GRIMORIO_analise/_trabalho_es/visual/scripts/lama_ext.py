import subprocess, numpy as np, cv2, warnings; warnings.filterwarnings("ignore")
from PIL import Image
from simple_lama_inpainting import SimpleLama
V = r"C:\Users\PICHAU\Downloads\GRIMORIO V2.mp4"
IDX = np.load("../_tmp/ext_idx.npy"); ALL = np.load("../_tmp/mask_all2.npy"); MKS = ALL[IDX]; lama = SimpleLama()
p = subprocess.Popen(["ffmpeg","-v","error","-i",V,"-vf","scale=in_color_matrix=bt709:in_range=full:flags=accurate_rnd+full_chroma_int,format=bgr24","-f","rawvideo","-"],stdout=subprocess.PIPE)
T = 720*1280*3; S = set(IDX.tolist()); pos = {k: j for j, k in enumerate(IDX.tolist())}; out = []
for i in range(int(IDX.max()) + 1):
    b = p.stdout.read(T)
    if i not in S: continue
    f = np.frombuffer(b, np.uint8).reshape(1280,720,3).copy()
    m = np.unpackbits(MKS[pos[i]])[:1280*720].reshape(1280,720)
    ys = np.where(m.any(1))[0]; a0, a1 = max(0, ys.min()-120), min(1280, ys.max()+120)
    r = lama(Image.fromarray(cv2.cvtColor(f[a0:a1], cv2.COLOR_BGR2RGB)), Image.fromarray(m[a0:a1]*255))
    r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:a1-a0,:720].astype(np.float32)
    al = np.maximum(cv2.GaussianBlur(m.astype(np.float32),(9,9),0), m)[a0:a1,...,None]
    f[a0:a1] = np.clip(r*al + f[a0:a1]*(1-al), 0, 255).astype(np.uint8); out.append(f)
p.kill(); np.save("../_tmp/ext_frames.npy", np.array(out)); print("ok", len(out))
