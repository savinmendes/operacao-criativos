# -*- coding: utf-8 -*-
"""TTS ElevenLabs com alinhamento. Rodar de kit-edicao-criativos.
uso: python tts.py <id> <voz> <modelo> "<texto>" [estab] [estilo] [prev] [next]"""
import base64, json, sys
from pathlib import Path
import requests
sys.path.insert(0, "ferramentas")
import tts_elevenlabs as T
OUT = Path(__file__).resolve().parent / "tts"
i, voz, modelo, texto = sys.argv[1:5]
est = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
sty = float(sys.argv[6]) if len(sys.argv) > 6 else 0.0
prev = sys.argv[7] if len(sys.argv) > 7 else None
nxt = sys.argv[8] if len(sys.argv) > 8 else None
body = {"text": texto, "model_id": modelo, "language_code": "es",
        "voice_settings": {"stability": est, "similarity_boost": 0.8, "style": sty, "use_speaker_boost": True}}
if modelo != "eleven_v3":
    body["previous_text"] = prev or None; body["next_text"] = nxt or None; body["voice_settings"]["speed"] = 1.0
r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voz}/with-timestamps", params={"output_format": "mp3_44100_128"},
                  headers={"xi-api-key": T.chave(), "Content-Type": "application/json"}, json=body, timeout=300)
if r.status_code != 200: raise SystemExit(f"ElevenLabs {r.status_code}: {r.text[:400]}")
d = r.json()
(OUT / f"{i}.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
(OUT / f"{i}.alinhamento.json").write_text(json.dumps(d.get("alignment"), ensure_ascii=False), encoding="utf-8")
with open(OUT / "caracteres.log", "a", encoding="utf-8") as f: f.write(f"{i}\t{voz}\t{modelo}\t{len(texto)}\n")
print("ok", i, len(texto), "car")
