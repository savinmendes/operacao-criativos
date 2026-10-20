# uso: python emendas.py video.mp4 saida_prefixo  -> folhas de 1 em 1 quadro (±3) em volta de cada corte (scdet), 8 cortes por folha
import sys, subprocess, re, cv2, numpy as np
v, pre = sys.argv[1], sys.argv[2]
o = subprocess.run(["ffmpeg","-threads","4","-i",v,"-vf","scdet=threshold=8","-f","null","-"],capture_output=True,text=True,encoding="utf-8",errors="ignore").stderr
ts = [float(x) for x in re.findall(r"lavfi\.scd\.time: ([\d.]+)", o)]
cap = cv2.VideoCapture(v); fps = cap.get(5); fr = []
while True:
    ok, f = cap.read()
    if not ok: break
    fr.append(cv2.resize(f, (108, 192)))
linhas = []
for t in ts:
    q = int(round(t*fps)); cel = []
    for k in range(q-3, q+4):
        im = fr[k].copy() if 0 <= k < len(fr) else np.zeros_like(fr[0])
        cv2.putText(im, f"{k/fps:.2f}", (2, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0,255,255) if k == q else (255,255,255), 1)
        cel.append(im)
    linhas.append(np.hstack(cel))
for i in range(0, len(linhas), 8):
    cv2.imwrite(f"{pre}_{i//8+1}.jpg", np.vstack(linhas[i:i+8]))
print("cortes", [round(t,2) for t in ts])
