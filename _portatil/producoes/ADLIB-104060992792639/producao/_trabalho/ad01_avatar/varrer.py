import sys, cv2, numpy as np
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
r = cl.Rastreador(alvo=(300, 250, 260, 300))
cap = cv2.VideoCapture('../../../UNICOS_HD/01.mp4')
out = []
i = 0
while True:
    ok, f = cap.read()
    if not ok or i > 3470: break
    if i % 3 == 0:
        p = r.pontos(f)
        if p is not None:
            larg = np.linalg.norm(p[234] - p[454])
            ab = cl._abertura(p)
            eye = (np.linalg.norm(p[159]-p[145]) + np.linalg.norm(p[386]-p[374])) / 2 / larg
            # frontalidade: nariz no meio das bochechas
            fr = abs((p[1][0]-p[234][0]) / (p[454][0]-p[234][0]) - 0.5)
            sharp = cv2.Laplacian(cv2.cvtColor(f[300:520, 330:520], cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()
            out.append((i, ab, eye, fr, sharp, larg))
    i += 1
np.save('varre.npy', np.array(out))
a = np.array(out)
print(len(a), 'ab pct', np.percentile(a[:,1], [5,50,95]), 'eye', np.percentile(a[:,2], [5,50,95]))
sc = a[:,1] / np.median(a[:,1]) - 0.5 * a[:,2] / np.median(a[:,2]) + 2 * a[:,3] - 0.2 * a[:,4] / np.median(a[:,4])
for k in np.argsort(sc)[:25]:
    print(f"q{int(a[k,0])} t={a[k,0]/30:.2f} ab={a[k,1]:.3f} eye={a[k,2]:.3f} fr={a[k,3]:.3f} sharp={a[k,4]:.0f}")
