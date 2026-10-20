import sys, json, subprocess, numpy as np
from rapidocr_onnxruntime import RapidOCR
v, out = sys.argv[1], sys.argv[2]
y0, y1 = 1300, 1620
W, H = 1080, y1-y0
cmd = ['ffmpeg','-v','error','-i',v,'-vf',f'fps=5,crop={W}:{H}:0:{y0}','-f','rawvideo','-pix_fmt','bgr24','-']
p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
ocr = RapidOCR()
res = []; i = 0
while True:
    b = p.stdout.read(W*H*3)
    if len(b) < W*H*3: break
    f = np.frombuffer(b, np.uint8).reshape(H, W, 3)
    r, _ = ocr(f)
    items = [] if not r else [(round(float(np.mean([q[0] for q in x[0]])),0), round(float(np.mean([q[1] for q in x[0]]))+y0,0), x[1], round(float(x[2]),2), [min(q[0] for q in x[0]), max(q[0] for q in x[0])]) for x in r]
    res.append({'t': round(i/5, 2), 'items': items})
    i += 1
json.dump(res, open(out,'w',encoding='utf-8'), ensure_ascii=False, indent=0)
print('frames', i)
