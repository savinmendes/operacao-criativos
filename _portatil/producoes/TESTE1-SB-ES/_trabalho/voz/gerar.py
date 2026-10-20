# -*- coding: utf-8 -*-
"""Gera as falas (ElevenLabs, tts_elevenlabs.gerar) -> voz/<id>.mp3 + .alinhamento.json. Uso: python voz/gerar.py [ids...]"""
import sys, json
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import tts_elevenlabs as T
AQ = Path(__file__).resolve().parent
F = json.loads((AQ / "falas.json").read_text(encoding="utf-8"))
ids = sys.argv[1:]
tot = 0
for f in F:
    if ids and f["id"] not in ids: continue
    if not ids and (AQ / f"{f['id']}.mp3").exists(): continue
    T.gerar(f["t"], str(AQ / f"{f['id']}.mp3"), f["voz"], estabilidade=f["est"], estilo=f["estilo"], velocidade=f["vel"])
    tot += len(f["t"]); print(f["id"], "ok", flush=True)
print("caracteres", tot, "≈ US$", round(tot / 1000 * T.USD_POR_1000, 3))
