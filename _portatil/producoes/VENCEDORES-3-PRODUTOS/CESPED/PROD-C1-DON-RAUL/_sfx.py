import requests
from dotenv import dotenv_values
key = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
r = requests.post("https://api.elevenlabs.io/v1/sound-generation", headers={"xi-api-key": key},
    json={"text": "Single short smartphone chat message notification pop sound with a quick phone vibration buzz", "duration_seconds": 1.0, "prompt_influence": 0.6}, timeout=120)
print(r.status_code); open("audio/sfx_msg.mp3", "wb").write(r.content) if r.ok else print(r.text[:300])
