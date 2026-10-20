import cv2,numpy as np,subprocess,sys
n,x,y,w,h=sys.argv[1],*map(int,sys.argv[2:6])
p=subprocess.run(['ffmpeg','-v','error','-t','8.3','-i',rf'C:\Users\PICHAU\Downloads\PERFUMES-PL\PARA-SUBIR\{n}.mp4','-vf',f'fps=10,crop={w}:{h}:{x}:{y}','-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True).stdout
fr=np.frombuffer(p,np.uint8).reshape(-1,h,w,3)
tiles=[]
for i,f in enumerate(fr):
    f=f.copy(); cv2.putText(f,f'{i/10:.1f}',(3,15),0,0.45,(0,0,255),1); tiles.append(f)
cols=12
while len(tiles)%cols: tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite(f'ev/{n}_rosto.jpg',np.vstack([np.hstack(tiles[i:i+cols]) for i in range(0,len(tiles),cols)]))
# mouth motion energy per frame
m=fr[:, h//2:, w//4:3*w//4].astype(int)
d=np.abs(np.diff(m,axis=0)).mean(axis=(1,2,3))
print(n,' '.join(f'{(i+1)/10:.1f}:{v:.1f}' for i,v in enumerate(d)))
