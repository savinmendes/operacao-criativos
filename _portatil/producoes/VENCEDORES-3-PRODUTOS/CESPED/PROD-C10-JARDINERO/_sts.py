import requests
from dotenv import dotenv_values
key = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
H = {"xi-api-key": key}
VOZ = "G4IAP30yc6c1gK0csDfu"  # WYZE Juan Carlos
for src, dst in (("V1_gancho", "gancho_jc"), ("V2_selfie", "selfie_jc")):
    r = requests.post("https://api.elevenlabs.io/v1/audio-isolation", headers=H, files={"audio": open(f"audio/{src}_raw.wav", "rb")}, timeout=300)
    r.raise_for_status(); open(f"audio/{src}_voz.mp3", "wb").write(r.content)
    r = requests.post(f"https://api.elevenlabs.io/v1/speech-to-speech/{VOZ}", headers=H,
        files={"audio": open(f"audio/{src}_voz.mp3", "rb")},
        data={"model_id": "eleven_multilingual_sts_v2", "remove_background_noise": "false",
              "voice_settings": '{"stability":0.5,"similarity_boost":0.85,"style":0.2}'}, timeout=300)
    r.raise_for_status(); open(f"audio/{dst}.mp3", "wb").write(r.content); print(dst, "ok")
