import json,subprocess,numpy as np
SR=48000
a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i','demucs/htdemucs/es_audio/no_vocals.wav','-ac','2','-ar','48000','-f','f32le','-'],capture_output=True).stdout,np.float32).reshape(-1,2)
TL=json.load(open('timeline.json'))
es_cuts=[6.27,10.27,11.8,15.5,19.33,22.25,25.6,28.8,len(a)/SR]
en=[s[2] for s in TL['scenes']]
out=[];prev_en=0.0;X=int(0.03*SR)
for e_end,e_f in zip(es_cuts,en):
    d=e_f-prev_en; s=max(0,e_end-d)
    seg=a[int(s*SR):int(e_end*SR)].copy()
    need=int(round(d*SR))
    if len(seg)<need: seg=np.concatenate([np.zeros((need-len(seg),2),np.float32),seg])
    seg=seg[-need:]
    ramp=np.linspace(0,1,X)[:,None]; seg[:X]*=ramp; seg[-X:]*=ramp[::-1]
    out.append(seg); prev_en=e_f
b=np.concatenate(out)
b[-int(0.4*SR):]*=np.linspace(1,0,int(0.4*SR))[:,None]
b.astype(np.float32).tofile('audio/bed.f32')
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar','48000','-ac','2','-i','audio/bed.f32','-c:a','pcm_s16le','audio/bed_en.wav'])
print(len(b)/SR)
