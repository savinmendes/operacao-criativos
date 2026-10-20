# -*- coding: utf-8 -*-
"""Voz Juan Méndez (clone BskzYZ6zvapoZ3mBu93C, eleven_multilingual_v2), 1 chamada por linha do roteiro v2, com alinhamento.
Rodar com cwd = kit-edicao-criativos. uso: python tts.py [ids...]"""
import base64, json, sys
from pathlib import Path
import requests
sys.path.insert(0, "ferramentas")
import tts_elevenlabs as T
P = Path(__file__).resolve().parent; OUT = P / "tts"; OUT.mkdir(exist_ok=True)
VOZ = "BskzYZ6zvapoZ3mBu93C"
LINHAS = [
 "¡Detente! Si este video llegó a ti, no fue por casualidad.",
 "Esta es la oración a San Benito que escondieron de ti durante novecientos años.",
 "La escondieron porque quien la reza de la forma correcta rompe cualquier atadura: deudas, envidia, puertas cerradas.",
 "Tú rezas, trabajas, haces todo bien… y aun así el dinero se va, la familia pelea y nada avanza.",
 "Eso no es falta de fe. Es un camino bloqueado.",
 "Repite conmigo, ahora mismo:",
 "Oh poderoso San Benito, guardián de los arcanos sagrados, que venciste a las serpientes con la señal de la cruz y callaste el rugido de los abismos con tu fe inquebrantable…",
 "¡Alto! Lo que viene después no lo puedo decir aquí. Ya me borraron videos por enseñarla.",
 "La última vez que la recé en vivo, más de seiscientas noventa y siete personas me escribieron al día siguiente contando bendiciones. Todavía no termino de leer los mensajes.",
 "Pero escucha bien: si la rezas de la forma equivocada, no funciona. Tiene una manera correcta de hacerla y de escucharla.",
 "Por eso, en este momento, la estoy rezando completa, en vivo, paso a paso, con miles de familias.",
 "Envía este video a quien amas, antes de que lo borren otra vez.",
 "Toca en «Ver más», aquí abajo, y entra a rezar conmigo. Tu bendición empieza hoy.",
]
EST, STY, SPD = 0.30, 0.55, 1.05
ids = [int(x) for x in sys.argv[1:]] or range(1, len(LINHAS) + 1)
for i in ids:
    tx = LINHAS[i - 1]
    body = {"text": tx, "model_id": "eleven_multilingual_v2", "language_code": "es",
            "previous_text": LINHAS[i - 2] if i > 1 else None, "next_text": LINHAS[i] if i < len(LINHAS) else None,
            "voice_settings": {"stability": EST, "similarity_boost": 0.8, "style": STY, "use_speaker_boost": True, "speed": SPD}}
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}/with-timestamps", params={"output_format": "mp3_44100_128"},
                      headers={"xi-api-key": T.chave(), "Content-Type": "application/json"}, json=body, timeout=300)
    if r.status_code != 200: raise SystemExit(f"ElevenLabs {r.status_code}: {r.text[:300]}")
    d = r.json()
    (OUT / f"L{i:02d}.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
    (OUT / f"L{i:02d}.alinhamento.json").write_text(json.dumps(d.get("alignment"), ensure_ascii=False), encoding="utf-8")
    with open(OUT / "caracteres.log", "a", encoding="utf-8") as f: f.write(f"L{i:02d}\t{len(tx)}\n")
    print("ok", i, len(tx))
