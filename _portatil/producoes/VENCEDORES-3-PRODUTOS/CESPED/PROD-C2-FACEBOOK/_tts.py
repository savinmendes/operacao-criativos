import json, base64, requests
from dotenv import dotenv_values
key = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
VOZ = "JjHBC66wF58p4ogebCNA"
L = {
     "L4_mecanismo": "Es cortapasto, orilladora y bordeadora en uno. Tiene ruedas, así que la usas con una sola mano. Cuchilla de metal reforzada: olvídate de los hilos que se cortan. Y es inalámbrica, con dos baterías.",
     "L6_cta": "Despacho gratis a todo Chile, pagas al recibir y tienes noventa días de garantía. Toca el botón y pídela."}
tot = 0
for n, t in L.items():
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}/with-timestamps", headers={"xi-api-key": key},
        json={"text": t, "model_id": "eleven_multilingual_v2", "language_code": "es",
              "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.3, "use_speaker_boost": True, "speed": 1.15}}, timeout=120)
    r.raise_for_status(); d = r.json()
    open(f"audio/{n}.mp3", "wb").write(base64.b64decode(d["audio_base64"]))
    json.dump(d["alignment"], open(f"audio/{n}.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
    tot += len(t); print(n, round(d["alignment"]["character_end_times_seconds"][-1], 2), r.headers.get("character-cost"))
print("chars", tot)
