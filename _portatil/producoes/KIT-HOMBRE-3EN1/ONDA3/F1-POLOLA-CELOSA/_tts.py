import json, base64, requests
from dotenv import dotenv_values
key = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
VOZ = "BPwS5yO6aXvwg8auqNwS"  # Damián
NORMAL = {"stability": 0.45, "similarity_boost": 0.8, "style": 0.3, "use_speaker_boost": True, "speed": 1.15}
NERV = {"stability": 0.3, "similarity_boost": 0.8, "style": 0.55, "use_speaker_boost": True, "speed": 1.0}
L = {"L2_nervioso": ("Eh... son tres... uno pa' cada momento.", NERV),
     "L3_oferta": ("Tres perfumes árabes al precio de uno.", NORMAL),
     "L4_dia": ("De día, Armaf Club. Fresco, masculino y poderoso.", NORMAL),
     "L5_noche": ("De noche, Lattafa Asad. Intenso, sofisticado y seductor.", NORMAL),
     "L6_finde": ("Y el finde, Afnan Nine PM. Elegante, moderno y refinado.", NORMAL),
     "L8_cta": ("Los tres te llegan a la casa y pagas cuando los recibes. ¡Pídelo ahora!", NORMAL)}
tot = 0
for n, (t, vs) in L.items():
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}/with-timestamps", headers={"xi-api-key": key},
        json={"text": t, "model_id": "eleven_multilingual_v2", "language_code": "es", "voice_settings": vs}, timeout=120)
    r.raise_for_status(); d = r.json()
    open(f"audio/{n}.mp3", "wb").write(base64.b64decode(d["audio_base64"]))
    json.dump(d["alignment"], open(f"audio/{n}.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
    tot += len(t); print(n, round(d["alignment"]["character_end_times_seconds"][-1], 2), r.headers.get("character-cost"))
print("chars", tot)
