# -*- coding: utf-8 -*-
import json, subprocess, sys, time
from faster_whisper import WhisperModel
src, dst = sys.argv[1], sys.argv[2]
subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-vn","-ac","1","-ar","16000","a16.wav"],check=True)
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
t0=time.time()
segs, info = m.transcribe("a16.wav", language="es", word_timestamps=True, condition_on_previous_text=False)
pal=[]; out=[]
for s in segs:
    out.append([round(s.start,2),round(s.end,2),s.text.strip()])
    pal += [[w.word.strip(), round(w.start,2), round(w.end,2)] for w in s.words]
    print(f"[{s.end/info.duration:.0%}] {s.end:.0f}s decorrido {time.time()-t0:.0f}s", flush=True)
json.dump(pal, open(dst,"w",encoding="utf-8"), ensure_ascii=False)
json.dump(out, open(dst.replace(".json","_seg.json"),"w",encoding="utf-8"), ensure_ascii=False)
print("OK")
