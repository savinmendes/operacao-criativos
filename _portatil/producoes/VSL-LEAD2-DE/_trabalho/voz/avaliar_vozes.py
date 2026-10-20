import gpu
import glob, numpy as np, subprocess, librosa, sys, json
from faster_whisper import WhisperModel
def f0(path, ss=None, t=None):
    cmd=["ffmpeg","-v","error"]+(["-ss",str(ss),"-t",str(t)] if ss is not None else [])+["-i",path,"-ac","1","-ar","16000","-f","f32le","-"]
    x=np.frombuffer(subprocess.run(cmd,capture_output=True).stdout,np.float32)
    f,v,_=librosa.pyin(x,fmin=60,fmax=400,sr=16000,frame_length=1024)
    f=f[~np.isnan(f)]; return round(float(np.median(f)),1), round(float(np.percentile(f,90)-np.percentile(f,10)),1)
src=r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\base\audio_orig.wav"
for nome,(a,b) in {"orig_apresentador":(0,7.5),"orig_apres2":(29.6,41.7),"orig_dep1":(585,604),"orig_dep2":(620,648),"orig_dep3":(660,690),"orig_padre":(1000,1020)}.items():
    print(nome, f0(src,a,b-a))
m=WhisperModel("medium",device="cuda",compute_type="float16")
for p in sorted(glob.glob("testes_vozes/*.mp3")):
    segs,info=m.transcribe(p,language=None,beam_size=5)
    txt=" ".join(s.text for s in segs)
    print(p, f0(p), info.language, round(info.language_probability,3), txt[:120])
