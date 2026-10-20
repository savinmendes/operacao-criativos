import numpy as np,cv2,json
from fr import frames
from sheet import lab,grid
V='../../SB-FR-ADS-13.13F-REZA-MUJER.mp4'; O=r'C:\Users\PICHAU\Downloads\ADS 13\ADS 13.13F REZA-MUJER.mp4'
F=[f.copy() for f in frames(V)]; print(len(F))
np.save('F_pip.npy',np.stack([f[640:1280] for f in F[:170]]))
Ofr=[]
for i,f in enumerate(frames(O)):
    if i<180: Ofr.append(f.copy())
    else: break
# PiP face crops 2x, FR every 6 frames 0..165, orig same idx
def pip(f): return cv2.resize(f[700:1050,380:680],(600,700),interpolation=cv2.INTER_CUBIC)
idx=list(range(0,166,6))
cv2.imwrite('pip_fr_A.jpg',grid([lab(pip(F[i]),f'FR {i/30:.2f}') for i in idx[:14]],7),[cv2.IMWRITE_JPEG_QUALITY,90])
cv2.imwrite('pip_fr_B.jpg',grid([lab(pip(F[i]),f'FR {i/30:.2f}') for i in idx[14:]],7),[cv2.IMWRITE_JPEG_QUALITY,90])
oi=list(range(0,175,12))
cv2.imwrite('pip_orig.jpg',grid([lab(pip(Ofr[i]),f'ES {i/30:.2f}') for i in oi],7),[cv2.IMWRITE_JPEG_QUALITY,90])
# subtitle band PiP: y1050-1260 every 0.25s
def band(f,y0,y1): return f[y0:y1]
ims=[lab(band(F[i],1060,1250),f'{i/30:.2f}') for i in range(0,166,8)]
cv2.imwrite('band_pip.jpg',grid(ims,3),[cv2.IMWRITE_JPEG_QUALITY,90])
ims=[lab(band(F[i],660,920),f'{i/30:.2f}') for i in range(166,835,15)]
cv2.imwrite('band_mid_1.jpg',grid(ims[:24],3),[cv2.IMWRITE_JPEG_QUALITY,88])
cv2.imwrite('band_mid_2.jpg',grid(ims[24:],3),[cv2.IMWRITE_JPEG_QUALITY,88])
# gaps between subtitle blocks
bl=json.load(open('../blocos_fr.json',encoding='utf-8'))
gaps=[(a[1],b[0]) for a,b in zip(bl,bl[1:]) if b[0]-a[1]>0.03]
print(gaps)
ims=[]
for a,b in gaps:
    i=int(round((a+b)/2*30)); y0,y1=(1040,1270) if i<166 else (620,940)
    ims.append(lab(cv2.resize(F[i][y0:y1],(720,int((y1-y0)))),f'gap {i/30:.2f}'))
cv2.imwrite('gaps.jpg',grid([cv2.resize(x,(720,280)) for x in ims],2),[cv2.IMWRITE_JPEG_QUALITY,90])
# cut frames: around each cut, 2 before/2 after full frames small
cuts=[166,256,355,466,567,659]
ims=[]
for c in cuts:
    for i in range(c-2,c+3): ims.append(lab(cv2.resize(F[i],(216,384)),f'{i} {i/30:.2f}'))
cv2.imwrite('cuts.jpg',grid(ims,5),[cv2.IMWRITE_JPEG_QUALITY,88])
# frame diffs
d=[float(np.abs(F[i+1].astype(int)-F[i]).mean()) for i in range(len(F)-1)]
json.dump(d,open('diffs.json','w'))
s=sorted(range(len(d)),key=lambda k:-d[k])[:15]; print([(k,round(d[k],1)) for k in sorted(s)])
