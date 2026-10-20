import json
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=6)
segs, info = m.transcribe("demucs/htdemucs/orig/vocals.wav", language="pt", word_timestamps=True, vad_filter=False)
out=[]
for s in segs:
    for w in s.words: out.append([round(w.start,2), round(w.end,2), w.word.strip()])
    print(round(s.start,2), round(s.end,2), s.text, flush=True)
json.dump(out, open("palavras_pt.json","w",encoding="utf-8"), ensure_ascii=False)
