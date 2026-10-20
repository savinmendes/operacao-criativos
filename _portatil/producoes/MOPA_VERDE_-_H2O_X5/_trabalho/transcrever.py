import json, sys, os, glob
from faster_whisper import WhisperModel
BASE = r"C:\Users\PICHAU\Downloads\MOPA VERDE - H2O X5"
out = os.path.join(BASE, "_trabalho", "transcricoes")
if False:
    m = WhisperModel("large-v3", device="cuda", compute_type="float16")
else:
    m = WhisperModel("medium", device="cpu", compute_type="int8")
for f in sorted(glob.glob(os.path.join(BASE, "VIDEOS", "*.mp4"))):
    vid = os.path.basename(f)[:2]
    try:
        segs, info = m.transcribe(f, language="en", word_timestamps=True, vad_filter=False)
        segs = list(segs)
    except Exception as e:
        print(vid, "ERRO", e); json.dump({"erro": str(e)}, open(os.path.join(out, vid + ".json"), "w")); continue
    data = {"id": vid, "texto": " ".join(s.text.strip() for s in segs),
            "segmentos": [{"ini": round(s.start,2), "fim": round(s.end,2), "texto": s.text.strip(), "no_speech": round(s.no_speech_prob,2),
                           "palavras": [{"w": w.word.strip(), "ini": round(w.start,2), "fim": round(w.end,2), "p": round(w.probability,2)} for w in (s.words or [])]} for s in segs]}
    json.dump(data, open(os.path.join(out, vid + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(vid, "|", data["texto"][:400])
