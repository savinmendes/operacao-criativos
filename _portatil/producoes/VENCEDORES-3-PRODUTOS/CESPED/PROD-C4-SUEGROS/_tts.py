# -*- coding: utf-8 -*-
import os, json, base64, sys, requests
from pathlib import Path
from dotenv import dotenv_values
K = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
KEY = K.get("ELEVENLABS_API_KEY") or K.get("ELEVEN_API_KEY") or [v for k, v in K.items() if "ELEVEN" in k.upper()][0]
VOZ = "NDcVpQJv7Naa7ZKrqtEk"
AU = Path(__file__).parent / "audio"; AU.mkdir(exist_ok=True)
H = {"xi-api-key": KEY}
LINHAS = {
    "L3_probe": "Hasta que probé esta.",
    "L4_mecanismo": "Es cortapasto, orilladora y bordeadora en uno. Tiene ruedas, así que la usas con una sola mano. Cuchilla de metal reforzada: olvídate de los hilos que se cortan. Y es inalámbrica, con dos baterías.",
    "L6_cta": "Despacho gratis a todo Chile, pagas al recibir y tienes noventa días de garantía. Toca el botón y pídela.",
}
for nome, txt in LINHAS.items():
    if len(sys.argv) > 1 and nome not in sys.argv[1:]:
        continue
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}/with-timestamps", headers=H,
                      json={"text": txt, "model_id": "eleven_multilingual_v2", "language_code": "es",
                            "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.3, "use_speaker_boost": True, "speed": 1.15}})
    r.raise_for_status(); d = r.json()
    (AU / f"{nome}.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
    json.dump(d["alignment"], open(AU / f"{nome}.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
    print(nome, "ok", d["alignment"]["character_end_times_seconds"][-1], "chars", len(txt))
