import json, subprocess, sys
from faster_whisper import WhisperModel
src = r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\originais\01.mp4"
subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-vn","-ac","1","-ar","16000","orig16.wav"],check=True)
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
segs,_ = m.transcribe("orig16.wav", language="es", word_timestamps=True)
pal=[]; out=open("transcr_seg.txt","w",encoding="utf-8")
for s in segs:
    out.write(f"{s.start:7.2f}-{s.end:7.2f} {s.text.strip()}\n"); out.flush()
    pal += [[w.word.strip(), round(w.start,2), round(w.end,2)] for w in s.words]
    print(f"{s.end:.0f}/463", flush=True)
json.dump(pal, open("palavras.json","w",encoding="utf-8"), ensure_ascii=False)
print("OK")
