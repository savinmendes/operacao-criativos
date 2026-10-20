# LaMa com máscara RETANGULAR (caixa da legenda inteira) nos quadros 4554-4644 (luz dourada: texto branco sobre fundo claro)
import subprocess, numpy as np, cv2, warnings; warnings.filterwarnings("ignore")
from PIL import Image
from simple_lama_inpainting import SimpleLama
V = r"C:\Users\PICHAU\Downloads\GRIMORIO V2.mp4"; A, B = 4554, 4645
MK = np.load("../_tmp/mask_all.npy"); lama = SimpleLama()
p = subprocess.Popen(["ffmpeg","-v","error","-i",V,"-vf",f"select=gte(n\,{A}),scale=in_color_matrix=bt709:in_range=full:flags=accurate_rnd+full_chroma_int,format=bgr24","-fps_mode","passthrough","-f","rawvideo","-"],stdout=subprocess.PIPE)
out = []; T = 720*1280*3
# caixa única que cobre a legenda em todo o trecho (união), com folga
U = np.zeros((1280,720),bool)
for i in range(A,B): U |= np.unpackbits(MK[i])[:1280*720].reshape(1280,720) > 0
ys, xs = np.where(U); print("uniao", xs.min(), ys.min(), xs.max(), ys.max())
for i in range(A,B):
    f = np.frombuffer(p.stdout.read(T),np.uint8).reshape(1280,720,3).copy()
    m = np.unpackbits(MK[i])[:1280*720].reshape(1280,720)
    if m.any():
        yy, xx = np.where(m); R = np.zeros_like(m); R[max(0,yy.min()-8):yy.max()+8, max(0,xx.min()-12):min(720,xx.max()+12)] = 1
        a0, a1 = max(0, yy.min()-140), min(1280, yy.max()+140)
        r = lama(Image.fromarray(cv2.cvtColor(f[a0:a1],cv2.COLOR_BGR2RGB)), Image.fromarray(R[a0:a1]*255))
        r = cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:a1-a0,:720].astype(np.float32)
        al = cv2.GaussianBlur(R.astype(np.float32),(15,15),0)[a0:a1,...,None]; al = np.maximum(al, R[a0:a1,...,None])
        f[a0:a1] = np.clip(r*al + f[a0:a1]*(1-al),0,255).astype(np.uint8)
    out.append(f)
np.save("../_tmp/fim_frames.npy", np.array(out)); print("ok", len(out))
