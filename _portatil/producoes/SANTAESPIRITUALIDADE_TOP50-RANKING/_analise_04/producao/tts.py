# -*- coding: utf-8 -*-
"""Vozes do Ranking 04 (roteiro v1, palavra por palavra). 1 chamada por linha, com alinhamento.
Rodar com cwd = kit-edicao-criativos. uso: python <este>.py [ids...]"""
import base64, json, sys
from pathlib import Path
import requests
sys.path.insert(0, "ferramentas")
import tts_elevenlabs as T
P = Path(__file__).resolve().parent; OUT = P / "tts"; OUT.mkdir(exist_ok=True)
APR, SEN, JM = "7nCYbNPCi8RLAKVnYEoO", "wfTWLJ20rcMqvU8gIiAB", "BskzYZ6zvapoZ3mBu93C"
S_APR = dict(stability=0.35, similarity_boost=0.8, style=0.55, use_speaker_boost=True, speed=1.05)
S_SEN = dict(stability=0.45, similarity_boost=0.8, style=0.35, use_speaker_boost=True, speed=1.0)
S_JM = dict(stability=0.30, similarity_boost=0.8, style=0.55, use_speaker_boost=True, speed=1.05)
V2 = "eleven_multilingual_v2"
LINHAS = {
 "A01": (APR, S_APR, "¡El mundo entero tiene que escuchar lo que este padre acaba de revelar!"),
 "J02": (JM, S_JM, "Cuando te caiga el sueldo, no gastes ni un centavo antes de hacer esta oración. Y vas a ver tu dinero multiplicarse."),
 "J03": (JM, S_JM, "Te la voy a enseñar ahora, antes de que me callen."),
 "J04": (JM, S_JM, "Presta mucha atención, porque puede cambiar tu vida para siempre."),
 "J05": (JM, S_JM, "Es una oración antigua de San Benito, escondida durante siglos. Y tiene una forma correcta de hacerse."),
 "J06": (JM, S_JM, "Repite conmigo: Oh poderoso San Benito, guardián de los arcanos sagrados, que venciste a las serpientes con la señal de la cruz…"),
 "J07": (JM, S_JM, "¡Alto! El resto no lo puedo decir aquí. La última vez que la enseñé completa, me borraron la transmisión."),
 "J08": (JM, S_JM, "Miles de personas ya me escribieron: salieron de las deudas después de hacerla."),
 "J09": (JM, S_JM, "Pero solo funciona si la haces de la forma correcta. No es una oración cualquiera."),
 "J10": (JM, S_JM, "Y antes de que me pregunten: ¿Dios quiere que prosperes? ¡Sí! Con prosperidad tu familia deja de vivir angustiada y puedes ayudar al prójimo."),
 "J11": (JM, S_JM, "Miren lo que me contó un hermano de la parroquia."),
 "S12": (SEN, S_SEN, "No es exageración, no. Empecé a hacer esta oración todos los días… y desde entonces todo cambió. Llegó la paz, llegó el dinero. Pero lo más importante fue lo que cambió por dentro."),
 "J13": (JM, S_JM, "Mucha gente no creyó. Pero quien la hizo, cambió de vida."),
 "J14": (JM, S_JM, "Por eso la estoy rezando completa, en vivo, paso a paso. Vuelve en siete días y cuéntame qué bendiciones llegaron."),
 "J15": (JM, S_JM, "Envía este video a quien amas. Toca en «Ver más», aquí abajo, y entra a rezar conmigo."),
}
ORD = list(LINHAS)
if __name__ == "__main__":
    ids = sys.argv[1:] or ORD
    for k in ids:
        voz, st, tx = LINHAS[k]; i = ORD.index(k)
        viz = lambda j: LINHAS[ORD[j]][2] if 0 <= j < len(ORD) and LINHAS[ORD[j]][0] == voz else None
        body = {"text": tx, "model_id": V2, "language_code": "es", "voice_settings": st, "previous_text": viz(i - 1), "next_text": viz(i + 1)}
        r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voz}/with-timestamps", params={"output_format": "mp3_44100_128"},
                          headers={"xi-api-key": T.chave(), "Content-Type": "application/json"}, json=body, timeout=300)
        if r.status_code != 200: raise SystemExit(f"ElevenLabs {k} {r.status_code}: {r.text[:300]}")
        d = r.json()
        (OUT / f"{k}.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
        (OUT / f"{k}.alinhamento.json").write_text(json.dumps(d.get("alignment"), ensure_ascii=False), encoding="utf-8")
        with open(OUT / "caracteres.log", "a", encoding="utf-8") as f: f.write(f"{k}\t{len(tx)}\n")
        print("ok", k, len(tx))
