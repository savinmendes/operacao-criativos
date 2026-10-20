import numpy as np,cv2,sys
a=np.load('fr.npy')
exec(open('rep.py').read().split('def feat')[0].split('b=[0]')[0])
b=[0]+cuts+[len(a)];shots=[(b[i],b[i+1]) for i in range(len(b)-1)]
tiles=[]
for i,(s,e) in enumerate(shots):
    row=[]
    for f in (s,(s+e)//2,e-1):
        im=cv2.cvtColor(a[f],cv2.COLOR_RGB2BGR).copy()
        cv2.putText(im,f'{i} {f/30:.2f}',(2,12),cv2.FONT_HERSHEY_SIMPLEX,0.38,(0,255,255),1)
        row.append(im)
    tiles.append(np.hstack(row))
# 4 shots per row
rows=[np.hstack(tiles[k:k+4]+[np.zeros_like(tiles[0])]*(4-len(tiles[k:k+4]))) for k in range(0,len(tiles),4)]
for p in range(0,len(rows),6):
    cv2.imwrite(f'shots_{p//6}.jpg',np.vstack(rows[p:p+6]),[cv2.IMWRITE_JPEG_QUALITY,85])
print(len(rows))
