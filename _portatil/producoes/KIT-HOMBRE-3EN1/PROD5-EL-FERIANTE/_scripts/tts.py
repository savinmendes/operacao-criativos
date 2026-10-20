# -*- coding: utf-8 -*-
import json, base64, os, sys, requests
from dotenv import dotenv_values
K = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
V = "sKgg4MPUDBy69X7iv3fA"
AU = r"C:\Users\PICHAU\Downloads\KIT-HOMBRE-3EN1\PROD5-EL-FERIANTE\audio"
L = {
 "L4_oferta": "Tres perfumes árabes al precio de uno.",
 "L5_dia": "En el día, Armaf Club. Fresco, masculino y poderoso. Las caseras ya no regatean.",
 "L6_noche": "En la noche, Lattafa Asad. Intenso y seductor. Mi señora me dice \"casero\" a mí ahora.",
 "L7_finde": "Y el fin de semana, Afnan Nine PM. Elegante y moderno.",
 "L8_cta": "Los tres te llegan a la casa y pagas cuando los recibes. ¡Pídelo ahora!",
}
sel = sys.argv[1:] or list(L)
for n in sel:
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{V}/with-timestamps", headers={"xi-api-key": K},
        json={"text": L[n], "model_id": "eleven_multilingual_v2", "language_code": "es",
              "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True}})
    r.raise_for_status(); d = r.json()
    open(os.path.join(AU, n + ".mp3"), "wb").write(base64.b64decode(d["audio_base64"]))
    json.dump(d["alignment"], open(os.path.join(AU, n + ".alinhamento.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print(n, "ok", round(d["alignment"]["character_end_times_seconds"][-1], 2), "s", r.headers.get("x-character-count"))
