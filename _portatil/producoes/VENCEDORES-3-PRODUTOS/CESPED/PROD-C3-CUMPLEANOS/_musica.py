import requests
from dotenv import dotenv_values
key = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
r = requests.post("https://api.elevenlabs.io/v1/music", headers={"xi-api-key": key},
    json={"prompt": "Instrumental pop rock for a family social media ad: starts tense and anxious for 10 seconds (ticking pulse, muted guitar, low synth), then turns bright, warm and joyful like a kids birthday party (upbeat acoustic guitar strum, claps, light drums, cheerful glockenspiel), steady groove, no vocals", "music_length_ms": 40000, "force_instrumental": True}, timeout=300)
print(r.status_code)
if r.ok: open("audio/trilha.mp3", "wb").write(r.content)
else: print(r.text[:500])
