import requests
from dotenv import dotenv_values
key = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
r = requests.post("https://api.elevenlabs.io/v1/music", headers={"xi-api-key": key},
    json={"prompt": "Playful romantic Latin cumbia-pop instrumental, bright accordion and guira, bouncy bass, light synth plucks, cheeky funny feel-good energy of a young guy finding love, steady danceable groove, for a funny social media ad", "music_length_ms": 40000, "force_instrumental": True}, timeout=300)
print(r.status_code)
if r.ok: open("audio/trilha.mp3", "wb").write(r.content)
else: print(r.text[:500])
