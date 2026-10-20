import json
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cpu", compute_type="int8")
out = {}
for arq, lang in [("gancho.wav","es"),("gancho_2s.wav","es"),("gancho_2s.wav",None),("gancho_2s.wav","pt")]:
    segs, info = m.transcribe(arq, language=lang, word_timestamps=True, beam_size=5)
    segs = list(segs)
    words = [(w.word, round(w.start,2), round(w.end,2), round(w.probability,2)) for s in segs for w in s.words]
    print(f"== {arq} lang={lang} detect={info.language} p={info.language_probability:.2f}")
    print(" ".join(s.text for s in segs))
    print(words[:12])
    out[f"{arq}|{lang}"] = {"det": info.language, "words": words}
json.dump(out, open("transcricao_gancho.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
