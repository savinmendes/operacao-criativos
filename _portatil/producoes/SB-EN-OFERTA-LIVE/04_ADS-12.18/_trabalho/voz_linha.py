# Coloca as frases EN na linha do tempo do AD ES (cenas iguais ao original) -> audio/voz_en.wav + audio/palavras_en.json
import soundfile as sf, numpy as np, subprocess, json, re
SR=48000; TOTAL=31.62
INI={"p1":0.15,"p2":6.30,"p3":10.84,"p4":12.56,"p5":15.84,"p6":23.76,"p7":26.25}
def load(p):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,2).copy()
v=np.zeros((int(TOTAL*SR),2),np.float32); pal=[]
for k,t0 in INI.items():
    a=load(f"audio/{k}.mp3"); i=int(t0*SR); v[i:i+len(a)]+=a[:len(v)-i]
    al=json.load(open(f"audio/{k}.alinhamento.json",encoding="utf-8"))
    ch=al["characters"]; st=al["character_start_times_seconds"]; en=al["character_end_times_seconds"]
    w="";s=None
    for c,a0,a1 in zip(ch+[" "],st+[0],en+[0]):
        if c.isspace():
            if w: pal.append([w,round(s+t0,3),round(e+t0,3),k]); w=""
        else:
            if not w: s=a0
            w+=c; e=a1
    print(k,t0,"->",round(t0+len(a)/SR,2))
sf.write("audio/voz_en.wav",v,SR)
json.dump(pal,open("audio/palavras_en.json","w",encoding="utf-8"),ensure_ascii=False,indent=0)
