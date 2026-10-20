import json, base64, requests, sys
from dotenv import dotenv_values
key = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
VOZ = "lLsDvdl6OjtZfLJPM2HA"  # Isa Pro (chilena)
L = {"L2_compra": "Así que le compré estos tres. Los pagué recién cuando llegaron… y se los envolví para regalo.",
     "L3_oferta": "Tres perfumes árabes al precio de uno.",
     "L4_armaf": "Armaf Club, fresco, masculino y poderoso.",
     "L5_asad": "Lattafa Asad, intenso y seductor.",
     "L6_9pm": "Y Afnan Nine PM, elegante y moderno.",
     "L7_virada": "Ahora la que no lo deja tranquilo soy yo.",
     "L8_cta": "Los tres te llegan a la casa y pagas cuando los recibes. ¡Pídelo ahora!"}
sel = sys.argv[1:] or list(L)
for n in sel:
    t = L[n]
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}/with-timestamps", headers={"xi-api-key": key},
        json={"text": t, "model_id": "eleven_multilingual_v2", "language_code": "es",
              "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True, "speed": 1.12}}, timeout=120)
    r.raise_for_status(); d = r.json()
    open(f"audio/{n}.mp3", "wb").write(base64.b64decode(d["audio_base64"]))
    json.dump(d["alignment"], open(f"audio/{n}.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
    print(n, round(d["alignment"]["character_end_times_seconds"][-1], 2), r.headers.get("character-cost"))
