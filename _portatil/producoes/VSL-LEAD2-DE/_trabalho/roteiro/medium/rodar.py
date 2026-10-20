import sys, json, subprocess, os
from faster_whisper import WhisperModel
SRC=r"C:\Users\PICHAU\Downloads\Lead 2.mp4"
trechos=[(200,295),(385,470),(578,710),(780,850),(815,855),(1425,1445),(1700,1740),(1735,1760),(2140,2165),(2495,2515)]
m=WhisperModel('Systran/faster-whisper-medium',device='cpu',compute_type='int8')
out=[]
for a,b in trechos:
    wav=f"medium/t_{a}.wav"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(a),"-t",str(b-a),"-i",SRC,"-ac","1","-ar","16000",wav],check=True)
    segs,_=m.transcribe(wav,language='es',word_timestamps=False,vad_filter=False,beam_size=5)
    for s in segs:
        t=a+s.start
        line=f"[{int(t//60):02d}:{t%60:05.2f}-{int((a+s.end)//60):02d}:{(a+s.end)%60:05.2f}] {s.text.strip()}"
        print(line,flush=True); out.append(line)
    print('----',flush=True); out.append('----')
open('medium/medium.txt','w',encoding='utf-8').write("\n".join(out))
