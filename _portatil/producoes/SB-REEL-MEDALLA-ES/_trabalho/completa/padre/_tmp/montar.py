import json,subprocess,re
P="C:/Users/PICHAU/Downloads/SB-REEL-MEDALLA-ES/_trabalho/completa/padre"
T=P+"/_tmp"; PAUSA=0.35
falas=json.load(open(T+"/falas.json",encoding="utf-8"))
def palavras(al):
    ch,st,en=al["characters"],al["character_start_times_seconds"],al["character_end_times_seconds"]
    out=[];cur=None
    for c,s,e in zip(ch,st,en):
        if c.isspace():
            if cur: out.append(cur);cur=None
            continue
        if cur is None: cur={"w":c,"ini":s,"fim":e}
        else: cur["w"]+=c;cur["fim"]=e
    if cur: out.append(cur)
    return out
segs=[];words=[];blocos=[];t=0.0
for i in range(3):
    al=json.load(open(f"{T}/f{i+1}.alinhamento.json",encoding="utf-8"))
    ws=palavras(al)
    a=max(0.0,ws[0]["ini"]-0.04); b=ws[-1]["fim"]+0.06
    # recorte
    subprocess.run(["ffmpeg","-y","-v","error","-i",f"{T}/f{i+1}.mp3","-af",f"atrim={a}:{b},asetpts=N/SR/TB","-ar","44100","-ac","1",f"{T}/c{i+1}.wav"],check=True)
    if i>0: t+=PAUSA
    off=t-a
    for w in ws: words.append({"w":w["w"],"ini":round(w["ini"]+off,3),"fim":round(w["fim"]+off,3),"personagem":"padre"})
    blocos.append({"fala":i+1,"texto":falas[i],"ini":round(ws[0]["ini"]+off,3),"fim":round(ws[-1]["fim"]+off,3)})
    t+=b-a
subprocess.run(["ffmpeg","-y","-v","error","-f","lavfi","-t",str(PAUSA),"-i","anullsrc=r=44100:cl=mono",f"{T}/sil.wav"],check=True)
lst="\n".join(f"file '{x}'" for x in [f"{T}/c1.wav",f"{T}/sil.wav",f"{T}/c2.wav",f"{T}/sil.wav",f"{T}/c3.wav"])
open(T+"/lista.txt","w").write(lst)
subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",T+"/lista.txt","-c:a","libmp3lame","-b:a","192k",P+"/padre.mp3"],check=True)
subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",T+"/lista.txt","-c:a","pcm_s16le",T+"/padre.wav"],check=True)
json.dump(words,open(P+"/palavras.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
json.dump({"audio":"padre.mp3","duracao_total":round(t,3),"pausa_entre_falas":PAUSA,"falas":blocos},open(P+"/blocos.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(t,blocos)
