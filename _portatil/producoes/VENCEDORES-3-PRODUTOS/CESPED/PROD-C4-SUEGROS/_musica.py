import requests
from dotenv import dotenv_values
K = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
KEY = K.get("ELEVENLABS_API_KEY") or [v for k, v in K.items() if "ELEVEN" in k.upper()][0]
r = requests.post("https://api.elevenlabs.io/v1/music", headers={"xi-api-key": KEY},
    json={"prompt": "Upbeat Chilean cumbia instrumental for a weekend family barbecue, playful light tension at the start then warm and festive, guiro, bass, accordion-like synth, no vocals", "music_length_ms": 42000, "force_instrumental": True}, timeout=600)
r.raise_for_status(); open("audio/trilha.mp3", "wb").write(r.content); print("ok", len(r.content))
