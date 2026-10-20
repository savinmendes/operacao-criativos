import json, base64, requests, sys
from dotenv import dotenv_values
key = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
VOZ = "JjHBC66wF58p4ogebCNA"  # Eduardo
L = {"L2_entrega": "Pedí los tres, y al otro día ya estaban en la casa.",
     "L3_unbox": "Revisé los tres: Armaf, fresco y masculino; Asad, intenso y seductor; y el Afnan Nine PM, elegante. ¡Ahí recién pagué!",
     "L4_oferta": "Tres perfumes árabes al precio de uno.",
     "L6_cta": "Pagas cuando te llega, y el envío es en 24 horas. ¡Pídelo ahora!"}
sel = sys.argv[1:] or list(L)
for n in sel:
    t = L[n]
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}/with-timestamps", headers={"xi-api-key": key},
        json={"text": t, "model_id": "eleven_multilingual_v2", "language_code": "es",
              "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.3, "use_speaker_boost": True, "speed": 1.15}}, timeout=120)
    r.raise_for_status(); d = r.json()
    open(f"audio/{n}.mp3", "wb").write(base64.b64decode(d["audio_base64"]))
    json.dump(d["alignment"], open(f"audio/{n}.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
    print(n, round(d["alignment"]["character_end_times_seconds"][-1], 2), r.headers.get("character-cost"))
