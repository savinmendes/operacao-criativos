# -*- coding: utf-8 -*-
"""Transcreve arquivos (faster-whisper large-v3 GPU, word_timestamps). Uso: python _transcrever.py saida.json a.mp3 b.mp4 ..."""
import sys, json
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\ferramentas\transcritor-youtube")
from lib.whisper_local import _registrar_dlls_cuda
_registrar_dlls_cuda()
from faster_whisper import WhisperModel

m = WhisperModel("large-v3", device="cuda", compute_type="float16")
res = {}
for f in sys.argv[2:]:
    segs, _ = m.transcribe(f, language="es", word_timestamps=True, beam_size=5)
    ws = [(w.word.strip(), round(w.start, 2), round(w.end, 2)) for s in segs for w in s.words]
    res[f] = ws
    print(f, "|", " ".join(f"{w}[{a}-{b}]" for w, a, b in ws))
json.dump(res, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
