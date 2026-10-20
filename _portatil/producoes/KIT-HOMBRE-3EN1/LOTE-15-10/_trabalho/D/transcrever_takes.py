# -*- coding: utf-8 -*-
"""Transcreve takes (faster-whisper CPU int8, tempo por palavra) -> qa/<take>_transcricao.txt
python transcrever_takes.py takes/s_t1.mp4 takes/s_t2.mp4 ..."""
import sys
from pathlib import Path
from faster_whisper import WhisperModel

m = WhisperModel("medium", device="cpu", compute_type="int8")
for f in sys.argv[1:]:
    segs, _ = m.transcribe(f, language="es", word_timestamps=True, vad_filter=False, beam_size=5)
    linhas = []
    for s in segs:
        linhas.append(f"[{s.start:.2f}-{s.end:.2f}] {s.text.strip()}")
        for w in s.words:
            linhas.append(f"    {w.start:6.2f} {w.end:6.2f} {w.word.strip()}")
    out = Path(__file__).parent / "qa" / (Path(f).stem + "_transcricao.txt")
    out.write_text("\n".join(linhas), encoding="utf-8")
    print("==", f)
    print("\n".join(linhas))
