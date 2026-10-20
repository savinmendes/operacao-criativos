# Trilha do original (demucs no_vocals) recortada por cena na duração IT; cena IT mais longa que a ES puxa trilha de antes (sem buraco de silêncio)
import json,subprocess,numpy as np
SR=48000
a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i','demucs/htdemucs/es_audio/no_vocals.wav','-ac','2','-ar','48000','-f','f32le','-'],capture_output=True).stdout,np.float32).reshape(-1,2)
TL=json.load(open('timeline.json'))
es_cuts=[6.27,10.27,11.8,15.5,19.33,22.25,25.6,28.8,len(a)/SR]
it=[s[2] for s in TL['scenes']]
out=[];prev=0.0;X=int(0.03*SR)
for e_end,e_f in zip(es_cuts,it):
    need=int(round((e_f-prev)*SR)); i1=int(e_end*SR); i0=max(0,i1-need)
    seg=a[i0:i1].copy()
    if len(seg)<need: seg=np.concatenate([seg,a[i1:i1+need-len(seg)]])
    ramp=np.linspace(0,1,X)[:,None]; seg[:X]*=ramp; seg[-X:]*=ramp[::-1]
    out.append(seg); prev=e_f
b=np.concatenate(out)
b[-int(0.4*SR):]*=np.linspace(1,0,int(0.4*SR))[:,None]
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar','48000','-ac','2','-i','-','-c:a','pcm_s16le','audio/bed_it.wav'],input=b.astype(np.float32).tobytes())
print(len(b)/SR)
