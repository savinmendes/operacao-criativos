import json, sys
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=8)
base = r"C:\Users\PICHAU\Downloads\PERFUMES-PL\PARA-SUBIR\\"
for n in ["PL_PF-MASC-17","PL_PF-MASC-18","PL_PF-MASC-TESTE-1","PL_PF-MASC-TESTE-3","PL_PF-7"]:
    segs,_ = m.transcribe(base+n+".mp4", language="pl", word_timestamps=True, vad_filter=False, beam_size=5)
    out=[]
    for s in segs:
        out.append({"s":s.start,"e":s.end,"t":s.text,"w":[(w.start,w.end,w.word,w.probability) for w in s.words]})
    json.dump(out, open(n+"_whisper.json","w",encoding="utf-8"), ensure_ascii=False, indent=0)
    print(n, "ok", flush=True)
