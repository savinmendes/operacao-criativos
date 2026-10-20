import sys, json
from faster_whisper import WhisperModel
wav, out = sys.argv[1], sys.argv[2]
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=8)
res = {}
for lang in ["fr", "es", None]:
    segs, info = m.transcribe(wav, language=lang, word_timestamps=True, vad_filter=False, beam_size=5)
    segs = list(segs)
    res[str(lang)] = {"lang": info.language, "prob": info.language_probability,
        "segs": [{"s": s.start, "e": s.end, "t": s.text, "w": [(w.start, w.end, w.word, w.probability) for w in s.words]} for s in segs]}
    print("=== lang", lang, info.language, round(info.language_probability, 3))
    for s in segs: print(f"{s.start:6.2f}-{s.end:6.2f} {s.text}")
# language detect per 5s window
import numpy as np
from faster_whisper.audio import decode_audio
a = decode_audio(wav, 16000)
print("=== deteccao por janela 4s")
for i in range(0, len(a), 16000*4):
    seg = a[i:i+16000*4]
    if len(seg) < 16000: break
    l, p, allp = m.detect_language(seg)
    d = dict(allp[:3]) if isinstance(allp, list) else {}
    print(f"{i/16000:5.1f}s {l} {p:.2f} {[(k, round(v,2)) for k,v in allp[:3]]}")
json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
