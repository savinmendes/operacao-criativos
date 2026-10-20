# -*- coding: utf-8 -*-
"""TTS com timestamps (v2 ou v3). Rodar de kit-edicao-criativos.  python tts.py <txt> <saida.mp3> <voz> <modelo> [estab] [prev] [next]"""
import base64, json, sys
from pathlib import Path
import requests
sys.path.insert(0, "ferramentas")
import tts_elevenlabs as T
txtf, saida, voz, modelo = sys.argv[1:5]
estab = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
texto = Path(txtf).read_text(encoding="utf-8").strip()
js = {"text": texto, "model_id": modelo,
      "voice_settings": {"stability": estab, "similarity_boost": 0.75, "style": 0.0, "use_speaker_boost": True, "speed": 1.0}}
if modelo != "eleven_v3":
    if len(sys.argv) > 6: js["previous_text"] = sys.argv[6]
    if len(sys.argv) > 7: js["next_text"] = sys.argv[7]
r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voz}/with-timestamps", params={"output_format": "mp3_44100_128"},
                  headers={"xi-api-key": T.chave(), "Content-Type": "application/json"}, json=js, timeout=300)
if r.status_code != 200:
    raise SystemExit(f"ElevenLabs {r.status_code}: {r.text[:400]}")
d = r.json()
Path(saida).write_bytes(base64.b64decode(d["audio_base64"]))
Path(str(Path(saida).with_suffix("")) + ".alinhamento.json").write_text(json.dumps(d.get("normalized_alignment") or d["alignment"], ensure_ascii=False), encoding="utf-8")
print("ok", len(texto), "caracteres")
