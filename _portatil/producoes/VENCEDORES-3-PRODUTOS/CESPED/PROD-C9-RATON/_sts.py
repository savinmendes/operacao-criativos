import sys, subprocess, requests
from dotenv import dotenv_values
key = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
H = {"xi-api-key": key}
VOZ = "prblQcKOdF08ozhxP2mk"  # Andrea Rabbit (chilena)
src, nome = sys.argv[1], sys.argv[2]   # ex.: takes/V1_gancho.mp4 v1
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "44100", f"audio/{nome}_raw.wav"], check=True)
r = requests.post("https://api.elevenlabs.io/v1/audio-isolation", headers=H, files={"audio": open(f"audio/{nome}_raw.wav", "rb")}, timeout=300)
r.raise_for_status(); open(f"audio/{nome}_voz.mp3", "wb").write(r.content)
r = requests.post(f"https://api.elevenlabs.io/v1/speech-to-speech/{VOZ}", headers=H,
    files={"audio": open(f"audio/{nome}_voz.mp3", "rb")},
    data={"model_id": "eleven_multilingual_sts_v2", "remove_background_noise": "false",
          "voice_settings": '{"stability":0.5,"similarity_boost":0.85,"style":0.2}'}, timeout=300)
r.raise_for_status(); open(f"audio/{nome}_andrea.mp3", "wb").write(r.content); print("ok", nome)
