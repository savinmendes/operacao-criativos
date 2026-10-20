import subprocess,numpy as np,sys
from PIL import Image,ImageDraw
V='../../SB-PL-OP2-ASCENSAO.mp4'
def frames(t0,t1,crop):
    x,y,w,h=crop
    p=subprocess.run(['ffmpeg','-v','error','-ss',str(t0),'-i',V,'-t',str(t1-t0),'-vf',f'crop={w}:{h}:{x}:{y}','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    n=len(p)//(w*h*3); return np.frombuffer(p,np.uint8)[:n*w*h*3].reshape(n,h,w,3)
jobs=[('A',0.8,3.25,(340,480,400,400)),('B',3.15,3.6,(340,480,400,400)),('C',6.6,7.15,(340,480,400,400)),
      ('D',19.2,19.85,(320,740,400,400)),('E',25.2,25.9,(340,740,400,400)),('F',27.2,28.73,(340,740,400,400))]
for name,t0,t1,c in jobs:
    f=frames(t0,t1,c)
    d=[0]+[float(np.abs(f[i].astype(int)-f[i-1].astype(int)).mean()) for i in range(1,len(f))]
    print(name,t0,'n',len(f),' '.join(f'{t0+i/30:.2f}:{v:.1f}' for i,v in enumerate(d)))
    step=max(1,len(f)//16); sel=list(range(0,len(f),step))[:16]
    w,h=c[2]//2,c[3]//2; cols=8
    im=Image.new('RGB',(w*cols,h*((len(sel)+cols-1)//cols)))
    dr=ImageDraw.Draw(im)
    for k,i in enumerate(sel):
        im.paste(Image.fromarray(f[i]).resize((w,h)),((k%cols)*w,(k//cols)*h))
        dr.text(((k%cols)*w+3,(k//cols)*h+3),f'{t0+i/30:.2f}',fill=(255,0,0))
    im.save(f'boca_{name}.jpg',quality=88)
