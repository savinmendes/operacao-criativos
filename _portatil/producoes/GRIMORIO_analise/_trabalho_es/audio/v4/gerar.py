# -*- coding: utf-8 -*-
"""v4 do grito: ambiente de igreja em tumulto (SFX) + 3 tomadas do grito no eleven_v3. Rodar de kit-edicao-criativos."""
import sys, json, requests
from pathlib import Path
sys.path.insert(0, "ferramentas")
import tts_elevenlabs as T
W = Path(__file__).resolve().parent
H = {"xi-api-key": T.chave(), "Content-Type": "application/json"}
VOZ = "sKgg4MPUDBy69X7iv3fA"  # Alejandro Duran = mesma voz do padre chorando (linhas 03-05)
sfx = {
 "amb_a": "Inside a large crowded Catholic church, chaotic commotion: dozens of people gasping and murmuring in alarm, women shouting indistinctly in Spanish, a scuffle with shuffling feet and wooden pews creaking, big echoing church reverb, handheld phone recording",
 "amb_b": "Panicked congregation inside a reverberant church while security guards drag a priest out, crowd booing and protesting, people yelling 'no' in Spanish, footsteps and pushing, tense, recorded on a phone",
}
for n, p in sfx.items():
    if (W / f"{n}.mp3").exists(): continue
    r = requests.post("https://api.elevenlabs.io/v1/sound-generation", headers=H, timeout=300,
                      json={"text": p, "duration_seconds": 9.0, "prompt_influence": 0.5})
    if r.status_code != 200: raise SystemExit(f"sfx {r.status_code}: {r.text[:300]}")
    (W / f"{n}.mp3").write_bytes(r.content); print("ok", n)
txt = {
 "g1": "[gritando, desesperado] ¡Graben! ¡GRABEN! [gritando con rabia] ¡No quieren que el pueblo prospere!",
 "g2": "[shouting desperately] ¡Graben! [shouting] ¡No quieren que el pueblo prospere!",
 "g3": "[grita con la voz quebrada] ¡Graben, graben! ¡No quieren que el pueblo prospere!",
}
for n, t in txt.items():
    if (W / f"{n}.mp3").exists(): continue
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}", params={"output_format": "mp3_44100_128"}, headers=H, timeout=300,
                      json={"text": t, "model_id": "eleven_v3", "language_code": "es", "voice_settings": {"stability": 0.0, "similarity_boost": 0.8}})
    if r.status_code != 200: raise SystemExit(f"tts {n} {r.status_code}: {r.text[:300]}")
    (W / f"{n}.mp3").write_bytes(r.content); print("ok", n, len(t))
