# -*- coding: utf-8 -*-
"""Whisper es (faster-whisper small, cpu int8) em arquivos e compara com o texto do roteiro.
Uso: python whisper_qa.py wav|take [ids...]  -> qa/<id>_<modo>_whisper.json + resumo"""
import sys, json, re, unicodedata, difflib
from pathlib import Path
from faster_whisper import WhisperModel
AQ = Path(__file__).resolve().parent; I = json.load(open(AQ / "audio" / "itens.json", encoding="utf-8"))
modo = sys.argv[1]; ids = sys.argv[2:] or list(I)
NUM = {"918": "novecientos dieciocho", "497": "cuatrocientos noventa y siete"}
def norm(s):
    for k, v in NUM.items(): s = s.replace(k, v)
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]", " ", s).split()
M = WhisperModel("medium", device="cpu", compute_type="int8")
for i in ids:
    it = I[i]
    if modo == "wav": f = AQ / ("audio/" + it["arquivo"] if it["avatar"] else it["arquivo"])
    else:
        if not it["avatar"]: continue
        f = next(iter(sorted(AQ.glob(f"take_{i}*.mp4"))), None)
        if f is None: continue
    segs, _ = M.transcribe(str(f), language="es", word_timestamps=True, beam_size=5)
    W = [dict(w=w.word.strip(), ini=round(w.start, 2), fim=round(w.end, 2)) for s in segs for w in s.words]
    txt = " ".join(w["w"] for w in W); a, b = norm(it["texto"]), norm(txt)
    r = difflib.SequenceMatcher(None, a, b).ratio()
    dif = [(op, " ".join(a[i1:i2]), " ".join(b[j1:j2])) for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes() if op != "equal"]
    json.dump(dict(arquivo=f.name, whisper=txt, palavras=W, ratio=round(r, 3), dif=dif), open(AQ / "qa" / f"{i}_{modo}_whisper.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(f"{i} {f.name} ratio={r:.3f} {'OK' if not dif else dif}\n   {txt}", flush=True)
