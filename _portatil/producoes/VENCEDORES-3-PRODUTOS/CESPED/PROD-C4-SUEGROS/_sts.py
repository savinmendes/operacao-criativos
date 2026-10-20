# -*- coding: utf-8 -*-
"""uso: python _sts.py takes/V1_gancho.mp4 audio/v1_gerardo.mp3  -> isola a voz e passa por STS (Gerardo), mesmo tempo"""
import sys, subprocess, requests
from dotenv import dotenv_values
K = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
KEY = K.get("ELEVENLABS_API_KEY") or [v for k, v in K.items() if "ELEVEN" in k.upper()][0]
VOZ = "NDcVpQJv7Naa7ZKrqtEk"
src, dst = sys.argv[1], sys.argv[2]
raw = dst.rsplit(".", 1)[0] + "_raw.wav"; iso = dst.rsplit(".", 1)[0] + "_iso.mp3"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "44100", raw], check=True)
r = requests.post("https://api.elevenlabs.io/v1/audio-isolation", headers={"xi-api-key": KEY}, files={"audio": open(raw, "rb")}, timeout=300)
r.raise_for_status(); open(iso, "wb").write(r.content)
r = requests.post(f"https://api.elevenlabs.io/v1/speech-to-speech/{VOZ}", headers={"xi-api-key": KEY},
                  data={"model_id": "eleven_multilingual_sts_v2", "remove_background_noise": "true",
                        "voice_settings": '{"stability":0.5,"similarity_boost":0.85,"style":0.2}'},
                  files={"audio": open(iso, "rb")}, timeout=300)
r.raise_for_status(); open(dst, "wb").write(r.content); print("ok", dst)
