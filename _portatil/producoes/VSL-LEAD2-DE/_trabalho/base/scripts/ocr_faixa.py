# Deteccao de texto (RapidOCR det) na faixa y 640..910 a cada PASSO quadros -> ocr_boxes.json {quadro: [[x0,y0,x1,y1],...]}
import sys, json, os, subprocess, time, numpy as np
from rapidocr_onnxruntime import RapidOCR
SRC = r"C:\Users\PICHAU\Downloads\Lead 2.mp4"; PASSO = int(sys.argv[1]) if len(sys.argv) > 1 else 6; Y0, H = 640, 270; N = 76899
OUT = "ocr_boxes.json"
D = json.load(open(OUT)) if os.path.exists(OUT) else {}
ini = max([int(k) for k in D] + [-PASSO]) + PASSO
o = RapidOCR()
ss = ini / 30.0
pr = subprocess.Popen(["ffmpeg","-v","error","-ss",f"{ss:.4f}","-i",SRC,"-vf",f"select=not(mod(n\\,{PASSO})),crop=720:{H}:0:{Y0},format=bgr24",
    "-fps_mode","passthrough","-f","rawvideo","-"], stdout=subprocess.PIPE)
t0 = time.time(); k = 0; T = 720*H*3; q = ini
while True:
    b = pr.stdout.read(T)
    if len(b) < T: break
    f = np.frombuffer(b, np.uint8).reshape(H, 720, 3)
    r, _ = o(f, use_det=True, use_cls=False, use_rec=False)
    bx = []
    for p in (r or []):
        p = np.array(p); bx.append([int(p[:,0].min()), int(p[:,1].min())+Y0, int(p[:,0].max()), int(p[:,1].max())+Y0])
    D[str(q)] = bx; q += PASSO; k += 1
    if k % 500 == 0:
        json.dump(D, open(OUT, "w")); el = time.time()-t0; rest = (N-q)/PASSO
        print(f"[{q}/{N}] {100*q//N}% falta ~{el/k*rest/60:.1f} min", flush=True)
json.dump(D, open(OUT, "w")); print("ok", q, round(time.time()-t0), "s")
