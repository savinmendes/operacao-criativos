import subprocess, sys, json
from faster_whisper import WhisperModel
segs=json.loads(sys.argv[1])
parts=[]
for i,(a,b) in enumerate(segs):
    o=f"tc{i}.wav"; subprocess.run(["ffmpeg","-v","error","-y","-ss",str(a),"-to",str(b),"-i","orig16.wav",o],check=True); parts.append(o)
subprocess.run(["ffmpeg","-v","error","-y",*sum([["-i",p] for p in parts],[]),"-filter_complex","".join(f"[{i}:a]" for i in range(len(parts)))+f"concat=n={len(parts)}:v=0:a=1","tc.wav"],check=True)
m=WhisperModel("small",device="cpu",compute_type="int8",cpu_threads=4)
s,_=m.transcribe("tc.wav",language="es",word_timestamps=True)
off=[0];
for a,b in segs: off.append(off[-1]+b-a)
print("limites:",[round(x,2) for x in off])
for x in s:
    print(" ".join(f"{w.word.strip()}[{w.start:.2f}]" for w in x.words))
