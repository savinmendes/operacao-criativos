# -*- coding: utf-8 -*-
"""TTS ElevenLabs (multilingual v2) com previous/next text e alinhamento. Rodar de kit-edicao-criativos.
uso: python tts_es.py <id> <voz> "<texto>" "<prev>" "<next>" [estab] [estilo]"""
import base64, json, sys
from pathlib import Path
import requests
sys.path.insert(0, "ferramentas")
import tts_elevenlabs as T
OUT = Path(__file__).resolve().parent / "tts"
i, voz, texto, prev, nxt = sys.argv[1:6]
est = float(sys.argv[6]) if len(sys.argv) > 6 else 0.5
sty = float(sys.argv[7]) if len(sys.argv) > 7 else 0.0
r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voz}/with-timestamps", params={"output_format": "mp3_44100_128"},
                  headers={"xi-api-key": T.chave(), "Content-Type": "application/json"},
                  json={"text": texto, "model_id": "eleven_multilingual_v2", "language_code": "es", "previous_text": prev or None, "next_text": nxt or None,
                        "voice_settings": {"stability": est, "similarity_boost": 0.8, "style": sty, "use_speaker_boost": True, "speed": 1.0}},
                  timeout=300)
if r.status_code != 200:
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voz}/with-timestamps", params={"output_format": "mp3_44100_128"},
                  headers={"xi-api-key": T.chave(), "Content-Type": "application/json"},
                  json={"text": texto, "model_id": "eleven_multilingual_v2", "previous_text": prev or None, "next_text": nxt or None,
                        "voice_settings": {"stability": est, "similarity_boost": 0.8, "style": sty, "use_speaker_boost": True, "speed": 1.0}}, timeout=300)
    if r.status_code != 200:
        raise SystemExit(f"ElevenLabs {r.status_code}: {r.text[:300]}")
d = r.json()
(OUT / f"{i}.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
(OUT / f"{i}.alinhamento.json").write_text(json.dumps(d.get("alignment"), ensure_ascii=False), encoding="utf-8")
with open(OUT / "caracteres.log", "a", encoding="utf-8") as f: f.write(f"{i}\t{voz}\t{len(texto)}\n")
print("ok", i, len(texto), "car")
