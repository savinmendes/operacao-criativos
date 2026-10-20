import requests, subprocess, sys
from pathlib import Path
from dotenv import dotenv_values
K = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
KEY = next(v for k, v in K.items() if "ELEVEN" in k.upper()); H = {"xi-api-key": KEY}
VOZ = "tomkxGQGz4b1kE0EM722"; AU = Path("audio"); src, nome = sys.argv[1], sys.argv[2]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "44100", str(AU / f"{nome}_raw.wav")], check=True)
r = requests.post("https://api.elevenlabs.io/v1/audio-isolation", headers=H, files={"audio": open(AU / f"{nome}_raw.wav", "rb")}, timeout=300); r.raise_for_status()
(AU / f"{nome}_voz.mp3").write_bytes(r.content)
r = requests.post(f"https://api.elevenlabs.io/v1/speech-to-speech/{VOZ}", headers=H, files={"audio": open(AU / f"{nome}_voz.mp3", "rb")},
                  data={"model_id": "eleven_multilingual_sts_v2", "remove_background_noise": "true"}, timeout=300); r.raise_for_status()
(AU / f"{nome}_mario.mp3").write_bytes(r.content); print("ok", len(r.content))
