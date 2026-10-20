# -*- coding: utf-8 -*-
"""Lista as vozes da conta ElevenLabs (nome, id, gênero, sotaque, idioma). Não imprime a chave."""
import sys
import requests
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import chave  # noqa: E402

r = requests.get("https://api.elevenlabs.io/v2/voices", params={"page_size": 100},
                 headers={"xi-api-key": chave()}, timeout=60)
r.raise_for_status()
for v in r.json()["voices"]:
    lb = v.get("labels") or {}
    print(f'{v["voice_id"]} | {v["name"][:40]:40} | {v.get("category")} | {lb.get("gender","")} | {lb.get("accent","")} | {lb.get("language","")} | {lb.get("age","")}')
