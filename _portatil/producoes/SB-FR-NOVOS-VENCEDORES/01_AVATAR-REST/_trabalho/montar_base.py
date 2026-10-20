# base_fr.mp4: cenas da base limpa reposicionadas na linha do tempo FR (alongamento por repetição de quadro + congelamento final)
import json, subprocess, numpy as np
from comum3 import quadros, ENC_VF, ENC_TAG
T=json.load(open("timeline.json",encoding="utf-8")); FPS=30; NT=int(round(T["total"]*FPS))
idx=[]
for k in range(NT):
    t=(k+0.5)/FPS
    c=next(c for c in T["cenas"] if c["out_ini"]<=t<c["out_fim"]) if t<T["total"] else T["cenas"][-1]
    st=c["src_ini"]+min((t-c["out_ini"])/c["fator"], c["src_dur"]-0.5/FPS)
    idx.append(int(st*FPS))
assert all(b>=a for a,b in zip(idx,idx[1:]))
json.dump(idx,open("map_quadros.json","w"))
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","1080x1920","-r","30","-i","-",*ENC_VF,
    "-c:v","libx264","-crf","13","-preset","medium",*ENC_TAG,"base_fr.mp4"],stdin=subprocess.PIPE)
j=0
for i,f in enumerate(quadros("base_limpa.mp4",w=1080,h=1920)):
    while j<NT and idx[j]==i: enc.stdin.write(f.tobytes()); j+=1
    if j>=NT: break
enc.stdin.close(); enc.wait(); print("ok",j,"/",NT)
