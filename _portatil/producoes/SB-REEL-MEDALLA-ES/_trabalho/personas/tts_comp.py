# -*- coding: utf-8 -*-
"""Gera hook (firme) e selfie (triste) de uma persona da série COMPLETA via app/tts_ctx.py. Uso: python tts_comp.py <slug> <voice_id> [hook|selfie ...]"""
import subprocess, sys, time
from pathlib import Path
slug, voz = sys.argv[1:3]
quais = sys.argv[3:] or ["hook", "selfie"]
P = Path(__file__).resolve().parent / slug / "completa"
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
CTX = Path(__file__).resolve().parent.parent / "app" / "tts_ctx.py"
PREV = {"hook": "Lo dijo con voz firme, mirando a la cámara, como quien cuenta algo que le cambió la vida:",
        "selfie": "Habló despacio, con la voz quebrada y triste, conteniendo el llanto:"}
NEXT = {"hook": "", "selfie": ""}
for q in quais:
    txt = (P / f"{q}.txt").read_text(encoding="utf-8").strip()
    subprocess.run([sys.executable, str(CTX), txt, str(P / f"{q}.mp3"), voz, PREV[q], NEXT[q]], cwd=KIT, check=True)
    with open(Path(__file__).resolve().parent / "_c" / "caracteres.log", "a", encoding="utf-8") as f:
        f.write(f"{slug}\tcompleta_{q}\t{len(txt)}\t{time.strftime('%H:%M')}\n")
