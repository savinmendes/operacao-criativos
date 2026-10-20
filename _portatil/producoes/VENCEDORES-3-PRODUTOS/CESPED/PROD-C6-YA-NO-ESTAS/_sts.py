import sys, subprocess, requests
from dotenv import dotenv_values
key = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
H = {"xi-api-key": key}
nome = sys.argv[1]  # ex.: V3_virada
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"takes/{nome}.mp4", "-vn", "-ac", "1", "-ar", "44100", f"audio/{nome}_raw.wav"], check=True)
r = requests.post("https://api.elevenlabs.io/v1/audio-isolation", headers=H, files={"audio": open(f"audio/{nome}_raw.wav", "rb")}, timeout=300)
r.raise_for_status(); open(f"audio/{nome}_voz.mp3", "wb").write(r.content)
r = requests.post("https://api.elevenlabs.io/v1/speech-to-speech/wfTWLJ20rcMqvU8gIiAB", headers=H,
    files={"audio": open(f"audio/{nome}_voz.mp3", "rb")},
    data={"model_id": "eleven_multilingual_sts_v2", "remove_background_noise": "false",
          "voice_settings": '{"stability":0.5,"similarity_boost":0.85,"style":0.2}'}, timeout=300)
r.raise_for_status(); open(f"audio/{nome}_salvatore.mp3", "wb").write(r.content); print("ok", nome)
