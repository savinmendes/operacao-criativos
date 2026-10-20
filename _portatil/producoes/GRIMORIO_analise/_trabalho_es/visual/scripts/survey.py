import sys, json, subprocess, numpy as np, cv2
from rapidocr_onnxruntime import RapidOCR
V = r"C:\Users\PICHAU\Downloads\GRIMORIO V2.mp4"
e = RapidOCR()
p = subprocess.Popen(["ffmpeg","-v","error","-i",V,"-vf","scale=in_color_matrix=bt709:in_range=full:flags=accurate_rnd+full_chroma_int,format=bgr24","-f","rawvideo","-"],stdout=subprocess.PIPE)
out = {}
i = 0; T = 720*1280*3
while True:
    b = p.stdout.read(T)
    if len(b) < T: break
    if i % 5 == 0:
        f = np.frombuffer(b, np.uint8).reshape(1280,720,3)
        r, _ = e(f, use_cls=False, use_rec=False)
        bx = []
        for q in (r or []):
            q = np.array(q); bx.append([int(q[:,0].min()), int(q[:,1].min()), int(q[:,0].max()), int(q[:,1].max())])
        out[i] = bx
        if i % 500 == 0: print(i, flush=True)
    i += 1
json.dump(out, open(sys.argv[1], "w"))
