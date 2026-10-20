import requests
from dotenv import dotenv_values
key = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
r = requests.post("https://api.elevenlabs.io/v1/music", headers={"xi-api-key": key},
    json={"prompt": "Light comedic Chilean cumbia instrumental, starts with a few seconds of playful suspense (pizzicato strings and a ticking güiro), then opens into an upbeat sunny cumbia groove with accordion, bass, timbales and güiro, neighborhood feel-good vibe, for a funny social media ad", "music_length_ms": 42000, "force_instrumental": True}, timeout=300)
print(r.status_code)
if r.ok: open("audio/trilha.mp3", "wb").write(r.content)
else: print(r.text[:500])
