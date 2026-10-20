# -*- coding: utf-8 -*-
"""TTS com previous/next text, usando a chave do kit via tts_elevenlabs.chave() (não imprime). Rodar de kit-edicao-criativos."""
import base64, json, sys
from pathlib import Path
import requests
sys.path.insert(0, "ferramentas")
import tts_elevenlabs as T
texto, saida, voz, prev, nxt = sys.argv[1:6]
r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voz}/with-timestamps", params={"output_format": "mp3_44100_128"},
                  headers={"xi-api-key": T.chave(), "Content-Type": "application/json"},
                  json={"text": texto, "model_id": "eleven_multilingual_v2", "previous_text": prev, "next_text": nxt,
                        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.0, "use_speaker_boost": True, "speed": 1.0}},
                  timeout=300)
if r.status_code != 200:
    raise SystemExit(f"ElevenLabs {r.status_code}: {r.text[:300]}")
d = r.json()
Path(saida).write_bytes(base64.b64decode(d["audio_base64"]))
Path(str(Path(saida).with_suffix("")) + ".alinhamento.json").write_text(json.dumps(d.get("normalized_alignment") or d["alignment"], ensure_ascii=False), encoding="utf-8")
print("ok", len(texto), "caracteres")
