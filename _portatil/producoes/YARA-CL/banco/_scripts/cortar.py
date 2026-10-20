# cortar.py takes.json -> corta cada take em 720x1280 9:16, 30fps, sem audio, h264 crf18; gera indice.json
import json,subprocess,sys,os
B=r"C:\Users\PICHAU\Downloads\YARA-CL\banco"
takes=json.load(open(sys.argv[1],encoding="utf-8"))
so=set(sys.argv[2:])
def probe(f):
    o=subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=width,height:stream_side_data=rotation","-of","json",f],capture_output=True,text=True).stdout
    s=json.loads(o)["streams"][0]; return s["width"],s["height"]
idx=[]
for t in takes:
    src=os.path.join(B,"_src",t["src"]); W,H=probe(src)
    # regiao util (x0,y0,w,h) em fracao opcional (ex.: pillarbox)
    rx,ry,rw,rh=t.get("regiao",[0,0,1,1]); RX,RY,RW,RH=rx*W,ry*H,rw*W,rh*H
    z=t.get("zoom",1.0)
    if RW/RH>9/16: ch=RH/z; cw=ch*9/16
    else: cw=RW/z; ch=cw*16/9
    cx=RX+t.get("cx",0.5)*RW; cy=RY+t.get("cy",0.5)*RH
    x=min(max(cx-cw/2,RX),RX+RW-cw); y=min(max(cy-ch/2,RY),RY+RH-ch)
    cw,ch,x,y=[int(round(v))//2*2 for v in (cw,ch,x,y)]
    out=os.path.join(B,t["arquivo"])
    if not so or t["arquivo"] in so:
        vf=f"crop={cw}:{ch}:{x}:{y},scale=720:1280:flags=lanczos,fps=30,format=yuv420p"
        subprocess.run(["ffmpeg","-v","error","-y","-ss",str(t["ini"]),"-i",src,"-t",str(t["dur"]),"-vf",vf,"-an","-c:v","libx264","-crf","18","-preset","slow","-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709","-movflags","+faststart",out],check=True)
    d=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",out],capture_output=True,text=True).stdout)
    idx.append({"arquivo":t["arquivo"],"perfume":t["perfume"],"duracao_s":round(d,2),"acao":t["acao"],"fonte_url":t["url"],"trecho_original":f'{t["ini"]}s +{t["dur"]}s',"resolucao_fonte":f"{W}x{H}","recorte_px":f"{cw}x{ch}","observacoes":t.get("obs","")})
    print(t["arquivo"],f"{W}x{H} crop {cw}x{ch}@{x},{y}",round(d,2))
json.dump(idx,open(os.path.join(B,"indice.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
