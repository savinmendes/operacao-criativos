import os, requests
from dotenv import dotenv_values
K = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
key = K.get("ELEVENLABS_API_KEY") or K.get("ELEVEN_API_KEY") or K.get("XI_API_KEY")
r = requests.post("https://api.elevenlabs.io/v1/music", headers={"xi-api-key": key},
    json={"prompt": "Playful smooth Latin reggaeton instrumental, soft dembow beat, warm synth plucks, light marimba accents, cheeky confident nerd-turned-charmer comedic vibe, office comedy swagger, steady groove, for a funny social media ad", "music_length_ms": 40000, "force_instrumental": True}, timeout=300)
print(r.status_code, r.headers.get("content-type"), r.headers.get("character-cost") or r.headers.get("x-character-count"))
if r.ok: open("audio/trilha.mp3", "wb").write(r.content)
else: print(r.text[:500])
