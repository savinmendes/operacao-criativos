# -*- coding: utf-8 -*-
"""OCR por amostragem no video final: procura texto espanhol / EN VIVO. Uso: python qa_ocr.py final.mp4 passo_s"""
import sys, json, re, numpy as np
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\montagem\scripts")
from vslcomum import ler
from rapidocr_onnxruntime import RapidOCR
import subprocess
v = sys.argv[1]; passo = float(sys.argv[2])
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", v], capture_output=True, text=True).stdout)
ocr = RapidOCR()
ES = re.compile(r"\b(que|el|los|las|una|por|para|con|vivo|oraci[oó]n|dios|usted|tu|su|del|y|es|est[aá]|m[aá]s|como|pero|muy)\b|[áéíóúñ¿¡]", re.I)
res = []; flag = []
t = 1.0
while t < dur - 0.5:
    f = ler(v, t, 1)[0]
    r, _ = ocr(f)
    txt = [x[1] for x in (r or []) if x[2] > 0.6]
    s = " | ".join(txt)
    hit = [m.group(0) for m in ES.finditer(s)]
    res.append({"t": round(t, 1), "texto": s, "es": hit})
    if hit: flag.append(res[-1])
    t += passo
json.dump({"amostras": res, "suspeitos": flag}, open(v + ".ocr.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(len(res), "amostras;", len(flag), "suspeitas")
for x in flag: print(x)
