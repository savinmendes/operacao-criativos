import requests
from dotenv import dotenv_values
K = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
r = requests.post("https://api.elevenlabs.io/v1/music", headers={"xi-api-key": K}, json={
  "prompt": "Upbeat playful Chilean cumbia instrumental, festive street market vibe, guiro, congas, bright accordion and bass, cheeky fun groove, steady 100 bpm, good for a funny ad background, no vocals",
  "music_length_ms": 40000, "force_instrumental": True})
print(r.status_code, r.headers.get("content-type"))
if r.ok: open(r"C:\Users\PICHAU\Downloads\KIT-HOMBRE-3EN1\PROD5-EL-FERIANTE\audio\trilha.mp3","wb").write(r.content)
else: print(r.text[:500])
