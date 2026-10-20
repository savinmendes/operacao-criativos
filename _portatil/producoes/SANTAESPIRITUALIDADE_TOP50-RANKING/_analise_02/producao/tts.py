# -*- coding: utf-8 -*-
"""Vozes do Ranking 02 (roteiro v1, palavra por palavra). 1 chamada por linha, com alinhamento.
Rodar com cwd = kit-edicao-criativos. uso: python <este>.py [ids...]"""
import base64, json, sys
from pathlib import Path
import requests
sys.path.insert(0, "ferramentas")
import tts_elevenlabs as T
P = Path(__file__).resolve().parent; OUT = P / "tts"; OUT.mkdir(exist_ok=True)
JEFE, MUJ, JM = "JjHBC66wF58p4ogebCNA", "cIBxLwfshLYhRB9lCXEg", "BskzYZ6zvapoZ3mBu93C"
S_JEFE = dict(stability=0.0, similarity_boost=0.8, style=0.0, use_speaker_boost=True)      # v3: stability 0 = Creative
S_MUJ = dict(stability=0.45, similarity_boost=0.8, style=0.35, use_speaker_boost=True, speed=1.0)
S_MUJ_F = dict(stability=0.40, similarity_boost=0.8, style=0.55, use_speaker_boost=True, speed=1.02)
S_JM = dict(stability=0.30, similarity_boost=0.8, style=0.55, use_speaker_boost=True, speed=1.05)
LINHAS = {
 "P1": (JEFE, S_JEFE, "eleven_v3", "[furious] [shouting] ¡Tú nunca vas a ser nadie en la vida! ¡Solo sobrevives porque yo te pago! ¡Estás despedida! ¡Lárgate de mi tienda!"),
 "M3": (MUJ, S_MUJ, "eleven_multilingual_v2", "Sí, esto me pasó a mí. Pero no se enojen, porque ese mismo día aprendí la oración de San Benito."),
 "M4": (MUJ, S_MUJ_F, "eleven_multilingual_v2", "Pocos días después me llamaron para el trabajo de mis sueños… y mi antiguo jefe terminó en la quiebra."),
 "M5": (MUJ, S_MUJ, "eleven_multilingual_v2", "La aprendí con el padre Juan Méndez, en la transmisión en vivo que intentaron borrar de internet."),
 "J06": (JM, S_JM, "eleven_multilingual_v2", "Solo existe una oración capaz de abrir los caminos así de rápido. Y yo no voy a dejar de enseñarla."),
 "J07": (JM, S_JM, "eleven_multilingual_v2", "Repitan conmigo: Oh poderoso San Benito, guardián de los arcanos sagrados, que venciste a las serpientes con la señal de la cruz…"),
 "J08": (JM, S_JM, "eleven_multilingual_v2", "¡Alto! El resto no lo puedo decir aquí. La última vez que la enseñé, me silenciaron."),
 "J09": (JM, S_JM, "eleven_multilingual_v2", "Esta oración estuvo escondida por novecientos años. Solo la élite religiosa la conocía."),
 "J10": (JM, S_JM, "eleven_multilingual_v2", "La última vez que la recé en vivo, recibimos cientos de mensajes al día siguiente, todos contando bendiciones."),
 "J11": (JM, S_JM, "eleven_multilingual_v2", "Pero atención: tiene una forma correcta de hacerla y de escucharla."),
 "J12": (JM, S_JM, "eleven_multilingual_v2", "Por eso la estoy rezando completa, en vivo, paso a paso. Y a quien te humilló, Dios le responde."),
 "J13": (JM, S_JM, "eleven_multilingual_v2", "Vuelve en siete días y cuéntame qué pasó. Envía este video a quien amas. Toca en «Ver más», aquí abajo, y entra a rezar conmigo."),
}
ORD = list(LINHAS)
ids = sys.argv[1:] or ORD
for k in ids:
    voz, st, mod, tx = LINHAS[k]; i = ORD.index(k)
    viz = lambda j: LINHAS[ORD[j]][3] if 0 <= j < len(ORD) and LINHAS[ORD[j]][0] == voz else None
    body = {"text": tx, "model_id": mod, "language_code": "es", "voice_settings": st}
    if mod != "eleven_v3": body.update(previous_text=viz(i - 1), next_text=viz(i + 1))
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voz}/with-timestamps", params={"output_format": "mp3_44100_128"},
                      headers={"xi-api-key": T.chave(), "Content-Type": "application/json"}, json=body, timeout=300)
    if r.status_code != 200: raise SystemExit(f"ElevenLabs {k} {r.status_code}: {r.text[:300]}")
    d = r.json()
    (OUT / f"{k}.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
    (OUT / f"{k}.alinhamento.json").write_text(json.dumps(d.get("alignment"), ensure_ascii=False), encoding="utf-8")
    with open(OUT / "caracteres.log", "a", encoding="utf-8") as f: f.write(f"{k}\t{len(tx)}\n")
    print("ok", k, len(tx))
