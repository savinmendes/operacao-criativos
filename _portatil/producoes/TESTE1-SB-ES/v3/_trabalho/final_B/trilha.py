# -*- coding: utf-8 -*-
"""Trilha do B04-B06 via ElevenLabs Sound Effects (/v1/sound-generation). Mede créditos antes/depois.
Uso: python trilha.py  -> trilha/triste_*.mp3, trilha/esperanca_*.mp3, trilha/custo.json"""
import json, sys, urllib.request
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import chave
AQ = Path(__file__).resolve().parent / "trilha"; AQ.mkdir(exist_ok=True)
def req(url, body=None):
    r = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, method="POST" if body else "GET",
                               headers={"xi-api-key": chave(), "Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=180) as f: return f.read()
def uso(): return json.loads(req("https://api.elevenlabs.io/v1/user/subscription"))
PEDIDOS = [
  ("triste_1", 5.0, "Sad melancholic solo piano melody, slow, soft sustained strings underneath, emotional cinematic underscore, minor key, no drums, no vocals"),
  ("triste_2", 5.0, "Lonely emotional piano and cello, slow sad cinematic music cue, minor key, gentle, no percussion, no voices"),
  ("esperanca_1", 8.0, "Gentle hopeful cinematic piano with warm strings rising, uplifting, major key, slow build, no drums, no vocals"),
]
if __name__ == "__main__":
    a = uso(); log = dict(antes=dict(usados=a.get("character_count"), limite=a.get("character_limit")), itens=[])
    for nome, d, txt in PEDIDOS:
        if (AQ / f"{nome}.mp3").exists(): continue
        b = req("https://api.elevenlabs.io/v1/sound-generation", dict(text=txt, duration_seconds=d, prompt_influence=0.5))
        (AQ / f"{nome}.mp3").write_bytes(b); log["itens"].append(dict(nome=nome, dur=d, prompt=txt)); print("ok", nome, len(b))
    z = uso(); log["depois"] = dict(usados=z.get("character_count"), limite=z.get("character_limit"))
    log["creditos_gastos"] = (z.get("character_count") or 0) - (a.get("character_count") or 0)
    (AQ / "custo.json").write_text(json.dumps(log, indent=1, ensure_ascii=False), encoding="utf-8"); print(log["creditos_gastos"], "créditos")
