import requests
from dotenv import dotenv_values
key = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
r = requests.post("https://api.elevenlabs.io/v1/music", headers={"xi-api-key": key},
    json={"prompt": "Smooth sensual Latin R&B and soft reggaeton instrumental, warm night date mood, romantic but confident, mellow plucked guitar, soft synth pads, gentle dembow groove, finger snaps, building slightly toward the end, for a cheeky social media ad", "music_length_ms": 40000, "force_instrumental": True}, timeout=300)
print(r.status_code, r.headers.get("character-cost"))
if r.ok: open("audio/trilha.mp3", "wb").write(r.content)
else: print(r.text[:500])
