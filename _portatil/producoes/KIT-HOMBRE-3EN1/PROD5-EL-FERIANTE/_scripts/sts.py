# selfie: extrai áudio -> audio-isolation -> STS Alejandro Duran (tempo original)
import subprocess, requests
from dotenv import dotenv_values
K = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
V = "sKgg4MPUDBy69X7iv3fA"
D = r"C:\Users\PICHAU\Downloads\KIT-HOMBRE-3EN1\PROD5-EL-FERIANTE"
raw, iso, out = D + r"\audio\v2_raw.wav", D + r"\audio\v2_voz.mp3", D + r"\audio\v2_alejandro.mp3"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", D + r"\takes\V2_selfie.mp4", "-vn", "-ac", "1", "-ar", "44100", raw], check=True)
r = requests.post("https://api.elevenlabs.io/v1/audio-isolation", headers={"xi-api-key": K}, files={"audio": open(raw, "rb")})
r.raise_for_status(); open(iso, "wb").write(r.content)
r = requests.post(f"https://api.elevenlabs.io/v1/speech-to-speech/{V}", headers={"xi-api-key": K},
                  data={"model_id": "eleven_multilingual_sts_v2", "remove_background_noise": "false",
                        "voice_settings": '{"stability":0.5,"similarity_boost":0.85,"style":0.3}'},
                  files={"audio": open(iso, "rb")})
r.raise_for_status(); open(out, "wb").write(r.content); print("ok")
