# -*- coding: utf-8 -*-
"""Revisão (ad18/ad30): whisper es + termos proibidos + folha de contato 1/2 s.  python rev_ad.py video.mp4 pasta"""
import re, subprocess, sys, tempfile
from pathlib import Path
from faster_whisper import WhisperModel
v = Path(sys.argv[1]); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
wav = Path(tempfile.mkdtemp()) / "a.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(v), "-vn", "-ac", "1", "-ar", "16000", str(wav)], check=True)
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
segs, _ = m.transcribe(str(wav), language="es")
txt = "\n".join(f"[{s.start:7.2f}-{s.end:7.2f}] {s.text.strip()}" for s in segs)
(out / (v.stem + "_transc.txt")).write_text(txt, encoding="utf-8")
pat = r"maya ?verra|mayaverra|emporio|herbal|sesenta d|60 d[ií]as|hecho en|estados unidos|ozempic|tiktok|cofepris|c[aá]ncer|precio|\$|link|70 ?%|descuento|treinta d|30 d[ií]as|45 d[ií]as"
hits = [l for l in txt.splitlines() if re.search(pat, l, re.I)]
print("TERMOS:", hits if hits else "nenhum")
subprocess.run([sys.executable, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas\folhas_contato.py",
                "--cada", "2", "--colunas", "14", "--largura", "120", "--saida", str(out), str(v)], check=True, capture_output=True)
