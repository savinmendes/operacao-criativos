import requests
from dotenv import dotenv_values
K = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
KEY = K.get("ELEVENLABS_API_KEY") or [v for k, v in K.items() if "ELEVEN" in k.upper()][0]
r = requests.post("https://api.elevenlabs.io/v1/sound-generation", headers={"xi-api-key": KEY},
    json={"text": "smartphone chat message notification pop, short double ding, clean", "duration_seconds": 1.0, "prompt_influence": 0.6})
r.raise_for_status(); open("audio/sfx_msg.mp3", "wb").write(r.content); print("ok")
