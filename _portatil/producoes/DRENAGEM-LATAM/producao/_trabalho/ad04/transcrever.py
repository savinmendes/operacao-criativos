# -*- coding: utf-8 -*-
import json, subprocess, sys
from faster_whisper import WhisperModel
src, dst = sys.argv[1], sys.argv[2]
subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-vn","-ac","1","-ar","16000","a.wav"],check=True)
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
segs, _ = m.transcribe("a.wav", language="es", word_timestamps=True)
pal=[]
for s in segs:
    for w in s.words: pal.append([w.word.strip(), round(w.start,2), round(w.end,2)])
    print(f"{s.start:.1f} {s.text}", flush=True)
open(dst,"w",encoding="utf-8").write(json.dumps(pal,ensure_ascii=False))
print("OK")
