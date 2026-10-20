import subprocess,numpy as np,json
V=r'C:/Users/PICHAU/Downloads/TESTE1-SB-ES/v4/SB-ES_NOTICIA-AURELIO_B-ORACION-COMPLETA_FICTICIO.mp4'
W,H=90,160
p=subprocess.run(['ffmpeg','-v','error','-i',V,'-vf',f'scale={W}:{H}','-f','rawvideo','-pix_fmt','gray','-'],capture_output=True)
a=np.frombuffer(p.stdout,np.uint8).reshape(-1,H,W).astype(np.float32)
np.save('gray.npy',a)
n=len(a);print('frames',n)
d=np.abs(a[1:]-a[:-1]).mean((1,2))
mean=a.mean((1,2))
for i in range(n):
    if mean[i]<15: print('escuro',i,f'{i/30:.2f}',mean[i])
# isolated: frame i differs from i-1 and i+1 strongly but i-1 vs i+1 is similar
for i in range(1,n-1):
    d1=np.abs(a[i]-a[i-1]).mean(); d2=np.abs(a[i+1]-a[i]).mean(); d3=np.abs(a[i+1]-a[i-1]).mean()
    if d1>12 and d2>12 and d3<0.6*min(d1,d2): print('solto?',i,f'{i/30:.2f}',round(d1,1),round(d2,1),round(d3,1))
# cuts
cuts=[i+1 for i in range(len(d)) if d[i]>14]
print('cortes',[(c,round(c/30,2),round(float(d[c-1]),1)) for c in cuts])
# 2-frame flashes: cut followed by another cut within 3 frames
for x,y in zip(cuts,cuts[1:]):
    if y-x<=3: print('flash curto',x,y,f'{x/30:.2f}')
