import sys, json, subprocess, numpy as np
v, out = sys.argv[1], sys.argv[2]
W,H=108,192
p = subprocess.Popen(['ffmpeg','-v','error','-i',v,'-vf',f'scale={W}:{H}','-f','rawvideo','-pix_fmt','gray','-'], stdout=subprocess.PIPE)
fr=[]
while True:
    b=p.stdout.read(W*H)
    if len(b)<W*H: break
    fr.append(np.frombuffer(b,np.uint8).reshape(H,W).astype(np.float32))
fr=np.array(fr)
lum=fr.mean(axis=(1,2))
d=np.r_[0, np.abs(np.diff(fr,axis=0)).mean(axis=(1,2))]
json.dump({'lum':lum.round(2).tolist(),'diff':d.round(2).tolist()},open(out,'w'))
med=np.median(d)
cuts=[i for i in range(1,len(d)) if d[i]>max(12,6*med)]
print('n',len(fr),'cuts',[(i,round(i/30,2),round(float(d[i]),1)) for i in cuts])
c=[0]+cuts+[len(fr)]
for a,b in zip(c[:-1],c[1:]):
    print(f'shot {a/30:6.2f}-{b/30:6.2f} dur {(b-a)/30:5.2f} lum {lum[a:b].mean():6.1f} min {lum[a:b].min():6.1f} max {lum[a:b].max():6.1f}', ' <<SHORT' if (b-a)<9 else '')
blk=[i for i in range(len(lum)) if lum[i]<8]
print('black frames', [round(i/30,2) for i in blk][:40])
# flash: luma spike vs neighbours
fl=[i for i in range(1,len(lum)-1) if lum[i]-max(lum[i-1],lum[i+1])>15 or min(lum[i-1],lum[i+1])-lum[i]>15]
print('flash/dip single frames', [round(i/30,2) for i in fl])
