# folha de contato dos últimos N s (a cada passo) de cada vídeo
import subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw
def dur(f): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
def folha(video, saida, ult=10.0, passo=1.0, w=180):
    d = dur(video); ts=[]; t=max(0,d-ult)
    while t < d-0.05: ts.append(t); t+=passo
    ts.append(d-0.25)
    ims=[]
    for t in ts:
        p = subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.3f}","-i",video,"-frames:v","1","-vf",f"scale={w}:-2","-f","image2pipe","-vcodec","png","-"],capture_output=True).stdout
        import io
        if not p: continue
        im=Image.open(io.BytesIO(p)).convert("RGB"); ImageDraw.Draw(im).text((4,4),f"{t:.1f}",fill=(255,0,0)); ims.append(im)
    W=w*len(ims); H=ims[0].height
    out=Image.new("RGB",(W,H)); [out.paste(im,(i*w,0)) for i,im in enumerate(ims)]
    out.save(saida, quality=85); print(saida, d)
if __name__=="__main__":
    folha(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv)>3 else 10, float(sys.argv[4]) if len(sys.argv)>4 else 1)
