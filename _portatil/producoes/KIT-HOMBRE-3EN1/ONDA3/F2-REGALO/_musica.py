import requests
from dotenv import dotenv_values
key = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
r = requests.post("https://api.elevenlabs.io/v1/music", headers={"xi-api-key": key},
    json={"prompt": "Flirty playful latin R&B pop instrumental, smooth bass, finger snaps, soft Rhodes keys and a sly muted trumpet hook, mischievous romantic vibe, light dembow-free groove at 95 bpm, for a cheeky social media ad", "music_length_ms": 40000, "force_instrumental": True}, timeout=300)
print(r.status_code)
if r.ok: open("audio/trilha.mp3", "wb").write(r.content)
else: print(r.text[:500])
