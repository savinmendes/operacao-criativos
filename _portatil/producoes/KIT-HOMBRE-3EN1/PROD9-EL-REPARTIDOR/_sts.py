import requests
from dotenv import dotenv_values
key = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
H = {"xi-api-key": key}
r = requests.post("https://api.elevenlabs.io/v1/audio-isolation", headers=H, files={"audio": open("audio/v2_raw.wav", "rb")}, timeout=300)
r.raise_for_status(); open("audio/v2_voz.mp3", "wb").write(r.content)
r = requests.post("https://api.elevenlabs.io/v1/speech-to-speech/6xnxeygeMfFgAqKpWy1A", headers=H,
    files={"audio": open("audio/v2_voz.mp3", "rb")},
    data={"model_id": "eleven_multilingual_sts_v2", "remove_background_noise": "false",
          "voice_settings": '{"stability":0.5,"similarity_boost":0.85,"style":0.2}'}, timeout=300)
r.raise_for_status(); open("audio/v2_aiden.mp3", "wb").write(r.content); print("ok")
