import json,subprocess,numpy as np
NB=' '
def words(p):
    d=json.load(open(p,encoding='utf-8'))
    out=[];cur='';t0=None
    for c,a,b in zip(d['characters'],d['character_start_times_seconds'],d['character_end_times_seconds']):
        if c.isspace() and c!=NB:
            if cur: out.append([cur,t0,ult])
            cur='';t0=None
        else:
            if t0 is None:t0=a
            cur+=c;ult=b
    if cur: out.append([cur,t0,ult])
    return out
def load(p):
    return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar','48000','-f','f32le','-'],capture_output=True).stdout,np.float32)
SR=48000
HOOK=5.60
hw=words('audio/hook_fr09.alinhamento.json'); ha=load('audio/hook_fr09.mp3')
cw=words('audio/corpo_v2.alinhamento.json'); ca=load('audio/corpo_v2.wav')
# sentence ends
ends=[i for i,w in enumerate(cw) if w[0].endswith('.')]
extra=[0.2,0.5,0.1,0.0,0.2,0.0]  # after sentences A..F
LEAD=0.3
pieces=[];newcw=[];shift=LEAD;prev_cut=0.0
cuts=[]
for k,e in enumerate(ends):
    if k<len(ends)-1:
        cut=(cw[e][2]+cw[e+1][1])/2
    else:
        cut=len(ca)/SR
    seg=ca[int(prev_cut*SR):int(cut*SR)]
    for w in cw[(ends[k-1]+1 if k else 0):e+1]:
        newcw.append([w[0],w[1]+shift,w[2]+shift])
    pieces.append(seg)
    if k<len(extra): pieces.append(np.zeros(int(extra[k]*SR),np.float32)); 
    shift+= extra[k] if k<len(extra) else 0
    prev_cut=cut
body=np.concatenate([np.zeros(int(LEAD*SR),np.float32)]+pieces+[np.zeros(int(0.55*SR),np.float32)])
bodylen=len(body)/SR
hookpad=np.zeros(int(HOOK*SR),np.float32); hookpad[:len(ha)]=ha[:len(hookpad)]
full=np.concatenate([hookpad,body])
full.tofile('audio/voz_fr_full.f32')
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar','48000','-ac','1','-i','audio/voz_fr_full.f32','-c:a','pcm_s16le','audio/voz_fr_full.wav'])
allw=[[w[0],round(w[1],3),round(w[2],3)] for w in hw]+[[w[0],round(w[1]+HOOK,3),round(w[2]+HOOK,3)] for w in newcw]
json.dump(allw,open('audio/voz_fr_words.json','w',encoding='utf-8'),ensure_ascii=False)
def st(word,n=0):
    c=[w for w in allw if w[0].lower().startswith(word.lower())]; return c[n][1]
total=len(full)/SR
sc={}
sc['hook']=(0,HOOK)
b=[HOOK, st('Jésus')-0.2, st('Il')-0.35, st('Dans')-0.05, st('débloque')-0.05, st('Mais')-0.1, st('Appuie')-0.1, st('Reçois')-0.15, total]
names=['crown1','woman','key','crown2','gate','sad','crown3','door']
scenes=[('hook',0,HOOK)]+[(n,round(b[i],3),round(b[i+1],3)) for i,n in enumerate(names)]
json.dump({'total':total,'scenes':scenes,'arrow':st('Appuie')},open('timeline.json','w'),indent=1)
for s in scenes: print(s, round(s[2]-s[1],2))
print('total',round(total,2),'arrow',st('Appuie'))
