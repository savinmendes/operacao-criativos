"""Corrige 'carninero'->'carnicero' e 'clientes'->'clientas' no áudio STS da selfie, colando as palavras do TTS Santiago."""
import json, base64, requests, subprocess
from dotenv import dotenv_values
key = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
VOZ = "VXZKNah1ssrzM8c81OiY"
txt = "Soy carnicero... y ahora las clientas vienen todos los días."
r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}/with-timestamps", headers={"xi-api-key": key},
    json={"text": txt, "model_id": "eleven_multilingual_v2", "language_code": "es",
          "voice_settings": {"stability": 0.5, "similarity_boost": 0.85, "style": 0.2, "use_speaker_boost": True}}, timeout=120)
r.raise_for_status(); d = r.json()
open("audio/_selfie_tts.mp3", "wb").write(base64.b64decode(d["audio_base64"]))
al = d["alignment"]; s = "".join(al["characters"])
def span(w):
    i = s.index(w); return al["character_start_times_seconds"][i], al["character_end_times_seconds"][i + len(w) - 1]
json.dump({"carnicero": span("carnicero"), "clientas": span("clientas")}, open("audio/_selfie_spans.json", "w"))
print(span("carnicero"), span("clientas"))
