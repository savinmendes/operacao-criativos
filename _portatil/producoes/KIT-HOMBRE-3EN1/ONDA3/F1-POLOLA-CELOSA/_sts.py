"""Voz da namorada: isola a voz nativa do Seedance e passa as 2 falas (gancho e virada) para UMA voz feminina chilena."""
import requests, subprocess, sys
from dotenv import dotenv_values
key = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
H = {"xi-api-key": key}
VOZES = ["oJIuRMopN0sojGjwD6rQ", "uHo8F3FY11rc2LxCwDSB"]  # Camila (es-chilean, young); fallback: Chilena (conta)
for n in ["v1", "v2"]:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"takes/V{n[1]}_{'gancho' if n=='v1' else 'virada'}.mp4", "-vn", "-ac", "1", "-ar", "44100", f"audio/{n}_raw.wav"], check=True)
    r = requests.post("https://api.elevenlabs.io/v1/audio-isolation", headers=H, files={"audio": open(f"audio/{n}_raw.wav", "rb")}, timeout=300)
    r.raise_for_status(); open(f"audio/{n}_voz.mp3", "wb").write(r.content)
    for voz in VOZES:
        r = requests.post(f"https://api.elevenlabs.io/v1/speech-to-speech/{voz}", headers=H,
            files={"audio": open(f"audio/{n}_voz.mp3", "rb")},
            data={"model_id": "eleven_multilingual_sts_v2", "remove_background_noise": "false",
                  "voice_settings": '{"stability":0.5,"similarity_boost":0.85,"style":0.2}'}, timeout=300)
        if r.ok:
            open(f"audio/{n}_ella.mp3", "wb").write(r.content); print(n, "voz", voz); VOZES = [voz]; break
        print(n, voz, r.status_code, r.text[:200])
