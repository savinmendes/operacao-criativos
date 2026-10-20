import subprocess,numpy as np
V=r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\VSL-LEAD2-DE.mp4"
x0,y0,W,H=90,25,160,45; fps=5
p=subprocess.Popen(["ffmpeg","-v","error","-i",V,"-vf",f"fps={fps},crop={W}:{H}:{x0}:{y0}","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
fr=[]
while True:
    b=p.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    fr.append(np.frombuffer(b,np.uint8).reshape(H,W,3).astype(np.int16))
fr=np.array(fr); np.save('badge.npy',fr.astype(np.uint8))
r,g,bb=fr[...,0],fr[...,1],fr[...,2]
red=((r>150)&(g<90)&(bb<90)).mean(axis=(1,2))
white=((r>200)&(g>200)&(bb>200))
tmpl=white[int(10*fps)]  # frame at 10s known LIVE
res=[]
for i in range(len(fr)):
    w=white[i]; inter=(w&tmpl).sum(); uni=(w|tmpl).sum()+1
    res.append((i/fps,red[i],inter/uni,w.mean()))
np.save('badge_res.npy',np.array(res))
bad=[x for x in res if x[1]>0.15 and x[2]<0.5]
print(len(res),'frames; red-present-but-text-not-LIVE:',len(bad))
prev=None
for t,rd,iou,wm in bad:
    print(f"{int(t//60):02d}:{t%60:05.2f} red={rd:.2f} iou={iou:.2f} white={wm:.3f}")
