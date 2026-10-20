import subprocess,numpy as np,sys
from PIL import Image,ImageDraw
V=r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\VSL-LEAD2-DE.mp4"
segs=[(121,(250,410,220,360)),(251,(270,430,620,760)),(287,(300,440,280,400)),(546,(250,410,180,320)),(1111,(230,390,190,330)),(1641,(240,400,170,300)),(2011,(290,450,190,330)),(2271,(280,440,220,360))]
if len(sys.argv)>1: segs=[s for s in segs if s[0] in map(int,sys.argv[1:])]
for a,(x0,x1,y0,y1) in segs:
    d=4.0;fps=10
    r=subprocess.run(["ffmpeg","-v","error","-ss",str(a),"-t",str(d),"-i",V,"-vf",f"fps={fps},crop={x1-x0}:{y1-y0}:{x0}:{y0}","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
    W,H=x1-x0,y1-y0; f=np.frombuffer(r,np.uint8).reshape(-1,H,W,3)
    au=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-ss",str(a),"-t",str(d),"-i",V,"-ac","1","-ar","48000","-f","f32le","-"],capture_output=True).stdout,np.float32)
    n=len(f); cols=10; rows=(n+cols-1)//cols
    out=Image.new('RGB',(cols*W,rows*(H+24)),'black'); dr=ImageDraw.Draw(out)
    for i in range(n):
        seg=au[int(i*4800):int((i+1)*4800)]; e=float(np.sqrt(np.mean(seg**2))) if len(seg) else 0
        x,y=(i%cols)*W,(i//cols)*(H+24)
        out.paste(Image.fromarray(f[i]),(x,y))
        dr.rectangle([x,y+H+2,x+int(min(e/0.3,1)*W),y+H+12],fill='lime')
        dr.text((x+2,y+H+11),f"{a+i/fps:.1f}",fill='white')
    out.save(f"z/strip_{a}.jpg",quality=88)
