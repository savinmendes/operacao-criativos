import subprocess,numpy as np,sys
def frames(p):
  cmd=["ffmpeg","-v","error","-i",p,"-vf","scale=90:160,format=gray","-f","rawvideo","-"]
  b=subprocess.run(cmd,capture_output=True).stdout
  return np.frombuffer(b,np.uint8).reshape(-1,160,90).astype(np.float32)
pl=frames(sys.argv[1]); it=frames(sys.argv[2])
print(len(pl),len(it))
d=np.abs(np.diff(pl,axis=0)).mean(axis=(1,2))
# loose frame: high diff to prev and next while prev~next
for i in range(1,len(pl)-1):
  a=d[i-1]; b=d[i]; pn=np.abs(pl[i+1]-pl[i-1]).mean()
  if a>8 and b>8 and pn<min(a,b)*0.5: print("solto? f",i,"t=%.3f"%(i/30),round(a,1),round(b,1),round(pn,1))
cuts=[i for i in range(len(d)) if d[i]>12]
print("cortes PL:",[round((i+1)/30,2) for i in cuts])
# compare to IT excluding subtitle band (rows 0.50-0.65?) - use top 45% and bottom 25%
n=min(len(pl),len(it))
m=np.ones((160,90),bool); m[int(160*0.48):int(160*0.66)]=False
dd=np.array([np.abs(pl[i]-it[i])[m].mean() for i in range(n)])
idx=np.where(dd>6)[0]
if len(idx):
  # group
  g=[[idx[0],idx[0]]]
  for i in idx[1:]:
    if i-g[-1][1]<=3: g[-1][1]=i
    else: g.append([i,i])
  for a,b in g: print("dif PLxIT %.2f-%.2f max %.1f"%(a/30,b/30,dd[a:b+1].max()))
print("mean diff",dd.mean())
