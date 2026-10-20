# -*- coding: utf-8 -*-
"""Vozes do Ranking 03 (roteiro v1, palavra por palavra). 1 chamada por linha, com alinhamento.
Rodar com cwd = kit-edicao-criativos. uso: python <este>.py [ids...]"""
import base64, json, sys
from pathlib import Path
import requests
sys.path.insert(0, "ferramentas")
import tts_elevenlabs as T
P = Path(__file__).resolve().parent; OUT = P / "tts"; OUT.mkdir(exist_ok=True)
MUJ, JM = "hHjbwzYZW17oh0p05AKv", "BskzYZ6zvapoZ3mBu93C"     # Gabriela (nova, ≠ Carolina do R02) / clone Juan
S_MUJ = dict(stability=0.40, similarity_boost=0.8, style=0.50, use_speaker_boost=True, speed=1.0)
S_MUJ_F = dict(stability=0.40, similarity_boost=0.8, style=0.60, use_speaker_boost=True, speed=1.02)
S_JM = dict(stability=0.30, similarity_boost=0.8, style=0.55, use_speaker_boost=True, speed=1.05)
LINHAS = {
 "W1": (MUJ, S_MUJ, "¡Miren el abuso que me hicieron!"),
 "W2": (MUJ, S_MUJ, "Mi jefe me humilló delante de todos y me echó como si yo no valiera nada."),
 "W3": (MUJ, S_MUJ, "Ese mismo día recé la oración de San Benito con toda mi fe… llorando."),
 "W4": (MUJ, S_MUJ_F, "Y minutos después me llamaron con una oferta de trabajo… ¡para ganar ocho veces más!"),
 "W5": (MUJ, S_MUJ_F, "La aprendí con el padre Juan Méndez, en una transmisión en vivo. Aquí les dejo lo que intentaron borrar."),
 "J06": (JM, S_JM, "Están intentando callarme. Pero no voy a dejar de enseñarles."),
 "J07": (JM, S_JM, "Presten mucha atención, porque puede ser la última vez que hable de esto en público. Ya me tumbaron la transmisión por ayudar a la gente."),
 "J08": (JM, S_JM, "Repitan conmigo: Oh poderoso San Benito, guardián de los arcanos sagrados, que venciste a las serpientes con la señal de la cruz…"),
 "J09": (JM, S_JM, "¡Alto! El resto no lo puedo decir aquí."),
 "J10": (JM, S_JM, "La última vez que la enseñé completa, al día siguiente me llegaron miles de mensajes: milagros, deudas pagadas, puertas abiertas."),
 "J11": (JM, S_JM, "Pero tiene una forma correcta de hacerla. No es una oración cualquiera."),
 "J12": (JM, S_JM, "Muchos me preguntan: padre, ¿Dios quiere que prosperemos? ¡Claro que sí! La prosperidad te libra de la angustia y te deja tiempo para tu familia y para hacer el bien."),
 "J13": (JM, S_JM, "Lo dice Deuteronomio ocho, dieciocho: «Acuérdate del Señor tu Dios, porque es él quien te da la fuerza para crear riqueza»."),
 "J14": (JM, S_JM, "Por eso la estoy rezando completa, en vivo, paso a paso. A partir de hoy, despídete de las deudas. Vuelve en siete días y cuéntame qué pasó."),
 "J15": (JM, S_JM, "Envía este video a quien amas. Toca en «Ver más», aquí abajo, y entra a rezar conmigo."),
}
ORD = list(LINHAS)
ids = sys.argv[1:] or ORD
for k in ids:
    voz, st, tx = LINHAS[k]; i = ORD.index(k)
    viz = lambda j: LINHAS[ORD[j]][2] if 0 <= j < len(ORD) and LINHAS[ORD[j]][0] == voz else None
    body = {"text": tx, "model_id": "eleven_multilingual_v2", "language_code": "es", "voice_settings": st,
            "previous_text": viz(i - 1), "next_text": viz(i + 1)}
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voz}/with-timestamps", params={"output_format": "mp3_44100_128"},
                      headers={"xi-api-key": T.chave(), "Content-Type": "application/json"}, json=body, timeout=300)
    if r.status_code != 200: raise SystemExit(f"ElevenLabs {k} {r.status_code}: {r.text[:300]}")
    d = r.json()
    (OUT / f"{k}.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
    (OUT / f"{k}.alinhamento.json").write_text(json.dumps(d.get("alignment"), ensure_ascii=False), encoding="utf-8")
    with open(OUT / "caracteres.log", "a", encoding="utf-8") as f: f.write(f"{k}\t{len(tx)}\n")
    print("ok", k, len(tx))
