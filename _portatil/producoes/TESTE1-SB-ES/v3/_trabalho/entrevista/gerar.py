# -*- coding: utf-8 -*-
"""TTS ElevenLabs das falas -> audio/<id>.mp3 + .alinhamento.json. Uso: python gerar.py [ids]"""
import sys, json
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import tts_elevenlabs as T
AQ = Path(__file__).resolve().parent; (AQ / "audio").mkdir(exist_ok=True)
ids = sys.argv[1:]; tot = 0
for f in json.loads((AQ / "falas.json").read_text(encoding="utf-8")):
    if ids and f["id"] not in ids: continue
    T.gerar(f["t"], str(AQ / "audio" / f"{f['id']}.mp3"), f["voz"], estabilidade=f["est"], estilo=f["estilo"], velocidade=f["vel"])
    tot += len(f["t"]); print(f["id"], "ok", flush=True)
print("caracteres", tot, "US$", round(tot / 1000 * T.USD_POR_1000, 3))
