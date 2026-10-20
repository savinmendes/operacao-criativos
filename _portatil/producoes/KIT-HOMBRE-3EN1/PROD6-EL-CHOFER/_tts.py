# -*- coding: utf-8 -*-
import json, base64, os, sys, requests
from pathlib import Path
from dotenv import dotenv_values
K = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
KEY = next(v for k, v in K.items() if "ELEVEN" in k.upper())
H = {"xi-api-key": KEY}
VOZ = "tomkxGQGz4b1kE0EM722"
AU = Path(__file__).parent / "audio"
L = {
 "L4_oferta": "Tres perfumes árabes al precio de uno.",
 "L5_dia": "En el día, Armaf Club. Fresco, masculino y poderoso. Me piden que dé otra vuelta.",
 "L6_noche": "En la noche, Lattafa Asad. Intenso y seductor. Mi señora me espera despierta.",
 "L7_finde": "Y el fin de semana, Afnan Nine PM. Elegante y moderno.",
 "L8_cta": "Los tres te llegan a la casa y pagas cuando los recibes. ¡Pídelo ahora!",
}
which = sys.argv[1:] or list(L)
for n in which:
    if n == "trilha":
        r = requests.post("https://api.elevenlabs.io/v1/music", headers=H, json={
            "prompt": "Upbeat modern Chilean cumbia instrumental, festive and playful, guacharaca, bass, bright synth accordion lead, steady danceable groove, background music for a funny commercial, no vocals",
            "music_length_ms": 40000, "force_instrumental": True}, timeout=300)
        r.raise_for_status(); (AU / "trilha.mp3").write_bytes(r.content); print("trilha ok", len(r.content)); continue
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}/with-timestamps", headers=H, json={
        "text": L[n], "model_id": "eleven_multilingual_v2", "language_code": "es",
        "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.3, "use_speaker_boost": True}}, timeout=120)
    r.raise_for_status(); d = r.json()
    (AU / f"{n}.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
    json.dump(d["alignment"], open(AU / f"{n}.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
    print(n, "ok", d["alignment"]["character_end_times_seconds"][-1])
