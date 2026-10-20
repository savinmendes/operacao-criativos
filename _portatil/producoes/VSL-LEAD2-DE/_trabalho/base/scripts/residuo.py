import subprocess, numpy as np, json
from rapidocr_onnxruntime import RapidOCR
o = RapidOCR(); H = 270; Y0 = 640; res = []
p = subprocess.Popen(["ffmpeg","-v","error","-i","base_limpa.mp4","-vf",f"fps=1/4,crop=720:{H}:0:{Y0},format=bgr24","-f","rawvideo","-"],stdout=subprocess.PIPE)
k = 0
while True:
    b = p.stdout.read(720*H*3)
    if len(b) < 720*H*3: break
    f = np.frombuffer(b, np.uint8).reshape(H, 720, 3)
    r, _ = o(f, use_cls=False)
    for bx, txt, c in (r or []):
        if c > 0.6 and len(txt.strip()) >= 3: res.append([k*4, txt, round(float(c), 2)])
    k += 1
json.dump(res, open("rev/residuo_ocr.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("amostras", k, "com texto legivel:", len(res)); [print(x) for x in res[:40]]
