# folha.py video saida_prefixo [passo_s] [larg]  -> folhas de contato com tempo rotulado (max 80 quadros/folha)
import sys,subprocess,os,tempfile,glob
from PIL import Image,ImageDraw,ImageFont
v,out=sys.argv[1],sys.argv[2]; passo=float(sys.argv[3]) if len(sys.argv)>3 else 1.0; W=int(sys.argv[4]) if len(sys.argv)>4 else 160
d=tempfile.mkdtemp()
subprocess.run(["ffmpeg","-v","error","-i",v,"-vf",f"fps=1/{passo},scale={W}:-2","-q:v","4",os.path.join(d,"%05d.jpg")],check=True)
fs=sorted(glob.glob(os.path.join(d,"*.jpg")))
try: font=ImageFont.truetype("arialbd.ttf",14)
except: font=ImageFont.load_default()
N=80;cols=10
for p in range(0,len(fs),N):
    grp=fs[p:p+N]; im0=Image.open(grp[0]); w,h=im0.size; rows=(len(grp)+cols-1)//cols
    sheet=Image.new("RGB",(cols*w,rows*h),"black")
    for i,f in enumerate(grp):
        im=Image.open(f); t=(p+i)*passo; dr=ImageDraw.Draw(im)
        lab=f"{int(t//60)}:{t%60:04.1f}"; dr.rectangle([0,0,62,17],fill="black"); dr.text((2,1),lab,fill="yellow",font=font)
        sheet.paste(im,((i%cols)*w,(i//cols)*h))
    sheet.save(f"{out}_{p//N+1}.jpg",quality=80)
print(len(fs),"quadros")
