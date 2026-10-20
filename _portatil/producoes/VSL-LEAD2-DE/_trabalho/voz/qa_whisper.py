import gpu, json, glob, os, re, sys
from faster_whisper import WhisperModel
import gerar
try:
    from num2words import num2words
except ImportError:
    num2words = None
def norm(t):
    t = t.lower().replace("ß", "ss")
    if num2words:
        t = re.sub(r"\d+", lambda m: num2words(int(m.group()), lang="de"), t)
    t = re.sub(r"[-–]", " ", t)
    t = re.sub(r"[^\wäöüé ]", " ", t)
    return t.split()
def wer(ref, hyp):
    import difflib
    sm = difflib.SequenceMatcher(None, ref, hyp, autojunk=False)
    err = 0; diffs = []
    for op, a, b, c, d in sm.get_opcodes():
        if op != "equal":
            err += max(b - a, d - c); diffs.append((" ".join(ref[a:b]), " ".join(hyp[c:d])))
    return err / max(1, len(ref)), diffs
ids = sys.argv[1:]
m = WhisperModel("medium", device="cuda", compute_type="float16")
res = json.load(open("qa_whisper.json", encoding="utf-8")) if os.path.exists("qa_whisper.json") else {}
for i, b in enumerate(gerar.BL):
    if ids and b["id"] not in ids: continue
    p = f"tts/{b['id']}.mp3"
    segs, info = m.transcribe(p, language="de", beam_size=5, word_timestamps=True, condition_on_previous_text=False)
    segs = list(segs)
    hyp = " ".join(s.text.strip() for s in segs)
    probs = [w.probability for s in segs for w in (s.words or [])]
    w, diffs = wer(norm(gerar.texto_tts(b)), norm(hyp))
    res[b["id"]] = {"wer": round(w, 3), "whisper": hyp, "diffs": diffs, "prob_min": round(min(probs or [0]), 2)}
    if (i + 1) % 20 == 0: print(f"[{i+1}/{len(gerar.BL)}]", flush=True)
json.dump(res, open("qa_whisper.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
bad = {k: v for k, v in res.items() if v["wer"] > 0.0}
print("blocos com diferenca:", len(bad), "WER medio", round(sum(v["wer"] for v in res.values()) / len(res), 4))
for k, v in sorted(bad.items()): print(k, v["wer"], v["diffs"])
