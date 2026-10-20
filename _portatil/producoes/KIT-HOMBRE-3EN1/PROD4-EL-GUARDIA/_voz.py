# -*- coding: utf-8 -*-
"""Narrações TTS (voz Diego) + trilha. Uso: python _voz.py tts | musica | sts <entrada> <saida>"""
import sys, json, base64, requests
from pathlib import Path
from dotenv import dotenv_values

P = Path(__file__).parent
AU = P / "audio"; AU.mkdir(exist_ok=True)
K = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
H = {"xi-api-key": K}
VOZ = "Iq9IDbsAh0XiIAKtSuSg"  # Diego
FALAS = {
    "L4_oferta": "Tres perfumes árabes al precio de uno.",
    "L5_dia": "En el día, Armaf Club. Fresco, masculino y poderoso. Ya no vigilo yo, me vigilan a mí.",
    "L6_noche": "En la noche, Lattafa Asad. Intenso y seductor. Mi señora me pide turno de noche… en la casa.",
    "L7_finde": "Y el fin de semana, Afnan Nine PM. Elegante y moderno.",
    "L8_cta": "Los tres te llegan a la casa y pagas cuando los recibes. ¡Pídelo ahora!",
}


def tts(so=None):
    for nome, txt in FALAS.items():
        if so and nome not in so:
            continue
        r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}/with-timestamps", headers=H,
                          json={"text": txt, "model_id": "eleven_multilingual_v2", "language_code": "es",
                                "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True}})
        r.raise_for_status(); d = r.json()
        (AU / f"{nome}.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
        json.dump(d["alignment"], open(AU / f"{nome}.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
        print(nome, "ok", round(d["alignment"]["character_end_times_seconds"][-1], 2), "s")


def musica():
    r = requests.post("https://api.elevenlabs.io/v1/music", headers=H, json={
        "prompt": "Upbeat Chilean cumbia instrumental, festive neighborhood party vibe, guiro, congas, accordion-like synth, "
                  "warm bass, playful and cheeky, steady energy, no vocals",
        "music_length_ms": 40000, "force_instrumental": True})
    r.raise_for_status(); (AU / "trilha.mp3").write_bytes(r.content); print("trilha ok", len(r.content))


def sts(ent, sai):
    iso = AU / "v_iso.mp3"
    with open(ent, "rb") as f:
        r = requests.post("https://api.elevenlabs.io/v1/audio-isolation", headers=H, files={"audio": f})
    r.raise_for_status(); iso.write_bytes(r.content)
    with open(iso, "rb") as f:
        r = requests.post(f"https://api.elevenlabs.io/v1/speech-to-speech/{VOZ}", headers=H, files={"audio": f},
                          data={"model_id": "eleven_multilingual_sts_v2", "remove_background_noise": "true",
                                "voice_settings": json.dumps({"stability": 0.5, "similarity_boost": 0.85})})
    r.raise_for_status(); Path(sai).write_bytes(r.content); print("sts ok", sai)


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "tts": tts(sys.argv[2:] or None)
    elif c == "musica": musica()
    elif c == "sts": sts(sys.argv[2], sys.argv[3])
