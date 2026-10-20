# base_en.mp4: cenas da base limpa reposicionadas na linha do tempo EN (alongamento por repetição de quadro).
# Aceita fonte fora de ordem (jump cut para tomada anterior): guarda em memória só os quadros ainda pendentes.
import json, subprocess, collections
from comum3 import quadros, ENC_VF, ENC_TAG
T=json.load(open("timeline.json",encoding="utf-8")); FPS=30; NT=int(round(T["total"]*FPS))
idx=[]
for k in range(NT):
    t=(k+0.5)/FPS
    c=next((c for c in T["cenas"] if c["out_ini"]<=t<c["out_fim"]),T["cenas"][-1])
    st=c["src_ini"]+min((t-c["out_ini"])/c["fator"], c["src_dur"]-0.5/FPS)
    idx.append(int(st*FPS))
json.dump(idx,open("map_quadros.json","w"))
resta=collections.Counter(idx); cache={}
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","1080x1920","-r","30","-i","-",*ENC_VF,
    "-c:v","libx264","-crf","13","-preset","medium",*ENC_TAG,"base_en.mp4"],stdin=subprocess.PIPE)
src=enumerate(quadros("base_limpa.mp4",w=1080,h=1920)); j=0; pico=0
for k in range(NT):
    while idx[k] not in cache:
        i,f=next(src)
        if resta[i]: cache[i]=f
    enc.stdin.write(cache[idx[k]].tobytes()); resta[idx[k]]-=1
    if not resta[idx[k]]: del cache[idx[k]]
    pico=max(pico,len(cache))
enc.stdin.close(); enc.wait(); print("ok",NT,"pico cache",pico)
