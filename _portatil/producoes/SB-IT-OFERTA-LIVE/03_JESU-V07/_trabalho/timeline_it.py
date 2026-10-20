# Voz IT na linha do tempo (gancho com pausa + corpo com pausas dramáticas), palavras e cenas
import json,subprocess,numpy as np
from palavras import palavras
SR=48000
def load(p): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar','48000','-f','f32le','-'],capture_output=True).stdout,np.float32)
def pausar(audio,pw,P):
    # P: lista (palavra, segundos) -> insere silêncio no meio do vão após a palavra
    ins=[];j=0
    for q,(w,s,e) in enumerate(pw):
        if j<len(P) and w==P[j][0]:
            nx=pw[q+1][1] if q+1<len(pw) else e+0.1
            ins.append(((e+nx)/2,P[j][1])); j+=1
    assert j==len(P),(j,P)
    out=[];prev=0
    for t,d in ins: i=int(t*SR); out+=[audio[prev:i],np.zeros(int(d*SR),np.float32)]; prev=i
    out.append(audio[prev:])
    sh=lambda x: x+sum(d for t,d in ins if x>=t)
    return np.concatenate(out),[[w,sh(s),sh(e)] for w,s,e in pw]
ha=load('audio/hook_it.mp3'); hw=palavras('audio/hook_it.alinhamento.json')
ha,hw=pausar(ha,hw,[('adesso,',0.25)])
hend=hw[-1][2]+0.12; ha=ha[:int(hend*SR)]
HOOK=round(hend+0.45,2)
ca=load('audio/corpo_it.mp3'); cw=palavras('audio/corpo_it.alinhamento.json')
ca,cw=pausar(ca,cw,[('modo.',0.10),('te.',0.10),('te.',0.10),('diretta.',0.15)])
cend=cw[-1][2]+0.12; ca=ca[:int(cend*SR)]
LEAD=0.30; TAIL=0.70
hookpad=np.zeros(int(HOOK*SR),np.float32); hookpad[:len(ha)]=ha
f=int(0.01*SR); hookpad[len(ha)-f:len(ha)]*=np.linspace(1,0,f)
full=np.concatenate([hookpad,np.zeros(int(LEAD*SR),np.float32),ca,np.zeros(int(TAIL*SR),np.float32)])
full.tofile('audio/voz_it_full.f32')
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar','48000','-ac','1','-i','audio/voz_it_full.f32','-c:a','pcm_s16le','audio/voz_it_full.wav'])
allw=[[w,round(s,3),round(e,3)] for w,s,e in hw]+[[w,round(s+HOOK+LEAD,3),round(e+HOOK+LEAD,3)] for w,s,e in cw]
json.dump(allw,open('audio/voz_it_words.json','w',encoding='utf-8'),ensure_ascii=False)
def st(word,n=0): return [w for w in allw if w[0]==word][n][1]
total=round(len(full)/SR,4)
b=[HOOK, st('Gesù')-0.2, st('Ha')-0.3, st('Oggi')-0.1, st('sblocca')-0.05, st('Ma')-0.1, st('Tocca')-0.1, st('Ricevi')-0.15, total]
names=['crown1','woman','key','crown2','gate','sad','crown3','door']
scenes=[('hook',0,HOOK)]+[(n,round(b[i],3),round(b[i+1],3)) for i,n in enumerate(names)]
json.dump({'total':total,'scenes':scenes,'arrow':st('Tocca')},open('timeline.json','w'),indent=1)
for s in scenes: print(s, round(s[2]-s[1],2))
print('total',total,'arrow',st('Tocca'))
