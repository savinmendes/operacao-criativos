# -*- coding: utf-8 -*-
"""TTS do sacerdote (Pa Gabriel, parametros do falas.json v1: est 0.5, estilo 0.25, vel 1.06) -> audio/<id>.mp3 + .alinhamento.json
Uso: python gerar_tts.py [ids...]"""
import sys, json
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import tts_elevenlabs as T
AQ = Path(__file__).resolve().parent; A = AQ / "audio"
VOZ = "Zkg9LlmGNlBWLgWjzTnu"; EST, ESTILO, VEL = 0.5, 0.25, 1.06
# texto = roteiro exato; tts = o que vai pro ElevenLabs (numeros por extenso)
B = json.loads((AQ / "blocos.json").read_text(encoding="utf-8"))
ids = sys.argv[1:]; tot = 0
for b in B:
    if ids and b["id"] not in ids: continue
    if not ids and (A / f"{b['id']}.mp3").exists(): continue
    T.gerar(b.get("tts", b["texto"]), str(A / f"{b['id']}.mp3"), VOZ, estabilidade=EST, estilo=ESTILO, velocidade=VEL)
    tot += len(b.get("tts", b["texto"])); print(b["id"], "ok", flush=True)
print("caracteres", tot, "US$", round(tot / 1000 * T.USD_POR_1000, 3))
