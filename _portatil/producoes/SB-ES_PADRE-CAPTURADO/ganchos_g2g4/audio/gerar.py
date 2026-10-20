# -*- coding: utf-8 -*-
"""G2/G4: falas (Alejandro, eleven_v3) + SFX. Rodar de kit-edicao-criativos. Não regenera o que já existe."""
import sys, json, base64, requests
from pathlib import Path
sys.path.insert(0, "ferramentas")
import tts_elevenlabs as T
W = Path(__file__).resolve().parent
H = {"xi-api-key": T.chave(), "Content-Type": "application/json"}
VOZ = "sKgg4MPUDBy69X7iv3fA"
sfx = {
 "sfx_batidas": ("Heavy fists pounding violently and repeatedly on a thick wooden door from the outside, muffled men shouting indistinctly, heard from inside a small quiet stone room, tense, recorded on a phone", 7.0),
 "sfx_queda": ("A smartphone is roughly yanked off a tripod, quick plastic clatter and fumbling, the phone tumbles and hits a stone floor with a hard thud, recorded by the phone microphone", 2.5),
 "sfx_glitch": ("Digital video signal loss: harsh short glitch static burst and electronic stutter, then silence", 1.5),
}
for n, (p, d) in sfx.items():
    if (W / f"{n}.mp3").exists(): continue
    r = requests.post("https://api.elevenlabs.io/v1/sound-generation", headers=H, timeout=300,
                      json={"text": p, "duration_seconds": d, "prompt_influence": 0.5})
    if r.status_code != 200: raise SystemExit(f"sfx {r.status_code}: {r.text[:300]}")
    (W / f"{n}.mp3").write_bytes(r.content); print("ok", n)
txt = {
 "g2_voz": "[susurrando, aterrado] Si este video se corta... [susurrando] busquen al padre Juan Méndez. Él tiene la oración.",
 "g4_voz": "[rezando con devoción, voz firme] Oh poderoso San Benito, guardián de los arcanos sagrados.",
}
for n, t in txt.items():
    if (W / f"{n}.mp3").exists(): continue
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}/with-timestamps", params={"output_format": "mp3_44100_128"}, headers=H, timeout=300,
                      json={"text": t, "model_id": "eleven_v3", "language_code": "es", "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}})
    if r.status_code != 200: raise SystemExit(f"tts {n} {r.status_code}: {r.text[:300]}")
    j = r.json()
    (W / f"{n}.mp3").write_bytes(base64.b64decode(j["audio_base64"]))
    json.dump(j.get("alignment"), open(W / f"{n}.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
    print("ok", n, len(t))
