import subprocess,numpy as np,json,sys
V=r'C:\Users\PICHAU\Downloads\SB-IT-OFERTA-LIVE\06_ADS-6\SB-IT-ADS-6.mp4'
W,H=1080,400
p=subprocess.Popen(['ffmpeg','-v','error','-i',V,'-vf','fps=4,crop=1080:400:0:1300','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
i=0;res=[]
while True:
    b=p.stdout.read(W*H*3)
    if len(b)<W*H*3:break
    a=np.frombuffer(b,np.uint8).reshape(H,W,3).astype(int)
    # yellow text: R>200,G>200,B<90 ; white text R,G,B>235
    yel=(a[...,0]>200)&(a[...,1]>190)&(a[...,2]<100)
    cols=np.where(yel.any(0)|((a.min(2)>240).sum(0)>3))[0]
    rows=np.where(yel.any(1))[0]
    res.append((i/4, int(cols.min()) if len(cols) else -1, int(cols.max()) if len(cols) else -1, int(yel.sum()), int(rows.min())+1300 if len(rows) else -1, int(rows.max())+1300 if len(rows) else -1))
    i+=1
json.dump(res,open('edge.json','w'))
print('frames',len(res))
print('min left',min(r[1] for r in res if r[1]>=0),'max right',max(r[2] for r in res))
print('yel rows',min(r[4] for r in res if r[4]>0),max(r[5] for r in res))
print('no-yellow times',[r[0] for r in res if r[3]<200][:40])
print('edge-touch',[r for r in res if 0<=r[1]<25 or r[2]>1055][:20])
