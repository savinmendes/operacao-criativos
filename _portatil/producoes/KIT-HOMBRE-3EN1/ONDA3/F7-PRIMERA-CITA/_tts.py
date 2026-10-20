import json, base64, requests
from dotenv import dotenv_values
key = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
VOZ = "i4Kar2uamCWyas8TAu31"  # Adán
L = {"L2_noche": "Esa noche usé el Lattafa Asad. Intenso, sofisticado y seductor.",
     "L3_oferta": "Tres perfumes árabes al precio de uno.",
     "L4_semana": "Y los otros dos, para el resto de la semana: Armaf Club, fresco y masculino… y Afnan Nine PM, elegante y moderno.",
     "L5_virada": "Ni pedimos el postre… salimos de la mano.",
     "L6_cta": "Los tres te llegan a la casa, y pagas cuando los recibes. ¡Pídelo ahora!"}
tot = 0
for n, t in L.items():
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}/with-timestamps", headers={"xi-api-key": key},
        json={"text": t, "model_id": "eleven_multilingual_v2", "language_code": "es",
              "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.3, "use_speaker_boost": True}}, timeout=120)
    r.raise_for_status(); d = r.json()
    open(f"audio/{n}.mp3", "wb").write(base64.b64decode(d["audio_base64"]))
    json.dump(d["alignment"], open(f"audio/{n}.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
    tot += len(t); print(n, round(d["alignment"]["character_end_times_seconds"][-1], 2), r.headers.get("character-cost"))
print("chars", tot)
