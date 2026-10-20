import json, base64, requests
from dotenv import dotenv_values
key = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
VOZ = "aI9919Z6KR2NIkiqeIWg"
L = {"L4_oferta": "Tres perfumes árabes al precio de uno.",
     "L5_dia": "En el día, Armaf Club. Fresco, masculino y poderoso. En la plaza ya me dicen el galán.",
     "L6_noche": "En la noche, Lattafa Asad. Intenso y seductor. Mi señora se puso celosa... y cariñosa.",
     "L7_finde": "Y el fin de semana, Afnan Nine PM. Elegante y moderno.",
     "L8_cta": "Los tres te llegan a la casa y pagas cuando los recibes. ¡Pídelo ahora!"}
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
