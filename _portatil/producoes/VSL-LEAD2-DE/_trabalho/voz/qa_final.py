import gpu, json, numpy as np, difflib, re
from faster_whisper import WhisperModel
from qa_whisper import norm
A = json.load(open("alinhamento_de.json", encoding="utf-8"))["palavras"]
m = WhisperModel("medium", device="cuda", compute_type="float16")
segs, _ = m.transcribe("narracao_de_completa.wav", language="de", beam_size=5, word_timestamps=True, vad_filter=True, condition_on_previous_text=False)
W = [w for s in segs for w in s.words]
json.dump([[w.word, w.start, w.end] for w in W], open("whisper_final.json", "w", encoding="utf-8"), ensure_ascii=False)
ref = []; rt = []
for a in A:
    for t in norm(a["palavra"]): ref.append(t); rt.append(a["ini"])
hyp = []; ht = []
for w in W:
    for t in norm(w.word): hyp.append(t); ht.append(w.start)
sm = difflib.SequenceMatcher(None, ref, hyp, autojunk=False)
err = 0; off = []; dif = []
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op == "equal": off += [ht[j1 + k] - rt[i1 + k] for k in range(i2 - i1)]
    else:
        err += max(i2 - i1, j2 - j1); dif.append((round(rt[i1] if i1 < len(rt) else -1, 1), " ".join(ref[i1:i2]), " ".join(hyp[j1:j2])))
off = np.array(off)
print("palavras ref", len(ref), "whisper", len(hyp), "WER %.3f" % (err / len(ref)))
print("offset whisper-alinhamento: mediana %.3f s, p95 abs %.3f s" % (np.median(off), np.percentile(np.abs(off), 95)))
json.dump(dif, open("qa_final_diffs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("diferencas", len(dif))
