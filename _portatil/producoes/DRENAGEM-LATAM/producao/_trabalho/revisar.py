# -*- coding: utf-8 -*-
"""Revisão: whisper (es, vad off) no vídeo final + busca de termos proibidos + folha de contato (1 quadro/2 s)."""
import json, re, subprocess, sys, tempfile, unicodedata
from pathlib import Path
from faster_whisper import WhisperModel
K = r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas\folhas_contato.py"
TERMOS = ["maya", "verra", "mayaverra", "sesenta", "60", "hecho en", "estados unidos", "ozempic", "tiktok", "tik tok",
          "cofepris", "cancer", "precio", "dolar", "dolares", "usd", "link", "45 dias", "30 dias", "treinta", "garantia"]
def norm(s): return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
for v in sys.argv[1:]:
    v = Path(v); out = v.with_name(v.stem + "_revisao.txt")
    wav = Path(tempfile.mkdtemp()) / "a.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(v), "-vn", "-ac", "1", "-ar", "16000", str(wav)], check=True)
    segs, _ = m.transcribe(str(wav), language="es", vad_filter=False, condition_on_previous_text=False)
    linhas = [f"{s.start:7.1f} {s.text.strip()}" for s in segs]
    achados = [l for l in linhas if any(re.search(r"\b" + re.escape(t) + r"\b", norm(l)) for t in TERMOS)]
    out.write_text("\n".join(linhas) + "\n\n=== ACHADOS ===\n" + "\n".join(achados), encoding="utf-8")
    subprocess.run([sys.executable, K, "--cada", "2", "--colunas", "15", "--largura", "120", "--saida", str(v.parent / "_revisao"), str(v)], check=True,
                   stdout=subprocess.DEVNULL)
    print(v.name, "| achados:", len(achados)); [print("   ", a) for a in achados]
