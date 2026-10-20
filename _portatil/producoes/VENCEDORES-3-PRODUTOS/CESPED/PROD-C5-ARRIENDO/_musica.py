import requests
from dotenv import dotenv_values
key = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
r = requests.post("https://api.elevenlabs.io/v1/music", headers={"xi-api-key": key},
    json={"prompt": "Warm uplifting Latin acoustic pop instrumental, starts slightly melancholic and tense with soft piano and nylon guitar, then turns hopeful and bright with light percussion, claps and cajón, feel-good home makeover vibe, steady groove, for a social media ad", "music_length_ms": 40000, "force_instrumental": True}, timeout=300)
print(r.status_code, r.headers.get("character-cost"))
if r.ok: open("audio/trilha.mp3", "wb").write(r.content)
else: print(r.text[:500])
