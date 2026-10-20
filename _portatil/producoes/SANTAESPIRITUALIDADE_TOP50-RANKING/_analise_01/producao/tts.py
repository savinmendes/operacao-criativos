# -*- coding: utf-8 -*-
"""Vozes do Ranking 01 (roteiro v1, palavra por palavra). 1 chamada por linha, com alinhamento.
Rodar com cwd = kit-edicao-criativos. uso: python tts.py [ids...]"""
import base64, json, sys
from pathlib import Path
import requests
sys.path.insert(0, "ferramentas")
import tts_elevenlabs as T
P = Path(__file__).resolve().parent; OUT = P / "tts"; OUT.mkdir(exist_ok=True)
REP, DUE, JM = "ODO4sbmD3pTjhgRVVRP6", "N2HSRirbsHTZ8DE2WqjB", "BskzYZ6zvapoZ3mBu93C"
S_REP = dict(stability=0.45, similarity_boost=0.8, style=0.45, use_speaker_boost=True, speed=1.05)
S_DUE = dict(stability=0.45, similarity_boost=0.8, style=0.45, use_speaker_boost=True, speed=1.1)
S_JM = dict(stability=0.30, similarity_boost=0.8, style=0.55, use_speaker_boost=True, speed=1.05)
LINHAS = {
 "R1": (REP, S_REP, "¿Vieron lo que acaba de pasar en este restaurante? ¡Nadie lo puede explicar!"),
 "D1": (DUE, S_DUE, "No lo van a creer. Pasé seis meses casi sin clientes… ya iba a cerrar."),
 "D2": (DUE, S_DUE, "Recé la oración de San Benito y minutos después mi restaurante se llenó. La aprendí con el padre Juan Méndez, en una transmisión en vivo."),
 "J04": (JM, S_JM, "Presten mucha atención, porque esta oración puede cambiar su vida. Cada vez que la enseño, intentan tumbar la transmisión y decir que es mentira. No quieren que nuestra gente prospere."),
 "J05": (JM, S_JM, "Pero los testimonios que llegan todos los días no mienten. Y yo no voy a dejar de enseñarla."),
 "J06": (JM, S_JM, "Repitan conmigo: Oh poderoso San Benito, guardián de los arcanos sagrados, que venciste a las serpientes con la señal de la cruz…"),
 "J07": (JM, S_JM, "¡Alto! El resto no lo puedo decir aquí. Ya me borraron la transmisión por enseñarla."),
 "J08": (JM, S_JM, "Esta oración estuvo escondida por novecientos años. Solo los más poderosos la conocían. Y tiene una forma correcta de hacerla y de escucharla."),
 "J09": (JM, S_JM, "Muchos me preguntan: padre, ¿Dios quiere que prosperemos? ¡Claro que sí! La falta de dinero es lo que más divide a las familias."),
 "J10": (JM, S_JM, "Lo dice el Salmo ciento doce: «Riqueza y abundancia habrá en su casa, y su justicia permanece para siempre.»"),
 "J11": (JM, S_JM, "Por eso la estoy rezando completa, en vivo, paso a paso. A partir de hoy, despídete de las deudas. Vuelve en siete días y cuéntame qué pasó."),
 "J12": (JM, S_JM, "Envía este video a quien amas. Toca en «Ver más», aquí abajo, y entra a rezar conmigo."),
 # v3 / ganchos
 "JN": (JM, S_JM, "Imagina pagar la última cuota y dormir tranquilo otra vez."),
 "JG1": (JM, S_JM, "Mira lo que le pasó a este hombre."),
 "G2": (REP, S_REP, "Hace una hora este restaurante estaba vacío."),
 "G3": (REP, S_REP, "Intentaron borrar este video tres veces."),
 "G4": (REP, S_REP, "Si tienes un negocio y pasas el día mirando la puerta esperando clientes…"),
 "G5": (DUE, S_DUE, "Esa noche conté las monedas de la caja tres veces… y no alcanzaba ni para la luz."),
}
ORD = list(LINHAS)
ids = sys.argv[1:] or ORD
for k in ids:
    voz, st, tx = LINHAS[k]; i = ORD.index(k)
    viz = lambda j: LINHAS[ORD[j]][2] if 0 <= j < len(ORD) and LINHAS[ORD[j]][0] == voz else None
    body = {"text": tx, "model_id": "eleven_multilingual_v2", "language_code": "es",
            "previous_text": viz(i - 1), "next_text": viz(i + 1), "voice_settings": st}
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voz}/with-timestamps", params={"output_format": "mp3_44100_128"},
                      headers={"xi-api-key": T.chave(), "Content-Type": "application/json"}, json=body, timeout=300)
    if r.status_code != 200: raise SystemExit(f"ElevenLabs {r.status_code}: {r.text[:300]}")
    d = r.json()
    (OUT / f"{k}.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
    (OUT / f"{k}.alinhamento.json").write_text(json.dumps(d.get("alignment"), ensure_ascii=False), encoding="utf-8")
    with open(OUT / "caracteres.log", "a", encoding="utf-8") as f: f.write(f"{k}\t{len(tx)}\n")
    print("ok", k, len(tx))
