import cv2,numpy as np,sys,ast,subprocess,os
n=sys.argv[1]
hits=[ast.literal_eval(l.strip()) for l in open(f'pontos_{n}.txt') if l.startswith('   ')]
# dedupe: keep first of runs within 0.35s and 15px
keep=[]
for h in hits:
    if any(abs(h[0]-k[0])<=0.35 and abs(h[1]-k[1])<20 and abs(h[2]-k[2])<20 for k in keep[-6:]): continue
    keep.append(h)
tiles=[]
for t,x,y,a in keep:
    subprocess.run(['ffmpeg','-v','error','-ss',f'{t:.2f}','-i',rf'C:\Users\PICHAU\Downloads\PERFUMES-PL\PARA-SUBIR\{n}.mp4','-frames:v','1','-y','tmpp.png'])
    im=cv2.imread('tmpp.png'); x0=max(0,min(720-160,x-80)); y0=max(0,min(1280-120,y-60))
    c=cv2.resize(im[y0:y0+120,x0:x0+160],None,fx=2,fy=2)
    cv2.rectangle(c,((x-x0-6)*2,(y-y0-6)*2),((x-x0+20)*2,(y-y0+20)*2),(0,0,255),1)
    cv2.putText(c,f'{t:.1f}s',(4,22),0,0.7,(0,0,255),2); tiles.append(c)
while len(tiles)%4: tiles.append(np.zeros_like(tiles[0]))
rows=[np.hstack(tiles[i:i+4]) for i in range(0,len(tiles),4)]
cv2.imwrite(f'ev/{n}_pontos.jpg',np.vstack(rows)); print(n,len(keep))
