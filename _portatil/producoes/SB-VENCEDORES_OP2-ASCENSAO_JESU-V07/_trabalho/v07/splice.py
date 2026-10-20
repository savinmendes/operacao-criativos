import json,subprocess,numpy as np
SR=48000
def load(p): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar','48000','-f','f32le','-'],capture_output=True).stdout,np.float32)
A=json.load(open('audio/corpo_fr09.alinhamento.json',encoding='utf-8')); a=load('audio/corpo_fr09.mp3')
C=json.load(open('audio/cta_fr09.alinhamento.json',encoding='utf-8')); c=load('audio/cta_fr09.mp3')
ch=A['characters']; st=A['character_start_times_seconds']; en=A['character_end_times_seconds']
s=''.join(ch); iF=s.index('Touche'); iG=s.index('Reçois')
endE=en[iF-2]; startF=st[iF]; endF=en[iG-2]; startG=st[iG]
cutA=(endE+startF)/2; cutB=(endF+startG)/2
# cta speech bounds
cs=[t for t,x in zip(C['character_start_times_seconds'],C['characters']) if not x.isspace()][0]
ce=[t for t,x in zip(C['character_end_times_seconds'],C['characters']) if not x.isspace()][-1]
print('old F',startF,endF,'cut',cutA,cutB,'cta',cs,ce)
leadA=startF-cutA; tailB=cutB-endF
seg=c[max(0,int((cs-leadA)*SR)):int((ce+tailB)*SR)]
if (cs-leadA)<0: seg=np.concatenate([np.zeros(int(-(cs-leadA)*SR),np.float32),seg])
fade=int(0.01*SR); seg=seg.copy(); seg[:fade]*=np.linspace(0,1,fade); seg[-fade:]*=np.linspace(1,0,fade)
pre=a[:int(cutA*SR)]; post=a[int(cutB*SR):]
out=np.concatenate([pre,seg,post]); delta=len(seg)/SR-(cutB-cutA)
off=cutA-(cs-leadA)
nch=ch[:iF]+[x for x in C['characters']]
nst=st[:iF]+[t+off for t in C['character_start_times_seconds']]
nen=en[:iF]+[t+off for t in C['character_end_times_seconds']]
# ensure separator space between CTA and G
nch+=[' ']; nst+=[nst[-1]]; nen+=[nen[-1]]
nch+=ch[iG:]; nst+=[t+delta for t in st[iG:]]; nen+=[t+delta for t in en[iG:]]
json.dump({'characters':nch,'character_start_times_seconds':nst,'character_end_times_seconds':nen},open('audio/corpo_v2.alinhamento.json','w',encoding='utf-8'),ensure_ascii=False)
out.tofile('audio/corpo_v2.f32'); subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar','48000','-ac','1','-i','audio/corpo_v2.f32','-c:a','pcm_s16le','audio/corpo_v2.wav'])
print('delta',round(delta,3),'len',len(out)/SR)
